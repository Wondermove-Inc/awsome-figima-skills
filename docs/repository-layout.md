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

scripts/
  stage-codex.sh       Mirrors local plugin skills and agents into Codex
```

The old private umbrella setup used submodules and project-specific data. This
public repository intentionally tracks only the source, plugin, and reusable
documentation that are safe to publish.
