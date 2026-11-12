# Managing an existing component set

All management starts with an audit read. Never mutate a set you have not read in this session.

## 1. Audit

### figma-mcp-express
```
get_node(nodeId:<setId>, depth:1)        → children[].name  ("Prop=Value, Prop=Value")
get_local_components()                   → key, componentSetId, variantProperties per variant
scan_nodes_by_types(nodeId:<page>, types:["INSTANCE"]) → instances to migrate later
```
Parse the child names into axes. Report:

| Check | Defect |
|---|---|
| Cartesian completeness | missing combinations (blank cells in the variant picker) |
| Duplicates | two children with the same combo (Figma shows a conflict badge) |
| Vocabulary drift | `Hover` and `Hovered` on the same axis |
| Casing drift | `State=default` next to `State=Default` |
| Orphan axis | an axis present on one child only |
| Oversize matrix | more than 30 combinations |

### use_figma
Read `componentPropertyDefinitions` on the **COMPONENT_SET** node (never on a variant child):
```js
const set = await figma.getNodeByIdAsync(SET_ID);
if (set.type !== "COMPONENT_SET") throw new Error("expected COMPONENT_SET");
return { names: set.children.map(c => c.name), defs: set.componentPropertyDefinitions };
```
Add to the report: properties with no `componentPropertyReferences` on any descendant (dead
properties), and nested instances that should be exposed (`isExposedInstance`).

## 2. Rename an axis or a value (both backends)

Variant props are derived from child names, so a consistent rename across **all** children is the
whole operation.

figma-mcp-express:
```
batch_rename_nodes(nodeIds:[<all children>], regex:"State=Hover\\b", replacement:"State=Hovered")
get_node(setId, depth:1) → confirm every child changed
```
use_figma: loop `set.children`, replace in `child.name`, return changed ids. Axis rename
(`Type=` → `Style=`) is the same regex on the axis key. Instances keep working because Figma
re-maps by name; still run the audit again afterwards.

## 3. Add a value to an existing axis

figma-mcp-express:
```
clone_node(nodeId:<closest sibling>, parentId:<setId>)      → newId
rename_node(nodeId:newId, name:"Style=Primary, Size=Md, State=Loading")
… edit the delta (fills, visibility, text) with variable bindings …
move_nodes(nodeIds:[newId], x:<col>, y:<row>)
get_node(setId, depth:1) → child count +N, no duplicates
```
Repeat for every other-axis combination the new value needs (adding `State=Loading` to a
3×3 Style×Size set means 9 clones). If the server rejects `parentId` = set id for `clone_node`,
clone next to the set, then `reparent_nodes` into it; if that is rejected too, switch to `use_figma`.

use_figma: `const n = sibling.clone(); n.name = "..."; set.appendChild(n);` then position.

## 4. Add a new axis

Adding `Theme=[Light, Dark]`:
1. Rename every existing child by appending `, Theme=Light` (`batch_rename_nodes` suffix mode or
   regex `$` anchor).
2. Clone every child once, rename `Theme=Light` → `Theme=Dark`, apply the dark-mode delta.
   Prefer binding to variables and switching the **variable mode** on the child over manual fills.
3. Re-grid: the new axis becomes a row group; resize the set.
4. Audit again. The matrix doubled; check the 30 cap.

## 5. Delete a value or an axis

- Delete a value: `delete_nodes` on every child carrying it. Before deleting, migrate instances
  that use it (section 7) or Figma will reset them to the default variant.
- Delete an axis: rename every child to drop the `Axis=Value` segment, then delete the duplicates
  that collapse onto the same combo.

## 6. Component properties, slots, exposed instances (use_figma only)

Not reachable through figma-mcp-express; do these with `use_figma` or ask the user to do them in the UI.

```js
// add + link on the base variant (keys are generated — capture them, never type them)
const base = set.children.find(c => c.name === "Style=Primary, Size=Md, State=Default");
const labelKey = base.addComponentProperty("Label", "TEXT", "Button");
const text = base.findOne(n => n.type === "TEXT");
text.componentPropertyReferences = { characters: labelKey };

// rename or change default
set.editComponentProperty(labelKey, { name: "Text", defaultValue: "Label" });

// delete
set.deleteComponentProperty(labelKey);

// expose a nested instance so its props show on the parent
const icon = base.findOne(n => n.type === "INSTANCE" && n.name === "Icon");
icon.isExposedInstance = true;

// slot
const slot = base.createSlot(); slot.name = "Content";
```
Property definitions live on the set once combined; adding a property to one variant child applies
to the set, but link it in every variant that has the corresponding child node.

## 7. Migrate instances (deprecate a set or move to new values)

figma-mcp-express, one round-trip each:
```
scan_nodes_by_types(nodeId:<page or frame>, types:["INSTANCE"])              → $0.matchingNodes
swap_component(nodeIds:["$0.matchingNodes[*].id"], componentId:<new variant>)  (bulk)
set_instance_properties(nodeIds:[...], properties:{"State":"Default"})          (bulk, resetOverrides:false)
```
Filter the scan to instances whose main component belongs to the old set before swapping. Keep
text overrides by swapping to the matching variant (same axis values) rather than the default.
Verify with `get_nodes_info` on the swapped ids.

## 8. Ledger entry

```
set: Button (123:45)   backend: use_figma | figma-mcp-express + user combine
axes before: Style[3] Size[3] State[4]   after: Style[3] Size[3] State[5]
children: 36 → 45   duplicates: 0   dead properties: 0
properties: Label#1:0 (TEXT) Show Icon#1:1 (BOOLEAN) Icon#1:2 (INSTANCE_SWAP)
instances migrated: 18 (swap_component)   handed to user: none
```
