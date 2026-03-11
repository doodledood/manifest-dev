#!/usr/bin/env bash
# manifest-dev installer for OpenCode CLI
# Idempotent, additive install. Safe to re-run for updates.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
#
# Or clone and run locally:
#   bash dist/opencode/install.sh
#
# Optional:
#   OPENCODE_INSTALL_TARGET=project bash dist/opencode/install.sh

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
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "manifest-dev installer for OpenCode"
echo "====================================="

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

if [ "$INSTALL_MODE" = "project" ]; then
  TARGET=".opencode"
  echo "Installing to project: .opencode/"
else
  TARGET="$HOME/.config/opencode"
  echo "Installing globally: ~/.config/opencode/"
fi

echo "Namespacing components..."
python3 "$SRC/install_helpers.py" namespace "$SRC" opencode

mkdir -p "$TARGET/skills"
find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/skills/"* "$TARGET/skills/"
echo "  Skills: $(ls -d "$SRC/skills/"*/ 2>/dev/null | wc -l | tr -d ' ') installed"

mkdir -p "$TARGET/agents"
find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/agents/"* "$TARGET/agents/"
echo "  Agents: $(ls "$SRC/agents/" | wc -l | tr -d ' ') installed"

mkdir -p "$TARGET/commands"
find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/commands/"* "$TARGET/commands/"
echo "  Commands: $(ls "$SRC/commands/" | wc -l | tr -d ' ') installed"

mkdir -p "$TARGET/plugins"
ROOT_PLUGIN="$TARGET/plugins/index.ts"
if [ -f "$ROOT_PLUGIN" ] && grep -q 'manifest-dev plugin for OpenCode CLI' "$ROOT_PLUGIN"; then
  cp "$ROOT_PLUGIN" "$ROOT_PLUGIN.manifest-dev-legacy.bak"
  rm -f "$ROOT_PLUGIN"
  echo "  Plugin: migrated legacy manifest-dev root plugin (backup at $ROOT_PLUGIN.manifest-dev-legacy.bak)"
fi
rm -f "$TARGET/plugins/manifest-dev.ts" "$TARGET/plugins/manifest-dev.HOOK_SPEC.md"
rm -rf "$TARGET/plugins/manifest-dev"
cp "$SRC/plugins/index.ts" "$TARGET/plugins/manifest-dev.ts"
cp "$SRC/plugins/HOOK_SPEC.md" "$TARGET/plugins/manifest-dev.HOOK_SPEC.md"
echo "  Plugin: installed to plugins/manifest-dev.ts"

if [ -f "$TARGET/opencode.json" ]; then
  cp "$TARGET/opencode.json" "$TARGET/opencode.json.bak"
  python3 "$SRC/install_helpers.py" cleanup-config "$TARGET/opencode.json"
  if cmp -s "$TARGET/opencode.json" "$TARGET/opencode.json.bak"; then
    echo "  Config: opencode.json left unchanged"
  else
    echo "  Config: removed legacy manifest-dev plugin registration (backup at $TARGET/opencode.json.bak)"
  fi
fi

echo ""
echo "Done! Restart OpenCode to activate."
echo ""
echo "Components installed to $TARGET/ (all workflow files suffixed with -manifest-dev):"
echo "  skills/    - 6 skills (define-manifest-dev, do-manifest-dev, etc.)"
echo "  agents/    - 12 agents (code-bugs-reviewer-manifest-dev, etc.)"
echo "  commands/  - 3 commands (/define-manifest-dev, /do-manifest-dev, /learn-define-patterns-manifest-dev)"
echo "  plugins/manifest-dev.ts - OpenCode hook plugin"
echo ""
echo "No manual plugin wiring is required."
