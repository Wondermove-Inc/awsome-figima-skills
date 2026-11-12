# Figma MCP Landscape (October 2026)

What changed around Figma MCP in 2026 and what it means for the skills in this
repository. Surveyed 2026-10-22.

## Two backends, different strengths

| | figma-mcp-express (this repo) | Official Figma MCP server |
| --- | --- | --- |
| Transport | Local Go server plus Desktop plugin over WebSocket; optional remote follower since 2.8.0 | Remote `https://mcp.figma.com/mcp` (write support), Desktop server for reads |
| Write model | Validated declarative `batch` ops, no script execution | `use_figma` runs Plugin API JavaScript |
| Quota | None | Starter and View/Collab seats: 6 calls per month; paid Dev/Full seats: per-minute limits; writes exempt |
| Variants | Consume and manage by name; cannot combine or add component properties | Full: `combineAsVariants`, component properties, slots, exposed instances |
| FigJam, Slides, Specs, code layers | No | Yes |
| Multi-file, multi-agent | Channels, presence roster, origin discipline | One file per call |

Use figma-mcp-express for high-volume screen building and redesign. Use the
official server for library authoring that needs the Plugin API, and for
FigJam, Slides, Specs, and code layers.

## Official Figma MCP timeline (2026)

- **March**: `use_figma` tool added, executing Plugin API code against the
  canvas: create, edit, delete nodes; create and bind variables; build
  components and variants; change auto layout.
- **Summer**: Slots (`createSlot`, `SLOT` component properties) documented in
  the `figma-use` skill; `generate_image` plus `upload_assets` for placeholder
  imagery.
- **October 6**: Figma Agent out of beta; custom skills available on Starter;
  generative plugins generally available; guidelines for design-library context.
- **October 14 to 15 (Config India)**: MCP generates code layers and works with
  Specs; faster server with fewer errors and lower token use; 20 new partner
  clients; code layers open beta; Specs open beta; centralized design systems
  preview.
- **Skills**: 16 skills bundled with the Figma plugin plus 2 standalone
  workflow skills. Community AI skills catalog at
  `figma.com/community/ai-skills`. See `docs/figma-official-skills.md`.

## figma-mcp-express timeline (2026)

- **2.6.0 (June 20)**: media and vector creation, dev resources, GLASS, NOISE,
  TEXTURE effects, progressive blur, GRID auto layout, min and max constraints,
  `set_text_range`, variable metadata management.
- **2.7.0 (June 24)**: `create_instance` accepts `componentKey` and
  auto-imports; `set_auto_layout` works on components and component sets;
  intent-based `search_batch_ops` categories; capability seed in MCP
  `instructions`; skill-gate PreToolUse hook; `visual-craft.md`.
- **2.7.1 (June 25)**: self-contained Codex and Claude plugin bundles; hook
  duplicate-loading fix; macOS marker path fix.
- **2.8.0 (July 11)**: remote follower mode (`--mode remote-follower`) with
  hardened transport.
- **2.8.1 (August 6)**: license simplified to plain MIT with upstream
  attribution; docs on auto-layout sizing, elevation hierarchy, SECTION
  coordinates.
- Component ops in the live catalog: `create_component`, `create_instance`,
  `set_instance_properties`, `swap_component`, `detach_instance`,
  `import_component_by_key`, `get_local_components`. No variant combining.

## What this repository changed in response

- Added the `figma-variants` skill with a backend matrix and recipes for
  authoring, auditing, renaming, extending, and migrating component sets.
- Added `scripts/sync-figma-official-skills.sh` and a catalog of the official
  skills so agents without the Claude Code or Cursor plugin can use them.
- The vendored `figma-mcp-express` folder should track upstream 2.8.1; the
  runtime already does because `.mcp.json` runs `npx -y figma-mcp-express`.

## Watch list

- An upstream `combine_as_variants` or component-property batch op in
  figma-mcp-express would let `figma-variants` drop the `use_figma` dependency.
- Figma's write-to-canvas is free during beta and planned to become usage-based.
- Code layers creation is free on paid plans through November 4, 2026.

## Sources

- Figma MCP server docs: https://developers.figma.com/docs/figma-mcp-server/
- Figma skills for MCP: https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP
- figma/mcp-server-guide: https://github.com/figma/mcp-server-guide
- Figma release notes: https://www.figma.com/release-notes/
- figma-mcp-express changelog: https://github.com/sunhome243/figma-mcp-express/blob/main/CHANGELOG.md
