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
#   4. Merges enableAgents + hooks into ~/.gemini/settings.json additively
#
set -euo pipefail

REPO="doodledood/manifest-dev"
BRANCH="main"
INSTALL_DIR="${HOME}/.gemini/extensions/manifest-dev"
SETTINGS_FILE="${HOME}/.gemini/settings.json"
SCRIPT_SOURCE="${BASH_SOURCE[0]-}"
SCRIPT_DIR=""
if [ -n "$SCRIPT_SOURCE" ] && [ -f "$SCRIPT_SOURCE" ]; then
    SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_SOURCE")" && pwd)"
fi
TMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/install_helpers.py" ] && [ -d "$SCRIPT_DIR/skills" ] && [ -d "$SCRIPT_DIR/agents" ] && [ -d "$SCRIPT_DIR/hooks" ] && [ -f "$SCRIPT_DIR/gemini-extension.json" ]; then
    echo "==> Using local dist/gemini from ${SCRIPT_DIR}..."
    SOURCE_DIR="${TMP_DIR}/local-dist"
    mkdir -p "$SOURCE_DIR"
    cp -R "$SCRIPT_DIR"/. "$SOURCE_DIR"/
else
    echo "==> Downloading manifest-dev extension..."

    TARBALL_URL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.tar.gz"
    curl -fsSL "$TARBALL_URL" -o "${TMP_DIR}/repo.tar.gz"

    tar xzf "${TMP_DIR}/repo.tar.gz" -C "$TMP_DIR"

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
fi

echo "==> Namespacing components..."
python3 "${SOURCE_DIR}/install_helpers.py" namespace "$SOURCE_DIR" gemini

mkdir -p "$INSTALL_DIR"

echo "==> Installing to ${INSTALL_DIR}..."

if [ -d "${SOURCE_DIR}/agents" ]; then
    mkdir -p "${INSTALL_DIR}/agents"
    find "${INSTALL_DIR}/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
    cp -r "${SOURCE_DIR}/agents/"* "${INSTALL_DIR}/agents/"
    echo "    agents/ ($(ls "${INSTALL_DIR}/agents" | wc -l | tr -d ' ') files)"
fi

if [ -d "${SOURCE_DIR}/skills" ]; then
    mkdir -p "${INSTALL_DIR}/skills"
    find "${INSTALL_DIR}/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
    cp -r "${SOURCE_DIR}/skills/"* "${INSTALL_DIR}/skills/"
    echo "    skills/ ($(ls "${INSTALL_DIR}/skills" | wc -l | tr -d ' ') dirs)"
fi

if [ -d "${SOURCE_DIR}/hooks" ]; then
    rm -rf "${INSTALL_DIR}/hooks"
    cp -r "${SOURCE_DIR}/hooks" "${INSTALL_DIR}/hooks"
    chmod +x "${INSTALL_DIR}/hooks/"*.py 2>/dev/null || true
    echo "    hooks/ ($(ls "${INSTALL_DIR}/hooks" | wc -l | tr -d ' ') files)"
fi

if [ -f "${SOURCE_DIR}/gemini-extension.json" ]; then
    cp "${SOURCE_DIR}/gemini-extension.json" "${INSTALL_DIR}/gemini-extension.json"
    echo "    gemini-extension.json"
fi

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

if [ -f "${SOURCE_DIR}/README.md" ]; then
    cp "${SOURCE_DIR}/README.md" "${INSTALL_DIR}/README.md"
    echo "    README.md"
fi

mkdir -p "$(dirname "$SETTINGS_FILE")"
if [ -f "$SETTINGS_FILE" ]; then
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.bak"
    python3 "${SOURCE_DIR}/install_helpers.py" merge-settings "${INSTALL_DIR}/hooks/hooks.json" "$SETTINGS_FILE"
    echo "    settings.json (merged, backup at settings.json.bak)"
else
    python3 "${SOURCE_DIR}/install_helpers.py" merge-settings "${INSTALL_DIR}/hooks/hooks.json" "$SETTINGS_FILE"
    echo "    settings.json (created with enableAgents + manifest-dev hooks)"
fi

echo ""
echo "==> Installation complete!"
echo ""
echo "No manual settings changes are required."
echo "Start a Gemini session and ask it to use the define-manifest-dev skill for your task."
echo ""
echo "Installed to: ${INSTALL_DIR}"
