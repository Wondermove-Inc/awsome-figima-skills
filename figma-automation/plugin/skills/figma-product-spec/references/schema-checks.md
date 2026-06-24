# Schema checks — gating the spec before the build

Both spec artifacts are validated before Step 5 (build). A failing artifact is not build-ready; the
orchestrator's Step-4 gate blocks on it. Regenerate-on-fail, like `figma-design-md`'s lint loop.

## DESIGN.md — @google/design.md lint

```bash
npx @google/design.md lint <sot>/design/DESIGN.md --format json
```

- Exit clean (no errors) = pass. Warnings are advisory (unknown sections/tokens are accepted by the
  spec) — read them, fix if real, but they don't block.
- On error: read the JSON, fix the frontmatter/section issue, re-lint. **Max 3 attempts.** Common
  causes: malformed YAML frontmatter, duplicate section headings (the spec rejects two `## Colors`),
  bad token reference syntax (`{path.to.token}`).
- If `npx` can't fetch the package (offline/sandboxed), report it and fall back to a structural check:
  frontmatter parses as YAML, required keys present, section order valid, no duplicate headings.

## DESIGN.md — direction + art-direction presence (the anti-flat check the linter can't do)

The `@google/design.md` lint validates *structure*, not whether the **soul layer** is present. A spec
that lints clean but carries no art-direction builds flat/assembled (the L3 craft reviewer then has no
craft bar and silently passes generic screens). So before marking the spec build-ready, also assert:

- **`<sot>/direction/concept.md` exists** and contains its frozen section headings (Signature DNA,
  Meaning-encoding philosophy, "What this is NOT", Craft toolkit per register, Register map). A missing
  `concept.md` = **STOP, run Step 2 (direction) first** — do not advance to build.
- **Every `### <screen-id>` block carries populated art-direction fields** — Metaphor, Expresses,
  Hero+meaning, Craft moves, Signature usage, Motion — each non-empty and traced to a `concept.md`
  section (not blank, not boilerplate copy-pasted across screens). A block with only the structural
  fields (Archetype / Regions / States) is a **flattened spec** → send back to Step 4 to re-apply the
  direction.

This is the spec-side mirror of `spec-build-review.md` STEP 4.5's "Direction + soul presence" backstop.
Treat a missing concept.md or blank art-direction fields as a red check — never advance.

## COPY.md — schema + screen coverage

`<figma-product-spec-skill-dir>` means the installed `figma-product-spec` skill directory shown in
Codex's available-skills list.

```bash
python "<figma-product-spec-skill-dir>/scripts/check_copy.py" <sot>/design/COPY.md --screens "login,dashboard,settings"
```

Pass the **confirmed screen ids** (from `state.json.screens[]`) as a comma list. The script:
1. Splits the YAML frontmatter from the markdown body and parses the frontmatter.
2. Validates it against `assets/copy-md.schema.json` (voice/tone/terminology/patterns present;
   `screens` is a map of screenId → object).
3. Checks **coverage**: every passed screen id has an entry in `screens`, and each entry is non-empty.
4. Scans for placeholder leakage (`lorem`, `ipsum`, `TODO`, `Title`, `Label`, `placeholder text`) and
   flags any hit.

Exit code 0 = pass; non-zero prints the failures. Fix COPY.md and re-run (max 3 attempts).

> The script depends only on `pyyaml` (already used elsewhere in this repo's tooling). If unavailable,
> the script falls back to a minimal hand-parser for the frontmatter so the coverage check still runs.

## After both pass
Update the spec step's `schemaCheck = "pass"` in `state.json.steps[…]` and let the orchestrator advance
to the build step (Step 5). (The state.json step-id *key* is a cross-skill contract owned by the
orchestrator — use whatever key it defines; don't rename it here.) Never advance with a red check — the
build's whole completeness gate (reviewer D1) compares the canvas against these files; a broken spec
means a meaningless gate.
