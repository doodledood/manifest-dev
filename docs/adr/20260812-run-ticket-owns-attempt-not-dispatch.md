# ADR: run-ticket owns an execution attempt, not dispatch

## Status
Accepted

## Area
Ticketing

## Context

Hosted coding products can launch an agent from a GitHub event or another external trigger. Binding manifest-dev to one provider's webhook, event payload, checkout setup, or runner API would duplicate that infrastructure and make the workflow unusable in another harness.

The existing `next-ticket` skill solves a different problem: it ranks ready work, claims one Ticket, and presents the choice to a person. Combining selection, dispatch policy, and execution would make manual invocation ambiguous and let a missing trigger input turn into an unintended backlog pick.

## Decision

Add a harness-neutral `run-ticket` skill that receives exactly one Ticket, claims it, invokes `auto` with that Ticket as the task contract, and records DONE or ESCALATED evidence on the same Ticket.

The dispatcher owns event delivery, agent launch, credentials, checkout, and the policy that decides which Tickets to run. `run-ticket` does not scan the store, invoke `next-ticket`, or enforce the Auto grant. Missing or ambiguous Ticket input fails before work. A person may invoke it manually on an ungranted Ticket.

`next-ticket` remains the human-facing selector: it claims and presents one Ticket, then stops. Selection and execution are separate actions.

## Alternatives Considered

- **Build a GitHub-specific webhook workflow in manifest-dev**: Provides a turnkey integration. — Rejected because hosted runners already own launch mechanics and each provider exposes a different contract.
- **Have run-ticket call next-ticket when input is missing**: Makes manual use convenient. — Rejected because an execution entrypoint would silently choose unrelated backlog work when a trigger payload is incomplete.
- **Require Auto inside run-ticket**: Adds defense in depth for unattended use. — Rejected because Auto is dispatch policy and the same skill must remain available for deliberate manual runs.
- **Make next-ticket execute its pick**: Removes one explicit boundary. — Rejected because asking what comes next should not begin an autonomous attempt.

## Consequences

### Positive
- Claude Code, Codex, Pi, OpenCode, and future harnesses can use the same execution skill.
- Trigger failure cannot become accidental backlog selection.
- Manual and unattended execution share one terminal-outcome path.

### Negative
- Each hosted runner still needs a small adapter that supplies the exact Ticket context.
- Dispatchers must enforce Auto and any trusted-actor policy outside the skill.

## Source
- Session: unattended Ticket automation design (2026-08-12)
- Related: 20260810-next-ticket-claims-the-ticket-it-picks, 20260812-ticket-identity-follows-work-across-automated-attempts
