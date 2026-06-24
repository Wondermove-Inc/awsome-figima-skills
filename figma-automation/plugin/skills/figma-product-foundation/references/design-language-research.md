# Design-language research — concept → full, sourced design-language profile

The goal: turn the signed-off direction into a **transferable, sourced design language** you can apply
to this product and this library.

## Your input — the signed-off direction

You do **not** propose or pick an aesthetic. The aesthetic is settled: `concept.md` carries it,
human-approved at Gate A. **Your input is `concept.md`** — specifically its *Adopted aesthetic* (the
era-trend / category-taste chosen + why it fits this audience) and *Signature DNA* — plus the analyzed
reference screens captured in `<sot>/direction/refs/`. Read those and extract the profile below. Do
not re-open the aesthetic choice.

## Extract the profile (reuse the captured refs; research only to fill gaps)

**Reuse first — don't re-research the anchor.** Step 2 already captured the analyzed reference screens
in `<sot>/direction/refs/` and recorded the *Adopted aesthetic* in `concept.md`. Extract the profile
below from **those**. Only when the captured refs are insufficient for a specific decision (e.g. a
motion/haptic detail they don't show) do a **targeted top-up**: spawn a research subagent (`ToolSearch`
→ `select:WebFetch,WebSearch`) that returns a tight, cited digest for the missing piece, and save any
new image to `<sot>/foundation/refs/`. Cite every claim in `research-sources.md`. The builder grounds
itself by **opening these images with the Read tool**, so any image you rely on must live on disk.

### What to search for
- `<anchor> design language` / `<anchor> design system` — official writeups, design-team blogs.
- `<anchor> UI screens <relevant flow>` — real product screens for the flows in your PRD.
- `<anchor> motion` / `<anchor> animation principles` / `<anchor> microinteractions`.
- `<anchor> haptics` / `<anchor> haptic feedback`.
- `<anchor> brand guidelines` / `<anchor> tone of voice` / `<anchor> voice and tone`.
- Case studies (Medium, design publications, the company's own engineering/design blog).

Prefer **primary sources** (the company's own design blog, official brand site) over secondary
commentary. `WebFetch` the most authoritative 2–4 pages and extract specifics. Cite each in
`research-sources.md` (url + the exact claim you took from it).

> Note on cloud/headless runs: interactively-authenticated browsers may be unavailable. `WebSearch`
> + `WebFetch` are the reliable path here; don't depend on a logged-in browser session.

### What to extract — the full profile (not just visuals)

Write these files. For each bullet, capture the *principle* (how the anchor decides), not just an
instance, so it transfers. **Color and tokens are necessary but the least of it.** The highest-leverage
thing to extract is the anchor's **layout and compositional language** — how its screens are *structured*
— because that, far more than palette, is what separates a designed product from a generic one. Pull it
out in depth for every distinct screen archetype the anchor shows; do not treat layout as an afterthought
to color.

**design-language.md**
- **Color philosophy & temperature** — how many colors, how restrained, warm/cool, how the accent is
  rationed (e.g. "single accent, used only for the one primary action per screen"). Light/dark stance.
- **Typography system** — type personality, scale relationships, weight usage, how hierarchy is built
  (size vs weight vs color), any numerals/data treatment.
- **Spacing & density rhythm** — generous vs dense, the base grid, how grouping is signaled (proximity
  vs dividers vs cards).
- **Shape & radius language** — corner-radius personality (sharp/engineered vs soft/friendly),
  consistency rules.
- **Iconography & imagery** — icon style (line/filled/duotone), illustration vs photography, how
  imagery is used.
- **Elevation & depth** — shadows vs tonal layers vs borders; how hierarchy is conveyed.
- **Layout & composition system** — the structural backbone: how each recurring surface is *built*.
  Screen skeleton (header / scrollable content / pinned action zones, safe-area), grid and column
  behavior, the anatomy of every recurring unit (list row, stat block, card, hero, form section,
  tab / chip / segmented control, status badge, primary-action zone), how each unit sizes (fill vs hug
  vs fixed), and how separation is signaled (whitespace vs hairline vs card — and *when* each is used).
  This is the most transferable layer of all; extract it per screen archetype, not once for the whole app.

**interaction-motion.md**
- Transition language (what animates between states/screens), easing/timing *feel* (snappy vs
  gentle), signature micro-interactions, gesture vocabulary (swipe, pull, long-press conventions).

**haptics.md**
- When haptic feedback fires (success, selection, error, threshold), what each communicates, and the
  intensity language (light tick vs firm thunk). Even if the target build is a Figma static design,
  this documents intended behavior for handoff and grounds motion choices.

**brand-voice.md**
- Voice (the personality — e.g. "a calm, competent friend"), tone shifts by context (celebratory on
  success, plain and steady on error), terminology conventions, and stated design principles. This
  file grounds `COPY.md` in Step 4 — write it so a copywriter could adopt the voice from it alone.

### Transfer, don't transplant — record each pattern as builder-executable structural anatomy
You are extracting a *way of deciding*, then re-applying it to this product's content and the target
library. A screenshot reproduction is the wrong artifact. The right artifact, in `pattern-transfer.md`,
is — for **every** distinct layout pattern the anchor shows — its **structural anatomy a builder can
reconstruct without the screenshot**: the element order/composition, each part's sizing behavior
(fill / hug / fixed), the separator mechanism, the alignment, where the primary action and the accent
sit, and which of *this* product's surfaces it maps to. "Group related items by proximity and a hairline
divider, not cards" is the right altitude; "looks like <anchor>" is not.

Capture the **full set** (every recurring row, grid, hero, card, form section, tab, chip, toggle,
badge, nav, and pinned-action zone) — a thin pattern list is the failure mode this step exists to
prevent, because a builder handed only colors rebuilds a generic layout no matter how good the palette.
Map each pattern to a concrete library component/variant, or flag it as an assembled structure when the
library has no single component for it.
