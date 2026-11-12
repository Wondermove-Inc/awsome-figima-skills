#!/usr/bin/env bash
# Fetch Figma's official agent skills into a local, git-ignored vendor folder.
#
# Figma publishes these skills in github.com/figma/mcp-server-guide under the
# Figma Developer Terms (no OSS license file), so this repository does not
# redistribute them. This script pulls the current copy for local agent use.
#
# Usage:
#   ./scripts/sync-figma-official-skills.sh            # default target: vendor/figma-official-skills
#   ./scripts/sync-figma-official-skills.sh ~/.codex/skills/figma-official
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-$repo_root/vendor/figma-official-skills}"
source_repo="${FIGMA_SKILLS_REPO:-https://github.com/figma/mcp-server-guide.git}"
source_ref="${FIGMA_SKILLS_REF:-main}"

if ! command -v git >/dev/null 2>&1; then
  echo "git not found in PATH" >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

echo "Fetching $source_repo@$source_ref ..."
git clone --quiet --depth 1 --branch "$source_ref" --filter=blob:none --sparse "$source_repo" "$tmp/guide"
git -C "$tmp/guide" sparse-checkout set skills workflow-skills >/dev/null

mkdir -p "$target"
for dir in skills workflow-skills; do
  if [ -d "$tmp/guide/$dir" ]; then
    rm -rf "${target:?}/$dir"
    cp -R "$tmp/guide/$dir" "$target/$dir"
  fi
done

commit="$(git -C "$tmp/guide" rev-parse --short HEAD)"
{
  echo "source: $source_repo"
  echo "ref: $source_ref"
  echo "commit: $commit"
  echo "fetched: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "terms: https://www.figma.com/legal/developer-terms/"
} > "$target/SOURCE.txt"

count="$(find "$target/skills" "$target/workflow-skills" -name SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
echo "Synced $count official Figma skills into $target (commit $commit)."
echo "Point your agent's skill loader at that folder, or copy the folders you need."
