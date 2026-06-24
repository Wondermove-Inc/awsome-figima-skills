---
name: figma-product-foundation
description: >-
  Step 3 of /figma-product — turn the signed-off art direction (concept.md from Step 2) into a
  concrete, library-bound DESIGN SYSTEM before any spec or screen. Does NOT choose the look (that was
  decided and human-approved at Gate A); it faithfully systematizes concept.md into design-language,
  interaction/motion, haptics, and brand-voice decisions, builds the bespoke SIGNATURE LAYER (the
  motif / illustration / motion tokens the concept calls for), and maps every decision to the target
  library's tokens/variants — flagging gaps. Library-first (fetches the catalog before mapping).
  Reads audience from the Research step (prd-analysis.json); it does not derive the audience or choose
  the aesthetic itself. Orchestrated by /figma-product but independently invocable. Use whenever you need
  to convert an approved design direction into a token-bound, component-mapped design system.
---

# /figma-product-foundation — concept.md → the design system

The art direction is already **decided and signed off** (Step 2, `concept.md`, human-approved at
Gate A). This step does **not** re-open taste. Its job is to **systematize** that direction: translate
the concept into concrete, library-expressible decisions, build the bespoke signature layer, and bind
everything to the target library — so the spec and build derive from a real system, not from adjectives.

## Mental model — the hat you wear here

> **You are the design-systems engineer.** Not the art director (that was Step 2 — the look is
> settled), not the product designer (that's Step 4). Your job is **faithful, disciplined
> translation**: take a signed-off direction and make it *systematic, buildable, and traceable*.

Operate in **systematize** mode: high consistency, low invention. You add **zero new taste** — every
decision here either derives from `concept.md` or resolves a library-feasibility question. When the
concept implies something the library can't express, you don't invent a substitute — you **flag a
gap**. The failure mode to avoid is *quietly redesigning* the direction under the guise of
"systematizing" it. If you find yourself making an aesthetic choice the concept didn't make, stop:
either it's derivable from the concept (derive it) or it's a gap (escalate it).

Three commitments shape it:

1. **Faithful to the direction.** Everything traces to `concept.md` (its exact sections — Signature
   DNA, Adopted aesthetic, Cohesion decision, Craft toolkit per register). No fresh anchors, no new
   palette, no off-concept motion.
2. **Expressed through the library, never around it.** The build is component-first and zero-raw-hex,
   so the foundation is *how to use the chosen library* — which tokens, which variants, what density
   and type scale. Where the direction can't be expressed in the library, that's a **gap** to flag.
3. **Build the signature layer.** The concept's distinctiveness (its motif, semantic motion,
   illustration language) usually needs **bespoke** tokens/assets the stock library lacks. Defining
   how those are built/sourced and bound is this step's most concept-specific output.

---

## What you produce

A thorough, machine-readable dossier under `<sot>/foundation/`:

```
foundation/
├── design-principles.md     # 3–5 product-specific principles that drive tradeoffs (derived from concept.md)
├── design-language.md        # color philosophy, type system, density/rhythm, shape, iconography, imagery, elevation — the concept made concrete
├── signature-layer.md        # ⭐ the bespoke layer: the concept's motif, semantic-motion tokens, illustration language — how each is built/sourced in the library and bound
├── pattern-transfer.md       # the concept's layout language → structural anatomy of each recurring unit → library components (use/adapt/assemble/gap)
├── interaction-motion.md     # transitions, easing/timing, micro-interactions, gesture vocabulary (platform-gated; carries the concept's semantic motion)
├── haptics.md                # feedback model (mobile-native only)
├── brand-voice.md            # voice, tone, personality (derived from concept's direction; also grounds COPY.md)
├── library-mapping.md        # every foundation decision → library token/variant; feasibility audit + gaps
├── component-preferences.md  # component preference rules for recurring layout decisions
├── research-sources.md       # library-feasibility evidence + the concept references it builds on
├── refs/                     # captured kit/library screenshots (anchor refs live in <sot>/direction/refs/)
└── foundation.json           # machine-readable rollup (schema: assets/foundation.schema.json)
```

Exit condition (checked by the orchestrator): the dossier **faithfully systematizes `concept.md`** —
every major design-language/motion/voice decision traces to a `concept.md` section or a library fact;
the **signature layer is defined** (how the concept's motif/motion is built + bound, or a flagged
gap); `foundation.json` validates; library gaps are flagged; platform-gated (no hover/drag-drop on
touch). *(There is no anchor-pick gate here — the direction was decided at Gate A.)*

## Inputs you read (do not re-derive)

- **`<sot>/direction/concept.md`** — the contract. The source of every aesthetic decision.
  (See `../figma-product-direction/references/concept-template.md` for its exact section names.)
- **`<sot>/design/prd-analysis.json`** — the **audience** (derived in the Research step) + the
  **`targetPlatform`** (a CONFIRMED fact — never re-derived) + per-screen purpose/register. Use the
  audience to inform density/tone mapping; use the platform to gate motion/haptics/gestures.
- **`<sot>/direction/refs/`** — the analyzed reference screens from Step-2 grounding (reuse; don't re-research the anchor).

## Process

1. **Library first** — delegate to a **kit-investigation subagent**. You must know what
   tokens/components/variants exist *before* you map the concept onto them — so gaps surface now
   (cheap) not mid-build (expensive). Against the live library (follow the `figma-mcp-express` skill:
   `get_pages` → scoped reads, `get_styles`) or via `fetch_library_catalog` (REST, needs
   `FIGMA_TOKEN`), return a **digest**: the token spine (semantic color roles + light/dark modes,
   spacing scale, radius scale, type styles), the component families relevant to the PRD's screens
   (set name + key variants), the **gaps** for those screens, and **4–5 representative kit
   screenshots** saved to `refs/` via `save_screenshots`. Do not pull the raw catalog into the
   orchestrator. If the live plugin is the only access, pass its `channel` on every call.
2. **Read `concept.md` and `targetPlatform`.** Internalize the Signature DNA, Adopted aesthetic,
   Cohesion decision, and Craft toolkit per register. Read `targetPlatform` from `prd-analysis.json` —
   it gates which patterns are in-scope (hover/drag-drop/cursor only where supported; gestures +
   haptics only on `mobile-native-*`; safe-area on mobile). Keep `references/platform-conventions.md`
   open while authoring `interaction-motion.md` and `haptics.md`.
3. **Systematize the design language.** Turn `concept.md` into `design-principles.md` +
   `design-language.md`: color philosophy & temperature, typography system, spacing/density rhythm,
   shape & radius language, iconography & imagery, elevation/depth — each **derived from the concept**,
   not freshly chosen. For each register/surface group, carry the concept's matched **craft toolkit**
   and concrete elevation / hero-numeral / status / light treatments — see
   `../figma-product-direction/references/craft-elevation.md` (the craft layer; this is what separates
   a token-correct build from one that reads "designed, not AI-flat"). Honor the concept's **cohesion
   decision** (shared DNA vs. allowed variation; the one-canvas + contained-dark-moment call).
   - **Make the craft concrete + buildable, not adjectives.** Capture as real values the builder can
     apply directly: an **EFFECT PALETTE** (which of soft-depth / glass / blur / progressive-blur /
     accent-lift / motion — *per register*, mapped to real effect-style keys or `set_effects` params,
     with where + how strong), the **color-codes** (bg, surfaces, the 1–2 accent roles with hex +
     text-safe variants, tri-encoded status colors), and the **emphasis rules** (mono numerals, hero
     hierarchy, say-it-once, what gets amplified vs. recede). These are the difference between "feels
     modern" and a builder that can execute it. **Calibrate, don't max out:** advanced features go
     적재적소 — right place, right amount, fit to each surface's UI-UX purpose; over-decoration is as
     much a fail as flatness, and "modern/professional" is whatever the direction chose, not a fixed
     style.
4. **Build the signature layer** → `signature-layer.md`. The concept's distinctiveness usually needs
   bespoke assets the stock kit lacks: the **motif** (how it's constructed as a component/asset), the
   **semantic motion** (a motion token spec — what it does and what it *means*, e.g. a settle/glow that
   reads as "confirmed"), and any **illustration** language. For each: how it's built or sourced in the
   library, how it's bound (token/variant/asset), and the feasibility/gap. This is the most
   concept-specific output — don't skip it into a generic style note.
5. **Transfer the layout language** → `pattern-transfer.md`. Take the concept's layout/composition
   intent and map each recurring unit (row, stat block, card, hero, form section, tab/chip/segmented
   control, badge, pinned-action zone) to **library components** via its structural anatomy: element
   order, fill/hug/fixed sizing, separator mechanism, primary-action + accent placement → use / adapt /
   assemble / gap.
6. **Author interaction/motion, haptics, voice.** `interaction-motion.md` (carries the concept's
   semantic motion, platform-gated), `haptics.md` (mobile-native only — omit otherwise), and
   `brand-voice.md` (voice/tone/personality derived from the concept's direction; grounds COPY.md).
7. **Cross-cutting asset prefetch + stage them INTO Figma.** If `<sot>/design/visual-needs.json` names
   concrete global assets independent of screen layout (brand marks, payment-provider logos, partner
   logos), dispatch `visual-researcher` in `asset_pack` mode now; validate, save under
   `<sot>/_build-cache/assets/`, record the pack path in `state.json`. Leave ambiguous icons, hero art,
   photos, and Lottie moments for Step 4.
   - **Division of stores (2026-06-19):** the **file system holds the structured/diffable** layer —
     `asset-manifest.json` (provenance, license, slug→file map), JSON, specs, memory. **Figma holds the
     visual** layer — stage the procured images onto a **`📦 Assets` page** (import each as an image
     node, name it by slug; optionally promote recurring ones to components) and the analyzed Step-2
     reference screenshots onto a **`🔖 References` page**. Then the canon co-design + every builder
     **reference and reuse those Figma nodes directly** (clone / re-instance — no re-`import_image` per
     screen, refs visible on-canvas to eyeball against), while provenance stays auditable in the
     manifest. Record the Figma asset/ref page ids in `state.json`.
8. **Map to the library.** Follow `references/library-mapping.md`: bind each decision to a concrete
   library token/variant (color role → token, density → spacing scale + component sizes, type level →
   text style, shape → radius token, key components → variants to favor), plus the signature layer's
   bespoke bindings. Include a **feasibility audit**: what the library expresses directly, what needs
   assembled primitives, what must be escalated. Write `library-mapping.md`.
9. **Write component preference rules** → `component-preferences.md`: list vs card vs table, tabs vs
   segmented controls, bottom sheet vs modal, inline stats vs metric cards, and library variants by
   screen situation. Rules of use, not new components.
10. **Roll up + validate.** Write `foundation.json` (the machine-readable summary the spec and builder
    consume) and confirm it validates against `assets/foundation.schema.json`.

## Guardrails

- **Add no new taste.** Every aesthetic decision derives from `concept.md` or is a flagged gap. If
  you're choosing a color/feel the concept didn't, you're redesigning — stop and derive or escalate.
- **Don't invent raw values.** Every color/spacing/type decision resolves to a library token, or it's
  a flagged gap. The foundation never contains a hex value the library can't produce.
- **Respect the audience.** Use the Research step's audience to tune density/tone *within* the
  concept's direction — never against it.
- **The signature layer is not optional.** A foundation that systematizes the generic tokens but drops
  the concept's distinctive motif/motion has flattened the direction — the exact failure Gate A exists
  to prevent.

## References

| File | Role |
|---|---|
| `../figma-product-direction/references/concept-template.md` | The `concept.md` contract — exact sections this step consumes |
| `../figma-product-direction/references/craft-elevation.md` | **Anti-flat craft layer.** The craft toolkit (precision vs texture) per register; universal anti-flat moves; real-app reference sourcing; validate in HTML before Figma. Read when authoring `design-language.md`/`signature-layer.md`. |
| `references/library-mapping.md` | Map every foundation decision → library tokens/variants; gap escalation |
| `references/platform-conventions.md` | **Platform → UX patterns + microcopy conventions.** Read when authoring interaction-motion.md, haptics.md, and any copy that names an input gesture. Consumed by figma-product-spec and figma-product-build. |
| `references/design-language-research.md` | Protocol for extracting a concrete design-language profile from the concept + references (anchor *selection* now lives in Step-2 Direction) |
| `assets/foundation.schema.json` | The `foundation.json` rollup schema |
| `../figma-visual-researcher/SKILL.md` | Kit screenshots + concrete asset-pack procurement |
