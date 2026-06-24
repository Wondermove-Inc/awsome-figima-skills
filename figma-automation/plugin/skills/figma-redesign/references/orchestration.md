# Redesign Orchestration

Use this reference for `/figma-redesign` pre-flight, dispatch, and recovery details.

## Pre-Flight

1. Confirm the source file is open with `list_channels`; capture `channel` and `fileKey`. Stop if the
   file is not connected.
2. Confirm the target library is reachable with `fetch_library_catalog(libraryFileKey, scope:"all",
   outPath:<scratch>)`. Stop if unreachable.
3. Resolve frame ids to colon format with bounded metadata reads; screenshot every original frame.
4. Create or reuse a redesign/rebuild output page. Never mutate existing frames.
5. Pre-import the shared palette once and write `<sot>/rebuild/palette-map.json`:
   - foundation token ramp
   - common icon set
   - hot components shared by all screens
6. Default to serial. Concurrency is allowed only with a pre-imported palette, disjoint wrappers, and at
   most three writers.
7. Load `figma-playbook` memory indexes with `load --library <librarySlug> [--project <slug>]`. If
   library memory is sparse, bootstrap with `learn --library <librarySlug>`.
8. Report resolved frames, output page, and serial/concurrent mode before dispatching.

The orchestrator avoids deep structural reads; L1 owns inventory.

## Dispatch

Dispatch background Codex agents. Per-screen order is build, self-review, gate. Independent read-only
reviewers can run concurrently.

### Builder

Spawn one `figma_builder` per screen and reuse it across fix rounds.

Initial prompt must include:

- installed `figma-redesign` skill directory
- references to read: `builder-brief.md`, `original-inventory.md`, `variant-resolution.md`,
  `completeness-floor.md`, and `live-discovery.md`
- `channel`, original `frameId`, target `libraryFileKey`, scratch catalog path, `palette-map.json`,
  output `pageId`, ledger path, and memory index context
- requirement to build inventory first
- requirement to return the JSON defined in `builder-brief.md`
- concurrency rule: one writer on the assigned wrapper; on import-thread hang, record tail and return
  `importThreadHung:true`

For Phase 1.5 and fix rounds, resume the same builder with a lean delta. Do not resend the full brief.

### Verifiers

Spawn two fresh read-only verifiers every round, in parallel:

- `figma_structural_verifier`: execute D1-D5 plus scans from `review-protocol.md` and
  `completeness-floor.md`; build its own inventory.
- `figma_reviewer`: execute D6, section 1G/1H/5F, and D7 from `review-protocol.md`; judge craft,
  hierarchy, and meaning from screenshots plus targeted reads.

The orchestrator waits for both. `PASS` requires structural and craft pass. On failure, send the
combined findings to the same builder in one fix round.

## Hung Import Recovery

If a builder returns `importThreadHung:true`, do not retry the same import loop.

1. Ask the user to restart the Figma plugin or reconnect MCP.
2. Confirm with `list_channels`.
3. Drain recorded import tails in one post-restart single-writer pass.

Non-import writes can still succeed while the import thread is wedged; treat a structurally complete
build with a blocked import tail as recoverable.

## Watchdog

If a builder produces no new ledger, screenshot, or progress artifact for an extended period, probe disk
artifacts before assuming total failure. If artifacts show a complete-but-tail-blocked build, stop the
agent and recover the tail.
