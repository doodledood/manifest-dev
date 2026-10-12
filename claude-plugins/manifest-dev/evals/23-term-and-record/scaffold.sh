#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr src
cat > docs/adr/CONVENTIONS.md <<'CONVEOF'
# ADR Conventions

Write a record for a decision that shapes the system, constrains later options, or would be
costly to reverse. Not for bug fixes or defaults nobody weighed.

## Template

```markdown
# ADR: [Decision Title]

## Status
Accepted

## Area
[One short label]

## Decided by
[The user | An agent in an unattended run, with no review]

## Context
## Decision
## Alternatives Considered
## Consequences
## Source
- Related: [Supersedes / Superseded by / See also]
```

**Decided by**: `The user` when a person decided it; `An agent in an unattended run, with no
review` when a run with no person present accepts its own record.

## Files

`docs/adr/YYYYMMDD-kebab-case-title.md`, dated today.

## Writing a record is one act

In the same change: write the record; set the Status of every record it replaces to
`Superseded by <filename without .md>`, with the new record listing `Supersedes <filename>` in its
Source; and rebuild the index.

## The index

`docs/adr/README.md` is a title, a blank line, and one table row per record, ascending by
filename: `| YYYY-MM-DD | [title](filename) | Status | Area |`.
CONVEOF
cat > CONTEXT.md <<'EOF'
# Harvest Co-op ordering

The co-op's members order produce boxes online; volunteers pack them at the depot.

## Language

**Member**:
A household that pays the yearly co-op fee and can place orders.

**Box**:
One packed order for one member, collected at the depot.

**Cutoff**:
The last moment a member can change what goes into the next box.
EOF
cat > docs/adr/20260301-orders-close-on-a-rolling-cutoff.md <<'EOF'
# ADR: Orders close on a rolling cutoff

## Status
Accepted

## Area
Ordering

## Decided by
The user

## Context
Members asked for as much time as possible to change their box.

## Decision
Each member can change their box until 48 hours before their own collection slot.

## Alternatives Considered
- **One weekly cutoff for everyone**: simpler for packers — not chosen, members wanted flexibility.

## Consequences
### Positive
- Members get the longest possible window.
### Negative
- Packers never know the final count until the last slot closes.

## Source
- Session: planning meeting notes.
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-03-01 | [Orders close on a rolling cutoff](20260301-orders-close-on-a-rolling-cutoff.md) | Accepted | Ordering |
EOF
cat > src/cutoff.py <<'EOF'
from datetime import datetime, timedelta


def can_edit(collection_slot: datetime, now: datetime) -> bool:
    return now < collection_slot - timedelta(hours=48)
EOF
