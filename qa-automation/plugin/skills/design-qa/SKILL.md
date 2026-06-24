---
name: design-qa
description: Review implementation fidelity between a live app and Figma design. Use for design QA, screen-to-frame mapping, Playwright snapshots, and read-only drift findings.
---

You run an implementation-fidelity review: **is the rendered app faithful to the Figma design?**
You are READ-ONLY — you produce findings and fix candidates; you never edit code or Figma.

This is a **general method bound to a specific project by a manifest.** The skill holds no project
facts. Each run resolves `design-qa/<slug>/` (the manifest: `project.json`, `screen-map.json`,
`conventions.md` — see `references/manifest-schema.md`) and operates over it. The binding to a
project lives in that manifest, never hardcoded here; the method below is the same for every
project. The only deterministic code is `scripts/design_snapshot.py` (structured browser facts +
Layer-1 invariants). Mapping, correspondence, judgment, and localization are disciplined reasoning
over the three legs — **disciplined by the layers and rules below, not improvised.**

Empirical basis for the 3-layer method: `references/spike-findings.md`. The design-qa-reviewer
agent internalizes the full evidence-collection + decision-tree; this skill does not re-derive it.

## Operational rules (non-negotiable — validated empirically)

- **Figma reads via figma-mcp-express** (the default installed MCP server): verify the live namespace
  with tool discovery, then use scoped reads such as metadata/node reads, variable reads, and screenshot
  capture against the mapped frame. Keep reads bounded to the manifest's page/frame node; never pull an
  entire large file when a frame-scoped read is enough.
- **Browser via LOCAL Playwright** (`<design-qa-skill-dir>/scripts/design_snapshot.py`,
  where `<design-qa-skill-dir>` is the installed skill directory shown in Codex's available-skills
  list. The script imports its sibling `dom_snapshot.py`; both ship with this skill). Requires Playwright in the
  active Python env: `pip install playwright && playwright install chromium` (optional `python-dotenv`
  for env-based login). A remote browser extension may control a Chrome on a
  different host that cannot reach the local dev server — confirm the snapshot's `title`/`url` match
  the app under review.
- **Locale alignment is a precondition, not a nicety:** align the app's i18n language to the
  Figma design language before comparing (per `project.json.alignment.locale`). After alignment,
  residual sample-data text differences are still variations — establish correspondence by
  structure (name+position), not raw string match.
- **viewport = the Figma frame width** (from the screen's `reach.viewport`); layout still goes to
  Layer 3.
- **Snapshots are PII — never commit.** They write to the gitignored `.tmp/design-qa/`. The
  manifest under `design-qa/<slug>/` IS tracked (team knowledge) and must never contain a snapshot.

## Phase 0 — Resolve the manifest

1. Determine the slug. `ls design-qa/` for an existing project; match it to the codebase/Figma
   file the user named.
2. **Manifest exists →** load `project.json` + `screen-map.json` + `conventions.md`. Skip to the
   phase the user wants (a full sweep, or one screen). Re-runs **merge**, never overwrite.
3. **No manifest → init.** Collect the binding (ask only what you cannot read from the codebase):
   Figma `fileKey` + seed page node-id (scope to ONE page for a large Figma file); how to run the
   app + port; how locale/role are selected. Write `project.json`, then proceed to Phase 1 to
   build `screen-map.json` + `conventions.md`.

*Exit criteria:* a `project.json` exists for the slug and is loaded.

## Phase 1 — Mapping (agentic; precedes comparison; persists to the manifest)

1. Read the codebase like a developer: enumerate **every screen** and its **reach recipe**
   (router, pages, auth/role gating, locale, modal triggers, mock seeding). Record convention
   homes (token source, component-style idiom, nav/route config, i18n resources) into
   `conventions.md` as you find them.
   **Fan out:** spawn parallel worker subagents (a fast, cheap tier) — one per router file / page
   directory — each covering: route-level screens AND all overlays reachable from that route (modals,
   drawers, dialogs, bottom sheets — find the trigger: button onClick, state flag, route param) AND
   role-gated variants of each screen. Then synthesize the full list and resolve conflicts.
2. Enumerate Figma frames with `get_metadata(fileKey, nodeId)`. The same screen often has a
   distinct frame per role (a role-section variant) — match role too.
3. **Reason out screen↔frame matches** from frame name + role section + `get_design_context`
   text + screen purpose. Confident → record automatically; ambiguous or unmatched → **ask the
   user** before recording.
4. Write `screen-map.json`: each screen's `{ route, figmaNode, figmaFrameName, reach, match }`,
   plus `gaps.figmaOnly` (designed, not built) and `gaps.appOnly` (built, not designed) — the
   gaps are themselves review insight. Seed only validated entries; leave unknowns out.
5. Hard-to-reach screens: read the code to drive them (seed role/locale/mock, click the modal
   path). If a screen truly cannot be rendered, fall back to code↔Figma static comparison and
   flag it `STATIC`. **Never silently skip a screen.**

*Exit criteria:* every reachable screen is in `screen-map.json` with a reach recipe and a
confidence; ambiguous matches were confirmed by the user; gaps recorded.

## Phase 2 — Per-screen comparison (pipeline — screens fan out; stages within a screen are serial)

For each mapped screen (screens proceed in parallel — screen B captures while screen A is reviewed):
1. Capture snapshot:
   `python "<design-qa-skill-dir>/scripts/design_snapshot.py" --manifest design-qa/<slug> --screen <screen>
   --out .tmp/design-qa/<screen>.snap.json --screenshot .tmp/design-qa/<screen>.png`
   Reach (locale/role/auth/viewport) is applied from the manifest automatically.
   (Ad-hoc flags `--viewport/--locale/--set-storage` still work for one-off captures.)
2. **L1 pre-analysis (fast worker tier):** Pass `snap.json["invariants"]` + `snap.json["nodes"]` — no Figma
   reads, no judgment. The worker outputs `preAnalysis`:
   - `layer1Flag`: `"clean"` | list of fired signals (`"truncated[N]"`, `"offscreen[N]"`, `"zeroSize[N]"`)
   - `candidateElements`: filtered nodes keyed by guessed semantic kind
     (`status-badge`, `column-header`, `nav-item`, `form-field`, `action-button`, `image`)
   - `regionSummary`: `{ hasTable, hasBadges, hasNav, hasForm, badgeCount, tableRowCount }`
   This pre-classification is cheap here and makes the reviewer's key-map step a confirmation pass,
   not an exploratory one.
3. Dispatch Codex agent **`design_qa_reviewer`** (less advanced model / Sonnet tier) with coordinates + paths — not pre-fetched blobs:
   - `figmaCoords: { fileKey, nodeId, channel? }` — reviewer reads Figma directly through figma-mcp-express, scoped to its task
   - `snapshotPath: .tmp/design-qa/<screen>.snap.json`
   - `screenshotPath: .tmp/design-qa/<screen>.png`
   - `conventionsPath: design-qa/<slug>/conventions.md`
   - `preAnalysis` from step 2 — reviewer uses `candidateElements` as key-map scaffold
   The reviewer is the only PASS authority; do not self-approve.

*Exit criteria:* each screen has a reviewer verdict with a non-trivial key map; no Layer-1 harm
signal is left unexplained.

## Phase 3 — Gate + report + merge

- Collect each screen's verdict + findings + key map.
- **UNCERTAIN resolution (fan out):** spawn parallel worker subagents (fast tier) — one per `UNCERTAIN`
  finding — each running a targeted grep for the i18n key / route / conditional render cited in
  the finding's `coverageNote`. Each worker resolves to VARIATION (exists, conditionally rendered) or
  escalates to VIOLATION (key/route absent). Collect results and update findings before reporting.
- **Systemic synthesis (optional):** if ≥3 screens FAIL or multiple findings share the same token
  family or component import, run one synthesis pass (strongest available reasoning tier) over all
  FAIL findings to identify the systemic root cause (`file:line`, theme variable family, component
  import gap). Skip if ≤2 FAIL.
- Report: write each reviewer verdict to `.tmp/design-qa/<screen>.review.json`, then generate the
  screen-keyed report:
  `python "<design-qa-skill-dir>/scripts/generate_report.py" --screen-map design-qa/<slug>/screen-map.json --out reports/design_qa_<date>.json .tmp/design-qa/*.review.json`.
  The report contains a coverage matrix (mapped screens + figma-only/app-only/STATIC gaps),
  per-screen PASS/FAIL, and each drift as `{layer, severity, where, figmaValue, renderedValue, why,
  file, fix}`. Do not route design-qa findings through behavioral-QA tooling that expects `tc_id`.
- **Merge back into the manifest:** append newly-mapped screens, mark a recorded gap RESOLVED if
  the user confirms it now defined, add discovered convention homes to `conventions.md`. Never
  clobber the file.

*Exit criteria:* report produced; manifest merged forward (not overwritten).

## Out of scope

Auto-fixing code / opening PRs (review is READ-ONLY — findings + fix candidates only).
Behavioral QA. Naive pixel screenshot diff / whole-tree node diff.
