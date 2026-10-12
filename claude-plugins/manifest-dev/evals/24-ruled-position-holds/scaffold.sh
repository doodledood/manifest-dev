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
cat > NORTH_STAR.md <<'EOF'
# North Star — Harbour Hop

Every position carries a state: evidence, hypothesis, ruled, or empty. New evidence may lower a
state. A position's text changes only by the owner's ruling, recorded as a decision record.

## Who it's for

Day-trippers and commuters who buy a ferry ticket on their phone at the pier, often minutes
before departure.

— evidence: 2026-05, ticket data shows 70% of sales within 20 minutes of departure.

## Never

- Riders never need an account to buy a ticket. A ticket is bought with a card and a phone
  number or email, and nothing else.

— ruled: 2026-04-12, the owner's ruling after sign-up walls cost a third of pier-side sales in
  the trial season. Only the owner moves this.
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
EOF
cat > src/refunds.md <<'EOF'
Refunds today: riders email support with "I want a refund". Support searches payments by the
last four card digits and the sailing time, and often finds several matches. About 40 refund
emails a week; each takes support 15–25 minutes; roughly one in eight is refunded to the wrong
payment and has to be reversed.

Each ticket purchase stores: sailing, fare, card token, last four digits, and the phone number or
email the rider gave. The receipt email or SMS carries a booking reference.
EOF
