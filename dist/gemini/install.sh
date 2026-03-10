#!/usr/bin/env bash
#
# manifest-dev Gemini CLI Extension Installer
#
# Idempotent installer that downloads and installs the manifest-dev
# extension for Gemini CLI. Safe to run multiple times.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash
#
# What it does:
#   1. Downloads the latest dist/gemini from the repo
#   2. Namespaces all components with -manifest-dev suffix (avoids collisions)
#   3. Installs to ~/.gemini/extensions/manifest-dev/
#   4. Never overwrites user customizations in GEMINI.md
#
set -euo pipefail

REPO="doodledood/manifest-dev"
BRANCH="main"
INSTALL_DIR="${HOME}/.gemini/extensions/manifest-dev"
TMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "==> Downloading manifest-dev extension..."

# Download repo tarball
TARBALL_URL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.tar.gz"
curl -fsSL "$TARBALL_URL" -o "${TMP_DIR}/repo.tar.gz"

# Extract dist/gemini from tarball
tar xzf "${TMP_DIR}/repo.tar.gz" -C "$TMP_DIR"

# Find the extracted directory (manifest-dev-main or similar)
EXTRACTED_DIR=$(ls -d "${TMP_DIR}"/manifest-dev-*/ 2>/dev/null | head -1)
if [ -z "$EXTRACTED_DIR" ]; then
    echo "ERROR: Could not find extracted repo directory" >&2
    exit 1
fi

SOURCE_DIR="${EXTRACTED_DIR}dist/gemini"
if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: dist/gemini not found in downloaded repo" >&2
    exit 1
fi

# Namespace all components in source before installing
echo "==> Namespacing components..."
python3 "${SOURCE_DIR}/install_helpers.py" namespace "$SOURCE_DIR" gemini

# Create install directory
mkdir -p "$INSTALL_DIR"

echo "==> Installing to ${INSTALL_DIR}..."

# Agents (selective cleanup: remove only our namespaced files, preserve others)
if [ -d "${SOURCE_DIR}/agents" ]; then
    mkdir -p "${INSTALL_DIR}/agents"
    find "${INSTALL_DIR}/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
    cp -r "${SOURCE_DIR}/agents/"* "${INSTALL_DIR}/agents/"
    echo "    agents/ ($(ls "${INSTALL_DIR}/agents" | wc -l | tr -d ' ') files)"
fi

# Skills (selective cleanup: remove only our namespaced dirs)
if [ -d "${SOURCE_DIR}/skills" ]; then
    mkdir -p "${INSTALL_DIR}/skills"
    find "${INSTALL_DIR}/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
    cp -r "${SOURCE_DIR}/skills/"* "${INSTALL_DIR}/skills/"
    echo "    skills/ ($(ls "${INSTALL_DIR}/skills" | wc -l | tr -d ' ') dirs)"
fi

# Hooks (extension-private dir, safe to overwrite entirely)
if [ -d "${SOURCE_DIR}/hooks" ]; then
    rm -rf "${INSTALL_DIR}/hooks"
    cp -r "${SOURCE_DIR}/hooks" "${INSTALL_DIR}/hooks"
    chmod +x "${INSTALL_DIR}/hooks/"*.py 2>/dev/null || true
    echo "    hooks/ ($(ls "${INSTALL_DIR}/hooks" | wc -l | tr -d ' ') files)"
fi

# Copy extension manifest (always overwrite)
if [ -f "${SOURCE_DIR}/gemini-extension.json" ]; then
    cp "${SOURCE_DIR}/gemini-extension.json" "${INSTALL_DIR}/gemini-extension.json"
    echo "    gemini-extension.json"
fi

# Copy GEMINI.md (always update -- backup existing first)
if [ -f "${SOURCE_DIR}/GEMINI.md" ]; then
    if [ -f "${INSTALL_DIR}/GEMINI.md" ]; then
        cp "${INSTALL_DIR}/GEMINI.md" "${INSTALL_DIR}/GEMINI.md.bak"
        cp "${SOURCE_DIR}/GEMINI.md" "${INSTALL_DIR}/GEMINI.md"
        echo "    GEMINI.md (updated, backup at GEMINI.md.bak)"
    else
        cp "${SOURCE_DIR}/GEMINI.md" "${INSTALL_DIR}/GEMINI.md"
        echo "    GEMINI.md (new)"
    fi
fi

# Copy README
if [ -f "${SOURCE_DIR}/README.md" ]; then
    cp "${SOURCE_DIR}/README.md" "${INSTALL_DIR}/README.md"
    echo "    README.md"
fi

echo ""
echo "==> Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Enable agents in settings.json:"
echo '     { "experimental": { "enableAgents": true } }'
echo ""
echo "  2. Merge hooks into your settings.json (see hooks/hooks.json)"
echo ""
echo "  3. Start using: gemini> /define-manifest-dev my task"
echo ""
echo "Installed to: ${INSTALL_DIR}"
