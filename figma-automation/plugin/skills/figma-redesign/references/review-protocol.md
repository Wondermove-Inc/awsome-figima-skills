# Review Protocol — L3 Gate (two parallel verifiers, run RARELY, ONCE per screen)

## Contents

- Cold start
- Verifier method
- Review dimensions
- Delta-review mode
- Finding quality bar
- JSON output
- Hard rules

L3 is split into **two independent verifiers that run in parallel** (background, READ-ONLY) on a screen
already past L2 (the mechanical pre-gate, `completeness-floor.md`). Neither issues PASS alone — the
orchestrator merges them: **`PASS = structuralVerdict ∧ craftVerdict`**, with the combined findings sent
to the builder in one fix round.

| Verifier | Model | Owns | Reads |
|---|---|---|---|
| **figma-structural-verifier** | less advanced model / Sonnet tier | D1 completeness (own inventory), D2 keys, D3 tokens, D4 auto-layout, D5 content presence, + the scriptable scans (touch-target, accent-budget, icon-family, semantic names) | this doc's **D1–D5** + `completeness-floor.md` (a)–(j) |
| **figma-reviewer** | advanced model / Opus tier | D6 craft (PC1–PC13 incl. hierarchy gate), §1G asset MEANING, §1H functional fidelity, §5F duplicate, D7 patterns | this doc's **D6, §1G, §1H, §5F, D7** |

The split maps each check to the model that fits it: objective/scannable facts → less advanced model /
Sonnet tier; design taste + semantic meaning → advanced model / Opus tier. Read and run **only your assigned dimensions** — the other verifier owns the
rest, in parallel; do not re-derive its layer.

> **Cost model: this gate runs as FEW times as possible — ideally ONCE per screen.** The lever that keeps
> it cheap is the builder's strong evidence-based self-eval (R0 + R1 + Phase 1.5 dry-run); the first pass
> should usually PASS. When a verifier finds a defect its sibling layer should have caught (a raw value at
> the craft verifier, a craft miss the structural scans flagged), note it as an `l2GateMiss` so the
> upstream floor tightens — every round saved is the point.

## Step 0 — cold start

1. `Skill('figma-mcp-express')` — read-tool mechanics + bounded-read discipline. You are **READ-ONLY**: any
   read tool is fair game (`save_screenshots`, `scan_nodes_by_types`, `get_nodes_info`, `get_node`,
   `search_nodes`, `get_design_context`, `get_metadata`…). Constraint: no creates/edits/deletes.
2. Read this skill's local craft vocabulary for D6. The builder builds with this lens (auto-layout dynamic
   + resize test, component-first, padding/gap ownership, FILL/HUG/FIXED discipline, field affordance, no
   fake-distribute). You must judge in the SAME language or you will rubber-stamp crude composition the
   builder's lens should have caught. A violation of these craft rules is a D6 FAIL **even when the build
   matches the original** — the original is the reference for intent, not a licence to reproduce a crude
   layout.
3. You are given: `channel`, `builtFrameId`, `originalFrameId` (review is ALWAYS side-by-side),
   `ledgerPath`, `round` number, and on a re-review the prior round's findings to verify-as-fixed.

> If the original is a **broken component set**, `get_node`/`get_design_context` throw — use
> `save_screenshots` (crash-safe) + `scan_nodes_by_types`/`get_nodes_info`; skip broken INSTANCE ids.

---

## Method — by verifier

Both verifiers `save_screenshots` BOTH frames at `maxDimension: 2048` and inspect side by side first.
Then each runs only its layer (they run in parallel, so neither waits for the other):

**Structural verifier (less advanced model / Sonnet tier) — build YOUR OWN inventory, then diff.** Node-walk the original (recurse
every region, row, and chrome node: header / logo / toggle / back-button / footer / scrollbar), derive
the feature list yourself, and diff against the build. The builder's ledger is advisory; yours is
authoritative. Then run D1–D5 + the scriptable scans (scope every scan to the frame id, never a page).

**Craft verifier (advanced model / Opus tier) — judge from the screenshots + targeted reads.** You do not need a full node
inventory; compare the built and original frames visually for D6 craft, hierarchy, asset/function
meaning, and pattern adherence, doing targeted structural reads only where a finding hinges on one.

---

## Dimensions

### D1 — Completeness: every inventoried element survived + renders + is authentic

Three sub-axes together answer "is what the original had actually present and real?":

**Presence (feature coverage + no-excess):** your independent inventory diff. Any element the original
had that the build omits = feature-LOSS (critical, never minor). Any part the build added that the
original never had = feature-EXCESS (FAIL). Name the lost capability precisely — do not infer function
from position alone; verify against the original.

**Visual fidelity (asset fidelity §1G + render §1H-icon):**
- Every photo / logo (correct `Brand=`) / icon is present AND correct. An empty Thumbnail slot = FAIL.
- **Leftover-default check:** overriding a slot does NOT remove the component's own default content
  (C01 shipped a placeholder glyph on a real photo). The reliable catch is structural, not zoom: run
  `scan_nodes_by_types` on the built frame and confirm no default-named node (`placeholder`,
  `empty state`, `no image`, `ic_*_outline`, default text) is `visible:true` in an overridden slot.
  Zoom a region only when that scan or the full-frame view flags something. Leftover default = FAIL (major).
  If it reached you, flag the L2 gate miss.
- **Render check:** an instance can EXIST and render NOTHING — empty shell, `visible:false` glyph, or
  glyph fill the same color as its background (dark-on-dark / white-on-white — e.g. a near-black toolbar
  icon on a dark toolbar reads as absent). ZOOM icon strips (toolbars, nav rows, action columns) at high
  scale. Any icon that renders nothing = FAIL (major; a lightbox with no visible close button is
  critical). If it reached you, flag the L2 gate miss.

**Function fidelity (§1H meaning):** no function drift — a download button that became a share button
= FAIL; an icon whose MEANING differs = FAIL. Verify each icon's meaning vs the original, not just
that an icon exists.

**TEST-THE-OVERRIDE before "library-forced" or GAP:** if the builder claims a library limitation forced
a deviation — test it. Try the override (e.g. `instance.primaryAxisAlignItems="MIN"`) in a bounded read
or ask whether it was attempted. A "library-forced" excuse that was never actually tested is an invalid
justification. Do not accept undocumented GAP claims.

### D2 / D3 / D4 — Token / Typography / Auto-layout / Spacing binding

These should already be green from L2 — spot-check only. If L2 missed one, flag it as a gate miss.

**D4 structural scan (mandatory — do NOT skip):** run `scan_nodes_by_types(builtFrameId, ["FRAME"])` scoped to the built frame. Any FRAME node where `layoutMode = "NONE"` is a structural failure unless the node's name contains "spacer" or its width/height is 0 (pure decorative). A review that skips this scan and rubber-stamps auto-layout is an L2 gate miss — flag it. Also: `itemSpacing > 48` = FAIL (fake-distribute slop); x/y coordinates set inside auto-layout frame children = FAIL (layout is rigid, not dynamic).

**Mobile safe area (PC-SA — check on every mobile screen):** the root screen frame must have `paddingTop ≥ 59` and `paddingBottom ≥ 34`. This is a hard invariant — content that invades the status bar zone is not production-ready. Missing safe area = D4 FAIL (flag as `pc-sa`).



**Binding-proof caveat:** the figma-mcp-express read projection (`get_node`/`get_nodes_info`) often returns a
codegen `styles` view that STRIPS `boundVariables` (a bound white fill looks identical to a raw one).
Do NOT bounce a finding as "unverifiable" and do NOT assert a violation off a rendered hex alone.
Use the builder's returned **`bindingProof`** (nodeId + prop + boundVariable read-back receipts):
spot-check a few live and, if consistent, mark D2 verified-via-proof. Only FAIL D2 if a node has a
visibly RAW value the proof does not cover (e.g. a documented gradient the builder admits).

### D5 — Library utilization + duplicate + variant correctness + §1I authenticity

- **§5F duplicate:** no leftover-original-under-new, no double-built frame, no redundant wrapper.
- **Variant correctness:** no default-then-overlay, no feature-axis wrongly ON/OFF, the right MODE
  (e.g. compact header, not default).
- **§1I — TARGET-LIBRARY AUTHENTICITY (verify EVERY review).** This is the LOOK-ALIKE TRAP at the gate.
  A redesign that cloned the original instead of rebuilding in the target library passes D1/D2/D6 by
  definition — it matches the original perfectly, its nodes are instances, tokens resolve — so the
  component-key check is the ONLY catch. The trap: the original file's library has same-named components
  with DIFFERENT keys, so a clone is indistinguishable except by key (a screen can ship most of its
  components as original-library clones and still pass a full advanced-model review).
  - Read EVERY instance's `mainComponent.key` (`get_nodes_info`, recurse into top-level organism
    instances) and check membership in the target catalog. Trust the builder's `catalogKeyAudit` only
    after spot-checking 2–3 keys live; if absent, run the check yourself.
  - A non-target component is acceptable ONLY when the target genuinely has no equivalent AND the
    builder's `catalogKeyAudit` carries a sound `gapJustification`. A clone of something the target HAS
    = FAIL (major). A non-catalog key without justification = flag the L2 gate miss.

### D6 — Production-level, side-by-side (senior-designer judgment)

Leading/line-height rhythm, pattern consistency across repeated rows/cards, visual hierarchy. Structurally
correct but flat / uneven / crude = D6 FAIL. **The original is the reference for HOW, not just WHAT:**
judge whether the build reproduced the original's intent (which components, which variants, how combined)
with the new library, matching feature + design + quality + aesthetics. All-parts-present but combined
more crudely than the original = D6 FAIL.

**Hierarchy gate (assert these conditions BEFORE scoring PC9/PC11 — judge weight, don't read).** Hierarchy
inversion and urgency mismatch survive a *sharp* read because you can read the small text and rationalize
a weak hierarchy as fine. The gate is the outcome, not a ritual: setting legibility aside (judge by size,
weight, contrast, color-area, whitespace), assert each condition holds and cite the evidence:

- the screen's PRIMARY SUBJECT carries the most visual weight (not a badge/price/metadata) → else **PC9**;
- the PRIMARY ACTION stands out as the single rationed accent;
- grouped surfaces read as distinct groups — boundaries survive, cards don't melt into one column → **PC9**;
- the MOST URGENT / highest-stakes state is the most prominent, never the weakest → else **PC11**.

Compare against the original frame — it is the reference for intended weight. To judge weight independent
of content you may assess relative size/area directly, or blur the screenshot as an aid (Gaussian radius
≈ 8 via Pillow; `save_screenshots` has no blur param, so it is local post-processing). The blur is one
optional technique; what the gate requires is the four asserted conditions with evidence, not the blur.

**Score against the Production-Craft enum (PC1–PC13).** These are the recurring craft misses that pass
completeness yet read as "not production." Walk the build region-by-region and check each class — a hit
is a D6 FAIL with a five-part finding. (Some have a mechanical sibling in L2/R1; if one reached you, flag
the `l2GateMiss` so the floor tightens — but still report it.)

| ID | Defect class | Detection cue (screenshot + one structural read) |
|----|--------------|----------------------------------------------------|
| **PC1** | Fake-distribute / edge-stretch | A fixed-count control row (filter strip, toolbar, stat strip) spread across the full width via children `FILL` or `itemSpacing > 48`, leaving dead gaps. Fixed-count controls cluster compact + left/space-between, never stretch. |
| **PC2** | Missing field affordance | A select / input / dropdown rendered as bare text + chevron with **no field box** (no bound stroke/fill/radius). A control must look like a control. |
| **PC3** | Destructive action not red | A delete / trash / remove / 회수 icon not bound to the error/destructive color token (neutral-grey trash where the original was red). |
| **PC4** | Wrong icon chrome | A plain inline/directional icon wrapped in a bordered button box (or vice-versa) vs the original's treatment — adds weight or flips the signifier (a move-arrow reading as a dropdown chevron). |
| **PC5** | Missing implied separator | A grouped control set (search+download, segmented actions, inline stats) missing the divider/separator the pattern implies. |
| **PC6** | Excess default part visible | A component's own default slot / footer / legend / placeholder still showing (judgment backstop to R1 (f)). |
| **PC7** | Rhythm / hierarchy crudeness | Uneven leading, inconsistent row heights across one repeated list, >2 primary emphasis points, flat or inverted hierarchy. |
| **PC8** | Un-componentized repetition (maintainability) | N≥3 repeated rows/cards built as raw frames or raw clones instead of instances of ONE library/local component — a designer can't edit one and update all. Mostly an L2 catch (suspect → probe → decide); at the gate, confirm the repeated rows are instances and **do NOT score raw uniformity as a "consistency" strength** — uniform raw repeats ARE the defect, not a virtue. |
| **PC9** | Inverted / weak hierarchy | Judging by visual weight (per the hierarchy gate below), the screen's PRIMARY SUBJECT does not carry the most weight — a status badge / metadata / price out-shouts the title; or cards dissolve into one undifferentiated column because their boundary is too weak to read as a group. Distinct from PC7 (rhythm): PC9 is specifically *the wrong element winning at a glance*. A sharp render hides this because you can still read the small text — judge weight independent of content (size/contrast/area), optionally blurring as an aid. |
| **PC10** | Icon-family inconsistency | One screen mixes icon families / weights / grid sizes (thin-outline header icons + filled tab icons + ad-hoc mini glyphs inside grey circles). L2 (g6) flags it mechanically; at the gate confirm one family + one weight per screen. Mixed = the clearest "assembled, not designed" tell. |
| **PC11** | Urgency / emotional weight mismatch | The screen's MOST important state is rendered WEAKEST — a time-critical alert that demands immediate action shown as a small low-contrast pill while decorative metrics dominate; a high-significance outcome (a win, an approval, a milestone) styled identically to a routine row. Visual weight must track *stakes*: the element the user most needs to notice or feel should win the squint. The original's intent is the reference; under-weighting a high-stakes moment = FAIL. |
| **PC12** | Dead-space / under-fill | A short-content screen leaves a large vacuum (200–400px of empty surface above the tab bar) that reads as *broken/unfinished*, not minimal. Minimal has intentional rhythm; a vacuum has none. The fix is a designed fill (recommended next action, related content, a true empty-state composition), not stretched gaps. Pairs with the empty-state rule but applies to *populated* screens whose content is simply short. |
| **PC13** | Redundant label / badge | A label, chip, or **status badge that restates what an adjacent icon + headline (or a visible countdown / value) already conveys** — the state is already legible without it, so the badge is dead weight (no-redundant-labels). **The trap this catches:** a reviewer checks whether the badge is *styled* correctly and never asks whether it should *exist*, affirming dead weight as "correct treatment." For every intentionally-added label/chip/badge, ask **"does this carry information the icon / headline / value beside it does not already convey?"** — if not, **remove it** (don't restyle it). Distinct from PC6 (a component's leftover *default* slot): PC13 is an *added* element duplicating meaning already present. A sibling element earns its place only when it states a genuinely *different* fact, not a synonym of the one beside it. |

This enum is **append-only**: every production-craft miss a user catches that is not already covered
becomes a new PC row (mechanical-sibling pushed to L2/R1 if checkable, else a judgment line here). That is
how the bar rises each cycle — the gate learns from every catch, the way completeness learned from
inventory. Also score the build against this skill's craft rules (dynamic auto-layout + the
1200/1600 resize test, component-first, padding/gap ownership) — a violation is a D6 FAIL on its own.

Run D6 only after D1–D5 are clean.

### D7 — Library Pattern Adherence + Memory Curation

You (reviewer) are the **curator**, not just the validator. D7 runs after D1–D6 (never instead of them).

**1. Compliance check (progressive load — same discipline as the builder):**
As you walk each region of the built screen, scan the library memory index for `pattern_*` entries
matching that region's element types. Load only the matching files. Check whether the built placement
follows the pattern. A violation here is a D7 FAIL with a concrete fixInstruction.

**2. Proposal review:**
Read `memoryProposalsPath` (from the builder's return JSON). For each builder proposal:
- **Accept**: promote `status: tentative → confirmed`, add this screenId to `confirmedBy`
- **Reject**: remove from proposals JSON with a brief reason
- **Edit**: correct the rule body before accepting

Return an updated `memory-proposals.json`. The orchestrator calls `figma-playbook apply` after PASS.

**3. Active observation:**
As you review, independently note any pattern or learning from this screen not already in memory.
Add new tentative entries to the proposals file.

**4. Channel A on D7 violation:**
If a D7 violation is found and the relevant pattern entry is `tentative` (only one confirming screen),
you MAY run `Skill('figma-playbook') learn --library <librarySlug>` inline to find authoritative evidence in the
library's own documentation pages before issuing a definitive finding. A tentative pattern cannot be
treated as a confirmed convention without corroborating evidence.

**D7 does NOT block PASS** on its own. A D7 finding is reported but the screen can pass D1–D6 while D7
findings are recorded for the next round's fix loop. Exception: if a D7 violation also constitutes a D1
or D6 failure (e.g. placing search in the wrong location causes a feature-completeness miss or a crude
layout), the D1/D6 finding is the FAIL trigger.

**Add to reviewer return JSON:**
```json
"memoryProposalsPath": "design-system/_build-cache/<screenId>/memory-proposals.json",
"proposalActions": { "accepted": 3, "rejected": 1, "edited": 1, "added": 2 }
```

---

## Delta-review mode (re-review after builder fixes)

When reviewing a fix iteration, do ALL THREE — never only check the fixed node:
1. **Verify fixed findings:** confirm each flagged finding from the prior round is actually resolved
   (not just obscured or moved).
2. **Re-run the full L2 floor:** fast `scan_nodes_by_types` + `get_nodes_info` pass; a fix can
   introduce a new raw value, a new overflow, or leave a new default visible.
3. **Fast full-frame visual scan:** `save_screenshots` at `maxDimension: 2048`; scan the whole frame
   for any regression introduced during the fix (new label mismatch, glyph that disappeared, new
   component default surfaced).

A delta-review that only checks the fixed node WILL miss regressions.

---

## Feedback quality bar — every finding carries all five

A finding is never just "X is wrong." Give the builder enough to fix it AND the lens to prevent the class:

- **where** — `dimension` + `nodeId` + the element in plain words.
- **what** — the concrete defect.
- **why** — the user/design impact ("the user can no longer download — the function was lost").
- **mindsetNeeded** — the perspective that catches and prevents it ("verify each icon's MEANING vs the
  original"; "compare leading row-by-row, not at a glance").
- **fixInstruction** — the specific action: node + property + value.

---

## Output (your final message IS the JSON)

```json
{
  "screenId": "...",
  "round": 1,
  "reviewerModel": "opus",
  "builtFrameId": "...",
  "originalFrameId": "...",
  "verdict": "PASS | FAIL",
  "fixedSinceLastRound": [
    { "ref": "...", "description": "...", "nodeId": "..." }
  ],
  "findings": [
    {
      "dimension": "D1 | D2 | D3 | D4 | D5 | D6",
      "severity": "critical | major | minor",
      "where": "nodeId + plain words",
      "what": "...",
      "why": "...",
      "mindsetNeeded": "...",
      "fixInstruction": "node + property + value",
      "l2GateMiss": true
    }
  ],
  "strengths": [ "..." ]
}
```

Include `"l2GateMiss": true` on any finding that the L2 floor should have caught (raw value, coverage
gap, leftover default, invisible icon, non-catalog key). This signals the upstream floor needs tightening.

---

## Hard rules

- **READ-ONLY.** Never create/edit/delete nodes. You report; the builder fixes.
- PASS only when every D1–D5 check is clean AND D6 is production-level vs the original.
- Always review **against the original** — never in the abstract.
- Your findings should skew toward D1-§1H (function/asset meaning), D5 variant correctness, and D6
  craft — the things L2 structurally cannot catch. If you find a mechanical defect, flag it as an L2
  gate miss but do not bounce the screen on that alone if the builder can inline-fix it.
- BAR-RAISER thoroughness never drops — cut rounds by demanding strong builder self-eval, not by
  accepting a lower bar per round.
- LOOK-ALIKE TRAP: the original library has same-named, different-key components — always verify key ∈
  target catalog; never accept "it looks the same as the target" as proof of authenticity.
