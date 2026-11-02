#!/usr/bin/env bash
# A Shelfnote project whose file store holds one ready Ticket granted Auto, on a main branch whose
# required check already fails: a date helper returns a loan's due date a day early, and its test
# says so. A small code change fixes it. The orchestrate recipe's red-base scenario.
set -euo pipefail
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
git config user.name "Sam Okafor"
git config user.email sam@shelfnote.example
git checkout -q -B main
mkdir -p tickets/club src tests
printf '__pycache__/\n' > .gitignore
cat > CLAUDE.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed. Tickets live in `tickets/`.

Required check: `python3 -m unittest discover -s tests` passes on a branch before it lands on
`main`. Work lands on `main` by merging its branch.
EOF
cat > tickets/store-config.md <<'EOF'
Venue: files. Tickets live under `tickets/<effort>/`.
EOF
cat > tickets/club/README.md <<'EOF'
# Effort: club

Destination: an organizer runs a club's lending from Shelfnote alone, with nothing kept on paper.
EOF
cat > tickets/club/01-count-command.md <<'EOF'
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
cat > src/loans.py <<'EOF'
from datetime import date, timedelta

LOAN_DAYS = 21


def due_date(lent_on: date) -> date:
    """A loan is due LOAN_DAYS after the day it was lent."""
    return lent_on + timedelta(days=LOAN_DAYS - 1)


LOANS = [
    {"title": "Middlemarch", "member": "Ana", "lent_on": date(2026, 10, 1), "returned": False},
    {"title": "Beloved", "member": "Ravi", "lent_on": date(2026, 10, 5), "returned": True},
    {"title": "Kindred", "member": "Lena", "lent_on": date(2026, 10, 9), "returned": False},
]
EOF
cat > src/shelfnote.py <<'EOF'
import sys

from loans import LOANS, due_date


def overdue(today):
    return [loan for loan in LOANS if not loan["returned"] and due_date(loan["lent_on"]) < today]


def main(argv):
    if argv[1:] == ["list"]:
        for loan in LOANS:
            print(loan["title"], loan["member"], due_date(loan["lent_on"]).isoformat())
        return 0
    print("usage: shelfnote.py list", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
EOF
cat > tests/test_loans.py <<'EOF'
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from loans import due_date  # noqa: E402


class DueDate(unittest.TestCase):
    def test_a_loan_is_due_three_weeks_after_it_was_lent(self):
        self.assertEqual(due_date(date(2026, 10, 1)), date(2026, 10, 22))


if __name__ == "__main__":
    unittest.main()
EOF
git add -A
git commit -qm "Shelfnote: loans, list command and the club effort"
