#!/usr/bin/env bash
# manifest-dev installer for OpenCode CLI
# Idempotent — safe to re-run. Downloads from GitHub, copies components.
# All components are namespaced with -manifest-dev suffix to avoid collisions.
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

# --- Namespace components in source before installing ---
echo "Namespacing components..."
python3 "$SRC/install_helpers.py" namespace "$SRC" opencode

# --- Skills (selective cleanup: remove only our namespaced dirs) ---
mkdir -p "$TARGET/skills"
find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/skills/"* "$TARGET/skills/"
echo "  Skills: $(ls -d "$SRC/skills/"*/ 2>/dev/null | wc -l | tr -d ' ') installed"

# --- Agents (selective cleanup: remove only our namespaced files) ---
mkdir -p "$TARGET/agents"
find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/agents/"* "$TARGET/agents/"
echo "  Agents: $(ls "$SRC/agents/" | wc -l | tr -d ' ') installed"

# --- Commands (selective cleanup: remove only our namespaced files) ---
mkdir -p "$TARGET/commands"
find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
cp -r "$SRC/commands/"* "$TARGET/commands/"
echo "  Commands: $(ls "$SRC/commands/" | wc -l | tr -d ' ') installed"

# --- Plugins (update all except manually ported index.ts) ---
mkdir -p "$TARGET/plugins"
for f in "$SRC/plugins/"*; do
  fname=$(basename "$f")
  if [ "$fname" = "index.ts" ] && [ -f "$TARGET/plugins/$fname" ]; then
    # Only skip if user has manually ported (removed all TODOs)
    if grep -q "TODO" "$TARGET/plugins/$fname" 2>/dev/null; then
      cp "$f" "$TARGET/plugins/$fname"
      echo "  Plugins: index.ts updated (still contains TODOs)"
    else
      cp "$TARGET/plugins/$fname" "$TARGET/plugins/index.ts.bak"
      echo "  Plugins: index.ts skipped (manual port detected, backup at index.ts.bak)"
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
echo "Components installed to $TARGET/ (all suffixed with -manifest-dev):"
echo "  skills/    - 6 skills (define-manifest-dev, do-manifest-dev, etc.)"
echo "  agents/    - 12 agents (code-bugs-reviewer-manifest-dev, etc.)"
echo "  commands/  - 3 commands (/define-manifest-dev, /do-manifest-dev, /learn-define-patterns-manifest-dev)"
echo "  plugins/   - Hook stubs (require manual TS porting — see HOOK_SPEC.md)"
echo "  AGENTS.md  - Workflow overview and agent descriptions"
echo ""
echo "Hook stubs need manual TypeScript port — see plugins/HOOK_SPEC.md."
