# Repository Layout

This is a flat public repository.

```text
figma-mcp-express/
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
```

The repository intentionally tracks only source, plugin packages, and reusable
documentation that are safe to publish.
