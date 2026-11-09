#!/usr/bin/env bash
# A function already at its best: a dict lookup and one multiply, where only noise-level
# changes remain.
set -euo pipefail
# Copy the fixture tree, minus bytecode a local test run may have left in it.
cp -R "$DRIVE_CHECKOUT/verification/fixtures/climb-at-best/files/." .
find . -name __pycache__ -type d -prune -exec rm -rf {} +
