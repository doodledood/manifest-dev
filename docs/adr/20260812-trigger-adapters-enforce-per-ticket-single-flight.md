# ADR: Trigger adapters enforce single-flight per Ticket

## Status
Accepted

## Area
Ticketing

## Context

Unattended Ticket automation can launch the same Ticket from two sources. An issue event provides an immediate run, while a scheduled sweep provides recovery and advances newly ready work. Both sources can fire while an earlier run remains active.

The Ticket's claim records ownership, not process liveness. Two runs under the same automation identity can therefore both accept the claim and work concurrently. That risks conflicting branch changes, duplicate pull requests, repeated comments, and races around merge or closure.

The system needs crash recovery without placing provider-specific liveness state inside the harness-neutral `run-ticket` skill.

## Decision

Every trigger adapter that can launch the same Ticket from more than one source must enforce single-flight by canonical Ticket identity. For GitHub Issues, the key is the repository and issue number.

At most one run for that key may be active. A later trigger waits until the active run ends, then resolves the Ticket again. It stops when the Ticket is closed or claimed by a person. It may continue an open Ticket claimed by the automation after the earlier run failed.

The trigger adapter owns this serialization because the host knows which executions remain active. `run-ticket` does not implement leases, heartbeats, or process-liveness detection. Different Tickets remain free to run concurrently.

## Alternatives Considered

- **Use the Ticket claim as the lock**: An assignee or equivalent claim already prevents a different owner from taking the Ticket. — Rejected because it does not distinguish two live runs under the same automation identity and does not show whether the owning process still exists.
- **Add a lease and heartbeat protocol to `run-ticket`**: Persist expiry and renewal state on each Ticket so another run can judge the prior claim stale. — Rejected because it adds timing policy, mutable coordination state, and provider-specific failure handling to a harness-neutral execution skill.
- **Serialize all automated Ticket work globally**: Permit only one automated Ticket run for the entire repository or store. — Rejected because unrelated ready Tickets can run safely in parallel; global serialization removes useful concurrency without improving same-Ticket safety.

## Consequences

### Positive

- Event and sweep triggers cannot execute the same Ticket concurrently.
- Crash recovery can retry a Ticket without adding lease machinery to `run-ticket`.
- Trigger integrations remain free to use their host's native concurrency mechanism.
- Independent Tickets retain parallel execution.

### Negative

- Every adapter that combines trigger sources must provide keyed serialization.
- A hung run blocks later runs for that Ticket until the host terminates or times it out.
- A queued trigger may start only to discover that the earlier run already completed or escalated the Ticket.

## Source

- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260812-run-ticket-owns-attempt-not-dispatch, 20260812-ticket-identity-follows-work-across-automated-attempts
