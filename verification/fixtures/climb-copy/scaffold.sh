#!/usr/bin/env bash
# A short About page in its owner's own voice, with a local bare remote so a push is detectable.
set -euo pipefail
cp "$DRIVE_CHECKOUT/verification/fixtures/climb-copy/files/"* .
git init -q --bare ../remote.git
git remote add origin "$(cd .. && pwd)/remote.git"
