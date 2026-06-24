# Audience research — PRD → who this is for and how they think

The look serves the user, so you have to know the user before you choose the look. This is light UX
research, grounded in the PRD (not invented), enriched with general knowledge of the audience segment.

This research is written into the **`audience` block of `prd-analysis.json`** — the single canonical
home (the schema *requires* it). Step 2 (Direction) reads this block + the per-screen purpose/register
to ground its art direction, so the audience must be settled before any aesthetic choice is made.

## Extract from the PRD

Read `prd-analysis.json` `product`, `actors`, and any REFERENCE docs. Pull:

- **Primary persona(s)** — who actually uses this most. If the PRD names personas, use them; else
  infer from the actors and the product goal. Keep it to 1–2 primary personas, not a gallery.
- **Demographics that affect design** — age band, gender skew, region/locale (a Korean app's audience
  carries different conventions than a US one), tech-savviness. Only capture what changes a design
  decision; don't profile for its own sake.
- **Usage context** — where and how they use it: phone on the go vs desktop at a desk, glance vs deep
  session, one-handed vs two, high-stress (finance, health) vs leisure. Context drives density, tap
  target size, and motion restraint.
- **Mental model** — the metaphors and expectations the user already holds. What apps have trained
  them? What do they expect a "transfer" or a "dashboard" or a "feed" to feel like? Designing with the
  grain of an existing mental model reduces cognitive load; fighting it raises it.
- **Accessibility needs** — contrast and text-size sensitivity, motion sensitivity (reduced-motion),
  one-handed reach, color-blind-safe status signaling. Note any the audience plausibly needs.
- **Jobs-to-be-done** — the top 3 things the user is hiring this product to accomplish, phrased as
  outcomes ("know my balance is safe in 2 seconds"), not features. The aesthetic should make the top
  jobs feel effortless.

## Write the `audience` block of `prd-analysis.json`

Fold the findings into the schema's `audience` object (the canonical home — there is no separate
`audience.md`). Field mapping:

| Schema field | What goes in it |
|---|---|
| `primaryPersona` | the 1–2 primary personas — role + who they actually are |
| `ageContext` | age band / locale / tech-savviness + usage context (device, setting, session length, stress level) |
| `mentalModel` | which apps/experiences trained them; what they expect a "transfer"/"dashboard"/"feed" to feel like; the friction to avoid |
| `accessibilityNeeds` | contrast/text-size sensitivity, reduced-motion, one-handed reach, color-blind-safe status — each as a list entry |
| `jobsToBeDone` | the top 3 outcomes (phrased as outcomes, not features), ranked |

Capture only what changes a design decision — don't profile for its own sake. Surface as a
`[NEEDS INPUT]` openQuestion only the pieces that genuinely gate a product decision and the PRD leaves
blank; everything else is derived-and-recorded, not asked.

### Design implications — the bridge to Step 2

While researching, note the **design implications** — the constraint set the art direction must
satisfy (e.g. "high-stress finance + glanceable → calm, high-contrast, low-motion, generous spacing";
"one-handed mobile → primary actions in thumb reach, large tap targets"). You don't choose the look
here (that's Step 2), but these implications are what Direction must defend its choices against, so
make them legible — fold the sharpest ones into `jobsToBeDone` / `accessibilityNeeds` and, where they
shape a screen's energy, into that screen's initial `register`. Direction reads the audience block +
purpose/register map and grounds every aesthetic move on them, not on "looks nice".
