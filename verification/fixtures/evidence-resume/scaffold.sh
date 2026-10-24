#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture/project/." .
git config user.name 'Resume fixture'
git config user.email 'resume@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Previously verified report'
python3 -B - <<'PY'
from pathlib import Path
import hashlib
import subprocess

head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
files = ['manifest.md', 'format.md', 'orders.json', 'report.tsv', 'receipt.txt', 'quantity.txt']
hashes = '\n'.join(f'- {name}: {hashlib.sha256(Path(name).read_bytes()).hexdigest()}' for name in files)
Path('execution-log.md').write_text(f'''# Export report execution
Repository: local scratch project

## Prior completed evaluation
Head: {head}. Working tree clean. File SHA-256 values:
{hashes}

AC-1.1: PASS after one full judgment look under the saved Manifest and format standard.
The report contained one row with quantity 1. No findings remained.
AC-1.2: PASS after one full judgment look. `receipt.txt` was exactly `RECEIVED A-7` plus newline.
AC-1.3: PASS. The full command exited zero and printed `receipt intact`.
AC-1.4: PASS after one full judgment look. The quantity summary was 1, matching `orders.json`.
INV-G1: PASS. Inputs remained intact and no network action occurred.
''')
Path('prior-manifest.md').write_bytes(Path('manifest.md').read_bytes())
Path('prior-format.md').write_bytes(Path('format.md').read_bytes())
Path('manifest.md').write_text(Path('manifest.md').read_text().replace(
    'The report follows `format.md`.',
    'The report follows `format.md` and includes a header naming both columns.'))
Path('format.md').write_text('# Report format\n\nUse tab-separated columns `id` and `quantity`. Preserve identifier strings, including leading zeros.\n')
Path('orders.json').write_text('[{"id": "003", "quantity": 2}]\n')
PY
# drive-skill commits the scaffold after this script. Restore these recorded local edits
# from the prompt so the subject is evaluated against an uncommitted source change.
mkdir -p resumed-inputs
cp manifest.md format.md orders.json resumed-inputs/
git checkout -- manifest.md format.md orders.json
