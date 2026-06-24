# `concept.md` — the Direction contract (frozen template)

This is the **contract** between Step 2 and everything downstream. Foundation, spec, build, and the
L3 reviewer all bind to the **exact section headings** below — **do not rename them.** Filled at
Gate A approval and written to `<sot>/direction/concept.md`.

If a section would be empty, write "n/a — <why>" rather than deleting it (downstream looks for it).

```markdown
# Direction — <Project Name>

## Direction statement
<one line: "X for people who Y, so it feels Z">

## Signature DNA
- **Motif / signature device:** <the one thing you'd recognize it by>
- **Semantic motion:** <the signature motion AND what it MEANS — e.g. a settle/glow that reads as "confirmed">
- **Metaphor family:** <the organizing metaphor, if any>
- **Form language:** <corner family · depth/elevation language · contrast posture>

## Adopted aesthetic
- **Era-trend adopted:** <name> — lands on <which register/surfaces> — fits THIS audience because <why>
- **Category-taste:** <what fans of this category expect, and how we meet/subvert it>
- **Rejected:** <trend or idea> — because <why it failed purpose/register/legibility>

## Register map
| Screen | Register (energy / trust / neutral) | Rationale (only if adjusted from Step 1) |
|---|---|---|

## Creative-mode map
| Screen | Register | Mode (bolder·overdrive·delight / quieter·distill·polish / polish·layout) | 1–2 named moves |
|---|---|---|---|

## Cohesion decision
- **Shared DNA (constant across ALL registers):** <type · spacing rhythm · accent role · radius family · icon family · motif · depth language>
- **Allowed variation (by register):** <density · contrast · motion intensity · decoration>
- **Canvas call:** one canvas = <light | dark>; contained dark "moment" sanctioned at: <where, or "none">

## Craft toolkit per register
### Energy / expressive
- <concrete moves: hero numerals, motion, signature glow, characterful data-viz, vivid status…>
### Trust / transactional
- <concrete moves: restraint, tabular numerals, tight crisp depth, one rationed accent…>
### Neutral / utility
- <concrete moves: clean rhythm, clear scanning, focal element recedes…>

## Meaning-encoding philosophy
<how each screen's hero carries its meaning by hierarchy — and the rule that a value/state legible by
position/size/color must NOT be restated by a redundant badge/label (PC13).>

## What this is NOT
- <explicit anti-patterns this direction forbids — the slop and the off-brand moves>
```

## Downstream binding map (which step reads which section)

| Section | Read by | Used for |
|---|---|---|
| Signature DNA · Adopted aesthetic · Cohesion decision · Craft toolkit | **Step 3 foundation** | tokens + the bespoke signature layer (motif/illustration/motion tokens) + library mapping |
| Creative-mode map · Craft toolkit per register · Signature DNA · Meaning-encoding | **Step 4 spec** | per-screen art-direction fields (Metaphor / Expresses / Hero+meaning / Craft / Signature / Motion) + per-register mode — Metaphor/Signature/Motion come from Signature DNA |
| Craft toolkit · Signature DNA | **Step 5 build** | what the builder executes |
| Signature DNA · Meaning-encoding · What this is NOT | **Step 5 L3 reviewer** | the craft/function bar the build is judged against |

`register` has **one source of truth across the pipeline:** Step 1 (prd-analysis) sets the *initial*
tag → this **Register map finalizes it** → Step 4 spec only *references* it (never re-decides). If a
screen's register changes, change it here and re-flow, not in the spec.
