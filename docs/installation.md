# Installation

## Figma MCP Express

Install and run the Figma backend from the
[Figma MCP Express repository](https://github.com/sunhome243/figma-mcp-express#readme).
Keep the Figma Desktop plugin open while an agent is working. Most tools need a
live Desktop plugin connection to read or edit the current Figma file.

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
`figma-automation` and `qa-automation` use `local` sources with paths relative
to the repository root. `figma-mcp-express` lives in its own repository (tracked
here as a git submodule), so its entry uses a Git source
(`{ "source": "url", "url": "...", "ref": "main" }`) and installs without
needing submodules. The default Codex install does not need a project-level
`.mcp.json`; the `figma-mcp-express` plugin provides its MCP server config.

## Claude Code Plugins

This repository also exposes a Claude Code marketplace at
`.claude-plugin/marketplace.json`. From Claude Code, add the marketplace and
install the three plugins:

```text
/plugin marketplace add Wondermove-Inc/awsome-figima-skills
/plugin install figma-mcp-express@awesome-figma-skills
/plugin install figma-automation@awesome-figma-skills
/plugin install qa-automation@awesome-figma-skills
```

For non-interactive setup, use the equivalent Claude Code CLI commands:

```bash
claude plugin marketplace add Wondermove-Inc/awsome-figima-skills
claude plugin install figma-mcp-express@awesome-figma-skills
claude plugin install figma-automation@awesome-figma-skills
claude plugin install qa-automation@awesome-figma-skills
```

Each plugin keeps its own `.claude-plugin/plugin.json`. `figma-automation` and
`qa-automation` use relative-path sources. `figma-mcp-express` uses a
`{ "source": "github", "repo": "sunhome243/figma-mcp-express", "ref": "main" }`
source, so it installs straight from its own repository and does not depend on
the git submodule being fetched.

## Updating The Engine Pin

`figma-mcp-express/` is a git submodule. To move it to a newer upstream commit:

```bash
git submodule update --remote figma-mcp-express
git add figma-mcp-express
git commit -m "chore: bump figma-mcp-express"
```

The marketplace entries track upstream `main`; pin a release by setting `ref`
to a tag or `sha` to a full commit hash in both marketplace files.

Claude Code plugin skills are namespaced by plugin. Example invocations:

```text
/figma-automation:figma-redesign redesign this frame into our target library
/figma-automation:figma-product turn this PRD into a high-fidelity Figma product
/figma-automation:figma-variants audit the Button component set
/qa-automation:design-qa compare this route against the mapped Figma screen
```

## Other AI Coding Agents

Agents without Codex or Claude Code plugin support can import the skills
directly from their `SKILL.md` files. Keep each skill's sibling `references/`,
`scripts/`, `assets/`, and `agents/` folders with it so linked instructions and
helper scripts still resolve.

Recommended entry points:

- [Figma router](../figma-automation/plugin/skills/figma/SKILL.md)
- [Figma redesign](../figma-automation/plugin/skills/figma-redesign/SKILL.md)
- [Figma product pipeline](../figma-automation/plugin/skills/figma-product/SKILL.md)
- [Figma playbook memory](../figma-automation/plugin/skills/figma-playbook/SKILL.md)
- [Figma visual researcher](../figma-automation/plugin/skills/figma-visual-researcher/SKILL.md)
- [Figma variants](../figma-automation/plugin/skills/figma-variants/SKILL.md)
- [Design QA](../qa-automation/plugin/skills/design-qa/SKILL.md)

## Official Figma Skills

Variant authoring (combining components into a set, component properties,
slots), FigJam, Slides, Specs, and code layers need Figma's official MCP server
and its bundled skills. Claude Code users install `figma@claude-plugins-official`;
Cursor users run `/add-plugin figma`; other agents can fetch the skill folders
locally:

```bash
./scripts/sync-figma-official-skills.sh            # into vendor/figma-official-skills/ (git-ignored)
./scripts/sync-figma-official-skills.sh ~/.codex/skills/figma-official
```

See [Official Figma skills](figma-official-skills.md) for the catalog and
plan/seat requirements.

## Optional Figma Token

Most live Figma operations do not need a token. `FIGMA_TOKEN` is only needed
for REST-backed library catalog reads such as `fetch_library_catalog`.

Never commit `FIGMA_TOKEN` or any `.env` file.
