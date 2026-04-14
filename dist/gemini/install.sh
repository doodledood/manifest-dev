#!/usr/bin/env bash
# manifest-dev installer for Gemini CLI
#
# Idempotent — safe to re-run. Copies skills, agents, hooks to target directory.
# Uses install_helpers.py for namespacing (adds -manifest-dev suffix).
# Merges settings additively — never overwrites user config.
#
# Usage:
#   ./install.sh              # Install to project .gemini/
#   ./install.sh --global     # Install to ~/.gemini/
#   ./install.sh --dir <path> # Install to custom directory

set -euo pipefail

# When piped via curl | bash, BASH_SOURCE is unset and companion files aren't
# available. Detect this, clone the repo to a temp dir, and re-execute from there.
if [[ -z "${BASH_SOURCE[0]:-}" || "${BASH_SOURCE[0]}" == "bash" || "${BASH_SOURCE[0]}" == "/bin/bash" || "${BASH_SOURCE[0]}" == "/usr/bin/bash" ]]; then
    _tmpdir="$(mktemp -d)"
    trap 'rm -rf "$_tmpdir"' EXIT
    echo "Downloading manifest-dev (piped install detected)..."
    git clone --depth 1 --quiet https://github.com/doodledood/manifest-dev.git "$_tmpdir/manifest-dev"
    exec bash "$_tmpdir/manifest-dev/dist/gemini/install.sh" "$@"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="manifest-dev"

# Parse arguments
INSTALL_DIR=""
GLOBAL=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --global)
            GLOBAL=true
            shift
            ;;
        --dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./install.sh [--global | --dir <path>]"
            exit 1
            ;;
    esac
done

# Determine install directory
if [[ -n "$INSTALL_DIR" ]]; then
    TARGET="$INSTALL_DIR"
elif [[ "$GLOBAL" == "true" ]]; then
    TARGET="$HOME/.gemini"
else
    TARGET=".gemini"
fi

echo "manifest-dev installer for Gemini CLI"
echo "======================================"
echo "Source:  $SCRIPT_DIR"
echo "Target:  $TARGET"
echo ""

# Create directories
mkdir -p "$TARGET/skills"
mkdir -p "$TARGET/agents"
mkdir -p "$TARGET/hooks"

# --- Selective cleanup of previous manifest-dev installation ---
echo "Cleaning previous manifest-dev installation..."
find "$TARGET/skills" -maxdepth 1 -name "*-${NAMESPACE}" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/agents" -maxdepth 1 -name "*-${NAMESPACE}*" -exec rm -rf {} + 2>/dev/null || true
# Hooks directory: clean manifest-dev hook files
rm -f "$TARGET/hooks/gemini_adapter.py" 2>/dev/null || true
rm -f "$TARGET/hooks/hook_utils.py" 2>/dev/null || true
rm -f "$TARGET/hooks/post_compact_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/posttool_log_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/pretool_verify_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/prompt_submit_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/stop_do_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/understand_prompt_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/figure_out_prompt_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/thinking_disciplines_prompt_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/thinking_disciplines_pretool_hook.py" 2>/dev/null || true

# --- Copy hooks (no namespacing needed — extension-private) ---
echo "Installing hooks..."
cp "$SCRIPT_DIR/hooks/gemini_adapter.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/hook_utils.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/post_compact_hook.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/posttool_log_hook.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/pretool_verify_hook.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/prompt_submit_hook.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/stop_do_hook.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/thinking_disciplines_prompt_hook.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/thinking_disciplines_pretool_hook.py" "$TARGET/hooks/"

# --- Namespace and install skills + agents ---
echo "Installing skills and agents (with -${NAMESPACE} namespace)..."
python3 "$SCRIPT_DIR/install_helpers.py" "$SCRIPT_DIR" "$TARGET"

# --- Copy GEMINI.md if not exists ---
if [[ ! -f "$TARGET/GEMINI.md" ]]; then
    echo "Installing GEMINI.md..."
    cp "$SCRIPT_DIR/GEMINI.md" "$TARGET/GEMINI.md"
else
    echo "GEMINI.md already exists — skipping (not overwriting user file)"
fi

# --- Merge settings ---
echo "Merging settings..."
SETTINGS_FILE="$TARGET/settings.json"
HOOKS_JSON="$SCRIPT_DIR/hooks/hooks.json"

# Use Python helper to merge settings additively
python3 -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from pathlib import Path
from install_helpers import patch_hooks_json, merge_settings

hooks_config = patch_hooks_json(Path('${HOOKS_JSON}'), '${TARGET}/hooks')
merge_settings(Path('${SETTINGS_FILE}'), hooks_config)
print('  Settings merged successfully')
"

echo ""
echo "Installation complete!"
echo ""
echo "Components installed:"
echo "  Skills:  $(find "$TARGET/skills" -maxdepth 1 -name "*-${NAMESPACE}" -type d 2>/dev/null | wc -l) skills"
echo "  Agents:  $(find "$TARGET/agents" -maxdepth 1 -name "*-${NAMESPACE}.md" -type f 2>/dev/null | wc -l) agents"
echo "  Hooks:   9 hook scripts"
echo ""
echo "Required: enableAgents must be true in settings.json"
echo "  (already set by this installer)"
echo ""
echo "To uninstall:"
echo "  find \"$TARGET/skills\" -maxdepth 1 -name \"*-${NAMESPACE}\" -type d -exec rm -rf {} +"
echo "  find \"$TARGET/agents\" -maxdepth 1 -name \"*-${NAMESPACE}*\" -exec rm -rf {} +"
echo "  # Then remove hook entries from settings.json manually"
