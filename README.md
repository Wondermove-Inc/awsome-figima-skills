# Awesome Figma Skills

Agent-ready Figma automation for Codex: a live Figma MCP server, product-design
skills, and implementation-fidelity QA workflows in one public repository.

Use this repo when you want a coding agent to inspect Figma, build real Figma
screens, run component-first redesign workflows, or compare a live app against a
Figma design.

## What Is Included

| Package | What it provides |
| --- | --- |
| `figma-mcp-express` | Local MCP server plus Figma Desktop plugin for live Figma read/write automation. |
| `figma-automation` | Codex skills for one-screen redesign, PRD-to-product design, visual research, Figma build gates, and reusable design memory. |
| `qa-automation` | Codex skill for design-fidelity QA between a running app and a mapped Figma frame. |

The default setup is Codex-first and uses `figma-mcp-express` as the Figma MCP
backend. Development-only MCP server names such as `figma-mcp-express-dev` are
not required for normal users.

## Install

Clone the repository, then run one installer:

```bash
git clone https://github.com/Wondermove-Inc/awsome-figima-skills.git
cd awsome-figima-skills
./scripts/install.sh
```

The installer adds the Codex marketplace, installs the Figma MCP, Figma
automation, and design-QA plugins, and activates the reusable Codex subagents
used by those workflows. Start a new Codex thread after installation so the
skills, MCP server config, and agents are loaded.

## Figma Desktop Setup

Install the Figma Desktop plugin from:

```text
figma-mcp-express/plugin/manifest.json
```

Keep the Figma Desktop plugin open while an agent is working. Most workflows
need a live Desktop connection to read or edit the active Figma file.

For direct MCP server usage outside the Codex plugin install, run:

```bash
npx -y figma-mcp-express --port 1994
```

## Usage

Invoke the installed skills from Codex:

```text
$figma-redesign redesign this frame into our target library
$figma-product turn this PRD into a high-fidelity Figma product
$design-qa compare this route against the mapped Figma screen
```

The workflows are intentionally gated:

- Figma writes go through `figma-mcp-express`.
- Builders use component-first construction, bound tokens, dynamic auto layout,
  and local craft rules.
- Reviewers separate objective structural checks from craft/function checks.
- Design-QA uses bounded Figma reads and local Playwright snapshots.

## Repository Layout

```text
.
├── .agents/plugins/          # Codex marketplace entry
├── figma-mcp-express/        # MCP server, Figma Desktop plugin, MCP docs
├── figma-automation/plugin/  # Figma product-design skills and agent prompts
├── qa-automation/plugin/     # Design-QA skill, reviewer prompt, snapshot scripts
└── docs/                     # Installation, layout, and security notes
```

This is a flat source distribution. The `figma-automation` and `qa-automation`
folders stay flat; `figma-mcp-express` remains its own open-source package.

## Docs

- [Installation](docs/installation.md)
- [Repository layout](docs/repository-layout.md)
- [Security](docs/security.md)
- [Figma MCP Express](figma-mcp-express/README.md)
- [Figma MCP tools](figma-mcp-express/TOOLS.md)

## Security

Do not commit Figma tokens, `.env` files, browser snapshots, screenshots from
authenticated apps, generated QA reports, or project-specific design-system
catalogs. Design-QA snapshots can contain private UI data and should stay in
ignored temporary folders such as `.tmp/design-qa/`.

## License

MIT. See [LICENSE](LICENSE).
