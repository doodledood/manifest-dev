#!/usr/bin/env bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() { echo -e "${GREEN}==>${NC} $1"; }
warn() { echo -e "${YELLOW}==>${NC} $1"; }
error() { echo -e "${RED}==>${NC} $1"; exit 1; }

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

info "Setting up manifest-dev development environment..."

# Check/install uv
info "Checking for uv..."
if ! command -v uv &> /dev/null; then
    warn "uv not found. Installing..."
    if ! curl -LsSf https://astral.sh/uv/install.sh | sh; then
        error "Failed to install uv. Please install manually:
    curl -LsSf https://astral.sh/uv/install.sh | sh
Then re-run this script."
    fi
    # Source the shell config to get uv in PATH
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v uv &> /dev/null; then
        error "uv installed but not in PATH. Please restart your shell and re-run this script."
    fi
    info "uv installed successfully"
else
    info "uv found: $(uv --version)"
fi

# Create the virtual environment on Python 3.10 or later. uv picks an installed interpreter that
# fits or fetches one, so the machine's own python3 may be older than that.
if [ -d ".venv" ]; then
    info "Virtual environment already exists, skipping creation"
else
    info "Creating virtual environment..."
    uv venv --python '>=3.10' || error "uv found no Python 3.10 or later and could not fetch one. Install one, then re-run this script."
fi
if ! .venv/bin/python -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
    error "Python 3.10 or later is required, and .venv holds $(.venv/bin/python --version 2>&1). Remove .venv, then re-run this script."
fi
info "Using $(.venv/bin/python --version)"

info "Installing dev dependencies..."
uv pip install --python .venv/bin/python ruff black mypy pytest pytest-xdist pyyaml

# Node runs scripts/verify; its type check needs the dev dependencies in scripts/
info "Checking Node (22.18+, or 23.6+ on Node 23, runs scripts/verify)..."
if command -v node &> /dev/null && node -e 'const [a,b]=process.versions.node.split(".").map(Number);process.exit(a>23||(a===23&&b>=6)||(a===22&&b>=18)?0:1)'; then
    info "Found Node $(node --version)"
    npm --prefix scripts ci --silent
else
    error "Node 22.18 or later (23.6 or later on Node 23) is required for scripts/verify. Install it, then re-run this script."
fi

# The TLA+ tools run the ticket protocol model (verification/recipes/ticket-protocol-model.md).
# The download is pinned to one version and checked against its checksum before it is kept.
PIN="verification/models/tla2tools.pin"
TLA_URL="$(sed -n 's/^url=//p' "$PIN")"
TLA_SHA="$(sed -n 's/^sha256=//p' "$PIN")"
TLA_JAR=".tools/tla2tools.jar"
sha256_of() { (sha256sum "$1" 2>/dev/null || shasum -a 256 "$1") | cut -d' ' -f1; }
info "Checking the TLA+ tools ($(sed -n 's/^version=//p' "$PIN"))..."
if [ -f "$TLA_JAR" ] && [ "$(sha256_of "$TLA_JAR")" = "$TLA_SHA" ]; then
    info "Found the pinned TLA+ tools"
else
    mkdir -p .tools
    if ! curl -fsSL -o "$TLA_JAR.download" "$TLA_URL"; then
        rm -f "$TLA_JAR.download"
        warn "Could not download $TLA_URL. Only the ticket protocol model needs it; that recipe reports unreachable until it is here."
    elif [ "$(sha256_of "$TLA_JAR.download")" != "$TLA_SHA" ]; then
        rm -f "$TLA_JAR.download"
        error "The TLA+ tools downloaded from $TLA_URL do not match the checksum in $PIN; nothing was kept."
    else
        mv "$TLA_JAR.download" "$TLA_JAR"
        info "Installed the pinned TLA+ tools at $TLA_JAR"
    fi
fi
if ! "${JAVA_HOME:+$JAVA_HOME/bin/}java" -version &> /dev/null; then
    warn "No Java runtime found. Only the ticket protocol model needs it: install Java 11 or newer to run that recipe."
fi

# Verify installations
info "Verifying installations..."
.venv/bin/ruff --version
.venv/bin/black --version
.venv/bin/mypy --version
.venv/bin/pytest --version
.venv/bin/python -c "import xdist, yaml"

echo ""
info "Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "Development commands:"
echo "  scripts/check.sh --fix          # Lint and format (fixing), type check, test"
echo "  scripts/check.sh lint|types|tests   # One group; without --fix lint only reports"
