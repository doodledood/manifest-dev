#!/usr/bin/env bash
# Scratch copy of this repository at the commit carrying the v4 guidance, its surfaces still at v3.
# A drive passes the checkout's path as DRIVE_CHECKOUT and runs this in the scratch project.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
checkout="${DRIVE_CHECKOUT:?run this through scripts/drive-skill.sh --scaffold, which sets DRIVE_CHECKOUT}"
commit=9207ee6523075b192001948012b1e63b8388f603
git -C "$checkout" cat-file -e "$commit^{commit}" 2>/dev/null || {
  echo "this scaffold needs commit $commit, which a shallow clone lacks; run: git fetch --unshallow origin" >&2
  exit 2
}
git -C "$checkout" archive "$commit" | tar -x
