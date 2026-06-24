# R1 — Mechanical Pre-Gate (L2, inventory-driven, deterministic, ~free)

R1 answers exactly **one** question: **is the build mechanically complete per the original inventory?**
It is NOT a craft gate — that belongs to the Opus craft verifier (L3). R1 is the cheap, deterministic
precondition the L3 verifiers must never have to revisit. At L3 these same checks are re-run
INDEPENDENTLY by the **figma-structural-verifier** (Sonnet) — so this floor is the builder's self-check,
and the structural verifier is its independent backstop.

> **The gate is the independent verifier, not your self-report.** A floor administered BY the builder ON
> ITSELF as the gate produces a false green — a judgment-seam check gets self-rationalized ("bindings
> done" while every `boundVariables` is null; "excessParts: PASS" with a placeholder still on canvas).
> That is why these checks are mechanical/scriptable: a deterministic assertion can't be talked out of,
> and an independent agent re-running them can't be either. Run the checks below **inside your R0 loop**
> as your own early-warning, return `r1Report` as **advisory**, answer the Phase 1.5 challenge truthfully,
> and let the L3 verifiers be the gate. Do NOT mark yourself complete and stop.

## Ground truth: the original inventory

Every check below is driven by **`<sot>/rebuild/<screenId>-inventory.json`** — a node-walk of the
ORIGINAL, built independently by the builder (see `references/original-inventory.md`). One entry per
node `{nodeId, parentId, role, type, label, childCount, originalKey?}` recursed through EVERY region,
row, and chrome element (header / logo / toggle / back-button / footer / scrollbar). Named checks in
prior versions (nav-anatomy, chrome, render, fit, catalog-key) are EMERGENT — they fire automatically
when an inventoried element fails to survive.

---

## The six checks (a)–(f)

### (a) Catalog-key: every instance key ∈ target library

Every remote instance's `mainComponent.key` must be present in the target catalog
(`<sot>/rebuild/_redesign-cat-*.scratch.json` / `<sot>/library/**`). A key not in the catalog is either:
- A real GAP → **must** carry a sound `gapJustification` (prefer "assembled from target atoms" over
  keeping the original's component — the `assembly` rung is almost always available and always preferred).
- A clone-of-original → **VIOLATION.** The original file's library often has same-named components with
  DIFFERENT keys, so a clone passes every other check yet is not a target build (the LOOK-ALIKE TRAP —
  canonical in `live-discovery.md`). This is the single most expensive miss: it survives a full Opus
  review because it matches the original perfectly.

**Recurse into top-level organism instances** — a non-target organism key contaminates its whole subtree.
The check is on INSTANCES of remote components; structural FRAMEs you built and LOCAL components
assembled from target atoms have no remote key and are not violations.

**Allowed — assemble-from-target-atoms (legitimate GAP path):** wrapper is a local frame/component,
every atom instance inside it is a target key. Record `gapJustification("target has no whole X;
assembled from target atoms a,b,c")`.

Report: `catalogKeyAudit: [{name, key, inTargetCatalog, gapJustification?}]` — any
`inTargetCatalog:false` without a sound justification = FIX before review.

**Reverse direction — component-first / no-escape-hatch (the OTHER half of (a)).** Check (a) proves every
INSTANCE is authentic; it does NOT catch a RAW FRAME+TEXT assembly **faking** a component the library has —
the escape-hatch failure (`feedback_always-use-library-no-escape-hatch`). For every element whose inventory
role maps to a library kind — **button / text-button, input, select/dropdown, badge, nav-row, pagination,
checkbox/toggle, icon, modal chrome** — assert it is an INSTANCE of a target component, not a hand-built
FRAME+TEXT(+icon) shell. A raw assembly faking one of these kinds = VIOLATION even though it has no remote
key to fail check (a). (Typical miss: a "back" row built as a raw frame of arrow-icon + TEXT when the
library has a text-button set with a left-icon+label variant — see library memory `pattern_back-nav-text-button`.) This is CLAUDE.md's "Library component audit" (REQUIRED kinds must be INSTANCE)
ported into the redesign floor. Structural shells with NO library equivalent (a section wrapper, a column
container) are the only legitimate raw frames. Report
`componentFirstAudit: [{nodeId, role, isInstance, libraryKindExists, verdict}]`.

**Un-componentized repetition (PC8) — a SUSPECT-then-investigate flag, NOT an auto-verdict.** Detect:
N≥3 sibling frames under one container with the same child-structure signature, none of them an INSTANCE
(raw copy-paste or raw clones). This is a FLAG, not an immediate failure — raw siblings can be a legitimate
mid-build state, so a blunt "N≥3 raw = fail" would false-positive. The suspicion triggers a probe; the
probe decides: (1) probe the target library (variants included) for a list-item / list-row / table-row /
data-table component that fits — prefer it (component-first); (2) if none fits, the repeated row must be
ONE local component (`local/<Name>`) instanced N times. Conclude a VIOLATION only if the rows are neither
a library instance nor a local-component instance — genuinely raw repeats with no component behind them,
which means a designer can't edit one row and have all update. Report
`repetitionFlags: [{containerId, n, structureSig, allInstances, libraryFit, verdict}]`.

### (b) Inventory coverage: every inventoried element is present

`coverage = (elements with a built instance or explicit GAP) / (total inventory entries)` must be N/N.
A dropped or collapsed element surfaces here — before Opus has to notice it by eye. Nav rows, chrome
items (header toggle, back-button, footer, scrollbar), and every icon are all in the inventory and
all count.

**Row-parity (repeated-row lists).** For any list of repeated rows (table rows, card lists), every row
must carry the SAME affordance set as its siblings — count the control children (move-arrow, delete,
chevron, action buttons) per row and assert uniform; cross-check against the section's count badge (a
"= 5" badge ⇒ 5 rows each with the full control set). A row that renders bare while its siblings carry
controls = VIOLATION (e.g. the last row of a list silently loses its move + delete buttons).

### (c) No-excess: no built node absent from the inventory

Any built node (INSTANCE, FRAME, visible TEXT) not traceable to an inventory entry is excess — a
fabricated part the original never had (a 3-button group where the original has one; an extra footer;
a placeholder the builder forgot to suppress). Also grep every TEXT node for default content strings:
`"swap it"`, `"Item 1"`, `"Item 1-5"`, `"Title"`, `"Heading"`, `"Label"`, `"Slot"`, and any
project-specific defaults.

### (d) Child-fits-parent: no overflow

For every FRAME, `Σ child extents ≤ frame dimensions` (the 622-in-602 class). Auto-layout miscalculation
and wrong FILL/FIXED on a child both surface here as hard overflow. A clipped child passes a visual check
but fails a resize.

### (e) Raw-value: no unbound style property

No target node has a raw fill / stroke / spacing / radius where a token should be bound. Assert
`boundVariables` is populated for every styled property (`fills`, `strokes`, `padding*`, `itemSpacing`,
`cornerRadius`). **Exception:** if the active project's memory declares `spacingPolicy:"raw-integers-allowed"`
(libraries with no spacing variables), discrete-scale integers (4/8/12/16/20/24/32) are acceptable.

Also assert every FRAME has `layoutMode ≠ null` — no raw frame without auto-layout. A parentless node
should not exist by the time R1 runs.

### (f) No-left-default-variant: no leftover slot default

Two sub-checks:
1. **Slot defaults visible after override:** overriding a slot (image fill, text, swap) does NOT remove
   the component's own default content. Check: `scan_nodes_by_types` the whole frame; any node whose name
   signals a component default (`placeholder`, `empty state`, `no image`, `ic_*_outline`, `Item 1`,
   `Title`, `Slot`, `swap it`) that is still `visible:true` inside an overridden slot = VIOLATION
   (`set_visible(false)` or set the component's visibility property). One frame-wide scan, not per-node
   screenshots.
2. **Variant axis left at default:** every instance whose component set exposes a `mode`/`size`/`state`
   axis must have that axis set (non-default) per the inventory's recorded variant values. Cross-check
   each inventory entry's `originalKey`/props against the built instance.
3. **Render check — icon/leaf instance actually renders:** an instance can exist and render NOTHING
   (empty glyph-less shell, `visible:false` glyph, or fill same color as its parent background).
   For every icon/leaf instance assert: (i) a non-empty VECTOR/BOOLEAN child exists, (ii) that child
   is `visible:true`, (iii) its fill contrasts the nearest surface fill (no dark-on-dark / white-on-white —
   e.g. a near-black toolbar icon on a dark toolbar is present but invisible). This is a structural fact
   (child / visible / fill-vs-bg), not judgment — so it belongs in the floor, not the Opus gate.

### (g) Production-craft mechanical floor — the scriptable members of the D6 PC enum

The craft checks a script CAN run, pulled forward so the Opus gate never spends a round on them (the
judgment members — PC4 icon chrome, PC5 separator, PC7 rhythm — stay D6). Driven by the
`figma-design-patterns` CORE RULES + QUICK ANTI-PATTERN FLAGS you loaded at Step 0.

1. **PC2 — boxless control.** Every INSTANCE whose inventory role is input / select / dropdown / field
   must have a visible field boundary: a bound stroke OR a non-transparent surface fill (or be a known
   bordered library variant). A select rendered as bare text + chevron with no stroke/fill = VIOLATION.
2. **PC3 — destructive not red.** Every delete / trash / remove / 회수 icon's GLYPH fill must be bound to
   the error/destructive color token (not a neutral token, not raw). Neutral trash = VIOLATION. The red
   must be on the GLYPH — a filled red background box instead of a glyph is PC4 (caught at D6).
   See library memory: `pattern_destructive-icon-ghost-glyph`.
3. **Semantic layer names (figma-design-patterns CORE RULE 5).** `scan_nodes_by_types(frame,["FRAME"])`;
   any name matching `/^Frame \d+/`, `/^Group \d+/`, or `/^Rectangle \d+/` = VIOLATION. A finished frame
   has ZERO auto-generated names — `batch_rename_nodes` to semantic roles before R1 passes.
4. **Touch-target audit (figma-design-patterns CORE RULE 13) — mobile/tablet only.** From the same
   `get_nodes_info` pass, for every node whose inventory `role` is interactive — **button, text-button,
   icon-button, nav-row, tab, chip, dropdown/select, input, pagination-button, toggle/checkbox, list-row
   with a tap action** — assert `min(bounds.width, bounds.height) ≥ 44` (iOS) / `≥ 48` (Android per the
   platform). The tappable bound is the node's own frame (an instance's padded hit-area), NOT the glyph
   inside it — a 24px icon inside a 44px button passes; a 40px bare icon-container fails. This is the
   structural sibling of CORE RULE 13, pulled forward so Opus never spends a round measuring pixels.
   Report `touchTargetViolations: [{nodeId, role, w, h}]`. Any entry = FIX (grow the frame / add padding).
   Skip on `desktop-*` / pointer platforms (denser is fine there).
5. **Accent-budget count (figma-design-patterns Stop-Flag "saturated accent flooded").** Count the
   nodes whose `fills`/`strokes` bind the **accent/primary/brand** color token (the one rationed for the
   primary action). Cluster them by role — *primary-action*, *active-nav/tab*, *urgent-status*,
   *filter/chip-active*, *link*, *unread-dot*, *badge*, *decoration*. **More than 2 distinct role-clusters
   wearing the accent on one screen = `accentBudgetExceeded` (advisory flag, not an auto-fail — Opus
   confirms which uses are load-bearing vs. noise).** This catches the "everything is orange, so nothing
   is" failure mechanically instead of by eye. Report `accentUses: [{nodeId, role, token}]` +
   `accentRoleClusters: N`.
6. **Icon-family consistency (figma-design-patterns CORE RULE 10 sibling).** Collect every icon INSTANCE
   (`role` ∈ icon / icon-button glyph). Assert they resolve to **one** icon system — a single
   component-set or a single key namespace (e.g. all `Icon24/*`, one stroke weight / one grid size).
   Mixed families or mixed sizes on one screen (thin-outline header icons + filled tab icons +
   ad-hoc mini glyphs) = `iconFamilyMismatch: [{nodeId, family, size}]`. One family, one weight, per
   screen — any mismatch = FIX (re-import from the canonical set).

---

## Hierarchy must pass the squint (the one judgment check the floor can't script)

The mechanical checks above can't see *visual weight* — whether the right element wins at a glance. That
is a perception judgment, so the gate lives at L3 (reviewer); state the pass conditions here so the
builder designs to them instead of discovering them at review. The screen passes the squint when, with
content legibility set aside (judge by size, weight, contrast, color-area, and whitespace — not by
reading the words):

- the screen's PRIMARY SUBJECT carries the most visual weight — not a status badge, price, or metadata;
- the PRIMARY ACTION stands out as the single rationed accent;
- the MOST URGENT / highest-stakes state is the most prominent, never the weakest;
- grouped surfaces (cards, sections) read as distinct groups — their boundaries survive rather than
  melting into one undifferentiated column.

Why this resists self-checking: a *sharp* screenshot lets you read the small text and rationalize a weak
hierarchy as acceptable. To judge weight independent of content, assess relative size/contrast/area
directly — or, as an optional aid, blur the screenshot (Gaussian radius ≈ 8 via Pillow; `save_screenshots`
has no blur param, so it is local post-processing) to strip the text and reveal raw weight. The blur is
just one technique; the gate is the four conditions above. The reviewer owns this gate (PC9/PC11 in
`review-protocol.md`); the builder treats the conditions as a design target during self-eval.

---

## Runnable recipe (Sonnet, inside R0)

```
# Load target catalog once:
cat <sot>/rebuild/_redesign-cat-*.scratch.json > /tmp/targetcat.json

# Scan the built frame:
nodes = scan_nodes_by_types(nodeId=<builtFrameId>, types=["FRAME","INSTANCE","TEXT"], limit=500)
info  = get_nodes_info(nodes)   # real fills / boundVariables / layoutMode / text / mainComponent.key

# (a) catalog-key
for each INSTANCE in info:
  if not grep -q mainComponent.key /tmp/targetcat.json:
    assert gapJustification exists and is sound

# (b) inventory-coverage
inventoryIds = set of all nodeIds from <screenId>-inventory.json
builtElements = set of inventory-traceable built nodes
assert len(builtElements) == len(inventoryIds)   # N/N

# (c) no-excess
builtNodes = all INSTANCE/FRAME/visible TEXT in info
for each builtNode not in inventoryIds:
  assert builtNode is a justified structural shell (no GAP fabrication)
grep TEXT nodes for "swap it|Item 1|Item 1-5|Title|Heading|Label|Slot"  # → VIOLATION if hit

# (d) child-fits-parent
for each FRAME in info:
  assert sum(child.width or child.height per axis) <= frame.width or frame.height

# (e) raw-value
for each node in info:
  assert no set fill/stroke/padding/radius has null boundVariables
  assert FRAME.layoutMode != null

# (f) no-left-default-variant — slot defaults
scan_nodes_by_types(<builtFrameId>, ["INSTANCE","VECTOR","TEXT"])
assert no node name ~/placeholder|empty.state|no.image|ic_.*_outline|Item 1|Title|Slot|swap it/
       remains visible:true where its parent slot was overridden

# (f) no-left-default-variant — variant axes
for each inventory entry with originalProps:
  builtInstance = find instance by inventory nodeId
  assert all exposed axes set non-default per originalProps

# (f) render check — every icon/leaf instance renders
for each icon/leaf INSTANCE:
  assert non-empty VECTOR/BOOLEAN child exists (not an empty shell)
  assert glyph child.visible == true
  assert glyph.fill color != parent surface fill color  # no dark-on-dark

# (g4) touch-target — mobile/tablet only
for each interactive node (role ∈ button|nav-row|tab|chip|input|select|pagination|toggle|icon-button|tap-row):
  assert min(node.width, node.height) >= 44   # 48 on android  → else touchTargetViolations

# (g5) accent-budget
accentUses = nodes whose fills/strokes bind the accent/primary token
accentRoleClusters = count distinct role-clusters among accentUses
if accentRoleClusters > 2: flag accentBudgetExceeded   # advisory

# (g6) icon-family consistency
iconInstances = INSTANCEs with role ∈ icon|icon-button-glyph
assert all share one component-set / key-namespace / size  → else iconFamilyMismatch

# (hierarchy) the four squint conditions above — judge visual weight independent of legibility
#   advisory at L1, owned at L3 (reviewer). Optional aid: blur the screenshot (Pillow) to strip text bias.
```

Return:

```json
r1Report: {
  "catalogKeyAudit": [{ "name": "...", "key": "...", "inTargetCatalog": true|false, "gapJustification": "..." }],
  "coverage": "N/N",
  "excessNodes": [],
  "overflowFrames": [],
  "rawValues": 0,
  "noAutoLayoutShells": 0,
  "leftoverDefaults": [],
  "invisibleOrContrastedIcons": [],
  "boxlessControls": [],
  "destructiveNotRed": [],
  "autoGeneratedNames": [],
  "componentFirstAudit": [],
  "repetitionFlags": [],
  "touchTargetViolations": [],
  "accentUses": [], "accentRoleClusters": 0, "accentBudgetExceeded": false,
  "iconFamilyMismatch": [],
  "squintHierarchyOk": true
}
```

All zeros, coverage N/N, every `inTargetCatalog:false` with a sound `gapJustification` = **green**.
`touchTargetViolations` / `iconFamilyMismatch` non-empty = FIX. `accentBudgetExceeded` /
`squintHierarchyOk:false` are advisory — fix forward if the builder agrees, else flag for the L3 gate.
Any violation = **FIX FORWARD, do not request Opus review.**

---

## What R1 does NOT catch (Opus L3 owns these)

- A **wrong-but-present** icon (function drift — feedback→share looks right mechanically).
- Feature **behavior** loss (a present button wired to the wrong meaning).
- Designer-level hierarchy / leading / spacing rhythm / craft (D6).
- "Did we achieve the goal / does it read as production-quality vs the original."

Broken-component-set workaround (preserved from prior art): when `get_node`/`get_design_context` throw
`in get_componentProperties: Component set has existing errors`, use `scan_nodes_by_types` +
`get_nodes_info` on raw types (TEXT/RECT/FRAME/VECTOR) — they never throw. Skip broken INSTANCE ids.
Container fills that also throw = "측정 불가"; never estimate.

R1 first (cheap, deterministic), Opus second (judgment, rare). They are complementary layers, not substitutes.
