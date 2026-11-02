#!/usr/bin/env bash
# The Taste test, principle arm: a project context file whose Taste entry states the principle alone.
set -euo pipefail
cat > CLAUDE.md <<'EOF'
# Larder

A recipe site with a small shop that posts spice kits.

## Taste

- Prefer the route with the fewest steps between what the person asked for and getting it: at a gate such as sign-in or payment, show only the gate's own choice and ask for nothing a later step could ask. The owner's reason: every extra step loses people. Yield when the person needs a step to decide, or to trust what comes next.
EOF
