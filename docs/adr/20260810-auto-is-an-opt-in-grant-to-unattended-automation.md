# ADR: The Auto marker is an opt-in grant; absence fences automation off entirely

## Status
Accepted

## Area
Ticketing

## Context

Ticket stores are about to feed unattended automation: a dispatch flow that picks the next eligible ticket and sends an agent at it with nobody watching. That flow needs to know, per ticket, whether an agent may take it end to end — and store venues can be shared surfaces (GitHub Issues holds convention tickets next to human-filed issues), so it equally needs to know what to leave alone.

Three tensions shaped the decision. Any agent run can hit a surprise and escalate, so no marker can promise "no human ever." An agent could usefully work *part* of almost any ticket, so "can an agent help" does not discriminate. And whether a ticket is safe to hand over is a write-time judgment resting on trust and context a picker does not have.

## Decision

**Auto is a per-ticket marker granted at write time, on either kind of ticket — shaped or question — and its absence is the fence.** Marker present: unattended automation may take the ticket end to end, doing the work and judging it done. Marker absent: automation does not touch the ticket at all — no partial prep, no half-commits, nothing.

**The criterion for granting: neither doing the work nor judging it done needs any human's knowledge, taste, or authority.** Unstated taste in the done-judgment and deferred mid-flight decisions are open cruxes and already disqualify a ticket from being shaped; for shaped tickets the residual disqualifier is authority — an approval, access the agent won't have, or an irreversible act. The criterion is necessary but never sufficient: the author still chooses to grant, and withheld trust alone is a legitimate reason not to.

**Escalation stays the exception valve and does not demote a ticket.** A granted ticket that hits a surprise blocker stops and surfaces; the grant was still honest at write time. Only a *known* human step, or withheld trust, keeps the marker off.

Default-off is what makes shared venues safe: nothing is ever marked "not auto" — untrusted tickets, tickets with designed-in human steps, and venue items never written as tickets are all covered by silence. Supervised agent help on unmarked tickets remains available; that is a human dispatching manually, outside the marker's jurisdiction.

## Alternatives Considered

- **Expected-terminal-state semantics**: auto = the run ends at done; non-auto = the run ends at a prepared handoff (branch pushed, refs written, human's part teed up). — Rejected: it has automation touching every ticket, which is exactly what the owner of an untrusted ticket doesn't want, and it gives a shared venue's non-ticket items no protection at all.
- **Derive eligibility at pick time** instead of storing a marker. — Rejected: the judgment needs write-time context and trust; an unattended agent deciding for itself "I can take this end to end" is the failure the marker exists to prevent.
- **A third ticket kind.** — Rejected: auto is orthogonal to kind — question tickets can be auto too, since investigation runs autonomously; folding auto into kind would fence agents out of discoverable-answer investigation work.
- **Filter on provenance** (manifest-opened tickets vs everything else). — Rejected: origin correlates with the grant but isn't it — a manifest ticket with an authority step must not be picked, and a hand-written ticket that clears the bar legitimately can be.

## Consequences

### Positive

- One default-off rule covers untrusted tickets, human-step tickets, and unrelated venue items — nothing needs negative marking, and automation on a shared venue is safe by construction.
- The dispatch flow gets a per-ticket success contract: a granted ticket either closes or escalates; it never silently half-finishes.
- Human attention is priced at write time: ungranted tickets are visibly the owner's queue.

### Negative

- Every eligible ticket needs its grant written explicitly; a forgotten grant hides work from automation until someone notices.
- Grant quality rests on the author's judgment of the criterion — a wrongly granted ticket is caught only by the escalation valve.
- Agent help on ungranted tickets must be dispatched and supervised manually; the store offers no middle tier.

## Source
- Session: figure-out session, 2026-08-10
- Related: [20260810-shaped-means-the-decision-space-is-closed](20260810-shaped-means-the-decision-space-is-closed.md), [20260806-retire-decision-map-for-ticket-up-and-ticket-store](20260806-retire-decision-map-for-ticket-up-and-ticket-store.md)
