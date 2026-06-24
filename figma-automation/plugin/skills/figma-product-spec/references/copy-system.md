# Authoring COPY.md — the copy system + the real strings

COPY.md does two jobs: it teaches **how to write copy** for this product (so future copy stays
consistent), and it provides **the actual strings** for every screen (so the build has no
placeholders). Both are required — a system with no strings can't be built from; strings with no
system drift the moment someone adds a screen.

Structure: YAML frontmatter (machine-readable: voice + the `screens` string map) + a markdown body
(the human-readable system guide). The frontmatter is what `scripts/check_copy.py` validates.

## Part 1 — the system (grounded in foundation/brand-voice.md)

Capture, in the frontmatter `voice` block and expanded in the body:

- **voice** — the product's personality in a sentence (e.g. "a calm, competent friend who never
  patronizes"). Straight from `brand-voice.md`.
- **tone** — how the voice flexes by context: success (warm, brief), error (plain, blame-free,
  actionable), empty (encouraging, points to the next action), destructive-confirm (serious, clear).
- **terminology** — the glossary: preferred terms and banned ones (e.g. use "송금", never "이체";
  "삭제" not "제거"). Consistency in product nouns/verbs is most of perceived polish.
- **patterns** — microcopy rules:
  - **Button labels name the resulting action or destination**, not a generic confirm. A label should
    let the user predict what happens next (the next screen, or the thing that gets done), so prefer a
    specific action verb over a generic confirm word (the local equivalent of "OK / Submit / Done").
    Sentence vs title case and punctuation: pick one convention and hold it.
  - **No redundant labels** — don't restate a value the UI already shows. A field whose value is
    self-evident needs no repeated caption; a status already conveyed by a countdown, a headline, and a
    disabled action does not also need a badge spelling it out. Redundant copy is visual noise the L3
    craft verifier will flag for removal — cut it at authoring time.
  - **Define formatting conventions once, in the voice block** — currency (grouping + unit placement),
    dates, time, relative-time thresholds (e.g. "just now" / "N minutes ago" / "yesterday" cutovers),
    and countdowns (the D-day style). Decide these explicitly for the product's locale so every string
    is consistent by construction, rather than each screen improvising its own format. (The exact
    formats are a per-product decision — record them here; don't leave them to the builder.)
  - **Length limits per element** (button ≤ N chars, helper text ≤ N) so labels don't wrap or truncate.
- **platform-appropriate wording** — every string that names an input gesture, upload method, or
  navigation action MUST match the `targetPlatform` confirmed in Step 1. Read
  `figma-product-foundation/references/platform-conventions.md` (Part 2) before writing any such
  string. The rules:
  - On **touch platforms** (`mobile-native-*`, `mobile-web`): use "탭", "사진 첨부"/"업로드",
    "공유" (OS share-sheet), "길게 눌러 …" — NEVER "클릭", "드래그", "마우스를 올리면", "우클릭".
  - On **desktop** (`desktop-web`): drag-drop affordances ("드래그하여 올리거나 파일 선택"),
    hover tooltips, and "클릭" are all natural.
  - For **`responsive-web`**: prefer action-neutral words ("업로드", "선택") that work at both
    widths. When the interaction is structurally different at the two widths (drag-drop on desktop vs
    tap-to-pick on mobile), define two copy variants keyed to the breakpoint.
  - **The upload example** (canonical): "이미지를 여기에 올려주세요" is a desktop drag-drop
    instruction — it is WRONG on a mobile screen. Mobile correct: "사진 첨부" / "업로드" as a tap
    CTA; the dropzone metaphor does not exist on touch.
- **do/don'ts** — the sharp guardrails (don't say "오류가 발생했습니다" with no next step; don't use
  exclamation marks in error states; etc.).

## Part 2 — the strings (the `screens` map)

The frontmatter `screens` map is the real copy, keyed `screenId → region → string(s)`. Cover every
piece of text the build will render, **including state text**:

```yaml
screens:
  login:
    title: "다시 오신 걸 환영해요"
    subtitle: "계정에 로그인하세요"
    fields:
      email: { label: "이메일", placeholder: "you@example.com", error: "올바른 이메일을 입력해주세요" }
      password: { label: "비밀번호", helper: "8자 이상" }
    actions:
      submit: "로그인"
      forgot: "비밀번호를 잊으셨나요?"
    states:
      error: "이메일 또는 비밀번호가 올바르지 않아요"
  dashboard:
    title: "..."
    states:
      empty: "아직 활동이 없어요. 첫 거래를 시작해보세요."
      loading: "불러오는 중…"
```

Rules:
- **Real strings, the product's language.** If the audience/PRD is Korean, write Korean. No
  `Lorem ipsum`, no "Title"/"Label"/"Button", no English stand-ins for Korean UI.
- **Cover every confirmed screen id** (the coverage check fails otherwise) and every state that shows
  text. Pull which states exist from `prd-analysis.json`; write the message for each.
- **Derive strings from the PRD content + the voice.** Field names and data come from
  `prd-analysis.json`; the *wording* comes from the voice/tone system. This is the one place copy is
  written — the builder pulls these verbatim (reviewer D5 checks they match), so get them right here.
- Keep keys stable and descriptive so the builder can map `region → string` unambiguously.

## Why strings live here, not in the build
If the builder invented copy, you'd get inconsistent voice across screens and placeholder text slipping
into review. Centralizing strings in COPY.md makes the voice consistent by construction and lets D5
(content fidelity) check the canvas against a single source of truth. The builder's autonomy is over
*craft*, never over *copy*.
