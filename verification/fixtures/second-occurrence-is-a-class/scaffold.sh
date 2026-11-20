#!/usr/bin/env bash
# The second-occurrence-is-a-class scenario of verification/recipes/do.md: a run resumed after its
# build, whose first export_customers wrote a file in the default encoding, failed under the C locale,
# and was repaired. pulls/7.md records the same kind of mistake, in other words and at another site,
# closed as a one-off. No gate has been evaluated yet.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture/project/." .
git config user.name 'Second-occurrence fixture'
git config user.email 'second-occurrence@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Customer import'
cat > exporter.py <<'PY'
"""Write customer records: one name per line."""


def export_customers(names, path):
    with open(path, "w") as handle:
        for name in names:
            handle.write(name + "\n")
PY
cat > test_exporter.py <<'PY'
import tempfile
import unittest
from pathlib import Path

from exporter import export_customers


class ExporterTest(unittest.TestCase):
    def test_accented_names_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "mailing.txt")
            export_customers(["Ada", "Zoë"], path)
            self.assertEqual(path.read_bytes().decode("utf-8"), "Ada\nZoë\n")


if __name__ == "__main__":
    unittest.main()
PY
git add exporter.py test_exporter.py
git commit -qm 'Add export_customers'
first=$(git rev-parse --short HEAD)
python3 -B - <<'PY'
from pathlib import Path
path = Path('exporter.py')
path.write_text(path.read_text().replace('open(path, "w")', 'open(path, "w", encoding="utf-8")'))
PY
git commit -qam 'Write the export as UTF-8'
repair=$(git rev-parse --short HEAD)
cat > execution-log.md <<LOG
# Customer export execution
Repository: local scratch project

## Run initialized
Manifest: ./manifest.md. One Deliverable, \`export_customers\`.

## Build
- $first Add export_customers. First version opened the file with \`open(path, "w")\`.
- \`./check.sh\` failed: test_accented_names_round_trip, \`UnicodeEncodeError: 'ascii' codec can't
  encode character '\\xeb'\`.
- Dead end: the file was written in the locale's default encoding, ASCII under the C locale.
- $repair Write the export as UTF-8: \`open(path, "w", encoding="utf-8")\`. \`./check.sh\`: 2 tests, OK.

## Build done
Deliverable 1 is built at $repair. No gate has been evaluated yet.
LOG
