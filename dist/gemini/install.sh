#!/usr/bin/env bash
# manifest-dev installer for Gemini CLI
#
# Idempotent — safe to re-run. Copies skills, agents, hooks to target directory.
# Uses install_helpers.py for namespacing (adds plugin-owned suffixes).
# Merges settings additively — never overwrites user config.
#
# Usage:
#   ./install.sh              # Install globally to ~/.gemini/
#   ./install.sh --local      # Install to project .gemini/
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
SCOPE="global"
ACTION="install"

while [[ $# -gt 0 ]]; do
    case "$1" in
        install|uninstall)
            ACTION="$1"
            shift
            ;;
        --global)
            SCOPE="global"
            shift
            ;;
        --local)
            SCOPE="local"
            shift
            ;;
        --dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./install.sh [install|uninstall] [--global | --local | --dir <path>]"
            exit 1
            ;;
    esac
done

# Determine install directory
if [[ -n "$INSTALL_DIR" ]]; then
    TARGET="$INSTALL_DIR"
elif [[ "$SCOPE" == "local" ]]; then
    TARGET=".gemini"
else
    TARGET="$HOME/.gemini"
fi

echo "manifest-dev installer for Gemini CLI"
echo "======================================"
echo "Source:  $SCRIPT_DIR"
echo "Target:  $TARGET"
echo ""

SETTINGS_FILE="$TARGET/settings.json"
STATE_FILE="$TARGET/manifest-dev-install-state.json"

if [[ "$ACTION" == "uninstall" ]]; then
    echo "Removing manifest-dev-managed Gemini files..."
    find "$TARGET/skills" -maxdepth 1 -name "*-${NAMESPACE}" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$TARGET/skills" -maxdepth 1 -name "*-${NAMESPACE}-tools" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$TARGET/agents" -maxdepth 1 -name "*-${NAMESPACE}*" -exec rm -rf {} + 2>/dev/null || true
    rm -f "$TARGET/hooks/gemini_adapter.py" 2>/dev/null || true
    rm -f "$TARGET/hooks/hook_utils.py" 2>/dev/null || true
    rm -f "$TARGET/hooks/post_compact_hook.py" 2>/dev/null || true
    rm -f "$TARGET/hooks/stop_do_hook.py" 2>/dev/null || true

    if [[ -f "$TARGET/GEMINI.md" ]] && cmp -s "$SCRIPT_DIR/GEMINI.md" "$TARGET/GEMINI.md"; then
        rm -f "$TARGET/GEMINI.md"
    fi

    python3 -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from pathlib import Path
from install_helpers import unmerge_settings

unmerge_settings(Path('${SETTINGS_FILE}'), Path('${STATE_FILE}'))
print('  Settings unmerged successfully')
"

    rmdir "$TARGET/skills" "$TARGET/agents" "$TARGET/hooks" "$TARGET" 2>/dev/null || true
    echo "Removed manifest-dev-managed Gemini files only."
    exit 0
fi

# Create directories
mkdir -p "$TARGET/skills"
mkdir -p "$TARGET/agents"
mkdir -p "$TARGET/hooks"

# --- Selective cleanup of previous manifest-dev installation ---
echo "Cleaning previous manifest-dev installation..."
find "$TARGET/skills" -maxdepth 1 -name "*-${NAMESPACE}" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/skills" -maxdepth 1 -name "*-${NAMESPACE}-tools" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/agents" -maxdepth 1 -name "*-${NAMESPACE}*" -exec rm -rf {} + 2>/dev/null || true
# Hooks directory: clean manifest-dev hook files
rm -f "$TARGET/hooks/gemini_adapter.py" 2>/dev/null || true
rm -f "$TARGET/hooks/hook_utils.py" 2>/dev/null || true
rm -f "$TARGET/hooks/post_compact_hook.py" 2>/dev/null || true
rm -f "$TARGET/hooks/stop_do_hook.py" 2>/dev/null || true

# --- Copy hooks (no namespacing needed — extension-private) ---
echo "Installing hooks..."
cp "$SCRIPT_DIR/hooks/gemini_adapter.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/hook_utils.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/post_compact_hook.py" "$TARGET/hooks/"
cp "$SCRIPT_DIR/hooks/stop_do_hook.py" "$TARGET/hooks/"

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
HOOKS_JSON="$SCRIPT_DIR/hooks/hooks.json"

# Use Python helper to merge settings additively
python3 -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from pathlib import Path
from install_helpers import (
    build_install_state,
    patch_hooks_json,
    merge_settings,
    write_install_state,
)

hooks_config = patch_hooks_json(Path('${HOOKS_JSON}'), '${TARGET}')
settings_path = Path('${SETTINGS_FILE}')
state = build_install_state(settings_path)
merge_settings(settings_path, hooks_config)
write_install_state(Path('${STATE_FILE}'), state)
print('  Settings merged successfully')
"

echo ""
echo "Installation complete!"
echo ""
echo "Components installed:"
echo "  Skills:  $(find "$TARGET/skills" -maxdepth 1 \( -name "*-${NAMESPACE}" -o -name "*-${NAMESPACE}-tools" \) -type d 2>/dev/null | wc -l) skills"
echo "  Agents:  $(find "$TARGET/agents" -maxdepth 1 -name "*-${NAMESPACE}.md" -type f 2>/dev/null | wc -l) agents"
echo "  Hooks:   4 hook scripts (adapter + utils + 2 hooks)"
echo ""
echo "Required: enableAgents must be true in settings.json"
echo "  (already set by this installer)"
echo ""
echo "To uninstall:"
if [[ "$SCOPE" == "global" && -z "$INSTALL_DIR" ]]; then
    echo "  $0 uninstall --global"
elif [[ -n "$INSTALL_DIR" ]]; then
    echo "  $0 uninstall --dir \"$INSTALL_DIR\""
else
    echo "  $0 uninstall --local"
fi

if [[ "$TARGET" != ".gemini" && -d ".gemini" ]]; then
    local_count=$(
        (find ".gemini/skills" ".gemini/agents" \
            -maxdepth 1 \( -name "*-manifest-dev" -o -name "*-manifest-dev-tools" -o -name "*-manifest-dev.md" -o -name "*-manifest-dev-tools.md" \) \
            2>/dev/null || true) | wc -l | tr -d ' '
    )
    if [[ "${local_count:-0}" != "0" ]]; then
        echo ""
        echo "Note: found $local_count manifest-dev component(s) in project-local .gemini/."
        echo "Gemini CLI may prefer project-local components in this repo. Update them with:"
        echo "  curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash -s -- --local"
        echo "Or remove only local manifest-dev files with:"
        echo "  curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash -s -- uninstall --local"
    fi
fi
