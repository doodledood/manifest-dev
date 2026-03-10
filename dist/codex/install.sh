#!/usr/bin/env bash
set -euo pipefail

# manifest-dev for Codex CLI -- idempotent installer
# All components are namespaced with -manifest-dev suffix to avoid collisions.
#
# Remote:  curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash
# Local:   bash dist/codex/install.sh

REPO="doodledood/manifest-dev"
BRANCH="main"
DIST_PATH="dist/codex"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "manifest-dev installer for Codex CLI"
echo "======================================"
echo ""

# --- Download ---
echo "Downloading from github.com/$REPO ($BRANCH)..."
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" \
  | tar -xz -C "$TMP_DIR" --strip-components=1

SRC="$TMP_DIR/$DIST_PATH"

if [ ! -d "$SRC" ]; then
  echo "Error: $DIST_PATH not found in archive" >&2
  exit 1
fi

# --- Namespace components in source before installing ---
echo ""
echo "Namespacing components..."
python3 "$SRC/install_helpers.py" namespace "$SRC" codex

# --- Skills (selective cleanup: remove only our namespaced dirs) ---
echo ""
echo "Installing skills..."
mkdir -p ".agents/skills"
find ".agents/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
for skill_dir in "$SRC/skills/"*/; do
  skill_name=$(basename "$skill_dir")
  cp -r "$skill_dir" ".agents/skills/$skill_name"
  echo "  + $skill_name"
done
echo "  Skills: $(ls -d "$SRC/skills/"*/ | wc -l | tr -d ' ') installed to .agents/skills/"

# --- AGENTS.md ---
echo ""
echo "Installing AGENTS.md..."
cp "$SRC/AGENTS.md" "./AGENTS.md"
echo "  AGENTS.md installed to project root"

# --- Agent TOML stubs (selective cleanup: remove only our namespaced files) ---
echo ""
echo "Installing agent TOML stubs..."
mkdir -p ".codex/agents"
find ".codex/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
for toml_file in "$SRC/agents/"*.toml; do
  toml_name=$(basename "$toml_file")
  cp "$toml_file" ".codex/agents/$toml_name"
  echo "  + $toml_name"
done
echo "  Agents: $(ls "$SRC/agents/"*.toml | wc -l | tr -d ' ') TOML stubs installed to .codex/agents/"

# --- Execution rules ---
echo ""
echo "Installing execution rules..."
mkdir -p ".codex/rules"
cp "$SRC/rules/default.rules" ".codex/rules/"
echo "  Rules: default.rules installed to .codex/rules/"

# --- Config (always update — backs up existing first) ---
echo ""
mkdir -p ".codex"
if [ -f ".codex/config.toml" ]; then
  cp ".codex/config.toml" ".codex/config.toml.bak"
  cp "$SRC/config.toml" ".codex/config.toml"
  echo "Config: config.toml updated (backup at .codex/config.toml.bak)"
  echo "  If you had custom settings, merge from the backup."
else
  cp "$SRC/config.toml" ".codex/config.toml"
  echo "Config: config.toml installed to .codex/"
fi

echo ""
echo "======================================"
echo "Done!"
echo ""
echo "What's installed (all suffixed with -manifest-dev):"
echo "  - 6 skills in .agents/skills/ (define-manifest-dev, do-manifest-dev, etc.)"
echo "  - AGENTS.md in project root (describes all 12 agents)"
echo "  - 12 TOML agent stubs in .codex/agents/ (multi-agent config)"
echo "  - Execution rules in .codex/rules/default.rules"
echo "  - Config in .codex/config.toml (multi-agent enabled, 12 agents registered)"
echo ""
echo "Skills are ready to use. Agents use 6 default tools:"
echo "  shell_command, apply_patch, update_plan, request_user_input, web_search, view_image"
echo ""
echo "Hooks are not available -- Codex has no hook system yet (Issue #2109)."
echo "Run this script again to update. Existing config.toml will be backed up."
