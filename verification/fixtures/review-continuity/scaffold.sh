#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
git branch -M main
git config user.name 'Review fixture'
git config user.email 'review@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
cp "$fixture/contract.md" .
git add contract.md
git commit -qm contract
git update-ref refs/remotes/origin/main HEAD
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main
git switch -qc feature/export
cp "$fixture/initial.py" order_export.py
git add order_export.py
git commit -qm 'Add order export'
reviewed=$(git rev-parse HEAD)
cp "$fixture/repaired.py" order_export.py
git add order_export.py
git commit -qm 'Remove private note from export'
cp "$fixture/prior-review.md" .
printf '\nReviewed commit: `%s`. Scope: `order_export.py` against `main`.\n' "$reviewed" >> prior-review.md
