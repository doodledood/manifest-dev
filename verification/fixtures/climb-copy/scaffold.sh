#!/usr/bin/env bash
# A short About page in its owner's own voice, with a local bare remote so a push is detectable.
set -euo pipefail
# Copy the fixture tree, minus bytecode a local test run may have left in it.
cp -R "$DRIVE_CHECKOUT/verification/fixtures/climb-copy/files/." .
find . -name __pycache__ -type d -prune -exec rm -rf {} +
git init -q --bare ../remote.git
git remote add origin "$(cd .. && pwd)/remote.git"
