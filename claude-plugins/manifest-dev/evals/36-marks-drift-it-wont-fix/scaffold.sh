#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr src
cat > CLAUDE.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed.

## Project surfaces

This project keeps its direction, vocabulary, and decision memory in the repo. Read
`NORTH_STAR.md` and `CONTEXT.md` at the start of every session.

- **NORTH_STAR.md** — why this project exists and who it's for.
- **CONTEXT.md** — what words mean here.
- **docs/adr/** — why decisions went the way they did. Write new records per
  `docs/adr/CONVENTIONS.md`.
EOF
cat > CONTEXT.md <<'EOF'
# Shelfnote

Tracks borrowed books for a reading club.

## Language

**Loan**:
One book lent to one member, from checkout to return.
EOF
cat > NORTH_STAR.md <<'EOF'
# North Star — Shelfnote

## Who it's for

Volunteer organizers of small reading clubs.

— hypothesis: from the README. 2026-05
EOF
cat > docs/adr/CONVENTIONS.md <<'EOF'
# ADR Conventions

Write a record for a decision that shapes the system or would be costly to reverse.

## Template

```markdown
# ADR: [Decision Title]

## Status
Accepted

## Area
[One short label]

## Context
## Decision
## Alternatives Considered
## Consequences
## Source
```

Files are `docs/adr/YYYYMMDD-kebab-case-title.md`. Writing a record is one act: the record,
the restatus of what it changes, and the index.
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-05-02 | [Loans are stored in one JSON file](20260502-loans-in-one-json-file.md) | Accepted | Storage |
EOF
cat > docs/adr/20260502-loans-in-one-json-file.md <<'EOF'
# ADR: Loans are stored in one JSON file

## Status
Accepted

## Area
Storage

## Context
A club has at most a few hundred loans.

## Decision
All loans live in `data/loans.json`, written only by `src/store.py`.

## Alternatives Considered
- **SQLite**: more than the club needs.

## Consequences
### Positive
- Nothing to install.
### Negative
- One writer at a time.

## Source
- Session: (none)
EOF
cat > src/store.py <<'EOF'
# Enforces docs/adr/20260502-loans-in-one-json-file.md: the only writer of data/loans.json.
import json, pathlib
PATH = pathlib.Path("data/loans.json")
def save(loans):
    PATH.write_text(json.dumps(loans))
EOF

mkdir -p src tests
cat > README.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed.

    python -m shelfnote checkout --member ana --book "Middlemarch"
    python -m shelfnote return --book "Middlemarch"
    python -m shelfnote overdue
    python -m shelfnote export --format csv
EOF
cat > src/shelfnote.py <<'EOF'
import argparse, json, pathlib, sys
DATA = pathlib.Path("data/loans.json")
def load():
    return json.loads(DATA.read_text()) if DATA.exists() else []
def main(argv=None):
    p = argparse.ArgumentParser(prog="shelfnote")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("checkout"); c.add_argument("--member"); c.add_argument("--book")
    r = sub.add_parser("return"); r.add_argument("--book")
    sub.add_parser("overdue")
    e = sub.add_parser("export"); e.add_argument("--format", choices=["csv", "json"])
    args = p.parse_args(argv)
    print(args.cmd)
if __name__ == "__main__":
    main()
EOF

mkdir -p verify/features
cat > verify/README.md <<'EOF'
# Verification surface

This directory is how this project checks that the shelfnote CLI still does its job.

## How to run it

    python verify/control.py doctor
    python verify/control.py run checkout --member ana --book Middlemarch

## Statuses

- `unverified` — catalogued but not yet exercised. Not proof of anything.
- `verified` — exercised by a run, with the date.
- `stale` — a run found it drifting; the entry carries a dated line naming what differs.
EOF
cat > verify/control.py <<'EOF'
import subprocess, sys
def main():
    if sys.argv[1] == "doctor":
        print("ok")
    else:
        subprocess.run([sys.executable, "-m", "shelfnote", *sys.argv[2:]], check=True)
main()
EOF
cat > verify/features/checkout.md <<'EOF'
# Checkout

Status: verified (2026-09-30)

## How to get to it
`shelfnote checkout --member <name> --book <title>`

## Driving it
    python verify/control.py run checkout --member ana --book Middlemarch

## What proves it works
The loan appears in `data/loans.json` with today's date.
EOF
cat > verify/features/overdue.md <<'EOF'
# Overdue list

Status: unverified

## How to get to it
`shelfnote overdue`

## Driving it
    python verify/control.py run overdue

## What proves it works
Every loan older than 21 days is listed once, oldest first.
EOF
cat > verify/features/export.md <<'EOF'
# Export

Status: verified (2026-08-11)

## How to get to it
`shelfnote export --csv`

## Driving it
    python verify/control.py run export --csv

## What proves it works
A CSV with one row per loan is written to stdout.
EOF

cat >> CLAUDE.md <<'EOF'
- **Verification surface** — `verify/`, a harness and feature map: how this project checks
  that its result still does its job. Read its README before exercising a change.
EOF
