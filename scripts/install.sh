#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
marketplace_url="${AWESOME_FIGMA_SKILLS_REPO:-https://github.com/Wondermove-Inc/awsome-figima-skills.git}"
marketplace_name="${AWESOME_FIGMA_SKILLS_MARKETPLACE:-awesome-figma-skills}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
agents_dir="$codex_home/agents"

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found in PATH" >&2
  exit 1
fi

codex plugin marketplace add "$marketplace_url" 2>/dev/null || true
codex plugin add "figma-mcp-express@$marketplace_name"
codex plugin add "figma-automation@$marketplace_name"
codex plugin add "qa-automation@$marketplace_name"

mkdir -p "$agents_dir"
cp "$repo_root"/figma-automation/plugin/codex-agents/*.toml "$agents_dir"/
cp "$repo_root"/qa-automation/plugin/codex-agents/*.toml "$agents_dir"/

echo "Installed Awesome Figma Skills plugins and Codex agents."
echo "Restart Codex or start a new Codex thread before using the skills."
