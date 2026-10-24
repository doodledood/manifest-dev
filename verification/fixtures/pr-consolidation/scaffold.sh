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
git switch -qc feature/export
cp "$fixture/before.py" order_export.py
git add order_export.py
git commit -qm 'Add order export'
reviewed=$(git rev-parse HEAD)
cp "$fixture/current.py" order_export.py
git add order_export.py
git commit -qm 'Remove private note from export'
cp "$fixture/review.json" .
python3 -B - "$reviewed" "$(git rev-parse HEAD)" <<'PY'
import json
import sys
from pathlib import Path

path = Path("review.json")
packet = json.loads(path.read_text())
packet["reviewed_commit"] = sys.argv[1]
packet["current_commit"] = sys.argv[2]
packet["reviewed_range"] = f"{sys.argv[1]}..{sys.argv[2]}"
path.write_text(json.dumps(packet, indent=2) + "\n")
PY
