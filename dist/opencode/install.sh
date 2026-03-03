#!/usr/bin/env bash
# manifest-dev installer for OpenCode CLI
# Idempotent — safe to re-run. Downloads from GitHub, copies components.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
#
# Or clone and run locally:
#   bash dist/opencode/install.sh

set -euo pipefail

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
    # Check if the existing file has been manually ported (no TODOs remaining)
    if grep -q "TODO: Port from" "$TARGET/plugins/$fname" 2>/dev/null; then
      cp "$f" "$TARGET/plugins/$fname"
      echo "  Plugins: index.ts updated (still contains TODOs)"
    else
      echo "  Plugins: index.ts exists — skipped (won't overwrite manual port)"
    fi
  else
    cp "$f" "$TARGET/plugins/$fname"
  fi
done
echo "  Plugins: stubs installed (see HOOK_SPEC.md to implement)"

# --- Install plugin deps ---
if [ -f "$TARGET/plugins/package.json" ]; then
  if command -v bun &>/dev/null; then
    (cd "$TARGET/plugins" && bun install --silent 2>/dev/null) && echo "  Deps: installed via bun" || echo "  Deps: run manually: cd $TARGET/plugins && bun install"
  elif command -v npm &>/dev/null; then
    (cd "$TARGET/plugins" && npm install --silent 2>/dev/null) && echo "  Deps: installed via npm" || echo "  Deps: run manually: cd $TARGET/plugins && npm install"
  else
    echo "  Deps: bun/npm not found — run: cd $TARGET/plugins && bun install"
  fi
fi

# --- Context file ---
cp "$SRC/AGENTS.md" "./AGENTS.md" 2>/dev/null || cp "$SRC/AGENTS.md" "$TARGET/AGENTS.md"
echo "  Context: AGENTS.md installed"

echo ""
echo "Done! Restart OpenCode to activate."
echo ""
echo "Components installed to $TARGET/:"
echo "  skills/    - 6 skills (define, do, done, escalate, learn-define-patterns, verify)"
echo "  agents/    - 12 agents (code reviewers, criteria-checker, manifest-verifier, etc.)"
echo "  commands/  - 3 commands (/define, /do, /learn-define-patterns)"
echo "  plugins/   - Hook stubs (require manual TS porting — see HOOK_SPEC.md)"
echo "  AGENTS.md  - Workflow overview and agent descriptions"
echo ""
echo "Hook stubs need manual TypeScript port — see plugins/HOOK_SPEC.md."
