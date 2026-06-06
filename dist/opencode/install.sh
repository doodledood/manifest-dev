#!/usr/bin/env bash
set -euo pipefail

# manifest-dev OpenCode distribution installer
# Idempotent — safe to re-run. Only touches *-manifest-dev files.
#
# Usage:
#   ./install.sh                    # Install globally to ~/.config/opencode/
#   ./install.sh --local            # Install to project-local .opencode/
#   ./install.sh --dir <path>       # Install to custom directory
#   ./install.sh uninstall [scope]  # Remove only manifest-dev-managed files

# When piped via curl | bash, BASH_SOURCE is unset and companion files aren't
# available. Detect this, clone the repo to a temp dir, and re-execute from there.
if [[ -z "${BASH_SOURCE[0]:-}" || "${BASH_SOURCE[0]}" == "bash" || "${BASH_SOURCE[0]}" == "/bin/bash" || "${BASH_SOURCE[0]}" == "/usr/bin/bash" ]]; then
    _tmpdir="$(mktemp -d)"
    trap 'rm -rf "$_tmpdir"' EXIT
    echo "Downloading manifest-dev (piped install detected)..."
    git clone --depth 1 --quiet https://github.com/doodledood/manifest-dev.git "$_tmpdir/manifest-dev"
    exec bash "$_tmpdir/manifest-dev/dist/opencode/install.sh" "$@"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACTION="install"
INSTALL_DIR=""
SCOPE="global"
SCOPE_EXPLICIT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        install|uninstall)
            ACTION="$1"
            shift
            ;;
        --global)
            SCOPE="global"
            SCOPE_EXPLICIT=true
            shift
            ;;
        --local)
            SCOPE="local"
            SCOPE_EXPLICIT=true
            shift
            ;;
        --dir)
            if [[ $# -lt 2 ]]; then
                echo "Missing path after --dir" >&2
                exit 1
            fi
            INSTALL_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Usage: bash install.sh [install|uninstall] [--global | --local | --dir <path>]" >&2
            exit 1
            ;;
    esac
done

if [[ -n "$INSTALL_DIR" ]]; then
    TARGET="$INSTALL_DIR"
elif [[ "$SCOPE" == "local" ]]; then
    TARGET=".opencode"
elif [[ -n "${OPENCODE_TARGET:-}" && "$SCOPE_EXPLICIT" == "false" ]]; then
    TARGET="$OPENCODE_TARGET"
else
    TARGET="$HOME/.config/opencode"
fi

echo "manifest-dev OpenCode installer"
echo "================================"
echo "Source:  $SCRIPT_DIR"
echo "Target:  $TARGET"
echo ""

if [[ "$ACTION" == "uninstall" ]]; then
    echo "Removing manifest-dev-managed OpenCode files..."
    find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev-tools" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
    find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
    find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev-tools*" -exec rm -rf {} + 2>/dev/null || true
    rm -f "$TARGET/plugins/manifest-dev.ts" 2>/dev/null || true
    rm -f "$TARGET/plugins/manifest-dev.HOOK_SPEC.md" 2>/dev/null || true

    if [[ -f "$TARGET/AGENTS.md" ]] && cmp -s "$SCRIPT_DIR/AGENTS.md" "$TARGET/AGENTS.md"; then
        rm -f "$TARGET/AGENTS.md"
    fi

    rmdir "$TARGET/skills" "$TARGET/agents" "$TARGET/commands" "$TARGET/plugins" "$TARGET" 2>/dev/null || true
    echo "Removed manifest-dev-managed OpenCode files only."
    exit 0
fi

# Ensure target directories exist
mkdir -p "$TARGET"/{skills,agents,commands}

# ---------------------------------------------------------------------------
# Step 1: Selective cleanup of previous install (only *-manifest-dev files)
# ---------------------------------------------------------------------------
echo "Cleaning previous manifest-dev components..."
find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev-tools" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev-tools*" -exec rm -rf {} + 2>/dev/null || true
rm -f "$TARGET/plugins/manifest-dev.ts" 2>/dev/null || true
rm -f "$TARGET/plugins/manifest-dev.HOOK_SPEC.md" 2>/dev/null || true
rmdir "$TARGET/plugins" 2>/dev/null || true

# ---------------------------------------------------------------------------
# Step 2: Run namespacing helper to copy and namespace all components
# ---------------------------------------------------------------------------
echo "Installing components with -manifest-dev namespace..."
python3 "$SCRIPT_DIR/install_helpers.py" "$SCRIPT_DIR" "$TARGET"

# ---------------------------------------------------------------------------
# Step 3: Install context file
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

skill_count=$(find "$TARGET/skills" -maxdepth 1 \( -name "*-manifest-dev" -o -name "*-manifest-dev-tools" \) -type d 2>/dev/null | wc -l)
agent_count=$(find "$TARGET/agents" -maxdepth 1 \( -name "*-manifest-dev.md" -o -name "*-manifest-dev-tools.md" \) -type f 2>/dev/null | wc -l)
command_count=$(find "$TARGET/commands" -maxdepth 1 \( -name "*-manifest-dev.md" -o -name "*-manifest-dev-tools.md" \) -type f 2>/dev/null | wc -l)

echo "  Skills:   $skill_count"
echo "  Agents:   $agent_count"
echo "  Commands: $command_count"
echo "  Context:  AGENTS.md"
echo ""
echo "Usage: /define-manifest-dev, /do-manifest-dev, /adr-manifest-dev-tools, etc."

if [[ "$TARGET" != ".opencode" && -d ".opencode" ]]; then
    local_count=$(
        (find ".opencode/skills" ".opencode/agents" ".opencode/commands" \
            -maxdepth 1 \( -name "*-manifest-dev" -o -name "*-manifest-dev-tools" -o -name "*-manifest-dev.md" -o -name "*-manifest-dev-tools.md" \) \
            2>/dev/null || true) | wc -l | tr -d ' '
    )
    if [[ "${local_count:-0}" != "0" ]]; then
        echo ""
        echo "Note: found $local_count manifest-dev component(s) in project-local .opencode/."
        echo "OpenCode may prefer project-local components in this repo. Update them with:"
        echo "  curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- --local"
        echo "Or remove only local manifest-dev files with:"
        echo "  curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- uninstall --local"
    fi
fi
