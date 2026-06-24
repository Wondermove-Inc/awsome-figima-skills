---
name: figma-visual-researcher
description: Dynamic visual research and asset procurement for Figma product builds. Use when an orchestrator, builder, or reviewer needs real product UI/UX reference screenshots, anchor pattern analysis, brand logos, icons, photos, avatars, Lottie assets, or a structured reference/asset pack before or during a Figma build. Replaces narrow asset-fetch scripts with source-aware research, candidate judgment, provenance, and local file handoff.
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
- **Persistent ref-library write for common patterns.** When the request is for a recurring UI pattern
  (receipt/price-summary, empty state, list row, confirmation, payment, form), save the curated result
  to **both** `<sot>/_build-cache/visual-research/<pattern>/` AND the cross-project persistent
  ref-library at `design-system/_build-cache/ref-library/<pattern>/`. Future sessions check the
  ref-library first — a common pattern should be fetched ONCE, ever.
- **No browsing loops.** Stop at the first set that produces ≥2 curated candidates. More is not better
  when candidates are already strong.

## Reference Pack Contract

Return:

```json
{
  "mode": "reference_pack",
  "references": [
    {
      "id": "ref-strava-leaderboard",
      "requestId": "mobile-competitive-list-refs",
      "candidateRank": 1,
      "localPath": "/abs/path/foundation/refs/ref-strava-leaderboard.png",
      "sourceUrl": "https://...",
      "sourceYear": 2025,
      "product": "Strava",
      "screen": "Segment Leaderboard",
      "selectionRationale": "Best candidate for dense ranked rows and rationed competitive accent.",
      "patternsToTransfer": [
        "dense ranked rows",
        "number-first stat hierarchy",
        "single rationed accent"
      ],
      "trendSignals": [
        "compact rank rows",
        "segmented leaderboard filters",
        "restrained achievement emphasis"
      ],
      "doNotCopy": [
        "exact dark theme",
        "brand mark",
        "pixel layout"
      ],
      "confidence": "high"
    },
    {
      "id": "ref-nike-run-club-achievement",
      "requestId": "mobile-competitive-list-refs",
      "candidateRank": 2,
      "localPath": "/abs/path/foundation/refs/ref-nike-run-club-achievement.png",
      "sourceUrl": "https://...",
      "sourceYear": 2024,
      "product": "Nike Run Club",
      "screen": "Achievement / activity detail",
      "selectionRationale": "Alternate candidate for sports celebration and large stat hierarchy.",
      "patternsToTransfer": ["achievement hierarchy", "sporty empty/result energy"],
      "trendSignals": ["large stat-led result moment", "mobile-native activity recap"],
      "doNotCopy": ["Nike brand language", "exact badge art"],
      "confidence": "medium"
    }
  ]
}
```

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

Return:

```json
{
  "mode": "asset_pack",
  "assets": [
    {
      "id": "brand-naverpay",
      "requestId": "brand-naverpay",
      "candidateRank": 1,
      "type": "brand",
      "format": "svg",
      "localPath": "/abs/path/_build-cache/assets/brand-naverpay.svg",
      "ingest": "svg:createNodeFromSvg",
      "sourceUrl": "https://...",
      "selectionRationale": "Cleanest wordmark lockup for a compact payment-method row.",
      "confidence": "high"
    },
    {
      "id": "brand-naverpay-raster",
      "requestId": "brand-naverpay",
      "candidateRank": 2,
      "type": "brand",
      "format": "png",
      "localPath": "/abs/path/_build-cache/assets/brand-naverpay-raster.png",
      "ingest": "raster:import_image",
      "sourceUrl": "https://...",
      "selectionRationale": "Fallback raster candidate if the SVG lockup renders poorly at target size.",
      "confidence": "medium"
    }
  ]
}
```

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

If a builder cannot continue because it needs media, it returns:

```json
{
  "blocked": true,
  "reason": "visual_research_required",
  "referenceRequests": [
    {
      "id": "mobile-payment-status-refs",
      "mode": "reference_pack",
      "referenceKind": "real mobile payment status screenshots",
      "brief": "Find real mobile payment-status UI references for a Korean fintech/sports app. I need trustworthy success, pending, and failure states with calm hierarchy, clear transaction outcome, compact receipt-like detail rows, restrained celebratory feedback, and no playful illustration-heavy treatment. Prefer polished production screenshots over marketing mockups; examples can be Toss, KakaoPay, NaverPay, Apple Pay, Stripe mobile, or similarly credible payment apps.",
      "targetScreen": "payment status screen",
      "screens": ["payment success", "payment pending", "payment failure"],
      "minSourceYear": 2024,
      "trendFocus": ["modern fintech status hierarchy", "compact receipt rows", "restrained confirmation feedback"],
      "usage": "pattern reference before composing the payment completion and error states",
      "placement": "full-screen mobile UI reference for status hierarchy and receipt detail layout",
      "targetSize": "mobile screenshots near 390x844 or source listing screenshots large enough to inspect at phone scale",
      "sourcePreference": ["App Store screenshots", "Google Play screenshots", "official product pages"],
      "candidateCount": 4,
      "desiredQualities": ["trustworthy", "Korean fintech", "mobile", "receipt detail", "clear status hierarchy"],
      "styleKeywords": ["calm", "precise", "high-trust", "minimal celebration"],
      "mustHave": ["real product screenshot", "source URL", "transferable status pattern"],
      "avoid": ["generic success clipart", "landing-page mockups", "overly playful 3D mascot art"]
    }
  ],
  "assetRequests": [
    {
      "id": "brand-naverpay",
      "mode": "asset_pack",
      "type": "brand",
      "assetKind": "payment row logo",
      "query": "NaverPay logo",
      "brief": "Find a high-confidence NaverPay brand mark for a mobile payment-method row. Prefer an official or near-official SVG with the real NaverPay wordmark, clean transparent background, and horizontal lockup that can sit beside KakaoPay and card-network marks at small size. Do not substitute a generic Naver logo, generic wallet icon, or recreated look-alike.",
      "targetScreen": "payment method selection screen",
      "usage": "payment method row logo",
      "placement": "left side of a compact payment-method list row beside the method label",
      "targetSize": "16-24px tall rendered logo inside a 390px mobile payment row",
      "preferredFormat": "svg",
      "sourcePreference": ["official brand/press assets", "verified SVG source", "high-confidence public asset fallback"],
      "candidateCount": 3,
      "fallbackAllowed": false,
      "styleKeywords": ["official", "flat vector", "small-size legible", "transparent background"],
      "desiredQualities": ["authentic wordmark", "crisp at small size", "compatible with other payment logos"],
      "mustHave": ["NaverPay, not generic Naver", "transparent background", "local SVG if available"],
      "avoid": ["generic Naver symbol only", "raster screenshot crop", "fake recreation"]
    }
  ]
}
```

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

Bad:

```json
{ "id": "trophy", "mode": "asset_pack", "type": "icon", "query": "trophy", "brief": "Find trophy icon" }
```

Good:

```json
{
  "id": "hero-trophy",
  "mode": "asset_pack",
  "type": "icon",
  "assetKind": "dimensional hero trophy icon",
  "query": "premium 3D trophy celebration icon",
  "brief": "Find a premium dimensional trophy visual for a mobile amateur sports tournament result screen. It should feel athletic, celebratory, and polished rather than childish, with a strong silhouette at 96-140px, transparent background, and no busy confetti competing with Korean copy.",
  "targetScreen": "match result empty state",
  "usage": "hero visual above the result summary and primary CTA",
  "placement": "top-of-screen hero illustration",
  "targetSize": "96-140px rendered size inside a 390px mobile frame, transparent background",
  "preferredFormat": "svg-or-png",
  "sourcePreference": ["Iconify colorful sets", "official public asset libraries", "LottieFiles poster fallback"],
  "candidateCount": 3,
  "styleKeywords": ["3D", "premium", "athletic", "celebratory", "small-size legible"],
  "desiredQualities": ["strong silhouette", "clear against Korean text", "not childish", "mobile-safe"],
  "mustHave": ["transparent background", "usable at 96px", "local file handoff"],
  "avoid": ["flat line icon", "cartoon trophy", "busy confetti", "watermarked stock"]
}
```

Validate request objects before dispatch when possible:

`<figma-visual-researcher-skill-dir>` means this installed skill directory as shown in Codex's
available-skills list.

```bash
python3 <figma-visual-researcher-skill-dir>/scripts/validate-visual-request.py <request.json>
```

## Files

- Read `references/contracts.md` when implementing or changing orchestration contracts.
- Run `scripts/validate-visual-pack.py <pack.json>` before returning a pack from automation.
- Run `scripts/validate-visual-request.py <request.json>` before dispatching a request from automation.
