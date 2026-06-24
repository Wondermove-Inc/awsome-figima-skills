---
name: figma-redesign
description: >-
  Production redesign of ONE Figma screen into a target design-system library — the primary,
  self-contained redesign skill. No upstream report, no relibrary matching, no cached catalog:
  the builder discovers the target library LIVE per element, builds fresh from component
  instances (auto-layout + tokens native), self-reviews on two axes (COMPLETENESS via an
  exhaustive original-inventory + CRAFT via the Production-Craft enum), then passes a single
  adversarial Sonnet gate. WRITES to the Figma canvas. Use whenever the user wants to redesign,
  migrate, re-skin, port, or rebuild a screen with a different/new design-system library — even
  when they say "rebuild", "swap the library", or "make this in <library>" rather than "redesign".
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
> The older report-driven rebuild/relibrary pipeline is archived; this skill supersedes it. It failed
> because the lossy report→build handoff made neither half thorough, which is why this skill folds
> discovery, build, and review into one inventory-driven loop (the three-axis model below).

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
  inventory-emergent: a structurally-complete screen can still be crude. Builder, self-eval, AND the Opus
  gate judge craft in the SAME vocabulary — `figma-design-patterns` CORE RULES + the PC enum — so a craft
  miss has three chances to be caught and the gate stays a bar-raiser, not the safety net.
- **Maintainability** — guarded by component-reuse (figma-design-patterns CORE RULE 6): N≥3 identical rows
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

### L1 — Builder (Sonnet)
Build the inventory → build against it → run the mechanical floor on itself → self-review =
**inventory-diff** (every entry present and rendered? any built node NOT in inventory = excess?).
Details: `references/builder-brief.md`, `references/live-discovery.md`, `references/variant-resolution.md`.
Inventory method: `references/original-inventory.md`.

### L2 — Mechanical Pre-Gate (deterministic; green before any Opus call)
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
Two fresh READ-ONLY verifiers run concurrently (background): **figma-structural-verifier** (Sonnet) builds
its OWN inventory and runs D1–D5 + the scriptable scans (touch-target / accent / icon / names) — the
independent backstop to the builder's L2 floor; **figma-reviewer** (Opus) loads `figma-design-patterns`
and judges D6 craft (**Production-Craft enum PC1–PC13**, incl. the hierarchy gate) + §1G/§1H/§5F/D7
semantics. A CORE-RULE violation is a FAIL even when the build matches the original. The orchestrator
**AND-merges** (`PASS = structuralVerdict ∧ craftVerdict`). Delta-review after a fix verifies the fixed
findings AND re-runs the full L2 floor + a fast full-frame visual scan — never only the fixed node.
Details: `references/review-protocol.md`.

> **Bar-raiser principle:** every builder submission is COMPLETE + HIGH-CONFIDENCE by its OWN evidence
> before the gate. Opus raises the bar beyond "complete + correct" (subtle craft, hierarchy, feature-loss
> semantics). If the gate finds a missing icon, a typo, or a dropped affordance, the builder failed its
> own bar — a builder failure, not the system working. The gate runs ONCE and PASSES a clean submission.

---

## Backend

**figma-go** backend (`mcp__figma-mcp-express-dev__*`, discrete tools). Load `figma-go` +
`figma-design-patterns` before any build call. If `$FIGMA_BACKEND` is inherited from a `/figma` router
session, honor it; standalone, assume `figma-go`.

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

1. **File open + channel.** `list_channels` → confirm the file containing the original frame is
   connected; capture `channel` + `fileKey`. Not connected → STOP: "Open the file in Figma Desktop
   and run the MCP plugin."
2. **Target library reachable.** `fetch_library_catalog(libraryFileKey, scope:"all", outPath:<scratch>)`
   — doubles as the live-discovery fetch (see `references/live-discovery.md`). Unreachable → STOP.
3. **Resolve frame id(s)** to colon format. `get_metadata` (bounded) to confirm each exists, grab
   name + page. `save_screenshots` each original frame as the visual target.
4. **Pick the output page.** Scan pages for an existing redesign/rebuild page; or create
   `"🔄 Redesign — <libraryName>"`. New frames go here; **never touch existing frames.**
5. **Pre-import the shared palette ONCE (A1).** The plugin has a SINGLE import thread shared by every
   agent, and under heavy concurrent load it can hang in a way that does NOT self-clear — so N builders
   each calling `import_*` is the main source of stalls. Pre-empt it: before fanning out, import the
   shared palette once and write `<sot>/rebuild/palette-map.json`:
   - Foundation token ramp (surface/background, border, text, spacing/radius via `get_library_variables`
     + `import_variable_by_key`).
   - Common icon set (close/✕, chevron, search, download, trash, plus/minus, kebab, zoom/nav glyphs via
     `import_component_by_key`).
   Pass `palette-map.json` to every builder. Builders bind/instantiate from it and do NOT re-import what
   it covers — only screen-specific extras. This removes most head-of-line blocking.
6. **Concurrency rule (R5).** Default = serial (safest). Concurrent (≤3 writers) allowed ONLY with the
   pre-imported palette (step 5) in place and each builder on a **disjoint** wrapper. Even then,
   screen-specific imports still serialize on the one thread. If a builder returns `importThreadHung:true`
   → STOP launching builders; ask the user to restart the plugin/MCP; drain the recorded import tails in
   one post-restart single-writer pass (see "Hung-import recovery" below).
7. **Load memory.** `Skill('figma-playbook') load --library <libraryFileKey> [--project <slug>]`
   Returns the library + project + global MEMORY.md indexes (index only, no topic files).
   If library memory is empty or sparse (first use of this library): also call
   `Skill('figma-playbook') learn --library <libraryFileKey>` to bootstrap pattern memory from
   the library's own documentation/example pages. Pass loaded memory index context to each builder.
8. **Report** resolved target frame(s) + output page (+ serial vs concurrent) to the user before
   dispatching.

The orchestrator does **no** deep structural read — that is the builder's job inside L1.

---

## The Per-Screen Loop

```
ORCHESTRATOR (main session)
  └─ Phase 0  orient: screenshot original, resolve ids, catalog fetched live (scratch)
  └─ Phase 1  spawn ONE NAMED BUILDER (Sonnet) — kept alive & REUSED across rounds
        builder: node-walk → inventory.json (FIRST) → build against it → L2 floor
        → inventory-diff self-review → return { builtFrameId, ledgerPath, r1Report, inventoryDiff,
          catalogKeyAudit, bindingProof, selfReview, finalScreenshot, gaps[], escalations[], importThreadHung }
  └─ Phase 1.5  SELF-REFLECTION CHALLENGE — RESUME the SAME builder (a follow-up message)
        "run the verifiers' D1–D6 on yourself, adversarially, prove each with an artifact"
        builder finds a problem → fixes it, re-runs L1/L2 on touched sections, answers again
        builder confirms good  → answers with selfReview evidence → go to review
  └─ Phase 2  spawn TWO FRESH VERIFIERS in PARALLEL (background, one message) → THE GATE
        • figma-structural-verifier (Sonnet) → D1–D5 + scans  → structuralVerdict
        • figma-reviewer (Sonnet)              → D6/§1G/§1H/§5F/D7 → craftVerdict
        AND-merge (wait for BOTH; no short-circuit):
        PASS = structuralVerdict ∧ craftVerdict  → screen done, proceed to next screen
        FAIL → message the COMBINED findings to the SAME builder to fix
                → builder fixes AND RE-RUNS THE FULL PHASE 1.5 SELF-EVAL RITUAL
                → ONLY THEN spawn TWO NEW fresh verifiers
```

> **Self-eval ritual gates EVERY "done" claim — first build, every fix round.** A fix round is a new
> submission; it must clear the same bar. The orchestrator never sends "fix → re-review" directly;
> it sends "fix → re-run the self-eval ritual → return selfReview", then dispatches the fresh reviewer.

**Agent identity:**
- The **builder is reused** within a screen's rounds (spawn once, named `redesign-builder-<screenId>`;
  use a follow-up message for fix rounds — it keeps the ledger, variant rationale, node ids).
- **Both verifiers are fresh every round** (brand-new agents — a Sonnet structural + an Opus craft;
  independence prevents rubber-stamping). They run in parallel and never persist across rounds.
- Across different screens, each gets its own builder.

### Hung-import recovery

A builder may finish its bulk build but return `importThreadHung: true` — the single import thread is
wedged and will not self-clear. Do NOT retry (it will just re-hit the lock):
1. Ask the user to restart the Figma plugin / reconnect MCP. `list_channels` after to confirm.
2. Drain all recorded tails in ONE post-restart single-writer pass — each builder recorded its blocked
   import keys + target node ids in its ledger. Resume builders serially (one at a time, thread now
   free) to apply their recorded binds/swaps; or drain simple deterministic ones inline.
Non-import writes (`clone_node`/`set_fills`/`set_text`/`get_node`) keep working during a hang — a build
can complete structurally while its import tail waits; that is expected, not a failure.

### Stuck-agent watchdog (A3)

A builder can hang silently — grinding on a blocked import — without returning. If a builder has
produced **no new disk artifact** (ledger / progress screenshot) for an extended window, or a fresh
`import_*` returns "thread busy" while no builder should be importing: **probe on-disk artifacts**
(ledger + latest screenshot) to see if the build is actually complete-but-tail-blocked, then stop the agent
the stuck process and recover its tail per "Hung-import recovery" above.

---

## Subagent Dispatch

Dispatch **blank `general-purpose` shells** with a model override — the skill's reference files carry
every rule, so the shell needs no special agent body.

> **ALWAYS dispatch as BACKGROUND agents** (run them in the background). follow-up-message resumes are
> already background. Never spawn a reviewer foreground/blocking.
>
> **Independent steps run concurrently — do not serialize what doesn't conflict:**
> - Reviews are read-only → fan out freely. Both verifiers per screen, and N screens' gates, run at once.
> - Self-review challenges + disjoint-frame fixes run concurrently up to the ≤3 writer budget.
> - Only serialize genuinely conflicting heavy WRITES on the same frame.
> - Per-screen logical order must hold: build → self-review → gate. Different screens never gate
>   each other.

### Builder dispatch (agent: `figma-builder`) — spawn ONCE per screen, NAMED

Required in the initial prompt:

- "Read and FOLLOW EXACTLY:
  `${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-redesign/references/builder-brief.md`,
  `${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-redesign/references/original-inventory.md`,
  `${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-redesign/references/variant-resolution.md`,
  `${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-redesign/references/completeness-floor.md`,
  `${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-redesign/references/live-discovery.md`."
- "Build the **inventory FIRST** (node-walk, before building anything). See `original-inventory.md`."
- "You do the WHOLE job: node-walk → inventory.json → live library MATCHING (discover + deliberate +
  resolve-variant + probe) → fresh DESIGN (auto-layout, component-first, FILL/HUG/FIXED) → L2 floor
  → inventory-diff self-review."
- "USE `figma-design-patterns` as you build — not just load it. Every frame must satisfy its CORE RULES
  and trip ZERO of its QUICK ANTI-PATTERN FLAGS (dynamic auto-layout + resize test, tokens not raw values,
  component-first, semantic layer names — `batch_rename_nodes` away every `Frame <number>`/`Group <number>`
  before finishing, no default/excess parts). A CORE-RULE violation means not-done, regardless of feature
  coverage."
- Inputs: `channel`, original `frameId`, target `libraryFileKey` + scratch catalog path, the
  `palette-map.json` path, output `pageId`, ledger path `<sot>/rebuild/<screenId>-ledger.json`,
  memory index context (from orchestrator's `figma-playbook load`).
- "Return JSON: `{ screenId, builtFrameId, ledgerPath, r1Report, inventoryDiff, catalogKeyAudit,
  bindingProof, selfReview, finalScreenshot, gaps[], escalations[], importThreadHung,
  memoryProposalsPath }` — full field definitions in builder-brief.md STEP 5."
- Concurrency note (C1): "You are the only writer on YOUR wrapper. Other builders are irrelevant to
  you. On a genuine import-thread hang: ONE bounded attempt, no retry-loop, record the tail, set
  `importThreadHung:true`, return. Never `git stash/reset/clean`."

**Phase 1.5 + fix rounds — REUSE via a follow-up message:** for the self-reflection challenge, send the
adversarial dry-run prompt: "run the reviewer's D1–D6 on yourself, adversarially; re-derive features from
the ORIGINAL (not your ledger); diff every text string; render-zoom every icon strip; read back every
binding; run the catalog-key audit for the LOOK-ALIKE TRAP; score craft against `figma-design-patterns`
CORE RULES + the PC1–PC8 enum in `review-protocol.md`; prove each clear with an artifact." The full ritual
is builder-brief.md STEP 4 — the goal is that the fresh reviewer finds nothing the builder could have
caught itself. For a post-review fix, send a lean delta — just the reviewer's findings + "fix these,
re-run L1/L2 + the design-patterns/PC self-check on touched sections, return updated r1Report." Do NOT
re-send the whole brief.

### Verifier dispatch — spawn TWO NEW FRESH agents every round, in PARALLEL (one message, background)

The L3 gate is two independent verifiers running concurrently. Dispatch both in a single message so they
pipeline; both are READ-ONLY, so concurrent reads on one channel are safe. **AND-merge: wait for BOTH
verdicts, never short-circuit** — the builder gets one combined fix-list per round.

**Structural verifier** (`agent: figma-structural-verifier`, Sonnet):
- "You are READ-ONLY. Read and EXECUTE the D1–D5 + scan dimensions of `review-protocol.md` and run
  `completeness-floor.md` checks (a)–(j) INDEPENDENTLY. Build your OWN inventory of the original — do NOT
  trust the builder's ledger."
- Inputs: `channel`, `builtFrameId`, `originalFrameId`, `ledgerPath`, round, prior findings.
- "Output the structural JSON with `structuralVerdict: PASS|FAIL`."

**Craft verifier** (`agent: figma-reviewer`, Opus):
- "You are READ-ONLY. Read and EXECUTE the D6/§1G/§1H/§5F/D7 dimensions of `review-protocol.md`. Judge
  craft, hierarchy, and asset/function meaning from the screenshots; do not re-derive structural facts."
- Inputs: same as above.
- "Output the craft JSON with `craftVerdict: PASS|FAIL`."

**Merge (orchestrator):** `PASS` iff `structuralVerdict == PASS && craftVerdict == PASS`. On any FAIL,
concatenate both verifiers' `findings` and send the combined list to the builder in one fix round.

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

After screen 1 reaches Opus PASS, STOP and assess before starting screens 2–3:
- **Did builder self-green (L1+L2) correlate with the Opus verdict?** If the builder declared itself
  green and the fresh Opus reviewer then found multiple critical D1/§1H/D6 issues, L1 is not doing its
  job — screens 2–3 will just repeat the failure at higher cost. This is a stop-and-reconsider signal
  (write the retrospective on what L1 missed and why).
- R1 (L2) mechanically backstops binding lies. Nothing backstops visual self-review except Opus — so
  this correlation must be measured on screen 1, not assumed.
- A watchdog/plugin death on screen 1 is a methodology signal to STOP, not to retry.

Only continue to screens 2–3 if screen 1 reached PASS in ≤2 rounds with the self-green↔Opus
correlation holding (few/no criticals the builder should have caught itself).

---

## Stop Conditions

- **SUCCESS** — all target screens reach Opus `verdict:"PASS"` AND L2 floor green AND ledger green
  → Apply pending memory proposals: for each screen's `memoryProposalsPath`, run
  `Skill('figma-playbook') apply <path>` then delete the scratch file.
  → Run post-session cleanup: `Skill('figma-playbook') consolidate --library <libraryFileKey> [--project <slug>]`
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

1. Merged `PASS` = `structuralVerdict ∧ craftVerdict` (D1–D5 + scans by Sonnet, D6/§1G/§1H/§5F/D7 by
   Opus, vs the original). **This is the gate** — the only thing that can say a screen is done.
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
| `references/completeness-floor.md` | L2 (a.k.a. R1) | Mechanical pre-gate — checks (a–g) incl. component-first reverse, row-parity, production-craft floor; green before any Opus call |
| `references/review-protocol.md` | L3 | Two-verifier gate — ownership map (Sonnet D1–D5+scans / Opus D6/§1G/§1H/§5F/D7), feedback bar, verdict JSONs, delta-review rules |
| `references/builder-brief.md` | L1 | Builder's binding protocol — R-OTF, section loop, ledger forcing function, batch-first |
| `references/variant-resolution.md` | L1 | Deep recipe: map original props → variant axes → shortlist → probe-render → commit → trim |
| `references/live-discovery.md` | L1 | On-demand catalog fetch + bounded variant-axis reads + anti-false-GAP deliberation |
| `design-system/<library-slug>/memory/` | L1 + L3 | Library pattern memory (e.g. `design-system/hae-dl/memory/`) — load via `figma-playbook load`; progressive (index first, topic files on demand) |

---

## Path Resolution

`<sot>` = `design-system/<slug>/` — discover the slug via `ls design-system/` and read `<slug>/project.json`
to confirm the fileKey. Scratch artifacts (catalog fetch, ledgers, screenshots) live under
`design-system/_build-cache/`. New frames live on the redesign/rebuild page in the working file.
