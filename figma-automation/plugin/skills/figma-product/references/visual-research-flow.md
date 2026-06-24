# Visual Research Lane

`/figma-product` uses `visual-researcher` before and during build. This is not a fifth product step and
not four extra steps. It is a cross-cutting lane with hooks inside the existing PRD, direction, spec,
and build steps. The goal is to avoid generic screens, missing logos/icons/photos, and builder-side
browsing.

## Ownership

- `visual-researcher` finds references and concrete media only. It writes files and JSON packs; it never
  mutates Figma.
- Builders consume local files only. They never browse and never substitute a weaker asset.
- The orchestrator owns dispatch, validation, aggregation, and resuming the same builder.

## Hooks

1. **PRD hook: visual-needs census** — while `figma-product-prd` structures the PRD, write
   `<sot>/design/visual-needs.json` as a sidecar, not inside
   `prd-analysis.json`. Capture likely reference needs and named concrete assets from the PRD:
   payment brands, partner logos, domain photos, avatars, illustrations, Lottie moments, empty-state
   heroes, and screen-specific reference needs.
2. **Direction hook: reference prefetch + taste scan** — while `figma-product-direction` grounds the
   art direction, dispatch `visual-researcher` in `reference_pack` mode for 2024+ shipped UI/UX
   references (cache-first against the cross-project KB), and capture the dated taste scan (era-trends
   + category-taste). Save images to `<sot>/direction/refs/` and pack JSON to
   `<sot>/_build-cache/visual-research/direction-reference-pack.json`; analyzed refs also flow to the KB.
3. **Spec hook: concrete asset prefetch** — while `figma-product-spec` converts the foundation into
   buildable screen specs, turn concrete visible media needs into detailed `assetRequests` and fetch
   obvious assets before build. Save assets to
   `<sot>/_build-cache/assets/`, pack JSON to `<sot>/_build-cache/visual-research/prefetch-asset-pack.json`,
   and aggregate usable assets in `<sot>/_build-cache/assets/asset-manifest.json`.
4. **Build hook: active fetch** — while `figma-product-build` is running, if a builder returns
   `blocked:true, reason:"visual_research_required"`, validate its request, dispatch
   `visual-researcher`, append the returned pack to the aggregate, and resume the same builder with all
   candidates. Do not restart the screen unless the builder state is corrupted.

## Request Rules

- Validate every builder/orchestrator request:

```bash
python3 ${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-visual-researcher/scripts/validate-visual-request.py <request.json>
```

- Reference requests require `minSourceYear: 2024` and `trendFocus`.
- Asset and reference requests must be detailed natural-language prompts with `targetScreen`, `usage`,
  `placement`, `targetSize`, `sourcePreference`, `candidateCount`, `styleKeywords`,
  `desiredQualities`, `mustHave`, and `avoid`.
- Ask for candidates, not one final answer. The builder chooses in layout context.

## Pack Rules

- Validate every returned pack:

```bash
python3 ${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/figma-visual-researcher/scripts/validate-visual-pack.py <pack.json>
```

- Pass packs to builders as:

```json
{
  "visualResearch": {
    "references": [],
    "assets": [],
    "packs": ["/abs/path/to/pack.json"]
  }
}
```

- SVG assets use `svg:createNodeFromSvg`.
- PNG/JPEG/WebP assets and Lottie posters use `raster:import_image`.
- Lottie JSON is handoff-only plus poster preview; Figma MCP does not import live animation.

## State Tracking

Store visual research state under `state.json.visualResearch`. This state tracks the lane; it does not
change `currentStep` by itself:

```json
{
  "needs": "design/visual-needs.json",
  "referencePacks": ["_build-cache/visual-research/direction-reference-pack.json"],
  "assetPacks": ["_build-cache/visual-research/prefetch-asset-pack.json"],
  "assetManifest": "_build-cache/assets/asset-manifest.json",
  "pendingRequests": [],
  "resolvedRequests": []
}
```

If validation fails, return the request to the builder/orchestrator for more detail. Do not dispatch a
vague request.
