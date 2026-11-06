#!/usr/bin/env bash
# A Pollbox project with no surfaces, whose history holds two explained overrides of shipped
# defaults, one preference a shipped default already states, one choice a decision record settles,
# and one correction with no stated reason: the setup-project recipe's taste-from-history scenario.
set -euo pipefail
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
commit() { git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example add -A && git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -q "$@"; }
mkdir -p src docs/adr docs/reviews tests
cat > README.md <<'EOF'
# Pollbox

Web app for running votes in clubs and associations: an organizer creates a poll, members get a
link by email, results publish when the poll closes. Run it with `python3 src/app.py`; test with
`python3 -m pytest tests/`.
EOF
cat > src/app.py <<'EOF'
"""Pollbox: organizers create polls, members vote by emailed link."""
POLL_SETTINGS = {"ballot": "secret", "results": "on-close", "quorum": None}

def create_poll(organizer, question, options, settings):
    if organizer is None:
        raise PermissionError("sign in to create a poll")
    return {"question": question, "options": options, **POLL_SETTINGS, **settings}
EOF
cat > tests/test_app.py <<'EOF'
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))
from app import create_poll

def test_guest_cannot_create():
    try:
        create_poll(None, "q", ["a"], {})
    except PermissionError:
        return
    raise AssertionError
EOF
commit -m "feat: first poll flow"

cat > docs/adr/0001-store-votes-in-sqlite.md <<'EOF'
# 1. Store votes in SQLite

Status: Accepted

Votes and polls live in one SQLite file per deployment. Clubs self-host on small machines, a
server database is one more thing for a volunteer to keep running, and our largest club casts
about 900 votes a year.
EOF
commit -m "docs: record the storage decision"

cat > docs/reviews/pr-41-signup.md <<'EOF'
# Review notes exported from pull request #41 (member sign-up)

**Proposal (contributor):** the sign-up form asks for name, club role, phone and newsletter choice
up front, so profiles are complete.

**Dana:** Ask only for the email at sign-up; the rest when it is needed. Nobody fills a phone field
to vote.

**Proposal (contributor):** organizers can create a poll as a guest and claim it later, so they see
the result screen before committing to an account.

**Dana:** No. Nobody creates a poll that other people receive without a verified account first.
Our guest polls were used to send spam from our domain last spring and school mail filters blocked
us for a month; members never got their ballots. Anything that sends to other people waits for a
verified sender, even if it costs us first-time organizers.
EOF
commit -m "docs: keep the sign-up review notes"

cat >> src/app.py <<'EOF'

def ballot_secrecy_choice(settings):
    # Organizers must pick secret or open ballot themselves; there is no preselected default.
    return settings["ballot"]
EOF
commit -m "fix: make organizers choose ballot secrecy and quorum themselves" \
  -m "Reverts the preselected 'secret ballot, no quorum' defaults from last week. Our associations run formal elections under their own bylaws: when the tool picked for them, the choice got challenged at two AGMs as one the organizer never made. For anything that decides whether a vote is valid, the organizer sets it explicitly, even though it adds a step."

sed 's/POLL_SETTINGS = .*/POLL_SETTINGS = {"ballot": None, "results": "on-close", "quorum": None}/' src/app.py > src/app.py.tmp
mv src/app.py.tmp src/app.py
commit -m "fix: leave ballot secrecy unset until the organizer picks it"

printf '%s\n' '<header><a href="/polls">Polls</a> <a href="/export">Export results</a></header>' > src/header.html
commit -m "revert: put the export button back in the header"
