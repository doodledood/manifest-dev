#!/usr/bin/env bash
set -euo pipefail

# manifest-dev OpenCode distribution installer
# Idempotent — safe to re-run. Only touches *-manifest-dev files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${OPENCODE_TARGET:-.opencode}"

echo "manifest-dev OpenCode installer"
echo "================================"
echo "Source:  $SCRIPT_DIR"
echo "Target:  $TARGET"
echo ""

# Ensure target directories exist
mkdir -p "$TARGET"/{skills,agents,commands,plugins}

# ---------------------------------------------------------------------------
# Step 1: Selective cleanup of previous install (only *-manifest-dev files)
# ---------------------------------------------------------------------------
echo "Cleaning previous manifest-dev components..."
find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
rm -f "$TARGET/plugins/manifest-dev.ts" 2>/dev/null || true
rm -f "$TARGET/plugins/manifest-dev.HOOK_SPEC.md" 2>/dev/null || true

# ---------------------------------------------------------------------------
# Step 2: Run namespacing helper to copy and namespace all components
# ---------------------------------------------------------------------------
echo "Installing components with -manifest-dev namespace..."
python3 "$SCRIPT_DIR/install_helpers.py" "$SCRIPT_DIR" "$TARGET"

# ---------------------------------------------------------------------------
# Step 3: Install plugin (no namespacing — single file, auto-loaded)
# ---------------------------------------------------------------------------
echo "Installing plugin..."
cp "$SCRIPT_DIR/plugins/index.ts" "$TARGET/plugins/manifest-dev.ts"
cp "$SCRIPT_DIR/plugins/HOOK_SPEC.md" "$TARGET/plugins/manifest-dev.HOOK_SPEC.md"

# ---------------------------------------------------------------------------
# Step 4: Install context file
# ---------------------------------------------------------------------------
echo "Installing AGENTS.md..."
cp "$SCRIPT_DIR/AGENTS.md" "$TARGET/AGENTS.md"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "Installation complete."
echo ""
echo "Components installed to $TARGET/:"

skill_count=$(find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d 2>/dev/null | wc -l)
agent_count=$(find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev.md" -type f 2>/dev/null | wc -l)
command_count=$(find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev.md" -type f 2>/dev/null | wc -l)

echo "  Skills:   $skill_count"
echo "  Agents:   $agent_count"
echo "  Commands: $command_count"
echo "  Plugin:   manifest-dev.ts"
echo "  Context:  AGENTS.md"
echo ""
echo "Usage: /define-manifest-dev, /do-manifest-dev, /auto-manifest-dev, etc."
