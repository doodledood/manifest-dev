# ADR: Autonomous figure-out shows a draft to an owner it can reach

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context
In `--autonomous` mode, figure-out resolves offers without waiting. The draft offer always took
the flagged-candidate branch: the content a draft needs is the owner's reaction, which a session
cannot derive, so the run produced no draft and recorded the choice as a Known Assumption
candidate (`ASM-*`).

Some autonomous runs can reach the owner. A run-ticket Question can be answered through a relay
that shows the owner an artifact and returns the reply, and a session can hold a question
capability the owner is watching. There the draft is the fastest way to get the owner's design
choice, and an assumption in its place guesses a decision the owner could have made in minutes.

The decision sits inside the North Star's Purpose: people keep control of the choices they retain
without supervising every step.

## Decision
Where the assignment or the host shows a channel that can show the owner an artifact and return
their reaction, autonomous mode accepts the draft offer: it produces the draft under figure-out's
draft rules (20261031-figure-out-drafts-are-unverified-and-shown-in-minutes), shows it through
that channel with the question it poses, asks for the reaction, and keeps working independent
branches while it is out. The choice the draft settles waits for the reaction; a read named before
it arrives carries the draft and a recommendation as awaiting the owner. Only where no reaction
can reach the owner does the offer become a Known Assumption candidate, as before.

## Alternatives Considered
- **Keep the assumption branch always**: no run waits on anyone — not chosen because where a
  channel exists, the assumption guesses a decision the owner can make quickly.
- **Treat any question capability as reaching the owner**: simpler — not chosen because an
  unattended run would block on a reply that never comes; the channel counts only when the
  assignment or the host shows it reaches the owner.

## Consequences

### Positive
- A relayed run gets the owner's design choice instead of a guess.

### Negative
- A run must judge whether a channel reaches the owner; a wrong "no" falls back to the
  assumption branch, a wrong "yes" leaves the choice waiting while independent work continues.

## Enforced by
partly — `tests/test_drafts_are_unverified.py` pins the reach-the-owner branch and the fallback in
`figure-out/references/autonomous.md`; whether a given channel reaches the owner stays judgment.

## Source
- Related: 20261031-figure-out-drafts-are-unverified-and-shown-in-minutes,
  20261024-absence-is-not-acceptance-of-optional-authority-offers
