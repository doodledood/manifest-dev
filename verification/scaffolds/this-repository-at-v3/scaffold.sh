#!/usr/bin/env bash
# Scratch copy of this repository at the commit carrying the v4 guidance, its surfaces still at v3.
set -euo pipefail
git -c safe.directory='*' -C /repo archive 9207ee65 | tar -x
