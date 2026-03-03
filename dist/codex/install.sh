#!/usr/bin/env bash
set -euo pipefail

# manifest-dev for Codex CLI — install or update everything
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

# --- Download ---
echo "Downloading from github.com/$REPO..."
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" | tar -xz -C "$TMP_DIR" --strip-components=1
SRC="$TMP_DIR/$DIST_PATH"

if [ ! -d "$SRC" ]; then
  echo "Error: $DIST_PATH not found in archive" >&2
  exit 1
fi

# --- Skills ---
mkdir -p ".agents/skills"
cp -r "$SRC/skills/"* ".agents/skills/"
echo "  Skills: $(ls "$SRC/skills/" | wc -l | tr -d ' ') installed"

# --- AGENTS.md ---
cp "$SRC/AGENTS.md" "./AGENTS.md"
echo "  Context: AGENTS.md installed"

# --- Agent TOML stubs ---
mkdir -p ".codex/agents"
cp "$SRC/agents/"*.toml ".codex/agents/"
echo "  Agents: $(ls "$SRC/agents/"*.toml | wc -l | tr -d ' ') TOML stubs installed"

# --- Execution rules ---
mkdir -p ".codex/rules"
cp "$SRC/rules/default.rules" ".codex/rules/"
echo "  Rules: default.rules installed"

# --- Config (don't overwrite existing) ---
if [ -f ".codex/config.toml" ]; then
  echo "  Config: .codex/config.toml exists — merge manually from downloaded config"
  echo "          Tip: cat $SRC/config.toml"
else
  mkdir -p ".codex"
  cp "$SRC/config.toml" ".codex/config.toml"
  echo "  Config: config.toml installed"
fi

echo ""
echo "Done! Skills are ready to use."
echo "Agent TOML stubs provide multi-agent support (limited to shell + apply_patch)."
echo "Hooks not available — Codex hook system expected mid-2026."
