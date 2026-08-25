# ADR: Escalation clears the claim and carries its own mark

## Status
Accepted

## Area
Ticketing

## Context

A claim on a Ticket expresses two states: unclaimed means takeable, and claimed means someone or
something is working it. Escalation produces a third that neither covers — an attempt ended, a
person is needed, and nobody is working it. The convention squeezed that third state into the claim
field: escalation assigned the person needed next, and the human claim paused automation.

Two defects follow from the squeeze.

`run-ticket` cannot always assign a person, so it carries a fallback — preserve a claim and mark the
handoff plainly. The preserved claim is held by the automation identity, and an automation-held
claim is defined as an interrupted attempt the sweep's recovery path may resume. The scheduled sweep
therefore recovers an escalated Ticket, `run-ticket` sees its own identity on the claim and takes
the recovery path, the same human-needing blocker recurs, and the Ticket escalates again every tick.
The prose marker written to prevent this has no reader: both the sweep's selection rule and
`run-ticket`'s recovery trigger key on claim identity, not on comment text.

The second defect is on the human side. Ticket selection minimizes delay loss among ready Tickets,
and ready requires unclaimed. An escalated Ticket is claimed, so the human picker filters out the
one Ticket that just declared it needs a person, surfacing it only when nothing else is ready. A
tracker's assignment notification delivers the handoff once; it is not a queue the person can return
to a week later.

Resolving the second defect is what forecloses the narrower fix. Requiring escalation to always land
on a human claim closes the sweep loop, but leaves the picker skipping the Ticket unless the picker
begins admitting claimed Tickets — at which point the picker must itself distinguish parked from
actively held, and the overload has moved rather than gone.

## Decision

**Escalation clears the claim and records the escalated state as its own durable fact.**

An escalated attempt writes its handoff record and releases the claim rather than assigning a person
or preserving an automation claim. The Ticket returns to open and unclaimed, so the human picker
admits it into the ordinary delay-loss comparison with no special case — an escalated Ticket
competes for human attention on the same terms as any other candidate, and the handoff record names
the person whose input is needed.

The escalated state lives in the handoff record itself, made machine-readable with a hidden marker,
following the attempt-checkpoint comment that already carries one. No field is added to the Ticket
anatomy.

Every unattended dispatch path excludes escalated Tickets: the scheduled sweep when it builds its
eligible set, and the trigger adapter's event eligibility. The adapter check is load-bearing rather
than defensive — clearing the claim is itself an unassignment event, one of the events an adapter
listens for, so without the check the event path relaunches the run immediately.

After resolving the blocker, the person records the continuation context and clears the escalation
mark. That single act restores unattended eligibility, replacing the unassignment that previously
served the same purpose.

The Auto grant is untouched throughout. Human claims continue to pause unattended execution; only
escalation stops expressing its pause through the claim field.

## Alternatives Considered

- **Escalation always lands on a human claim**: Remove the preserve-an-automation-claim fallback so
  a human assignee is the invariant, rendering the person in the body where a venue cannot assign
  them natively. — Rejected because it closes only the sweep loop. The picker still skips the
  Ticket, and admitting claimed Tickets there forces the picker to tell parked from actively held,
  relocating the overload instead of removing it.
- **A third Status value, `escalated`**: Give the state a slot in the Ticket anatomy beside `open`
  and `done`. — Rejected because Status is deliberately two-valued and derived state is kept out of
  it; the handoff record is already written on every escalation and needed only a reader.
- **Remove the Auto grant on escalation**: Let the absence of Auto fence automation off, since a
  Ticket needing a person is the negation of the grant. — Rejected on the standing rule that Auto is
  durable authority rather than mutable queue state, and that a surprise mid-attempt is the
  exception path working rather than evidence the grant was wrong.
- **Leave escalated Tickets permanently outside unattended execution**: Nothing to clear, so nothing
  can be forgotten. — Rejected because it discards work the grant still authorizes once the blocker
  is gone, for a class of blockers that are usually one-time.

## Consequences

### Positive
- The claim field carries one meaning again; the sweep's recovery path and the picker's readiness
  rule read it the same way.
- The human picker needs no change to honor delay-loss comparison for escalated work.
- The re-escalation loop cannot occur on either dispatch path.
- The handoff record gains a reader instead of the system gaining a state surface.

### Negative
- Re-entry stops being free. Clearing the claim previously doubled as the handback signal; a
  separate mark must now be cleared, and a person who forgets leaves the Ticket invisible to
  automation with nothing announcing it.
- The escalated check must be stated in three places — the sweep, the adapter's event eligibility,
  and each venue reference — and a venue reference written for an unmapped tracker must carry it too.
- Reading escalated state costs a comment fetch per candidate on venues that render the handoff as a
  comment.

## Source
- Session: figure-out on cross-awareness among the Ticket skills (2026-08-25)
- Related: 20260812-human-assignment-pauses-auto-ticket-execution,
  20260812-ticket-identity-follows-work-across-automated-attempts,
  20260812-scheduled-ticket-sweep-is-recovery-first-and-one-ticket,
  20260812-trigger-adapters-enforce-per-ticket-single-flight,
  20260814-ticket-selection-minimizes-delay-loss-across-available-executors
