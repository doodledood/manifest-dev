# ADR: The scheduled Ticket sweep is recovery-first and handles one Ticket

## Status
Accepted

## Area
Ticketing

## Context

Issue events can launch an Auto Ticket quickly, but they are not a complete correctness mechanism.
A delivery can be missed, a runner can stop without a Ticket outcome, and closing a dependency does
not necessarily emit an event on every dependent Ticket that just became ready.

A scheduled worker can repair all three cases. It could batch the whole ready set, pulse labels to
retrigger issue automation, or execute one Ticket itself. The design needs a fallback that remains
easy to reason about and does not add queue state to Tickets.

## Decision

Add a scheduled `sweep-tickets` entrypoint that handles at most one Ticket per invocation. It first
looks for one open Auto Ticket claimed by the configured automation identity, representing an
interrupted attempt admitted after the adapter's per-Ticket single-flight wait. If none exists, it
selects one open, unassigned Auto Ticket with closed dependencies under the store's priority and
configured filter rules.

It passes that exact Ticket to `run-ticket` and stops. Issue-event triggers remain an optional fast
path; the sweep is the correctness and recovery path. Closing a predecessor makes dependents
eligible by the ordinary readiness rule, so no label pulse, ready label, or dependency-close
controller is introduced.

## Alternatives Considered

- **Remove and reapply `auto` from a schedule**: Reuse the label event as the only launch mechanism. — Rejected because it turns durable authority into a delivery pulse, can create event loops, and does not identify interrupted in-flight work cleanly.
- **Batch every eligible Ticket in one sweep**: Maximize throughput from the scheduled path. — Rejected because one failure then owns a batch lifecycle and the sweep becomes an orchestrator; independent issue events and Ticket keys already provide parallelism.
- **Use only issue events**: Avoid a schedule entirely. — Rejected because missed delivery, runner interruption, and dependency closure can strand work without another event on the eligible Ticket.
- **Have the sweep call `next-ticket`**: Reuse the human selector. — Rejected because `next-ticket` does not filter on Auto, claims work for presentation, and deliberately does not execute it.

## Consequences

### Positive

- One simple scheduled invocation can drive the whole graph eventually, even without issue events.
- Interrupted work is resumed before new work consumes capacity.
- Readiness stays derived from existing Ticket state.
- One-Ticket scope bounds failure handling and reasoning.

### Negative

- A schedule-only deployment advances at most one Ticket per invocation.
- Event triggers are still useful when low latency or parallel start matters.
- The adapter must expose a stable automation claim identity so recovery candidates are recognizable.

## Source
- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260812-trigger-adapters-enforce-per-ticket-single-flight, 20260812-ticket-recovery-uses-coherent-pushed-checkpoints, 20260812-human-assignment-pauses-auto-ticket-execution
