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

# Check Python version (>= 3.10)
info "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed. Please install Python 3.10 or later."
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; }; then
    error "Python 3.10 or later is required. Found: Python $PYTHON_VERSION"
fi
info "Found Python $PYTHON_VERSION"

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

# Create virtual environment (skip if exists)
if [ -d ".venv" ]; then
    info "Virtual environment already exists, skipping creation"
else
    info "Creating virtual environment..."
    uv venv
fi

# Install dev dependencies into the venv
info "Installing dev dependencies..."
uv pip install --python .venv/bin/python ruff black mypy pytest

# Verify installations
info "Verifying installations..."
.venv/bin/ruff --version
.venv/bin/black --version
.venv/bin/mypy --version
.venv/bin/pytest --version

echo ""
info "Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "Development commands:"
echo "  ruff check --fix claude-plugins/   # Lint"
echo "  black claude-plugins/              # Format"
echo "  mypy                               # Type check"
echo "  pytest tests/hooks/ -v             # Run tests"
