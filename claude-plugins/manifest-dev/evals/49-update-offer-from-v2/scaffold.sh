#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr docs/features src tests
cat > CLAUDE.md <<'EOF'
# Shelfnote

Command-line tool that tracks books a reading club has borrowed.

## Project surfaces

<!-- setup-project surfaces v2 -->

This project keeps its direction, vocabulary, and decision memory in the repo. Read
`NORTH_STAR.md` and `CONTEXT.md` at the start of every session.

- **NORTH_STAR.md** — why this project exists and who it's for.
- **CONTEXT.md** — what words mean here.
- **docs/adr/** — why decisions went the way they did. Write new records per
  `docs/adr/CONVENTIONS.md`.
- **Verification surface** — `tests/`, a test suite: how this project checks that the CLI
  still does its job. A change to anything a test covers updates that test and runs it.
- **Feature map** — `docs/features/`: how a user reaches each feature and how to drive and check
  it. Start there to place a report or find what a change touches.
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

Only an `Accepted` record is in effect. Backfilling `Enforced by`, building a `not yet` check,
and citing a record as a ruling read only records in effect.
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

## Enforced by
`src/store.py` — the only module that writes `data/loans.json`; it carries a comment citing
this record.

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
cat > tests/test_cli.py <<'EOF'
import subprocess, sys

def run(*args):
    return subprocess.run([sys.executable, "src/shelfnote.py", *args], capture_output=True, text=True)

def test_overdue_runs():
    assert run("overdue").returncode == 0
EOF
cat > docs/features/README.md <<'EOF'
# Shelfnote feature map

How a user reaches each command and how to drive it.

## Baseline preconditions

- Python 3 on the path; run commands from the repository root.

## Driving conventions

- Run `python3 src/shelfnote.py <command>`; take commands literally.

## Proof and skip rules

- Proof is the command, its output and its exit code.
- An entry point that could not be driven is recorded `unreachable` with the missing prerequisite.

## Features

- [checkout](./checkout.md)
- [return](./return.md)
- [overdue](./overdue.md)
EOF
cat > docs/features/checkout.md <<'EOF'
# checkout

Records that a member borrowed a book.

Status: unverified

## Sub-features

- `checkout` — the command itself.

## How to get to it (user POV)

- `python3 src/shelfnote.py checkout`.

## Driving it

Preconditions: the baseline in the index.

- **Run.** `python3 src/shelfnote.py checkout`. Exit `0`; it prints `checkout`.

## How it is checked

`tests/test_cli.py`.

## Gotchas

- The command parses its arguments and prints its name; it does not read loans yet.
EOF
cat > docs/features/return.md <<'EOF'
# return

Records that a borrowed book came back.

Status: unverified

## Sub-features

- `return` — the command itself.

## How to get to it (user POV)

- `python3 src/shelfnote.py return`.

## Driving it

Preconditions: the baseline in the index.

- **Run.** `python3 src/shelfnote.py return`. Exit `0`; it prints `return`.

## How it is checked

`tests/test_cli.py`.

## Gotchas

- The command parses its arguments and prints its name; it does not read loans yet.
EOF
cat > docs/features/overdue.md <<'EOF'
# overdue

Lists loans past their due date.

Status: unverified

## Sub-features

- `overdue` — the command itself.

## How to get to it (user POV)

- `python3 src/shelfnote.py overdue`.

## Driving it

Preconditions: the baseline in the index.

- **Run.** `python3 src/shelfnote.py overdue`. Exit `0`; it prints `overdue`.

## How it is checked

`tests/test_cli.py`.

## Gotchas

- The command parses its arguments and prints its name; it does not read loans yet.
EOF
