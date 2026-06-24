---
name: figma-product-build
description: Build high-fidelity Figma screens from approved DESIGN.md and COPY.md. Use for final PRD-to-product rendering with component-first, token-bound Figma output.
---

# /figma-product-build — spec → high-fidelity screens, three-layer gated

## Mental model

Build the approved spec into real Figma screens, then gate the result adversarially. Execute the signed
direction; do not reopen PRD, art-direction, or system decisions.

Operate in sequence:

1. **Build** component-first, token-bound, auto-layout screens from `DESIGN.md` and verbatim `COPY.md`.
2. **Polish** hierarchy, rhythm, states, and sibling consistency so the screens read as one product.
3. **Critique** with L1.5 self-review before L2/L3. A "done" that cannot survive self-review does not
   reach verifiers.

Completeness comes from `DESIGN.md` and `COPY.md`. Craft comes from signed-off `concept.md`,
`foundation/`, and this skill's references. New MCP mechanics belong in `figma-mcp-express`; new
workflow/gate rules belong here.

Read `references/spec-build-review.md` for the full per-screen protocol; this file is the shape.

## Backend
Use the installed **figma-mcp-express** MCP server and skill as the default backend. Verify the live MCP
namespace in each session before calling tools; it is plugin/runtime dependent and should not be hardcoded
to `figma-mcp-express-dev`. Use the `-dev` server only when the user is explicitly developing the local
MCP server source. In the `core` profile all WRITES go through `batch`.

Each builder reads the relevant local references progressively, plus `concept.md`, `foundation/`, and
the `figma-mcp-express` skill for MCP mechanics.

## Pre-flight (orchestrator, cheap)

Load the `figma-mcp-express` skill first — it owns the MCP mechanics this section relies on (bounded
reads, channel handling, library-import gotchas). Don't re-derive them here.

Read `references/build-preflight.md`; it owns file-shape detection, accent binding, palette-map
harvest, required pages, visual-research pack loading, and brief-assembly checks.

Minimum gates before any builder:

1. Resolve the live channel from `fileKey`; stop if the file is not connected.
2. Record whether the file is `library-local` or `subscriber`.
3. Build or reuse `<sot>/_build-cache/palette-map.json`.
4. Prove one accent-bearing component end to end.
5. Create/reuse `Components`, `Assets`, `References`, and build pages.
6. Read `DESIGN.md`, `COPY.md`, and relevant visual-research packs.
7. Verify each builder brief is resourced and COPY-diffed.

## Rollout

Read `references/canon-fanout.md`. Canon screens are built with the user first; do not delegate them.
No fan-out until canon sign-off is recorded in `governance/JUDGMENT.md`, `do-not-flag` entries are
minted, shared chrome is componentized, and `state.json` records the checkpoint.

Only remaining screens fan out to `figma-builder` agents, each briefed with the canon's verified
patterns, relevant sibling screenshots, staged assets, and reference pages.

## Cross-screen visual consistency

Build against already-approved siblings, not just the spec. Every fan-out brief includes canon
screenshots, nearest sibling screenshots, relevant reference nodes, and locked component masters. L3
fails spec-complete screens that drift from the canon's visual language. Details live in
`references/canon-fanout.md`.

## Per-screen loop

Run each remaining screen through L1 builder, L1.5 resume-to-self-reflect, L2 mechanical pre-gate,
and L3 two-verifier gate. Read `references/per-screen-loop.md` before dispatching builders or
verifiers; it owns the exact loop, subagent contracts, and gate artifacts.

The self-eval ritual gates **every** "done" claim — first build and every fix round — so the L3
verifiers run on an already-self-verified screen and stay bar-raisers, not the safety net. L2 checks
for the `l1.5-r<n>.md` artifact, not the builder's claim.

## The craft-autonomy rule (the build-time half of the boundary)

The spec gives layout intent and real copy. It deliberately does **not** dictate every UI/UX detail.
When the spec/PRD is silent on a craft detail — a state's exact layout, a component variant, spacing
within the token scale, a micro-interaction, an empty/error-state treatment — the builder **designs it
well** from `foundation/` + this skill's craft rules. PRD/spec silence on craft is a mandate to make a
clean, considered choice, **never** an excuse to skip the element or stub it.

Contrast with functional gaps: those don't exist here, because Step 1 resolved them. If the builder
ever feels it must invent a *product* decision (a behavior, a data rule, a screen that should exist but
doesn't) — that's a Step-1 escape, not a craft call. **Stop and escalate** to the orchestrator rather
than inventing it; the answer is "this should have been clarified," not "guess."

## Correction channel (advanced-model builder ↔ less-advanced verifiers)

Builder: advanced model / Opus tier. Verifiers: less advanced model / Sonnet tier. Objective L2 facts
are settled by tool re-read. Judgment disputes require `rebuttal-r<n>.md` with a cited
`JUDGMENT.md`, spec, or `concept.md` ground; otherwise comply. New disputes go to the orchestrator or
user, not into silent do-not-flag entries.

## Dispatch

Reuse the existing agents (same as `/figma-redesign`):
- **Builder** — Codex agent `figma_builder` (advanced model / Opus tier), background, spawned ONCE per screen and named
  `product-builder-<screenId>`; reused via a follow-up message for self-eval and fix rounds.
- **Verifiers (L3 gate, two in parallel, fresh every round, background):**
  - Codex agent `figma_structural_verifier` (less advanced model / Sonnet tier) → D1–D5 vs spec + the scriptable scans.
  - Codex agent `figma_reviewer` (less advanced model / Sonnet tier) → D6 craft + §1G/§1H meaning + platform-appropriateness.
  Dispatch both in one message. Findings flow through files: each verifier writes
  `<sot>/_build-cache/<screenId>/review-r<round>-<structural|craft>.md` and returns only
  `{ verdict, findingsPath, criticalCount, highCount }`. The orchestrator AND-merges verdicts and sends
  failing `findingsPath`s to the same builder.
- **Visual researcher** — Codex agent `visual_researcher` (less advanced model / Sonnet tier), spawned only when the builder
  returns `referenceRequests` / `assetRequests`, or when the orchestrator pre-fetches a richer
  reference pack before a build. It writes files + JSON only; it never mutates Figma.

In each prompt, point the agent at `references/spec-build-review.md` and pass the spec as the
completeness reference (D1 is adapted to "vs spec" there). Full prompt contracts are in that reference
file.

**Distinct presence identity.** Each concurrently-dispatched agent gets a **distinct assigned `origin`**
from the MCP presence roster in its brief — handing them all the same origin collapses them into one
Figma presence identity (no per-agent follow/attribution). The orchestrator keeps its own assigned
origin; each child gets a unique one.

**Mistake retrospective.** Every dispatched agent ends with concrete missteps: failed tool calls,
gotchas, dead ends, and ambiguities. Append them to `<sot>/_build-cache/retrospective.md`; generalize
recurring items into the owning skill after the run.

## Visual research escalation

Read `references/visual-research-escalation.md` when a screen needs external UI references, logos,
icons, photos, avatars, Lottie assets, or a common-pattern reference before dispatch. Keep the
orchestrator cache-first, validate builder requests with
`figma-visual-researcher/scripts/validate-visual-request.py`, and resume the same builder with the
validated pack.

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
- **SUCCESS** — every screen reaches `verdict:"PASS"` (both less-advanced verifiers AND-merged). Hand back to the orchestrator to apply
  memory proposals + `consolidate`.
- **FAILURE** — abort a screen after 3 build→review rounds without PASS, or two consecutive rounds with
  no net reduction in findings, or a recurring plugin/watchdog death. Write a short retrospective
  (which screen, recurring findings, root cause: spec gap vs builder gap vs infra) and stop the run.

## References
| File | Role |
|---|---|
| `references/spec-build-review.md` | Per-screen protocol: build brief from spec, L1 self-eval checklist, L2 mechanical checks, L3 adapted-D1 reviewer prompt, async/R5, recovery |
| `references/build-preflight.md` | File-shape detection, accent binding, palette map, required pages, visual-research inputs, and brief resource checks |
| `references/canon-fanout.md` | Canon co-design, user sign-off, do-not-flag handoff, fan-out briefing, and cross-screen consistency |
| `references/visual-research-escalation.md` | Conditional visual-reference and asset escalation: common-pattern gate, cost discipline, request schema, validation, and result curation |
