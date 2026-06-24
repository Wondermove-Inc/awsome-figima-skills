---
name: figma-product-direction
description: >-
  Art-direction step of the product pipeline. Use after figma-product-prd (Research) and before
  figma-product-foundation. Turns the research (purpose map + register tags + audience) into a
  distinctive, purposeful visual DIRECTION: grounds on real references + a current taste scan
  (era-trends + category-taste), decides the register/cohesion system, DIVERGES into several
  orthogonal concepts, CRITIQUES them adversarially (anti-generic), converges to one signed-off
  concept.md (signature DNA + craft toolkits + creative-mode-per-register map), proves it with an
  HTML look-&-feel, and gates on ONE human direction sign-off. Invoked by /figma-product; also
  runnable standalone to (re)set the art direction.
---

# /figma-product-direction — Art Direction (Step 2)

This step decides **what the product should look and feel like, and why** — before any token,
component, or screen exists. It is the difference between a build that is merely *correct* and one
that is *distinctive and purposeful*. The Research step (Step 1) defined **what each screen is for**;
this step decides **how that purpose is expressed**, and hands the next step a concept concrete
enough to systematize.

It is the **only step with a human creative gate** (Gate A). Everything downstream — foundation,
spec, build — executes this direction faithfully. So this step must be both **divergent** (explore
real alternatives, not the first safe idea) and **rigorous** (kill generic, kill trend-for-its-own-sake,
defend every choice by purpose).

---

## Mental model — the hat you wear here

> **You are the art director / design lead.** Not a researcher (that was Step 1), not a systems
> engineer (that's Step 3), not a builder (that's Step 5). Your job is *taste with a reason*:
> propose a strong point of view, then attack it until only the defensible part survives.

Operate in **three modes, in sequence — never collapse them:**

1. **DIVERGE** (generative): widen the space. Many distinct directions, orthogonal angles,
   cross-domain analogy. Suspend judgment. The enemy here is *converging too early on the obvious*.
2. **CRITIQUE** (adversarial): narrow ruthlessly. Score every concept against purpose, distinctiveness,
   cohesion, craft, feasibility, accessibility. The enemy here is *defending your darling*.
3. **CONVERGE** (committing): synthesize one direction from the winner + the best grafts of the
   runners-up. Write it down so precisely the builder cannot drift. The enemy here is *vagueness*.

**The creativity dial is driven by register, not by mood.** Each surface has a register (set in
Step 1); the register sets how bold the treatment runs:

| Register | Mode (the creativity dial — our defined vocabulary, below) | Looks like |
|---|---|---|
| **Energy / expressive** (competitive, achievement, hero, marketing surfaces) | **bolder · overdrive · delight** | high contrast, motion, oversized numerals, signature moment, personality |
| **Trust / transactional** (payment, settings, legal, data-entry, results) | **quieter · distill · polish** | restraint, legibility first, calm hierarchy, no decoration that competes with the number that matters |

A product is rarely all one register. The **cohesion decision** (Phase 2) is what keeps a
bolder dashboard and a quieter checkout feeling like *one product* — see
`references/register-cohesion-model.md`.

---

## Inputs

- **Step-1 research** (`<sot>/design/prd-analysis.json` + purpose map): screen list, per-screen
  **purpose + register tag**, audience, jobs-to-be-done, success metrics, platform.
- **Knowledge base** (cache-first — see `references/knowledge-base.md`): previously-analyzed
  references, the concept/metaphor catalog, craft principles, taste exemplars, and the **dated
  taste-scan** (era-trends + category-taste). Read before any live research; only research what's
  missing or stale.
- **Target library** (URL/key): the kit the build must use. The direction must be *buildable in this
  kit* — feasibility is a critique axis, not an afterthought.

## Output (what Step 3 consumes)

```
<sot>/direction/
├── taste-scan.json        # era-trends + category-taste, DATED (refreshable)
├── refs/                  # analyzed reference screens from Phase-1 grounding (reused by Step 3; don't re-research)
├── concepts/              # the diverged candidates + their critique scores
│   ├── concept-A.md … concept-E.md
│   └── critique.json      # structured scores + the kill/keep rationale
├── concept.md             # ⭐ THE signed-off direction (signature DNA, craft toolkits, mode map)
└── look-and-feel/         # the proof: 1 HTML screen per register zone + render PNGs + self-crit
```

`concept.md` is the contract. Foundation turns it into tokens + a signature layer; Spec applies it
per screen; Build executes it; the L3 reviewer judges against it.

---

## Process

Run the phases in order. Phases 1–5 are desk work (cheap, fast, no Figma). Phase 6 proves it in
HTML. Phase 7 is the human gate.

### Phase 1 — Ground (research the space, don't invent in a vacuum)

Three grounding passes, **cache-first** against the knowledge base; dispatch `visual-researcher`
only for what's missing or stale.

1. **Reference pass** — pull real, recent (2024+) product UI for this category and adjacent
   categories. Analyze **intent, not surface**: *why* does the category leader put the hero there,
   run dark, oversize the number? Transferable structure > pretty pixels. Save the captured refs to
   `<sot>/direction/refs/` (Step 3 reuses them — don't re-research) AND write the analyses to the KB.
2. **Taste scan** — *(this is what keeps the output modern and audience-true, not dated or generic)*
   write `taste-scan.json` with two parts, each **dated**:
   - **Era-trends**: the aesthetics currently in vogue — e.g. glass / *liquid-glass*, glow, bento,
     editorial-minimal, brutalist, claymorphism, soft-depth, mono-accent. For each: a one-line
     "what it is", its moment, and *where it works / where it fails*.
     ⚠️ **Trends rot.** Stamp the scan with the current date. If the cached scan is older than ~6
     months, **refresh it** (the trend menu in 2027 is not the menu in 2026). Never freeze.
   - **Category-taste**: what the people who *love this category* gravitate to — derived from the
     audience (Step 1) + the category leaders (Reference pass). (Competitive-sport fans → dark
     stadium energy; fintech → clean trust; meditation → soft gradient calm; dev tools → terminal
     density.) This is the taste-culture the product must feel native to.
3. **Craft pass** — load `references/craft-elevation.md`: the high-craft moves (elevation, depth,
   signature moment, motion semantics, anti-flat) and the slop tells to avoid.

> **The trend guardrail (read before you fall in love with liquid-glass):** a trend is adopted ONLY
> where it serves the screen's **purpose, register, and legibility** — the same "transfer intent,
> not surface" rule. Liquid-glass on a sunlit payment total *fails* legibility → veto. Glass cards on
> an energy dashboard *sing* → adopt. Being fluent in current aesthetics keeps us from looking dated;
> deploying them purposefully keeps us from trading AI-slop for **trend-slop**. A trend is a tool, not
> a goal.

### Phase 2 — Decide the system (register map + cohesion)

Before generating concepts, fix the rules they must satisfy. Using `references/register-cohesion-model.md`:

- Confirm the **register map**: every screen → energy or trust (or a named in-between), inherited
  from Step 1, adjusted with rationale.
- Make the **cohesion decision**: what is *shared* across all registers (the constants — type system,
  spacing rhythm, one accent role, corner language, the signature motif) vs. what *varies* (density,
  contrast, motion intensity, decoration). Write the decision + *why*. This is the single most
  important call for "feels like one product."
- Note which **era-trend / category-taste** elements are candidates, and on which register they'd land.

### Phase 3 — Diverge (generate distinct concepts)

Produce **4–5 genuinely different concepts**, each from a different angle so they don't collapse
into one idea with reskins (divergence before convergence — the antidote to the safe first idea).
See `references/concept-divergence.md` for the full angle menu; at minimum span:

- a **metaphor-led** concept (an organizing real-world metaphor — stadium, ledger, trail, control room),
- a **motion/energy-led** concept (the feel is defined by how it moves and reacts),
- a **data/clarity-led** concept (the information *is* the aesthetic — restraint, density, typographic),
- an **emotion-led** concept (what the user should *feel* — pride, calm, momentum), and
- one **contrarian** concept (deliberately rejects the category default — a provocation to test the brief).

Each concept is a short `concept-X.md`: **thesis** (one sentence) · **signature device** (the one
thing you'd recognize it by) · **register treatment** (how energy vs trust look under it) ·
**meaning-encoding** (how the hero of each screen carries its meaning) · **craft toolkit** (the 4–6
concrete moves) · **which taste-scan elements it uses**. Use cross-domain analogy and the
provocations in the reference to push past the safe first idea.

### Phase 4 — Critique (adversarial scoring, anti-generic)

Score every concept adversarially — structured scoring + remediation, through an explicit
anti-generic lens (is this too safe / bland / generic?). Write `critique.json` scoring each on:

| Axis | Question |
|---|---|
| **Purpose-fit** | Does it make each screen *better at its job*, or just decorate? |
| **Distinctiveness** | Squint test — could this be any competitor? If yes, it's generic → penalize hard. |
| **Cohesion** | Do energy and trust surfaces read as one product under it? |
| **Craft ceiling** | Does it enable high-craft moves, or top out at flat? |
| **Feasibility** | Buildable in the target kit + Figma without fighting the tools? |
| **Accessibility / legibility** | Does the treatment ever cost contrast, touch size, or reading the number that matters? (a11y can VETO a trend) |
| **Freshness vs. timelessness** | Modern without chasing a trend that will look dated in a year? |

Be ruthless: **the safe/generic concept dies here even if it's "fine."** Note what each concept
should *borrow from* before it's killed (the graft list). Output scores + a one-paragraph verdict
per concept.

### Phase 5 — Converge (write `concept.md`)

Pick the winner; graft the best surviving ideas from the runners-up. Write `concept.md` — the
direction contract — **using the frozen template in `references/concept-template.md`** (downstream
steps bind to its exact section headings; don't rename them). It contains:

*(Use the EXACT headings from `concept-template.md` — downstream greps them. The bullets below name them.)*

- **Direction statement** ("X for people who Y, so it feels Z").
- **Signature DNA**: the motif/device, the **semantic motion** (e.g. a signature glow/settle that
  *means* success), the metaphor family, the form (corner/depth/contrast) language.
- **Adopted aesthetic**: the era-trend / category-taste adopted + where it lands + why it fits *this*
  audience; and what was rejected and why.
- **Register map** and **Cohesion decision**: carry them verbatim from Phase 2 (shared DNA vs.
  allowed variation; the one-canvas + contained-dark-moment call).
- **Creative-mode map**: every screen (from Step 1) → its register → its mode → 1–2 named moves.
- **Craft toolkit per register**: the concrete moves Spec/Build will reach for on energy vs trust
  surfaces (this is where bolder/overdrive vs quieter/distill becomes a checklist).
- **Meaning-encoding philosophy**: how heroes carry meaning (the lesson that a value/number/state
  should be *legible by hierarchy*, not restated by a redundant badge — ties to PC13).
- **What this is NOT** — the anti-patterns this direction explicitly forbids.

### Phase 6 — Prove it (look-&-feel gate)

A direction on paper is a hypothesis. Prove it **cheaply** here, before the pipeline commits — this is
a fast *feel-check of the concept*, **not** the production canon.

> **Scope note (2026-06-19): Phase 6 ≠ the build canon.** The real, high-craft **canon screens are
> co-designed for real in Figma, WITH the user, at the START of Step 5 (build) — AFTER the spec**, once
> the foundation has wired up the library/tokens/effects/assets so they're actually buildable. That is
> where the user settles production craft (depth/effects, the bottom bar, alignment, spacing) by hand
> and gives the real hands-on sign-off, and where the rest of the screens then fan out to agents (see
> `figma-product-build` → Rollout). Phase 6 stays a **cheap HTML feel-check of the direction** — don't
> over-polish it or try to make it the canon; it just has to validate the *concept* enough for Gate A.

**Medium choice — HTML to diverge, Figma to prove effects/material (2026-06-19):**
- **Diverge in HTML.** The 4–5 concepts and the broad *vibe* (color, type, composition, layout) are
  cheapest and fastest as throwaway HTML/CSS — fidelity doesn't matter yet, breadth does.
- **Prove the WINNING direction's effect/material layer in a small Figma mini-mood-board** before
  Gate A — anything that **renders differently across media** (glass, blur, depth, native effects) or
  that the user will *sign off on*. CSS `backdrop-filter` ≠ Figma native `GLASS`; an HTML render can
  promise a look the Figma build then can't reproduce 1:1, which forces re-litigation. Proving the
  effects in Figma (real library/tokens/effects) makes the sign-off **predict the build**. This needs
  the foundation/library wired, so it naturally runs as a light Figma pass *after Step 3*, feeding
  Gate A. **Rule of thumb: vibe/layout → HTML; effects, material, and anything signed-off → Figma.**

Per `references/look-and-feel-gate.md` (the HTML diverge recipe):

- Build **one representative screen per register zone** (≥1 energy + ≥1 trust) as **static HTML/CSS**
  — fast, throwaway, *not* Figma. Use the real strings (Step 1 copy) and the concept's signature moves.
- **Render headless** to PNG (the reference shows the recipe). Look at the *rendered pixels*, not the code.
- **Self-critique** — run the **subtraction pass FIRST, side-by-side with the captured `refs/`**
  ("what did I ADD that the shipped reference didn't?" — this is what kills AI-chrome slop that presence
  checks wave through), then the Phase-4 rubric + squint test + slop scan + legibility check. Refine
  **one** pass. (Feel check, not a build — don't polish to perfection; check the *direction*.)
  **Do not advance to Gate A until the subtraction pass has run** — if the user catches additive chrome,
  this step was skipped.

This gate catches a weak/generic/dated direction **before** Step 3 systematizes it — far cheaper than
discovering it after screens are built.

### Phase 7 — Gate A (the human direction sign-off)

Present to the user: the **direction statement**, the **look-&-feel renders** (1 per register), the
**cohesion decision**, and the **adopted aesthetic** (which trend/taste, and why it fits *them*).
Frame it as *"이런 느낌으로 가려고 해요 — 왜냐하면…"*.

- **Approve** → write `concept.md` as final, record Gate A in `state.json`, write the winning
  concept + analyzed refs back to the knowledge base, advance to Step 3.
- **Steer** → one focused revision loop (usually a graft swap or register/cohesion tweak, rarely a
  full re-diverge). Re-render the affected zone, re-present.

This is the gate that makes the rest of the pipeline safe to run autonomously: once the *feel* is
signed off, foundation/spec/build don't re-litigate taste — they execute it.

---

## Knowledge base (cross-project memory)

This step both **reads** the shared KB (so each project starts from accumulated taste, not zero) and
**writes** to it (so the next project is smarter). Full contract in `references/knowledge-base.md`.
Read cache-first; write the winning concept, the analyzed references, and the dated taste-scan; let
`figma-playbook consolidate` curate. Never let a stale cached trend scan ship — check the date.

## Anti-patterns (this step's own slop guard)

- **Converging on concept 1** — if you didn't generate genuine alternatives, you didn't do Phase 3.
- **Trend-chasing** — adopting liquid-glass/glow because it's hot, not because it serves a surface.
- **Decoration mistaken for direction** — a gradient and a shadow are not a point of view.
- **Cohesion by uniformity** — making everything the same register to "feel cohesive" (kills energy
  surfaces). Cohesion = shared constants + purposeful variation, not sameness.
- **Vague concept.md** — "modern, clean, bold" is not a direction. If the builder can't act on it
  without guessing, it fails. Every claim must be a concrete, buildable move.
- **Skipping the HTML proof** — committing the pipeline to an unproven feel.

## References

| File | Role |
|---|---|
| `references/concept-template.md` | The frozen `concept.md` contract — exact section headings + the downstream binding map (which step reads what) |
| `references/register-cohesion-model.md` | The register taxonomy + the cohesion decision-model (shared constants vs. purposeful variation) |
| `references/concept-divergence.md` | The divergence angle menu, cross-domain analogy, provocations, and the structured critique rubric |
| `references/craft-elevation.md` | High-craft moves (elevation, depth, signature moment, semantic motion, anti-flat) + slop tells |
| `references/look-and-feel-gate.md` | The HTML look-&-feel recipe: build 1 screen/zone, headless render, self-critique loop |
| `references/knowledge-base.md` | Cross-project KB read/write contract (references, concepts, craft, exemplars, dated taste-scan) |
