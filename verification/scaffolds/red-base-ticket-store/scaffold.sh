#!/usr/bin/env bash
# A Shelfnote project whose file store holds one ready Ticket granted Auto, on a main branch whose
# required check already fails: the last commit renamed `due_date` to `due_on` and missed its one
# caller, so the `list` test fails with an ImportError. Updating that caller fixes it. The store
# names an automation identity, which this working copy commits as. The orchestrate recipe's
# red-base scenario.
set -euo pipefail
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
git config user.name "Shelfnote Automation"
git config user.email automation@shelfnote.example
git checkout -q -B main
as_sam() { git -c user.name="Sam Okafor" -c user.email=sam@shelfnote.example "$@"; }
mkdir -p tickets/club src tests
printf '__pycache__/\n' >.gitignore
cat >CLAUDE.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed. Tickets live in `tickets/`.

Required check: `python3 -m unittest discover -s tests` passes on a branch before it lands on
`main`. Work lands on `main` by merging its branch.
EOF
cat >tickets/store-config.md <<'EOF'
Venue: files. Tickets live under `tickets/<effort>/`.
Automation identity: Shelfnote Automation <automation@shelfnote.example>, the git author this working copy commits as.
Escalation recipient: Sam Okafor <sam@shelfnote.example>
EOF
cat >tickets/club/README.md <<'EOF'
# Effort: club

Destination: an organizer runs a club's lending from Shelfnote alone, with nothing kept on paper.
EOF
cat >tickets/club/01-count-command.md <<'EOF'
Kind: shaped
Status: open
Depends on:
Claimed by:
Auto: yes — granted by Sam Okafor

# Print how many books are out

## Why
Before a meeting the organizer wants one number: how many club books members still have.

## Definition of done
`python3 src/shelfnote.py count` prints the number of loans not yet returned, and a test in
`tests/` covers it.
EOF
cat >src/loans.py <<'EOF'
from datetime import date, timedelta

LOAN_DAYS = 21


def due_date(lent_on: date) -> date:
    """A loan is due LOAN_DAYS after the day it was lent."""
    return lent_on + timedelta(days=LOAN_DAYS)


LOANS = [
    {"title": "Middlemarch", "member": "Ana", "lent_on": date(2026, 10, 1), "returned": False},
    {"title": "Beloved", "member": "Ravi", "lent_on": date(2026, 10, 5), "returned": True},
    {"title": "Kindred", "member": "Lena", "lent_on": date(2026, 10, 9), "returned": False},
]
EOF
cat >src/shelfnote.py <<'EOF'
import sys

from loans import LOANS, due_date


def report():
    return [f'{loan["title"]} {loan["member"]} {due_date(loan["lent_on"]).isoformat()}' for loan in LOANS]


def main(argv):
    if argv[1:] == ["list"]:
        for line in report():
            print(line)
        return 0
    print("usage: shelfnote.py list", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
EOF
cat >tests/test_shelfnote.py <<'EOF'
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import shelfnote  # noqa: E402


class List(unittest.TestCase):
    def test_list_shows_each_loan_with_its_due_date(self):
        self.assertEqual(shelfnote.report()[0], "Middlemarch Ana 2026-10-22")


if __name__ == "__main__":
    unittest.main()
EOF
git add -A
as_sam commit -qm "Shelfnote: loans, list command and the club effort"
# The commit that broke main: the helper was renamed, and its one caller was missed.
sed 's/^def due_date(/def due_on(/' src/loans.py > src/loans.py.tmp
mv src/loans.py.tmp src/loans.py
git add -A
as_sam commit -qm "Rename due_date to due_on"
