# Original Inventory — Ground Truth for Every Screen

## Contents

- What this is
- Invariants
- Inventory JSON schema
- Walk procedure
- Inventory-diff self-review
- Look-alike trap
- Memory proposals

## What this is

The `<sot>/rebuild/<screenId>-inventory.json` file is the **single source of truth** for completeness. Every completeness check — from the builder's self-review to the advanced-model gate — reduces to one question per element: **did this inventory entry survive into the built screen, rendered and visible?**

This design is deliberate. Every past miss on this project (clone-of-original components, missing leading icons, excess chevrons, footer overflow, dropped logo, dropped back-row) was an original element that was never enumerated. Named per-category checks are emergent from inventory coverage, never special-cased prose. If the inventory is exhaustive, exhaustive coverage is sufficient.

## The invariants (never negotiable)

1. **Built by node-walk** — `get_metadata` on the frame → `get_node` with depth, recurse EVERY region, EVERY row, and EVERY chrome node (header, logo, menu-toggle, back-button, footer, scrollbar). Never from memory, never from a screenshot glance. The walk must be mechanical and deterministic.
2. **Built independently by BOTH builder AND reviewer** — the builder builds the inventory FIRST (before building anything). The reviewer builds its OWN inventory at the gate, independently (never trusting the builder's). Both must agree on what the original contains; discrepancies = the builder missed something.
3. **Every past miss = an un-enumerated element** — the root cause of every dropped feature is always "we never put it in the inventory." So the walk must be paranoid: walk chrome nodes as carefully as content nodes.

## Inventory JSON schema

File: `<sot>/rebuild/<screenId>-inventory.json`

```json
{
  "screenId": "C01",
  "frameId": "123:456",
  "builtAt": "ISO-8601 timestamp",
  "entries": [
    {
      "nodeId": "123:456",
      "parentId": "123:100",
      "role": "sidebar-nav",
      "type": "region",
      "label": "Left Navigation",
      "content": null,
      "childCount": 12,
      "originalKey": null
    },
    {
      "nodeId": "123:789",
      "parentId": "123:456",
      "role": "nav-row",
      "type": "row",
      "label": "프로젝트 관리",
      "content": "프로젝트 관리",
      "childCount": 3,
      "originalKey": "abc123def456..."
    },
    {
      "nodeId": "123:790",
      "parentId": "123:789",
      "role": "nav-row-leading-icon",
      "type": "icon",
      "label": "folder-icon",
      "content": null,
      "childCount": 0,
      "originalKey": null
    },
    {
      "nodeId": "123:801",
      "parentId": "123:100",
      "role": "top-bar-logo",
      "type": "chrome",
      "label": "Logo",
      "content": null,
      "childCount": 2,
      "originalKey": null
    }
  ]
}
```

### Field definitions

| Field | Required | Description |
|---|---|---|
| `nodeId` | yes | Figma node id in colon format |
| `parentId` | yes | Direct parent's nodeId |
| `role` | yes | Semantic role: descriptive string identifying WHAT this element does in the UI (e.g. `"nav-row"`, `"table-header-cell"`, `"footer-cancel-button"`, `"scrollbar"`) |
| `type` | yes | Structural category: `region` \| `row` \| `control` \| `icon` \| `chrome` |
| `label` | yes | Human-readable descriptor for diff/review output |
| `content` | yes/null | Visible text content if any; null for purely visual nodes |
| `childCount` | yes | Number of direct children (for density sanity-check) |
| `originalKey` | yes/null | If this node is an INSTANCE in the original, its `mainComponent.key`; null for raw frames/groups |

### `type` values

| Type | Includes |
|---|---|
| `region` | Structural layout containers: sidebar, header bar, main content area, card, panel, dialog |
| `row` | Repeated horizontal units: nav row, table row, list item, comment row, form row |
| `control` | Interactive leaf elements: button, input, checkbox, dropdown, chip, tab |
| `icon` | Icon/glyph nodes: leading icons, action icons, signifier icons (search magnifier, calendar, chevron) |
| `chrome` | Non-content structural anchors: logo, hamburger/menu-toggle, back-button, footer divider, scrollbar, modal-overlay |

## Walk procedure

```
1. get_metadata(frameId) → identify top-level regions
2. For each region: get_node(regionId, depth=3) → enumerate child structure
3. For EVERY row-type child: recurse one more level to enumerate per-row controls + icons
4. For chrome nodes (header bar, footer bar): walk explicitly — do not assume they have no notable children
5. Scan for: logo, hamburger/menu-toggle, back-navigation, breadcrumb, any persistent widget outside main content
6. For EVERY instance in the original: record its mainComponent.key as originalKey
7. Write all entries to inventory.json (one entry per meaningful node — not every atomic sub-pixel frame)
```

**Paranoid chrome rule:** Header/logo/menu-toggle/back/footer/scrollbar are the most-often-dropped elements. Walk them last but explicitly; do not rely on "the region walk covered it."

**Per-row affordances rule:** For EVERY repeated row type (comment rows, table rows, nav rows), walk at least one representative row fully and record ALL its child controls and icons. Per-row actions (edit/delete/timestamp, status-dot, signifier icon) must appear as separate `type: icon` or `type: control` entries.

## Inventory-diff self-review

The builder's self-review (L1) = diff the inventory against the built frame:

```
For every entry in inventory.json:
  - Is there a built counterpart? (MISSING = L2 coverage failure)
  - Is it visible:true and rendered (not invisible, not clipped)? (INVISIBLE = L2 check)
  - Is there a built node with NO inventory entry? (EXCESS = L2 no-excess check)
```

This is the ONLY completeness check that matters. The six named L2 checks in `completeness-floor.md` are mechanical verifications that fall out of this diff; they are not additional checks beyond it.

## LOOK-ALIKE TRAP (inventory-specific)

When recording `originalKey` for instances, note: the original file may use its own library's same-NAMED components with different keys than the target library. The inventory records what the original HAS (its keys), not what the build will use. The L2 `catalog-key` check (see `completeness-floor.md`) then verifies that every BUILT instance key ∈ target catalog. These are two separate passes; do not conflate them.

## Memory proposals

After a screen is built, write any newly discovered component interaction patterns to
`design-system/_build-cache/<screenId>/memory-proposals.json` as tentative entries. The orchestrator
calls `figma-playbook apply` after PASS to commit confirmed proposals. Scan the library memory index
at STEP 0 before any discovery phase to avoid re-deriving what the team already knows.
