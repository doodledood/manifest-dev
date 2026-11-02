#!/usr/bin/env bash
# The journeys-gate fixture app, with its five seeded journey defects, for define's journeys-gate scenarios.
set -euo pipefail
# A drive passes the checkout in DRIVE_CHECKOUT; run by hand, the checkout is found from here.
checkout=${DRIVE_CHECKOUT:-$(cd "$(dirname "$0")/../../.." && pwd)}
# The two arms differ only by the patch.
DRIVE_CHECKOUT=$checkout bash "$checkout/verification/scaffolds/journeys-app-fixed/scaffold.sh"
patch -s -p1 -d app <"$checkout/verification/fixtures/journeys-app/seeded.patch"
