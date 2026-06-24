#!/usr/bin/env python3
"""
apply.py — sole atomic writer to all figma-automation playbook stores.

Usage:
  python "${SKILL_DIR:-${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-playbook}/scripts/apply.py" <proposals.json> [--dry-run]

Store resolution:
  global              → .claude/memory/
  library <slug>      → design-system/<slug>/memory/   (e.g. "hae-dl")
  project <slug>      → design-system/<slug>/memory/   (e.g. "ccs")

Proposal JSON schema: see /figma-playbook docs.
"""

import fcntl
import json
import os
import pathlib
import re
import sys

def _resolve_repo_root() -> pathlib.Path:
    """Locate the figma-automation repo root that owns the memory stores.

    The stores (`.claude/memory/`, `design-system/<slug>/memory/`) live in the
    user's repo checkout, NOT next to this script. Under Claude the local
    marketplace runs this file in-place inside the repo, but under Codex the
    skill is COPIED to ~/.codex/skills/, so a __file__-relative walk would
    resolve to the home dir and misdirect every write. Derive from the working
    directory (the repo the user is in) instead, with an explicit override.
    """
    override = os.environ.get("FIGMA_PLAYBOOK_REPO_ROOT")
    if override:
        return pathlib.Path(override).resolve()
    cwd = pathlib.Path.cwd().resolve()
    for parent in (cwd, *cwd.parents):
        if (parent / "design-system").is_dir() or (parent / ".git").exists():
            return parent
    # Last resort: original in-repo layout (plugin/skills/figma-playbook/scripts/).
    return pathlib.Path(__file__).resolve().parents[4]


REPO_ROOT = _resolve_repo_root()

VALID_ACTIONS  = {"create", "update", "delete"}
VALID_STORES   = {"global", "library", "project"}
VALID_TYPES    = {"pattern", "feedback", "reference", "preference", "judgment"}
VALID_STATUSES = {"confirmed", "tentative"}

_NAME_RE      = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]*$')
_STORE_KEY_RE = re.compile(r'^[a-z0-9][a-z0-9_-]*$')


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def store_dir(store: str, store_key: str | None) -> pathlib.Path:
    if store == "global":
        return REPO_ROOT / ".claude" / "memory"
    if store in ("library", "project"):
        if not store_key:
            raise ValueError(f"storeKey required for {store} store")
        resolved = (REPO_ROOT / "design-system" / store_key / "memory").resolve()
        allowed  = (REPO_ROOT / "design-system").resolve()
        if not str(resolved).startswith(str(allowed) + os.sep):
            raise ValueError(f"storeKey {store_key!r} escapes design-system directory")
        return resolved
    raise ValueError(f"Unknown store: {store!r}")


def topic_filename(entry_type: str, name: str) -> str:
    return f"{entry_type}_{name}.md"


# ---------------------------------------------------------------------------
# Content builders
# ---------------------------------------------------------------------------

def build_topic_file(proposal: dict) -> str:
    meta    = proposal.get("metadata", {})
    c_by    = meta.get("confirmedBy") or []
    stream  = meta.get("stream") or ""
    d_via   = meta.get("discoveredVia") or ""
    status  = meta.get("status") or "tentative"

    lines = [
        "---",
        f"name: {proposal['name']}",
        f"description: {proposal['description']}",
        "metadata:",
        f"  type: {proposal['type']}",
        f"  status: {status}",
    ]
    if c_by:
        lines.append(f"  confirmedBy: [{', '.join(str(x) for x in c_by)}]")
    if d_via:
        lines.append(f"  discoveredVia: {d_via}")
    if stream:
        lines.append(f"  stream: {stream}")
    lines.append("---")
    lines.append("")  # blank line after frontmatter

    body = proposal.get("body", "").strip()
    if body:
        lines.append(body)
        lines.append("")

    return "\n".join(lines)


def index_line(filename: str, name: str, description: str) -> str:
    # Truncate description to keep index entries concise
    desc = description[:140] if len(description) > 140 else description
    return f"- [{name}]({filename}) — {desc}\n"


# ---------------------------------------------------------------------------
# Index operations (flock-protected)
# ---------------------------------------------------------------------------

def _upsert_index(memory_md: pathlib.Path, filename: str, name: str, description: str) -> None:
    memory_md.parent.mkdir(parents=True, exist_ok=True)
    if not memory_md.exists():
        memory_md.write_text("# Memory Index\n\n", encoding="utf-8")

    with open(memory_md, "r+", encoding="utf-8") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            content = fh.read()
            lines   = content.splitlines(keepends=True)
            new_line = index_line(filename, name, description)

            # Replace existing entry (match by filename or name)
            updated = False
            for i, line in enumerate(lines):
                if f"]({filename})" in line or (f"[{name}](" in line and "—" in line):
                    lines[i] = new_line
                    updated = True
                    break

            if not updated:
                # Append before the trailing newline, if any
                if lines and lines[-1] == "\n":
                    lines.insert(-1, new_line)
                else:
                    lines.append(new_line)

            fh.seek(0)
            fh.truncate()
            fh.writelines(lines)
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _remove_from_index(memory_md: pathlib.Path, filename: str) -> None:
    if not memory_md.exists():
        return
    with open(memory_md, "r+", encoding="utf-8") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            lines = [l for l in fh.readlines() if f"]({filename})" not in l]
            fh.seek(0)
            fh.truncate()
            fh.writelines(lines)
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# Core: apply one proposal
# ---------------------------------------------------------------------------

def apply_proposal(proposal: dict, dry_run: bool) -> dict:
    action    = proposal["action"]
    store     = proposal["store"]
    store_key = proposal.get("storeKey")
    name      = proposal["name"]

    try:
        mem_dir = store_dir(store, store_key)
    except ValueError as exc:
        return {"name": name, "status": "error", "reason": str(exc)}

    entry_type = proposal["type"]
    description = proposal["description"]
    filename   = topic_filename(entry_type, name)
    topic_path = mem_dir / filename
    # Containment guard: resolved path must stay inside mem_dir
    if not str(topic_path.resolve()).startswith(str(mem_dir.resolve()) + os.sep):
        return {"name": name, "status": "error", "reason": "path escapes store dir"}
    memory_md  = mem_dir / "MEMORY.md"
    store_label = f"{store}/{store_key or 'global'}"

    if dry_run:
        print(f"  [dry-run] {action:6s} {store_label} → {filename}")
        return {"name": name, "status": "dry-run", "action": action}

    if not mem_dir.exists():
        return {
            "name": name,
            "status": "error",
            "reason": f"Store dir does not exist: {mem_dir}  (run: figma-playbook init)",
        }

    if action == "delete":
        if topic_path.exists():
            topic_path.unlink()
        _remove_from_index(memory_md, filename)
        return {"name": name, "status": "ok", "action": "delete"}

    # create / update — write topic file first, index last
    topic_path.write_text(build_topic_file(proposal), encoding="utf-8")
    _upsert_index(memory_md, filename, name, description)

    return {
        "name":   name,
        "status": "ok",
        "action": action,
        "file":   str(topic_path.relative_to(REPO_ROOT)),
    }


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_proposal(p: dict) -> list[str]:
    errors = []
    if p.get("action") not in VALID_ACTIONS:
        errors.append(f"invalid action {p.get('action')!r} (must be one of {VALID_ACTIONS})")
    if p.get("store") not in VALID_STORES:
        errors.append(f"invalid store {p.get('store')!r} (must be one of {VALID_STORES})")
    if p.get("store") in ("library", "project") and not p.get("storeKey"):
        errors.append("storeKey is required for library/project stores")
    store_key = p.get("storeKey") or ""
    if store_key and not _STORE_KEY_RE.match(store_key):
        errors.append(f"storeKey {store_key!r} must match ^[a-z0-9][a-z0-9_-]*$")
    if p.get("type") not in VALID_TYPES:
        errors.append(f"invalid type {p.get('type')!r} (must be one of {VALID_TYPES})")
    name = p.get("name") or ""
    if not name:
        errors.append("missing required field: 'name'")
    elif not _NAME_RE.match(name):
        errors.append(f"name {name!r} must match ^[A-Za-z0-9][A-Za-z0-9_-]*$")
    if not p.get("description"):
        errors.append("missing required field: 'description'")
    meta = p.get("metadata") or {}
    if meta.get("status") and meta["status"] not in VALID_STATUSES:
        errors.append(f"invalid status {meta['status']!r} (must be one of {VALID_STATUSES})")
    return errors


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    proposals_path = pathlib.Path(argv[0])
    dry_run        = "--dry-run" in argv

    if not proposals_path.exists():
        print(f"Error: proposals file not found: {proposals_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(proposals_path.read_text(encoding="utf-8"))
    proposals = data.get("proposals", [])

    if not proposals:
        print("No proposals to apply.")
        return

    prefix = "[DRY RUN] " if dry_run else ""
    print(f"{prefix}Applying {len(proposals)} proposal(s) from {proposals_path.name}")
    if data.get("screenId"):
        print(f"  Source: screenId={data['screenId']}")

    applied, errors = [], []

    for proposal in proposals:
        errs = validate_proposal(proposal)
        if errs:
            name = proposal.get("name", "?")
            for err in errs:
                print(f"  SKIP [{name}]: {err}")
            errors.append({"name": name, "errors": errs})
            continue

        result = apply_proposal(proposal, dry_run)
        if result["status"] in ("ok", "dry-run"):
            if not dry_run:
                print(f"  OK   [{result['action']:6s}] {result.get('file', result['name'])}")
            applied.append(result)
        else:
            print(f"  ERR  [{result['name']}]: {result.get('reason', 'unknown error')}")
            errors.append(result)

    print(f"\n{'[dry-run] ' if dry_run else ''}Done: {len(applied)} applied, {len(errors)} errors")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
