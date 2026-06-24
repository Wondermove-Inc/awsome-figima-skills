# Build Pre-Flight

Use this reference during `/figma-product-build` pre-flight before any screen builder is dispatched.

## Backend And File Shape

Use the installed `figma-mcp-express` MCP backend by default. Resolve the live MCP namespace in the
session; use `figma-mcp-express-dev` only when developing the local MCP server source.

Resolve the build file by `fileKey`, not by cached `channel`. Channel ids can change after reconnects;
node ids and file keys are the durable identifiers.

Detect whether the build file is:

- `library-local`: the build file is the design-system file or a copy of it. Components and variables
  are local; bind directly.
- `subscriber`: the build file has a subscribed design-system library. `get_variable_defs` can be empty;
  confirm subscribed variables with library APIs and import by key.

Record this shape in `state.json`; it determines token binding.

## Accent Binding

Most products customize one accent over a neutral library system.

- `library-local`: re-point the library primary token once when possible; instances inherit it.
- `subscriber`: subscribed variables are read-only in the consuming file. Create one local accent token
  and bind only accent surfaces such as primary CTA fill, status accent, focus ring, and active tab.

Do not rebind neutral, spacing, radius, or typography internals unless the spec explicitly requires it.

## Palette Map

Harvest component and variable keys once into `<sot>/_build-cache/palette-map.json`.

Rules:

- Reuse an existing cache if the library has not changed.
- Prefer REST or `fetch_library_catalog` with `FIGMA_TOKEN` over live plugin page walks.
- Without a token, use local component listing by page; spilled output is success and should be queried
  from disk.
- Store a wide role inventory with alternates and variant axes, not a single premature choice.
- Include accent token ids, token-spine variable keys, component-set keys by role, icon keys, text-style
  keys, and canonical device width.

Before building screens, prove one accent-bearing component end to end: import, instance, bind the
accent, screenshot, and record the verified recipe in `_build-cache`.

## Required Pages

Create or reuse:

- `Components`: local recurring product components and variants. Masters live here, organized in a
  clean grid; screens use instances.
- `Assets`: non-kit visual assets staged once and reused, including photos, maps, logos, wordmarks, and
  sourced icons.
- `References`: external shipped-product screenshots plus adjacent borrow-note captions. Do not stage
  the project's own generated renders here.
- `<Product> - Build`: final screen frames.

During canon work, promote recurring units to `Components` as soon as the repetition is clear. After the
canon locks, fan-out builders reuse those instances instead of rebuilding shared chrome.

## Build Inputs

Read:

- `DESIGN.md` for tokens and `## Screens`
- `COPY.md` for the `screens` string map
- `state.json.visualResearch`
- `<sot>/design/visual-needs.json`
- `<sot>/_build-cache/visual-research/`
- `<sot>/_build-cache/assets/asset-manifest.json`, if present

Validate visual packs before passing them to builders. Each builder brief receives only the relevant
references/assets plus pack paths.

Before dispatch, reconcile `state.json` with Figma reality, confirm the register surface treatment,
confirm pre-imported ids landed, confirm the SoT path, and char-diff COPY per region.
