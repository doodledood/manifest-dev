#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp "$fixture"/{manifest.md,display.py,check.py} .
git config user.name 'Convergence fixture'
git config user.email 'convergence@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Add readable labels and fee calculation'
python3 - <<'PY'
from pathlib import Path
p = Path('display.py')
p.write_text(p.read_text().replace('text.strip()', 'text.strip(" ")'))
PY
git add display.py
git commit -qm 'Normalize whitespace for every label'
python3 - <<'PY'
from pathlib import Path
p = Path('display.py')
p.write_text(p.read_text().replace('text.strip(" ")', 'text.strip()'))
PY
git add display.py
git commit -qm 'Make every Unicode label spacing canonical'
head=$(git rev-parse HEAD)
cat > execution-log.md <<EOF
# Label and fee execution
Repository: local scratch project

## Prior gate evaluations at $head
The first full look is complete. AC-1.1 found the labels readable; AC-1.2 has
an unresolved fee error. The implementation file and check are display.py and check.py.

Related repairs, both on the promise "all Unicode label spacing is canonical":
- F-12, Low: extra label padding for a narrow Unicode case. Changed strip handling.
  The continued change-intent look still returned FAIL for F-17, a different spacing case.
- F-17, Low: normalize every label's whitespace. Changed strip handling again.
  The continued look returned FAIL for F-39, yet another cosmetic spacing case.
- F-39, Low remains open: labels with an internal thin space are not normalized.
  The finding cites the latest repair commit's "every Unicode label" wording.

New findings from that continued look:
- F-40, Low: rename text to raw_text in label. Both names are clear; this is an
  naming nit, with no correctness or maintenance cost.
- F-41, Low: extract label's strip call into a separate private helper. This is
  an structural nit; it identifies no must-fix quality gap.

F-22, received as Low, remains open: net_after_fee(100, 1) is 100 rather than 99.
Its prior reviewer called it Low because fee=1 is unusual and callers can subtract it manually.
The current deterministic check has not passed. No unrelated pre-existing issues were reported.
EOF
