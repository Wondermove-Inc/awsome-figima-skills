# state.json — orchestrator state machine + resume

`/figma-product` is resumable: re-invoking it never redoes finished work. The single source of
truth for "where are we" is `<sot>/governance/state.json`. One deterministic writer: the
orchestrator. Step skills read it for context but the orchestrator owns the step transitions.

## Schema

```json
{
  "slug": "toss-onboarding",
  "pipeline": "figma-product",
  "prdPath": "docs/prd/onboarding.md",
  "library": { "key": "<libraryFileKey>", "slug": "<library-slug>", "url": "https://figma.com/design/..." },
  "currentStep": 4,
  "steps": {
    "1-prd":        { "status": "done",        "artifacts": ["design/prd-analysis.json", "design/prebuild-product-map.md"], "confirmedAt": "<ts>" },
    "2-direction":  { "status": "done",        "artifacts": ["direction/concept.md", "direction/look-and-feel/"], "gate": "A", "signedOffAt": "<ts>" },
    "3-foundation": { "status": "done",        "artifact": "foundation/foundation.json", "confirmedAt": "<ts>" },
    "4-spec":       { "status": "in_progress", "artifacts": ["design/DESIGN.md", "design/COPY.md", "design/build-readiness.md"], "schemaCheck": null },
    "5-build":      { "status": "pending",     "screens": [] }
  },
  "visualResearch": {
    "needs": "design/visual-needs.json",
    "referencePacks": ["_build-cache/visual-research/direction-reference-pack.json"],
    "assetPacks": ["_build-cache/visual-research/prefetch-asset-pack.json"],
    "assetManifest": "_build-cache/assets/asset-manifest.json",
    "pendingRequests": [],
    "resolvedRequests": []
  },
  "screens": [
    { "id": "login",     "name": "로그인",     "buildState": "pending", "frameId": null, "verdict": null, "channel": null },
    { "id": "dashboard", "name": "대시보드",   "buildState": "pending", "frameId": null, "verdict": null, "channel": null }
  ],
  "createdAt": "<ts>",
  "updatedAt": "<ts>"
}
```

- `status` ∈ `pending | in_progress | done | blocked`. A `blocked` step carries a `blockedReason`.
- `screens[]` is populated at the end of Step 1 (confirmed list) and carries per-screen build state
  through Step 5. `buildState` ∈ `pending | building | self-eval | review | pass | failed`.
- `visualResearch` is append-only except for `pendingRequests`. It is lane state, not a separate
  product step: the PRD hook writes `needs`, the direction hook appends reference packs, the spec hook
  appends prefetch asset packs and the manifest, and the build hook moves builder requests from
  `pendingRequests` to `resolvedRequests` after the returned pack validates.
- Timestamps: the runtime forbids `Date.now()` in some contexts — stamp `updatedAt` from the shell
  (`date -u +%Y-%m-%dT%H:%M:%SZ`) when you write, or omit and let the user's environment fill it.

## Step exit conditions (gates)

A step's `status` may flip to `done` **only** when its exit condition holds. The orchestrator checks
these before advancing `currentStep`:

| Step | Exit condition |
|---|---|
| `1-prd` | `prd-analysis.json` validates against `prd-analysis.schema.json`; `openQuestions` has zero items with `severity:"NEEDS_INPUT"` unresolved; **every screen carries a `purpose` + initial `register`**; the user has confirmed `screens[]` + scope/register; `prebuild-product-map.md` includes the north-star task, journey / IA map, screen-state matrix, content/data inventory, and non-goals. |
| `2-direction` | `concept.md` written per the contract template; the HTML look-&-feel rendered ≥1 energy + ≥1 trust screen; the adversarial direction check passed (distinctive / purposeful / cohesive / modern-not-trend-chasing / buildable); **the user signed off on the rendered look-&-feel (Gate A)**; winning concept written to the cross-project KB. |
| `3-foundation` | `foundation.json` validates against `foundation.schema.json`; every major design-language/motion/voice decision traces to a `concept.md` section or library fact; **the signature layer is defined** (motif / semantic-motion built+bound, or a flagged gap); library gaps flagged; `research-sources.md` backs the feasibility claims; pattern-transfer + component-preference rules present. |
| `4-spec` | `DESIGN.md` passes `npx @google/design.md lint --format json` (no errors); `COPY.md` passes `copy-md.schema.json`; the `COPY.md` `screens` map covers every screen id; **each screen carries its concept.md art-direction fields (creative mode + craft moves)**; all `libraryGaps` in DESIGN.md are marked resolved; visible concrete media needs are either prefetched into the asset manifest or explicitly deferred to the build hook's active fetch; `build-readiness.md` includes a per-screen asset plan, responsive/device behavior, builder acceptance checklist, and risk list. |
| `5-build` | every entry in `screens[]` has `buildState:"pass"` (advanced-model `verdict:"PASS"`). |

## Resume algorithm

1. Read `state.json`. If absent, create it with all steps `pending`, `currentStep:1`.
2. Find the first step whose `status` ≠ `done`. Set `currentStep` to it.
3. If that step is `in_progress`, re-enter its skill — the step skills are themselves idempotent
   (they read their own partial artifact and continue), so a half-written `foundation/` or a spec
   that failed lint is picked up, not restarted from zero.
4. Never re-run a `done` step unless the user explicitly asks (e.g. "redo the direction" → set
   `2-direction` back to `pending`, which also invalidates `3-foundation`, `4-spec`, and `5-build`
   downstream, because they derive from it). Downstream invalidation is the orchestrator's call — warn
   the user that changing an upstream artifact stales everything after it.

## Project-slug resolution

- Prefer `--project <slug>` if given.
- Else derive from the PRD title → kebab-case (`"Toss Onboarding Flow"` → `toss-onboarding`).
- `ls design-system/` — if a slug already exists for this product/file, reuse it (don't fork a
  second project for the same Figma file). Confirm the match by reading its `project.json` `fileKey`.
- A new slug means this run creates `design-system/<slug>/` and its `project.json`.
