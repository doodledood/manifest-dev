#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp "$fixture"/{AGENTS.md,totals.py} .
git branch -M main
git config user.name 'Review policy fixture'
git config user.email 'policy@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Add totals and advisory naming convention'
git switch -qc feature/local-name
python3 - <<'PY'
from pathlib import Path
p = Path('totals.py')
p.write_text(p.read_text().replace('total = sum(amounts)\n    return total', 'n = sum(amounts)\n    return n', 1))
PY
git add totals.py
git commit -qm 'Shorten one accumulator name'
