# QA Automation Plugin Pack

Design-fidelity QA skills and agents for comparing a live rendered application
against its Figma design.

This public distribution contains only the reusable plugin package. Project
manifests, screenshots, browser snapshots, reports, and product knowledge bases
belong in the project repository that owns that data.

## Contents

```text
plugin/
  .claude-plugin/      Claude Code plugin manifest
  .codex-plugin/       Codex plugin manifest
  agents/              Design QA reviewer agent
  codex-agents/        Codex agent TOML wrapper
  skills/design-qa/    Design-fidelity QA skill and snapshot scripts
```

## Requirements

- Python 3
- Playwright with Chromium installed
- A running local application to inspect
- Figma design coordinates for the target screens

Install the browser dependency in your active Python environment:

```bash
pip install playwright
playwright install chromium
```

## Codex Setup

Install from the public repository marketplace:

```bash
codex plugin marketplace add https://github.com/Wondermove-Inc/awsome-figima-skills.git
codex plugin add qa-automation@awesome-figma-skills
```

Start a new Codex thread after installation.

## Claude Code Setup

From the repository root:

```bash
claude plugin marketplace add ./qa-automation/plugin
```

Restart Claude Code after installing or updating the plugin.

## Artifact Safety

Design QA snapshots can contain authenticated UI data. Write them to ignored
temporary folders, keep them out of git, and delete them after review.
