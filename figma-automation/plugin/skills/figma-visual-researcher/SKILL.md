---
name: figma-visual-researcher
description: Find visual references and media assets for Figma product builds. Use for UI screenshots, pattern analysis, logos, icons, photos, avatars, or asset packs with provenance.
---

# Figma Visual Researcher

Use this skill when a Figma workflow needs visual evidence or concrete media. The output is a
structured pack of saved local files plus provenance and design guidance. Do not write to Figma.

## Operating Model

You are a dynamic researcher, not a fixed registry lookup. Use the best available source for the
request, inspect candidates, choose deliberately, and return a compact JSON result the orchestrator can
pass to a builder.

Two modes:

- `reference_pack` — find real UI/UX product screenshots and explain which patterns transfer.
- `asset_pack` — find concrete media files: logo SVG/PNG, icon SVG, product/photo image, avatar, or
  Lottie JSON plus poster preview.

If a runtime supports nested agent calls, a builder may invoke `visual-researcher` directly. Otherwise
the builder returns `referenceRequests` or `assetRequests`; the orchestrator dispatches this agent and
resumes the same builder with the returned pack.

## Source Policy

Prefer real product evidence:

1. For UI/UX references, use sources evidenced as 2024 or newer. Prefer current App Store / Google
   Play screenshots, official product pages, official docs/blogs, public product galleries, or live
   product screenshots captured now. Do not use stale pre-2024 UI references.
2. Prefer references that show current, trendy shipped UI patterns: modern mobile navigation, dense but
   scan-friendly rows, bottom sheets, progressive disclosure, AI-era search/command surfaces, current
   fintech/sports/content patterns, updated platform conventions, and restrained motion/visual depth.
3. Official brand guidelines, docs, blogs, press kits, and public product galleries are preferred for
   concrete assets.
4. Well-known live products whose UI can be captured with browser screenshots are acceptable when the
   capture is current.
5. Public asset APIs only when they are a good match, not as the only source.

Avoid Dribbble, Behance, Pinterest, pure moodboards, and concept art in v1 unless the request explicitly
asks for mood exploration. Never pass decorative inspiration as product UX evidence.

## Workflow

1. Parse the request and decide whether it is `reference_pack`, `asset_pack`, or both.
2. Search broadly enough to find real candidates. Use web/image search, official listings, official
   pages, and source-specific APIs where available.
3. Inspect candidates before saving. Reject low-resolution, cropped, unrelated, watermarked, generic
   stock, fake logo, or concept-only results.
4. Save selected files under the requested project path:
   - references: `<sot>/foundation/refs/`
   - assets: `<sot>/_build-cache/assets/`
5. Return JSON only. Include multiple candidates per request, source URL, confidence, and why each file
   is useful.
6. Validate output with `scripts/validate-visual-pack.py` before handing it back.

Do not return a single "best" asset/reference for a request. Bring back a small, curated set and let the
builder choose in screen context. Default target: 2-4 candidates per `requestId`; for foundation-level
references, 4-6 total references is still the bar.

**Bounded capture discipline (cost control).**
- **Triage on thumbnails first.** Before downloading a full-resolution screenshot, reject candidates
  that are clearly off-target from the thumbnail alone (wrong category, obvious stock imagery,
  pre-2024 UI style). Only download candidates that survive thumbnail inspection.
- **Save only curated references.** Candidates rejected after thumbnail review are discarded — do NOT
  save them locally. The local file count == the curated set.
- **Persistent reference memory for common patterns.** When the request is for a recurring UI pattern
  (receipt/price-summary, empty state, list row, confirmation, payment, form), save the curated files
  under `<sot>/_build-cache/visual-research/<pattern>/` and also return a `memoryProposals` entry for
  `figma-playbook apply` with `store:"global"`, `type:"reference"`, and a `ref-<pattern>-<slug>` name.
  Future sessions check the global playbook memory first; `_build-cache` is only the local artifact
  cache for this run.
- **No browsing loops.** Stop at the first set that produces ≥2 curated candidates. More is not better
  when candidates are already strong.

## Reference Pack Contract

Read `references/contracts.md#reference-object` for the exact output fields and acceptance rules.

Reference quality bar:

- 4-6 references for a new product foundation.
- 2-4 candidates per request when a builder asks for a specific reference need.
- Every UI/UX reference must have `sourceYear >= 2024`; if the source cannot be dated or captured as
  current, reject it.
- Each reference must map to a product need, screen, or interaction pattern.
- Each reference must include `requestId`, `candidateRank`, and `selectionRationale` so the builder can
  compare options.
- `patternsToTransfer` must be practical builder guidance, not vague adjectives.
- `trendSignals` must identify why this is a current UI/UX pattern worth studying, not just describe
  the screenshot.
- `doNotCopy` must prevent pixel cloning and brand misuse.

## Asset Pack Contract

Read `references/contracts.md#asset-object` for the exact output fields, ingest values, and acceptance
rules.

Asset quality bar:

- Brand/logo: prefer official SVG/press kit. If not found, use a high-confidence downloadable SVG/PNG
  with source URL and note confidence. Never substitute a look-alike brand.
- Icon: prefer the product's kit/library icon if available, then Iconify/Lucide with an exact slug.
  If the requested concept is ambiguous, return candidates instead of forcing one.
- Photo/image: prefer official product/domain imagery or clearly suitable public imagery; avoid generic
  stock-like filler when the UI needs real domain signal.
- Lottie: save JSON and a poster PNG when available. Figma MCP cannot import live animation; builder
  imports the poster and keeps JSON for handoff.
- Every asset candidate must include `requestId`, `candidateRank`, and `selectionRationale`. Return
  2-4 candidates per request whenever physically possible. If only one legitimate candidate exists
  (rare, usually official brand source), include `singleCandidateReason` and describe rejected sources.

Figma ingest values:

- SVG: `svg:createNodeFromSvg`
- PNG/JPEG/WebP poster or photo: `raster:import_image`
- Lottie JSON: `lottie:poster-import-json-handoff`

## Request Escalation

Every visual request is a prompt, not a keyword lookup. Builders must describe the intended screen,
placement, size, style, file needs, source preference, required properties, and anti-targets clearly
enough that the researcher can return useful candidates without another clarification round.

Required fields for each `referenceRequests[]` item:

- `id`: stable kebab-case request id.
- `mode`: `reference_pack`.
- `referenceKind`: what kind of reference is needed, e.g. `real mobile payment status screenshots`.
- `brief`: detailed natural-language prompt, at least 120 characters.
- `targetScreen`: the screen being built.
- `screens`: concrete source screens/states to search for.
- `minSourceYear`: minimum acceptable evidence year for UI/UX references; must be `2024` or newer.
- `trendFocus`: current UI/UX patterns the researcher should actively look for.
- `usage`: how the builder will use the reference.
- `placement`: where the pattern applies in the Figma screen.
- `targetSize`: expected source/crop scale, e.g. `mobile screenshots around 390x844`.
- `sourcePreference`: preferred source classes, e.g. App Store, Google Play, official product pages.
- `candidateCount`: requested number of candidates, normally 2-4.
- `styleKeywords`: aesthetic/rendering language.
- `desiredQualities`: quality bar for acceptance.
- `mustHave`: non-negotiable properties.
- `avoid`: sources, styles, or treatments that should be rejected.

Required fields for each `assetRequests[]` item:

- `id`: stable kebab-case request id.
- `mode`: `asset_pack`.
- `type`: `brand`, `icon`, `image`, `avatar`, `lottie`, or `other`.
- `assetKind`: more specific kind, e.g. `dimensional hero trophy icon` or `payment row logo`.
- `query`: search phrase.
- `brief`: detailed natural-language prompt, at least 120 characters.
- `targetScreen`: the screen being built.
- `usage`: how the asset will be used.
- `placement`: exact UI placement.
- `targetSize`: rendered Figma size and any crop/background constraints.
- `preferredFormat` or `outputFormats`: expected file handoff format.
- `sourcePreference`: preferred sources or source classes.
- `candidateCount`: requested number of candidates, normally 2-4.
- `styleKeywords`: style/rendering keywords such as `3D`, `4D/motion-like`, `isometric`,
  `flat vector`, `photo-real`, `glass`, `editorial`, or `small-size legible`.
- `desiredQualities`: quality bar for acceptance.
- `mustHave`: non-negotiable properties.
- `avoid`: look-alikes, weak substitutes, bad source types, or visual treatments to reject.

If a builder cannot continue because it needs media, it returns the request object described in
`references/contracts.md#builder-behavior`.

The orchestrator dispatches `visual-researcher`, then resumes the same builder with the returned
`references` and `assets`.

The builder chooses from the returned candidates. The researcher recommends via `candidateRank`, but the
builder owns the final choice because only the builder sees the live layout, scale, crop, hierarchy, and
neighboring assets.

Every request item must include a detailed natural-language `brief`. The brief is where the builder
explains what it actually needs: dimensionality (`flat`, `3D`, `4D/motion-like`, `glass`, `isometric`),
aesthetic, product context, target screen, intended Figma usage, constraints, and anti-targets. Do not
send vague requests such as "find trophy icon" or "get payment refs". For `reference_pack`, always ask
for 2024-or-newer product evidence and name the current UI/UX trends to look for.

For bad and good request examples, read `references/contracts.md#builder-behavior`.

Validate request objects before dispatch when possible:

`<figma-visual-researcher-skill-dir>` means this installed skill directory as shown in Codex's
available-skills list. Run
`python3 <figma-visual-researcher-skill-dir>/scripts/validate-visual-request.py <request.json>`.

## Files

- Read `references/contracts.md` when implementing or changing orchestration contracts.
- Run `scripts/validate-visual-pack.py <pack.json>` before returning a pack from automation.
- Run `scripts/validate-visual-request.py <request.json>` before dispatching a request from automation.
