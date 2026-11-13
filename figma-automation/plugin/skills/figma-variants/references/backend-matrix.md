# Backend matrix for variant work

Verified 2026-10-22 against the live figma-mcp-express catalog (npm v2.8.1, `search_batch_ops
category:components`) and the official Figma MCP `figma-use` skill (plugin v2.2.157,
`references/component-patterns.md`).

## Capability table

| Operation | figma-mcp-express | Official Figma MCP `use_figma` | Figma UI fallback |
|---|---|---|---|
| Convert a frame to a COMPONENT in place | `create_component` | `figma.createComponentFromNode(node)` | Cmd/Ctrl+Alt+K |
| Create an empty component | `create_frame` → `create_component` | `figma.createComponent()` | — |
| **Combine components into a COMPONENT_SET** | **none** | `figma.combineAsVariants(components, parent)` | Select → "Combine as variants" |
| Add TEXT / BOOLEAN / INSTANCE_SWAP property | **none** | `comp.addComponentProperty(name, type, default)` | Properties panel "+" |
| Rename / change default of a property | **none** | `comp.editComponentProperty(key, {name, defaultValue})` | Properties panel |
| Delete a property | **none** | `comp.deleteComponentProperty(key)` | Properties panel |
| Link a property to a child (`characters`, `visible`, `mainComponent`) | **none** | `child.componentPropertyReferences = {...}` | Layer property picker |
| Create a SLOT | **none** | `comp.createSlot()` or `addComponentProperty(name, "SLOT", "")` | Slot tool |
| Expose a nested instance's properties | **none** | `nestedInstance.isExposedInstance = true` | Layer panel |
| Rename a variant axis or value | `rename_node` / `batch_rename_nodes` on the set's children | set `child.name` | Variants panel |
| Add a value to an existing axis | `clone_node` a sibling with `parentId` = set id, then `rename_node` | `sibling.clone()` + rename inside the set | Duplicate variant |
| Delete a variant | `delete_nodes` on the child | `child.remove()` | Delete |
| Reposition variants inside the set | `move_nodes` / `resize_nodes` | set `x`/`y`, `resizeWithoutConstraints` | Drag |
| Pick a variant for a new instance | `create_instance` with `variantProperties` or `componentKey` | `set.children.find(...)` + `createInstance()` | Instance panel |
| Set variant / text / boolean / swap on an instance | `set_instance_properties` (bulk with `nodeIds[]`) | `instance.setProperties({...})` | Instance panel |
| Swap the main component of instances | `swap_component` (bulk) | `instance.swapComponent(comp)` | Swap instance |
| Detach | `detach_instance` | `instance.detachInstance()` | Detach |
| Import a library set | `import_component_by_key(key, assetType:"COMPONENT_SET")` | `figma.importComponentSetByKeyAsync(key)` | Assets panel |
| Publish the library | none | none | Publish dialog |

## Prerequisites per backend

### figma-mcp-express
- Figma Desktop open with the **Figma MCP Express** plugin running; the file must be open.
- Pass `channel` when more than one file is connected.
- Load the `figma-mcp-express` skill first (the PreToolUse hook blocks tool calls otherwise).
- No token, no quota, no seat requirement.

### Official Figma MCP (`use_figma`)
- Remote server `https://mcp.figma.com/mcp`, authenticated. Writing to the canvas is remote-server only.
- Edit access to the file. Per Figma's guide, view/collab seats and the Starter plan are capped at
  6 tool calls per month; Dev/Full seats on paid plans get per-minute limits; write tools are exempt.
- Load `figma-use` before every `use_figma` call and include it in `skillNames`.
- For a reusable component set or library deliverable, also load `figma-generate-library`.
- One page switch per script; fan out multi-page work as parallel calls.

## Decision rule

1. `use_figma` available and authenticated for this file → author and manage there.
2. Otherwise → build loose, correctly named variant components through figma-mcp-express, lay them
   out in a grid, and hand the single combine step to the user. Say explicitly that the set is not
   combined yet.
3. Never mix backends on the same node inside one batch; finish one backend's step, re-read, then
   continue with the other.

## Known gaps to track upstream

- figma-mcp-express has no `combine_as_variants`, `add_component_property`,
  `edit_component_property`, `delete_component_property`, `create_slot`, or `set_exposed_instance`
  batch op as of v2.8.1. If any of these appear in `search_batch_ops category:components` later,
  prefer them over the `use_figma` path and update this matrix.
