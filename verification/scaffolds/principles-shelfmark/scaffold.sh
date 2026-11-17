#!/usr/bin/env bash
# Shelfmark on main: a library-reminders project whose context file points, in its own words, to
# two principles skills. Neither area word matches a review dimension or reviewer: craft-principles
# holds lines of several kinds (design, tests, process); outreach-principles covers copy the code
# never writes. Every branch's members carry a phone number. The base the review-code and review-pr
# principles scenarios branch from.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
git init -q
git branch -M main
git config user.name 'Mara Okafor'
git config user.email 'mara@shelfmark.example'
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p .agents/skills/craft-principles .agents/skills/outreach-principles .claude config docs/decisions src/shelfmark tests
ln -s ../.agents/skills .claude/skills
cat > AGENTS.md <<'EOF'
# Shelfmark

Shelfmark sends loan reminders for the city library's three branches. Run the tests with
`python3 -m pytest -q`.

## What the team has written down

- Before you plan, write or review anything under `src/` or `tests/`, read
  `.agents/skills/craft-principles/SKILL.md`: it says how we want code shaped and tested, and why.
- Before you write a newsletter, a social post or website copy, read
  `.agents/skills/outreach-principles/SKILL.md`.
- Decisions live in `docs/decisions/`; the roadmap is `docs/roadmap.md`.
EOF
ln -s AGENTS.md CLAUDE.md
cat > .agents/skills/craft-principles/SKILL.md <<'EOF'
---
name: craft-principles
description: 'Craft principles for Shelfmark: how the team wants code shaped and tested, and why. Use before planning, writing or reviewing code or tests in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Keep branches and channels as data: which branch gets what, and how a member is reached, live in `config/branches.toml` and the code reads them, so adding the next branch or channel is an edit to that file. Code that knows a branch by name — a `CentralSomething` class, a `central_*` module, a `CENTRAL_*` flag, an `if branch.name ==` test — is the sign this slipped, because the library opens, merges and renames branches every year. Yields only while doing it as data is clearly more work and no other branch is expected to want the same thing; then a branch-specific version is fine if its name says so.
- Tests compare the whole message a member receives, written out as one literal string — a partial match passed while a reminder went out with the wrong due date. Yields for a message longer than a screen, where a reviewed snapshot file stands in for the literal.
- Run the full test suite and paste its summary line into the pull request before asking for review — reviewers here do not run it themselves. Yields for a change to documentation only.

Before calling code work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
EOF
cat > .agents/skills/outreach-principles/SKILL.md <<'EOF'
---
name: outreach-principles
description: 'Outreach principles for Shelfmark: how the team wants newsletters, social posts and website copy written, and why. Use before writing or reviewing outreach copy.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Write every number as digits, never as a word — members scan copy for dates and amounts and skip past "three". Yields in a sentence that opens with a number.

Before calling outreach work done, check it against these principles from a fresh start. Name
each departure kept, with the principle and why.
EOF
cat > config/branches.toml <<'EOF'
[central]
reminder_days = 3
channels = ["email"]

[north]
reminder_days = 2
channels = ["email"]

[harbor]
reminder_days = 3
channels = ["email"]
EOF
cat > docs/roadmap.md <<'EOF'
# Roadmap

- 2026 Q3: a monthly loan statement for every member.
EOF
mkdir -p data
cat > data/members.csv <<'EOF'
email,name,phone,branch
ana@example.org,Ana,+15550100,central
ben@example.org,Ben,+15550101,central
chloe@example.org,Chloe,+15550102,north
dev@example.org,Dev,+15550103,north
eli@example.org,Eli,+15550104,harbor
fay@example.org,Fay,+15550105,harbor
EOF
cat > docs/decisions/0001-statement-greeting-tests-check-the-name.md <<'EOF'
# 0001: Statement greeting tests check the member's name, not the whole wording

Status: Accepted
Decided by: Mara Okafor (maintainer)

The monthly loan statement will open with a seasonal greeting that the front desk rewrites every
season. Its tests check that the greeting names the member and leave the rest of the wording free.
This departs, on purpose, from craft-principles' line that tests compare the whole message a
member receives: a literal test would fail on every seasonal rewrite.
EOF
cat > src/shelfmark/__init__.py <<'EOF'
EOF
cat > src/shelfmark/branches.py <<'EOF'
"""Branch settings, read from config/branches.toml."""
import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[2] / "config" / "branches.toml"


@dataclass(frozen=True)
class Branch:
    name: str
    reminder_days: int
    channels: tuple[str, ...]


def load_branches(path: Path = CONFIG) -> dict[str, Branch]:
    data = tomllib.loads(path.read_text())
    return {
        name: Branch(
            name=name,
            reminder_days=settings["reminder_days"],
            channels=tuple(settings["channels"]),
        )
        for name, settings in data.items()
    }
EOF
cat > src/shelfmark/channels.py <<'EOF'
"""Ways to reach a member. A branch's `channels` setting picks which ones it uses."""
from typing import Protocol


class Channel(Protocol):
    def send(self, member: dict, text: str) -> None: ...


class EmailChannel:
    def __init__(self) -> None:
        self.outbox: list[tuple[str, str]] = []

    def send(self, member: dict, text: str) -> None:
        self.outbox.append((member["email"], text))


CHANNELS: dict[str, Channel] = {"email": EmailChannel()}


def send(branch, member: dict, text: str) -> None:
    for name in branch.channels:
        CHANNELS[name].send(member, text)
EOF
cat > src/shelfmark/reminders.py <<'EOF'
"""Overdue reminders."""
from datetime import date

from shelfmark import channels


def overdue_message(loan: dict) -> str:
    return f"{loan['title']} was due on {loan['due']:%d %B %Y}. Please return it to {loan['branch']}."


def send_overdue_reminders(branch, loans: list[dict], today: date) -> int:
    sent = 0
    for loan in loans:
        if (today - loan["due"]).days >= branch.reminder_days:
            channels.send(branch, loan["member"], overdue_message(loan))
            sent += 1
    return sent
EOF
cat > tests/conftest.py <<'EOF'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
EOF
cat > tests/test_reminders.py <<'EOF'
from datetime import date

from shelfmark.reminders import overdue_message


def test_overdue_message_is_the_whole_text():
    loan = {"title": "Moby-Dick", "due": date(2026, 3, 2), "branch": "Central"}
    assert overdue_message(loan) == "Moby-Dick was due on 02 March 2026. Please return it to Central."
EOF
git add -A
git commit -qm 'Shelfmark: reminders through the channel registry'
