# ADR: An Auto follow-up requires both source authority and its own grant

## Status
Accepted

## Area
Ticketing

## Context

An automated Ticket attempt can discover separate work and ask `ticket-up` to create a follow-up. If the follow-up always inherited Auto, a broad source grant could silently expand into work whose risks and done judgment were never considered. If every follow-up always withheld Auto, safe automated work would stop at each discovery and lose the recursive execution the grant was meant to permit.

Manual execution adds a second boundary. `run-ticket` deliberately permits a person to run an ungranted Ticket, so the execution path alone cannot confer authority on work it discovers.

## Decision

A follow-up Ticket receives Auto only when both conditions hold:

1. its source Ticket carries Auto; and
2. the follow-up independently meets the normal Auto grant criterion and the authoring step chooses to grant it.

Either condition failing withholds Auto. In particular, an ungranted source can create only ungranted follow-ups, including when a person manually invokes `run-ticket` on it.

## Alternatives Considered

- **Always inherit Auto from the source**: Preserves uninterrupted automation. — Rejected because the source grant did not assess the discovered work and a manual run could create unattended work indirectly.
- **Never grant Auto to follow-ups**: Makes every discovery a human checkpoint. — Rejected because it blocks safe recursive automation even when both the original authority and the follow-up's own risk profile support it.
- **Judge only the follow-up**: Treat each new Ticket as independent of its source. — Rejected because it lets execution of an ungranted source create new unattended work, bypassing the dispatch boundary.

## Consequences

### Positive
- Recursive automation stays inside an explicitly granted chain.
- Every follow-up still receives its own safety and judgment check.
- Manual runs cannot create unattended work indirectly.

### Negative
- A safe follow-up from an ungranted source waits for a human grant.
- Ticket authors must carry the source grant into the follow-up decision.

## Source
- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260810-auto-is-an-opt-in-grant-to-unattended-automation, 20260812-ticket-identity-follows-work-across-automated-attempts
