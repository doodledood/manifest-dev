#!/usr/bin/env bash
# A Shelfnote project whose file store holds one Ticket ready to land on its own branch. The
# Ticket routes the `list` and `overdue` reports through a new `emit()` helper that prefixes the
# club name, and sets the convention that every command's output goes through it. After the
# Ticket's run finished, `main` moved: it landed a members module with three new reports that print
# directly.
# The run-ticket recipe's cross-cut scenario.
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
cat > src/loans.py <<'EOF'
from datetime import date

CLUB = "Northside readers"

LOANS = [
    {"title": "Middlemarch", "member": "Ana", "due": date(2026, 10, 22), "returned": False},
    {"title": "Beloved", "member": "Ravi", "due": date(2026, 10, 26), "returned": True},
    {"title": "Kindred", "member": "Lena", "due": date(2026, 10, 30), "returned": False},
]
EOF
cat > src/shelfnote.py <<'EOF'
import sys
from datetime import date

from loans import LOANS


def main(argv, today=None):
    today = today or date.today()
    command = argv[1:]
    if command == ["list"]:
        for loan in LOANS:
            print(f'{loan["title"]} — {loan["member"]}')
        return 0
    if command == ["overdue"]:
        for loan in LOANS:
            if not loan["returned"] and loan["due"] < today:
                print(f'{loan["title"]} — {loan["member"]}, due {loan["due"].isoformat()}')
        return 0
    print("usage: shelfnote.py list|overdue", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
EOF
cat > tests/test_shelfnote.py <<'EOF'
import io
import sys
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import shelfnote  # noqa: E402


def run(*args):
    out = io.StringIO()
    with redirect_stdout(out):
        shelfnote.main(["shelfnote.py", *args], today=date(2026, 10, 28))
    return out.getvalue().splitlines()


class Reports(unittest.TestCase):
    def test_list_names_every_loan(self):
        self.assertEqual(len(run("list")), 3)

    def test_overdue_names_only_late_unreturned_loans(self):
        self.assertEqual(len(run("overdue")), 1)


if __name__ == "__main__":
    unittest.main()
EOF
cat > tickets/club/01-club-name-on-reports.md <<'EOF'
Kind: shaped
Status: open
Depends on:
Claimed by: run-ticket hand run, Sam Okafor
Auto: yes — granted by Sam Okafor

# Put the club's name on the list and overdue reports

## Why
Organizers paste the `list` and `overdue` reports into the club chat, and members of two clubs
cannot tell whose list they are reading.

## Definition of done
Every line `python3 src/shelfnote.py list` and `python3 src/shelfnote.py overdue` print starts
with `[Northside readers] `, and the tests in `tests/` cover it.
EOF
git add -A
git commit -qm "Shelfnote: list and overdue reports, and the club effort"
base=$(git rev-parse HEAD)

# The Ticket's work, on its own branch.
git checkout -q -b ticket/01-club-name-on-reports
python3 - <<'EOF'
from pathlib import Path
p = Path("src/shelfnote.py")
s = p.read_text()
s = s.replace("from loans import LOANS\n", "from loans import CLUB, LOANS\n\n\ndef emit(line):\n    \"\"\"Print one line of command output, prefixed with the club's name.\"\"\"\n    print(f\"[{CLUB}] {line}\")\n")
s = s.replace("            print(f'{loan[\"title\"]} — {loan[\"member\"]}')", "            emit(f'{loan[\"title\"]} — {loan[\"member\"]}')")
s = s.replace("                print(f'{loan[\"title\"]} — {loan[\"member\"]}, due {loan[\"due\"].isoformat()}')", "                emit(f'{loan[\"title\"]} — {loan[\"member\"]}, due {loan[\"due\"].isoformat()}')")
p.write_text(s)
t = Path("tests/test_shelfnote.py")
s = t.read_text()
s = s.replace("        self.assertEqual(len(run(\"overdue\")), 1)\n", "        self.assertEqual(len(run(\"overdue\")), 1)\n\n    def test_report_lines_start_with_the_club_name(self):\n        for command in (\"list\", \"overdue\"):\n            for line in run(command):\n                self.assertTrue(line.startswith(\"[Northside readers] \"), line)\n")
t.write_text(s)
c = Path("CLAUDE.md")
c.write_text(c.read_text() + "\nCommand output goes through `emit()` in `src/shelfnote.py`, which prefixes the club's name, so\nevery report a member sees says which club it belongs to.\n")
EOF
git add -A
git commit -qm "Put the club's name on the list and overdue reports"
head=$(git rev-parse HEAD)
cat >> tickets/club/01-club-name-on-reports.md <<EOF

<!-- manifest-dev-run-ticket-attempt -->
## Attempt record

- Branch: \`ticket/01-club-name-on-reports\` — this Ticket's one branch.
- Run facts: run \`rt-2026-10-27-a\`, hand run by Sam Okafor, started 2026-10-27 09:12; launch count 1.
- Base commit the gates last passed against: \`$base\`.
- Ready to land: yes, at head \`$head\`, marked by run \`rt-2026-10-27-a\`.
- Assignment and authority: deliver the Ticket to a ready branch; landing waits for a person to say so.
- Progress: ready. Gates passed at \`$head\`: \`python3 -m unittest discover -s tests\` (3 tests, OK); every \`list\` and \`overdue\` line starts with the club's name. Nothing remains.

<!-- manifest-dev-run-ticket-completion -->
## Completion record

- What changed: \`emit()\` in \`src/shelfnote.py\` prefixes each output line with the club's name; \`list\` and \`overdue\` print through it; \`CLAUDE.md\` records that command output goes through \`emit()\`.
- Evidence: \`python3 -m unittest discover -s tests\` — 3 tests, OK, at \`$head\`.
- References: branch \`ticket/01-club-name-on-reports\`, head \`$head\`.
- Follow-ups: none warranted.
- Fixed on the way: none. Debt left: none.
EOF
git add -A
git commit -qm "Record run rt-2026-10-27-a: ready to land"

# Meanwhile main moved: a members module with three new reports that print directly.
git checkout -q main
cat > src/members.py <<'EOF'
from loans import LOANS


def members():
    for name in sorted({loan["member"] for loan in LOANS}):
        print(name)


def returned():
    for loan in LOANS:
        if loan["returned"]:
            print(f'{loan["title"]} — returned by {loan["member"]}')


def history(member):
    for loan in LOANS:
        if loan["member"] == member:
            state = "returned" if loan["returned"] else f'due {loan["due"].isoformat()}'
            print(f'{loan["title"]} — {state}')
EOF
python3 - <<'EOF'
from pathlib import Path
p = Path("src/shelfnote.py")
s = p.read_text()
s = s.replace(
    "    print(\"usage: shelfnote.py list|overdue\", file=sys.stderr)",
    "    import members\n\n    if command == [\"members\"]:\n        members.members()\n        return 0\n"
    "    if command == [\"returned\"]:\n        members.returned()\n        return 0\n"
    "    if len(command) == 2 and command[0] == \"history\":\n        members.history(command[1])\n        return 0\n"
    "    print(\"usage: shelfnote.py list|overdue|members|returned|history <member>\", file=sys.stderr)",
)
p.write_text(s)
EOF
cat > tests/test_members.py <<'EOF'
import unittest

from test_shelfnote import run


class MemberReports(unittest.TestCase):
    def test_members_lists_each_member_once(self):
        self.assertEqual(run("members"), ["Ana", "Lena", "Ravi"])

    def test_returned_names_each_returned_loan(self):
        self.assertEqual(run("returned"), ["Beloved — returned by Ravi"])

    def test_history_shows_one_members_loans(self):
        self.assertEqual(run("history", "Ana"), ["Middlemarch — due 2026-10-22"])


if __name__ == "__main__":
    unittest.main()
EOF
git add -A
git commit -qm "Add member reports: members, returned and history"
git checkout -q ticket/01-club-name-on-reports
