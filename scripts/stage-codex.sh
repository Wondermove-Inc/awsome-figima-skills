#!/usr/bin/env bash
#
# stage-codex.sh - mirror the local plugin packs into Codex's scan dirs.
#
# Codex does NOT auto-expose skills from a *local* marketplace; it scans
# ~/.codex/skills (skills) and ~/.codex/agents (agents). So the two local
# plugins (figma-automation, qa-automation) are copied into those locations.
# figma-mcp-express is an MCP server/plugin dependency and is not staged here.
#
# No path rewriting is needed: skill/agent script paths use a runtime-neutral
# fallback chain
#     ${SKILL_DIR:-${CLAUDE_PLUGIN_ROOT:-${CODEX_HOME:-$HOME/.codex}}/skills/<name>}
# which resolves to the repo plugin under Claude (CLAUDE_PLUGIN_ROOT set) and to
# ~/.codex/skills/<name> under Codex. A plain copy therefore works on both.
#
# Re-run this after pulling submodule updates, then restart Codex.
#
# Usage: scripts/stage-codex.sh
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_SKILLS="${CODEX_HOME:-$HOME/.codex}/skills"
CODEX_AGENTS="${CODEX_HOME:-$HOME/.codex}/agents"
mkdir -p "$CODEX_SKILLS" "$CODEX_AGENTS"

stage_skills() {
  local src="$1"
  [ -d "$src" ] || { echo "  (no skills dir: $src)"; return 0; }
  for d in "$src"/*/; do
    [ -d "$d" ] || continue
    local name; name="$(basename "$d")"
    rsync -a --delete "$d" "$CODEX_SKILLS/$name/"
    echo "  skill: $name"
  done
}

stage_agents() {
  local src="$1"
  [ -d "$src" ] || { echo "  (no codex-agents dir: $src)"; return 0; }
  for t in "$src"/*.toml; do
    [ -f "$t" ] || continue
    cp "$t" "$CODEX_AGENTS/$(basename "$t")"
    echo "  agent: $(basename "$t")"
  done
}

echo "Staging figma-automation -> $CODEX_SKILLS"
stage_skills "$REPO/figma-automation/plugin/skills"
stage_agents "$REPO/figma-automation/plugin/codex-agents"

echo "Staging qa-automation -> $CODEX_SKILLS"
stage_skills "$REPO/qa-automation/plugin/skills"
stage_agents "$REPO/qa-automation/plugin/codex-agents"

echo "Done. Restart Codex to pick up changes."
