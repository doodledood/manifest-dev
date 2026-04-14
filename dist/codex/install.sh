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
INSTALL_ROOT="${CODEX_HOME:-$HOME/.codex}"
STATE_FILE="$INSTALL_ROOT/manifest-dev-install-state.json"
SCRIPT_SOURCE="${BASH_SOURCE[0]-}"
SCRIPT_DIR=""
if [ -n "$SCRIPT_SOURCE" ] && [ -f "$SCRIPT_SOURCE" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
fi
ACTION="${1:-install}"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "manifest-dev installer for Codex CLI"
echo "======================================"
echo ""

case "$ACTION" in
  install|uninstall)
    ;;
  *)
    echo "Usage: bash install.sh [install|uninstall]" >&2
    exit 1
    ;;
esac

if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/install_helpers.py" ] && [ -d "$SCRIPT_DIR/skills" ] && [ -d "$SCRIPT_DIR/agents" ] && [ -f "$SCRIPT_DIR/config.toml" ]; then
  echo "Using local dist/codex from $SCRIPT_DIR..."
  SRC="$TMP_DIR/local-dist"
  mkdir -p "$SRC"
  cp -R "$SCRIPT_DIR"/. "$SRC"/
else
  echo "Downloading from github.com/$REPO ($BRANCH)..."
  curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" \
    | tar -xz -C "$TMP_DIR" --strip-components=1

  SRC="$TMP_DIR/$DIST_PATH"
fi

if [ ! -d "$SRC" ]; then
  echo "Error: $DIST_PATH not found in archive" >&2
  exit 1
fi

if [ "$ACTION" = "uninstall" ]; then
  echo "Removing manifest-dev-managed Codex files from $INSTALL_ROOT..."

  find "$INSTALL_ROOT/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
  find "$INSTALL_ROOT/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
  rm -f "$INSTALL_ROOT/rules/manifest-dev.rules"

  if [ -f "$INSTALL_ROOT/config.toml" ]; then
    cp "$INSTALL_ROOT/config.toml" "$INSTALL_ROOT/config.toml.pre-manifest-dev-uninstall.bak"
    python3 "$SRC/install_helpers.py" unmerge-config "$INSTALL_ROOT/config.toml" "$STATE_FILE"
    echo "Config: manifest-dev sections removed (backup at $INSTALL_ROOT/config.toml.pre-manifest-dev-uninstall.bak)"
  elif [ -f "$STATE_FILE" ]; then
    rm -f "$STATE_FILE"
  fi

  rmdir "$INSTALL_ROOT/skills" 2>/dev/null || true
  rmdir "$INSTALL_ROOT/agents" 2>/dev/null || true
  rmdir "$INSTALL_ROOT/rules" 2>/dev/null || true
  rmdir "$INSTALL_ROOT" 2>/dev/null || true

  echo ""
  echo "======================================"
  echo "Done!"
  echo ""
  echo "Removed manifest-dev-managed Codex files only."
  exit 0
fi

# --- Namespace components in source before installing ---
echo ""
echo "Namespacing components..."
python3 "$SRC/install_helpers.py" namespace "$SRC" codex

# --- Skills (selective cleanup: remove only our namespaced dirs) ---
echo ""
echo "Installing skills..."
mkdir -p "$INSTALL_ROOT/skills"
find "$INSTALL_ROOT/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
for skill_dir in "$SRC/skills/"*/; do
  skill_name=$(basename "$skill_dir")
  cp -r "$skill_dir" "$INSTALL_ROOT/skills/$skill_name"
  echo "  + $skill_name"
done
echo "  Skills: $(ls -d "$SRC/skills/"*/ | wc -l | tr -d ' ') installed to $INSTALL_ROOT/skills/"

# --- Agent TOML stubs (selective cleanup: remove only our namespaced files) ---
echo ""
echo "Installing agent TOML stubs..."
mkdir -p "$INSTALL_ROOT/agents"
find "$INSTALL_ROOT/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
for toml_file in "$SRC/agents/"*.toml; do
  toml_name=$(basename "$toml_file")
  cp "$toml_file" "$INSTALL_ROOT/agents/$toml_name"
  echo "  + $toml_name"
done
echo "  Agents: $(ls "$SRC/agents/"*.toml | wc -l | tr -d ' ') TOML stubs installed to $INSTALL_ROOT/agents/"

# --- Execution rules ---
echo ""
echo "Installing execution rules..."
mkdir -p "$INSTALL_ROOT/rules"
cp "$SRC/rules/default.rules" "$INSTALL_ROOT/rules/manifest-dev.rules"
echo "  Rules: manifest-dev.rules installed to $INSTALL_ROOT/rules/"

# --- Config (merge into existing config — backs up existing first) ---
echo ""
mkdir -p "$INSTALL_ROOT"
if [ -f "$INSTALL_ROOT/config.toml" ]; then
  cp "$INSTALL_ROOT/config.toml" "$INSTALL_ROOT/config.toml.bak"
  python3 "$SRC/install_helpers.py" merge-config "$SRC/config.toml" "$INSTALL_ROOT/config.toml" "$STATE_FILE"
  echo "Config: config.toml merged (backup at $INSTALL_ROOT/config.toml.bak)"
else
  python3 "$SRC/install_helpers.py" merge-config "$SRC/config.toml" "$INSTALL_ROOT/config.toml" "$STATE_FILE"
  echo "Config: config.toml installed to $INSTALL_ROOT/"
fi

echo ""
echo "======================================"
echo "Done!"
echo ""
echo "What's installed (all suffixed with -manifest-dev):"
echo "  - 12 skills in $INSTALL_ROOT/skills/ (define-manifest-dev, do-manifest-dev, etc.)"
echo "  - 14 TOML agent stubs in $INSTALL_ROOT/agents/ (multi-agent config)"
echo "  - Execution rules in $INSTALL_ROOT/rules/manifest-dev.rules"
echo "  - Config in $INSTALL_ROOT/config.toml (multi-agent enabled, 14 agents registered)"
echo ""
echo "Skills are ready to use. Agents use 6 default tools:"
echo "  shell_command, apply_patch, update_plan, request_user_input, web_search, view_image"
echo ""
echo "Hooks are not available -- Codex has no hook system yet (Issue #2109)."
echo "Run this script again to update. Existing config.toml is backed up and merged."
