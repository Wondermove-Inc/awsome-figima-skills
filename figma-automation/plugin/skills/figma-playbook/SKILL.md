---
name: figma-playbook
description: Manage Figma workflow memory stores. Use when reading or writing project, library, or global playbook memory through the atomic apply script.
---

# /figma-playbook — Progressive Memory Management

Manage the Figma workflow memory system. It has three stores:

- global: `.codex/figma-playbook-memory/`
- library: `design-system/<library-slug>/memory/`
- project: `design-system/<project-slug>/memory/`

All writes go through `scripts/apply.py`; never hand-edit `MEMORY.md` or topic files. Use a
human-readable library family slug such as `material-design`, never a Figma file key. The file keys live
in `project.json` and are used only for Figma API calls.

Read `references/contracts.md` when you need exact store layout, proposal JSON, `learn` procedure,
`reflect` procedure, or consolidation rules.

## Commands

### `load --library <slug> [--project <slug>]`

Load memory indexes only:

1. Read `design-system/<slug>/memory/MEMORY.md`.
2. If `--project` is given, read `design-system/<project-slug>/memory/MEMORY.md`.
3. Read `.codex/figma-playbook-memory/MEMORY.md`.
4. Return the three indexes as context to the caller.

Do not load all topic files up front. The index line is the relevance filter; builders and reviewers
open matching topic files only when they hit that element type or decision point.

On a memory miss, check live Figma (`fetch_library_catalog`, `get_node`, or `save_screenshots`). If a
convention is found, apply it and create a tentative proposal JSON for `apply`.

### `learn --library <slug>`

Bootstrap or refresh library pattern memory by analyzing the library's own documentation/example
screens. Run it once for a new library or when memory is sparse. Follow
`references/contracts.md#learn-procedure`.

Write proposals to `design-system/_build-cache/learn-proposals-<slug>.json`, then call `apply`. If no
composed frames are found, write nothing and do not fabricate patterns.

### `apply <proposals.json>`

Commit proposals to memory stores:

`python scripts/apply.py <proposals.json>` or `python scripts/apply.py <proposals.json> --dry-run`

Use the schema in `references/contracts.md#proposal-json`. Report applied / skipped / errors. On any
error, surface it before proceeding.

### `list [--library <slug>] [--project <slug>] [--type <type>]`

Print relevant `MEMORY.md` entries. If `--type` is given, filter entries whose filename starts with
`<type>_`.

### `migrate <file> --format recipes-json`

Convert a `component-recipes.json` file to proposal JSON, then call `apply`. Use
`references/contracts.md#migration-mapping` for routing rules.

### `init --global | --library <slug> | --project <slug>`

Create an empty memory store and write a `MEMORY.md` header. Use the exact paths and header in
`references/contracts.md#store-layout`.

### `consolidate [--library <slug>] [--project <slug>]`

Run post-session cleanup after all screens pass. Deduplicate, merge obvious siblings, flag
contradictions, repair orphaned index entries, and flag stale references. Use a fast model for
mechanical checks and a less advanced / Sonnet-tier model for mergeable-sibling judgment; do not use an
advanced / Opus-tier model for this cleanup pass. Follow `references/contracts.md#consolidation`.

### `reflect --ai-screen <node-id> --human-screen <node-id> --library <slug> [--project <slug>] [--screen-id <id>] [--annotations <frame-id>] [--channel <channel>]`

Learn from a human-corrected screen. Capture both frames, diff structure and craft deltas, classify root
causes, generate proposals, and apply them. Human corrections are high-confidence entries with
`discoveredVia: "human-correction"`. Follow `references/contracts.md#reflect-procedure`.

## Permissions

| Actor | Allowed commands |
|---|---|
| Builder | `load` only |
| Reviewer | `load`, `learn` when memory is empty or a D7 pattern violation needs evidence |
| Orchestrator | `load`, `apply`, `init`, `consolidate`, `reflect` |
| Human | all commands |

## Constraint

Skills determine what to record as proposal JSON. `scripts/apply.py` determines how it is written
atomically. This keeps concurrent memory writes auditable and prevents store corruption.
