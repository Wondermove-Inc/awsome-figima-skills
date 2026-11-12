# Official Figma Skills

Figma ships its own agent skills with the official Figma MCP server. They are
maintained in [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide)
and are governed by the
[Figma Developer Terms](https://www.figma.com/legal/developer-terms/), not an
open-source license, so this repository does not vendor them. Use the install
path for your agent below, then combine them with the workflow skills here.

Surveyed 2026-10-22 (plugin version 2.2.157, repository pushed 2026-10-20).

## Install

| Agent | Command |
| --- | --- |
| Claude Code | `claude plugin install figma@claude-plugins-official` |
| Cursor | `/add-plugin figma` |
| Gemini CLI | `gemini extensions install https://github.com/figma/mcp-server-guide` |
| Codex and other agents | `./scripts/sync-figma-official-skills.sh [target-dir]` then point the agent's skill loader at the folder (default `vendor/figma-official-skills/`, git-ignored) |

All of them talk to the remote server `https://mcp.figma.com/mcp`. Writing to
the canvas (`use_figma`) is remote-server only and needs edit access to the
file. Figma caps Starter plans and View/Collab seats at 6 tool calls per month;
Dev/Full seats on paid plans get per-minute limits, and write tools are exempt.

## Skill catalog

| Skill | Purpose | Needs |
| --- | --- | --- |
| `figma-use` | Mandatory prerequisite for every `use_figma` call. Plugin API rules, component and variant patterns, variable patterns, validation and recovery. | Design file, edit access |
| `figma-generate-design` | Build full screens, modals, panels, and other composed UI from code or a description using the connected design system. | Design file, design system |
| `figma-generate-library` | Build or update a design system: variable collections, component sets with variants and properties, theming, reconciliation. Ships `createComponentWithVariants.js`. | Codebase, design file |
| `figma-design-to-code` | Mandatory prerequisite for `get_design_context`; implements a selected frame in code. | Frame URL |
| `figma-code-connect` | Create and maintain Code Connect template files mapping components to code. | Published components, paid plan |
| `figma-code-workflows` | Import local HTML or project files into Figma as design frames, code layers, or Make files. | Edit access, Full seat for code layers |
| `figma-create-new-file` | Create a blank Design, FigJam, or Slides file. | Account |
| `figma-generate-diagram` | Turn a description of a system or flow into an editable FigJam diagram. | FigJam |
| `figma-use-figjam` | `use_figma` in the FigJam context: stickies, sections, connectors, tables. | FigJam, edit access |
| `figma-use-slides` | `use_figma` in the Slides context: slides, themes, speaker notes. | Slides, edit access |
| `figma-use-motion` | Animate nodes with keyframes, animation styles, easing. | Design file |
| `figma-implement-motion` | Translate Figma motion into production animation code. | Frame URL |
| `figma-spec` | Create, read, edit, and comment on Figma Specs (PRDs, briefs, requirements). | Spec URL or file |
| `figma-swiftui` | Bidirectional SwiftUI and Figma translation. | Frame URL |
| `figma-shaders` | Create or update shader effects. | Design file |
| `figma-generative-plugins` | Create or update generative plugins. | Design file |
| `workflow-skills/generate-project-plan` | PRD plus codebase context into a FigJam project plan board. | FigJam |
| `workflow-skills/video-interaction-mapper` | UI recordings into annotated Figma storyboards. | Design file |

## How they fit this repository

- Variant authoring (`combineAsVariants`, component properties, slots) is only
  available through `use_figma`. The `figma-variants` skill in this repository
  decides between that path and the figma-mcp-express fallback.
- Screen building and redesign stay on figma-mcp-express: no quota, no seat
  requirement, direct Desktop plugin bridge.
- FigJam and Slides are not supported by figma-mcp-express; use the official
  skills for those surfaces.
- Load only the official skill you need per call; the `figma-use` references
  alone are large.
