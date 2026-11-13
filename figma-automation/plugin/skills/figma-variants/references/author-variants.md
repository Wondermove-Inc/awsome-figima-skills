# Authoring a component set

Input is either a **spec** (axes + base anatomy) or **existing frames** that already represent the
states. Output is one COMPONENT_SET whose children are named `Prop=Value, Prop=Value`, laid out in a
grid, with linked component properties.

## 0. Plan the matrix on paper

```
name:        Button
axes:        Style=[Primary, Secondary, Ghost]  Size=[Sm, Md, Lg]  State=[Default, Hover, Pressed, Disabled]
properties:  Label (TEXT, "Button")  Show Icon (BOOLEAN, false)  Icon (INSTANCE_SWAP, Icon/Placeholder)
matrix:      3 × 3 × 4 = 36  → over the 30 cap → move State=Disabled to a BOOLEAN? or split Ghost out
grid:        rows = Style × Size, columns = State, gap 16, header labels on
```

Fix the plan before creating nodes. Changing an axis after 30 components exist is the expensive path.

## Path A — `use_figma` (official Figma MCP)

Load `figma-use` and `figma-generate-library`. Reuse the official script
`figma-generate-library/scripts/createComponentWithVariants.js` for a fresh matrix; it generates
the Cartesian product, names each component, calls `figma.combineAsVariants`, and positions the grid.
Do not copy that script into this repository; reference it from the installed plugin.

Order of operations in one script per set:

1. `await figma.setCurrentPageAsync(componentsPage)` once.
2. Build the **base** variant fully: auto layout, bound variables, text with loaded font.
3. Add component properties to the base **before** combining:
   `labelKey = base.addComponentProperty("Label", "TEXT", "Button")` and link
   `textNode.componentPropertyReferences = { characters: labelKey }`. Same for BOOLEAN (`visible`) and
   INSTANCE_SWAP (`mainComponent`).
4. Clone the base for every other combination (`base.clone()`), rename to the combo string, mutate
   only the axis-specific properties (fill token, size token, opacity for Disabled).
5. `const set = figma.combineAsVariants(components, componentsPage); set.name = "Button";`
6. Grid layout: parse each child's name, `x = colIndex * (w + gap)`, `y = rowIndex * (h + gap)`,
   then `set.resizeWithoutConstraints(maxX + pad, maxY + pad)`.
7. `set.description = "..."` (only on COMPONENT/COMPONENT_SET), return `{ setId, variantIds }`.

Converting **existing frames**: `figma.createComponentFromNode(frame)` per frame, rename each to its
combo string, then steps 3, 5, 6. Properties added after combining go on a child component, not on the
set; prefer adding them before.

## Path B — figma-mcp-express (no combine step available)

What this path produces: correctly named, token-bound, grid-arranged **loose components**, ready for
a one-click combine. Say so in the ledger and to the user.

```
1. create_section(name:"Button — variants (uncombined)")            → sectionId
2. for each combination (batch, continueOnError:false):
     clone_node(nodeId:<base frame>, parentId:sectionId)             → frameId
     rename_node(nodeId:frameId, name:"Style=Primary, Size=Md, State=Hover")
     set_fills / set_text / set_opacity with variable bindings for the axis delta
     create_component(nodeId:frameId)                                → componentId
3. move_nodes into the grid (x = col*(w+gap), y = row*(h+gap))
4. get_nodes_info on all component ids → confirm type COMPONENT and names
5. save_screenshots([sectionId]) → final visual pass
6. Hand-off: "Select all components in section <name> → Combine as variants → rename set to Button."
```

Validate the batch with `validateOnly:true` first. Use `get_batch_op_spec` for exact params; do not
guess op schemas.

After the user combines the set, re-read it with `get_node(setId, depth:1)` and continue with
`references/manage-variants.md` for anything else (property linking still needs `use_figma` or the UI).

## From existing instances of a library set (re-skin, not author)

If the "variants" the user wants already exist in a subscribed library, do not author anything:
`import_component_by_key(key, assetType:"COMPONENT_SET")` → `create_instance(componentId,
variantProperties:{...})` → `set_instance_properties`. See the figma-redesign skill's
`variant-resolution.md` for choosing the right variant from an inventory.

## Validation checklist

- [ ] child count = matrix size; no duplicate names
- [ ] every axis value appears with the same spelling and casing across children
- [ ] component properties exist on the set (A) or are listed as "pending combine" in the ledger (B)
- [ ] each property is linked to a child (A) — unlinked properties are a defect
- [ ] all variant fills/strokes/radii/spacing are variable-bound; zero raw hex
- [ ] grid laid out, set resized, header labels match sibling sets
- [ ] no scratch frames or probe instances left on the canvas
