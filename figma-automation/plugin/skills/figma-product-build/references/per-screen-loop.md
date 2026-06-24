# Per-Screen Build Loop

Use this reference before dispatching builders or verifiers for `/figma-product` Step 5.

## Loop

For each screen, run the loop asynchronously across available channels, subject to the concurrency rules in the parent `SKILL.md`.

### L1 Builder

Dispatch `figma-builder` on an advanced model / Opus tier.

- Spawn once per screen, name the subagent, and reuse it across fix rounds.
- Assemble the build brief from `DESIGN.md` screen intent and `COPY.md` strings.
- Build component-first.
- Run the self-eval ritual against the spec, `concept.md` craft bar, completeness floor, binding requirements, no-placeholder rules, L1.5 squint/a11y/contrast/touch-target checks, and motion handoff.
- Loop on the builder's own findings through a follow-up message until self-eval is clean.

### L1.5 Resume-To-Self-Reflect

Treat L1.5 as a resume-to-self-reflect step, not a self-asserted checkbox.

When the builder reports "done", resume the same builder by `agentId` with an adversarial "are you sure?" challenge. Force it to re-look, not re-assert:

- Run fresh `save_screenshots` and read the image.
- Run a squint test based on pixels and visual weight, not memory.
- Diff every visible string against `COPY.md` verbatim.
- Audit component-first construction: every atom must be an instance; no raw look-alike of a kit or local component.
- Re-measure touch targets at 44px or larger.
- Check contrast, transparency bugs, and safe-area handling.

The builder must return a per-item `PASS`/`FIXED` list plus a corrected screenshot. It fixes what it finds before the screen can proceed.

The builder saves this resume output to `<sot>/_build-cache/<screenId>/l1.5-r<n>.md`.

### L2 Mechanical Pre-Gate

The orchestrator runs L2 only after the `l1.5-r<n>.md` artifact exists.

Objective checks:

- `layoutMode` via `scan_nodes_by_types`; `NONE` is a fail for constructed UI.
- No `opacity: 0` placeholder or transparency workaround.
- Touch targets are at least 44px.
- Visible string coverage matches `COPY.md`.
- Variables are bound and raw hex values are rejected.
- Component-first construction is enforced; raw `FRAME` for a kit component kind is a fail.

Write `<sot>/_build-cache/<screenId>/l2-r<n>.md`. L3 does not run without this artifact. On failure, return to L1.

### L3 Two-Verifier Gate

Dispatch both verifiers in parallel as fresh background subagents for every round.

- `figma-structural-verifier` on a less advanced model / Sonnet tier checks D1 completeness vs spec, D2 keys, D3 tokens, D4 auto-layout, D5 verbatim `COPY.md` content, and structural scans.
- `figma-reviewer` on a less advanced model / Sonnet tier checks D6 craft, PC1-PC13 including hierarchy gate, the `concept.md` craft bar, Signature DNA, Meaning-encoding, "What this is NOT", section 1G/1H meaning, and platform appropriateness.

Each verifier writes full findings to a file and returns only:

```json
{ "verdict": "PASS|FAIL", "findingsPath": "...", "criticalCount": 0, "highCount": 0 }
```

The orchestrator AND-merges verdicts only. It does not read verifier findings text during the gate.

- `PASS`: structural verdict and craft verdict are both pass; screen is done.
- `FAIL`: send the same builder both findings paths verbatim with a fix prompt: "read both files, fix every CRITICAL/HIGH, then re-run L1". The builder reads the files, fixes, re-runs L1 self-eval, and then two fresh verifiers run.

## Artifacts

Store gate artifacts per round under `<sot>/_build-cache/<screenId>/`:

- `l1.5-r<n>.md` gates L2.
- `l2-r<n>.md` gates L3.
- `review-r<n>-structural.md`
- `review-r<n>-craft.md`
- `rebuttal-r<n>.md`
- `do-not-flag.md`

See `spec-build-review.md` for artifact formats.
