#!/usr/bin/env bash
# The journeys-gate fixture app, with no seeded defect, for define's journeys-gate scenarios.
set -euo pipefail
# A drive passes the checkout in DRIVE_CHECKOUT; run by hand, the checkout is found from here.
checkout=${DRIVE_CHECKOUT:-$(cd "$(dirname "$0")/../../.." && pwd)}
mkdir -p app
cp "$checkout/verification/fixtures/journeys-app/server.js" app/server.js
cat > README.md <<'MD'
# Waymark

A trip planner. This repository holds the Saved places page for a shared trip.

Run it: `node app/server.js` (no dependencies), then open http://localhost:4180/. PORT overrides
the port. Sign in with any email address; state is kept in memory until the server stops.
MD
