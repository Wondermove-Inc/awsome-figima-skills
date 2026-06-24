# Visual Researcher Contracts

This file is the stable handoff contract between orchestrators, builders, and the `visual-researcher`
agent.

## Modes

`reference_pack` finds visual UX evidence. It saves images to `<sot>/foundation/refs/` and returns
`references[]` grouped by `requestId`. UI/UX references must be evidenced as 2024 or newer and should
surface current shipped-product patterns, not stale screenshots.

`asset_pack` finds concrete media for a build. It saves files to `<sot>/_build-cache/assets/` and
returns `assets[]` grouped by `requestId`.

A single request can ask for both modes, but outputs stay separated.

## Builder Behavior

Builders do not browse. They consume saved files and contract JSON.

If a builder needs references or assets that were not in its brief, it must stop and return a request
object. It must not search, guess, or substitute.

Every `referenceRequests[]` and `assetRequests[]` item must include a detailed natural-language
`brief`. This is not optional metadata. It is how the builder transfers intent to the researcher.
Requests must be specific enough to answer these questions without another clarification round:

- target screen and exact usage;
- placement in the screen;
- target rendered/source size;
- asset/reference kind;
- preferred file format or source size;
- desired number of candidates;
- source preferences;
- minimum source year for UI/UX references;
- current trend focus, such as bottom-sheet flows, compact AI-era search/command surfaces, modern
  mobile-native result states, current fintech trust patterns, or dense scan-friendly rows;
- desired aesthetic and quality bar;
- dimensionality or rendering style, when relevant (`flat`, `3D`, `4D/motion-like`, `isometric`,
  `glass`, `editorial`, `photo-real`, etc.);
- domain/product context and audience;
- constraints such as official source, transparent background, small-size legibility, or mobile-first;
- anti-targets: what must not be returned.

Reject vague requests like "find logo", "find good refs", "3D trophy", or "payment screenshot".
The visual researcher returns multiple candidates per request. The builder chooses the final candidate.

### Request Item Fields

Common required fields:

- `id`: stable kebab id.
- `mode`: `reference_pack` or `asset_pack`.
- `brief`: detailed natural-language prompt, at least 120 characters.
- `targetScreen`: screen being built.
- `usage`: how the builder will use the returned file or reference.
- `placement`: exact screen placement or pattern area.
- `targetSize`: expected source/rendered size, including mobile frame size or asset px size.
- `sourcePreference`: source classes to try first.
- `candidateCount`: requested candidate count, 2-6.
- `styleKeywords`: non-empty list.
- `desiredQualities`: non-empty list.
- `mustHave`: non-empty list.
- `avoid`: non-empty list.

Additional `referenceRequests[]` fields:

- `referenceKind`: e.g. `real mobile payment status screenshots`.
- `screens`: source screens/states to search for.
- `minSourceYear`: integer year, minimum `2024`.
- `trendFocus`: current UI/UX patterns the researcher must actively evaluate.

Additional `assetRequests[]` fields:

- `type`: `brand`, `icon`, `image`, `avatar`, `lottie`, or `other`.
- `assetKind`: e.g. `dimensional hero trophy icon` or `payment row logo`.
- `query`: search phrase.
- `preferredFormat` or `outputFormats`: desired handoff formats.

```json
{
  "blocked": true,
  "reason": "visual_research_required",
  "referenceRequests": [
    {
      "id": "mobile-payment-status-refs",
      "mode": "reference_pack",
      "referenceKind": "real mobile payment status screenshots",
      "brief": "Find real mobile payment-status UI references for a Korean fintech/sports app. I need trustworthy success, pending, and failure states with calm hierarchy, clear transaction outcome, compact receipt-like detail rows, restrained celebratory feedback, and no playful illustration-heavy treatment. Prefer polished production screenshots over marketing mockups.",
      "targetScreen": "payment status screen",
      "screens": ["payment success", "payment pending", "payment failure"],
      "minSourceYear": 2024,
      "trendFocus": ["modern fintech status hierarchy", "compact receipt rows", "restrained confirmation feedback"],
      "usage": "pattern reference before composing the payment completion and error states",
      "placement": "full-screen mobile UI reference for status hierarchy and receipt detail layout",
      "targetSize": "mobile screenshots near 390x844 or source listing screenshots large enough to inspect at phone scale",
      "sourcePreference": ["App Store screenshots", "Google Play screenshots", "official product pages"],
      "candidateCount": 4,
      "desiredQualities": ["trustworthy", "mobile", "clear status hierarchy"],
      "styleKeywords": ["calm", "high-trust", "fintech", "receipt-like", "minimal celebration"],
      "mustHave": ["real product screenshot", "source URL", "transferable status pattern"],
      "avoid": ["generic success clipart", "landing-page mockups"]
    }
  ],
  "assetRequests": [
    {
      "id": "hero-trophy-asset",
      "mode": "asset_pack",
      "type": "icon",
      "assetKind": "dimensional hero trophy icon",
      "query": "trophy celebration",
      "brief": "Find a hero trophy asset for a mobile amateur sports tournament app. It should feel premium and celebratory without looking childish: preferably a polished 3D or dimensional vector/PNG with warm athletic energy, strong silhouette at 96-140px, transparent background, and no confetti clutter that would fight Korean text. A flat Lucide line icon is too weak for this hero use.",
      "targetScreen": "match result empty state",
      "usage": "empty-state or result hero visual",
      "placement": "top-of-screen hero illustration above the result summary",
      "targetSize": "96-140px rendered size inside a 390px mobile frame, transparent background",
      "preferredFormat": "svg-or-png",
      "sourcePreference": ["Iconify colorful sets", "official public asset libraries", "LottieFiles poster fallback"],
      "candidateCount": 3,
      "styleKeywords": ["3D", "premium", "sports", "celebratory", "transparent background"],
      "desiredQualities": ["strong silhouette", "clear against Korean text", "not childish", "mobile-safe"],
      "mustHave": ["transparent background", "usable at 96px", "local file handoff"],
      "avoid": ["flat line icon", "cartoon trophy", "busy confetti"]
    }
  ]
}
```

## Reference Object

Required fields:

- `id`: stable kebab id.
- `requestId`: the originating request id.
- `candidateRank`: integer rank starting at 1; rank 1 is the researcher's recommendation, not a forced
  builder choice.
- `localPath`: absolute path to the saved image.
- `sourceUrl`: source page or direct media URL.
- `sourceYear`: evidence year for the screenshot/source/capture; must be `2024` or newer.
- `product`: product or brand name.
- `screen`: what the screenshot shows.
- `selectionRationale`: why this candidate is useful and how it differs from the alternatives.
- `patternsToTransfer`: concrete builder guidance.
- `trendSignals`: specific current UI/UX patterns visible in the reference.
- `doNotCopy`: boundaries that prevent cloning or brand misuse.
- `confidence`: `high`, `medium`, or `low`.

Return 2-4 references per specific `requestId` when the builder asks for a targeted reference need. For
foundation-wide research, return 4-6 references total.

## Asset Object

Required fields:

- `id`: stable kebab id.
- `requestId`: the originating request id.
- `candidateRank`: integer rank starting at 1; rank 1 is the researcher's recommendation, not a forced
  builder choice.
- `type`: `brand`, `icon`, `image`, `avatar`, `lottie`, or `other`.
- `format`: file format such as `svg`, `png`, `jpeg`, `webp`, or `json`.
- `localPath`: absolute path to the saved file.
- `ingest`: one of `svg:createNodeFromSvg`, `raster:import_image`,
  `lottie:poster-import-json-handoff`, or `handoff-only`.
- `sourceUrl`: source page or direct media URL.
- `selectionRationale`: why this candidate is useful and how it differs from alternatives.
- `confidence`: `high`, `medium`, or `low`.

Optional but recommended fields:

- `posterPath` for Lottie poster PNG.
- `licenseNote` when the source has usage terms worth surfacing.
- `singleCandidateReason` only when a real source search finds exactly one legitimate candidate.

Return 2-4 asset candidates per `requestId` whenever physically possible. Do not collapse candidates into
one final answer just because rank 1 looks best.

## Acceptance Rules

Reject a pack when:

- any local path is relative or missing on disk;
- any UI/UX reference has `sourceYear < 2024`;
- any reference lacks `patternsToTransfer`, `trendSignals`, or `doNotCopy`;
- any asset lacks an ingest route;
- any candidate lacks `requestId`, `candidateRank`, or `selectionRationale`;
- any `requestId` group has fewer than 2 candidates without a `singleCandidateReason`;
- a brand asset has `confidence:"low"` and no `alternates`;
- an output cites concept-art/moodboard sources as product UX evidence without explicit user request.
