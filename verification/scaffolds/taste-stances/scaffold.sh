#!/usr/bin/env bash
# The Taste test, stance-only arm: the same project context file with no Taste entry.
set -euo pipefail
cat > CLAUDE.md <<'EOF'
# Larder

A recipe site with a small shop that posts spice kits.
EOF
