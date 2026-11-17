#!/usr/bin/env bash
# Shelfmark with a change on feature/monthly-statements that touches the three craft-principles
# lines and owes nothing on any: the return address is a branch setting, as the first line asks;
# the long statement is compared with a reviewed snapshot file, which the second line's own yield
# allows; the greeting test checks the name only, a departure the maintainer chose in decision 0001
# before the change; and the third line is about how the author asks for review, which the change
# cannot show. A code comment writes a number as a word, which only outreach-principles, whose
# stated use does not cover code, would object to.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../principles-shelfmark/scaffold.sh"
git switch -qc feature/monthly-statements
git config user.name 'Jonas Pike'
git config user.email 'jonas@shelfmark.example'
mkdir -p tests/snapshots
python3 - <<'PY'
from pathlib import Path
p = Path("config/branches.toml")
t = p.read_text()
for section, address in [
    ("central", "Central Library, 1 Market Square"),
    ("north", "North Library, 40 Mill Road"),
    ("harbor", "Harbor Library, 7 Quay Street"),
]:
    head = f"[{section}]\n"
    assert t.count(head) == 1, f"the base scaffold's branches.toml no longer has [{section}]"
    at = t.index("channels = ", t.index(head))
    eol = t.index("\n", at) + 1
    t = t[:eol] + f'address = "{address}"\n' + t[eol:]
p.write_text(t)
PY
python3 - <<'PY'
from pathlib import Path
p = Path("src/shelfmark/branches.py")
t = p.read_text()
for old, new in [
    ("    channels: tuple[str, ...]\n", "    channels: tuple[str, ...]\n    address: str\n"),
    ("            channels=tuple(settings[\"channels\"]),\n", "            channels=tuple(settings[\"channels\"]),\n            address=settings[\"address\"],\n"),
]:
    assert t.count(old) == 1, f"the base scaffold's branches.py no longer holds {old!r}"
    t = t.replace(old, new)
p.write_text(t)
PY
cat > src/shelfmark/statements.py <<'EOF'
"""Monthly loan statements, sent to each member through their branch's channels."""
from datetime import date

from shelfmark import channels


def statement_greeting(name: str) -> str:
    """The opening line. The front desk rewrites its wording each season (decision 0001)."""
    return f"Hello {name}, here is your month at the library."


def statement_body(loans: list[dict], branch, today: date) -> str:
    if not loans:
        return f"You have no loans out on {today:%d %B %Y}."
    # Oldest first: a loan held three weeks or more is the one members forget.
    lines = [f"Your loans on {today:%d %B %Y}:"]
    for loan in sorted(loans, key=lambda loan: loan["borrowed"]):
        lines.append(f"- {loan['title']}, due {loan['due']:%d %B %Y}")
    lines.append(f"Return them to {branch.address}.")
    return "\n".join(lines)


def loan_statement(member: dict, loans: list[dict], branch, today: date) -> str:
    return f"{statement_greeting(member['name'])}\n\n{statement_body(loans, branch, today)}"


def send_statements(branch, members: list[dict], loans_by_member: dict[str, list[dict]], today: date) -> int:
    for member in members:
        loans = loans_by_member.get(member["email"], [])
        channels.send(branch, member, loan_statement(member, loans, branch, today))
    return len(members)
EOF
python3 - <<'PY'
from datetime import date, timedelta
titles = [f"{t}, volume {v}" for v in (1, 2, 3) for t in [
    "Moby-Dick", "Dune", "Beloved", "Middlemarch", "Ulysses", "Emma", "Kindred", "Persuasion",
    "Solaris", "Rebecca", "Hamnet", "Matilda", "Ivanhoe", "Walden", "Dracula", "Frankenstein",
    "Jane Eyre", "Lolita", "Ulysses Annotated", "Hard Times", "Night", "Siddhartha", "Cosmos", "Atonement"]]
start = date(2026, 1, 1)
lines = ["Your loans on 31 March 2026:"]
for i, t in enumerate(titles):
    lines.append(f"- {t}, due {start + timedelta(days=21 + i):%d %B %Y}")
lines.append("Return them to Central Library, 1 Market Square.")
open("tests/snapshots/statement-body-72-loans.txt", "w").write("\n".join(lines) + "\n")
PY
cat > tests/test_statements.py <<'EOF'
from datetime import date, timedelta
from pathlib import Path

from shelfmark.branches import Branch
from shelfmark.statements import loan_statement, statement_body, statement_greeting

CENTRAL = Branch("central", 3, ("email",), "Central Library, 1 Market Square")
SNAPSHOT = Path(__file__).parent / "snapshots" / "statement-body-72-loans.txt"
TITLES = [f"{t}, volume {v}" for v in (1, 2, 3) for t in [
    "Moby-Dick", "Dune", "Beloved", "Middlemarch", "Ulysses", "Emma", "Kindred", "Persuasion",
    "Solaris", "Rebecca", "Hamnet", "Matilda", "Ivanhoe", "Walden", "Dracula", "Frankenstein",
    "Jane Eyre", "Lolita", "Ulysses Annotated", "Hard Times", "Night", "Siddhartha", "Cosmos", "Atonement"]]


def loans():
    start = date(2026, 1, 1)
    made = [
        {"title": t, "borrowed": start + timedelta(days=i), "due": start + timedelta(days=21 + i)}
        for i, t in enumerate(TITLES)
    ]
    return list(reversed(made))


def test_long_statement_body_matches_the_reviewed_snapshot():
    assert statement_body(loans(), CENTRAL, date(2026, 3, 31)) + "\n" == SNAPSHOT.read_text()


def test_member_with_no_loans_is_told_so():
    member = {"name": "Ana", "email": "ana@example.org"}
    assert loan_statement(member, [], CENTRAL, date(2026, 3, 31)) == (
        statement_greeting("Ana") + "\n\nYou have no loans out on 31 March 2026."
    )


def test_greeting_names_the_member():
    assert "Ana" in statement_greeting("Ana")


def test_statement_is_the_greeting_then_the_body():
    member = {"name": "Ana", "email": "ana@example.org"}
    expected = statement_greeting("Ana") + "\n\n" + SNAPSHOT.read_text().rstrip("\n")
    assert loan_statement(member, loans(), CENTRAL, date(2026, 3, 31)) == expected
EOF
git add -A
git commit -qm 'Send a monthly loan statement to each member'
