# ADR: An Auto Ticket completes only after its required landing

## Status
Accepted

## Area
Ticketing

## Context

`run-ticket` delegates implementation and verification to `auto`. For repository work, that chain
can finish with a pushed branch or a mergeable pull request while the Ticket's result is not yet on
the target branch. Closing the Ticket at that point would make dependents ready even though they
cannot rely on the change.

Keeping every merge as a human step would preserve that distinction, but it would also prevent an
Auto Ticket graph from advancing without routine intervention. The Auto grant already permits
unattended automation to do the work and judge it done, and is withheld when a known human approval
or irreversible authority decision is required.

## Decision

For an Auto Ticket, end-to-end authority includes the required landing. When repository work must
reach a target branch, `run-ticket` drives the pull request through normal checks and protections,
refreshes the Ticket authority, claim, pull-request head, and repository state immediately before
the irreversible action, merges through the protected mechanism, and observes the merged state.

Only then may it write DONE and close the Ticket. A branch or merely mergeable pull request is not a
completed repository outcome. Work whose durable result is an answer, deployment, or another
artifact uses that actual landing state instead.

A person may still invoke `run-ticket` directly on an ungranted Ticket. That direct invocation is
the authority for the supervised run; unattended adapters must establish Auto eligibility before
launch, and `run-ticket` refreshes Auto again before unattended landing.

## Alternatives Considered

- **Close after `/done`, before merge**: Treat verified implementation as completion. — Rejected because dependents could start before the required result exists on the target branch.
- **Always stop at a mergeable pull request for human merge**: Preserve a universal human merge gate. — Rejected because the Ticket graph would require routine intervention even where the author explicitly granted unattended end-to-end authority.
- **Let the trigger adapter press merge**: Keep irreversible actions outside `run-ticket`. — Rejected because the adapter would need to duplicate Ticket definition-of-done, pull-request, and terminal-outcome logic that belongs to the attempt.

## Consequences

### Positive

- Closed Tickets continue to mean their outcomes are actually available to dependents.
- Auto Ticket graphs can advance through ordinary repository work without routine merge handoffs.
- Landing uses the same repository protections as human work.

### Negative

- `run-ticket` must remain active through checks, mergeability, and merge observation.
- A withdrawn Auto grant or changed claim near merge stops the run even after implementation is complete.
- Repositories that require human approval cannot grant Auto to Tickets needing that approval.

## Source
- Session: unattended Ticket automation design (2026-08-12)
- Related: Narrows 20260810-auto-is-an-opt-in-grant-to-unattended-automation; see also 20260812-run-ticket-owns-attempt-not-dispatch, 20260812-ticket-identity-follows-work-across-automated-attempts
