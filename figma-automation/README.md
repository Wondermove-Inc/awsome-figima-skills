# Figma Automation Plugin Pack

Reusable Figma product-design skills and agents for Claude Code and Codex.

This folder is intentionally small. It contains the public plugin package only;
project-specific design-system data, memory, cached catalog exports, and local
agent runtime files are not part of this distribution.

## Contents

```text
plugin/
  .claude-plugin/      Claude Code plugin manifest
  .codex-plugin/       Codex plugin manifest
  agents/              Agent prompts for Figma build and review workflows
  codex-agents/        Codex agent TOML wrappers
  skills/              Figma product and redesign skills
```

## Main Skills

- `figma`: unified entry point for Figma workflows
- `figma-redesign`: redesign one existing Figma screen against a target system
- `figma-product`: greenfield PRD-to-product design workflow
- `figma-product-prd`: product research and requirement ingestion
- `figma-product-direction`: visual and product direction
- `figma-product-foundation`: design-system foundation setup
- `figma-product-spec`: build-ready design spec authoring
- `figma-product-build`: high-fidelity Figma screen build
- `figma-playbook`: memory and project workflow support
- `figma-visual-researcher`: visual research support for product builds

## Requirements

- `figma-mcp-express` must be installed and running for live Figma operations.
- Figma Desktop must have the `figma-mcp-express` plugin open in the target file.
- Some workflows may use local files for generated specs and temporary research assets.

## Codex Setup

From the repository root:

```bash
./scripts/stage-codex.sh
```

Restart Codex after staging.

## Claude Code Setup

From the repository root:

```bash
claude plugin marketplace add ./figma-automation/plugin
```

Restart Claude Code after installing or updating the plugin.

## Public Repo Policy

Do not add private Figma file exports, client design-system catalogs, local
memory folders, screenshots, or `.env` files to this folder. Keep those in a
private project repository.
