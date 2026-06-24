# Variant Resolution + Probe-to-Best (R-OTF steps 3b + 4)

**Source of truth for the element being resolved:** the inventory entry in
`<sot>/rebuild/<screenId>-inventory.json` (built per `original-inventory.md`). Read the original's
properties FROM the inventory, not from a fresh screenshot or from memory.

**Known levers:** scan the library memory index first (loaded at STEP 0). If a `feedback_*` or `pattern_*`
entry matches this element type, load that file — the axis-mapping may already be solved.

---

## 3b — RESOLVE THE VARIANT → SHORTLIST

Map the original element's inventory entry onto the component set's variant axes. Never accept the
default variant.

### Read the axes LIVE
`import_component_by_key(key, assetType:"COMPONENT_SET")` then `get_node(setId, depth:2)` → enumerate
axes and their possible values (`Mode`, `Size`, `State`, `Type`, `Count`, `Thumbnail`, `Footer`, etc.).
If the scratch catalog already lists `variantProperties`, use it to enumerate; confirm against the live node.

### Derive each axis value from the inventory entry

| Axis kind | How to derive from the original | Common miss |
|---|---|---|
| **density / MODE** (compact vs default) | Row height / padding from the inventory entry's dims. Dense toolbar/table header → `compact`. | **#1 missed variant.** Compact-capable header left at default looks bloated. |
| **SIZE** (sm/md/lg) | Element dims relative to siblings in the inventory. | Picking md when the original is clearly sm. |
| **STATE** (default/active/selected/disabled) | Which row/tab/item is highlighted (from inventory `role` + screenshot). | Building everything in default state; losing the active tab. |
| **TYPE / STYLE** (filled/outlined/ghost; primary/secondary) | Original's fill + emphasis level. | Primary where the original is secondary. |
| **FEATURE axes** (Thumbnail / Footer / leading-icon / trailing-icon) | ON **only if** the original has that part (inventory entry carries it). | Thumbnail=true with no image; Footer the original lacks. |
| **COUNT / repetition** | Exact count from inventory `childCount`. | Count=3 where the original has 1 (feature-excess). |

For specific known mappings (date column = textfield+calendar not Picker; form Dropdown vs filter-select
by role; nav-row trailing chevron = per-row boolean toggle), load the matching library memory topic file
— it holds the exact property keys, which are library-specific and must be re-verified live.

### Output: a SHORTLIST, not a single guess
Emit 2–4 plausible variants (+ rival components you're torn between). Paper-reasoning narrows;
the probe decides.

---

## 4 — PROBE TO CONFIRM

**Axis-mapping (3b) is the primary discriminator; the probe confirms it.** You are a Sonnet agent —
pixel-level visual comparison is the weak capability. Reason the variant from the axes + measured
properties, arrive at a confident top pick, then render it to CONFIRM — not to discover.

```
# DEFAULT (unambiguous after 3b): 1-candidate confirm
create_instance(pick.variantKey, parentId=<scratch area>)
set_text / set_instance_properties  → inject same original content (compare like-for-like)
save_screenshots([instanceId])      → render BESIDE the original element
confirm form / mode / parts match.
yes → commit.  no → diagnose the wrong axis, fix it, re-confirm (still 1 candidate).

# ONLY when 3b leaves a GENUINE tie: compare ≤3 candidates the same way, pick closest.
```

**Hard cost bound:**
- ≤3 candidates per element; multi-candidate ONLY for a genuine 3b tie.
- Delete each probe instance immediately after the decision (`delete_nodes`). No probe debris.
- If probing fights you (imports hanging, screenshots slow): commit the structurally-reasoned pick.
  Opus catches a variant miss; a watchdog death loses the whole build.

Commit the winner; record in the ledger: which candidates were compared, the axis reasoning, the
confirmation, and the slot/text-node relPaths (`get_node depth:6`) for content injection.

---

## 5 — TRIM TO NEED (feature-EXCESS is as wrong as feature-LOSS)

After committing, make the composition match the original's inventory entry:

1. **Prefer a simpler variant** (Count=1 over Count=3; no-Footer over Footer).
2. Else **hide unused parts**: `set_visible(false)` on extra buttons / footers / legends / secondary
   slots the inventory doesn't list.
3. **Kill default placeholder content**: no leftover "swap it", "Item 1", "Title", "Label".
4. **Never pad**: don't add a part the inventory lacks just because the component offers it.

---

## Anti-patterns (any hit = redo the resolution)

- Default variant shipped (no axis derived from the inventory entry).
- Variant picked on paper with no probe when the choice was genuinely ambiguous.
- A FEATURE axis turned ON with an empty slot (Thumbnail=true, no image).
- Count=3 variant where the inventory shows one item.
- Probe instance left on the canvas (debris not deleted).
- "Used the right variant" claimed in the ledger with no record of candidates compared.
- Declared "library-forced" or GAP without probing the override (`TEST-THE-OVERRIDE` — see builder-brief.md).
