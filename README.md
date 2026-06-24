# Awesome Figma Skills

Production-ready Figma automation tools for coding agents.

This repository is a public, flat-source distribution. It combines the
`figma-mcp-express` MCP server with two agent plugin packs:

| Path | Purpose |
| --- | --- |
| `figma-mcp-express/` | Local Figma MCP server and Desktop plugin for live Figma read/write automation. |
| `figma-automation/plugin/` | Product-design and Figma build skills for Claude Code and Codex. |
| `qa-automation/plugin/` | Design-fidelity QA skill and reviewer agent for comparing a live app against Figma. |

The old umbrella repository used git submodules. This public repository does
not: every included file is tracked directly so users can clone it normally.

## Quick Start

### Figma MCP Express

Install the MCP server from npm or from the plugin marketplace, then import the
Figma Desktop plugin.

```bash
npx -y figma-mcp-express --port 1994
```

For full setup, build, release, and tool details, see:

- [figma-mcp-express/README.md](figma-mcp-express/README.md)
- [figma-mcp-express/DEV-SETUP.md](figma-mcp-express/DEV-SETUP.md)
- [figma-mcp-express/TOOLS.md](figma-mcp-express/TOOLS.md)

### Agent Skills

The plugin packs are kept as plain folders:

```text
figma-automation/plugin/
qa-automation/plugin/
```

For Codex, mirror the skills and agents into the local Codex scan directories:

```bash
./scripts/stage-codex.sh
```

For Claude Code, add each plugin folder as a local marketplace plugin:

```bash
claude plugin marketplace add ./figma-automation/plugin
claude plugin marketplace add ./qa-automation/plugin
```

## Repository Hygiene

- Do not commit Figma tokens, `.env` files, screenshots, browser snapshots, or generated QA reports.
- Keep project-specific design-system data out of this public repository unless it is explicitly sanitized.
- Keep generated builds out of git. `figma-mcp-express/plugin/dist/` and `figma-mcp-express/bin/` are build outputs.
- Tag pushes can trigger release automation under `figma-mcp-express/.github/workflows/`; only push release tags intentionally.

## Docs

- [docs/installation.md](docs/installation.md)
- [docs/repository-layout.md](docs/repository-layout.md)
- [docs/security.md](docs/security.md)

## License

MIT. See [LICENSE](LICENSE).
