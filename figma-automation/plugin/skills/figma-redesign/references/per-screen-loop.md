# Per-Screen Redesign Loop

Use this reference when running `/figma-redesign` after pre-flight completes.

## Loop

### Phase 0: Orient

The orchestrator screenshots the original, resolves ids, and fetches the target catalog into scratch
storage. Do not perform deep structural reads in the orchestrator.

### Phase 1: Builder

Spawn one named `figma-builder` on a less advanced model / Sonnet tier and reuse that same builder
across fix rounds.

The builder must:

- Node-walk the original frame and write `inventory.json` first.
- Build against the inventory, not a screenshot-only impression.
- Run the L2 floor.
- Run inventory-diff self-review.
- Return `builtFrameId`, `ledgerPath`, `r1Report`, `inventoryDiff`, `catalogKeyAudit`,
  `bindingProof`, `selfReview`, `finalScreenshot`, `gaps[]`, `escalations[]`, and
  `importThreadHung`.

### Phase 1.5: Self-Reflection Challenge

Resume the same builder with an adversarial self-review prompt:

> Run the verifiers' D1-D6 on yourself, adversarially, and prove each with an artifact.

If the builder finds a problem, it fixes it, re-runs L1/L2 on touched sections, and answers again.
If the builder confirms the screen is good, it answers with self-review evidence and the orchestrator
proceeds to review.

### Phase 2: Two-Verifier Gate

Spawn two fresh background verifiers in parallel:

- `figma-structural-verifier` on a less advanced model / Sonnet tier owns D1-D5 plus scans and returns
  `structuralVerdict`.
- `figma-reviewer` on an advanced model / Opus tier owns D6, section 1G/1H/5F, D7, and returns
  `craftVerdict`.

Wait for both verifiers. Do not short-circuit.

- `PASS`: `structuralVerdict` and `craftVerdict` are both pass; screen is done.
- `FAIL`: send the combined findings to the same builder, require fixes, require the full Phase 1.5
  self-eval ritual again, then spawn two new fresh verifiers.

## Done Claim Rule

The self-eval ritual gates every "done" claim, including the first build and every fix round. The
orchestrator never sends "fix -> re-review" directly; it sends "fix -> re-run the self-eval ritual ->
return selfReview", then dispatches fresh verifiers.
