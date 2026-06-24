# Authoring DESIGN.md — library-faithful spec + per-screen layout intent

`DESIGN.md` follows the `@google/design.md` schema (the same format the `figma-design-md` skill
produces) so it lints cleanly and is portable. Read that skill's `design-md-schema.md` for the
authoritative token/section rules; this file covers the two things specific to greenfield authoring:
**library-faithful tokens** and the **`## Screens` layout-intent section**.

## Token frontmatter — from the library, not from taste

The YAML frontmatter (`colors`, `typography`, `spacing`, `rounded`, `components`) must mirror the
`foundation/library-mapping.md` bindings. Rules:

- **Every token corresponds to a real library token role.** Concrete values may appear for the spec's
  human readability, but each must be the value of a named library token (record the token name in the
  prose so the builder knows which variable to bind). The builder will bind the library variable —
  never a literal — so a value with no backing token is a latent zero-raw-hex violation.
- **Use the recommended semantic names** where possible (`primary`, `secondary`, `surface`,
  `on-surface`, `error`; `headline-lg`, `body-md`, `label-sm`; `rounded.sm/md/lg`). It keeps the spec
  legible and maps cleanly onto most libraries.
- **Spacing** comes from the library's spacing scale (e.g. shadcn `spacing/2..6`), not invented
  numbers. If the project's memory declares `spacingPolicy: "raw-integers-allowed"`, discrete-scale
  integers are acceptable — otherwise tokens only.
- **components** entries capture per-component style intent (which variants to favor for this
  aesthetic), referencing tokens with `{path.to.token}`.

## Prose sections — grounded rationale

Use the standard section order (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes,
Components, Do's and Don'ts). Keep the rationale tied to `foundation/design-language.md` — the prose
explains *how to apply* the tokens for this audience and adopted aesthetic. The Do's and Don'ts should encode the
foundation's guardrails (e.g. "Do ration the accent to one primary action per screen").

## The `## Screens` section — greenfield layout intent + per-screen art direction

This is what makes DESIGN.md buildable without an original frame. Each screen block carries two layers:
the **structural intent** (regions, components, sizing — from `prd-analysis.json`) and the
**art-direction intent** (what this screen should *mean* and *feel* — from `direction/concept.md`).
Specify decisions, not the pixel design — visual polish is the builder's craft. Recommended structure
per screen:

```markdown
## Screens

### <screen-id> — <name>
**Purpose:** <one line from the PRD>
**Register:** <energy | trust | neutral>  (REFERENCED from concept.md's Register map — never re-tagged here)
**Creative mode:** <bolder·overdrive·delight | quieter·distill·polish | polish·layout>  (from concept.md Creative-mode map)
**Archetype:** <list | detail | form | dashboard | feed | gallery | profile | text-heavy>
**Metaphor:** <the organizing metaphor for this screen, drawn from concept.md Signature DNA → Metaphor family>
**Expresses:** <what this screen should make the user feel — synthesized from the Direction statement + this screen's named moves>
**Hero + meaning-encoding:** <#1 focal element> — <what it MEANS, carried by hierarchy (size/position/color), NOT a redundant badge>
**Hierarchy rank:** <#1 focal element> › <#2> › <#3>  (what wins the glance, in order)
**Craft moves:** <1–3 concrete moves from concept.md's Craft toolkit for THIS screen's register>
**Signature usage:** <where/if the concept's signature motif appears on this screen — or "none">
**Motion:** <the semantic motion for this screen, from concept.md Signature DNA → Semantic motion — or "n/a (static spec)">
**Regions (top→bottom / outer→inner):**
- <region> — <which library component/family fills it> · <FILL|HUG|FIXED behavior> · <hierarchy note>
- ...
**States to render:** default, empty, error  (only those the PRD requires)
**Primary action:** <the one accent action, if any>
**Asset needs:** <hero-image | photo | illustration | avatar | logo | none> — <brief usage, or "none">
**Notes:** <anything structural the builder must honor — e.g. "sidebar FIXED 280, main FILL">
```

Guidance — these are **decisions, not pixels.** Each field is one choice that is cheap to state here
and expensive to recover from at build time (a wrong archetype = a section rebuilt; a missed asset = a
build-time STOP). Leave exact spacing, variant micro-choices, and visual polish to the builder;
over-specifying craft here just duplicates `figma-design-patterns` and gets stale.

**Structural fields (from `prd-analysis.json` + `design-language.md`):**

- **Archetype** — name the layout pattern so the builder doesn't default to the generic AI shape (a
  monotonous card-per-item list, a hero-metric grid). The archetype is the single highest-leverage
  steer against "looks generated."
- **Hierarchy rank** — order the 1–3 elements that should win the glance. One line, but it is what
  prevents inverted hierarchy (a status badge out-weighing the title) — the exact failure the L3
  hierarchy gate fails on. Pair with the one **Primary action** (the accent budget).
- **Regions + component families + sizing** (FILL/HUG/FIXED) — the layout contract. A region line names
  **what fills it** (the component family / role), its **sizing**, and a **hierarchy note** — NOT a
  frozen, child-by-child assembly recipe. Specifying every internal part (`Card + Badge + chevron + cover
  + title + meta`) collapses the builder into a transcriptionist and the screen comes out as lifeless
  kit-assembly; it also breaks when the chosen component doesn't decompose that way. Name the container
  and its intent, set the sizing and the focal hierarchy, and leave the internal composition — exact
  parts, spacing, variant micro-choices — to the builder's craft. The spec is a contract of *what* and
  *roughly where*, not an assembled wireframe.
- **Asset needs** — name any real media the screen requires (a hero image, a photo, an illustration) so
  the visual-research prefetch resolves it **before** the build, not as a build-time escalation. A
  screen that needs imagery and declares `none` ships an empty gray placeholder. `none` is a valid,
  deliberate answer — most utilitarian screens need no media.
- **States to render** — only the ones the PRD confirmed must exist. How each state *looks* is craft
  (builder); *that* it exists is functional (already decided in Step 1).

### Art-direction fields — bind each to its `concept.md` section

The signed-off `direction/concept.md` (Step 2, the only human creative gate) carries the intent; the
spec's job is to *express it on this exact screen*, not re-invent it. Bind each field to the **exact
concept.md section heading** below — never coin your own names, and never re-decide what concept.md
settled:

| Spec field | `concept.md` section it reads | What you write |
|---|---|---|
| **Register** | **Register map** | The finalized register, *referenced*. Spec **never re-tags** a screen's register — if it feels wrong, that's a Step-2 fix, re-flow from there. |
| **Creative mode** | **Creative-mode map** | This screen's mode verbatim: `bolder·overdrive·delight` (energy) / `quieter·distill·polish` (trust) / `polish·layout` (neutral). |
| **Metaphor** | **Signature DNA → Metaphor family** | The organizing metaphor as it applies to this screen. |
| **Expresses** | **Direction statement** + this screen's named moves in the **Creative-mode map** | A per-screen *synthesis* (not a single named concept.md field): the feeling this screen should land. |
| **Hero + meaning-encoding** | **Meaning-encoding philosophy** | The focal element + what it MEANS. Encode meaning by hierarchy (size/position/color). A value or state already legible by hierarchy must NOT be restated by a redundant badge/label — that is **PC13**, the redundant-label gate (see `copy-system.md`'s "No redundant labels"). |
| **Craft moves** | **Craft toolkit per register** (the sub-section for *this screen's register*) | 1–3 concrete moves the builder reaches for here (e.g. hero numerals + signature glow for energy; tabular numerals + one rationed accent for trust). |
| **Signature usage** | **Signature DNA → Motif / signature device** | Where/if the signature motif appears on this screen, or `none` (not every screen carries it — overuse cheapens it). |
| **Motion** | **Signature DNA → Semantic motion** | The semantic motion for this screen and what it means (e.g. a settle/glow that reads as "confirmed"), or `n/a` for a purely static spec. |

Why bind to exact headings: `concept.md` is a frozen contract (its template is
`figma-product-direction/references/concept-template.md`). If the spec invents field names or quietly
overrides the direction, the build drifts from what the user signed off at Gate A and the L3 reviewer —
which also judges against `concept.md` — has nothing consistent to check. **Hierarchy rank** (above)
and **Hero + meaning-encoding** are complementary: the rank orders the glance; the hero says what the
#1 element *means* and forbids restating it redundantly.

## Library gaps

If specifying a screen surfaces a component the library lacks (a pattern with no home), don't fudge
it in the spec. Record it and resolve with the user before finishing:
1. closest existing component/variant, 2. assemble from primitives, 3. escalate. Mark every gap
resolved in the spec (a short `> GAP RESOLVED: …` note) so the Step-4 spec gate passes and the builder
isn't blocked.

## Output check
Before handing off: the frontmatter lints (`npx @google/design.md lint`), every PRD screen has a
`### <screen-id>` block with its art-direction fields traced to `concept.md`, and no token lacks a
library backing. Then COPY.md.
