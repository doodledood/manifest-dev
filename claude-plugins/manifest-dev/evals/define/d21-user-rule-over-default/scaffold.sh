#!/usr/bin/env bash
set -euo pipefail
mkdir -p src checks data
cat > README.md <<'EOF'
# Shelfnote

List overdue loans: `python3 src/shelfnote.py overdue`.
`--data PATH` selects another loan-event file. Renewals append an event with the same loan ID;
only its latest due date should decide whether that loan appears.

Verification: `bash checks/overdue.sh`.
EOF
cat > CLAUDE.md <<'EOF'
# Shelfnote

This repository holds no test files. Behavior is checked only through the scripted acceptance
checks in `checks/`; the test suite lives in a separate repository the club does not control.
EOF
cat > data/loans.json <<'EOF'
[{"id": "loan-1", "book": "Middlemarch", "due": "2000-01-01"},
 {"id": "loan-1", "book": "Middlemarch", "due": "2000-02-01"}]
EOF
cat > src/shelfnote.py <<'EOF'
import argparse
from datetime import date
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="shelfnote")
    parser.add_argument("command", choices=["overdue"])
    parser.add_argument("--data", default="data/loans.json")
    args = parser.parse_args()
    events = json.loads(Path(args.data).read_text())
    for event in events:
        if date.fromisoformat(event["due"]) < date.today():
            print(event["book"])


if __name__ == "__main__":
    main()
EOF
cat > checks/overdue.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import json
from pathlib import Path
import subprocess
import sys
import tempfile

with tempfile.TemporaryDirectory() as scratch:
    data = Path(scratch) / 'loans.json'
    data.write_text(json.dumps([{'id': 'loan-1', 'book': 'Middlemarch', 'due': '2000-01-01'}]))
    result = subprocess.run([sys.executable, 'src/shelfnote.py', 'overdue', '--data', str(data)],
                            text=True, capture_output=True, check=True)
    assert result.stdout == 'Middlemarch\n', repr(result.stdout)
PY
EOF
