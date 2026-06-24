---
version: alpha
name: <Product / Design-language name>
description: <one line — adopted aesthetic + audience, e.g. "Toss-calm fintech for Korean 20–30s">
colors:
  # Each token mirrors a library token role (see foundation/library-mapping.md). Values shown for
  # readability; the builder binds the library variable, never a literal.
  primary: "#000000"
  secondary: "#000000"
  surface: "#FFFFFF"
  on-surface: "#000000"
  border: "#000000"
  error: "#000000"
typography:
  headline-lg:
    fontFamily: <library text style family>
    fontSize: 28px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: <family>
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-sm:
    fontFamily: <family>
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.2
spacing:
  # From the library's spacing scale.
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
rounded:
  sm: 4px
  md: 8px
  lg: 12px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
---

# <Product> Design

## Overview
<Brand personality, target audience, the feeling the UI evokes — grounded in the audience (from
prd-analysis.json), direction/concept.md, and foundation/design-language.md. Cite the concept's
direction statement and adopted aesthetic, and why it fits.>

## Colors
<Palette rationale. Map each descriptive name to its token. State the accent-rationing rule.>

## Typography
<Type personality + how hierarchy is built (size vs weight vs color).>

## Layout
<Grid/spacing strategy, grouping principle (proximity vs dividers vs cards), density stance.>

## Elevation & Depth
<Tonal layers vs shadows vs borders — how hierarchy is conveyed.>

## Shapes
<Radius language and consistency rules.>

## Components
<Per-component intent: which variants to favor for this aesthetic.>

## Do's and Don'ts
- Do <foundation guardrail>
- Don't <foundation guardrail>

## Screens

### <screen-id> — <name>
**Purpose:** <one line>
**Register:** <energy | trust | neutral>  <!-- REFERENCED from concept.md Register map — never re-tag here -->
**Creative mode:** <bolder·overdrive·delight | quieter·distill·polish | polish·layout>  <!-- concept.md Creative-mode map -->
**Archetype:** <list | detail | form | dashboard | feed | gallery | profile | text-heavy>
**Metaphor:** <screen metaphor>  <!-- concept.md Signature DNA → Metaphor family -->
**Expresses:** <the feeling this screen should land>  <!-- synthesis: Direction statement + this screen's named moves -->
**Hero + meaning-encoding:** <#1 focal element> — <what it MEANS, by hierarchy; no redundant badge (PC13)>  <!-- concept.md Meaning-encoding philosophy -->
**Hierarchy rank:** <#1> › <#2> › <#3>
**Craft moves:** <1–3 moves>  <!-- concept.md Craft toolkit for THIS register -->
**Signature usage:** <where the motif appears, or none>  <!-- concept.md Signature DNA → Motif / signature device -->
**Motion:** <semantic motion + what it means, or n/a>  <!-- concept.md Signature DNA → Semantic motion -->
**Regions (outer→inner / top→bottom):**
- <region> — <library component/family> · <FILL|HUG|FIXED> · <hierarchy note>
**States to render:** default<, empty, error — only those the PRD requires>
**Primary action:** <the one accent action, or none>
**Asset needs:** <hero-image | photo | illustration | avatar | logo | none> — <usage, or none>
**Notes:** <structural constraints the builder must honor>
