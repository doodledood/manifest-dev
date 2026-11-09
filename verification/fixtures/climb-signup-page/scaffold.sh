#!/usr/bin/env bash
# A main sign-up page with its traffic stated and no way to test on real visitors.
set -euo pipefail
# Copy the fixture tree, minus bytecode a local test run may have left in it.
cp -R "$DRIVE_CHECKOUT/verification/fixtures/climb-signup-page/files/." .
find . -name __pycache__ -type d -prune -exec rm -rf {} +
