#!/usr/bin/env bash
# The scratch project is this repository at its last commit. A drive mounts the checkout
# read-only at /repo; uncommitted changes are not in the copy.
set -euo pipefail
git -c safe.directory='*' -C /repo archive HEAD | tar -x
