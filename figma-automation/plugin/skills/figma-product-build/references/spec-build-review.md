# Per-screen build + review protocol (spec-as-reference)

This is the operational detail behind the three-layer loop. It mirrors `/figma-redesign`'s
builder-brief / completeness-floor / review-protocol, with one structural change: **there is no
original frame**, so the **spec** (`DESIGN.md` `## Screens` intent + `COPY.md` strings) is the
completeness reference at every layer.

## Contents

- **STEP 4.5** — plan-completeness gate (after spec=Step 4, before build=Step 5)
- **The build brief** — orchestrator → builder
- **L1** — builder self-eval ritual (vs the spec + the concept.md craft bar)
- **L1.5** — adversarial "are you sure?" self-reflection challenge (always before L2/L3): squint test +
  a11y/contrast + touch-target, plus the motion-handoff rule (document non-trivial concept Motion, don't fake it)
- **L2** — mechanical pre-gate, checks (a)–(j) incl. touch-target / accent-budget / icon-consistency
- **L3** — two parallel verifiers (D1 = vs spec; D6 craft incl. the hierarchy/squint gate + the concept.md craft bar)
- **Async / R5**, **Concurrency vs heavy imports**, **Recovery**, **Done bar (per screen)**

## STEP 4.5 — PLAN-COMPLETENESS GATE (mandatory, after spec=Step 4, BEFORE build=Step 5)

> A missing screen / flow / state caught HERE is cheap; caught at build time it's expensive; caught by the user after build is a credibility hit (the "where's the login screen?" failure). The pipeline has a rigorous *build* gate (L1.5/L2/L3) but that only checks "is each screen built well" — it cannot catch "a screen that should exist is missing from the plan." So before Step 5 (build), the orchestrator runs an **adversarial plan-completeness review** of the Step 1–4 outputs (`prd-analysis` screen list + `direction/concept.md` + `DESIGN.md` + `COPY.md`) against the PRD. Do NOT enter the build with an incomplete plan.

Check, and resolve every gap WITH THE USER (add the missing screens/states to the list + spec, loop until solid):

- **Flow completeness — walk each user flow end-to-end and list the screens it IMPLIES, then diff against the screen list.** Whole flows imply standard screens that a feature-by-feature PRD reading silently drops: **auth → welcome/landing + login + signup + password-reset**; a list → list + detail + empty; a create flow → form + confirm + success + error; a purchase → cart/summary + payment + result; onboarding → welcome + steps + done. If the list has "signup" but no "login", the flow is incomplete.
- **State completeness** — every screen has the states its data behavior requires (default / loading / empty / error / success). A screen that fetches → needs loading + empty + error; a form that submits → needs success + error.
- **Standard-screen coverage** — scan for the easily-missed-but-expected screens: login/logout, settings, search, notifications-empty, password reset, edit-vs-create variants, permission/error screens. An app that lets users *sign up* almost always needs them to *log in*.
- **PRD traceability** — every PRD feature / persona / flow maps to ≥1 screen, and every screen traces to the PRD. Orphan features (no screen) and orphan screens (no PRD basis) are both gaps to resolve.
- **Direction + soul presence (the anti-flat backstop).** `<sot>/direction/concept.md` MUST exist with its frozen sections (Signature DNA, Meaning-encoding philosophy, "What this is NOT", Craft toolkit per register, Register map), AND every screen's `DESIGN.md` block MUST carry its **populated art-direction fields** (Metaphor / Expresses / Hero+meaning / Craft moves / Signature usage / Motion, each bound to a concept.md section). A missing `concept.md`, or art-direction fields left blank/boilerplate, means the build has **no craft bar** — the L3 craft reviewer silently falls back to generic patterns and passes flat, assembled screens (this is precisely how a build comes out lifeless / assembled). If `concept.md` is absent → STOP and run Step 2 (direction) first; if the spec flattened the direction (fields blank) → send it back to Step 4. Do NOT enter the build without the soul layer.

Output a short gate report: implied-vs-present screen diff, missing states, the concept.md/art-direction presence check, and the resolved additions. Only when the plan has ZERO unresolved completeness gaps does the build (Step 5) begin. (This is the gate that would have caught the missing login screen — and the missing direction layer.)

## The build brief (orchestrator → builder)

**Context budget — pre-digest, do NOT firehose (a builder that reads too much dies "Prompt is too
long" before it builds anything).** The `figma-builder` runs with a large base context (broad tool
schemas). If the brief tells it to load 2–3 skills AND read several big files (DESIGN.md, COPY.md,
the recipe, a multi-KB catalog/palette map) AND open multiple PNG references, it overflows mid-setup
and produces nothing. Instead, the orchestrator **pre-digests once** into a single compact cheat-sheet
(e.g. `_build-cache/kit-keys.md`: the component/icon/style keys + local color spine + the condensed
binding recipe + the common build rules + shared-chrome ids + the self-eval checklist + a hard
"read ONLY this file; never open the raw catalog; cap self-eval screenshots" discipline). Then each
per-screen brief is **lean**: "read that one cheat-sheet, follow it; here is your screen's layout
intent + COPY strings **inlined**; here is your x-lane." Builders load **no** skills upfront (the
discipline is internalized in the agent prompt, and the cheat-sheet *digests* the `figma-design-patterns`
+ `rad-spacing` craft rules into compact form — and the full craft skills are then read **progressively,
just-in-time at the phase that needs each** (the spacing/layout skills when composing layout, mechanics
when a tool question arises), one at a time, never an upfront firehose), read the cheat-sheet, and
inline-receive the spec/COPY — so they spend context building, not reading. Cap self-eval screenshots (≤2 per state) since
images are the heaviest cost.

The `figma-builder` agent already knows the figma-mcp-express rules and the absolute design-system
constraints (component-first, bound tokens, auto-layout, no placeholder). Give it, per screen (inlined
or via the compact cheat-sheet — NOT as a pile of file paths to read):

```
- **THE SCREEN'S INTENT — inlined as text and placed FIRST, never a path to "go open":** the screen's
  **Hero + what it means**, its **1–3 Craft moves**, its **Signature usage**, and the top 2–3
  **"What this is NOT"** anti-patterns — lifted from the DESIGN.md art-direction fields + the matching
  `concept.md` slice. It is short; inlining it (rather than handing over a path) is what makes the builder
  engage the *meaning* before the *mechanics*. Require the builder to commit a 1–2 sentence **design plan**
  before its first mutation — a decision ("what wins the glance + the moves"), not a field echo — and that
  plan is what L1 direction-fidelity + the L1.5 challenge hold the screen to. (`concept.md` / `DESIGN.md`
  stay available as paths for depth, but the build-SHAPING intent travels INLINE, never as "read this.")
  This is a reorder, not a new gate: it costs nothing against the context budget and adds no artifact —
  it just stops the builder opening the component inventory first and skimming past the soul.
- build-file `fileKey` (resolve the live `channel` by it each op group — ids churn) + output pageId,
  palette-map.json path, ledger path <sot>/_build-cache/<screenId>-ledger.json
- libraryFileKey + scratch catalog path
- library SOURCE shape (`local` | `subscriber`) + the binding model from pre-flight: the local accent
  token id(s) and the rule "bind ONLY accent surfaces (primary CTA fill, status/live accent, focus ring,
  active-tab indicator) to the accent token; imported instances keep their neutral/spacing/radius/type
  bindings — do not re-bind them". The verified import→instance→accent-bind recipe path.
- **targetPlatform** — the confirmed platform list from `foundation.json` (echoed from prd-analysis).
  This drives (a) canonical device width (mobile ≈ 390×844, desktop ≈ 1440-wide — use
  `deviceFrameDefaults` from foundation.json), (b) which navigation model to use (bottom tab bar vs
  top nav/sidebar), (c) touch-target sizing (≥44pt on touch platforms), (d) hover availability (NONE
  on touch), and (e) platform-correct microcopy. Include the path to
  `figma-product-foundation/references/platform-conventions.md` so the builder can resolve any
  platform-specific pattern question inline.
  **Mobile safe area (iOS 390×844):** root screen frame must be an auto-layout frame with
  `paddingTop: 59` (44px status bar + 15px inset) and `paddingBottom: 34` (home indicator).
  Usable content area = 390×751px. Apply via `set_auto_layout(screenFrameId, paddingTop:59, paddingBottom:34)`
  — NOT `move_nodes` (auto-layout children ignore direct position changes). Missing safe area = L2 FAIL.
- DESIGN.md path  (tokens + the `### <screenId>` layout-intent block — its build contract; it carries
  the per-screen art-direction fields **Craft moves / Creative mode / Signature usage / Motion** that
  Step 4 pulled from concept.md — EXECUTE these, don't re-choose them)
- COPY.md path    (the `screens.<screenId>` string map — the EXACT strings to render, verbatim)
- direction/concept.md path — the frozen Direction contract. The builder builds to the spec's carried
  craft fields; concept.md is the craft bar the L3 reviewer judges against (**Signature DNA**,
  **Meaning-encoding philosophy**, **"What this is NOT"**), so the builder should keep the Signature DNA
  present and avoid every "What this is NOT" anti-pattern.
- foundation/ path (design-language + signature-layer + interaction + brand — the source for any craft
  detail the spec leaves open) AND the saved visual references: `direction/refs/` (anchor app screens,
  from Step-2 grounding) + `foundation/refs/` (kit component galleries). Instruct the builder to **open
  these images with the Read tool** to ground its variant/layout choices in the real anchor look + the
  actual kit components, not just the prose.
- **visualResearch** — preloaded `reference_pack` / `asset_pack` JSON from `visual-researcher`, usually
  assembled during the foundation/spec steps (Steps 3–4) and filtered to this screen. References are pattern evidence; assets are
  concrete local files. The builder may use these saved paths, but must not browse for replacements or
  silently substitute weaker candidates. Empty is allowed only when the PRD/spec genuinely needs no
  external media.
- **built-siblings** — the frame-ids + screenshot paths of already-built screens (at minimum the
  proving/canon screen). Instruct the builder to `save_screenshots` + `get_node`/`scan_text_nodes` them
  and **match the established visual language**: same container padding + card rhythm + header height +
  type scale, and **re-instance the shared organisms** (tab bar, header, repeated card) rather than
  redrawing look-alikes. The screens must read as one product (see SKILL.md "Cross-screen visual
  consistency"). Empty on the canon screen itself (nothing built yet).
  > **Pre-digest the canon spine as NUMBERS so the consistency check survives the context budget.** "Open
  > every sibling PNG" collides with the screenshot-cap discipline above, and under budget pressure the
  > builder drops the image reads → dialect drift. Pre-empt it: the orchestrator extracts the canon's
  > spine ONCE — container padding scale, card rhythm/gaps, header height, type scale, and the
  > **shared-organism component keys** (tab bar / header / repeated card) — into the `kit-keys.md`
  > cheat-sheet as concrete values. The builder then matches the numbers + re-instances by key WITHOUT
  > loading many PNGs, and still views the single canon screenshot once to ground the gestalt. This is
  > what makes the L1.5 `cross-screen-consistency` row provable rather than aspirational.
- the screen's prd-analysis entry (states/actions/rules — what must exist)
```

**Layout planning — the orchestrator pre-plans the board grid BEFORE dispatching any builder.**
Use `figma-product-build/scripts/compute-layout.py` to compute a tidy grid: one row per screen
(its state frames left→right), rows grouped by IA section with a section header, consistent
gutters. The script reads `state.json`'s `layoutPlan.sections` + `screens[].frameIds` and
outputs each frame's exact `{x, y}` origin. Hand those exact origins to the builders — builders
NEVER pick arbitrary far-flung x/y coordinates on their own. After all builds are done, the same
script's `moveOps[]` output can reposition frames into the grid in a single batch.

**Node ID and coordinate discipline — live-resolve before every placement.**
Brief-time IDs and coordinates are hints, not ground truth: a session summary can record a frame
at x≈22000 while it actually lives at x≈1814, and `move_nodes` coordinates are parent-relative
(not absolute canvas), so passing a large "absolute" value flings the child off-canvas. Before
any placement or edit the builder MUST: `search_nodes` by name → `get_node` on the live id →
read `absoluteBoundingBox` → derive the target offset. After a fresh rebuild, delete the
superseded frame and confirm via `search_nodes` that exactly ONE frame with that name remains.
See `figma-mcp-express/references/gotchas.md` "Node IDs and placement coordinates" for the
full three-cause breakdown.

`<figma-product-build-skill-dir>` is the installed `figma-product-build` skill directory shown in
Codex's available-skills list.

```bash
python3 "<figma-product-build-skill-dir>/scripts/compute-layout.py" \
  --state <sot>/governance/state.json \
  [--frame-w 390] [--frame-h 844] [--state-gap 48] [--row-gap 120] [--section-gap 240]
```

Instruct the builder:
- "INTENT FIRST — before placing a single component, read your inlined screen intent (hero + meaning,
  craft moves, signature usage, 'What this is NOT') and commit a 1–2 sentence design plan: what wins the
  glance on THIS screen + the specific moves you'll use to get there. Starting from the component inventory
  instead of the intent is the flat-output failure; your design plan is what L1 direction-fidelity and the
  L1.5 challenge hold the built screen to."
- "SETUP — read the ONE cheat-sheet (`_build-cache/kit-keys.md`) first: keys + binding recipe + build
  rules, condensed. Then read the craft skills **PROGRESSIVELY — just-in-time at the phase that needs each,
  one at a time**, never a 4-skill upfront block (that overflows mid-setup → 'Prompt is too long' → you
  build nothing). The ladder: when you start COMPOSING layout & spacing, read `figma-design-patterns`
  (auto-layout + `references/padding-strategy.md` + composition) and `rad-spacing` **before you set gaps and
  padding** — that is where spacing / placement craft enters and exactly where builds go weak; during
  POLISH read `frontend-design`; consult `figma-mcp-express` mechanics the moment a specific tool / op
  question arises. Read → apply → move on, so context stays bounded but the craft skills DO get read — the
  failure to avoid is BOTH the upfront firehose AND never opening the spacing/layout skill at all. (Full-
  load-every-run is the single-screen `/figma-redesign` default; this product brief overrides it with this
  progressive ladder.)"
- "Build this ONE screen from library instances. The `### <screenId>` block in DESIGN.md is your
  layout contract: build the regions it names with the components/families and FILL/HUG/FIXED behavior
  it specifies. Pull all visible text VERBATIM from `COPY.md screens.<screenId>` — invent no copy."
- "USE `figma-design-patterns` + `rad-spacing` as you build — every frame satisfies the CORE RULES and
  trips ZERO anti-pattern flags (dynamic auto-layout + resize test, tokens not raw values, hierarchical
  spacing from library variables, component-first, semantic layer names, no default/excess slots)."
- "CRAFT AUTONOMY: where the spec is silent on a UI/UX detail, design it cleanly from `foundation/` +
  best practice — never skip or stub it. But if you feel you must invent a PRODUCT decision (a
  behavior, a data rule, a missing screen), STOP and return `escalate` — do not guess."
- "VISUAL RESEARCH: open the supplied `direction/refs/*.png` + `foundation/refs/*.png` and any `visualResearch.references`
  before composing. Transfer patterns, not pixels. If you need missing references or concrete media,
  STOP and return `{blocked:true, reason:'visual_research_required', referenceRequests:[...],
  assetRequests:[...]}`. Each request item MUST include a detailed natural-language `brief` explaining
  the desired usage, aesthetic, dimensionality/style (`flat`, `3D`, `4D/motion-like`, `isometric`, etc.),
  quality bar, constraints, and anti-targets, plus structured fields: `targetScreen`, `usage`,
  `placement`, `targetSize`, `sourcePreference`, `candidateCount`, `styleKeywords`,
  `desiredQualities`, `mustHave`, and `avoid`. Reference requests also need `referenceKind` and
  `screens`, `minSourceYear: 2024`, and `trendFocus`; asset requests also need `type`, `assetKind`,
  `query`, and `preferredFormat` or `outputFormats`. Do not browse or substitute assets yourself. When
  `visual-researcher` returns candidates, compare them in your layout context and choose one; do not
  blindly use rank 1. Record the chosen candidate id and reason in your ledger/self-review."
- "Render every state the screen requires (per the prd-analysis entry + COPY.md state strings)."
- "Return JSON: `{ screenId, builtFrameId, ledgerPath, selfReview, finalScreenshot, gaps[],
  escalations[], referenceRequests[], assetRequests[], importThreadHung }`."

## L1 — builder self-eval ritual (vs the spec + the concept.md craft bar)

After building, the SAME builder runs the adversarial self-check (resume via a follow-up message). It must
prove each clear with an artifact, judged against the SPEC and the `concept.md` craft bar:

- **Completeness floor** — every region in the `### <screenId>` block is built; every required state is
  rendered; every `COPY.md` string for the screen appears on the canvas (diff the screen's string map
  against `scan_text_nodes` — OCR is unreliable, use the text scan).
- **Content fidelity** — text matches `COPY.md` verbatim; no placeholder ("Title", "Label", "Item 1",
  "swap it", lorem); no English stand-in where Korean copy is specified.
- **Token binding** — no raw hex, no hardcoded px; every fill/spacing/radius bound via a library
  variable (read back `boundVariables`).
- **Component-first** — every element whose role maps to a library kind (button, input, select, nav
  row, icon, modal…) is an INSTANCE, not a raw frame faking it.
- **Auto-layout + resize** — every structural frame has `layoutMode`; FILL/HUG correct; `itemSpacing`
  ≤ 48; mentally resize the wrapper (1200/1600) — no clip, no rigid gap, no overflow.
- **Craft** — score against `figma-design-patterns` CORE RULES (visual hierarchy, spacing rhythm,
  repeated-rows-as-one-component, intentional variants). A CORE-RULE violation = not done.
- **Direction fidelity (concept.md craft bar)** — self-check the screen against `direction/concept.md`'s
  exact frozen sections — the SAME bar the Opus reviewer (D6) uses, caught here cheaply first:
  **Signature DNA** — is the motif / form-language / signature device actually carried, or is this
  generic kit placement? **Meaning-encoding philosophy** — does the hero carry its meaning by hierarchy,
  with NO redundant badge/label restating what an adjacent icon or value already conveys (PC13)?
  **"What this is NOT"** — does the screen trip any listed anti-pattern / off-brand move? A
  spec-complete screen that misses the Signature DNA or hits a "What this is NOT" item is NOT done.
  **Then hold it to the design plan you committed before building** — you named what should win the glance;
  if the built screen's actual focal weight landed somewhere else, that drift between your own opening
  decision and the result IS the flat-output tell. Fix the screen to the plan (or, if the plan was wrong,
  state the better decision and rebuild to it) — never quietly ship the drift.
- **Platform-appropriateness** — every element must conform to the confirmed `targetPlatform`.
  Specifically: touch targets are ≥44×44 pt on touch platforms; no hover-only affordances or
  hover-reveal actions exist on touch platforms (each must be tap-reachable); navigation follows the
  platform convention (bottom tab bar on mobile, top nav/sidebar on desktop); and ALL microcopy
  strings that name an input gesture or upload method are platform-correct (no "드래그", "클릭",
  "마우스를 올리면" on a mobile screen; no "탭" on a desktop-only screen). Cross-reference
  `figma-product-foundation/references/platform-conventions.md` Part 2 (anti-pattern table) against
  every visible string on the canvas. Any anti-pattern string from that table on the wrong platform
  = NOT done.
- **DRY / componentization** — any **composite** unit that appears more than once (card, list/table row,
  stat cell, payment row, message bubble, bracket node, **skeleton placeholder card**) MUST be ONE
  (file-local) component placed as **instances**, not copy-pasted duplicate frames. Read back the repeated
  nodes: if they are sibling FRAMEs with identical child-name signatures (not INSTANCEs of one master),
  that is a copy-paste duplication defect — componentize before claiming done. This applies to **authored**
  structures too (skeletons, not just library kinds), which is the crack the library-only D2 audit misses.
- **Cross-screen consistency** — this screen must read as one product with the already-built siblings,
  not a fresh dialect. Actually VIEW the canon + sibling screenshots supplied in the brief
  (`built-siblings`) — opening them is not optional, and matching the prose description is not a substitute
  for looking at the pixels. Match the established spine: container padding scale, card rhythm, header
  height, type scale. Shared organisms (tab bar, header, a repeated card) MUST be **instances of the
  canon's component** (same component key) — never a redrawn look-alike. Record the siblings you viewed +
  the spine numbers you matched + the shared-organism keys you reused as evidence; "I matched the language"
  is a claim, the viewed-and-matched record is the proof.

The builder **loops on its own findings** until the self-eval is clean, then returns `selfReview` with
the evidence.

## L1.5 — adversarial "are you sure?" SELF-REFLECTION CHALLENGE — MANDATORY, ALWAYS before L2/L3

> **THIS STEP IS NON-NEGOTIABLE.** The orchestrator MUST resume the SAME builder for this challenge after EVERY build and after EVERY fix round. Do NOT skip it to save time. Do NOT proceed directly to L2 after L1 self-eval. The user has had to remind the orchestrator of this step repeatedly — treat any omission as a process failure. The L1.5 challenge is the cheapest defect-catcher in the pipeline (builder-time vs Opus-reviewer-time = ~10:1 cost ratio). It exists because builders reliably skim their own output; the challenge forces them to prove it adversarially.

**Reuse figma-redesign's Phase 1.5 verbatim — do NOT reinvent it** (`figma-redesign/SKILL.md` ~line 167 +
253). A builder's first "done" is a *claim*, not proof — builders skim their own work, so push back BEFORE
spending the expensive Opus gate. **RESUME the SAME builder** (a follow-up message, not a fresh agent) with the
adversarial dry-run challenge:

> "Are you sure you're done? Run the reviewer's **D1–D6 on yourself, adversarially, against the SPEC**
> (`DESIGN.md` `### <screenId>` + `COPY.md` strings + prd-analysis states — NOT your own ledger): diff
> EVERY COPY string on canvas (`scan_text_nodes`); render-check EVERY state with a fresh screenshot; read
> back EVERY authored binding; run the catalog-key audit; check **DRY** (every repeated composite is an
> INSTANCE of one component, never a copy-pasted frame — and if you already made a component, that you
> actually USED it); confirm loading mirrors the loaded layout with no lurch and chrome is identical
> across states; score craft vs `figma-design-patterns` CORE RULES. **Prove each clear with an artifact.**
> **Pass the squint** — judging by visual weight alone (size, contrast, color-area, whitespace; not by
> reading the words, which a sharp render lets you rationalize away), confirm the primary subject carries
> the most weight, the primary action stands out, grouped surfaces read as distinct groups (card
> boundaries survive), and the most urgent state is the most prominent — never the weakest. If a badge or
> metadata out-shouts the subject, or the most important state renders weakest, the hierarchy is inverted
> — fix it with size/weight/accent, not by editing copy. (To judge weight independent of content you may
> assess sizes directly or blur the screenshot as an aid — Gaussian radius ≈ 8 via Pillow.) **Then read the
> spacing as rhythm, not just alignment:** do related items sit tight and separate groups/sections sit
> clearly apart (proximity grouping survives the squint), is the gap ratio between levels deliberate (~2x,
> not one default step everywhere), and does the density match the reference for this pattern — nothing
> crammed against an edge, no vacant dead-space padding a thin screen? A screen where section breaks read
> like item gaps, or that is uniformly loose / tight, is weak placement even with every element present —
> fix the gaps to the rhythm, citing the specific one that's too tight or too wide. While the
> screenshot is open, also run the **a11y pass**: every interactive target is ≥ 44pt, icons share one
> family and weight, and **text/background contrast** clears WCAG AA (≈ 4.5:1 for body, 3:1 for large
> text / UI affordances) — a light-on-light label, a low-contrast placeholder, or accent text on an
> accent fill is an a11y FAIL, not a taste call. If you find ANY gap, fix it, re-run L1 on the touched
> sections, re-screenshot, and answer again."

> **Motion is a SPEC, not a claim — Figma is static.** When the screen's `concept.md` Motion (carried into
> the spec's per-screen Motion field) is non-trivial — a signature settle/glow, a staged reveal, a
> transition that *means* something — the build does NOT pretend to animate it. Instead, **document the
> intended motion in handoff**: a short motion note (trigger → property → easing → duration → what it
> means) on the frame or in the ledger, and where the motion is a hero moment, a **Lottie poster frame**
> (the still that represents the loop) placed as the asset with the spec noted beside it. Claiming a
> static frame "animates" is a fidelity miss; a clear motion spec is the honest, build-correct deliverable.

When you already suspect specific defects from the returned screenshots, name them in the challenge (the
likeliest skimps: a too-large hero/cover pushing spec regions off-screen; a loading skeleton that doesn't
mirror the real layout; a built-but-unused component; an instance-override that diverges chrome between
states). The builder either **confirms good with evidence** → advance to L2, or **surfaces & fixes** issues
→ that is the challenge working, catching defects cheaply before Opus. A "done" that can't survive the
challenge never reaches the reviewer. (Same ritual re-runs after every post-review fix round.)

Only after the challenge clears does L2 run.

**L1.5 artifact (the harness).** After the challenge, the builder saves its resume output to
`<sot>/_build-cache/<screenId>/l1.5-r<n>.md`: a per-item PASS/FIXED list plus the path of a
screenshot taken AFTER its last mutation. The orchestrator checks for this file before invoking L2.
L2 will not start without it — "I did L1.5" is not an acceptable claim, the file is.

## L2 — mechanical pre-gate (deterministic, green before any Sonnet call)

No model judgment — scriptable checks, run by the orchestrator (Sonnet audit) on the builder's output:
- **(a) catalog-key** — every built INSTANCE key ∈ the target library catalog; AND the reverse
  (component-first): every library-kind role IS an instance, not a raw frame. **Run this as a
  deterministic OFFLINE script, never a live grep.** The builder returns its `catalogKeyAudit`
  (the list of component keys it instanced); feed those to `_build-cache/l2-catalog-check.py`
  (or the project's equivalent), which substring-checks each key against the target library's
  raw catalog JSON and exits non-zero on any MISSING (look-alike / wrong-library) key. The raw
  catalog is large (~9MB / thousands of components) — grepping it from inside a live agent HANGS
  the channel (a real failure mode); the offline script owns bulk membership. File-local organisms
  (remote:false, registered in the build-recipe) are passed via `--file-local` and skipped.
- **(b) spec-coverage** — every region in the `### <screenId>` block has a built counterpart; every
  required state rendered.
- **(c) string-coverage** — every `COPY.md screens.<screenId>` string is present on canvas (text-scan
  diff). This is the greenfield analogue of inventory-coverage. **Diff char-for-char against the exact
  COPY string — not "a node with similar text exists".** Mojibake/corruptions (a garbage syllable like
  `뷁`, a dropped middle-dot `·`, a wrong verb) and ANY builder-authored prose (e.g. a description not
  spelled out in COPY.md) must be proofread for correct Korean; gibberish/typo text (`보듈`, `남자부부`
  for 남자복식) is a content FAIL even when the surrounding strings match.
- **(d) no-excess** — every built node maps to a spec region/state (no stray invented structure).
- **(e) child-fits-parent / no occlusion** — no overflow/clip, AND on a fixed-height mobile frame every
  required region must render INSIDE the frame and ABOVE any pinned bottom bar/CTA. A content column fixed
  shorter than its content (or with no `paddingBottom` budget for a pinned CTA) renders its last region
  behind the opaque bar / off the frame edge — that region is invisible = FAIL (the canon pattern reserves
  `paddingBottom ≥ pinned-CTA height`). Never accept a builder rationalizing clipped/occluded content as
  "it scrolls" / "acceptable mobile behavior" — if a spec region isn't visible, it's a defect.
- **(f) raw-value** — scoped to **AUTHORED nodes only**: every fill/stroke the builder *created* binds to a
  design variable (or a published paint/text/effect style); no raw hex on authored frames/labels/dividers.
  **Imported library instances legitimately carry the library's own paints — NOT a violation; never flag
  them.** If the target library is style/raw-hex based (no color variables), the project's palette-map /
  build-recipe declares a localized color spine + a spacing policy (e.g. `raw-integers-allowed`, discrete
  scale) — judge against THAT, per CLAUDE.md Verification #8 precedent. Check the brief's token model.
- **(g) craft floor** — semantic layer names (no `Frame <number>`), no left-default variants, no
  visible placeholder slots.
- **(h) touch-target audit** (mobile/tablet only) — from the build's `scan_nodes_by_types` +
  `get_nodes_info` pass, every interactive node (role ∈ button / text-button / icon-button / nav-row /
  tab / chip / dropdown / input / pagination / toggle / tap-row) must have `min(width,height) ≥ 44` (iOS)
  / `≥ 48` (Android). The tappable bound is the node's own frame (the padded hit-area), not the glyph
  inside it. Report `touchTargetViolations`; any entry = FAIL (grow the frame / add padding). Skip on
  `desktop-*` / pointer platforms. (Sibling of `figma-design-patterns` CORE RULE 13.)
- **(i) accent-budget count** — count nodes binding the accent/primary token, clustered by role
  (primary-action / active-nav / urgent-status / active-filter / link / unread-dot / badge / decoration).
  More than **2 role-clusters** wearing the accent on one screen = `accentBudgetExceeded` (advisory →
  L3 confirms load-bearing vs noise). Catches "everything is accent, so nothing is" mechanically.
- **(j) icon-family consistency** — every icon INSTANCE must resolve to ONE icon system (one
  component-set / key namespace, one weight + grid size). Mixed families/weights/sizes on one screen =
  `iconFamilyMismatch` = FAIL. (Sibling of CORE RULE 10.)
Any fail → back to L1 (message the specific failures); never advance a red L2 to the reviewer.

**L2 artifact (the harness).** On PASS, L2 writes `<sot>/_build-cache/<screenId>/l2-r<n>.md`
recording checks (a)–(j) results per item. L3 is blocked until this file exists.

## L3 — Two verifiers in parallel (adapted: reference = spec, not an original frame)

The L3 gate is **two fresh READ-ONLY verifiers dispatched in ONE message (background) and AND-merged**:

| Verifier | Model | Owns (from the catalog below) |
|---|---|---|
| `figma-structural-verifier` | Sonnet | D1 completeness vs spec, D2 keys, D3 token binding, D4 auto-layout, D5 content = COPY verbatim, + the scriptable scans (touch-target / accent / icon / names) |
| `figma-reviewer` | Sonnet | D6 craft (incl. **concept.md craft bar** = Signature DNA + Meaning-encoding philosophy + "What this is NOT", cross-screen consistency, **platform-appropriateness**, DRY, **design-authority redirect**, **all-states equal rigor**) + §1G/§1H meaning |

Dispatch both, wait for BOTH (no short-circuit), then `PASS = structuralVerdict ∧ craftVerdict`; send the
combined findings to the builder in one fix round.

> **Both verifiers ALWAYS run — every round, every screen. A one-verifier review is NOT a gate.** The
> AND-merge is undefined with a missing half: a craft-only review never ran the touch/accent/icon/
> component-coverage/shared-organism scans, and a structural-only review never judged hierarchy or the
> concept craft bar. A screen that saw only one verifier is **ungated, not passed** — never advance it on
> a single verdict. (This is how earlier screens shipped with un-scanned touch targets and accent budget:
> the structural half simply never ran. If a verifier dies/returns nothing, re-dispatch it — do not fill
> the gap with the other's verdict.)

**`doNotFlagPath`** — include `<sot>/_build-cache/<screenId>/do-not-flag.md` in every dispatch prompt.
Both verifiers must read this file before writing findings and must NOT re-flag any `findingId` listed
there. Verified, signed-off JUDGMENT entries in this file are settled — re-flagging them wastes a round
and is a process failure.

Each verifier reads ONLY its rows of the catalog below (the items are labeled by dimension). The shared
preamble both use:

```
- You are READ-ONLY and adversarial. Build your OWN independent expectation of this screen from the
  SPEC + the frozen DIRECTION — do NOT trust the builder's ledger:
    * DESIGN.md `### <screenId>` block  → the regions/components/hierarchy/states that must be present
    * COPY.md `screens.<screenId>`      → the exact strings that must appear
    * prd-analysis `<screenId>` entry   → the states/actions that must exist
    * direction/concept.md              → the CRAFT BAR (figma-reviewer/D6 only): **Signature DNA**,
        **Meaning-encoding philosophy**, and **"What this is NOT"** — the screen must look like THIS
        product, encode meaning by hierarchy (not redundant badges), and trip none of the anti-patterns.
- D1 COMPLETENESS (adapted): every region, state, component, and string the spec requires is present
  on the canvas. "Missing" = in the spec, not on canvas. "Excess" = on canvas, not in the spec.
- D2 component fidelity: every INSTANCE key ∈ the target library catalog (no look-alikes).
  **Do NOT grep the raw catalog JSON — it is huge and grepping it live HANGS your channel.** Bulk
  key membership is already owned by the deterministic L2 script (`l2-catalog-check.py`); you only
  spot-check 2–3 keys live via `get_nodes_info` to confirm the L2 audit wasn't fabricated. If a key
  is genuinely in doubt, report it as a finding for the orchestrator's script to resolve — never
  grep the catalog yourself.
- D3 token binding (AUTHORED-node scope): every fill/stroke the builder created binds to a variable or a
  published style; authored text uses a text style; authored shadow an effect style. **Imported library
  instances may carry the library's own raw paints — that is NOT a violation; do not flag it.** If the
  library is style/raw-hex based, judge color against the project's localized color spine and spacing/radius
  against its declared policy (discrete raw integers allowed when no spacing vars exist) — read the brief's
  token model + `_build-cache/build-recipe.md`. Flag raw hex ONLY on authored nodes.
  **Fill bindings are NOT independently READABLE — do NOT gate D3 on them (false-negative trap).** No
  read surfaces a fill's variable binding: `get_node`/`get_nodes_info` flatten every fill to a resolved
  hex, and `get_design_context` at EVERY detail (compact/full/codegen) serializes fills only as
  resolved-hex dedup aliases in `globalVars.styles` (`s1=#ffffff`,…) — a variable-bound fill and a raw hex
  of the same value are byte-identical (proven with a positive control: a `set_fills variableId`-bound
  frame reads identically to an untouched one; zero `VariableID`/`boundVariables` appear for fills at any
  detail). Only EFFECT bindings emit `boundVariables`. So `globalVars` showing `sN`/hex is NOT evidence of
  "raw/unbound" — an earlier review FAILED a screen on exactly that inference and was WRONG. The ONLY real,
  readable fill violation is an OFF-PALETTE hex (a color value not in the project's token spine). Trust the
  builder's bind-op success (`bind_variable_to_node`/`set_fills variableId` return the bound `variableId`)
  for palette-matching values; flag ONLY off-palette colors. (⏳ MCP gap figma-mcp-express#27 — REVISE D3 to verify fill binding via reads once that lands.)
- D4 auto-layout: run `scan_nodes_by_types(builtFrameId, ["FRAME"])` — any FRAME with `layoutMode="NONE"` (excluding named spacers + 0-size decoratives) = FAIL. FILL/HUG correct; `itemSpacing` ≤ 48. Mobile safe area: root frame `paddingTop ≥ 59`, `paddingBottom ≥ 34`.
- D5 content: text matches COPY.md VERBATIM (scan_text_nodes); no placeholder.
- D6 craft: Production-Craft scoring in figma-design-patterns vocabulary, INCLUDING **cross-screen
  consistency** — screenshot the built sibling screens (esp. the canon screen) and FAIL divergence from
  their established visual language (different padding scale, a differently-composed card/header, a
  re-drawn tab bar instead of the shared instance). The screens must read as one product.
- D6 **direction fidelity (concept.md craft bar)** — the spec is the FLOOR; `direction/concept.md` is the
  bar. Judge the screen against concept.md's exact frozen sections (don't invent field names):
  **Signature DNA** — does the screen carry the motif / form-language / signature device, or is it generic
  kit placement? **Meaning-encoding philosophy** — does the hero carry its meaning by hierarchy, with NO
  value/state restated by a redundant badge (PC13)? **"What this is NOT"** — does the screen trip any
  listed anti-pattern / off-brand move? A spec-complete screen that misses the Signature DNA or hits a
  "What this is NOT" item is a craft FAIL. (If a per-screen Motion was specified, confirm it is DOCUMENTED
  as a motion spec / Lottie poster in handoff — not faked, not silently dropped.)
- D6 **platform-appropriateness** — **Every reviewer dispatch MUST carry this check; it is not
  optional.** Given the confirmed `targetPlatform` in the brief, verify:
  1. **Touch targets ≥44×44 pt** on all touch platforms (`mobile-native-*`, `mobile-web`, `tablet`).
     Any tappable element whose tap zone is smaller = FAIL.
  2. **No hover-only affordances on touch platforms.** If an action or piece of information is
     accessible ONLY via hover (hover tooltip, hover-reveal row action, hover-activated menu), that
     is a FAIL on touch platforms. Every affordance must be reachable by tap.
  3. **Platform-correct navigation.** Mobile screens must use a bottom tab bar (or back-chevron
     header for sub-screens); desktop screens use top nav / sidebar. The wrong nav pattern for the
     platform = FAIL.
  4. **Platform-correct microcopy.** Scan ALL visible text on the canvas against the anti-pattern
     table in `figma-product-foundation/references/platform-conventions.md` Part 2. Any match is a
     FAIL — for example: "드래그하여 올리기", "클릭", "마우스를 올리면" on a mobile screen; or
     "탭" as an affordance verb on a desktop-only screen. Flag the exact string and the rule it
     violates. For `responsive-web`, verify that mobile-breakpoint strings use touch-appropriate
     wording and desktop-breakpoint strings use pointer-appropriate wording.
  This is a craft FAIL even when D1–D5 are clean — a spec-complete screen with the wrong platform
  conventions is not production-ready.
- D6 **DRY / componentization**: a composite unit that repeats (card, row, stat cell, payment row,
  message bubble, bracket node, **skeleton placeholder**) MUST be instances of ONE component, not
  copy-pasted duplicate frames. Read the repeated nodes: sibling FRAMEs with identical child-name
  signatures instead of INSTANCEs = a copy-paste defect = craft FAIL. This covers **authored** structures
  (incl. skeletons), which the library-only D2 audit does not catch — that gap let a 3×-copy-pasted
  skeleton card pass an earlier review; do not repeat it.
- **DESIGN AUTHORITY — you are a senior production designer, not a spec-checker.** The spec (DESIGN.md
  regions + COPY strings) is the FLOOR, not the ceiling: every region present and every string rendered is
  necessary but NOT sufficient. You have full authority to REJECT and REDIRECT the builder's design when it
  isn't production-ready — a cramped or unbalanced layout, weak visual hierarchy/grouping, awkward element
  positioning, clumsy spacing, a poor component choice, a floating/misplaced CTA, weak button or label
  microcopy. Do NOT rubber-stamp a spec-complete screen that a senior designer wouldn't ship. When you
  reject on craft, give a CONCRETE direction the builder can execute ("the form is cramped and the CTA
  floats — group the fields with tighter 12px spacing, lift the title with more breathing room, move the
  consent directly above the CTA, full-bleed the CTA"), not a vague "improve hierarchy". Layout, position,
  grouping, sizing, emphasis, and composition are fully yours to redirect; for pinned COPY.md strings the
  wording is the baseline but you may flag awkward copy and propose better. Push until the screen is
  genuinely production-ready, not merely spec-complete.
  **The floor cuts BOTH ways — REMOVE redundant elements, don't only ADD missing ones.** A spec region
  means "communicate this information," NOT "render a dedicated widget even when the screen already says
  it." Actively flag elements that earn their keep nowhere and direct their removal: a status encoded a
  second/third time (a 유효/만료 badge when the countdown already shows validity and the "만료됐어요"
  headline + disabled CTA already show expiry), a label restating the value next to it, decorative chrome
  carrying no information, a duplicate affordance. Over-decoration / redundant clutter is a craft FAIL
  exactly like under-building — checking only that spec'd elements are PRESENT, without asking whether each
  is NECESSARY, is the spec-checker trap this clause exists to break. (Every reviewer dispatch must carry this clause.)
- **ALL STATES, EQUAL RIGOR (a screen is ALL its frames, not one main frame).** A screen ships every
  state the spec requires as its own frame (default / loading / empty / error / success). `save_screenshots`
  EVERY state frame the builder produced and run the FULL D1–D6 pass on each — a non-default state gets the
  SAME craft scrutiny as the default, never a glance-and-praise. Walk each state's BODY for readability and
  **separation from the fixed chrome**: a loading/empty status line jammed against the header (no gap), text
  crammed with no padding, an off-center cluster, or content that reads as "broken filler between header and
  skeletons" is a D6 FAIL — even when the words are correct. A defect in the loading or empty frame fails the
  whole screen exactly like a defect in the default. Enumerate the required states from the prd-analysis entry
  so you cannot silently skip one; report findings per `stateFrameId`.
- Inputs (both verifiers): channel, builtFrameId, specPaths { design, copy, prd }, screenId, ledgerPath,
  round, priorFindings, builtSiblings (frame-ids + screenshot paths of already-built screens / the canon
  screen), **findingsPath** (the exact file the verifier must write — see Output).
- **Output — write findings to a FILE, return only a compact handle.** Each verifier WRITES its full
  findings (per-dimension verdict + every CRITICAL/HIGH/MEDIUM finding with `stateFrameId`, the concrete
  redirect, and evidence) to its assigned file:
  - structural → `<sot>/_build-cache/<screenId>/review-r<round>-structural.md`
  - craft      → `<sot>/_build-cache/<screenId>/review-r<round>-craft.md`

  and **returns ONLY** `{ verdict: "PASS"|"FAIL", findingsPath, criticalCount, highCount }` (structural
  returns this as `structuralVerdict`, craft as `craftVerdict`). The verifier does NOT echo the findings
  prose back in its return message — the file is the single home of the detail. PASS a dimension only on
  evidence; any CRITICAL/HIGH = that verifier FAILs (and the file states why). Never rubber-stamp — a
  clean file still enumerates what was checked, with evidence.
  > **The dispatch prompt MUST state this file-write contract explicitly.** The shared verifier agents
  > (`figma-reviewer`, `figma-structural-verifier`) default to "return a single JSON object with an inline
  > `findings[]`" (their `## Output`) because they're also used by `/figma-redesign`, which is unchanged.
  > So when this skill dispatches them, the prompt must override that: "write your full findings to
  > `<findingsPath>` and return ONLY `{verdict, findingsPath, criticalCount, highCount}` — do not inline
  > the findings." Without that explicit line the agent reverts to inline output and the saving is lost.
```

**Merge + on FAIL (file-relayed — keep the orchestrator context lean).** AND-merge on the VERDICTS only:
`PASS = structuralVerdict ∧ craftVerdict`. **The orchestrator does NOT read either findings file** — that
prose stays out of its long-lived context. On any FAIL, message the SAME builder the two
`findingsPath`s **verbatim** plus a fix prompt: *"Read both review files; fix every CRITICAL and HIGH
finding in them; then re-run the full L1 self-eval ritual on the touched sections."* The builder READS the
two files itself, fixes, and re-runs L1 → then dispatch TWO NEW fresh verifiers (with fresh
`findingsPath`s for the new round). Do not re-review directly without the self-eval re-run. (Rationale:
the review prose is large and only the builder must act on it — shuttling a path costs the orchestrator a
few tokens; ingesting two full reviews every round across N screens does not.)

## Async / R5
- One heavy-write builder per channel at a time. Fan screens across channels for concurrency; within a
  channel, serialize builders. Reviewers (read-only) fan out freely and may read a channel while no
  builder writes it.
- Single channel → serial. Partitioned writes (one builder per disjoint frame) pipeline safely.
- The orchestrator creates truly-shared resources once (palette-map, output page) before fanning out,
  so partitioned builders don't double-create.

## Concurrency vs heavy imports (R5 corollary)
A large component-SET import (`import_component_by_key` on a multi-variant set like Radio/Select) is heavy and **times out under channel contention** — observed: with 4 concurrent builders on one channel, a Radio import hung at 15s repeatedly and blocked the screen (builder correctly set `importThreadHung:true` and stopped, per rule). Already-imported components keep working (they're in plugin memory); only NEW set-imports hang. So: for **import-heavy** screens (forms needing several distinct component sets not yet imported), run FEWER concurrent builders (1–2), or let the channel quiet and re-dispatch the blocked screen ALONE. The plugin is not crashed — no restart needed — just lower the load so the import gets the thread. Don't substitute a raw frame for a required kit kind to dodge a transient import hang; re-dispatch instead.

## Recovery
- `importThreadHung:true` → stop launching builders; ask the user to restart the plugin; drain recorded
  import tails in ONE post-restart single-writer pass (each builder logged its blocked keys + node ids).
- Stuck builder (no new ledger/screenshot for a long window) → probe on-disk artifacts; if complete-but-
  tail-blocked, recover the tail; else stop the agent and recover.

## Done bar (per screen)
1. Sonnet `verdict:"PASS"` (D1–D6 vs the spec). The only thing that can declare a screen done.
2. The builder passed the L1 self-eval ritual and L2 was green BEFORE the reviewer ran (so L3 ran once
   and passed first time).
3. Ledger records, per element: a real library instance + the variant chosen + the COPY string source.

## §Artifacts — per-round gate files

Each screen accumulates these under `<sot>/_build-cache/<screenId>/`:

| File | Written by | Gates |
|---|---|---|
| `l1.5-r<n>.md` | builder (on L1.5 resume) | L2 start |
| `l2-r<n>.md` | orchestrator (L2 pass) | L3 dispatch |
| `review-r<n>-structural.md` | figma-structural-verifier | — |
| `review-r<n>-craft.md` | figma-reviewer | — |
| `rebuttal-r<n>.md` | builder (judgment disputes only) | adjudication |
| `do-not-flag.md` | orchestrator (after adjudication) | passed to next verifier dispatch |

**Format — `l1.5-r<n>.md`:**
```
## L1.5 round <n> — <screenId>
| Item | Result | Notes |
|---|---|---|
| completeness | PASS/FIXED | … |
| copy-verbatim | PASS/FIXED | … |
| component-first | PASS/FIXED | … |
| touch-target | PASS/FIXED | … |
| token-binding | PASS/FIXED | … |
| DRY | PASS/FIXED | … |
| craft/squint | PASS/FIXED | … |
| opacity-bugs | PASS/FIXED | … |
| safe-area | PASS/FIXED | … |
| cross-screen-consistency | PASS/FIXED | siblings/canon VIEWED (list ids); matched padding·rhythm·header·type; shared organisms = canon instances (list keys) |
screenshot: <sot>/_build-cache/shots/<screenId>-l1.5-r<n>.png
```

**Format — `rebuttal-r<n>.md`:**
```json
[
  {
    "findingId": "D6-001",
    "ground": "JUDGMENT.md line 12 — corner radius 18 is signed-off as correct",
    "evidence": "governance/JUDGMENT.md confirms radius 18 = CompactCard canon"
  }
]
```

**Format — `do-not-flag.md`:**
```
# Do-not-flag registry — <screenId>
Verified, signed-off entries. Both verifiers must NOT re-flag these.

- findingId: D6-001 — corner radius 18 (signed-off JUDGMENT: CompactCard canon)
- findingId: D6-004 — Geist Mono numerals (signed-off JUDGMENT: scoreboard DNA)
```

## §Pre-flight — brief-assembly checklist (F cluster)

Run this before dispatching any builder. Each item is verifiable — no assertions, only reads.

| # | Check | How to verify |
|---|---|---|
| 1 | state.json matches reality | `get_pages` / `get_node` on the build file |
| 2 | Surface treatment from REGISTER | trust=white/no-aurora; energy=offwhite/aurora (from concept.md Register map) |
| 3 | Pre-imported component ids landed | `get_nodes_info` on the promised ids |
| 4 | SoT artifact path is correct slug | `ls <sot>/design/DESIGN.md` — right directory |
| 5 | COPY.md strings char-diffed per region | `diff` or verbatim compare per screenId key |
| 6 | Reuse inventory populated | shared chrome ids + kit keys listed for this screen |
| 7 | Reference artifact for common patterns | `l2-r<n>.md` or ref-library hit exists (H5 gate) |
| 8 | Visual research pack validated | `validate-visual-pack.py` passed; borrow-notes included |
