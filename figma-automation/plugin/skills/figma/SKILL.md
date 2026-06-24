---
name: figma
description: "Unified entry point for the Figma workflow. Routes to /figma-redesign (re-skin an existing screen) and /figma-product (build a brand-new product from a PRD). Use whenever the user says /figma redesign or /figma create, asks to redesign a screen with a new library, asks to design/build screens from a PRD or spec, or references Figma + a redesign or greenfield-design intent."
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

> "`/figma <verb>` is not available. The active skill is `/figma redesign <library> --frame <id>` — a self-contained fresh-build redesign of one screen into a target library."
>
> "Previously available verbs (init, audit, report, diff, tokenize, design-md, annotate, brainstorm, flowchart, wireframe, refresh-cache, matching) are archived."

## Archived verb aliases (inform user, then offer redesign)

| Old verb | Response |
|---|---|
| `harvest`, `relibrary`, `rebuild` | Archived. Use `/figma redesign <library> --frame <id>` — it discovers the library live and builds fresh, no upstream pipeline needed. |
| `audit`, `violations`, `gaps`, `health`, `clean` | Archived. |
| `report` | Archived. |
| `diff` | Archived. |
| `tokenize` | Archived. |
| `annotate` | Archived. |
| `design-md` | Archived. |
| `design` | Archived. Use `/figma redesign`. |
| `init`, `list`, `use`, `doctor` | Archived. Project registry lives in `.claude/figma-projects.json` — read/edit directly. |
| `brainstorm`, `analyze`, `flowchart`, `wireframe` | Archived. |
| `refresh-cache`, `matching` | Archived. |
| `normalize`, `dream`, `swap-library`, `swap-hub` | Archived. |

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
