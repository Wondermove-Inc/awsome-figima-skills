# Figma Playbook Contracts

## Contents

- Store layout
- Topic format
- Proposal JSON
- Learn procedure
- Migration mapping
- Consolidation
- Reflect procedure

## Store Layout

Memory stores live in the user's repository checkout:

- global: `.codex/figma-playbook-memory/`
- library: `design-system/<library-slug>/memory/`
- project: `design-system/<project-slug>/memory/`

Each store has a `MEMORY.md` index and topic files named `<type>_<name>.md`.

Initial `MEMORY.md`:

```markdown
# Memory Index

<!-- format: - [name](type_name.md) — one-line hook under 150 chars -->
```

Use the library family slug, not Figma file keys. Example: all Material Design sub-libraries
(components, icons, tokens, patterns) use `storeKey: "material-design"`.

## Topic Format

```markdown
---
name: pattern-search-placement
description: Search bar belongs in PageHeader's built-in Search slot, not above tables
metadata:
  type: pattern | feedback | reference | preference | judgment
  status: confirmed | tentative
  confirmedBy: [C01, C02]
  discoveredVia: anatomy | misfit | library-sweep | human-correction
  stream: redesign-2026
---

**Rule / Fact**: One sentence.

**Why**: The reason this matters.

**How to apply**: When and where to use this.

**Exceptions**: Edge cases where it does not apply.
```

`MEMORY.md` index rules:

- One line per entry: `- [name](filename) — hook under 150 chars`
- Max about 200 lines; run `consolidate` when approaching the limit
- Only `scripts/apply.py` writes to `MEMORY.md`

## Proposal JSON

```json
{
  "screenId": "C01",
  "proposals": [
    {
      "action": "create | update | delete",
      "store": "library | project | global",
      "storeKey": "<library-slug or project-slug>",
      "type": "pattern | feedback | reference | preference | judgment",
      "name": "pattern-search-placement",
      "description": "one-line for MEMORY.md index",
      "body": "**Rule / Fact**: ...\n\n**Why**: ...\n\n**How to apply**: ...",
      "metadata": {
        "status": "confirmed | tentative",
        "confirmedBy": ["C01"],
        "discoveredVia": "anatomy | misfit | library-sweep",
        "stream": null
      }
    }
  ]
}
```

## Learn Procedure

Phase 1: Index candidate frames.

```text
get_pages(fileKey=<library-file-key>)
for each page:
  scan_nodes_by_types(pageId, types=["FRAME"])
  record { id, name, width, height, childCount }
write design-system/_build-cache/learn-index-<library-slug>.json
```

Phase 2: Filter composed frames worth analyzing:

- `childCount > 3`
- width at least 400px
- not a repeated component-set strip
- cap at 20 frames total, prioritizing larger and more screen-like frames

Phase 3: Analyze selected frames:

```text
save_screenshots([frameId], maxDimension: 2048)
get_node(frameId)
get_nodes_info([frameId, ...top-level-children])
scan_text_nodes(frameId)
```

Extract placement, grouping, spacing tokens, hierarchy, sizing, composition, and frame structure.
Patterns from a single frame are `status: tentative`, `discoveredVia: library-sweep`, and include
evidence from frame ids, screenshots, or node properties.

Write `design-system/_build-cache/learn-proposals-<library-slug>.json`, then call `apply`.

## Migration Mapping

For `component-recipes.json`:

- `evidence.note` containing `Library-agnostic` -> `store: "global"`, `type: "feedback"`
- entries with only `material_*` evidence keys -> `store: "library"`, `storeKey: "material-design"`
- navigation structure or component variant axes -> `type: "feedback"`
- layout placement conventions -> `type: "pattern"`
- component keys or ids -> `type: "reference"`

Set migrated entries to `status: "confirmed"` and `discoveredVia: "anatomy"` when the recipes were
confirmed by prior builds.

## Consolidation

Check:

| Check | Action |
|---|---|
| Duplicate entries | Merge body, delete one, update index |
| Contradictions | Flag for human review; do not auto-resolve |
| Stale tentative entries | Flag entries with empty `confirmedBy` after 3+ screens |
| Mergeable siblings | Propose a broader merged entry |
| Orphaned files | Add topic files missing from `MEMORY.md` |
| Oversized index | Propose consolidation of related entries |
| Stale `reference_*` | Add a re-verify note when node ids or catalog keys may drift |

Write `design-system/_build-cache/consolidation-report-<screenId>.md`. Run `apply` only for
mechanical fixes; flag judgment calls.

## Reflect Procedure

Use after a human designer corrects an AI-built screen.

Phase 1: Capture evidence in parallel.

```text
save_screenshots([aiScreenId, humanScreenId], maxDimension: 2048)
get_node(aiScreenId, depth: 3)    -> ai-tree.json
get_node(humanScreenId, depth: 3) -> human-tree.json
scan_text_nodes(annotationsFrameId) -> annotations.json, if annotations were provided
```

Save under `design-system/_build-cache/<screenId>/reflect/`.

Phase 2: Walk both screens using the same inventory method as
`../../figma-redesign/references/original-inventory.md`. Record:

```text
{ nodeId, role, type, label, content, originalKey,
  boundVariables, layoutSizing, itemSpacing, padding, collectionId }
```

Phase 3: Match nodes by `role` and `label`, then classify deltas:

| Delta type | Signal |
|---|---|
| component-swap | Same role, different `originalKey` |
| variant-fix | Same key, different non-icon variant properties |
| icon-semantic-fix | Same icon set/size, different semantic variant |
| token-fix | Bound variable added or raw px/hex replaced |
| mode-fix | Same token keys, different collection or mode |
| layout-fix | Sizing, spacing, padding, or alignment changed |
| nesting-fix | Tree depth or wrapper count changed |
| composition-fix | Same key/variant, wrong slot or wrong component anatomy |
| content-fix | Visible text changed |
| craft-fix | Hierarchy, order, or axis alignment changed |
| asset-fix | Image fill, crop, or asset changed |
| added | Human screen has no AI counterpart |
| removed | AI screen has no human counterpart |

Phase 4: Attach annotations by nearest role/label or bounding-box proximity when annotations exist.

Phase 5: Hypothesize what memory would have prevented each delta. Search existing library and global
indexes first. If covered, update the entry and bump `confirmedBy`; if new, create a confirmed proposal.

Store routing:

- universal layout/craft rules -> global
- library-specific component/variant conventions -> library
- one-off product decisions -> project

Phase 6: Generate proposal JSON using the schema above, run `apply`, then report applied/skipped counts
and any deltas that need human triage.
