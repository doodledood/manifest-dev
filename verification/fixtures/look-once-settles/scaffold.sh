#!/usr/bin/env bash
# The look-once-settles scenario of verification/recipes/do.md: a run resumed after the first
# full looks, with one look-once gate and one look-again gate and a repair batch pending.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp "$fixture"/{manifest.md,inventory.py,test_inventory.py} .
git config user.name 'Look-once fixture'
git config user.email 'look-once@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Add the low-stock report'
head=$(git rev-parse HEAD)
cat > execution-log.md <<LOG
# Low-stock report execution
Repository: local scratch project

## Build done
Deliverable 1 is built at $head. INV-G2 passes (\`python3 -m unittest -q\`: 1 test, OK).

## First full looks at $head
- AC-1.1 first full look (change-intent, code-bugs on inventory.py): FAIL.
  - F-3, High: \`low_stock\` raises KeyError for an item with no \`qty\` key; the claim says it
    counts as 0. Trigger: \`low_stock([{"name": "salt"}], 3)\`.
- INV-G3 full look of record (test-quality, code-maintainability on test_inventory.py): FAIL.
  - F-1, Medium: no test covers an item without \`qty\`, so F-3's behavior is unprotected.
  - F-2, Medium: the test compares sets, so a result in the wrong order still passes; the
    Outcome requires names sorted by name.
  - F-4, Low: the test name \`test_reports_items_below_threshold\` could say the threshold is
    exclusive.
- The repair batch for F-1, F-2, F-3 and F-4 has not started.
LOG
