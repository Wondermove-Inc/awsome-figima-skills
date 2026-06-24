# Installation

## Figma MCP Express

Run the MCP server with npm:

```bash
npx -y figma-mcp-express --port 1994
```

Then import the Figma Desktop plugin from
`figma-mcp-express/plugin/manifest.json` or from the release `plugin.zip`.

Keep the Figma plugin open while an agent is working. Most tools need a live
Desktop plugin connection to read or edit the current Figma file.

## Codex Plugins

Clone the public repository, then run one installer:

```bash
git clone https://github.com/Wondermove-Inc/awsome-figima-skills.git
cd awsome-figima-skills
./scripts/install.sh
```

Start a new Codex thread after installation so the bundled skills and MCP server
appear in the prompt. The installer adds the marketplace, installs the plugins,
and activates the reusable Codex subagents used by the skills.

This repository exposes Codex plugins through `.agents/plugins/marketplace.json`.
The plugin `source.path` values are relative to the repository root, which is
the expected layout for Git-backed marketplaces. The default Codex install does
not need a project-level `.mcp.json`; the `figma-mcp-express` plugin provides
its MCP server config.

## Optional Figma Token

Most live Figma operations do not need a token. `FIGMA_TOKEN` is only needed
for REST-backed library catalog reads such as `fetch_library_catalog`.

Never commit `FIGMA_TOKEN` or any `.env` file.
