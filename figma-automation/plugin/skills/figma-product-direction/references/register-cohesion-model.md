# Register & cohesion model — how to keep a multi-surface product feeling like ONE thing

This is the linchpin decision of the Direction step. A product has surfaces with different jobs;
each job wants a different *intensity* of treatment. The risk is two-sided: treat them all the same
and the energy surfaces go dead; treat them too differently and it looks like two apps stapled
together. This model resolves both.

## 1. The register taxonomy

Every screen carries an emotional **register**, inherited from its purpose (set in Step 1) and
adjustable here with rationale.

| Register | The job of these surfaces | Examples (domain-neutral) |
|---|---|---|
| **Energy / expressive** | create momentum, pride, excitement, identity; make the user *feel* something | hero/home, achievement, leaderboards, results-celebration, marketing, onboarding peaks |
| **Trust / transactional** | create confidence and clarity; let the user *act without anxiety* | payment, settings, forms, legal/consent, data entry, dashboards-of-record |
| **Neutral / utility** (in-between) | get out of the way; support a task | lists, search, navigation, detail/reference views |

Assign every screen a register. Most products are **mostly one** with a few of the other — note the
dominant register, it anchors the shared canvas (see §3).

## 2. The creative-mode map (register → mode → moves)

The register sets the **creativity dial**. This is what makes "creativity" concrete and *purposeful*
rather than mood-driven. The mode names below are our own defined vocabulary — each is described in
the table, so the skill needs no external reference to use them.

| Register | Modes | Concrete moves it licenses | Modes it forbids |
|---|---|---|---|
| **Energy** | **bolder · overdrive · delight** | oversized numerals, high contrast, signature motion/glow, characterful data-viz, a memorable moment, vivid status | timid uniformity, mid-everything, decoration with no payoff |
| **Trust** | **quieter · distill · polish** | restraint, generous whitespace, tabular numerals, calm hierarchy, tight crisp depth, one rationed accent | grain/bloom/glow that competes with the value, decoration that costs legibility |
| **Neutral** | **polish · layout** | clean rhythm, clear scanning, the focal element recedes appropriately | hero treatment fighting the content |

In `concept.md`, produce the per-screen table: `screen → register → mode → 1–2 named moves`. The Spec
step copies this into each screen's art-direction fields; the Build step executes it.

## 3. The cohesion decision (shared constants vs. purposeful variation)

The single most important call. Decide explicitly **what is shared across ALL registers** (the DNA
that makes it one product) vs. **what is allowed to vary** (the intensity that lets each surface do
its job).

**Default the shared DNA to (these almost always stay constant):**
- type system (family + scale + the weight-contrast ratio)
- spacing rhythm (one scale)
- the accent **role** (one accent hue family, used for the same meaning everywhere)
- corner / radius family
- icon family
- the **signature motif** (the one recognizable device from the concept)
- depth language (the shadow/elevation family)

**Allow to vary by register (the intensity dial):**
- density (energy can breathe or compress for drama; trust stays calm)
- contrast / canvas *moment* (see the canvas rule below)
- motion intensity (energy moves more)
- decoration (signature glow/grain appears only where the register earns it)

### The canvas rule (the most common cohesion failure)

> **Canvas — light vs dark — is the LEAST transferable layer.** Flipping it per screen is what makes
> one app look like two. **Default to ONE canvas for the whole product** (usually what the trust
> surfaces need), and carry energy on expressive screens through **composition, not darkness**:
> the signature motif, oversized numerals, characterful data-viz, a vivid accent, motion. Energy is
> *not* the light↔dark axis.
>
> If a surface genuinely wants drama, prefer a **contained dark "moment"** — a single dark/gradient
> hero *card* bound to the light world by all the shared DNA — over a lone dark *screen* stranded
> among light ones. Cross the canvas only deliberately, and only with the DNA carried across.

(This rule and its worked reasoning live in `craft-elevation.md` — the cohesion section. Record the
*decision* — one canvas + where any contained dark moment is sanctioned — in `concept.md`.)

## 4. Worked decision (domain-neutral)

A product with an expressive home (energy), a list (neutral), and a checkout (trust):

- **Shared DNA:** one type scale, one 8px spacing rhythm, a single accent hue used only for the
  primary action + positive status, one radius family, one icon family, a "ring" signature motif,
  floating-card depth.
- **Varies:** home compresses and goes high-contrast with an oversized hero metric + the ring motif
  animated (bolder/overdrive); checkout stays light, calm, generous, tabular numerals, the accent
  reserved for the single confirm action (quieter/polish); the list is plain, scannable, the motif
  appears once as a small accent (polish).
- **Canvas:** one light canvas throughout; the home's drama comes from a contained dark gradient
  *stat card*, not a dark screen.

Result: three different intensities, one unmistakable product.

## 5. Output

Write into `concept.md`:
1. the **register map** (every screen → register, with any rationale for adjustments off Step 1),
2. the **creative-mode map** (screen → register → mode → moves),
3. the **cohesion decision** (the shared-DNA list + the allowed-variation list + the canvas call),
   each with a one-line *why*.
