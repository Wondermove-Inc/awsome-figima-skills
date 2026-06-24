# PRD parsing — extraction method, interrogation checklist, tagging

## 1. Read and classify

If the PRD is a folder, classify each file so you weight core requirements over reference material:

| Class | Examples | Use |
|---|---|---|
| CORE | requirements, functional spec, user stories | Primary source for screens/flows/rules |
| FLOWS | journey maps, flow diagrams, wireframe notes | Screen sequencing + navigation |
| REFERENCE | personas, market research, brand notes | Audience context — feeds the `audience` block (and downstream Step 2 Direction) |
| SKIP | changelogs, meeting notes, unrelated | Ignore unless they contain a real requirement |

A single-file PRD is all CORE — read it whole.

## 2. Extract structure → prd-analysis.json

Build these, in this order (the schema in `assets/prd-analysis.schema.json` is the exact shape):

- **product** — name, one-line goal, the problem it solves.
- **successMetrics** (+ optional **constraints**) — what the PRD says success looks like (outcomes the
  design must make achievable, e.g. "knows balance is safe in 2s", a stated completion/conversion
  target) and the hard limits the build must respect (platform / compliance / performance / legal /
  brand). Derive from the PRD; if it's silent on success, surface it as an `openQuestion` rather than
  inventing a metric. `successMetrics` are *goals*; `constraints` are *non-negotiable limits*.
- **audience** — primary persona, age/context, mental model, accessibility needs, jobs-to-be-done.
  Derived from the PRD (`product`, `actors`, REFERENCE docs), not invented. Full method in
  `audience-research.md`. Step 2 (Direction) grounds its art direction on it.
- **targetPlatform** — **extract this FIRST.** Platform is a functional fact that gates nearly every
  design decision downstream (frame size, navigation model, touch targets, hover availability, safe
  areas, and microcopy wording). Capture:
  - `platforms` — one or more of: `mobile-native-ios`, `mobile-native-android`, `mobile-web`,
    `responsive-web`, `desktop-web`, `tablet`. Multi-value and `responsive-web` are valid (the spec
    and builder will then satisfy both mobile and desktop conventions at their respective widths).
  - `confirmed: true` — this field is mandatory for Step 1 to close. If the PRD does not state the
    platform, record `confirmed: false` and tag this entry `[NEEDS INPUT]` — the user must answer
    before Step 1 closes. Platform is NOT safely inferable; being wrong about it means every
    downstream pattern, component choice, and microcopy string may be wrong. It is never `[AUTO]`.
  - `deviceFrameDefaults` — fill from the canonical values once confirmed: mobile ≈ `390×844`, tablet
    ≈ `820×1180`, desktop ≈ `1440 wide`. These drive the builder's canonical device width in Step 4.
  - `safeAreaNeeded` — `true` for `mobile-native-ios`, `mobile-native-android`, `mobile-web`.
- **actors** — each role/persona with what they can do. (Audience demographics/mental-model go in the
  `audience` block above, not here; in `actors` capture only role + permissions that affect *what*
  gets built.)
- **flows** — ordered user journeys; each step names the screen it lands on. This is the explicit
  **IA artifact** (the screen-to-screen map), and it's how you catch missing screens: a flow step with
  no screen = a gap. (The human-readable journey/IA view also lives in `prebuild-product-map.md`; the
  `flows` array is the structured source of truth.)
- **screens** — the deliverable list. For each screen:
  - `id` (kebab-case, stable), `name` (human, the PRD's own term — keep Korean if the PRD is Korean),
    `purpose` (one line: what this screen is FOR — its job/intent).
  - `register` — an **initial** tag: `energy` (expressive/competitive/hero), `trust`
    (transactional/calm/legibility-first), or `neutral` (utility/scanning). Tag from the screen's
    *job*, not its looks. This is the source of truth ONLY for the initial pass — Step 2 `concept.md`'s
    **Register map** *finalizes* it; never leave it blank, never re-decide it downstream.
  - `content` — what information/fields it shows; for each field, its **source** (static, user input,
    API/data, computed).
  - `states` — which must exist: `default`, and any of `empty`, `loading`, `error`, `success`,
    `disabled`, `permission-denied` the screen needs. **A state existing is functional** (ask if
    unclear); how it looks is craft (don't ask).
  - `actions` — interactive affordances and what they do / where they go.
  - `rules` — business rules that govern the screen (validation, visibility, role gating).
- **openQuestions** — every gap you surface (see §3), each with a `severity` tag.

## 3. The completeness interrogation checklist

For every screen and flow, ask each of these. Anything not answered by the PRD becomes an
`openQuestions` entry with the right severity.

**Platform (cross-cutting — ask ONCE, block until answered)**
- Is the target platform stated in the PRD? If not, this is `[NEEDS INPUT]` — never `[AUTO]`. Platform
  determines navigation models (bottom tab bar vs sidebar vs top nav), primary input modality (touch vs
  pointer), touch-target sizing requirements (≥44×44pt on touch platforms), hover availability (NONE on
  touch — nothing may rely on hover as the only affordance), gesture vocabulary, safe-area requirements,
  AND microcopy wording ("드래그하여 올리기" on desktop, "업로드 / 사진 첨부" on mobile). Getting it
  wrong downstream is expensive. Ask first; close this before proceeding.

**Flow & navigation**
- Is there a screen for every step of every flow? Any jump that skips an unbuilt screen?
- What's the back/cancel/dismiss behavior on each screen? Where does "done" go?
- Entry points — how does the user arrive at each screen?

**Data & content**
- For every displayed field: where does the value come from? What format? What if it's missing/long?
- Are there lists/tables? What's the empty case, the loading case, the error case, the max/overflow case?
- Pagination, sorting, filtering — specified or assumed?

**States & behavior**
- Which of empty / loading / error / success / permission-denied must this screen have?
- What does a failed action show? What does a successful one show/route to?
- Optimistic vs confirmed updates — does it matter here?

**Rules, roles, edges**
- Validation rules on inputs? Required vs optional?
- Role/permission gating — who sees/does what?
- Zero-item, single-item, max-item, very-long-string, offline/slow-network behavior.
- Acceptance criteria — is "done" defined for this screen?

**Research grounding (the facts Step 2 Direction builds on — fill from the PRD, don't invent)**
- Does every screen have a defensible **purpose** (one line: what is this FOR)? A screen you can't
  state a purpose for is either redundant or under-specified — flag it.
- What's each screen's **initial register** — `energy`, `trust`, or `neutral`? Read it from the
  screen's *job* (a results/celebration screen leans energy; a payment/settings screen leans trust).
  This is an initial tag, not a craft decision — Step 2 finalizes it; just don't leave it blank.
- Does the PRD state what **success** looks like (the outcomes the design must enable)? If not, that's
  an `openQuestion` — don't invent a metric.
- Are there hard **constraints** (platform already captured; plus compliance / performance / legal /
  brand) the build must respect?
- **Audience** — is the primary persona / context / mental model / a11y need derivable from the PRD?
  See `audience-research.md`; capture into the `audience` block, surface as `[NEEDS INPUT]` only the
  pieces that genuinely change a product decision and the PRD leaves blank.

## 4. Tagging and severity

| Tag | Meaning | Action |
|---|---|---|
| `[AUTO]` | Safely inferable, near-zero product risk | Record the inference in the field; no question |
| `[ASSUMED]` | You inferred a real product choice | Must be **confirmed** by the user before Step 1 closes |
| `[NEEDS INPUT]` | Blocking — cannot proceed correctly | Must be **answered** by the user |
| `[CONFIRMED]` | Resolved via user answer | Folded into the structured PRD as fact |

Calibration:
- Lean `[AUTO]` only when any reasonable PM would decide the same way and being wrong is cheap
  (e.g. "a list screen needs a loading state" → AUTO, it must exist; *which* states beyond the
  obvious → ASSUMED if the PRD is silent and it's a real choice).
- Lean `[NEEDS INPUT]` when being wrong means rebuilding or shipping the wrong product (e.g. "can
  non-admins delete?" with no answer in the PRD).
- When torn between AUTO and ASSUMED, choose ASSUMED — confirming is cheap; a silent wrong call is not.

## 5. Resolving with the user

- Group related questions into a single ask-the-user round (don't fire one tool call per gap).
- Offer a recommended default as the first option when you have a sound PM opinion — but never
  pre-decide a `[NEEDS INPUT]` by only offering your guess.
- After each round, write answers back into `prd-analysis.json`, flip resolved tags to `[CONFIRMED]`,
  and re-scan: answers often surface new gaps (a confirmed "yes, bulk delete" implies a confirm
  dialog screen — now a new screen + its states to confirm).
- Stop only when `openQuestions` has zero `NEEDS_INPUT` and zero unconfirmed `ASSUMED`.

## 6. Hand-off

The confirmed `screens[]` (id + name + purpose + register) seeds `state.json.screens[]`. The full
`prd-analysis.json` is read by:
- **Step 2 (direction / art direction)** — the **purpose map + initial `register` per screen +
  `audience` + `successMetrics`** are the grounding it builds its visual direction on. It also
  *finalizes* the register in `concept.md`'s **Register map** (Step 1 sets the initial tag; Step 2
  decides the final value; Steps 3–5 only reference it). See `figma-product-direction/references/concept-template.md`.
- **Step 3 (foundation / design system)** — derives tokens + signature layer from the signed-off
  `concept.md`; the confirmed `targetPlatform` drives which interaction/motion/gesture/haptic patterns
  are in scope (hover, drag, cursor-based motion only where platform supports it; gestures and haptics
  only on native) and which conventions the design language is applied under. See `figma-product-foundation/references/platform-conventions.md`.
- **Step 4 (spec/copy)** — per-screen content, states, rules → DESIGN.md layout intent; it *references*
  the finalized register (never re-tags); AND `targetPlatform` drives microcopy wording choices in
  COPY.md (never use desktop drag-drop / hover / click language on a mobile screen, and vice-versa).
  See `figma-product-spec/references/copy-system.md`.
- **Step 5 (build)** — `targetPlatform.deviceFrameDefaults` drives the builder's canonical device
  width; the platform governs which UX patterns and components the builder uses. The brief carries
  `targetPlatform` explicitly so the builder does not have to re-derive it.

Keep field sources accurate — Step 3 uses them to decide what's real data vs static copy.
