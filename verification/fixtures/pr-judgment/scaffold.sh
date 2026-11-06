#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
git branch -M main
git config user.name 'Review fixture'
git config user.email 'review@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p docs
cp "$fixture/README.md" .
cp "$fixture/purpose.md" docs/purpose.md
cp "$fixture/decisions.md" docs/decisions.md
cp "$fixture/catalog.json" .
cp "$fixture/base.py" recommendations.py
git add README.md docs catalog.json recommendations.py
git commit -qm 'Seed catalog and product context'
git switch -qc feature/sponsor-shelf
cp "$fixture/head.py" recommendations.py
git add recommendations.py
git commit -qm 'Reserve three shelf slots for sponsors'
cp "$fixture/pr.json" .
mkdir -p snapshots
cp "$fixture/reply-authority.md" "$fixture/reply-decision.md" "$fixture/reply-late.md" "$fixture/late.py" snapshots/
python3 -B - <<'INNER'
import json
import subprocess
from pathlib import Path
p=Path('pr.json')
s=json.loads(p.read_text())
s['base']=subprocess.check_output(['git','rev-parse','main'],text=True).strip()
s['head']=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
p.write_text(json.dumps(s,indent=2)+'\n')
INNER
