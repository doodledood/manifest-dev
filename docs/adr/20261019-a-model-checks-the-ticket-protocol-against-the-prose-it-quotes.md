# ADR: A model checks the ticket protocol against the prose it quotes

## Status
Accepted

## Area
Ticketing

## Decided by
The user

## Context
The unattended ticket protocol — `orchestrate`, `run-ticket` and the one landing procedure in
ticket-up's shared automation reference — is prose that several agents follow at once, on a venue
with no locks. Its failures are orders of events: two orchestrators reading the same Ticket before
either writes, a head that moves after a ready mark, a run that dies between two writes. The
property suite checks that sentences are present; reading the prose checks the orders a reader
thinks of. A TLA+ model of the protocol, checked by TLC, found a landing that stalls for good and
two attempt records for one Ticket on the protocol as shipped on 2026-10-18, which the review of
that change had not found.

## Decision
- The repository keeps a TLA+ model of the protocol under `verification/models/ticket-protocol/`,
  checked by TLC on fixed configurations through a free recipe,
  `verification/recipes/ticket-protocol-model.md`. It is a maintainer check: nothing under
  `claude-plugins/` or `dist/` ships it or names its tools.
- Each action and property quotes the sentence it encodes and the file holding it;
  `tests/test_ticket_protocol_model.py` fails when a quoted sentence leaves its file, so a change
  to the protocol prose changes the model in the same change. An action that models the world
  says so instead of quoting.
- The recipe carries a scenario that switches the model back to the old behaviors and passes only
  when TLC reports their violations, so the check is seen to fail.
- `scripts/setup.sh` downloads one pinned version of the TLA+ tools and keeps it only when its
  checksum matches. A missing Java runtime or tools exits 3, which the harness records as
  unreachable.
- The Manifest's own text is not model-checked. The model checks the protocol a Manifest's run
  follows, not what a Manifest says.

## Alternatives Considered
- **Example tests of the protocol prose only**: they check the orders of events someone wrote down,
  which is what missed the stall.
- **A property-based test harness in Python simulating the protocol**: no new runtime, but it
  samples orders of events where TLC enumerates them within the bound, and it is a second
  implementation of the protocol to keep in step.
- **A model with no link to the prose**: drifts silently the first time the prose changes.
- **Ship a formal-verification skill to users**: a new skill and a new user step, outside the
  appetite of the change that added this.

## Consequences

### Positive
- A change to the protocol prose that reopens a race fails a check rather than waiting for a
  reader to find it.
- The quote links show which sentence each model step stands for.

### Negative
- Contributors who run the model need Java 11 or newer and a download of about 2 MB.
- The model checks one Ticket within a small bound; a fault that needs more is not checked.
- A quote that still stands while its meaning changed around it passes the drift test.

## Enforced by
`tests/test_ticket_protocol_model.py` — fails when a quoted sentence leaves its file, or an action
or checked property carries no quote, world or pre-fix mark; the `prefix` scenario of
`verification/recipes/ticket-protocol-model.md` fails when any prefix configuration stops
reporting the violation its restored old behavior causes.

## Source
- Session: figure-out and define reviewing manifest-dev's verification practice, and a model of
  the ticket protocol (2026-10-19).
- Related: see also 20261019-the-comment-the-venue-created-first-decides-each-ticket-fact,
  20261019-every-way-a-landing-cannot-merge-relaunches-or-escalates,
  20261015-every-check-a-harness-project-keeps-is-a-recipe
