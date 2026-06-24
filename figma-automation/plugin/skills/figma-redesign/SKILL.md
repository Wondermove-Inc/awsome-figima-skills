---
name: figma-redesign
description: Redesign or migrate one existing Figma screen into a target design-system library. Use for re-skin, rebuild, port, or swap-library requests that write to Figma.
---

# /figma-redesign — On-the-Fly Fresh Redesign of One Screen

Redesign **one** screen into a target library by **building fresh from component instances**, with
**live** library discovery (no report, no relibrary, no cached catalog). The original is the
**visual reference + content source**; the target library is **how it should look/size/space**.
FUNCTION is preserved (every feature survives); FORM is reinterpreted with the new library's
components, variants, tokens, and auto-layout.

> **The primary redesign skill.** It builds fresh from target-library instances, discovering the
> library on the fly — best for component-heavy enterprise UI (tables, forms, dialogs, cards), which
> is most screens. For a region with dense idiosyncratic custom layout the library has no pattern for,
> the builder may clone-and-transform THAT region in place — an internal tactic, not a separate skill.
> Discovery, build, and review happen in one inventory-driven loop so the original screen, target
> library, and finished canvas stay connected through the same run.

---

## The Three-Layer Pipeline

A screen can be **complete** (every element present) yet read as **crude** (a stretched filter bar, a
neutral-grey trash icon) and be **unmaintainable** (60 copy-pasted rows no designer can edit in one
place). These are three independent failure modes, so the pipeline guards each with its own mechanism —
don't conflate them:

- **Completeness** — guaranteed by an exhaustive original-inventory, not a checklist. Every completeness
  miss this project has seen was an element never enumerated (a clone-of-original, a missing leading icon,
  a dropped back-row). So the checks are emergent: "did every inventoried element survive?" — there is no
  separate prose list to maintain.
- **Craft** — guarded by a NAMED enum (Production-Craft **PC1–PC8**), because craft is NOT
  inventory-emergent: a structurally-complete screen can still be crude. Builder, self-eval, AND the
  advanced-model gate judge craft in the SAME vocabulary — this skill's Production-Craft enum + local
  reference rules — so a craft miss has three chances to be caught and the gate stays a bar-raiser, not
  the safety net.
- **Maintainability** — guarded by component-reuse: N≥3 identical rows
  should be ONE component (library if one exists, else `local/<Name>`) instanced, never raw repeats. This
  is **suspect-then-investigate**, not an auto-verdict — raw repeated siblings *flag*, then you probe the
  library (variants included): use a library instance, or make a local component; it's a violation only if
  it's neither. A blunt "N≥3 raw = fail" false-positives on legitimate in-progress states, and raw
  uniformity is the defect, not a "consistency" strength.

**Why the skill keeps improving — the append-only learning loop.** Every production-craft miss a user
catches that isn't already covered becomes a new named check: a mechanical one (pushed to the L2 floor)
when it can be scripted, else a judgment line (a new PC row in the gate). So the bar rises every cycle and
the same mistake is never made twice. Where a heuristic sits at a judgment seam ("is this repetition
really a violation?"), make it a suspect-then-investigate flag — a blunt mechanical conclusion on a
judgment call produces false positives.

### L1 — Builder (less advanced model / Sonnet tier)
Build the inventory → build against it → run the mechanical floor on itself → self-review =
**inventory-diff** (every entry present and rendered? any built node NOT in inventory = excess?).
Details: `references/builder-brief.md`, `references/live-discovery.md`, `references/variant-resolution.md`.
Inventory method: `references/original-inventory.md`.

### L2 — Mechanical Pre-Gate (deterministic; green before any advanced-model call)
Completeness checks fall out of the inventory-diff; the scriptable craft members ride along. Checks (a)–(g),
full spec in `references/completeness-floor.md`:
(a) catalog-key — every built INSTANCE key ∈ target catalog, AND its **reverse** (component-first /
    no-escape-hatch): every element whose role maps to a library kind (button, input, select, badge,
    nav-row, icon…) IS an instance, not a raw FRAME+TEXT faking it;
(b) inventory-coverage — every inventory entry has a built counterpart, AND **row-parity** (each row in a
    repeated-row list carries the same control set as its siblings, cross-checked vs the count badge);
(c) no-excess — every built node maps to an inventory entry;
(d) child-fits-parent — no overflow/clip (Σ child extents ≤ frame size);
(e) raw-value — no raw hex / null boundVariables where a token belongs;
(f) no-left-default-variant;
(g) production-craft floor — the scriptable PC members: PC2 boxless-control, PC3 destructive-not-red,
    semantic layer names (no `Frame <number>`).

### L3 — Two-Verifier Gate (runs ONCE on a mechanically-clean screen, both in parallel)
Two fresh READ-ONLY verifiers run concurrently (background): **figma-structural-verifier** (less advanced
model / Sonnet tier) builds
its OWN inventory and runs D1–D5 + the scriptable scans (touch-target / accent / icon / names) — the
independent backstop to the builder's L2 floor; **figma-reviewer** (advanced model / Opus tier) judges D6
craft (**Production-Craft enum PC1–PC13**, incl. the hierarchy gate) + §1G/§1H/§5F/D7
semantics. A CORE-RULE violation is a FAIL even when the build matches the original. The orchestrator
**AND-merges** (`PASS = structuralVerdict ∧ craftVerdict`). Delta-review after a fix verifies the fixed
findings AND re-runs the full L2 floor + a fast full-frame visual scan — never only the fixed node.
Details: `references/review-protocol.md`.

> **Bar-raiser principle:** every builder submission is COMPLETE + HIGH-CONFIDENCE by its OWN evidence
> before the gate. The advanced-model verifier raises the bar beyond "complete + correct" (subtle craft, hierarchy, feature-loss
> semantics). If the gate finds a missing icon, a typo, or a dropped affordance, the builder failed its
> own bar — a builder failure, not the system working. The gate runs ONCE and PASSES a clean submission.

---

## Backend

Use the installed **figma-mcp-express** MCP server and skill as the default backend. Verify the live MCP
namespace in each session before calling tools; it is plugin/runtime dependent and should not be hardcoded
to `figma-mcp-express-dev`. Use the `-dev` server only when the user is explicitly developing the local
MCP server source.

Before any build call, load the `figma-mcp-express` skill for tool mechanics and use this skill's local
Production-Craft references for craft judgment. Do not require extra backend or craft skills that are not
part of the public install contract.

---

## Trigger

```
/figma-redesign <target-library> --frame <frameUrlOrNodeId>
/figma-redesign <target-library> --frame <id1,id2,id3>     # batch: SERIAL, one at a time
```

- `<target-library>`: Figma file URL **or** subscribed library key. Must be published/subscribed so
  `import_component_by_key` resolves at build time.
- `--frame`: original screen frame(s) to redesign (colon node-id, or figma.com URL whose `node-id`
  hyphen form converts to colon). Multiple ids run **serially** (≤3 writer budget — never parallel
  on one channel without the pre-imported palette in place).

---

## Pre-flight (orchestrator, cheap — no heavy reads)

Read `references/orchestration.md`; it owns channel resolution, target-library checks, palette
pre-import, memory loading, concurrency, and report-before-dispatch. The orchestrator does no deep
structural read; L1 owns inventory.

---

## The Per-Screen Loop

Run each screen through Phase 0 orientation, Phase 1 builder, Phase 1.5 self-reflection, and Phase 2
two-verifier gate. Read `references/per-screen-loop.md` before dispatching builders or verifiers; it
owns the exact loop and handoff contract.

> **Self-eval ritual gates EVERY "done" claim — first build, every fix round.** A fix round is a new
> submission; it must clear the same bar. The orchestrator never sends "fix → re-review" directly;
> it sends "fix → re-run the self-eval ritual → return selfReview", then dispatches the fresh reviewer.

**Agent identity:**
- The **builder is reused** within a screen's rounds (spawn once, named `redesign-builder-<screenId>`;
  use a follow-up message for fix rounds — it keeps the ledger, variant rationale, node ids).
- **Both verifiers are fresh every round** (brand-new agents — a less-advanced structural verifier +
  an advanced-model craft verifier;
  independence prevents rubber-stamping). They run in parallel and never persist across rounds.
- Across different screens, each gets its own builder.

Hung-import recovery and stuck-agent watchdog details live in `references/orchestration.md`.

---

## Subagent Dispatch

Dispatch background Codex agents. Spawn one named `figma_builder` per screen and reuse it across fix
rounds. Spawn two fresh read-only verifiers every round in parallel: `figma_structural_verifier` and
`figma_reviewer`. Prompt contracts live in `references/orchestration.md`; detailed builder and reviewer
criteria live in `references/builder-brief.md` and `references/review-protocol.md`.

---

## Cross-Cutting Rules

**TEST-THE-OVERRIDE before declaring library-forced/GAP:** probe an instance with the intended property
change first. A wrong-looking result + passing instance audit is usually YOUR layout/placement bug, not a
library limitation.

**LOOK-ALIKE TRAP:** the original file's own library has same-NAMED components with different keys, so a
clone of the original passes every other check by definition yet is NOT a target-library build. Verify
every built instance key ∈ target catalog. Canonical explanation + rule in `references/live-discovery.md`;
the L2 enforcement is `completeness-floor.md` check (a).

**MEMORY-CACHE discipline:** the orchestrator loads memory indexes via `figma-playbook load` before
dispatching builders. Builders scan the index on demand per element type — load the topic file only
when the hook matches what's being placed. On a memory miss, go live (fetch_library_catalog / get_node /
save_screenshots). Solved patterns already in library memory should never be re-derived from scratch.

---

## Screen-1 Checkpoint

After screen 1 reaches advanced-model PASS, STOP and assess before starting screens 2–3:
- **Did builder self-green (L1+L2) correlate with the advanced-model verdict?** If the builder declared itself
  green and the fresh advanced-model reviewer then found multiple critical D1/§1H/D6 issues, L1 is not doing its
  job — screens 2–3 will just repeat the failure at higher cost. This is a stop-and-reconsider signal
  (write the retrospective on what L1 missed and why).
- R1 (L2) mechanically backstops binding lies. Nothing backstops visual self-review except the
  advanced-model gate — so
  this correlation must be measured on screen 1, not assumed.
- A watchdog/plugin death on screen 1 is a methodology signal to STOP, not to retry.

Only continue to screens 2–3 if screen 1 reached PASS in ≤2 rounds with the self-green↔advanced-model
correlation holding (few/no criticals the builder should have caught itself).

---

## Stop Conditions

- **SUCCESS** — all target screens reach advanced-model `verdict:"PASS"` AND L2 floor green AND ledger green
  → Apply pending memory proposals: for each screen's `memoryProposalsPath`, run
  `Skill('figma-playbook') apply <path>` then delete the scratch file.
  → Run post-session cleanup: `Skill('figma-playbook') consolidate --library <librarySlug> [--project <slug>]`
  → Tidy remaining scratch artifacts; report each `builtFrameId` + ledger path.
  → **Human polish loop (async):** After a human designer corrects the AI screen, run
  `Skill('figma-playbook') reflect --ai-screen <builtFrameId> --human-screen <humanFrameId> --library <slug>`
  to harvest the corrections as confirmed playbook entries. This closes the learning loop.
- **FAILURE** — abort a screen when EITHER:
  (a) **3 build→review rounds** without a PASS, OR
  (b) **two consecutive rounds with no net reduction** in critical/major findings (looping, not
  improving), OR
  (c) a hard plugin/watchdog death recurs.
  On abort, STOP the whole run and write `<sot>/rebuild/RETROSPECTIVE-redesign.md`: which screen(s)
  stalled, the exact recurring findings, the root cause (skill-brief gap vs methodology gap vs infra),
  and the specific change that would fix it. A retrospective is a valid expected outcome.

---

## DONE Bar (per screen — all three at once)

1. Merged `PASS` = `structuralVerdict ∧ craftVerdict` (D1–D5 + scans by the less advanced model /
   Sonnet tier, D6/§1G/§1H/§5F/D7 by the advanced model / Opus tier, vs the original). **This is the
   gate** — the only thing that can say a screen is done.
2. The builder passed the Phase 1.5 evidence-based dry-run and returned a `selfReview` BEFORE the
   review — so both verifiers ran ONCE and PASSed first time. L2 (inventory-coverage,
   no-excess, no visible placeholder/default, no invisible/empty icon, no null `boundVariables`/raw
   hex, no `layoutMode:null` shell) is the builder's own checklist; the gate verifies it independently.
3. Per-element ledger records, for every element: a real library component (not a raw frame) + the
   probed-and-screenshot-compared variant + the deliberation. (Proves live-discovery + probe-to-best
   worked with no cached catalog.)

---

## References

| File | Phase | Role |
|---|---|---|
| `references/original-inventory.md` | L1 + L3 | **Ground truth** — node-walk method, inventory JSON schema, inventory-diff self-review |
| `references/completeness-floor.md` | L2 (a.k.a. R1) | Mechanical pre-gate — checks (a–g) incl. component-first reverse, row-parity, production-craft floor; green before any advanced-model call |
| `references/review-protocol.md` | L3 | Two-verifier gate — ownership map (less advanced model / Sonnet tier D1–D5+scans; advanced model / Opus tier D6/§1G/§1H/§5F/D7), feedback bar, verdict JSONs, delta-review rules |
| `references/orchestration.md` | Orchestrator | Pre-flight, palette import, memory loading, dispatch prompts, concurrency, hung-import recovery |
| `references/builder-brief.md` | L1 | Builder's binding protocol — R-OTF, section loop, ledger forcing function, batch-first |
| `references/variant-resolution.md` | L1 | Deep recipe: map original props → variant axes → shortlist → probe-render → commit → trim |
| `references/live-discovery.md` | L1 | On-demand catalog fetch + bounded variant-axis reads + anti-false-GAP deliberation |
| `design-system/<library-slug>/memory/` | L1 + L3 | Library pattern memory (e.g. `design-system/material-design/memory/`) — load via `figma-playbook load`; progressive (index first, topic files on demand) |

---

## Path Resolution

`<sot>` = `design-system/<slug>/` — discover the slug via `ls design-system/` and read `<slug>/project.json`
to confirm the fileKey. Scratch artifacts (catalog fetch, ledgers, screenshots) live under
`design-system/_build-cache/`. New frames live on the redesign/rebuild page in the working file.
