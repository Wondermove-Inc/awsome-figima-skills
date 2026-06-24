---
voice: "<the product's personality in one sentence — from foundation/brand-voice.md>"
tone:
  success: "<warm, brief>"
  error: "<plain, blame-free, actionable>"
  empty: "<encouraging, points to next action>"
  destructive: "<serious, clear>"
terminology:
  prefer: ["<term>", "<term>"]
  avoid: ["<banned term>", "<banned term>"]
patterns:
  buttonLabels: "verbs, sentence case"
  numbers: "<currency/date/number formatting rule>"
  lengthLimits: { button: 12, helper: 48 }
screens:
  # screenId -> regions -> real strings. Cover every confirmed screen and every state that shows text.
  <screen-id>:
    title: "<real string>"
    subtitle: "<real string>"
    fields:
      <field>: { label: "<>", placeholder: "<>", helper: "<>", error: "<>" }
    actions:
      <action>: "<real label>"
    states:
      empty: "<real message>"
      error: "<real message>"
---

# Copy System — <Product>

## Voice
<Expand the one-liner: who the product sounds like, what it never does.>

## Tone by context
- **Success:** <rule + example>
- **Error:** <rule + example>
- **Empty:** <rule + example>
- **Destructive confirm:** <rule + example>

## Terminology
<Glossary table: preferred term → meaning; banned term → use-instead.>

## Microcopy patterns
- Buttons: <rule>
- Numbers / currency / dates: <rule>
- Capitalization & punctuation: <rule>
- Length limits: <rule>

## Do's and Don'ts
- Do <...>
- Don't <...>
