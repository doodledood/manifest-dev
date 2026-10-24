#!/usr/bin/env bash
set -euo pipefail
mkdir -p src tests data
cat > README.md <<'EOF'
# Shelfnote

Overdue reminders for a reading club. Run `python3 src/shelfnote.py overdue`.
The current club-wide loan length is 21 days. Each member's `loan_days` is already stored,
but reminder generation does not use it yet.

Verification: `python3 -m unittest discover -s tests`.
EOF
cat > data/loans.json <<'EOF'
[{"book": "Middlemarch", "member": "ana"}]
EOF
cat > data/members.json <<'EOF'
{"ana": {"loan_days": 28}}
EOF
cat > src/shelfnote.py <<'EOF'
import argparse
import json
from pathlib import Path
from reminders import cli


def main():
    parser = argparse.ArgumentParser(prog="shelfnote")
    parser.add_argument("command", choices=["overdue"])
    parser.parse_args()
    loans = json.loads(Path("data/loans.json").read_text())
    print("\n".join(cli(loans)))


if __name__ == "__main__":
    main()
EOF
cat > src/reminders.py <<'EOF'
LOAN_DAYS = 21

def cli(loans, days=21): return scheduler(loans, days)
def scheduler(loans, days): return [reminder(loan, days) for loan in loans]
def reminder(loan, days): return format_line(loan, days or LOAN_DAYS)
def format_line(loan, days): return f"{loan['book']} due in {days or LOAN_DAYS} days"
EOF
cat > tests/test_reminders.py <<'EOF'
import subprocess
import sys
import unittest


class ExistingReminderBehavior(unittest.TestCase):
    def test_cli_uses_club_wide_loan_length(self):
        result = subprocess.run([sys.executable, "src/shelfnote.py", "overdue"],
                                text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, "Middlemarch due in 21 days\n")
EOF
