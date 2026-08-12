# ADR: Ticket recovery uses coherent pushed checkpoints

## Status
Accepted

## Area
Ticketing

## Context

An unattended `run-ticket` execution can stop before it reaches DONE or ESCALATED. A later scheduled run must continue the Ticket without access to the earlier agent's conversation or local workspace.

The Ticket already holds the work contract, while Git can preserve committed work and a pull request can preserve review and CI state. Preserving every local edit would require frequent work-in-progress commits, external workspace snapshots, or provider-specific session restoration. Those mechanisms add coordination state and can preserve changes before they form a coherent checkpoint.

The recovery contract needs a clear durability boundary that works across harnesses and providers.

## Decision

Repository work for one Ticket uses one stable remote branch. `run-ticket` creates or reuses that branch, records it in one early attempt comment on the Ticket, and reuses any pull request already associated with it.

The running agent pushes coherent checkpoints. A later attempt reconstructs the work from the Ticket, remote branch, pushed commits, pull request, and CI state. It does not depend on prior conversation context or a preserved local workspace.

Uncommitted work and commits that were not pushed may be lost when a runner stops. The later attempt restarts that portion from the Ticket and the latest pushed checkpoint. The contract does not require a push after every edit or arbitrary time interval.

## Alternatives Considered

- **Persist and restore the complete agent session and workspace**: Resume with the prior conversation and every local edit. — Rejected because it binds recovery to provider-specific session storage and makes the harness-neutral workflow depend on execution infrastructure it does not control.
- **Push every local change as a work-in-progress checkpoint**: Minimize lost edits by committing and pushing continuously. — Rejected because it creates noisy history and can expose partial changes that do not form a useful recovery point.
- **Record branch and pull-request references only at DONE or ESCALATED**: Keep Ticket comments limited to terminal outcomes. — Rejected because a runner that stops before either terminal leaves a fresh attempt with no reliable pointer to preserved work.

## Consequences

### Positive

- Any fresh agent can recover from durable repository and Ticket state.
- Recovery remains independent of agent conversations and provider workspaces.
- One branch and pull request retain a continuous history across attempts.
- Checkpoint frequency follows coherent work boundaries rather than a timer.

### Negative

- A crash can lose work completed after the latest pushed checkpoint.
- `run-ticket` must create or resolve the stable branch and record it before substantial repository work.
- Agents must inspect existing branch, pull-request, and CI state before continuing.

## Source

- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260812-ticket-identity-follows-work-across-automated-attempts, 20260812-trigger-adapters-enforce-per-ticket-single-flight
