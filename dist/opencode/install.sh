#!/usr/bin/env bash
# manifest-dev installer for OpenCode CLI (v0.74.0)
# Idempotent, additive install. Safe to re-run for updates.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
#
# Or clone and run locally:
#   bash dist/opencode/install.sh
#
# Options:
#   OPENCODE_INSTALL_TARGET=project bash dist/opencode/install.sh   # project-local install
#   bash dist/opencode/install.sh uninstall                         # remove manifest-dev files

set -euo pipefail

REPO="doodledood/manifest-dev"
BRANCH="main"
DIST_PATH="dist/opencode"
SCRIPT_SOURCE="${BASH_SOURCE[0]-}"
SCRIPT_DIR=""
if [ -n "$SCRIPT_SOURCE" ] && [ -f "$SCRIPT_SOURCE" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
fi
INSTALL_MODE="${OPENCODE_INSTALL_TARGET:-global}"
ACTION="${1:-install}"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "manifest-dev installer for OpenCode (v0.74.0)"
echo "================================================"

case "$ACTION" in
  install|uninstall)
    ;;
  *)
    echo "Usage: bash install.sh [install|uninstall]" >&2
    exit 1
    ;;
esac

# Determine source: local dist/ or download from GitHub
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/install_helpers.py" ] && [ -d "$SCRIPT_DIR/skills" ] && [ -d "$SCRIPT_DIR/agents" ] && [ -d "$SCRIPT_DIR/commands" ] && [ -d "$SCRIPT_DIR/plugins" ]; then
  echo "Using local dist/opencode from $SCRIPT_DIR..."
  SRC="$TMP_DIR/local-dist"
  mkdir -p "$SRC"
  cp -R "$SCRIPT_DIR"/. "$SRC"/
else
  echo "Downloading from github.com/$REPO..."
  curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" | tar -xz -C "$TMP_DIR" --strip-components=1
  SRC="$TMP_DIR/$DIST_PATH"
fi

if [ ! -d "$SRC" ]; then
  echo "Error: $DIST_PATH not found in archive" >&2
  exit 1
fi

# Determine target directory
if [ "$INSTALL_MODE" = "project" ]; then
  TARGET=".opencode"
  echo "Installing to project: .opencode/"
else
  TARGET="$HOME/.config/opencode"
  echo "Installing globally: ~/.config/opencode/"
fi

# --- Uninstall ---
if [ "$ACTION" = "uninstall" ]; then
  echo "Removing manifest-dev-managed OpenCode files from $TARGET..."

  # Selective cleanup: only remove *-manifest-dev* files
  find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
  find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
  find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true

  # Remove plugin files (never touch user's index.ts)
  rm -f \
    "$TARGET/plugins/manifest-dev.ts" \
    "$TARGET/plugins/manifest-dev.HOOK_SPEC.md"

  # Clean up empty directories (safe — rmdir only removes empty dirs)
  rmdir "$TARGET/skills" 2>/dev/null || true
  rmdir "$TARGET/agents" 2>/dev/null || true
  rmdir "$TARGET/commands" 2>/dev/null || true
  rmdir "$TARGET/plugins" 2>/dev/null || true
  rmdir "$TARGET" 2>/dev/null || true

  echo ""
  echo "Done! Removed manifest-dev files only. User files untouched."
  exit 0
fi

# --- Install ---

# Namespace components with -manifest-dev suffix
echo "Namespacing components..."
python3 "$SRC/install_helpers.py" namespace "$SRC" opencode

# Skills (copy entire directories)
mkdir -p "$TARGET/skills"
find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/skills/"* "$TARGET/skills/"
echo "  Skills: $(ls -d "$SRC/skills/"*/ 2>/dev/null | wc -l | tr -d ' ') installed"

# Agents
mkdir -p "$TARGET/agents"
find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/agents/"* "$TARGET/agents/"
echo "  Agents: $(ls "$SRC/agents/" | wc -l | tr -d ' ') installed"

# Commands
mkdir -p "$TARGET/commands"
find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/commands/"* "$TARGET/commands/"
echo "  Commands: $(ls "$SRC/commands/" | wc -l | tr -d ' ') installed"

# Plugin (own top-level file, never touches user's index.ts)
mkdir -p "$TARGET/plugins"
rm -f "$TARGET/plugins/manifest-dev.ts" "$TARGET/plugins/manifest-dev.HOOK_SPEC.md"
cp "$SRC/plugins/index.ts" "$TARGET/plugins/manifest-dev.ts"
cp "$SRC/plugins/HOOK_SPEC.md" "$TARGET/plugins/manifest-dev.HOOK_SPEC.md"
echo "  Plugin: installed to plugins/manifest-dev.ts"

echo ""
echo "Done! Restart OpenCode to activate."
echo ""
echo "Components installed to $TARGET/ (all suffixed with -manifest-dev):"
echo "  skills/    - 7 skills (define-manifest-dev, do-manifest-dev, etc.)"
echo "  agents/    - 14 agents (code-bugs-reviewer-manifest-dev, etc.)"
echo "  commands/  - 4 commands (/define-manifest-dev, /do-manifest-dev, etc.)"
echo "  plugins/manifest-dev.ts - workflow enforcement hooks"
echo ""
echo "No manual plugin wiring required. OpenCode auto-loads from plugins/."
