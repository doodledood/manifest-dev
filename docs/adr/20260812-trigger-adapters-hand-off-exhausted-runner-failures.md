# ADR: Trigger adapters hand off exhausted runner failures

## Status
Accepted

## Area
Ticketing

## Context

`run-ticket` can write DONE or ESCALATED only while an agent is alive. A provider process can crash,
time out, or fail before the skill reaches either outcome. Leaving that distinction implicit can
strand an automation-owned Ticket forever; treating every process failure as a Ticket blocker can
instead wake a person for a transient infrastructure fault.

The provider already knows execution liveness and often supplies retry and terminal-failure hooks.
The Ticket workflow needs a bounded bridge from that host state back to a visible human handoff
without recreating retry machinery inside the Ticket Store.

## Decision

The trigger adapter configures a finite provider-native retry policy. If every retry ends without a
Ticket-level DONE or ESCALATED outcome, its terminal failure hook refreshes the Ticket. When the
Ticket remains open and is not assigned to a person, the hook writes or updates one operational
handoff comment with the failed run references and last discoverable branch or pull request, states
that no terminal Ticket outcome was recorded, and assigns the configured human.

The hook is idempotent and uses a stable comment marker. Retry count, delay, timeout, and schedule
cadence remain provider configuration. No retry counter, heartbeat, lease, or failure label is
stored on the Ticket.

## Alternatives Considered

- **Escalate on the first runner failure**: Assign a person immediately. — Rejected because transient provider failures would consume human attention before the host's ordinary recovery mechanisms run.
- **Retry forever**: Leave the Ticket with automation until one attempt succeeds. — Rejected because a persistent infrastructure or integration failure would remain invisible and block the graph indefinitely.
- **Let `run-ticket` detect its own crash**: Write ESCALATED from the skill. — Rejected because a stopped process cannot reliably report its own terminal state, and the skill does not know which host jobs remain live.
- **Persist retry counters and leases on the Ticket**: Make recovery independent of the provider. — Rejected because it duplicates host liveness state and adds mutable coordination machinery to the Ticket model.

## Consequences

### Positive

- Transient failures get bounded automatic recovery before a person is interrupted.
- Exhausted infrastructure failures become visible and claimed rather than silently stranded.
- Ticket state remains small and provider-neutral.

### Negative

- Every trigger integration needs a terminal failure hook or equivalent finalizer.
- The handoff can conservatively pause a Ticket whose last process failed after completing durable work but before writing its outcome.
- Retry tuning remains an operational responsibility outside manifest-dev.

## Source
- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260812-trigger-adapters-enforce-per-ticket-single-flight, 20260812-ticket-recovery-uses-coherent-pushed-checkpoints, 20260812-human-assignment-pauses-auto-ticket-execution
