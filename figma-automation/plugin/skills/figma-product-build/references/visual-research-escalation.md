# Visual Research Escalation

Use this reference when a product-build screen needs a better UI reference, logo, icon, photo,
avatar, Lottie asset, or common-pattern example before dispatch or during a builder fix round.

## Common-Pattern Gate

A screen whose layout is a well-known pattern — receipt/price-summary, empty state, list row,
confirmation, payment — is **not dispatched** until a reference exists:
a cache hit in the `figma-playbook` global reference memory (`ref-<pattern>-...`) or a fresh researcher run, AND the
curated ref is staged on `🔖 References` with its analysis as an adjacent caption. A ref without
analysis is half a ref. The gate blocks dispatch like L2 blocks L3 — not advisory. Front-load:
enumerate all common patterns at spec/foundation time, fetch in one batched run, reuse across the
build.

## Cost Discipline

`visual-researcher` is token-heavy because image tokens and browsing dominate. Before dispatch:

1. **Cache-first / reuse.** Common patterns recur across screens and projects. Keep persistent
   reference entries in the `figma-playbook` global store with each ref's source, local artifact path,
   and transfer analysis. Reuse before researching; only fetch what is genuinely missing or stale.
2. **Front-load in one batched pass.** At foundation/spec, enumerate every common pattern the product
   will render and fetch them in a single visual-researcher run with multiple `requestId`s.
3. **Bound the request.** Ask for about three candidates, two or three named exemplar screens, saved
   curated candidates only, and thumbnail triage before full-resolution picks.
4. **Get it right once.** Use a sharp screen-type anchor, exemplars, and negative set to avoid an
   off-target re-run.
5. **Access-walled target.** Ask the user for a screenshot instead of repeatedly researching a
   login-gated or paywalled screen.
6. **Verify provenance.** Require every kept ref to have a verifiable source and date.

## Builder Block Contract

Builders do not browse. If a screen needs a better reference or asset that is not already in the
brief, the builder returns:

```json
{
  "blocked": true,
  "reason": "visual_research_required",
  "referenceRequests": [],
  "assetRequests": []
}
```

The orchestrator dispatches `visual-researcher`, validates the returned pack, adds the local paths to
the builder brief, and resumes the same builder. If the runtime supports nested subagent calls, the
builder may call `visual-researcher` directly, but the returned JSON contract is identical.

## Request Validation

Before dispatching, validate the builder's request with
`figma-visual-researcher/scripts/validate-visual-request.py`. If it fails, return it to the same
builder to add missing size/type/source/style/detail fields. Do not browse from the orchestrator with
a vague request.

Every request item must include a detailed natural-language `brief`: usage context, target screen,
aesthetic, dimensionality (`flat`, `3D`, `4D/motion-like`, `isometric`, etc.), quality bar, source
constraints, and what to avoid. It must also include structured fields:
`targetScreen`, `usage`, `placement`, `targetSize`, `sourcePreference`, `candidateCount`,
`styleKeywords`, `desiredQualities`, `mustHave`, and `avoid`.

Reference requests also need `referenceKind`, `screens`, `minSourceYear: 2024`, and `trendFocus`.
Asset requests also need `type`, `assetKind`, `query`, and `preferredFormat` or `outputFormats`.

```bash
python3 <figma-visual-researcher-skill-dir>/scripts/validate-visual-request.py <request.json>
```

`<figma-visual-researcher-skill-dir>` means the installed `figma-visual-researcher` skill directory
shown in Codex's available-skills list.

## Result Curation

`visual-researcher` returns multiple candidates per `requestId`, not a single final answer. Pass all
candidates back to the same builder. The builder chooses the candidate that best fits the actual
screen layout and records the chosen candidate id in its ledger/self-review.

Anchor the request on the screen type, not a sub-mechanic. A request that leads with a detail such as
"show the discount as a won amount" pulls screens that merely contain that detail instead of the
checkout/payment surface you actually want. State the surface, name exemplar real screens, give a
negative set, and treat the detail as a nice-to-have. Then curate returned candidates for on-target
relevance and stage only the useful ones.
