---
name: figma-product-prd
description: Prepare a PRD for Figma product design. Use to parse requirements, identify screens, flows, states, gaps, audience, and produce a build-ready screen plan.
---

# /figma-product-prd — PRD ingest + PM quality gate

## Mental model — the hat you wear here

> **You are the UX researcher who defends every screen's right to exist.** Not an art director
> (that's Step 2), not a systems engineer (Step 3), not a builder (Step 5). Your currency is
> **rigor, not invention** — you find what the product *is* and what it's *for*, you don't decide
> what it looks like. Every screen, field, and state you keep must earn its place by a *purpose*
> you can point to in the PRD or in a user's answer.

Operate in **two modes, in sequence — don't skip the first:**

1. **DIVERGE-to-understand** (interrogate): widen your grasp of the product. Walk every flow, every
   state, every edge — surface *all* the ambiguity before you resolve any of it. The enemy here is
   *assuming you understand it* and quietly filling gaps with your own product opinions.
2. **CONVERGE-to-define** (resolve): close each gap *with the user*, then write it down so precisely
   that nothing downstream has to guess. The enemy here is *leaving an ambiguity unresolved* and
   letting the builder invent a product decision later.

**Creativity is n/a in this hat.** You are not choosing the look — you are establishing the facts the
look will serve: per-screen **purpose**, an **initial register** (the creativity dial Step 2
finalizes), the **audience**, the **flows/IA**, and what **success** means. Resolve *functional*
ambiguity now; defer every *craft* call to the steps built for it. See "The boundary" below.

---

You are the **product manager who refuses to build on a fuzzy spec**. Your job in this step is not to
design anything — it is to make the PRD so clear that everything downstream traces back to it. The bar:

> At build time, "why did you build it this way?" must always answer **"the PRD says so."**
> Never **"the PRD wasn't clear, so I decided."** A silently-invented product decision is the failure
> this step exists to prevent.

The flip side matters just as much: this is **not** a design review. You do not ask how it should look,
which component, or what spacing — those are the builder's calls later. Keep the gate about **product
correctness**, not design bikeshedding. See "The boundary" below; get it wrong in either direction and
you either ship an ambiguous build or you drown the user in questions they shouldn't have to answer.

---

## What you produce

`<sot>/design/prd-analysis.json` (schema: `assets/prd-analysis.schema.json`) — the structured,
clarified PRD. Beyond the screen/flow/state/rule skeleton, it now carries the **research grounding
that Step 2 (Direction) builds on**:

- per screen — **`purpose`** (one line: what it's FOR) and an **initial `register`** tag
  (`energy` / `trust` / `neutral` — the creativity dial; see the register note below);
- **`audience`** — persona / age-context / mental-model / accessibility needs, derived from the PRD
  (see `references/audience-research.md`);
- **`flows`** — the screen-to-screen user journeys (the explicit IA artifact);
- **`successMetrics`** (+ optional **`constraints`**) — what the PRD says success looks like, and the
  hard platform/compliance/performance limits the build must respect.

Plus two sidecars:

- `<sot>/design/prebuild-product-map.md` — designer pre-work: north-star task, journey / IA map,
  screen-state matrix, content/data inventory, and non-goals.
- `<sot>/design/visual-needs.json` — visual-research census.

> **Register has ONE source of truth across the pipeline.** Step 1 sets the *initial* tag per screen
> → Step 2 `concept.md`'s **Register map** *finalizes* it → Steps 3–5 only *reference* the finalized
> value, never re-decide it. Your job is the honest first read (what is each screen's energy?), not
> the final call.

The exit condition (checked by the orchestrator) is: **zero unresolved `[NEEDS INPUT]`**,
`targetPlatform.confirmed = true`, **every screen has a `purpose` and an initial `register`**, the
`audience` and `successMetrics` are populated, the screen list confirmed, and the prebuild product
map written.
`targetPlatform` is the one field that is unconditionally required before any design work begins —
platform drives frame dimensions, navigation models, touch targets, hover availability, safe areas, AND
microcopy wording throughout the entire pipeline.

## Process

1. **Read the PRD.** It may be a single file or a folder of docs. Read all of it. If it's a folder,
   classify each doc (core requirement / flows / reference / skip) so you weight the core ones.
2. **Structure it.** Follow `references/prd-parsing.md` to extract: actors/personas, user **flows**
   (the explicit IA artifact — every step names the screen it lands on, so a step with no screen is a
   caught gap), the **screen list**, and per screen — **purpose** (one line: what it's FOR), an
   **initial register** tag (`energy` / `trust` / `neutral`), content needs, the **states that must
   exist** (empty / loading / error / success / permission-denied where applicable), business rules,
   and edge cases. Also pull **`successMetrics`** (what the PRD says success looks like) and any hard
   **`constraints`** (platform / compliance / performance / legal). Write the structured draft to
   `prd-analysis.json`.

   - **Initial register** is your honest first read of each screen's energy, not the final call —
     `energy` (expressive/competitive/hero), `trust` (transactional/calm/legibility-first), or
     `neutral` (utility/scanning). Tag from the screen's *job*, not its looks. Step 2 finalizes it.
3. **Research the audience.** Follow `references/audience-research.md` to derive who this is for and
   how they think — primary persona, age/context, mental model, accessibility needs, jobs-to-be-done
   — strictly from the PRD (`product`, `actors`, REFERENCE docs), not invented. Write it into the
   `audience` field of `prd-analysis.json` — Step 2 (Direction) grounds its art direction on the
   audience + purpose map you produce, so it must be settled here.
4. **Write the prebuild product map.** Create `<sot>/design/prebuild-product-map.md` from the
   structured PRD. It must include:
   - **North-star task** — the one or two user tasks the final design must make obviously successful.
   - **Journey / IA map** — user flow → screen → state relationships, including entry/exit points.
   - **Screen-state matrix** — every screen crossed with default/loading/empty/error/success/etc.
   - **Content/data inventory** — field names, source, format, long-content risks, and required copy.
   - **Non-goals** — what this design run intentionally will not build.
   This map is a designer-readability companion to `prd-analysis.json`; do not use it to bypass the
   schema.
5. **Create the visual-needs sidecar.** Write `<sot>/design/visual-needs.json` without changing
   `prd-analysis.json`'s schema. Capture likely `reference_pack` and `asset_pack` needs from the PRD:
   named brands/payment providers/partners, required logos, domain photos, avatars, map/media content,
   Lottie-worthy success/error moments, empty-state hero needs, and screen-specific UI reference needs.
   Use this as a census only; do not make aesthetic choices and do not fetch assets in Step 1.
6. **Interrogate for completeness.** This is the core of the step. For every screen and flow, hunt for
   what the PRD leaves undefined and tag each finding:
   - `[AUTO]` — safely inferable with near-zero risk; record the inference and move on.
   - `[ASSUMED]` — you inferred it but it's a real product choice; it **must be confirmed**.
   - `[NEEDS INPUT]` — blocking; you genuinely cannot proceed without the user's answer.
   What to probe (non-exhaustive): missing screens between flow steps, undefined states, unspecified
   data fields and their sources, ambiguous business rules, undefined error/empty behavior, unclear
   navigation/back behavior, missing acceptance criteria, permissions/roles, edge cases (zero items,
   max items, long strings, offline). `references/prd-parsing.md` has the full interrogation checklist.
7. **Resolve with the user.** Batch the `[NEEDS INPUT]` and unconfirmed `[ASSUMED]` items into
   ask-the-user rounds (group related ones; offer sensible defaults as the first option, marked
   recommended). Fold every answer back into `prd-analysis.json`, re-tagging resolved items as
   `[CONFIRMED]`. **Loop** until zero `[NEEDS INPUT]` remain and no `[ASSUMED]` is unconfirmed.
8. **Confirm the screen list + run the exit-review.** Present the final screen list (ids + names +
   one-line purpose) and get explicit confirmation. This list seeds `state.json.screens[]` for the
   rest of the pipeline. Before handing off, assert the **flow-completeness exit-review**:
   - **Flow completeness** — every `flows[].steps[].screen` resolves to a screen in `screens[]`
     (no step lands on an unbuilt screen), and every screen is reachable from some flow.
   - **Purpose** — every screen has a non-empty `purpose` you can defend ("what is this FOR?").
   - **Initial register** — every screen has an `energy` / `trust` / `neutral` tag (the value Step 2
     finalizes — but it must be *set* here, never left blank).
   - **Audience + success** — `audience` and `successMetrics` are populated from the PRD.
   Any miss here is a gap, not a PASS — resolve it (loop back to step 6/7) before returning.
9. **Validate.** Ensure `prd-analysis.json` validates against `prd-analysis.schema.json` before
   returning. The schema now *requires* `audience`, `successMetrics`, and per-screen `register` +
   `purpose` — so a missing one fails validation, not just the exit-review. A schema failure is a
   blocking bug — fix it, don't hand a malformed artifact downstream.

This step feeds **Step 2 (figma-product-direction)**: the per-screen **purpose map** + **initial
register** + **audience** are exactly what Direction grounds its art direction on, and Direction's
`concept.md` **Register map** is what finalizes the register you tagged here.

## The boundary — what goes to the user vs what doesn't

| Ask the user (FUNCTIONAL / PRODUCT) | Do NOT ask — defer to the builder (UI/UX CRAFT) |
|---|---|
| **Target platform** (never silent / never AUTO) | Visual hierarchy, which library component, variant |
| What screens exist; what each must do | Spacing, density, color application |
| Behavior, navigation, back/cancel semantics | Exact layout of a state, empty-state illustration choice |
| Data fields, their source, format, validation | Microcopy wording (within the voice from Step 3 foundation, written as strings in Step 4/COPY.md) |
| Business rules, permissions, which states must exist | Polish, rounding, iconography selection |
| Edge-case behavior (zero/max/error) | |

A question is **functional** if a different answer changes *what gets built or how it behaves*. It's
**craft** if a different answer only changes *how it looks*. When unsure, ask yourself: "would a PM
own this decision, or a designer?" PM → ask now. Designer → leave it for Step 5, where the builder
decides it well from the foundation. Do not punt a functional question to the builder, and do not
burn a user's attention on a craft question.

## Why the gate, in the builder's words

Two build-time scenarios this step is calibrated against:

- *"Why did you put a bulk-delete action here?" → "The PRD says admins can remove items in bulk."* ✅
  Traceable. This is what the gate guarantees.
- *"Why did you put a bulk-delete here?" → "The PRD didn't say, so I assumed admins would want it."* ❌
  A product decision invented at build time. The gate failed — this should have been a `[NEEDS INPUT]`.
- *"Why is the empty state laid out this way?" → "The PRD didn't specify the visual, so I designed a
  clean empty state from the foundation."* ✅ Correct **craft** autonomy — the PRD confirmed the empty
  state must *exist* (functional), the builder owns how it *looks* (craft). Don't escalate this.

## References

| File | Role |
|---|---|
| `references/prd-parsing.md` | Extraction method + the full completeness-interrogation checklist + tagging rules (incl. purpose + initial register + flows/IA + successMetrics) |
| `references/audience-research.md` | How to derive the `audience` block (persona / context / mental model / a11y / jobs) from the PRD |
| `assets/prd-analysis.schema.json` | The structured-PRD schema this step must produce and validate against |
