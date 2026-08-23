# ADR: Every split Ticket is exercisable end-to-end; verticality governs cut direction, never count

## Status
Accepted

## Area
Ticketing

## Decision

When work becomes multiple Shaped Tickets — from any input path, not only a Manifest — every
Ticket must be a slice that can be exercised end-to-end on its own: put in front of its real use
and judged working, not merely inspected as present. A cut along an implementation layer ("the
data model", "the API", "the UI") is not a legal Ticket boundary, because such a Ticket's
definition of done can only check existence.

Verticality governs *where* cuts fall, never *how many* Tickets there are. The lifecycle test
from `20260812-tickets-follow-independently-schedulable-work-units` — split only where separate
ownership, priority, blocking, or closure has real value — still decides count, and the
one-Ticket-per-Manifest default stands.

`ticket-up` carries this discipline in its own files (skill and Ticket convention), stated for
any input. It does not assume a Manifest produced the work or defer the rule to `/define` — a
shipped skill stands alone.

Question Tickets are outside the rule: an investigation has no slice to run.

## Context

`ticket-up` produced layer-shaped Tickets when work reached it without passing through
`/define` — a direct work request, or a figure-out session handed straight to ticketing. The
Ticket unit is defined purely by lifecycle in both `ticket-up/SKILL.md` and
`TICKET_CONVENTION.md`; nothing required a split Ticket's outcome to be exercisable.

The gap was assumed closed rather than closed:
`20260812-tickets-follow-independently-schedulable-work-units` rejected never-splitting because
"deliberate delegation remains valuable when Deliverables are genuinely independent vertical
slices" — presupposing verticality without requiring it — and
`20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty` requires it only of
Manifest Deliverables, which non-Manifest input never has.

A layer Ticket reproduces at store level exactly the failure 20260726 names at manifest level:
its definition of done degrades to existence checks — the type exists, the module imports — the
weakest thing a done-judgment can assert, and the false-completion shape the workflows exist to
prevent.

## Alternatives Considered

- **Prefer many thin vertical slices (maximize splitting)**: reads "as vertically sliced as
  possible" as a granularity target — Rejected: it reopens the fragment-noise failure 20260812
  was decided to stop; a store full of thin Tickets reflects units of thought, not units anyone
  schedules. Count stays with the lifecycle test.
- **Route non-Manifest work through `/define` first**: one home for the cutting rule —
  Rejected: `ticket-up` legitimately serves direct requests and figure-out handoffs, and forcing
  a Manifest on them adds ceremony the input does not need.
- **Rely on the convention's definition-of-done quality bar**: hope a layer Ticket fails the
  "checks a stranger can judge" requirement — Rejected: an existence check is judgeable prose,
  so a layer Ticket passes that bar cleanly. The cut itself must be constrained.

## Consequences

### Positive
- Definitions of done can judge behavior, because every split Ticket has behavior to run.
- Parallel pickup yields increments that each land and prove themselves independently.
- The same slicing discipline holds on both sides of the `/define` boundary, so a Ticket's
  quality no longer depends on which path authored it.

### Negative
- The exercisability rule now lives in two homes — `/define`'s Deliverable cutting and
  `ticket-up`'s Ticket cutting — restated because shipped skills stand alone; the two must be
  kept in step by hand.
- Genuinely infrastructural work is harder to cut: the honest slice must still be exercisable
  against something, which is more demanding than cutting by layer — the same accepted cost
  20260726 records for Deliverables.

## Source
- Session: figure-out, ticket-up vertical slicing (2026-08-23)
- Narrows: 20260812-tickets-follow-independently-schedulable-work-units
- Related: 20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty
