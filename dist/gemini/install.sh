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
#   2. Installs to ~/.gemini/extensions/manifest-dev/
#   3. Never overwrites user customizations in GEMINI.md
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

# Create install directory
mkdir -p "$INSTALL_DIR"

echo "==> Installing to ${INSTALL_DIR}..."

# Copy agents (always overwrite -- these are managed by the extension)
if [ -d "${SOURCE_DIR}/agents" ]; then
    rm -rf "${INSTALL_DIR}/agents"
    cp -r "${SOURCE_DIR}/agents" "${INSTALL_DIR}/agents"
    echo "    agents/ ($(ls "${INSTALL_DIR}/agents" | wc -l | tr -d ' ') files)"
fi

# Copy skills (always overwrite)
if [ -d "${SOURCE_DIR}/skills" ]; then
    rm -rf "${INSTALL_DIR}/skills"
    cp -r "${SOURCE_DIR}/skills" "${INSTALL_DIR}/skills"
    echo "    skills/ ($(ls "${INSTALL_DIR}/skills" | wc -l | tr -d ' ') dirs)"
fi

# Copy hooks (always overwrite)
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

# Copy GEMINI.md only if it doesn't exist (preserve user customizations)
if [ -f "${SOURCE_DIR}/GEMINI.md" ]; then
    if [ ! -f "${INSTALL_DIR}/GEMINI.md" ]; then
        cp "${SOURCE_DIR}/GEMINI.md" "${INSTALL_DIR}/GEMINI.md"
        echo "    GEMINI.md (new)"
    else
        echo "    GEMINI.md (skipped -- preserving existing)"
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
echo "  3. Start using: gemini> /define my task"
echo ""
echo "Installed to: ${INSTALL_DIR}"
