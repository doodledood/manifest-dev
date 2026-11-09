#!/usr/bin/env bash
# A Pollbox project set up at the newest surfaces version, whose history holds three design
# corrections with stated reasons, one design decision a record settles, one design reaction with
# no reason, and one stray storage comment: the create-principles-skill recipe's fixture.
set -euo pipefail
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
commit() { git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example add -A && git -c user.name="Dana Reyes" -c user.email=dana@pollbox.example commit -q "$@"; }
mkdir -p src/templates docs/adr docs/reviews tests
cat > README.md <<'EOF'
# Pollbox

Web app for running votes in clubs and associations: an organizer creates a poll, members get a
link by email, results publish when the poll closes. Run it with `python3 src/app.py`; test with
`python3 -m pytest tests/`.
EOF
cat > CLAUDE.md <<'EOF'
# Pollbox

## Project surfaces

<!-- setup-project surfaces v15 -->

This project keeps its direction, vocabulary, and decision memory in the repo. Read `CONTEXT.md`
at the start of every session.

- **CONTEXT.md** — what words mean here.
- **docs/adr/** — why decisions went the way they did. Write new records per
  `docs/adr/CONVENTIONS.md`.
- **Verification** — how this project checks that its work still does its job:
  `python3 -m pytest tests/`. This project verifies its own way by choice: add no separate
  verification tool to it.
EOF
cat > CONTEXT.md <<'EOF'
# Pollbox

Runs votes for clubs.

## Language

**Poll**:
One question put to a club's members, open until its organizer closes it.
EOF
cat > docs/adr/CONVENTIONS.md <<'EOF'
# ADR Conventions

One file per decision, `NNNN-title.md`, with Status, Context, Decision, Alternatives Considered
and Consequences. `docs/adr/README.md` lists them.
EOF
cat > docs/adr/0002-tailwind-for-styles.md <<'EOF'
# 0002: Tailwind for styles

## Status
Accepted

## Context
Templates were growing one-off CSS files.

## Decision
Style templates with Tailwind utility classes.

## Alternatives Considered
Plain CSS files per template: they drifted apart. A component library: too heavy for four pages.

## Consequences
Every template uses utility classes; no new CSS files.
EOF
printf '# Decision records\n\n- [0002: Tailwind for styles](0002-tailwind-for-styles.md)\n' > docs/adr/README.md
cat > src/app.py <<'EOF'
"""Pollbox: organizers create polls, members vote by emailed link."""
POLLS = {}

def create_poll(organizer, question, options):
    POLLS[question] = {"organizer": organizer, "options": options, "votes": {}}
    return question
EOF
cat > src/templates/results.html <<'EOF'
<main class="max-w-xl mx-auto"><h1>{{ question }}</h1>{% for o in options %}<p>{{ o.name }}: {{ o.count }}</p>{% endfor %}</main>
EOF
cat > tests/test_app.py <<'EOF'
from src.app import create_poll

def test_create_poll():
    assert create_poll("dana", "Venue?", ["hall", "park"]) == "Venue?"
EOF
touch src/__init__.py
commit -m "feat: polls and a results page"
cat > docs/reviews/pr-12-results.md <<'EOF'
# Review notes exported from pull request #12 (results view)

**Dana:** Not a modal, please. Results get shared — people paste the link into the club chat —
and a modal has no address of its own. Give results their own page.

**Sam:** Moved to /polls/<id>/results.
EOF
commit -m "docs: keep the results review notes"
cat > src/templates/results.html <<'EOF'
<main class="max-w-xl mx-auto"><h1>{{ question }}</h1>{% for o in options %}<p>{{ o.name }}: {{ o.count }} <span class="bg-gray-400" style="width: {{ o.pct }}%"></span></p>{% endfor %}</main>
EOF
commit -m "fix: results bars in one neutral grey" -m "Reverts the green/red bars. Colour reads as a winner and a loser, and two members took the red bar as the club voting against them. Show the count and a bar in one neutral colour; let the numbers speak."
cat > docs/reviews/pr-15-create-form.md <<'EOF'
# Review notes exported from pull request #15 (create-poll form)

**Dana:** Keep the form one column, labels above fields. Organizers fill it on their phones in the
middle of a meeting; two columns turned into a squeeze there and they mistyped options.

**Dana:** Make the submit button blue.

**Sam:** Done, both.
EOF
commit -m "docs: keep the create-form review notes"
cat > src/store.py <<'EOF'
import json, time

def save(path, polls):
    # Dana: use time.time() here.
    json.dump({"saved": time.time(), "polls": polls}, open(path, "w"))
EOF
commit -m "feat: save polls to a file"
