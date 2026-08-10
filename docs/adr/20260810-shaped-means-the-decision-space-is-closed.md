# ADR: Shaped means the decision space is closed, not that a workflow produced it

## Status
Accepted

## Area
Ticketing

## Context

The ticket convention's two kinds split on "ready to execute" (shaped) versus "needs figuring out first" (question) — and in practice tickets wearing the shaped label kept turning out to need a figure-out session before anyone could build them. The kind label is what tells a picker which tool to bring, and it was overpromising.

The candidate repair on the table was a provenance bar: shaped means a finished manifest or a full figure-out read stands behind the ticket. That bar had its own tension — a read-backed ticket still needs its gates written, and the two-equivalence distinction kept leaking workflow vocabulary into a convention meant to be readable by a stranger without manifest-dev.

## Decision

**A ticket is shaped when its decision space is closed: no open question remains whose answer would change what gets built or what done means.** One provably open crux makes it a question ticket, however much prior context it carries — a ticket holding the accumulated state of half a figure-out session is a question ticket with a thick "what's already known," not a shaped ticket.

**The line between a shaping decision and an execution choice: does its answer change what gets built or what done means?** If any competent answer is acceptable within the ticket's stated rules, it is execution, and leaving it open does not reopen shaped-ness.

The bar is a property of the ticket's content, not its provenance. No manifest, read, or any tool needs to have existed; a hand-written ticket can be genuinely shaped, and a manifest-produced ticket with a live crux is not. This keeps the convention self-contained for strangers, and it gives authors a falsifiable write-time test: try to name a question whose answer would change the work or its done.

## Alternatives Considered

- **Provenance bar** — shaped = backed by a finished manifest or a full figure-out read. — Rejected: imports tool vocabulary into a tool-agnostic convention; splits into two equivalence levels (read-backed work still needs gates written) that dissolve once the test is content-based; and it misclassifies in both directions — a manifest can exist while a crux is open, and a hand-written ticket can be closed-space without either artifact.
- **A third in-between kind** for partially-figured, rich-context work. — Rejected: that is a question ticket whose question is the remaining cruxes; the "what's already known" slot already carries the context.

## Consequences

### Positive

- The kind label becomes falsifiable at write time instead of a vibe about readiness.
- "Shaped work is usually automatable" becomes precise: unstated taste and deferred mid-flight decisions already disqualify shaped-ness, leaving authority as the only residual reason a shaped ticket needs a human.
- Mislabels are detectable in motion: an executor hitting an open crux escalates with the question rather than deciding it.

### Negative

- The stricter bar reclassifies many would-be shaped tickets as question tickets, which reads as a slower store even though the figuring-out was always owed.
- "Would this answer change what done means" is itself a judgment; authors can still get it wrong at the margin.

## Source
- Session: figure-out session, 2026-08-10
- Related: [20260810-auto-is-an-opt-in-grant-to-unattended-automation](20260810-auto-is-an-opt-in-grant-to-unattended-automation.md), [20260806-retire-decision-map-for-ticket-up-and-ticket-store](20260806-retire-decision-map-for-ticket-up-and-ticket-store.md)
