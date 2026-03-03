#!/usr/bin/env bash
set -euo pipefail

# manifest-dev for Gemini CLI — install or update everything
#
# Remote:  curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash
# Local:   bash dist/gemini/install.sh

REPO="doodledood/manifest-dev"
BRANCH="main"
DIST_PATH="dist/gemini"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "manifest-dev installer for Gemini CLI"
echo "======================================"

# --- Download ---
echo "Downloading from github.com/$REPO..."
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" | tar -xz -C "$TMP_DIR" --strip-components=1
SRC="$TMP_DIR/$DIST_PATH"

if [ ! -d "$SRC" ]; then
  echo "Error: $DIST_PATH not found in archive" >&2
  exit 1
fi

# --- Detect target ---
if [ -d ".gemini" ] || [ -d ".git" ]; then
  TARGET=".gemini"
  echo "Installing to project: .gemini/"
else
  TARGET="$HOME/.gemini"
  echo "Installing globally: ~/.gemini/"
fi

# --- Skills ---
mkdir -p "$TARGET/skills"
cp -r "$SRC/skills/"* "$TARGET/skills/"
echo "  Skills: $(ls "$SRC/skills/" | wc -l | tr -d ' ') installed"

# --- Agents ---
mkdir -p "$TARGET/agents"
cp -r "$SRC/agents/"* "$TARGET/agents/"
echo "  Agents: $(ls "$SRC/agents/" | wc -l | tr -d ' ') installed"

# --- Hooks ---
mkdir -p "$TARGET/hooks"
cp "$SRC/hooks/"*.py "$TARGET/hooks/"
cp "$SRC/hooks/hooks.json" "$TARGET/hooks/"
echo "  Hooks: $(ls "$SRC/hooks/"*.py | wc -l | tr -d ' ') hooks + adapter installed"

# --- Context file ---
cp "$SRC/GEMINI.md" "$TARGET/GEMINI.md"
echo "  Context: GEMINI.md installed"

# --- Extension manifest ---
cp "$SRC/gemini-extension.json" "$TARGET/gemini-extension.json" 2>/dev/null || true

echo ""
echo "Done! Restart Gemini CLI to activate."
echo ""
echo "Required: add to your settings.json:"
echo '  { "experimental": { "enableAgents": true } }'
echo ""
echo "Then merge hooks/hooks.json into your settings.json hooks section."
