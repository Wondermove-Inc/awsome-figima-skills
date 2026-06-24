# Concept divergence & critique — generate real alternatives, then kill the generic

This file spells out two complementary methods, fully self-contained: **divergence** (generate
several genuinely distinct concepts before choosing) and **adversarial critique** (structured
scoring with an explicit anti-generic lens). The goal is to stop the pipeline's #1 art-direction
failure: **converging on the first safe, generic idea.**

---

## A. Diverge — the angle menu

Generate **4–5 concepts from genuinely different angles** so they don't collapse into one idea with
reskins. Pick angles that are orthogonal for *this* product; span at least these:

| Angle | The organizing question | Yields |
|---|---|---|
| **Metaphor-led** | What real-world thing is this product *like*? | a system metaphor (stadium, ledger, trail, control room, studio) that organizes layout + language |
| **Motion/energy-led** | How does it *move and react*? | a feel defined by transitions, settle, momentum, the signature moment |
| **Data/clarity-led** | What if the information *is* the aesthetic? | restraint, density, typographic hierarchy as the look (think terminal/editorial) |
| **Emotion-led** | What should the user *feel* in one word? | pride / calm / momentum / mastery → drives contrast, color temperature, scale |
| **Material/trend-led** | What current aesthetic *fits this audience*? | a purposeful use of an era-trend (glass, soft-depth, brutalist) tied to a register |
| **Contrarian** | What does the category *always* do — and what if we didn't? | a provocation that tests whether the brief's defaults are real constraints |

Use the **taste-scan** (era-trends + category-taste) as raw material — a trend can *be* a concept's
spine (the "material/trend-led" angle), but it must earn its place in critique (§C), not just be hot.

### Push past the safe idea — techniques

- **Cross-domain analogy** — borrow structure from a *different* field that solved the same job
  (a trading terminal for dense status; a museum for a portfolio; a coach's clipboard for progress).
- **Provocations** — force range by asking each: *what if this were…* a physical product? a luxury
  good? a pro tool used 8 hours a day? a game? the opposite of what the category expects? Each
  provocation, taken seriously for 2 minutes, mutates a safe concept into a distinct one.
- **The "name it" test** — if you can't give the concept a 2–3 word name that a stranger could
  picture, it isn't distinct enough yet.

### Write each concept as `concepts/concept-X.md`

- **Thesis** — one sentence: the point of view.
- **Signature device** — the *one* thing you'd recognize it by.
- **Register treatment** — how energy vs trust surfaces look under it (ties to `register-cohesion-model.md`).
- **Meaning-encoding** — how each screen's hero carries its meaning (not decoration).
- **Craft toolkit** — the 4–6 concrete moves (depth, hero numerals, motion, status, motif…).
- **Taste-scan elements used** — which trend/category-taste it adopts, and on which register.

---

## B. The anti-generic squint test (run on every concept)

> **Cover the logo and the copy. Could this be any competitor in the category?** If yes, it is
> generic — and generic is the enemy, not "bad". A technically-correct, inoffensive, *forgettable*
> concept fails this step even though nothing is wrong with it.

The boldness lens: for any concept that feels safe/bland, ask *what's the boldest version of this
that still serves the purpose?* — then score the bolder version, not the timid one.

---

## C. Critique — structured scoring (`concepts/critique.json`)

Score every concept 1–5 on each axis. Be adversarial: you are trying to *kill* concepts, and a
defended darling is a bias to fight.

| Axis | 1 (fail) ⟶ 5 (excellent) |
|---|---|
| **Purpose-fit** | decorates ⟶ makes every screen measurably better at its job |
| **Distinctiveness** | could be any competitor ⟶ instantly recognizable, ownable |
| **Cohesion** | energy & trust read as two apps ⟶ one unmistakable product |
| **Craft ceiling** | tops out flat ⟶ enables high-craft moves natively |
| **Feasibility** | fights the target kit / Figma ⟶ buildable cleanly in the kit |
| **Accessibility / legibility** | treatment costs contrast/touch/readability ⟶ never; a11y safe |
| **Freshness vs. timelessness** | dated-on-arrival or trend-chasing ⟶ modern *and* durable |

**Kill rules (hard):**
- Distinctiveness ≤ 2 → killed (it's generic), regardless of other scores.
- Accessibility ≤ 2 → killed or the offending move vetoed (a11y can veto a trend outright — e.g.
  liquid-glass over a value that must stay legible).
- Feasibility ≤ 2 → killed unless the unbuildable part is the gratuitous bit (then cut it).

For each concept write a **one-paragraph verdict** + a **graft list** (the ideas worth stealing into
the winner even if this concept dies). Output a ranked table.

---

## D. Hand-off to Converge

The Phase-5 convergence picks the top concept and grafts the best surviving ideas from the graft
lists into `concept.md`. If the top two are close and *combinable*, synthesize; if they're close and
*incompatible*, that's a real fork — surface both at Gate A rather than guessing. Never average two
concepts into mush; pick a spine and graft *details*, not theses.
