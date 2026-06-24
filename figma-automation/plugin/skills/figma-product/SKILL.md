---
name: figma-product
description: Orchestrate PRD-to-Figma product design. Use when turning a PRD, spec, brief, or requirements doc into researched, specified, high-fidelity Figma screens.
---

# /figma-product — PRD → High-Fidelity Figma Product (orchestrator)

Turn a **PRD** into a designed product in Figma. This skill is a **thin sequencer**: it owns the
state machine and the user-confirmation gates between steps, and delegates each step to a dedicated
skill. It does almost no work itself — the depth lives in the step skills.

Why a suite and not one skill: each step has a different job and a different failure mode (an
ambiguous PRD, a generic look, an off-schema spec, a crude build). Splitting them lets each be
invoked, tested, and improved on its own — the same shape as `/figma-redesign` delegating memory
to `/figma-playbook`.

This is the **greenfield** path. `/figma-redesign` reinterprets ONE existing screen into a target
library and gates completeness by diffing the **original frame**. Here there is no original — the
**spec** (`DESIGN.md` per-screen intent + `COPY.md` strings) becomes the completeness reference.

---

## The pipeline

```
/figma product <prd-path> --library <url-or-key> [--project <slug>]

  Step 1  figma-product-prd          PRD → research: screens + flows + per-screen purpose & register  [GATE: scope/register confirm]
  Step 2  figma-product-direction    research → art direction (concept.md): the modern/professional
                                      aesthetic + EFFECTS + color-codes + emphasis, all concrete        [GATE A: human direction sign-off]
  Step 3  figma-product-foundation   concept.md → design system: tokens + EFFECT PALETTE + signature
                                      + library map; assets/refs staged INTO the Figma file            [GATE: completeness]
  Step 4  figma-product-spec         foundation + concept.md → DESIGN.md + COPY.md (schema-checked)    [GATE: coverage + faithful]
  Step 5  figma-product-build        ① CANON co-designed w/ user BY HAND → ② rest fan out to agents   [GATE: less-advanced / Sonnet-tier L3 PASS]

  Visual research lane              PRD hook: visual-needs census → Direction hook: references + taste scan
                                    → Foundation hook: stage assets/refs INTO the Figma file → Build hook: active fetch
```

> **Where the aesthetic is really locked (2026-06-19):** Gate A (human direction sign-off) stays in
> Step 2 on the *concept* (a cheap HTML feel-check is enough there). But the **production aesthetic and
> the user's real hands-on sign-off happen at the START of Step 5** — the orchestrator co-designs the
> 1–2 canon screens directly in Figma WITH the user (after the spec), THEN only the *rest* fan out to
> `figma-builder` (advanced model / Opus tier) + the two less-advanced / Sonnet-tier verifiers. **Two-sided bar — both are FAILs:** (a) **flat /
> AI just-assembling stock blocks** (under-crafted), and (b) **over-decoration / advanced features piled
> on for show** (over-crafted). SUCCESS = Figma's advanced capabilities (glass, blur, depth, effects,
> motion, real imagery) deployed **purposefully — in the right places, in the right amount, fit to the
> screen's UI/UX PURPOSE**, not for impressiveness. The *specific* aesthetic is whatever the direction
> chose for this project (liquid-glass / editorial-minimal / brutalist / soft-depth … — NOT a fixed
> style); execute *that* as authored composition with real assets, considered effects/color/emphasis,
> correct alignment + hierarchy — calibrated to purpose. See `figma-product-build` Rollout +
> `figma-product-direction` Phase 6.

Each step writes its artifact under `<sot>` (see Path Resolution) and records completion in
`state.json`. **Every step ends with an adversarial EXIT-REVIEW** the orchestrator runs on that
step's own output — it asks *"what did this step MISS?"* (a flow with no login screen, a screen with
no error state, a foundation section with no evidence, a spec string the copy never wrote) — because
a user confirming an incomplete artifact **cannot catch a gap they didn't notice either**. The review
surfaces gaps; resolve them with the user; only then advance. These are hard gates, not suggestions:

| Step | EXIT-REVIEW (an adversarial completeness review must pass to advance — not just a user "ok") |
|---|---|
| 1 | **Flow-completeness review (Research):** walk EVERY user flow end-to-end and confirm each screen it IMPLIES is in the list — `auth → welcome+login+signup+reset`, `list → list+detail+empty`, `form → form+success+error`, `purchase → summary+payment+result`. Plus: zero unresolved `[NEEDS INPUT]`/`[ASSUMED]`; **`targetPlatform.confirmed=true`**; every state a screen's data behavior implies is present; **every screen carries a `purpose` + an initial `register` tag**; full PRD traceability (every feature → ≥1 screen). THEN the user confirms the now-complete list + scope/register; `prd-analysis.json` validates. **This is where the "missing login screen" class is caught — surface it BEFORE the user confirm, because the user may not notice the absence either.** |
| 2 | **GATE A — direction sign-off (the one human creative gate).** The diverge→critique→converge produced a `concept.md`, and the HTML look-&-feel proved it on ≥1 energy + ≥1 trust screen. The adversarial check (run BEFORE presenting): is the direction **distinctive** (survives the squint test — not "any competitor"), **purposeful** (every signature move answers "what does this mean here?"), **cohesive** (energy & trust read as one product), **modern without trend-chasing** (adopted aesthetics serve register + legibility), and **buildable** in the target kit? A generic / decorative / flat direction is REJECTED and re-diverged HERE — this is where the "too weak / dull / generic" class is killed, before any token or screen exists. THEN the **user signs off on the rendered look-&-feel** ("이런 느낌"). On approve: `concept.md` finalized, winning concept written to the KB. |
| 3 | **Foundation-completeness review (Design System):** the dossier faithfully systematizes the **signed-off `concept.md`** — every section present (design-language, interaction-motion, haptics, brand-voice, library-mapping, **the bespoke signature layer**) and each decision traceable to `concept.md` or evidence; library gaps flagged; platform-gated (no hover/drag-drop on touch). `foundation.json` validates. *(Foundation has no human gate — the direction was signed off at Gate A.)* |
| 4 | **Spec coverage AND faithful-application review.** (a) *Coverage:* `DESIGN.md` lints + `COPY.md` schema-validates; every screen+state from the (now-complete) Step-1 census appears in BOTH `DESIGN.md` layout-intent AND `COPY.md` strings; everything derives from `foundation/` + `concept.md`; library gaps resolved with the user. (b) **Faithful-application review — dispatch an empowered design-director agent to confirm the spec did not FLATTEN the signed-off direction:** does each screen's layout intent carry its `concept.md` `Creative-mode map` + `Craft toolkit per register` (a clear focal point, hierarchy, the signature move where the register calls for it), or did it decay into generic boilerplate that builds flat? Weak/flattened application is reworked HERE. *(This does not re-judge the direction itself — that was signed off at Gate A — only whether the spec faithfully carries it.)* (The `spec-build-review.md` Step-4.5 plan-completeness gate is the final backstop right before build.) |
| 5 | Every screen reaches advanced-model `verdict:"PASS"` after its L1→L1.5→L2→L3 loop. |

If an exit-review surfaces a gap, **stop at that step and resolve it** — never paper over a Step-1
omission by guessing in Step 5. The front gates exist so the build is downstream of decisions already
made (and verified complete), not a place to discover them missing. **Gate A (Step 2) is the pivot:**
once the direction is signed off, Steps 3–5 *execute* it and never re-litigate taste.

---

## Visual research lane

Read `references/visual-research-flow.md` before running the product pipeline. This is a
cross-cutting lane, not a new numbered step. It uses `visual-researcher` as a standard subagent for two
jobs:

- **Reference prefetch** — 2024+ real product UI/UX screenshots and transferable pattern analysis,
  saved under `<sot>/direction/refs/` (consumed by Step-2 grounding; also written to the cross-project KB).
- **Asset prefetch / active fetch** — concrete logos, icons, photos, avatars, and Lottie posters saved
  under `<sot>/_build-cache/assets/`, with Figma ingest recipes.

Run it through hooks inside the existing steps:

- **PRD hook** writes `<sot>/design/visual-needs.json` as a sidecar from the PRD's named brands,
  domains, screen states, and likely media needs.
- **Direction hook** dispatches `visual-researcher` for the reference pack + taste scan that ground
  Step-2 art direction (cache-first against the cross-project KB).
- **Spec hook** turns the build spec into concrete `assetRequests` for visible media and prefetches
  obvious assets before build.
- **Build hook** passes all packs to builders as `visualResearch`; if a builder returns
  `visual_research_required`, validate the request, dispatch `visual-researcher`, then resume the same
  builder with the returned candidates.

## Run protocol

1. **Resolve the project.** Derive/confirm a project `<slug>` (kebab-case, from the PRD title or
   `--project`). `ls design-system/` — reuse an existing slug if it matches, else this run creates
   `design-system/<slug>/` (mirror the manifest shape of an existing `project.json`: `slug`, `name`,
   `fileKey`, `libraries[]`, `framework`, timestamps). Record both the target library API key/URL and
   a human-readable `librarySlug` for memory paths.
2. **Load memory once.** `Skill('figma-playbook') load --library <librarySlug> [--project <slug>]`.
   Pass the returned index context down to every step. (First use of a library → also
   `Skill('figma-playbook') learn --library <librarySlug>` to bootstrap pattern memory.)
3. **Initialize / resume state.** Read `<sot>/governance/state.json` if present and resume from the
   first incomplete step; else create it (schema in `references/state-and-resume.md`). Re-invoking
   `/figma product` is always safe — completed steps are not redone.
4. **Run each step in order**, invoking its skill, then **pausing at the gate** to report the
   artifact to the user and get the confirmation that step requires before advancing. Dispatch:
   - `Skill('figma-product-prd')` → research: screen list + flows + per-screen purpose & register
   - `Skill('figma-product-direction')` → `direction/concept.md` + look-&-feel renders → **GATE A: human sign-off**
   - `Skill('figma-product-foundation')` → `foundation/` dossier (systematizes the signed-off `concept.md`)
   - `Skill('figma-product-spec')` → `DESIGN.md` + `COPY.md`
   - `Skill('figma-product-build')` → built + advanced-model-passed screens
   After each, update `state.json` (`currentStep`, artifact paths, gate verdict, visual research pack
   paths, pending/resolved visual requests).
5. **Finish.** On all screens PASS: apply any pending memory proposals
   (`Skill('figma-playbook') apply <path>`), run `Skill('figma-playbook') consolidate`, and report
   each built `frameId`, the `foundation/` path, and the spec paths.

The step skills are also **independently invocable** — a user can run `/figma-product-foundation`
alone to (re)research the design language, or `/figma-product-spec` to regenerate the spec after a
library change. When invoked standalone they read/write the same `<sot>` artifacts, so the
orchestrator can pick up wherever they left off.

---

## Gates are about product, not polish

Two stances that must not blur (enforced by the step skills, surfaced here so the orchestrator
routes correctly):

- **Functional/product ambiguity** (what screens exist, behavior, data, business rules, which
  states must exist) is resolved **with the user at Step 1**. At build time, "why did you build it
  this way?" must always answer "the PRD says so." Inventing a product decision silently is the
  failure mode Step 1 exists to prevent.
- **UI/UX craft** the PRD doesn't spell out (visual hierarchy, component choice, spacing, empty /
  loading / error-state design, microcopy within the defined voice) is **decided autonomously by
  the builder** at Step 5 using the foundation + the local craft rules in `figma-product-build`.
  PRD silence on craft is a
  mandate to design it well — never license to skip it or stub it.

So the orchestrator never escalates a craft question to the user, and never lets a functional
question slide into the build.

---

## Path Resolution

`<sot>` = `design-system/<slug>/`. Artifacts:

```
<sot>/
├── project.json            # fileKey + library keys (this run creates/updates it)
├── governance/state.json   # orchestrator state machine (references/state-and-resume.md)
├── design/
│   ├── prd-analysis.json   # Step 1 (Research) — screens, flows, per-screen purpose + register
│   ├── DESIGN.md           # Step 4 (Spec)
│   └── COPY.md             # Step 4 (Spec)
├── direction/              # Step 2 — concept.md (the direction contract) + look-and-feel/ renders + taste-scan.json + refs/
└── foundation/             # Step 3 — design system systematizing concept.md (see figma-product-foundation)
```

Visual research sidecars:

```
<sot>/design/visual-needs.json
<sot>/direction/refs/
<sot>/_build-cache/visual-research/
<sot>/_build-cache/assets/asset-manifest.json
```

Scratch (catalog fetch, build ledgers, screenshots, visual research packs) lives under
`design-system/_build-cache/` or `<sot>/_build-cache/`, matching `/figma-redesign`.

## References

| File | Role |
|---|---|
| `references/state-and-resume.md` | `state.json` schema, step exit conditions, resume + project-slug resolution |
| `references/visual-research-flow.md` | How `visual-researcher` runs as PRD/foundation/spec/build hooks for prefetch and active media resolution |
