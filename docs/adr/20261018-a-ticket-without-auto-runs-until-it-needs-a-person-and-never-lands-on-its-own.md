# ADR: A Ticket without Auto runs until it needs a person, and never lands on its own

## Status
Accepted; amended by 20261023-assignment-bounds-delegated-decisions-and-retained-acceptance: assignment scope, delegated decisions and retained acceptance

## Area
Ticketing

## Decided by
The user

## Context
Under 20260810-auto-is-an-opt-in-grant-to-unattended-automation, a Ticket without Auto is fenced
off from automation entirely: no partial preparation, nothing. That record rejected the alternative
in which Auto decides only where a run ends, because automation would then touch every item,
including Tickets from people the owner does not trust and venue items that were never Tickets.

`orchestrate` now runs many Tickets at once, and the owner wants that capacity used. In the owner's
words, a Ticket without Auto is one that cannot be completed without their judgment, and that must
not be merged without them. It is not one that automation should leave alone. Under the full fence,
such a Ticket waits for a person to start it, even when most of its work needs no one.

Two protections from the 2026-08-10 record still apply. Ticket bodies and comments are untrusted work
context, and on a public repository anyone can open an issue. GitHub lets only people with triage or
write access label an issue as a Ticket, and the Ticket's author is known on every supported venue.

## Decision
- Auto keeps its grant criterion and its author's choice. What its absence means changes: a Ticket
  without Auto may be worked by automation, but never completed or landed by it.
- `orchestrate`, in both modes, works a Ticket without Auto when the Ticket is in its scope, has no
  person assigned, and was written by someone with write access to the repository. Its run asks
  for the person's judgment through the escalation mark wherever it needs it, keeps its progress on
  the Ticket, and stops at a ready pull request. Only a person lands it. A Question Ticket without
  Auto stops with its answer drafted on the Ticket, and a person accepts the answer before it closes.
- In `--autonomous`, these Tickets run beside Auto Tickets, ranked by the same delay-loss rule. A
  Ticket waiting on the person holds no run slot.
- A Ticket whose author lacks write access is never worked unattended. A person with write access
  can grant it Auto, or include it in a plan they approve in default mode. The status page lists it
  as left alone, with the reason.
- Venue items that are not Tickets stay untouched, as before.

## Alternatives Considered
- **Keep the full fence**: the standing design. A Ticket without Auto waits for a person to start it,
  and `orchestrate`'s capacity sits idle while it waits.
- **A preparation pass only**: investigate, write the person's questions on the Ticket, and stop
  without code. Less work is wasted on Tickets the person rejects, but the work waits for a second
  run once the questions are answered.
- **Work every Ticket regardless of author**: the most throughput, but an outside contributor's
  issue text would steer an unattended agent on a public repository.

## Consequences

### Positive
- Work that needs the person only for a decision or a review progresses unattended up to that point.
  The person's time goes to judgment and review.
- Auto now says one thing: the work can be finished and landed without anyone's judgment.

### Negative
- Quota is spent on work no person has approved, including work the person rejects at review. The
  North Star judges cost per unit of merged work, so rejected work counts against it.
- Untrusted Tickets are no longer covered by silence. The fence for them now rests on the write-access
  check, which every venue reference must say how to make.
- More pull requests wait on the person's look at once.

## Enforced by
`tests/test_ticket_automation_prompts.py` — `test_a_ticket_without_auto_runs_to_a_ready_pull_request_and_never_lands` fails if the
convention, `orchestrate`, `run-ticket` or the landing procedure lets automation land or complete a
Ticket without Auto, drops the write-access or no-assignee condition, ends such a Ticket anywhere
but a ready pull request or an escalation, or a venue reference stops saying how to check the
author's write access; `test_ticket_up_preserves_auto_authority_boundary` is retargeted to the
grant path that sits beside the new meaning of absence.

## Source
- Session: define on running unattended Ticket work with many agents at once (2026-10-18).
- Related: amends 20260810-auto-is-an-opt-in-grant-to-unattended-automation; see also
  20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep,
  20261018-orchestrate-lands-and-run-ticket-stops-at-a-ready-pull-request,
  20260812-human-assignment-pauses-auto-ticket-execution
