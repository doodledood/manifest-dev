# ADR: Only a person grants Auto to a follow-up

## Status
Accepted

## Area
Ticketing

## Decided by
The user

## Context
A Ticket run that finds separate work tickets it up as a follow-up. Under
20260814-human-authored-follow-ups-may-grant-auto-independently, a follow-up written without a
person's grant still carried Auto when its source carried Auto and the follow-up passed the grant
criterion on its own. The agent that found the work applied that criterion itself, so an
unattended chain could keep feeding its own queue with work no person had chosen. The owner ruled,
in 20261015-projects-drive-themselves-as-far-as-each-user-climbs, that agents never grant
themselves work.

## Decision
- A follow-up carries Auto only when a person grants it at its own `ticket-up` boundary — directly
  authoring it, or explicitly reviewing and authorizing Auto there — after it passes the grant
  criterion. The person still chooses; Shaped never implies Auto.
- Without that grant a follow-up carries no Auto, whatever its source carries. A source's Auto
  never carries over, and an agent never applies the grant criterion on its own behalf.
- A person merely invoking `run-ticket` on a source is still not a grant for the follow-ups found
  inside that run.
- Everything else about Auto stands: an ordinary new Ticket is granted by its author, absence is
  the fence, and Auto is durable authority rather than queue state.

## Alternatives Considered
- **Keep the source-Auto path for unattended follow-ups**: lets a granted chain continue without a
  person. — Rejected: the queue then grows on work no person judged worth doing, which the owner's
  ruling exists to stop, and the criterion is applied by the agent whose work it widens.
- **Never grant Auto to any follow-up**: the simplest fence, rejected in
  20260812-auto-follow-up-grant-requires-source-and-local-grant because it blocks safe automation.
  — Still rejected: a person reviewing a follow-up at the authoring boundary can grant it, and
  that keeps the person as the filter without making every discovery wait forever.

## Consequences

### Positive
- The queue of unattended work holds only what a person granted, so a self-feeding system cannot
  grow on agent-chosen work.
- The rule is shorter: one path to Auto for a follow-up, a person's grant.

### Negative
- Unattended runs no longer chain: each follow-up waits for a person to grant it before automation
  takes it.

## Enforced by
`tests/test_ticket_automation_prompts.py` — `test_ticket_up_preserves_auto_authority_boundary`
fails if ticket-up lets a source's Auto carry over to a follow-up, drops the person's grant at the
boundary, drops the limit on manual `run-ticket` calls, or drops "Shaped never implies Auto".

## Source
- Session: the owner's ruling on the North Star's open questions about unattended work.
- Supersedes 20260814-human-authored-follow-ups-may-grant-auto-independently
- Related: 20261015-projects-drive-themselves-as-far-as-each-user-climbs, 20260810-auto-is-an-opt-in-grant-to-unattended-automation
