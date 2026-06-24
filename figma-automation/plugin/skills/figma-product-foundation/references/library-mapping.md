# Library mapping — foundation decision → library token/variant, with gap escalation

The build is component-first and zero-raw-hex, so the foundation only counts if it's expressed in the
**target library's own tokens and variants**. This step binds each design-language decision to
something concrete in the library, and honestly flags what the library can't express.

## Inputs
- The **kit-investigation subagent's digest** (token spine + component families + gaps) and its 4–5
  `refs/` screenshots — not the raw catalog. Re-read the live library only to confirm a specific
  token/variant id before you bind it.
- `design-language.md`, `interaction-motion.md`, `brand-voice.md`.

## Map each decision

Walk the design-language profile and bind it:

| Foundation decision | Bind to | Notes |
|---|---|---|
| Color philosophy / accent rationing | color **token roles** (primary/surface/on-surface/border/error…) + light/dark **modes** | name the exact token roles to favor; don't pick raw hex |
| Density / spacing rhythm | the **spacing scale** tokens + which **component sizes/variants** (e.g. "use the `medium` density row, `large` only for primary CTAs") | density is mostly variant selection + spacing tokens |
| Typography system | the library's **text styles** mapped to roles (display/headline/body/label) | if the library lacks a needed level, flag it |
| Shape / radius language | **radius tokens** | pick the closest scale; note if the anchor's sharpness/softness isn't available |
| Iconography style | the library's **icon set / variants** | line vs filled — pick the matching variant family |
| Elevation strategy | **effect styles** or border tokens | tonal vs shadow — bind to what exists |
| Key components (button, input, card, nav, list row, modal…) | the **component + the specific variants** to favor for this aesthetic | this is the most useful output for the builder |

Write the bindings into `library-mapping.md` as a table the builder can act on directly: for each
role, the library token/component key (or stable name) and the variant to prefer.

## Gaps — be honest, escalate cheaply

When a foundation decision can't be expressed in the library, record a **gap** rather than inventing a
value. For each gap give the options, ranked:

1. **Closest token/variant** — the nearest thing the library does have (often fine; note the delta).
2. **Assemble from primitives** — compose the intent from existing components/tokens (e.g. a missing
   "stat row" built from a frame + existing text styles + divider token).
3. **Escalate** — the decision genuinely needs a value or component the library lacks and neither
   substitute is acceptable. Surface to the user with the trade-off.

Resolving gaps **now** is the whole reason this step is library-first: a gap found here costs one
question; the same gap found mid-build blocks a builder and burns a round. Record each gap in
`foundation.json.gaps[]` and in `library-mapping.md`; the orchestrator surfaces unresolved ones at the
Step 3 gate.

## Output contract for downstream

`foundation.json` must give the spec (Step 4) and builder (Step 5) a usable rollup: the `conceptRef`,
the token-role bindings, the favored component variants, the density/type/shape decisions, the
signature-layer bindings, and the gap list. Step 4's `DESIGN.md` token refs come straight from these
bindings — so if a binding is vague here, the spec will be vague too. Be specific: name tokens and
variants, not adjectives.
