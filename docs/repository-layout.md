# Repository Layout

This is a flat public repository. `figma-mcp-express/` is a git submodule of
<https://github.com/sunhome243/figma-mcp-express>; run
`git submodule update --init` after a plain clone.

```text
figma-mcp-express/     (submodule)
  cmd/ internal/        Go MCP server
  plugin/              Figma Desktop plugin source
  npm/                 npm package wrapper
  skills/              MCP usage skills

figma-automation/
  plugin/              Figma product-design skills and agents

qa-automation/
  plugin/              Design-fidelity QA skill and reviewer agent

.agents/plugins/
  marketplace.json     Codex marketplace entries for the plugin folders

.claude-plugin/
  marketplace.json     Claude Code marketplace entries for the same plugin folders

scripts/
  install.sh                      Codex plugin + agent installer
  sync-figma-official-skills.sh   Fetches Figma's official skills into vendor/ (git-ignored)

docs/
  figma-official-skills.md        Catalog of Figma's official MCP skills and install paths
  figma-mcp-landscape-2026.md     Backend comparison and 2026 timeline

vendor/figma-official-skills/     Local copy of Figma's skills (not tracked)
```

The repository intentionally tracks only source, plugin packages, and reusable
documentation that are safe to publish.
