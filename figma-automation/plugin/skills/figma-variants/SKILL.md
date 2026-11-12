---
name: figma-variants
description: Create and manage Figma component sets, variant axes, and component properties (TEXT, BOOLEAN, INSTANCE_SWAP, SLOT). Use for "turn these frames into a component with variants", "add a State axis", "add a Label property", "audit this component set", "rename a variant value everywhere", or "migrate instances to the new variants".
---

# /figma-variants — author and manage component sets

Variant work has two halves with different tool support:

| Half | What it means | figma-mcp-express (`batch` ops) | Official Figma MCP (`use_figma`) |
|---|---|---|---|
| **Consume** | pick a variant, set properties, swap, detach | full | full |
| **Author** | combine components into a set, add/edit/delete component properties, slots, exposed instances | **not available** (verified against the live catalog, v2.8.1) | full via Plugin API |
| **Manage** | audit axes, rename values, add a value/axis, delete a variant, migrate instances | mostly available through name-based ops | full |

Read `references/backend-matrix.md` before choosing a backend. Never claim a set was "combined" through
figma-mcp-express; it cannot do that step.

## Trigger

```
/figma-variants author <frame-ids|set-spec> [--library <key>]   → build a new component set
/figma-variants manage <component-set-id> <change>              → add/rename/delete axes, values, properties
/figma-variants audit <component-set-id>                        → report axes, gaps, dupes, unlinked props
/figma-variants migrate <old-set-id> <new-set-id>               → move instances to the new set
```

## Step 0 — Decide the backend (once per task)

1. Is `use_figma` (official Figma MCP, remote server) available and authenticated for this file?
   - Yes → **author** and **manage** through `use_figma`. Load `figma-use` first; for a reusable
     library deliverable also load `figma-generate-library`. Pass both names in `skillNames`.
   - No → build everything that does not require combining through figma-mcp-express, then hand
     the final "Combine as variants" step to the user (Figma UI: select the components → right
     panel → **Combine as variants**) or to a teammate session with `use_figma`.
2. Is the target a **published library** you do not own? Then you can only consume. Stop and say so.
3. Record the decision in the task ledger before touching the canvas.

## Step 1 — Read conventions before writing anything

Every file has its own variant grammar. Read a sibling component set first and match it exactly:

- Axis names and casing: `State=Default` vs `state=default` vs `Property 1=Default`.
- Value casing and vocabulary: `Hover` vs `Hovered`; `Sm/Md/Lg` vs `Small/Medium/Large`.
- Property key suffixes on instances: `Label#1:0` (the `#n:m` suffix is generated, never invented).
- Grid layout of existing sets: row axis, column axis, gap, header labels.

figma-mcp-express: `get_node(setId, depth:1)` returns the children named `Prop=Value, Prop=Value`;
parse those names to recover the axes. `get_local_components` returns keys, set ids, and
`variantProperties` per variant. `use_figma`: read `componentPropertyDefinitions` on the
**COMPONENT_SET** (never on a variant child).

## Step 2 — Author or manage

| Task | Recipe |
|---|---|
| New set from a spec or from existing frames | `references/author-variants.md` |
| Add/rename/delete an axis or value, add/edit/delete a component property, slots, exposed instances, migrate instances | `references/manage-variants.md` |

Rules that apply to both backends:

- **Variant names are the schema.** A variant's `Prop=Value, Prop=Value` name defines its axes. Rename
  carefully; one child with a typo creates a new axis value and a conflict badge in Figma.
- **Complete the matrix or split it.** Every axis combination must exist. If Size × Style × State
  exceeds 30 combinations, split into sub-components or move an axis to a BOOLEAN/INSTANCE_SWAP property.
- **Never a variant per icon.** Use one INSTANCE_SWAP property.
- **Properties must be linked.** A TEXT/BOOLEAN/INSTANCE_SWAP property that no child references does nothing.
- **Lay the grid out.** After combining, variants stack at (0,0); position them and resize the set.
- **Tokens, not hex.** Variant fills, strokes, radii, and spacing bind to library variables; only
  the axis value changes between variants.

## Step 3 — Verify (mandatory)

1. Structural read of the set (`get_node depth:1` or `use_figma` on the set): count of children equals
   the expected matrix size, no duplicate names, axis vocabulary matches Step 1.
2. Instantiate one variant with real content (`create_instance` + `set_instance_properties` /
   `setProperties`) and confirm every exposed property changes something visible.
3. One screenshot of the whole set as the final visual pass.
4. Ledger: axes, matrix size, property keys, the backend used, and anything handed to the user.

## Anti-patterns

- Reporting "component set created" when only loose components were produced through figma-mcp-express.
- Guessing a property key suffix (`Label#1:0`) instead of reading it from the component.
- Reading `componentPropertyDefinitions` from a variant child instead of the set.
- Adding a new axis value to some children only.
- Leaving probe instances or scratch frames on the canvas.
