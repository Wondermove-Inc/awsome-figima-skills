#!/usr/bin/env python3
"""Validate COPY.md: frontmatter schema + per-screen coverage + placeholder scan.

Usage:
    python check_copy.py <path/to/COPY.md> --screens "login,dashboard,settings"

Exit code 0 = pass. Non-zero = fail, with the reasons printed to stderr.

Dependencies: prefers PyYAML for frontmatter parsing; falls back to a minimal parser that
handles the flat `voice:`/`tone:`/`screens:` keys and the screen-id keys we need for coverage.
The schema check here is intentionally lightweight (required keys + types + coverage) — it mirrors
assets/copy-md.schema.json without requiring the `jsonschema` package.
"""
import argparse
import re
import sys

# Note: bare "placeholder" is intentionally NOT here — `placeholder:` is a legitimate input-field
# key in the screens map. We only flag obvious filler text.
PLACEHOLDER_PATTERNS = [
    r"\blorem\b", r"\bipsum\b", r"\bTODO\b", r"\bFIXME\b",
    r"placeholder text", r"your text here", r"\bswap it\b",
]


def read_frontmatter(text):
    """Return (frontmatter_str, ok). Frontmatter is between the first two '---' lines."""
    if not text.startswith("---"):
        return "", False
    parts = text.split("\n")
    if parts[0].strip() != "---":
        return "", False
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        return "", False
    return "\n".join(parts[1:end]), True


def parse_yaml(fm):
    try:
        import yaml  # type: ignore
        return yaml.safe_load(fm), None
    except ImportError:
        pass
    except Exception as e:  # malformed YAML
        return None, f"frontmatter is not valid YAML: {e}"
    # Minimal fallback: top-level keys + first-level screen ids (enough for coverage).
    data = {}
    cur_top = None
    screens = {}
    in_screens = False
    for line in fm.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        m = re.match(r"^(\s*)([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        key = m.group(2)
        val = m.group(3).strip()
        if indent == 0:
            cur_top = key
            in_screens = key == "screens"
            if val:
                data[key] = val.strip('"').strip("'")
            elif not in_screens:
                data[key] = {}
        elif in_screens and indent == 2:
            screens[key] = True  # presence is enough for coverage in fallback mode
    if screens:
        data["screens"] = screens
    return data, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--screens", default="", help="comma-separated confirmed screen ids")
    args = ap.parse_args()

    errors = []
    try:
        with open(args.path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"FAIL: cannot read {args.path}: {e}", file=sys.stderr)
        return 2

    fm, ok = read_frontmatter(text)
    if not ok:
        print("FAIL: COPY.md has no '---' YAML frontmatter block", file=sys.stderr)
        return 2

    data, perr = parse_yaml(fm)
    if perr:
        print(f"FAIL: {perr}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("FAIL: frontmatter did not parse to a mapping", file=sys.stderr)
        return 2

    # Required keys + types (mirrors copy-md.schema.json).
    if not isinstance(data.get("voice"), str) or not data.get("voice", "").strip():
        errors.append("`voice` must be a non-empty string")
    tone = data.get("tone")
    if not isinstance(tone, dict) or not tone:
        errors.append("`tone` must be a non-empty mapping of context -> string")
    screens = data.get("screens")
    if not isinstance(screens, dict) or not screens:
        errors.append("`screens` must be a non-empty mapping of screenId -> strings")
        screens = {}

    # Coverage: every confirmed screen id present and non-empty.
    wanted = [s.strip() for s in args.screens.split(",") if s.strip()]
    for sid in wanted:
        if sid not in screens:
            errors.append(f"screen `{sid}` is missing from the `screens` map")
        else:
            entry = screens[sid]
            if entry in (None, "", {}, []):
                errors.append(f"screen `{sid}` has an empty copy entry")

    # Placeholder leakage scan (whole file).
    low = text.lower()
    for pat in PLACEHOLDER_PATTERNS:
        m = re.search(pat, low)
        if m:
            errors.append(f"placeholder text detected: '{m.group(0)}'")

    if errors:
        print("FAIL: COPY.md validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"PASS: COPY.md valid; {len(wanted) or len(screens)} screen(s) covered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
