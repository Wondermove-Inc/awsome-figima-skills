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

Add this repository as a Codex marketplace, then install the plugins:

```bash
codex plugin marketplace add <REPO>
codex plugin add figma-mcp-express@awesome-figma-skills
codex plugin add figma-automation@awesome-figma-skills
codex plugin add qa-automation@awesome-figma-skills
```

Replace `<REPO>` with the absolute path to this checkout. Start a new Codex
thread after installation so the bundled skills appear in the prompt.

## Claude Code Plugins

Register the local plugin folders:

```bash
claude plugin marketplace add ./figma-automation/plugin
claude plugin marketplace add ./qa-automation/plugin
```

Restart Claude Code after installing or updating local plugins.

## Optional Figma Token

Most live Figma operations do not need a token. `FIGMA_TOKEN` is only needed
for REST-backed library catalog reads such as `fetch_library_catalog`.

Never commit `FIGMA_TOKEN` or any `.env` file.
