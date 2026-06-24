---
name: figma-product-spec
description: >-
  Step 4 of /figma-product — author the build-ready spec: DESIGN.md (a library-faithful design spec in
  the @google/design.md schema, with per-screen layout intent AND per-screen art-direction fields) and
  COPY.md (a copywriting system PLUS the real per-screen strings). Both derive strictly from the
  foundation/ dossier (Step 3) AND the signed-off direction/concept.md (Step 2) — no fresh aesthetic
  choices here — and BOTH are schema-checked before the build runs (DESIGN.md via @google/design.md
  lint, COPY.md via copy-md.schema.json with full screen coverage). Surfaces and resolves any remaining
  library gaps with the user. Orchestrated by /figma-product but independently invocable. Use whenever
  you need to produce a design spec + copy from an established foundation + concept, turn a design
  language into a token-bound DESIGN.md, or write the actual UI copy for a set of screens.
---

# /figma-product-spec — author DESIGN.md + COPY.md from the foundation + concept

This step converts the **foundation** (Step 3), the signed-off **direction** (Step 2's
`direction/concept.md`), and the **clarified PRD** (Step 1) into two artifacts a builder can execute
against without making product *or* aesthetic decisions:

- **`DESIGN.md`** — the design spec: tokens (bound to the library), plus per-screen **layout intent**
  **and per-screen art-direction** (Metaphor / Expresses / Hero+meaning / Craft / Signature / Motion /
  Creative mode), pulled from `concept.md`.
- **`COPY.md`** — the copy system (voice/tone/terminology/patterns) **and** the actual strings, keyed
  by screen so the build has zero placeholder text.
- **Visual asset prefetch plan** — updates `<sot>/design/visual-needs.json` with the concrete assets
  now known from the spec and prepares `assetRequests` for `visual-researcher` where useful.
- **`build-readiness.md`** — per-screen asset plan, responsive/device behavior notes, builder
  acceptance checklist, and risk list.

Everything here **derives from `foundation/` + `concept.md`**. The foundation gives you tokens,
components, and the systematized signature layer; concept.md gives you the per-screen *intent* (what
each screen should mean and feel). If you find yourself inventing a new color, density, or signature
move, stop — that decision belongs upstream (color/token in Step 3 foundation; aesthetic intent in
Step 2 direction). This step is **translation/expression, not invention**.

Both artifacts are **schema-checked before Step 5 (build)**. A spec that doesn't validate is not
build-ready; the orchestrator's Step-4 gate blocks on it.

---

## Mental model — the hat you wear here

> **You are the product designer.** Not the art director (Step 2 already chose the direction), not the
> systems engineer (Step 3 already built the tokens + signature layer), not the builder (Step 5
> executes the craft). Your job is to **apply the system, one screen at a time** — take the agreed
> direction and the agreed components and decide *how each individual screen expresses them*. You
> express the direction per screen; you never re-choose it.

The dial you turn per screen is the **register-driven creative mode**, read from `concept.md`'s
**Creative-mode map**: an energy screen runs **bolder · overdrive · delight** (lean into the hero
moment, motion, signature device); a trust screen runs **quieter · distill · polish** (restraint,
legibility, one rationed accent); a neutral/utility screen runs **polish · layout** (clean rhythm, the
focal element recedes). Same product, different volume per surface — this is what lets one spec read as
*one coherent product* across very different screens.

The **bolder ↔ quieter dial is driven by register, not by your mood**, and the register/cohesion model
is defined once, upstream — do not redefine it here. Read
`figma-product-direction/references/register-cohesion-model.md` if you need the taxonomy.

**Register has ONE source of truth across the pipeline.** Step 1 (prd) sets the *initial* tag →
Step 2's `concept.md` **Register map finalizes** it → this step (Spec) only **references** the
finalized register; **it never re-tags a screen's register.** If a screen's register feels wrong,
that's a Step-2 decision — flag it for the direction step and re-flow; don't quietly re-decide it in
the spec.

---

## What you produce

```
<sot>/design/DESIGN.md   # @google/design.md schema + ## Screens (per-screen layout intent)
<sot>/design/COPY.md     # YAML frontmatter (voice + screens map) + markdown system guide
<sot>/design/build-readiness.md
```

Exit condition: `DESIGN.md` passes `npx @google/design.md lint`; `COPY.md` passes
`copy-md.schema.json` and its `screens` map covers every screen id; `build-readiness.md` covers every
screen; all library gaps resolved.

## Process

1. **Author DESIGN.md.** Follow `references/design-md-authoring.md`. Use the `@google/design.md` schema
   (skeleton in `assets/design-md.template.md`; full schema reference is the
   `figma-design-md` skill's `design-md-schema.md` — read it for token/section rules). Fill:
   - **Token frontmatter** (`colors`, `typography`, `spacing`, `rounded`, `components`) sourced from
     `foundation/library-mapping.md` — every token reflects a library token role, **zero raw invented
     hex**. (The values may be concrete for the spec's readability, but each must correspond to a real
     library token named in the mapping; the builder binds the library variable, never a literal.)
   - **Prose sections** (Overview, Colors, Typography, Layout, Elevation, Shapes, Components, Do's &
     Don'ts) grounded in `design-language.md` — the rationale cites the foundation.
   - **A `## Screens` section** (the greenfield addition): per screen, the **layout intent** — regions,
     which components fill them, hierarchy, which states to render, and FILL/HUG/FIXED behavior at a
     structural level — **plus the per-screen art-direction fields** (Metaphor / Expresses /
     Hero+meaning-encoding / Craft moves / Signature usage / Motion / Creative mode), pulled from
     `direction/concept.md` so the builder expresses the agreed direction on this exact screen. This is
     what the builder turns into frames. Pull screen *structure* from `prd-analysis.json` (content,
     states, actions); pull screen *intent* from `concept.md`. `design-md-authoring.md` defines each
     field and exactly which concept.md section it binds to.
   - **Responsive/device behavior** for each screen: what changes across confirmed platform widths,
     safe-area constraints, touch target implications, and which structures are fixed vs adaptive.
2. **Resolve library gaps.** Any `foundation.json.gaps` still open, or new ones you hit while
   specifying screens, get resolved now with the user (escalate → assemble-from-primitives → closest
   token). A `DESIGN.md` shipped with an unresolved gap will block a builder — resolve it here.
3. **Author COPY.md.** Follow `references/copy-system.md`. Two parts:
   - **The system** (YAML frontmatter + body): voice, tone (and how it shifts by context — success vs
     error), terminology/glossary, microcopy patterns, length limits, do/don'ts — grounded in
     `foundation/brand-voice.md`.
   - **The strings** (YAML `screens` map): the **actual copy** for every screen, keyed by
     `screenId → region → string(s)`. Cover every state that shows text (empty/error/success messages,
     button labels, field labels, helper text). Real strings in the product's language (keep Korean if
     the PRD/audience is Korean). No `Lorem ipsum`, no "Title/Label" placeholders.
4. **Prepare concrete visual asset prefetch.** Re-read `<sot>/design/visual-needs.json` and the
   screen specs you just wrote. For every visible logo, icon outside the library, domain image, avatar,
   hero illustration, Lottie/poster moment, or screen-specific reference still needed, write detailed
   `assetRequests` / `referenceRequests` using `figma-visual-researcher`'s contract. If the asset is
   obvious and needed on the first build screen, dispatch `visual-researcher` before Step 5 (build) and
   write the returned pack under `<sot>/_build-cache/visual-research/`; otherwise mark it as deferred
   for the build hook's active fetch. Do not leave known visible media as an unstated builder surprise.
5. **Write build-readiness.md.** For every screen include:
   - **Per-screen asset plan** — required assets, prefetched assets, deferred active-fetch requests,
     local paths when known, and library-component substitutes when acceptable.
   - **Builder acceptance checklist** — the concrete conditions that make this screen done beyond
     generic linting: required states, copy coverage, hierarchy, accessibility, and asset usage.
   - **Risk list** — likely build blockers: missing component variants, difficult responsive behavior,
     ambiguous media, heavy imports, or library gaps the builder must not silently work around.
6. **Confirm art-direction coverage.** Before schema-check, walk every `### <screen-id>` block and
   confirm its art-direction fields trace to `concept.md` (Metaphor/Signature/Motion ← Signature DNA;
   Craft ← Craft toolkit for *this screen's register*; Creative mode ← Creative-mode map;
   Hero+meaning ← Meaning-encoding philosophy; Register ← Register map, *referenced not re-tagged*). A
   field with no concept.md backing is the same latent failure as a token with no library backing —
   the builder would have to invent it.
7. **Schema-check both.** Follow `references/schema-checks.md`:
   - `DESIGN.md`: `npx @google/design.md lint <path> --format json` — regenerate-on-fail (max 3×).
   - `COPY.md`: `python "${SKILL_DIR:-${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-product-spec}/scripts/check_copy.py" <COPY.md> --screens <id,id,...>` — validates frontmatter
     against `assets/copy-md.schema.json` and that the `screens` map covers every confirmed screen id.
   A still-failing artifact after 3 attempts is a blocking failure — report it, don't advance.

## Grounding discipline (why "derive, don't invent")

The foundation + concept are the agreed, sourced, user-approved design language and direction.
`concept.md` in particular passed **Gate A — the one human creative sign-off** — so its intent is
settled. If the spec quietly introduces a new accent color, a different density, or a different
signature move, two bad things happen: the build no longer matches what the user signed off on, and the
decision has no source. So:

- Every DESIGN.md token traces to a `foundation/library-mapping.md` binding.
- Every per-screen art-direction field traces to a `direction/concept.md` section (see the field-to-
  section map in `references/design-md-authoring.md`). Register is *referenced* from concept.md's
  Register map, never re-tagged here.
- Every COPY.md voice/tone rule traces to `foundation/brand-voice.md`.
- Per-screen layout intent traces to `prd-analysis.json` (what exists) + `design-language.md` (how it's
  composed). Layout *craft* details you don't specify are fine — the builder owns those (Step 5). But
  don't contradict the foundation or the concept.

## References

| File | Role |
|---|---|
| `references/design-md-authoring.md` | How to author DESIGN.md: token frontmatter from the library mapping, prose, and the `## Screens` layout-intent + per-screen art-direction section (with the concept.md field-to-section map) + gap handling |
| `references/copy-system.md` | COPY.md structure: the voice/tone system + the per-screen string map |
| `references/schema-checks.md` | Running DESIGN.md lint + COPY.md schema validation; regenerate-on-fail loop |
| `assets/design-md.template.md` | DESIGN.md skeleton (@google/design.md schema + `## Screens`) |
| `assets/copy-md.template.md` | COPY.md skeleton (frontmatter + screens map + body) |
| `assets/copy-md.schema.json` | COPY.md frontmatter schema (validated by `scripts/check_copy.py`) |
| `scripts/check_copy.py` | Validates COPY.md against the schema + screen-coverage |
