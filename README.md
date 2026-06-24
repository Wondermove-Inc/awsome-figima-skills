# Awesome Figma Skills

Build, redesign, and QA real Figma screens with AI coding agents.

Awesome Figma Skills packages a live Figma MCP backend, production design
workflows, reusable agent prompts, and implementation-fidelity QA into one
public plugin distribution for AI coding agents.

Use it when you want an agent to do more than call raw Figma tools:

- inspect and edit a live Figma file through `figma-mcp-express`
- redesign an existing screen into a target design-system library
- turn a PRD into high-fidelity Figma product screens
- keep reusable design memory across libraries and projects
- compare a running app route against a mapped Figma frame

## Why This Exists

Raw Figma MCP tools are powerful, but production design work needs a workflow:
bounded reads, component discovery, token binding, visual references, reviewer
gates, and safe local artifacts. This repository turns those practices into
installable plugins and skills.

The default backend is `figma-mcp-express`. Development-only server names such
as `figma-mcp-express-dev` are not required for normal users.

## Quick Start: Codex

Clone the repository, then run one installer:

```bash
git clone https://github.com/Wondermove-Inc/awsome-figima-skills.git
cd awsome-figima-skills
./scripts/install.sh
```

The installer adds this repository as a Codex plugin marketplace, installs the
Figma MCP, Figma automation, and design-QA plugins, and activates the reusable
Codex subagents used by those workflows.

Start a new Codex thread after installation so the skills, MCP server config,
and agents are loaded.

## Quick Start: Claude Code

This repository also includes Claude Code plugin manifests. From Claude Code,
add the marketplace and install the same three plugins:

```text
/plugin marketplace add Wondermove-Inc/awsome-figima-skills
/plugin install figma-mcp-express@awesome-figma-skills
/plugin install figma-automation@awesome-figma-skills
/plugin install qa-automation@awesome-figma-skills
```

For non-interactive setup, Claude Code also exposes equivalent CLI marketplace
commands:

```bash
claude plugin marketplace add Wondermove-Inc/awsome-figima-skills
claude plugin install figma-mcp-express@awesome-figma-skills
claude plugin install figma-automation@awesome-figma-skills
claude plugin install qa-automation@awesome-figma-skills
```

## Figma MCP Setup

Install and run the Figma backend from the
[Figma MCP Express repository](https://github.com/sunhome243/figma-mcp-express#readme).
Keep the Figma Desktop plugin open while an agent is working. Most live Figma
workflows require the target file to be open in Figma Desktop with the plugin
running.

Figma MCP Express talks directly to the local Figma Desktop file, avoiding
official MCP service quotas and keeping high-volume automation responsive.

## Other AI Coding Agents

Agents without Codex or Claude Code plugin support can use this repository as a
skill-file distribution. Import the relevant `SKILL.md` files into the agent's
own skill or instruction system, keeping each skill's sibling `references/`,
`scripts/`, `assets/`, and `agents/` folders with it.

Start with the router skill for broad Figma work, then add the workflow skills
you need:

- [Figma router](figma-automation/plugin/skills/figma/SKILL.md)
- [Figma redesign](figma-automation/plugin/skills/figma-redesign/SKILL.md)
- [Figma product pipeline](figma-automation/plugin/skills/figma-product/SKILL.md)
- [Figma playbook memory](figma-automation/plugin/skills/figma-playbook/SKILL.md)
- [Figma visual researcher](figma-automation/plugin/skills/figma-visual-researcher/SKILL.md)
- [Design QA](qa-automation/plugin/skills/design-qa/SKILL.md)

## Core Workflows

| Workflow                  | Use it for                                               | What makes it production-oriented                                                        |
| ------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `figma-redesign`          | Rebuild one existing Figma screen into a target library. | Inventory-first rebuild, component-key checks, mechanical pre-gate, two-verifier review. |
| `figma-product`           | Turn a PRD into a high-fidelity Figma product.           | PRD parsing, direction, foundation, spec, canon screen, gated build fan-out.             |
| `figma-playbook`          | Load, apply, reflect, and consolidate design memory.     | Library/project/global memory stores with proposal-based writes.                         |
| `figma-visual-researcher` | Fetch current UI references and assets.                  | Structured request validation, source-year constraints, ranked candidates.               |
| `design-qa`               | Compare a live app route against Figma.                  | Screen mapping, Playwright snapshots, bounded Figma reads, structured reports.           |

Codex example prompts:

```text
$figma-redesign redesign this frame into our target library
$figma-product turn this PRD into a high-fidelity Figma product
$design-qa compare this route against the mapped Figma screen
```

Claude Code plugin skills are namespaced by plugin:

```text
/figma-automation:figma-redesign redesign this frame into our target library
/figma-automation:figma-product turn this PRD into a high-fidelity Figma product
/qa-automation:design-qa compare this route against the mapped Figma screen
```

## How It Works

```text
AI coding agent
  -> Figma automation skills
  -> reusable subagents
  -> figma-mcp-express
  -> Figma Desktop plugin
  -> live Figma file

AI coding agent
  -> design-qa skill
  -> Playwright snapshot
  -> Figma frame comparison
  -> screen-keyed report
```

The workflows are intentionally gated:

- Figma writes go through `figma-mcp-express`.
- Builders use component-first construction, bound tokens, dynamic auto layout,
  and local craft rules.
- Reviewers separate objective structural checks from craft/function checks.
- Design-QA uses bounded Figma reads and local Playwright snapshots.
- Long instructions live in `references/`; repeated deterministic work lives in
  `scripts/`; `SKILL.md` files stay lean.

## Included Packages

| Package             | What it provides                                                                                                  |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `figma-mcp-express` | Local MCP server plus Figma Desktop plugin for live Figma read/write automation.                                  |
| `figma-automation`  | Agent skills for redesign, PRD-to-product design, visual research, Figma build gates, and reusable design memory. |
| `qa-automation`     | Design-fidelity QA skill for comparing a running app and a mapped Figma frame.                                    |

## Repository Layout

```text
.
├── .agents/plugins/          # Codex marketplace entry
├── .claude-plugin/           # Claude Code marketplace entry
├── figma-mcp-express/        # MCP server, Figma Desktop plugin, MCP docs
├── figma-automation/plugin/  # Figma product-design skills and agent prompts
├── qa-automation/plugin/     # Design-QA skill, reviewer prompt, snapshot scripts
└── docs/                     # Installation, layout, and security notes
```

This is a flat source distribution. The `figma-automation` and `qa-automation`
folders stay flat; `figma-mcp-express` remains its own open-source package.

## Security And Local Data

Do not commit Figma tokens, `.env` files, browser snapshots, screenshots from
authenticated apps, generated QA reports, or project-specific design-system
catalogs. Design-QA snapshots can contain private UI data and should stay in
ignored temporary folders such as `.tmp/design-qa/`.

`FIGMA_TOKEN` is optional and only needed for REST-backed library catalog reads.
Most live Desktop-plugin workflows do not need it.

## Docs

- [Installation](docs/installation.md)
- [Repository layout](docs/repository-layout.md)
- [Security](docs/security.md)
- [Figma MCP Express](https://github.com/sunhome243/figma-mcp-express#readme)
- [Figma MCP tools](https://github.com/sunhome243/figma-mcp-express/blob/main/TOOLS.md)

## License

MIT. See [LICENSE](LICENSE).
