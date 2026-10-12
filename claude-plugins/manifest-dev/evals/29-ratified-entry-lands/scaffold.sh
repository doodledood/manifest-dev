#!/usr/bin/env bash
set -euo pipefail
cat > CLAUDE.md <<'EOF'
# Pawprint Grooming

Booking app for a dog-grooming salon with three groomers.

## Commands

- `npm test` runs the unit tests.
- `npm run e2e` runs the booking journeys in a browser.

## Taste

- Prefer showing the groomer's photo next to every slot — owners pick the person, not the time; yield on screens too small to show it legibly.

## Deploy

Merges to `main` deploy to production. Never merge without the owner's yes.
EOF
