#!/usr/bin/env bash
# The principles-from-history project recorded at surfaces v14, its context file carrying one
# Taste entry that only design work needs, one that guides every session, and two operating-rule
# sections that are not principles: the setup-project
# recipe's principles-from-v14 scenario.
set -euo pipefail
bash "$(dirname "$0")/../principles-from-history/scaffold.sh"
sed -i.bak 's/surfaces v15 -->/surfaces v14 -->/' CLAUDE.md && rm -f CLAUDE.md.bak
cat >> CLAUDE.md <<'EOF'

## Releases

When changing anything under `src/`, bump `version` in `pyproject.toml`: patch for fixes, minor for
features. Update `CHANGELOG.md` in the same change.

## Before PR

Run `python3 -m pytest tests/` and paste its last line into the pull request.

## Taste

- When a design choice decides how loud a screen is, prefer the quieter option — members open Pollbox in the middle of a meeting and a loud screen pulls attention from the room. Yields when the screen must interrupt, such as a poll closing.
- Prefer one small pull request per change over a batched one — Dana reviews on her phone between meetings and loses her place in long diffs. Yields when the changes cannot land apart.
EOF
git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -qam "docs: record taste"
