# ADR: Human assignment pauses Auto Ticket execution

## Status
Accepted — its escalation branch is narrowed by 20260825-escalation-clears-the-claim-and-carries-its-own-mark: escalation no longer assigns the person needed next, but clears the claim and records the escalated state in its own marked handoff record, which every unattended dispatch path excludes. The rejection of a separate marker is overturned for that state alone. Human claims continue to pause unattended execution, and an automation-held claim continues to mean an interrupted attempt eligible for the sweep's recovery path.

## Area
Ticketing

## Context

An Auto Ticket can encounter a blocker that needs human knowledge, taste, access, or authority. Escalation leaves the Ticket open because its work remains incomplete, and it assigns the person needed next. The `auto` label remains the durable grant for unattended execution.

The system needs one clear operation that returns the Ticket to automation after the person resolves the blocker. Adding a retry label or assigning the automation identity would create another runnable state beside the existing readiness rule.

## Decision

A human claim pauses unattended execution of an Auto Ticket. Event and sweep dispatchers ignore Tickets assigned to a person, even when `auto` remains present and all dependencies are closed.

After resolving the blocker and recording any context needed for continuation, the person unassigns the Ticket. The existing readiness rule then applies: an open, unassigned Auto Ticket with closed dependencies is eligible for unattended execution. A scheduled sweep guarantees eventual pickup; an adapter may also react to the unassignment event for lower latency.

No retry label, status, or automation-queue assignment is added. An open Ticket claimed by the automation remains distinct: it represents an interrupted automated attempt eligible for the sweep's recovery path, not a human handback.

## Alternatives Considered

- **Remove `auto` on escalation and restore it after human resolution**: Use the grant label as both pause state and retry signal. — Rejected because escalation would erase durable automation authority, and a missed restoration would strand the Ticket.
- **Assign the Ticket back to the automation identity**: Make reassignment the explicit handback operation. — Rejected because it creates a second runnable state, claimed-but-queued, beside the existing open-and-unassigned readiness rule.
- **Add a retry label or status**: Mark the Ticket ready for another automated attempt after human resolution. — Rejected because readiness is already derived from claim, dependency, and open state; another marker can drift from those sources.

## Consequences

### Positive

- Human pause and handback use the existing claim lifecycle.
- `auto` remains a stable grant rather than mutable queue state.
- Dispatchers derive eligibility from one readiness rule.
- Crash recovery remains distinguishable from human escalation by claim owner.

### Negative

- The automation must use a stable, recognizable claim identity.
- A person who resolves the blocker but forgets to unassign the Ticket leaves automation paused.
- Without an unassignment event trigger, continuation waits for the next scheduled sweep.

## Source

- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260810-auto-is-an-opt-in-grant-to-unattended-automation, 20260812-ticket-identity-follows-work-across-automated-attempts, 20260812-trigger-adapters-enforce-per-ticket-single-flight
