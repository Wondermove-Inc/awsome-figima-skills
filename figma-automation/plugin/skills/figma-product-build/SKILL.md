---
name: figma-product-build
description: >-
  Step 5 (final) of /figma-product — build the high-fidelity Figma screens from the spec, gated like
  /figma-redesign: L1 builder self-eval → L2 mechanical pre-gate → L3 two parallel Sonnet verifiers
  (structural + craft, AND-merged). Completeness reference = the SPEC (DESIGN.md layout intent + COPY.md
  strings) plus the frozen direction/concept.md (the L3 craft bar). Reuses the figma-builder (Opus) +
  the two verifier agents; component-first, bound tokens, real copy — zero placeholder text, zero raw
  hex. Orchestrated by /figma-product but independently invocable. Use whenever you need to build
  screens in Figma from a DESIGN.md + COPY.md spec, or render an approved spec to high-fidelity canvas.
---

# /figma-product-build — spec → high-fidelity screens, three-layer gated

## Mental model — the hat you wear here

> **You are the UI engineer + the critic.** Not the researcher (Step 1), not the art director (Step 2),
> not the systems engineer (Step 3), not the product designer who wrote the spec (Step 4). Your job is
> to *make it real and make it ship-worthy* — execute the direction at full craft, then turn on yourself
> and refuse to ship anything a senior designer wouldn't.

Operate in **three modes, in sequence — don't collapse them:**

1. **BUILD** (executional): render every screen from library instances — component-first, bound tokens,
   real copy, dynamic auto-layout. You are *executing* the spec's per-screen Craft moves / Creative mode /
   Signature usage / Motion (which the spec carried down from `concept.md`); you are not re-choosing the
   direction. Where the spec is silent on a craft detail, design it well from the foundation — silence is
   a mandate to make a clean choice, never to skip or stub.
2. **DESLOP / POLISH** (corrective): hunt the recurring AI-slop tells (hero-metric cards, fake-distribute
   gaps, redundant badges, placeholder slots, drifting siblings) and fix the rhythm, hierarchy, and
   consistency so the screens read as ONE product.
3. **CRITIQUE** (adversarial): attack your own output before the gate does. **Squint test** (judge by
   visual weight, not by reading the words), **a11y/contrast + touch-target** pass, and a verbatim spec/COPY
   diff. A "done" that can't survive the L1.5 challenge never reaches the reviewer. The enemy here is
   *trusting your own first "done"* — builders reliably skim their own work.

> **SCOPE (skill ownership).** This skill owns **WORKFLOW / GATE / ORCHESTRATION**: the 5-step pipeline (this is Step 5, the final build), the L1 → L1.5 → L2 → L3 gate, dispatch discipline (lean briefs, plain agents, R5, slots-full), layout planning (`scripts/compute-layout.py`), the empowered-reviewer protocol, and platform propagation. A new **process/gate** rule belongs here. New **design-craft** rules (no-clip, BUTTON CANON, spacing, status colors) → `figma-design-patterns`. New **MCP tool-mechanics** (batch ops, ingestion, gotchas) → `figma-mcp-express`. Per-project keys + a condensed operational digest → that project's `_build-cache/kit-keys.md`. See memory `figma-skill-ecosystem-map`. Layered duplication across these is BY DESIGN — don't collapse it.

Build each screen in the confirmed list from the spec, and gate it the same way `/figma-redesign`
gates a redesign — except the **completeness reference is the spec, not an original frame**. There's
no screen to diff against; the `DESIGN.md` per-screen layout intent + the `COPY.md` strings ARE the
ground truth for "is this screen complete and correct?".

**The reference has two layers — completeness AND craft:**
- **Completeness** = the SPEC: `DESIGN.md` per-screen layout intent (every region/component/state) +
  `COPY.md` strings (verbatim). "Is everything that should be here, here, with the right words?"
- **Craft bar** = the frozen `<sot>/direction/concept.md` (Step 2's signed-off contract). The screen
  must read as *this* product, not generic. The builder executes the spec's per-screen art-direction
  fields — **Craft moves / Creative mode / Signature usage / Motion** — which Step 4 carried down from
  concept.md's **Craft toolkit per register** + **Creative-mode map**. The L3 reviewer (Sonnet) judges the
  result against concept.md's exact sections: **Signature DNA**, **Meaning-encoding philosophy**, and
  **"What this is NOT"** (the anti-pattern list). A spec-complete screen that misses the Signature DNA or
  trips a "What this is NOT" item is a craft FAIL even when every region and string is present. Bind to
  those exact section headings — they are the frozen Direction contract (see
  `figma-product-direction/references/concept-template.md`); never invent your own field names.

Read `references/spec-build-review.md` for the full per-screen protocol; this file is the shape.

## Backend
`figma-go` (`mcp__figma-mcp-express-dev__*`, discrete tools — but verify the live namespace per session;
in the `core` profile all WRITES go through `batch`).

**Every builder loads the frontend-design skill stack before building** — these are how it designs with
real craft instead of just placing components. The orchestrator names them in the brief and the builder
invokes each via the `Skill` tool at setup:
- **`figma-design-patterns`** — the shared build/craft vocabulary (auto-layout, component-first, states,
  handoff) that the builder, self-eval, AND reviewer all judge against. Mandatory.
- **`frontend-design`** — production-grade interface design quality (visual hierarchy, distinctive,
  considered layouts). Raises the screen above component-placement.
- **`rad-spacing`** — hierarchical spacing via the Gestalt proximity principle, using the file's library
  spacing variables (outer containers get proportionally more space than inner elements). This is how the
  spacing rhythm stays intentional and consistent.
- plus `figma-mcp-express` for the MCP mechanics.

A builder that skips these produces mechanically-correct but flat screens — load them, don't wing it.

## Pre-flight (orchestrator, cheap)

Load the `figma-mcp-express` skill first — it owns the MCP mechanics this section relies on (bounded
reads, channel handling, library-import gotchas). Don't re-derive them here.

1. **Resolve the build file by `fileKey`, not by a cached `channel`.** `list_channels` → find the entry
   whose `fileKey` is the build target; use that `channel`. Channel ids are reassigned on every plugin
   reconnect / MCP-server restart (node ids stay stable) — so re-resolve by `fileKey` at each op group,
   and on `"channel not connected"` just `list_channels` again. Not connected at all → STOP: open the
   file in Figma Desktop and run the MCP plugin. Capture `fileKey` (durable) in `state.json`.

2. **Detect the library SOURCE — local vs subscribed.** The build file is one of two shapes, and they
   bind differently:
   - **Library-local** — the file *is* (a copy of) the design-system file; components + variables are
     local. `get_variable_defs` returns the collections. Instance + bind directly.
   - **Subscriber** — a *separate* file with the design system **enabled as a library**. Here
     `get_variable_defs` returns **empty** (it's local-only) even though every token is available.
     Confirm with `list_library_variable_collections` (subscribed collections + keys); read variable
     keys with `get_library_variables`; bring tokens/components in with `import_variable_by_key` /
     `import_component_by_key`. **Never read an empty `get_variable_defs` as "no design system."**

   Record which shape it is in `state.json` — it determines the binding model below.

3. **Brand / accent binding model (the customization decision).** The product usually re-skins ONE
   accent (a brand color the foundation customized) over the library's neutral system. How you apply it
   depends on step 2:
   - **Library-local** → re-point the library's primary token to the brand value once; every component
     instance inherits it. Cleanest.
   - **Subscriber** → the library's primary token is a **subscribed variable and is read-only in the
     consuming file** — you cannot re-value it here, and the MCP has no set-variable-value op anyway.
     Instead: create **one local accent token** (e.g. a `accent/primary` COLOR variable in a local
     collection) holding the brand value, and **override only the accent surfaces** (primary CTA fill,
     "live"/status accent, focus ring, active-tab indicator) by binding their `fillColor` to it.
     **Imported component instances keep their internal `base/*`/neutral/spacing/radius/type bindings
     for free** — so you touch *only* the accent, nothing else. (Free-plan collections are 1-mode; for
     multi-mode theming use a name-prefix workaround, e.g. `light/…` / `dark/…`.)

4. **Catalog + key harvest → ONE cached, reusable, WIDE `palette-map.json`.** The builder's slowest,
   most-repeated work is discovering library component/variable keys. Harvest them **once**, cache to a
   **file**, and pass that file to every builder so no builder ever re-discovers.
   - **Reuse first.** If `<sot>/_build-cache/palette-map.json` already exists and the library hasn't
     changed, **reuse it** — do not re-harvest. The cache is durable across sessions, not a per-run scratch.
   - **Prefer REST over the live plugin.** With a `FIGMA_TOKEN` (read it from the project `.env` — see the
     `figma-mcp-express` skill), harvest via the Figma REST API or `fetch_library_catalog`:
     `GET /v1/files/<libraryFileKey>/component_sets` + `/components` + `/styles` return **every published
     component-set key, component key, and style key in one shot** — no plugin load, no 186-variant page
     spill, no timeout. This is the clean path and is what bogs builders when skipped.
   - **Fallback (no token).** `get_local_components(pageId)` per component page (heavy pages **spill to a
     file — that IS success; grep the spill for `key`**); `get_node` does NOT return a published `key`.
   - **Make it WIDE, not a premature pick.** Record the **full relevant inventory** — every component-set
     that could plausibly serve each role, with its key and its variant axes — NOT a single chosen variant
     per role. The builder picks the variant at build time against the spec + reference screens; the
     orchestrator narrowing to one option up front is exactly the "GAP 조기 선언 / wrong-component" failure
     mode. Give options; let the builder choose and adapt.
   - **Contents.** local accent token id(s) + the variable keys for the token spine (base/* neutrals,
     spacing, radius — for raw structural frames / assembled organisms) + the component-set keys grouped
     by role (with alternates) + the icon keys (the kit's Lucide `Icon / <Name>` set) + text-style keys +
     the canonical device width. Pre-import the hot palette ONCE if helpful (the single import thread
     hangs under concurrent `import_*`).

5. **Prove the pipeline on ONE component BEFORE any screen.** Import one accent-bearing component (e.g.
   the primary Button) into the build file, instance it, bind the accent token onto its fill, and
   `save_screenshots`. Confirm: instance lands as a real INSTANCE, neutrals render correct, accent shows
   the brand color. This catches a broken import path or a wrong binding model in ~1 minute instead of
   across 14 screens. Record the verified recipe in `<sot>/_build-cache/` for the builders to reuse.

6. **Pages — build a real design system, not copy-pasted frames.** Create/reuse four pages in the
   build file:
   - `"🧩 Components"` — the **local component library**. The recurring units this product needs but the
     external library doesn't provide (cards, list rows, status badges, chips, metric blocks, the nav/tab
     shell, the app header, the primary CTA, etc. — whatever *this* product repeats) live here as real
     Figma **components**, with **variants** where they vary (e.g. a card's size/density variants; a
     status badge's one-variant-per-state; a chip's active/default). **Screens are assembled from
     INSTANCES of these + external library components — never raw-rebuilt or copy-pasted look-alikes.**
     **Keep this page ORGANIZED and TIDY**: every registered master lives IN this section, laid out in a
     clean non-overlapping grid, grouped by kind, semantically named. Registering = move the master into
     the section + position it cleanly — never leave a master loose on a screen, orphaned, or scattered on
     the canvas. Builders read this page to discover-and-reuse, so a messy library breaks reuse decisions
     and lets dialects creep in. (See `figma-design-patterns` rule 15.)
   - `"📦 Assets"` — **every non-kit visual asset, staged ONCE and reused** — photos, maps,
     illustrations, AND **brand logos / wordmarks** (e.g. payment-provider marks, partner logos) AND
     **non-kit icons** (icons the kit's Lucide set doesn't cover, or ones you had to source as SVG→PNG).
     Stage them here as named image nodes / small components (named by slug, from `_build-cache/assets/`)
     and reuse by **clone/instance** — builders must NOT re-source or re-`import_image` the same mark per
     screen (a recurring waste: builders each fetched Visa/Mastercard/KakaoPay/DUPR/bank marks
     independently). If a builder sources a new logo/icon mid-build, it **registers it here** so the next
     screen reuses it.
   - `"🔖 References"` — **external, real-shipped-app** anchor screenshots, on-canvas to eyeball the
     build against. Pull these **generously and EARLY** (Step-2 grounding + foundation): not only the
     hero/brand look, but a reference for every **common pattern** the product will render — receipt /
     price-breakdown, empty & error states, list rows, forms, settings, confirmation — because builders
     under-polish a familiar pattern when they have no reference for it (user feedback). **Never put our
     own HTML look-&-feel proofs or build-output renders here** — that contaminates the quality bar;
     our renders live in `_build-cache/`, not here. Refs = what *real products* look like.
     **Every fetched reference is ALWAYS staged INTO this Figma section** (imported as named image nodes),
     not left only as local files — builders eyeball them on-canvas beside their work and the orchestrator
     points each builder at the relevant ref node ids. (visual-researcher saves the local files; the
     orchestrator imports them here — payload cap ~2MB per batch, so import in chunks.) **The analysis
     travels WITH the image.** visual-researcher returns per-candidate text (provenance + "what's
     transferable / what to borrow") in its pack JSON — stage each ref with that note as an **adjacent
     on-canvas caption** (so the builder sees image + "borrow the label-left/amount-right rows, hairline
     before total" together, not a bare image), AND pass the per-ref borrow-note in the builder brief. A
     reference image without its analysis is half a reference.
   - `"🎨 <Product> — Build"` — the screens themselves. New frames go here.

   **Discovery rule:** you find what repeats BY building the canon. So during the canon co-design, the
   moment a unit clearly recurs, **promote it to a component on `🧩 Components` immediately and instance
   it** (even within the canon — the canon's three identical cards must be one component + three
   instances, not three frames). After the canon locks, every recurring unit is a registered component;
   the fan-out only instances. For a NEW unit later: **search local components first → then the external
   library (`fetch_library_catalog`, Lucide/kit) → only then build fresh, and register it if it'll
   repeat.** Don't over-componentize one-offs (componentize units that recur ≥2–3×).

7. **Read the spec.** Load `DESIGN.md` (tokens + `## Screens`) and `COPY.md` (the `screens` string map).
   These are passed to each builder as the build contract + completeness reference.

8. **Load visual research packs.** Read `state.json.visualResearch`, `<sot>/design/visual-needs.json`,
   any packs under `<sot>/_build-cache/visual-research/`, and
   `<sot>/_build-cache/assets/asset-manifest.json` if present. Validate packs with
   `figma-visual-researcher/scripts/validate-visual-pack.py` before passing them to builders. Every
   builder brief gets a compact `visualResearch` object containing only the relevant references/assets
   plus pack paths; do not make builders rediscover or browse.

9. **Brief-assembly check.** Before dispatching any builder, verify each brief is correctly
   resourced: reconcile `state.json` vs reality (`get_pages` / `get_node`); confirm surface treatment
   comes from the screen's REGISTER (trust=white/no-aurora, energy=offwhite/aurora); verify
   pre-imported ids landed; confirm SoT artifact path (right slug); char-diff COPY per region.
   Full verifiable checklist: `references/spec-build-review.md` §Pre-flight.

## Rollout — CO-DESIGN the canon screen(s) WITH the user, THEN fan out agents

Do **not** launch all screens at once, even when channels are free. The **representative / canon
screen(s)** come first — and the orchestrator **co-designs them directly with the user, live in
Figma**, iterating on real craft (layout, glass/depth, the bottom bar, alignment, spacing) the way a
lead designer would at the user's shoulder. **Do not delegate the canon to an agent.** The canon is
where every systemic decision is settled (accent binding, the shared shell, the effect palette, a
layout convention the user likes, copy-tone) — settling it *with* the user, by hand, is far cheaper
than discovering a replicated miss across N agent-built screens. The canon is the **production
aesthetic lock + the real hands-on sign-off** — the Step-2 HTML was only a cheap *concept* feel-check;
the actual product look is decided here, on real Figma screens, with the user.

**The bar is professional, intentionally-designed, MODERN — and it fails in BOTH directions:**
- **Too weak** — flat, AI just-assembling stock blocks, no depth/effects where the UX wants them.
- **Too strong** — advanced features (glass, blur, depth, motion) piled on for show, decoration that
  doesn't serve the screen.

SUCCESS = Figma's advanced capabilities used **purposefully — in the right places, in the right amount, fit
to this screen's app/web UI-UX PURPOSE** (e.g. glass on floating chrome where content scrolls under it;
a solid CTA, not a glass one; depth on a card that should lift; restraint where the data must stay
legible). The judge is *purpose*, not impressiveness. What "modern/professional" *means* is whatever
**this project's direction chose** (NOT a fixed style — liquid-glass, editorial-minimal, brutalist,
soft-depth, etc.; the direction picks one per audience/category). Execute *that* at real, calibrated
depth: authored composition (not stock assembly), real assets in real slots, considered
effects/color/emphasis, correct alignment + hierarchy. Match a shipped real-app caliber — not an AI demo.

Only the **remaining** screens fan out to `figma-builder` agents (Opus build → Sonnet L3 review),
each briefed with the canon's verified patterns + the staged Figma asset/reference pages.

1. **Pick the representative screen(s)** — the ones that exercise the most shared structure: the
   primary nav/tab shell, the densest component mix, the energy *and* trust registers, the accent
   surfaces. (They seed the patterns the rest reuse. Often 1 canon per register zone, not just one.)
2. **Co-design it with the user** — build it for real in Figma at full craft, iterating live on the
   user's feedback until *they* are happy. (Use the live MCP tools directly; this is hand work, not an
   agent dispatch.) Run it through the gate (L1.5 self-eval → L2 → L3 Sonnet verifiers) for hygiene.
3. **Lock it with the user** — it is the visual canon every later screen matches.
4. **Fold in the fixes** on that same screen, then **record the learnings** — shared patterns, the
   verified component/variant choices, accent-binding recipe, layout conventions, copy-tone
   corrections — to `<sot>/_build-cache/` and via `figma-playbook learn` so every later builder inherits
   them. Update `state.json` strategy/notes.
   > **RECORD THE SIGN-OFF before fan-out — a canon held only in the session is invisible downstream.**
   > The user hand-signs the canon, so the human IS the gate (higher than the Sonnet verifiers) — but that
   > approval and its locked decisions must be written to `governance/JUDGMENT.md` (a `user-signed canon`
   > entry: the locked radius, chrome positions / z-order, card rhythm, register/surface treatment, type
   > and number system, effect palette) AND minted as `do-not-flag` entries, BEFORE any screen fans out.
   > Otherwise: later builders/verifiers can't see it was approved, the canon's DNA can't be inherited,
   > reviewers re-flag signed-off choices, and a later hand-edit has no baseline to diff against. **No
   > fan-out until the canon sign-off is recorded in JUDGMENT.md.** (This is the gap that left
   > `tournament-list` with zero gate/sign-off artifacts on disk.)
5. **Then fan out** the remaining screens (serial per channel, R5), each builder briefed with the
   screen-1 learnings. **Before fanning out:** the orchestrator **pre-creates all shared chrome**
   (AppHeader, BottomTabBar, CTA dock) on the `🧩 Components` page as real components so builders
   instance from the same master — never rely on the first fan-out builder to create shared chrome
   (race condition = N-dialect look-alikes).

Record this checkpoint in `state.json` (`4-build.strategy`) so a resumed run knows whether screen 1 has
been proven-and-reviewed yet.

## Cross-screen visual consistency (build against the siblings, not just the spec)

The screens must read as **ONE product, not N dialects.** The spec guarantees the same tokens and
component families, but spacing rhythm, header treatment, card composition, empty/loading patterns, and
type usage are craft choices that drift screen-to-screen unless anchored to what's already on the canvas.
So every builder grounds itself in the **already-built sibling screens**, not only the spec:

> **Mandatory grounding before ANY build — never build blind.** A fan-out builder must start with its
> eyes on the real thing, not just the spec text. Before constructing, it must have:
> 1. **Eyes on the aesthetic** — the **canon screenshot(s)** + the nearest already-built sibling(s),
>    actually viewed (image in context), to match depth/effects, spacing rhythm, header/tab treatment,
>    color/accent usage — not inferred from prose.
> 2. **The craft guides** — the relevant skills (`figma-design-patterns`, `frontend-design`, `rad-spacing`)
>    + this product's concept/effect-palette bar.
> 3. **The references** — the external anchor screenshots on the `🔖 References` page.
>
> **Preferred: the orchestrator pre-digests and hands each builder a ready-to-build, PER-SCREEN brief.**
> Don't make each builder independently search the canvas, hunt for the right refs, and re-derive the
> patterns every time — that's wasted tokens, drift, and inconsistency. The orchestrator does the
> reading/curation and, **for each screen, selects the material relevant to THAT screen** (not one
> global set bolted onto everyone): the external anchor ref(s) that match this screen's pattern/register,
> the nearest already-built siblings, and the canon. The brief is then an explicit instruction:
> *"look at these (canon screenshot `<path>` + the built `<sibling>` screen for consistency; external
> ref A for this pattern; these guide do/don'ts + the effect recipe), match our existing built screens'
> visual language, and build screen X with this content/spec."*
>
> Two reference layers, both per-screen:
> 1. **Our own already-built screens** (canon + the nearest built siblings) — the builder MUST look at
>    these and design to match them, for one-product visual consistency. Whether as **screenshots in the
>    brief or by reading the live Figma nodes** — eyes on our real built design, not inferred from prose.
> 2. **External anchor refs** — only the ones relevant to *this* screen's register/pattern (a payment
>    screen gets the payment anchors, not the energy hero ones).
>
> Keep it lean — *relevant* material, pre-chewed, not the whole library. *Fallback (builder self-grounds):*
> only when the digest would blow the brief (many large images) does the orchestrator pass explicit
> pointers and have the builder `save_screenshots`/read them itself. Either way the builder has *seen our
> canon + the right refs and knows the rules* before the first node — a spec-text-only builder drifts.

- **The proving screen is the visual canon.** Once it passes L3, its screenshots + structure are the
  reference every later screen matches — container padding, card internal rhythm, header height, the
  status-badge treatment, the number-first stat pattern, the type scale in use.
- **Look before building.** Before constructing (and again during self-eval), each builder
  `save_screenshots` the relevant built siblings and **probes their structure** (`get_node` /
  `scan_text_nodes` on the shared organisms) to copy the established rhythm rather than re-inventing it.
- **Reuse shared organisms as the SAME instance, not a look-alike.** The bottom tab bar, app header,
  and any repeated row/card built once on the canon screen are **instanced** on every later screen (or
  the registered file-local component is re-instanced) — never redrawn from scratch. A re-built
  look-alike that drifts 2px is the failure this rule exists to prevent.
- **Pass the pictures.** Give every builder the frame-ids + screenshot paths of the built siblings (at
  minimum the canon screen) so it has concrete images to match, exactly like the foundation/anchor refs.
- **The reviewer enforces it.** L3 checks cross-screen consistency: a screen that diverges from the
  established sibling language (different padding scale, a differently-composed card, a re-drawn tab bar)
  is a craft FAIL even when it satisfies the spec in isolation.

## Per-screen loop (the three layers)

```
For each screen (async across channels — see Concurrency):
  L1  BUILDER (figma-builder, Opus) — spawn ONCE per screen, NAMED, reused across rounds
        assemble build brief from DESIGN.md screen intent + COPY.md strings → build component-first
        → run self-eval ritual vs the SPEC + concept.md craft bar (completeness floor + craft +
            binding + no-placeholder + L1.5 squint/a11y-contrast/touch-target + motion-handoff)
        → loop on own findings (a follow-up message) until self-eval is clean
  L2  MECHANICAL PRE-GATE (orchestrator) — requires `l1.5-r<n>.md` first (gate); then objective
        tool re-reads: layoutMode via scan_nodes_by_types (NONE = FAIL), no opacity:0, touch ≥44,
        string-coverage vs COPY, boundVariables/no raw hex, component-first (raw FRAME for a kit
        kind = FAIL). Writes `l2-r<n>.md`. L3 will not run without it. Fail → back to L1.
  L3  TWO VERIFIERS in PARALLEL (background, fresh each round) — THE GATE
        • figma-structural-verifier (Sonnet) → D1 completeness vs SPEC; D2 keys; D3 tokens; D4
            auto-layout; D5 content = COPY.md strings verbatim; + scans  → structuralVerdict
        • figma-reviewer (Sonnet)              → D6 craft (PC1–PC13 incl. hierarchy gate) vs the
            concept.md craft bar (Signature DNA + Meaning-encoding + "What this is NOT");
            §1G/§1H meaning; platform-appropriateness                    → craftVerdict
        Each verifier WRITES its full findings to a FILE and returns ONLY a compact handle
            { verdict, findingsPath, criticalCount, highCount } — NOT the findings text.
        AND-merge on the VERDICTS only (the orchestrator never reads the findings text):
            PASS = structuralVerdict ∧ craftVerdict → screen done.
        FAIL → message the SAME builder the two findingsPaths VERBATIM + a fix prompt
            ("read both files, fix every CRITICAL/HIGH, then re-run L1") → it READS the files
            itself, fixes, AND re-runs the L1 self-eval ritual → two fresh verifiers.
```

The self-eval ritual gates **every** "done" claim — first build and every fix round — so the L3
verifiers run on an already-self-verified screen and stay bar-raisers, not the safety net.

**L1.5 is a RESUME-to-self-reflect step, never a self-asserted checkbox.** When a builder reports "done",
do NOT accept its inline "self-eval passed" — builders reliably skim their own work and report a green
checklist they didn't actually re-verify. The orchestrator **resumes the same builder (by agentId) with
an explicit adversarial "are you sure?" challenge** that forces it to *re-look, not re-assert*: fresh
`save_screenshots` + READ the image; squint test (judge pixels/visual weight, not memory); verbatim
COPY.md diff per string; **component-first audit (every atom an instance, no raw look-alike of a kit/local
component)**; touch-target ≥44 re-measure; contrast; transparency-bug check (no `opacity:0` faking);
safe-area. The builder must return a per-item PASS/FIXED list + the corrected screenshot — fixing what it
finds — and only THEN does the screen proceed to L2/L3. This catches the misses (raw-rebuilt CTAs, sub-44
tap targets, copy drift) before the gate spends a round on them. Do this for **every** screen, every
builder, every wave — it is the cheapest quality step in the pipeline.

**Artifact (the harness).** The builder saves this resume output to
`<sot>/_build-cache/<screenId>/l1.5-r<n>.md` (per-item PASS/FIXED list + post-mutation screenshot
path). **L2 will not start without this file** — the orchestrator checks for the artifact, not the
claim. Gate artifacts per round under `<sot>/_build-cache/<screenId>/`: `l1.5-r<n>.md` (gates L2) ·
`l2-r<n>.md` (gates L3) · `review-r<n>-{structural,craft}.md` · `rebuttal-r<n>.md` + `do-not-flag.md`.
See `references/spec-build-review.md` §Artifacts for formats.

## The craft-autonomy rule (the build-time half of the boundary)

The spec gives layout intent and real copy. It deliberately does **not** dictate every UI/UX detail.
When the spec/PRD is silent on a craft detail — a state's exact layout, a component variant, spacing
within the token scale, a micro-interaction, an empty/error-state treatment — the builder **designs it
well** from `foundation/` + `figma-design-patterns`. PRD/spec silence on craft is a mandate to make a
clean, considered choice, **never** an excuse to skip the element or stub it.

Contrast with functional gaps: those don't exist here, because Step 1 resolved them. If the builder
ever feels it must invent a *product* decision (a behavior, a data rule, a screen that should exist but
doesn't) — that's a Step-1 escape, not a craft call. **Stop and escalate** to the orchestrator rather
than inventing it; the answer is "this should have been clarified," not "guess."

## Correction channel (Opus builder ↔ Sonnet verifiers)

Builder→Opus, verifiers→Sonnet. A structured correction channel is therefore warranted — but the
builder can only win by citing evidence, never by seniority.

**Objective findings** (facts verifiable by L2 tool re-read: layoutMode:NONE, raw hex, sub-44 target)
are **not disputable** — settled by re-running the tool, not by argument.

**Judgment/taste/canon findings** the builder believes are wrong: fix what it agrees with; for the
rest, write a compact `rebuttal-r<n>.md` `{findingId, ground (JUDGMENT.md line / spec quote /
concept.md section / known limitation), evidence}`. No citation = comply.

**Adjudication (orchestrator):** auto-uphold only vs a pre-existing signed-off JUDGMENT entry; a new
dispute is verified against the cited source or escalated to the user. No minting new do-not-flags
by builder+orchestrator alone. Escalation does not burn the 3-round abort budget.

**Convergence ordering:** FAIL → fix + rebuttal → adjudicate → update `do-not-flag.md` → then spawn
fresh verifiers **with `doNotFlagPath` in the dispatch prompt**. Without the list = infinite re-flag.

## Dispatch

Reuse the existing agents (same as `/figma-redesign`):
- **Builder** — `agent: figma-builder` (Opus), background, spawned ONCE per screen and named
  `product-builder-<screenId>`; reused via a follow-up message for self-eval and fix rounds.
- **Verifiers (L3 gate, two in parallel, fresh every round, background):**
  - `agent: figma-structural-verifier` (Sonnet) → D1–D5 vs spec + the scriptable scans.
  - `agent: figma-reviewer` (Sonnet) → D6 craft + §1G/§1H meaning + platform-appropriateness.
  Dispatch BOTH in one message. **Findings flow through FILES, not the orchestrator's context** (token
  discipline): each verifier writes its findings to
  `<sot>/_build-cache/<screenId>/review-r<round>-<structural|craft>.md` and returns only
  `{ verdict, findingsPath, criticalCount, highCount }`. The orchestrator AND-merges on the VERDICTS
  alone (`PASS = structuralVerdict ∧ craftVerdict`) — it does NOT read the findings text. On FAIL it
  passes the two `findingsPath`s VERBATIM + a fix prompt to the builder in one fix round; the builder
  reads both files itself. This keeps the (long-lived, expensive) orchestrator context free of the full
  review prose — only the builder, which must act on it, ever loads it.
- **Visual researcher** — `agent: visual-researcher` (Sonnet), spawned only when the builder
  returns `referenceRequests` / `assetRequests`, or when the orchestrator pre-fetches a richer
  reference pack before a build. It writes files + JSON only; it never mutates Figma.

In each prompt, point the agent at `references/spec-build-review.md` and pass the spec as the
completeness reference (D1 is adapted to "vs spec" there). Full prompt contracts are in that reference
file.

**Distinct presence identity.** Each concurrently-dispatched agent gets a **distinct `origin`** from the
roster (grace/theo/zoe/taewon/emma/alex/rick/wolfgang) in its brief — handing them all the same origin
collapses them into one Figma presence identity (no per-agent follow/attribution). The orchestrator keeps
its own (e.g. `sunho`); each child gets a unique one. (See memory `agent-presence-poc`.)

**Mistake retrospective (every agent, on completion).** Every dispatched agent — builders, verifiers,
refactor/cleanup agents — ends its final report with an honest **retrospective of its own
mistakes/missteps**: failed tool calls + cause (wrong param name, stale id, wrong enum), gotchas hit
(auto-layout sizing, z-order/pin, dropped instances, import/channel issues), dead ends/rework, and any
brief/spec **ambiguity it had to guess on**. NOT a success summary — the misses are the value. The
orchestrator appends each to `<sot>/_build-cache/retrospective.md` (never ingests it into screen briefs)
and, between waves / at run end, **generalizes recurring entries into skill improvements via
`skill-creator`**, routed to the owning skill (MCP-mechanics → `figma-mcp-express`; design-craft →
`figma-design-patterns`; workflow/gate → this skill). This is how the pipeline compounds — each wave's
misses harden the next.

## Visual research escalation

**Common-pattern screen gate (H5).** A screen whose layout is a well-known pattern — receipt/price-
summary, empty state, list row, confirmation, payment — is **not dispatched** until a reference exists:
a cache hit in `design-system/_build-cache/ref-library/<pattern>/` or a fresh researcher run, AND the
curated ref is staged on `🔖 References` with its analysis as an adjacent caption. A ref without
analysis is half a ref. The gate blocks dispatch like L2 blocks L3 — not advisory. Front-load: enumerate
all common patterns at spec/foundation time, fetch in one batched run, reuse across the build.

**Cost discipline (visual-researcher is token-heavy — image tokens + browsing dominate).** Before any
dispatch, in this order:
1. **Cache-first / reuse.** Common patterns (receipt, empty/error state, list row, form, payment-summary,
   confirmation) recur across screens AND projects. Keep a persistent **reference library**
   (`design-system/_build-cache/ref-library/<pattern>/` + the cross-project KB) with each ref's image +
   analysis; **check it and REUSE before researching** — only fetch what's genuinely missing or stale.
   A common pattern should be fetched ONCE, ever.
2. **Front-load in ONE batched pass, not per-screen ad-hoc.** At foundation/spec, enumerate every common
   pattern the product will render and fetch them in a single visual-researcher run (multiple
   requestIds) — far cheaper than N separate spin-ups discovered mid-build, and it avoids late re-runs.
3. **Bound the request:** ~3 candidates (not 6), 2–3 named exemplar screens (not a wide sweep), and tell
   the researcher to **save ONLY the curated candidates** (not every search hit — a prior run dumped ~40
   raw grabs) and to **triage on thumbnails, full-res only the picks**.
4. **Get it right once** — a sharp, on-target request (screen-type anchor + exemplars + negative set,
   above) avoids the off-target re-run that doubles the cost.
5. **Access-walled target → ask the USER for a screenshot; do NOT keep re-researching.** Many on-target
   screens (mobile checkout/payment, logged-in flows, Medium/login-gated case studies) are unreachable
   by public WebFetch — the researcher will burn tokens and return little. The moment a target is
   confirmed paywalled/login-gated, STOP and ask the user to drop a screenshot (they can open the
   logged-in app) — near-zero cost and perfectly on-target. Re-running the researcher against a wall is
   the worst token spend.
6. **Verify provenance.** A researcher run once returned fabricated/unverifiable `sourceYear`s — require
   each kept ref to have a verifiable source + date (the stricter re-run correctly rejected the fakes).

Builders do not browse. If a screen needs a better UI reference, logo, icon, photo, avatar, or Lottie
that is not already in the brief, the builder returns:

```json
{
  "blocked": true,
  "reason": "visual_research_required",
  "referenceRequests": [],
  "assetRequests": []
}
```

The orchestrator dispatches `visual-researcher`, validates the returned pack, adds the local paths to the
builder brief, and resumes the SAME builder. If the runtime supports nested subagent calls, the builder
may call `visual-researcher` directly, but the returned JSON contract is identical.

Before dispatching, validate the builder's request with
`figma-visual-researcher/scripts/validate-visual-request.py`. If it fails, return it to the same builder
to add missing size/type/source/style/detail fields. Do not browse from the orchestrator with a vague
request.

Every request item must include a detailed natural-language `brief`. The brief should say what the
builder wants in design language, not just a keyword: usage context, target screen, aesthetic,
dimensionality (`flat`, `3D`, `4D/motion-like`, `isometric`, etc.), quality bar, source constraints,
and what to avoid. It must also include structured prompt fields so the request is actionable:
`targetScreen`, `usage`, `placement`, `targetSize`, `sourcePreference`, `candidateCount`,
`styleKeywords`, `desiredQualities`, `mustHave`, and `avoid`. Reference requests also need
`referenceKind`, `screens`, `minSourceYear: 2024`, and `trendFocus`; asset requests also need `type`,
`assetKind`, `query`, and `preferredFormat` or `outputFormats`. The orchestrator should reject vague request items before
dispatching `visual-researcher`, ideally by running:

`<figma-visual-researcher-skill-dir>` means the installed `figma-visual-researcher` skill directory
shown in Codex's available-skills list.

```bash
python3 <figma-visual-researcher-skill-dir>/scripts/validate-visual-request.py <request.json>
```

`visual-researcher` returns multiple candidates per `requestId`, not a single final answer. Pass all
candidates back to the same builder. The builder chooses the candidate that best fits the actual screen
layout and records the chosen candidate id in its ledger/self-review.

**Anchor the request on the SCREEN-TYPE, not a sub-mechanic — and curate the results.** A request that
leads with a *detail* ("show the discount as a won amount") pulls screens that merely contain that detail
(product-listing discount badges, promo banners, balance dashboards, post-pay confirmation receipts)
instead of the surface you actually want (the mobile **checkout/payment screen's price-summary region**).
So: (1) state the **surface/screen-type** as the target ("the 결제/checkout screen where line items sum to
a total above the Pay button"); (2) name **exemplar real screens** (the actual 결제 screen of 무신사/배민/
쿠팡/Stripe/Apple Pay), not just pattern keywords; (3) give an **explicit negative set** (what NOT to pull —
listings, promo banners, dashboards, confirmation-only); (4) the detail (discount-in-won) is a *nice-to-have*,
not the search anchor. Then the orchestrator **curates the returned candidates for on-target relevance and
stages only the on-target ones** — don't import all candidates blindly (a 2026-06-19 run staged off-target
discount/dashboard screens because the request over-emphasized the discount mechanic and results weren't filtered).

## Concurrency (R5 — the load-bearing constraint)
Async = **partition screens across channels, ONE heavy-write builder per channel at a time**.
Concurrent builders on *separate* channels pipeline safely; two heavy-write builders on one channel do
not — a single hung import head-of-line-blocks the channel and a real disconnect takes down every agent
on it (the documented 12-screen failure). A reviewer (read-only) may run on a channel while no builder
writes it. If only one channel is available, build **serially**. On `importThreadHung:true`, stop
launching builders, ask the user to restart the plugin, and drain recorded tails in one single-writer
pass (Hung-import recovery, same as `/figma-redesign`).

## Re-gate after any post-PASS edit (a PASS certifies bytes, not a node id forever)

A `verdict:"PASS"` certifies the exact pixels the verifiers reviewed — not the frame id in perpetuity.
Any frame edited AFTER it reached PASS — manual polish, prototype/interaction wiring, a hand-fix, a copy
tweak, a shared-chrome change — is a **new submission** and re-enters L1.5 → L2 → L3 before it counts as
done again. Hand-edits that skip the gate are exactly how a passed screen silently regresses (a tab bar
nudged behind content, a chrome instance that drifts). If a late edit touches **shared chrome** (header,
tab bar, CTA dock) it propagates to every screen that instances it — re-screenshot those siblings too.
Don't treat "it already passed" as a permanent certificate.

## Stop conditions
- **SUCCESS** — every screen reaches `verdict:"PASS"` (both Sonnet verifiers AND-merged). Hand back to the orchestrator to apply
  memory proposals + `consolidate`.
- **FAILURE** — abort a screen after 3 build→review rounds without PASS, or two consecutive rounds with
  no net reduction in findings, or a recurring plugin/watchdog death. Write a short retrospective
  (which screen, recurring findings, root cause: spec gap vs builder gap vs infra) and stop the run.

## References
| File | Role |
|---|---|
| `references/spec-build-review.md` | Per-screen protocol: build brief from spec, L1 self-eval checklist, L2 mechanical checks, L3 adapted-D1 reviewer prompt, async/R5, recovery |
