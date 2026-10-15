#!/usr/bin/env bash
# A project that never chose how to verify: no context file, no harness, a pytest suite of its own.
# The one test that claims to cover the overdue list runs it with no loans and checks only the exit code.
set -euo pipefail
mkdir -p src tests
cat > README.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed. A loan is overdue 21 days after
checkout.

    python -m shelfnote checkout --member ana --book "Middlemarch"
    python -m shelfnote return --book "Middlemarch"
    python -m shelfnote overdue

Run `python -m pytest` before a release.
EOF
cat > src/shelfnote.py <<'EOF'
import argparse, datetime, json, pathlib
DATA = pathlib.Path("data/loans.json")
LOAN_DAYS = 21
def load():
    return json.loads(DATA.read_text()) if DATA.exists() else []
def overdue(loans, today):
    due = lambda loan: datetime.date.fromisoformat(loan["out"]) + datetime.timedelta(days=LOAN_DAYS)
    return [loan for loan in loans if not loan.get("returned") and due(loan) < today]
def main(argv=None):
    p = argparse.ArgumentParser(prog="shelfnote")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("checkout"); c.add_argument("--member"); c.add_argument("--book")
    r = sub.add_parser("return"); r.add_argument("--book")
    sub.add_parser("overdue")
    args = p.parse_args(argv)
    if args.cmd == "overdue":
        for loan in overdue(load(), datetime.date.today()):
            print(loan["member"], loan["book"])
if __name__ == "__main__":
    main()
EOF
cat > tests/test_overdue.py <<'EOF'
"""Covers the overdue list."""
import subprocess, sys

def test_overdue_list():
    result = subprocess.run([sys.executable, "src/shelfnote.py", "overdue"], capture_output=True)
    assert result.returncode == 0
EOF
cat > tests/test_checkout.py <<'EOF'
import sys
sys.path.insert(0, "src")
import shelfnote

def test_parser_knows_checkout():
    shelfnote.main(["checkout", "--member", "ana", "--book", "Middlemarch"])
EOF
