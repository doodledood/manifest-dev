#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/adr notes
cat > docs/adr/20260310-member-notices-go-by-email-only.md <<'EOF'
# ADR: Member notices go by email only

## Status
Accepted

## Area
Notifications

## Decided by
The user

## Context
The app needs to tell members about session changes. Every member gives an email address when
they join. Our SMS provider charges 6p a message. Notices run to about 2,000 messages a month,
so SMS would cost about £120 a month. The club's whole software budget is £50 a month, and SMS
would take more than all of it.

## Decision
Member notices, cancellations included, go by email only. The app sends no SMS.

## Alternatives Considered
- **SMS for everything.** Rejected: about £120 a month, over the whole budget.
- **SMS for cancellations only.** Rejected: about 300 messages a month, about £18, which still
  takes over a third of the budget.

## Consequences
- Members who do not read email miss notices.
- No messaging cost.

## Revisit when
The SMS provider's price falls below 1p a message, read on its price page.

## Source
- Committee meeting, March 2026.
EOF
cat > docs/adr/README.md <<'EOF'
# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-03-10 | [Member notices go by email only](20260310-member-notices-go-by-email-only.md) | Accepted | Notifications |

The next record's file is reserved as `20261026-cancellation-notices.md`. A reserved draft at that
path is not an accepted record; a new record replaces the draft at that path.
EOF
cat > NORTH_STAR.md <<'EOF'
# North Star — Brightwater Swim Club app

Every position carries a state: evidence, hypothesis, ruled, or empty.

## Who it's for

Members of a volunteer-run swim club (about 400, a third of them families booking for
children), and the volunteers who run sessions.

— evidence: 2026-06, membership list.

## Goal

Members turn up to the sessions that run, and never to ones that don't.

— ruled: 2026-03, the committee.
EOF
cat > notes/cancellations.md <<'EOF'
Cancellations, September 2026: 14 sessions cancelled (lifeguard absence, pool maintenance).
Most were cancelled on the day, between 2 and 5 hours before the session.

31 members arrived for a cancelled session. We asked 20 of them how they heard about sessions:
17 said they never or rarely open club email, and several said it goes to a family inbox one
parent reads at the weekend. Everyone who joined since June gave a mobile number too; 88% of
members have one on file.

Email open rate for cancellation notices: 22% within 5 hours of sending.
EOF
cat > notes/budget.md <<'EOF'
Treasurer's note, 2026-09-02.

The council's community sport grant renewed in August with a new line: up to £40 a month for
member safety messaging, ring-fenced, for at least the next two years. It cannot be spent on
anything else. Nothing has drawn on it yet.

Software budget otherwise unchanged at £50 a month. Our SMS provider still charges 6p a message.
EOF
# No conventions file: the plugin's shipped ADR format governs, so the case measures it.
# A reserved draft lets the content judge distinguish no record from an accepted record.
cat > docs/adr/20261026-cancellation-notices.md <<'EOF'
<!-- Reserved record slot. No decision record has been written. -->
EOF
