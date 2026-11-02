#!/usr/bin/env bash
# The Taste test, principle-plus-case arm: the same entry with one case line from a different gate.
set -euo pipefail
cat > CLAUDE.md <<'EOF'
# Larder

A recipe site with a small shop that posts spice kits.

## Taste

- Prefer the route with the fewest steps between what the person asked for and getting it: at a gate such as sign-in or payment, show only the gate's own choice and ask for nothing a later step could ask. The owner's reason: every extra step loses people. Yield when the person needs a step to decide, or to trust what comes next.
  - Case: a newsletter sign-up form that also asked for job title and company size was rejected: "just the email field."
EOF
