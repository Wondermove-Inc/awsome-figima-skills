---
name: figma
description: Route Figma design tasks to figma-redesign or figma-product. Use for Figma redesign, design-system migration, PRD-to-Figma, or greenfield screen creation.
---

# /figma — Figma Workflow Entry Point

Router skill. Active sub-skills:
- **figma-redesign** — reinterpret ONE existing screen into a target library (original frame exists).
- **figma-product** — build a brand-new multi-screen product FROM a PRD (no original; the suite
  ingests the PRD, researches a design foundation, authors DESIGN.md + COPY.md, then builds).
- **figma-visual-researcher** — support skill used by `figma-product` to prefetch 2024+ UI/UX
  references and concrete brand/icon/image/avatar/Lottie assets, then actively resolve missing media
  during build. It writes files/JSON only; builders consume its local paths.

## Trigger

```
/figma redesign <library> --frame <id>            → redesign one existing screen with target library
/figma redesign <library> --frame <id1,id2,...>   → multiple screens, serial
/figma create <prd-path> --library <url-or-key>   → build a new product from a PRD (greenfield)
```

Pick by what exists: an **existing frame to re-skin** → `redesign`; a **PRD/spec with no screens yet**
→ `create`.

If the user types `/figma` with any other verb, respond with a redirect:

> "`/figma <verb>` is not available. Use `/figma redesign <library> --frame <id>` for an existing screen or `/figma create <prd-path> --library <url-or-key>` for a PRD-to-Figma product build."

## REDESIGN FLOW

Extract the target library (Figma file URL or subscribed library key) and `--frame <id>` from args.

If no target library or no `--frame`:
> "Provide the target library and frame: `/figma redesign <library-url> --frame <node-id>`"

Invoke `Skill('figma-redesign')` with all args.

## CREATE FLOW

Extract the PRD path (file or folder) and `--library <url-or-key>` from args.

If no PRD path or no `--library`:
> "Provide the PRD and target library: `/figma create <prd-path> --library <library-url>`"

Invoke `Skill('figma-product')` with all args. It orchestrates the four step skills
(`figma-product-prd` → `figma-product-foundation` → `figma-product-spec` → `figma-product-build`).
Its product pipeline includes a `visual-researcher` lane, not extra numbered steps: the PRD hook records
likely visual needs, the foundation hook prefetches reference packs, the spec hook prefetches concrete
assets where the spec makes them visible, and the build hook actively dispatches `visual-researcher` if
a builder reports missing media.
