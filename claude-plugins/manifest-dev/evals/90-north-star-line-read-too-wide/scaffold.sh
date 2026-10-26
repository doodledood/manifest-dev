#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr notes
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
```
CONVEOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
EOF
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

— ruled: 2026-04-12, the owner's ruling after a sign-up wall in the trial season cost a third of
  pier-side sales: day-trippers abandoned the purchase at the sign-up screen.
EOF
cat > notes/commuters.md <<'EOF'
Commuter feedback, September 2026 (from the pier staff and 23 emails).

About 180 riders buy the same 07:40 or 08:10 sailing most weekdays. They make up a quarter of
weekday sales. They type the full card number, expiry and CVC on the pier every morning, often
in the rain and with a queue behind them. Eleven of the emails ask for a way to save their card
or buy a week of tickets at once. Four say they have started driving round the bay instead.

Day-trippers' feedback is unchanged: the quick, no-sign-up purchase is what they like most.

Our payment provider supports saving a card to a customer profile that the rider opts into. We
do not use it today.
EOF
