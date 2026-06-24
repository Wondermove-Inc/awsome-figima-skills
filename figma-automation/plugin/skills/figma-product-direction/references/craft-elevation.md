# Craft elevation — making a build feel designed, not AI-flat

The most common failure of a component-first, token-rationed build is that it reads **"flat /
AI-generated"** — every token is technically correct and the result is still emotionally dead. That
critique is real and recurring (it is usually the first thing a client or senior stakeholder says).
Correct tokens are the floor, not the ceiling. This file is the **craft layer on top of correct
tokens**: it tells the foundation to name, per surface, the concrete craft moves so the spec and
builder *execute craft*, not merely bind variables.

The guiding idea: **AI-assisted design is fine — _generic_ is the enemy.** The fix is not "more
effects." It is the *right* effects for the surface's emotional register, applied with intent.

## Slop has TWO opposite failure modes — check for both

"Looks AI-generated" comes from *either* too little craft *or* too much decoration. They are
opposites, so a screen that passes one check can still fail the other. Scan for both.

### Tell-set A — "AI-flat" (too LITTLE — no hierarchy, emotionally dead)

- Single flat fills; content sitting on a white ground with no elevation (white-on-white).
- A uniform, equal-weight card grid — every element the same size and visual weight, no focal point
  (e.g. a "live" row weighted identically to a "finished" one — status differences not expressed).
- Status encoded only as a **gray pill / label**; no color, no icon.
- Generic stock icons; cold mathematically-perfect gradients; no implied light source.
- Mid-sized everything — no oversized hero, no hierarchy, no restraint either.

### Tell-set B — "AI-chrome" (too MUCH — decoration a shipped product would never add)

This is the more *insidious* set, because every element here passes a presence check ("has an accent! ✓
has a divider! ✓") — it only fails the **subtraction** question: *"what did I ADD that a real shipped
reference (Toss, a real sports app) didn't?"* Real products are astonishingly chrome-free; if removing
an element costs no information, it was slop. Hunt and delete:

- **Decorative left/side edge stripe or colored bar** on a card — pure "AI card" chrome, means nothing.
- **Accent fill behind a static, non-interactive label** (a colored pill behind a value like "코트 3").
  It makes a label masquerade as a button, and it usually breaks the one-accent rule — *accent belongs
  to the primary action + LIVE/positive status only, never to a label background.*
- **Decorative dashed/dotted dividers**, or any divider justified by a motif name ("court-line",
  "ticket perforation") instead of earned. A plain hairline between real sections is fine; a dashed
  flourish is decoration.
- **A status pill that restates** an adjacent eyebrow/heading ("곧 시작" pill above a "다음 경기 · 오늘"
  eyebrow). Replace vague status with one *concrete* fact (a live countdown "10분 후 시작") in accent
  **text**, not a pill. (This is the PC13 redundant-badge root.)
- **Fake placeholder media** — repeated identical thumbnails, flat gray "map" boxes, generic gradient
  squares, mono avatars. If you can't show real media, **remove the slot** and use a clean text/icon
  row (shipped apps do exactly this); never fake it.

The fix for tell-set B is **subtraction**, not "more effects." After subtracting, guard against
overcorrecting into tell-set A (a chrome-stripped card that's now a generic flat row): distinctiveness
must then come from **clarity, hierarchy, and meaning** (the glance hierarchy, a live countdown, the
brand motif/color), never from decoration. Restraint *rescues* a signature; it must not erase it.

## Keep copy simple — author nothing beyond the spec

Craft is about the *visual* layer; it is **not** license to embellish the words. When a mock needs
copy, use the spec/COPY strings **verbatim and minimal** — one clean headline, one short subtitle.
Do **not** invent extra sentences, reasons, or longer labels (e.g. expanding a status headline into
two lines, padding a label from "결제 금액" into "결제 시도 금액", or adding an explanatory clause the
spec never wrote). Invented copy reads as noise and is the fastest way to make a screen feel *more*
generated, not less. If the spec gives a string, render exactly that; if it doesn't, write the
shortest plain-language label that fits and stop. Respect any `lengthLimits` the copy system sets.

## The core rule: match the craft toolkit to the aesthetic REGISTER

Every surface carries an emotional register. There are **two craft toolkits**, and they are not
interchangeable — using one on the wrong register actively cheapens the result.

### Precision-craft → clean / trust / minimal register
*(payments, balances, transactions, forms, settings, productivity, enterprise, anything where the job is confidence)*

Earns quality through **restraint and exactness**:
- exact spacing rhythm on one consistent scale; generous but disciplined whitespace;
- **ledger-style tabular numerals**, tight tracking on hero numbers, strong type-weight contrast;
- **tight, crisp shadows** + a 1px top light-edge on raised surfaces — *no soft bloom*;
- thin concentric keylines / hairline dividers; one consistent radius family; color precision; one rationed accent.
- **Never** film grain or a large glow here — on near-white they read as *dirty* and *cheap*.

### Texture-craft → dark / editorial / energetic register
*(competitive sport, music, events, lifestyle, social, anything where the job is energy)*

Earns quality through **atmosphere and boldness**:
- a near-black or rich canvas + **one electric accent**;
- **oversized display numerals**, big scale contrast, display-weight faces;
- edge-to-edge photography / imagery;
- a **faint film grain** (soft-light blend, low opacity) to break the too-perfect sheen;
- a **contained**, state- or brand-colored **glow** acting as a light source (kept tight — never blooming across the whole screen / into the status bar);
- vivid color-coded status; characterful data-viz (rings, bars, sparklines with personality).

**THE RULE — but cohesion first.** The two toolkits describe *treatments* (tight shadow vs glow,
restraint vs grain), and you should never put grain on a clean trust screen or flat restraint on an
energy screen. **But the canvas — light vs dark — is the *least* transferable layer across screens**
(color/canvas is the first thing that stops reading as "the same product"; see
[[foundation-extract-layout-not-just-color]]). Switching the canvas per surface is what makes one app
look like two. So:

- **Default to ONE register/canvas for the whole product** — usually the one the trust/transaction
  screens need (light), since those are the hardest to make feel safe. Carry "energy" on the
  expressive screens through **composition, not darkness**: the signature motif, oversized numerals,
  data-viz with personality, a vivid accent, illustration, motion. *Energy is not the light↔dark axis.*
- **Cross registers only deliberately, and only with shared DNA.** What makes screens feel like one
  product is the **shared DNA — accent hue, type scale, radius family, icon family, the signature
  motif, spacing rhythm, depth language — not a uniform canvas.** If you do go dark on a surface, bind
  it to the light world with all of that shared DNA.
- **Prefer a contained "dark moment" over a dark screen.** A single dark/gradient hero *card* (e.g. a
  scoreboard-style stats block) on an otherwise light screen gives the drama without stranding a lone
  dark *screen* that reads as a different app. The card coheres with the product's floating-card depth
  language; a full dark screen among light ones does not.

Record the **one** product register and where (if anywhere) a contained dark moment is sanctioned —
as a deliberate, DNA-bound decision, not a per-screen canvas flip. (**Direction step:** into
`concept.md`'s *Cohesion decision / Canvas call*. **Foundation step:** into `design-language.md`.)

> **Process note (learned the hard way):** validate a craft direction in an HTML mock and get it
> blessed **before** encoding its *specific recipe* into this skill. Embed proven *principles* here;
> hold *recipes* until the user has signed off — otherwise the skill accumulates contradictory advice
> from mid-exploration guesses.

## Universal anti-flat moves (apply in either register)

- **Depth via elevation** — float surfaces with a real shadow on a *tinted* ground; never white-on-white.
- **Data as hero** — the single most important number is oversized; its label is small and muted.
- **Status as vivid color** — color + icon + text (tri-encoded), not a gray pill.
- **One focal point per screen** — the 2nd/3rd elements visibly recede.
- **Consistent families** — one radius scale, one shadow family, one icon family across the product.

## Source references on craft, not slop

- Prefer **real shipped apps**. Apple's iTunes Search API returns direct `screenshotUrls` with **no
  browser and no login**: `https://itunes.apple.com/search?term=<app>&entity=software&country=us&limit=1`
  — the mzstatic thumbnail size token in the URL is resizable; `curl` and view. One loop pulls a whole
  reference set in seconds.
- Avoid Dribbble "popular/mobile" — now mostly idealized *concept* shots (many AI-generated, none
  shipped). Mobbin / Screenlane / Refero are higher signal (Mobbin is login-walled).
- **Match the reference's register to the surface you are designing** (don't anchor a trust screen on a dark-editorial shot).

## Transfer a reference's *intent*, not its surface

A great reference's strongest moves are **meaningful, not decorative** — and copying the *look*
without the *meaning* is just the prettier face of AI-slop. Before borrowing any element, name **what
it expresses** and **why it works for that product**, then re-encode that intent for *your* screen's
own story.

Worked example: a live-match screen's split-color ambient glow puts **each team's color on its own
side** to express *confrontation* — two rivals clashing in an arena. A personal-stats screen has no
two teams, so copying that two-color glow literally expresses **nothing** (the classic trap: a pretty
gradient that means nothing). The honest transfer is to find *that* screen's own internal duality —
wins vs losses, this-period vs last, you vs the field — and let the glow encode **that**, proportioned
to the real data (e.g. a warm "win" glow that dominates the frame because the win-rate is high).

**Rule:** every deliberate visual element must answer *"what does this mean here?"* If the only answer
is "it looked good on the reference," cut it or re-encode it. This applies to glows, color splits,
motifs, motion, and illustration alike.

## Validate craft cheaply *before* committing to Figma

Depth, type weight, shadow tightness, and color are far faster to tune in a **throwaway HTML mock**
(all three states side by side at device width) than in a live Figma build. Iterate the look in HTML,
get a read, **then** port the *locked* treatment into Figma with real component instances + bound
tokens. This also surfaces which moves are native to Figma (gradients, inner+drop effects, tabular
numerals) vs. which need an asset (e.g. grain = a tiling noise image fill, not a native filter).

## How the direction consumes this

In `concept.md`, for **each register / surface group** state: (1) its register, (2) the matched craft
toolkit, (3) the concrete elevation / hero-numeral / status / light treatments — this is the
*craft toolkit per register* section of the concept. Step 3 (foundation) turns these into a token +
signature layer; Step 4 (spec) carries them as per-screen decisions; Step 5 (build) executes them;
the craft half of the L3 gate (D6) checks them. Tokens make the screen *correct*; this is what makes
it *crafted*. The cohesion call above is the linchpin — record it in `concept.md` per
`register-cohesion-model.md`.
