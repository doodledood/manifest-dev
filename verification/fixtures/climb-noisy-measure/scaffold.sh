#!/usr/bin/env bash
# A function whose only benchmark is dominated by a random stall far larger than the function's
# own cost, so no number of runs tells a known-worse version from the original; nothing else times it.
set -euo pipefail
cp "$DRIVE_CHECKOUT/verification/fixtures/climb-noisy-measure/files/"* .
