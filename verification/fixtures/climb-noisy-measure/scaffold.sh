#!/usr/bin/env bash
# A function whose only benchmark swings by a factor of ten between runs, so it cannot tell a
# known-worse version from a known-better one; nothing else times it.
set -euo pipefail
cp "$DRIVE_CHECKOUT/verification/fixtures/climb-noisy-measure/files/"* .
