# Repository Instructions

This repository is a public, flat-source distribution for Figma automation
tools.

## Working Rules

- Keep changes scoped to the requested package or plugin.
- Prefer source-of-truth docs from current code, scripts, manifests, and config.
- Do not commit secrets, tokens, `.env` files, screenshots, browser snapshots, or generated QA reports.
- Do not commit generated build outputs such as `figma-mcp-express/bin/` or `figma-mcp-express/plugin/dist/`.
- Run relevant verification before claiming a change passes.
- Do not push release tags without explicit user approval.

## Layout

```text
figma-mcp-express/       Figma MCP server, Desktop plugin, npm package, skills
figma-automation/plugin/ Figma product-design skills and agents
qa-automation/plugin/    Design-fidelity QA skill and reviewer agent
docs/                    Repository-level public documentation
scripts/                 Local helper scripts
```

## Public Repository Constraints

This repository must stay safe to publish. Keep project-specific design-system
catalogs, local caches, and machine-specific agent configuration out of git.

`figma-mcp-express` is the open-source engine. `figma-automation` and
`qa-automation` are included as flat plugin folders for local agent use.
