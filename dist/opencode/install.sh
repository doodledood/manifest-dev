#!/usr/bin/env bash
set -euo pipefail

# manifest-dev for OpenCode — install or update everything
#
# Remote:  curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
# Local:   bash dist/opencode/install.sh

REPO="doodledood/manifest-dev"
BRANCH="main"
DIST_PATH="dist/opencode"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "manifest-dev installer for OpenCode"
echo "====================================="

# --- Download ---
echo "Downloading from github.com/$REPO..."
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" | tar -xz -C "$TMP_DIR" --strip-components=1
SRC="$TMP_DIR/$DIST_PATH"

if [ ! -d "$SRC" ]; then
  echo "Error: $DIST_PATH not found in archive" >&2
  exit 1
fi

# --- Detect target ---
if [ -d ".opencode" ] || [ -d ".git" ]; then
  TARGET=".opencode"
  echo "Installing to project: .opencode/"
else
  TARGET="$HOME/.config/opencode"
  echo "Installing globally: ~/.config/opencode/"
fi

# --- Skills ---
mkdir -p "$TARGET/skills"
cp -r "$SRC/skills/"* "$TARGET/skills/"
echo "  Skills: $(ls "$SRC/skills/" | wc -l | tr -d ' ') installed"

# --- Agents ---
mkdir -p "$TARGET/agents"
cp -r "$SRC/agents/"* "$TARGET/agents/"
echo "  Agents: $(ls "$SRC/agents/" | wc -l | tr -d ' ') installed"

# --- Commands ---
mkdir -p "$TARGET/commands"
cp -r "$SRC/commands/"* "$TARGET/commands/"
echo "  Commands: $(ls "$SRC/commands/" | wc -l | tr -d ' ') installed"

# --- Plugins (hook stubs — won't overwrite manual ports) ---
mkdir -p "$TARGET/plugins"
for f in "$SRC/plugins/"*; do
  fname=$(basename "$f")
  if [ "$fname" = "index.ts" ] && [ -f "$TARGET/plugins/$fname" ]; then
    echo "  Plugins: index.ts exists — skipped (won't overwrite manual port)"
  else
    cp "$f" "$TARGET/plugins/$fname"
  fi
done
echo "  Plugins: stubs installed (see HOOK_SPEC.md to implement)"

# --- Install plugin deps ---
if [ -f "$TARGET/plugins/package.json" ]; then
  if command -v bun &>/dev/null; then
    (cd "$TARGET/plugins" && bun install --silent 2>/dev/null) && echo "  Deps: installed via bun" || echo "  Deps: run manually: cd $TARGET/plugins && bun install"
  else
    echo "  Deps: bun not found — run: cd $TARGET/plugins && npm install"
  fi
fi

# --- Context file ---
cp "$SRC/AGENTS.md" "./AGENTS.md" 2>/dev/null || cp "$SRC/AGENTS.md" "$TARGET/AGENTS.md"
echo "  Context: AGENTS.md installed"

echo ""
echo "Done! Restart OpenCode to activate."
echo "Hook stubs need manual TypeScript port — see plugins/HOOK_SPEC.md."
