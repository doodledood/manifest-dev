#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr
cat > CLAUDE.md <<'EOF'
# Loomwork

Shop where independent weavers sell their patterns.

## Project surfaces

<!-- setup-project surfaces v12 -->

This project keeps its direction, vocabulary, and decision memory in the repo. Read
`NORTH_STAR.md` and `CONTEXT.md` at the start of every session.

- **NORTH_STAR.md** — what this project is for and for whom, its principles, how it tells
  progress and the bets it rests on. The choices made along the way live in `docs/adr/`, never
  in it.
- **CONTEXT.md** — what words mean here.
- **docs/adr/** — why decisions went the way they did. Write new records per
  `docs/adr/CONVENTIONS.md`.
EOF
cat > CONTEXT.md <<'EOF'
# Loomwork

## Language

**Weaver**:
A person who designs patterns and sells them in the shop.

**Sales fee**:
The share of each pattern sale the shop keeps.
EOF
cat > NORTH_STAR.md <<'EOF'
# North Star — Loomwork

What this project is for, for whom, and how it measures progress. Every position carries a state:
evidence, hypothesis, ruled, or empty. New evidence may lower a state. A position's text changes
only by the owner's ruling, recorded as a decision record.

## Purpose

Independent weavers design good patterns and struggle to sell them: general marketplaces bury
them, and running their own shop takes time they would rather spend weaving.

For: weavers who sell their own patterns and do it alongside other work.

Not for: large pattern publishers, and buyers looking for finished textiles.

— hypothesis: from seller interviews. 2026-05

## Goal

"I list a pattern once, it reaches people who weave, and I keep most of what it earns."

— ruled: 2026-05

## Principles

- Weavers keep what they earn: the shop's fee stays the smallest that keeps the shop running.
- A weaver's patterns and buyer list are theirs, and leave with them in one export.

— ruled: 2026-05

## How we know

- Weavers still selling a year after they join — share, up. — empty: the shop is eight months
  old. What would fill it: the first cohort reaching a year. 2026-05
- Pattern sales per weaver per month — up. — ruled: 2026-05

## What this rests on

- Weavers would rather pay a small fee per sale than a monthly subscription. — hypothesis: from
  seller interviews. 2026-05

## Open

- Do buyers come back for a second weaver's patterns? What would fill it: repeat-purchase data
  across weavers. 2026-05

## Strategy choices in force

- Charge per sale, never per month
EOF
cat > docs/adr/CONVENTIONS.md <<'EOF'
# ADR Conventions

Write a record for a decision that shapes the product, constrains later options, or would be
costly to reverse.

## Template

```markdown
# ADR: [Decision Title]

## Status
Accepted

## Area
[One short label. A guiding choice the project pursues its goal through carries `Strategy`.]

## Decided by
[The user | An agent in an unattended run, with no review]

## Context
## Decision
## Alternatives Considered
## Consequences
## Enforced by
[A concrete check, or not yet plus the check to add.]
## Source
- Related: [Supersedes / Superseded by / See also]
```

## Files

The next record ID is reserved as `docs/adr/20261024-new-weavers-pay-no-fee-for-90-days.md`. If a decision
needs a record, use that path and its reserved date rather than the wall-clock date.

## Writing a record is one act

In the same change: write the record; set the Status of every record it replaces to
`Superseded by <filename without .md>`; rebuild the index; and, for a `Strategy` record, rebuild
the North Star's *Strategy choices in force* list from the `Strategy` records in effect.

## The index

`docs/adr/README.md` is a title, a blank line, and one table row per record, ascending by
filename: `| YYYY-MM-DD | [title](filename) | Status | Area |`.
EOF
cat > docs/adr/20260512-charge-per-sale-never-per-month.md <<'EOF'
# ADR: Charge per sale, never per month

## Status
Accepted

## Area
Strategy

## Decided by
The user

## Context
Weavers in the interviews sell a few patterns a month alongside other work.

## Decision
The shop earns a fee on each sale. It never charges weavers a monthly subscription.

## Alternatives Considered
- A monthly subscription: rejected — most weavers would pay more than they earn in a slow month.

## Consequences
The shop's income follows weavers' sales.

## Source
- Related: none
EOF
cat > docs/adr/20260601-new-weavers-pay-no-fee-at-first.md <<'EOF'
# ADR: New weavers pay no sales fee for their first 180 days

## Status
Accepted

## Area
Pricing

## Decided by
The user

## Context
A weaver who has just joined has no sales yet, and a fee on the first few feels like a toll.

## Decision
New weavers pay no sales fee for their first 180 days.

## Alternatives Considered
- No fee-free period: rejected — new weavers would leave before their first sale.

## Consequences
The shop earns nothing from a weaver's first 180 days.

## Source
- Related: see also 20260512-charge-per-sale-never-per-month
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-05-12 | [Charge per sale, never per month](20260512-charge-per-sale-never-per-month.md) | Accepted | Strategy |
| 2026-06-01 | [New weavers pay no sales fee for their first 180 days](20260601-new-weavers-pay-no-fee-at-first.md) | Accepted | Pricing |
EOF
