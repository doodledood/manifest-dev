#!/usr/bin/env bash
# A function already at its best: a dict lookup and one multiply, where only noise-level
# changes remain.
set -euo pipefail
cp "$DRIVE_CHECKOUT/verification/fixtures/climb-at-best/files/"* .
