# Platform conventions — UX patterns + microcopy by platform

**Why this file exists.** The same product feature works differently on mobile and desktop — not just
visually but structurally. Navigation lives in different places, primary input changes from pointer to
touch, hover doesn't exist on touch screens, and the same action is worded differently. This reference
captures those conventions per platform so every step in the pipeline (foundation, spec, build, review)
makes consistent, platform-correct decisions from a single source of truth rather than guessing
independently.

`targetPlatform` is captured at Step 1 and is required to be `confirmed: true` before any downstream
step proceeds. Everything in this file is applied **relative to the confirmed platform**. For
`responsive-web`, both the mobile-web AND desktop-web columns must be satisfied simultaneously at
their respective breakpoints.

---

## Contents

- UX patterns by platform
- Microcopy conventions by platform

## Part 1 — UX patterns by platform

| Concern | `mobile-native-ios` / `mobile-native-android` / `mobile-web` | `desktop-web` | `tablet` | `responsive-web` |
|---|---|---|---|---|
| **Primary navigation** | Bottom tab bar (5 items max); back chevron in a fixed header; drawers via swipe-from-edge or hamburger; NO persistent sidebar | Top navigation bar; horizontal tabs; persistent sidebar at ≥1280px; breadcrumbs for deep hierarchies | Bottom tab bar OR persistent sidebar (portrait vs landscape adaptive); avoid hidden drawers | Bottom tab on narrow; sidebar/top-nav on wide (≥1024px breakpoint); a single IA must work in both |
| **Primary input** | Touch — finger, not pointer. No hover. No cursor. Tap, swipe, pinch, long-press. | Pointer — mouse or trackpad. Hover states are valid and expected. Drag-and-drop is a first-class interaction. Keyboard shortcuts add value. | Touch (primary) + optional pointer on some devices | Same touch rules as mobile below ~1024px; same pointer rules above it |
| **Touch target size** | **Minimum 44×44 pt** (iOS HIG) / **48×48 dp** (Material) for every tappable element. Smaller visual elements are acceptable, but the tap zone must be ≥44×44. Non-negotiable. | No enforced minimum (pointer is precise); comfortable click targets are ≥32×32. | Minimum 44×44 pt (primarily touch) | ≥44 at mobile widths; ≥32 at desktop widths |
| **Hover availability** | **NONE.** Hover does not exist on touch. Never use hover as the ONLY path to information, affordance, or action (no hover-only tooltips, no hover-reveal buttons, no hover-activated menus). Every affordance must be reachable by tap alone. | Expected and useful. Hover states, hover tooltips, hover-reveal actions (row actions on hover), and sticky hover menus are valid patterns. | Treat as touch (hover unreliable) | Mobile breakpoints: no hover reliance. Desktop breakpoints: hover available. Design for both. |
| **Gestures** | Swipe (list dismiss, tab switch), pull-to-refresh, pinch-to-zoom, long-press (context menu, reorder) are natural and expected. Use system-standard gesture semantics (iOS: left swipe on row = destructive action). | Gestures are uncommon; drag-and-drop replaces swipe-to-dismiss. No pull-to-refresh convention. | Swipe and pinch supported; avoid complex multi-finger gestures | Mobile gestures at narrow; drag-drop at wide |
| **Density / spacing rhythm** | Touch-optimized: generous padding (≥16pt around tappable items), well-separated rows, minimal content density to avoid mistouch. | Compact is acceptable and often expected in productivity/data apps: 8–12px row padding, higher information density. | Medium — between mobile and desktop | Mobile density at narrow; desktop density at wide |
| **Safe areas / notch** | Required for `mobile-native-ios` and `mobile-native-android`. Respect top (status bar / Dynamic Island), bottom (home indicator — ≥34pt clear), and side insets on landscape. For `mobile-web`, at minimum respect bottom safe area for pinned CTAs. | Not applicable | Respect safe areas on iPad (ios) | Mobile breakpoints: apply mobile safe-area rules |
| **Scroll model** | Vertical scroll is the primary content delivery mechanism. Infinite scroll or pagination must work with one hand. Horizontal scroll only for explicitly scrollable carousels (not tables). | Vertical AND horizontal scroll both valid. Paginated tables, horizontal scrollable data grids, and sticky columns are standard patterns. | Vertical primary; horizontal for wide data | Mobile scroll rules at narrow; desktop at wide |
| **Modals / overlays** | Bottom sheet (action sheet) or full-screen modal are the native mobile patterns. Centered popovers are unusual and hard to dismiss on mobile. | Centered modal dialog; popover; tooltip; drawer from the side. All standard. | Bottom sheet or full-screen (portrait); popover (landscape with pointer) | Bottom sheet at mobile; centered modal at desktop |
| **Empty / loading states** | Full-screen skeleton or centered spinner + label at ≥44pt tap zone for any retry action. | Inline skeleton rows, table loading shimmer, or spinner in the content area. Smaller retry links acceptable. | Mobile patterns | Match the width's convention |
| **OS back / nav semantics** | iOS: swipe-from-left-edge = back. Android: system back button. In-app back chevron must always match the system's semantic. | Browser back button or breadcrumbs. No swipe-edge back convention. | iOS/Android patterns if native | Mobile at narrow (OS-aware back); browser back at wide |

> **Web-origin kit on a touch platform — size controls up to the floor.** A component library carries the
> input-modality assumptions of the platform it was built for. **Web/pointer-first kits (shadcn-class and
> most desktop UI kits) size their controls for a mouse** — their largest button/input is often only
> ~36–40px tall, *below* the 44/48 touch floor — because pointer targets have no minimum. So when the
> foundation maps a web-origin kit onto a touch `targetPlatform`, **do not assume the kit's native control
> size is touch-safe.** Record in `library-mapping.md` that touch controls (CTAs, rows, inputs, tappable
> icons) must be sized **up to ≥44/48 at the build layer** (and the label re-centered via the instance
> method — see `figma-design-patterns` Buttons). This is a normal modality adaptation, not a kit defect or
> a reason to switch libraries; flag it once at foundation time so the builder doesn't ship sub-floor controls.

---

## Part 2 — Microcopy conventions by platform

**The core principle:** the same action is worded through the lens of the platform's primary input
modality and OS conventions. A mobile user taps, shares via the OS share-sheet, uploads by
selecting from their gallery, and navigates with a back chevron — using desktop verb language on
their screen makes the interface feel out-of-place or worse, broken.

A word about `responsive-web`: the UI adjusts at breakpoints. The copy in COPY.md must either
(a) use language neutral enough that it works at both sizes ("업로드" works for both; "파일을
드래그하거나 선택하세요" only works at desktop widths), OR (b) define separate copy variants keyed
to the breakpoint. Prefer (a) where possible; fall back to (b) for actions that are structurally
different (drag-drop is a desktop-only interaction; the mobile equivalent is a tap-to-pick flow).

### Microcopy platform table

| Action / element | Desktop (`desktop-web`) | Mobile (`mobile-native-*`, `mobile-web`) | Notes |
|---|---|---|---|
| **File / image upload** | "드래그하여 올리거나 파일을 선택하세요" / "파일 선택" | "사진 첨부" / "업로드" / "갤러리에서 선택" | Drag-drop does not exist on mobile. NEVER use drag-drop language on a mobile screen — it's not just wrong wording, it's an impossible instruction. |
| **Affordance verb** | "클릭" / "클릭하여 …" | "탭" / "터치하여 …" | Prefer action-neutral verbs ("선택", "열기") when possible. Reserve explicit "클릭"/"탭" for instructional text or tooltips that must name the gesture. |
| **Share** | "링크 복사" / "공유 링크 복사" | "공유" (triggers OS share-sheet) | Mobile share goes through the native share-sheet; desktop has no equivalent and a copy-link CTA is more natural. |
| **Hover tooltip** | "마우스를 올리면 …" / described in tooltip on hover | Not used — no hover on touch. Use a tap-to-expand info icon ("ⓘ 탭하여 자세히 보기") or inline label. | Any desktop tooltip content that is non-trivial (required for task completion) must have a tap-accessible equivalent on mobile. |
| **Navigation back** | "이전으로" / breadcrumb link text | Back chevron icon only; label optional and short ("홈", "목록"). No long "이전 페이지로 돌아가기" labels. | Mobile real estate is tight; the OS/app chrome is the back affordance. |
| **Scroll prompt** | "아래로 스크롤하여 더 보기" | "밀어서 더 보기" / "스와이프하여 더 보기" | Desktop users scroll; mobile users swipe. |
| **Drag-and-drop reorder** | "드래그하여 순서 변경" | "길게 눌러 순서 변경" / drag-handle icon only | Long-press initiates reorder on mobile; mouse-drag on desktop. |
| **Right-click / context menu** | "우클릭하면 옵션이 표시됩니다" | Long-press bottom sheet / "⋯" icon tap | No right-click on mobile. |
| **Keyboard shortcut hints** | Valid: "⌘K로 빠른 검색" | Never shown — no physical keyboard is guaranteed on mobile (and virtual keyboard shortcuts are not discoverable). | |
| **Download** | "파일 다운로드" / "저장" | "저장" / "사진 저장" / "파일 저장" | Download to file system is a desktop mental model; mobile users save to Photos, Files app, etc. Use the platform's vocabulary for storage. |
| **Print** | "인쇄" / "PDF로 저장" | Omit or hide — mobile print flows are rare and complex. Expose only if the feature is explicitly spec'd. | |

### Anti-patterns to flag as FAIL

These must never appear on the listed platform:

| Anti-pattern | Platform where it's a FAIL | Correct replacement |
|---|---|---|
| "드래그하여 올리기" / drag-drop instructions | `mobile-native-*`, `mobile-web` | "사진 첨부" / "업로드" |
| "마우스를 올리면 …" / hover-only affordance | `mobile-native-*`, `mobile-web` | Tap-accessible equivalent (ⓘ, inline label, or bottom sheet) |
| "클릭" as an affordance verb | `mobile-native-*`, `mobile-web` | "탭" or action-neutral ("선택") |
| "우클릭" / right-click instruction | `mobile-native-*`, `mobile-web` | Long-press or ⋯ icon |
| Keyboard shortcut hints | `mobile-native-*`, `mobile-web` | Remove entirely |
| Bottom tab bar absent | `desktop-web` main navigation | Top nav / sidebar |
| No hover states on interactive elements | `desktop-web` | Add `:hover` / hover variants |
| Touch targets below 44×44 pt | `mobile-native-*`, `mobile-web`, `tablet` | Pad tap zones to ≥44×44 |

### The upload example (the canonical case)

The design was: an upload dropzone with the label "이미지를 여기에 올려주세요" — correct on desktop
(the user can drag a file), wrong on mobile (there is no drag gesture; the user taps a button to open
their photo library or file picker). Platform-correct versions:

```
desktop-web:  dropzone with icon + "파일을 드래그하거나 클릭하여 업로드하세요"
              secondary: "또는 파일 선택"

mobile-web / mobile-native:  tap CTA button "사진 첨부" or "업로드"
                              no dropzone area — replaced by a simple tap target (44×44 pt min)
                              bottom sheet or system file picker opens on tap

responsive-web:  desktop width → dropzone variant
                 mobile width  → tap-CTA variant
                 COPY.md: two copy variants keyed to breakpoint, OR a neutral label like
                 "업로드" that works at both (omit the drag instruction entirely)
```
