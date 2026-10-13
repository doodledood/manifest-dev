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

mkdir -p src/messages
printf 'Hi {name}, "{book}" is due back on {date}. Reply if you need more time.\n' > src/messages/reminder_email.txt
printf 'Hi {name}, "{book}" is due back on {date}. Reply if you need more time.\n' > src/messages/reminder_sms.txt
cat > docs/adr/20260610-message-wording-kept-per-channel.md <<'EOF'
# ADR: Message wording is kept separate per channel

## Status
Accepted

## Area
Messages

## Context
Email and text messages get read differently, and we tune them separately.

## Decision
Each channel keeps its own copy of every message, even when the wording matches today, so a
change for one channel never shifts the other.

## Alternatives Considered
- **One shared template**: one edit would change both channels.

## Consequences
### Positive
- Each channel can change alone.
### Negative
- Similar text in two files.

## Source
- Session: (none)
EOF
printf '| 2026-06-10 | [Message wording is kept separate per channel](20260610-message-wording-kept-per-channel.md) | Accepted | Messages |\n' >> docs/adr/README.md
