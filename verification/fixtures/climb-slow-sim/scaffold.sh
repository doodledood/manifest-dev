#!/usr/bin/env bash
# A traffic simulation whose full realism measure is slow and whose quick check reads one still
# frame of one preset, so a version that moves badly can pass it.
set -euo pipefail
cp -R "$DRIVE_CHECKOUT/verification/fixtures/climb-slow-sim/files/". .
