---
name: figma
description: Route Figma design tasks to figma-redesign, figma-product, or figma-variants. Use for Figma redesign, design-system migration, PRD-to-Figma, greenfield screen creation, or component-set / variant authoring and cleanup.
---

# /figma — Figma Workflow Entry Point

Router skill. Active sub-skills:
- **figma-redesign** — reinterpret ONE existing screen into a target library (original frame exists).
- **figma-product** — build a brand-new multi-screen product FROM a PRD (no original; the suite
  ingests the PRD, researches a design foundation, authors DESIGN.md + COPY.md, then builds).
- **figma-visual-researcher** — support skill used by `figma-product` to prefetch 2024+ UI/UX
  references and concrete brand/icon/image/avatar/Lottie assets, then actively resolve missing media
  during build. It writes files/JSON only; builders consume its local paths.
- **figma-variants** — author or manage a COMPONENT_SET: variant axes, component properties, slots,
  audits, renames, instance migration. Picks between the official `use_figma` backend (full
  authoring) and the figma-mcp-express fallback (consume + name-based management only).

## Trigger

```
/figma redesign <library> --frame <id>            → redesign one existing screen with target library
/figma redesign <library> --frame <id1,id2,...>   → multiple screens, serial
/figma create <prd-path> --library <url-or-key>   → build a new product from a PRD (greenfield)
/figma variants author|manage|audit|migrate <...>  → component sets, variant axes, component properties
```

Pick by what exists: an **existing frame to re-skin** → `redesign`; a **PRD/spec with no screens yet**
→ `create`; a **component set to build, extend, audit, or migrate** → `variants`.

If the user types `/figma` with any other verb, respond with a redirect:

> "`/figma <verb>` is not available. Use `/figma redesign <library> --frame <id>` for an existing screen, `/figma create <prd-path> --library <url-or-key>` for a PRD-to-Figma product build, or `/figma variants <author|manage|audit|migrate> ...` for component-set work."

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

## VARIANTS FLOW

Extract the sub-verb (`author`, `manage`, `audit`, `migrate`) and its target ids from args.

If no sub-verb or no target:
> "Provide the action and target: `/figma variants author <frame-ids|spec>`, `/figma variants manage <set-id> <change>`, `/figma variants audit <set-id>`, or `/figma variants migrate <old-set-id> <new-set-id>`"

Invoke `Skill('figma-variants')` with all args. It decides the backend first: the official Figma MCP
`use_figma` tool for combining and component properties, figma-mcp-express for everything that can be
done by naming and instance ops, and an explicit user hand-off for the combine step when `use_figma`
is unavailable.
