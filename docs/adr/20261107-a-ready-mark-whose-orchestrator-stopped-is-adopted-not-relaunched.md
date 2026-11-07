# ADR: A ready mark whose orchestrator stopped is adopted, not relaunched

## Status
Accepted

## Area
Ticketing

## Decided by
An agent in an unattended run, with no review — under the owner's delegation to fix the
findings of an audit of the skills' state machines

## Context
20261019-every-way-a-landing-cannot-merge-relaunches-or-escalates put in *To land* only Tickets
marked ready by the orchestrator's own run, and had one left by an orchestrator that stopped
taken over and relaunched. Orchestrators stop routinely: an autonomous one stops once only a
pull request held for review is left, and every new session takes a new orchestrator ID. Two
premises of that decision do not hold.

- A relaunch of a ready pull request held for a review is the redispatch that
  `AUTOMATED_EXECUTION.md` → *Waiting and acceptance* rules out: a held result "is never
  redispatched merely because acceptance has not arrived". Relaunching it spends a run on work
  that is done and waits only on a person.
- The orchestrate sort as written had no category for such a Ticket at all. It was not left
  alone once the run's timeout passed, not *To land* because the mark was not its own, not *To
  recover* because the run had written an outcome, and not *Ready* because it was claimed. Launch
  takes only planned Tickets, so the takeover was never reached, and approved work never landed
  or reached the person's list. A model of the protocol with an orchestrator that stops reports
  this as a ready Ticket that never resolves.

20261019-the-comment-the-venue-created-first-decides-each-ticket-fact gave the ready mark one
writer, the run that marked it. The decision sits inside the North Star's Purpose: delegated work
proceeds without the person supervising every step.

## Decision
- *To land* also holds a Ticket whose ready mark another orchestrator's run left, once that run's
  timeout has passed and no run is live. Before its landing turn the orchestrator adopts the
  mark: it writes a run ID of its own into the run facts and into the mark, keeps the head and
  base commits the mark names and the launch count, writes a fresh start time, starts no run, and
  re-reads the Ticket as a launcher does.
- Adoption is the ready mark's one other writer. The landing procedure then checks the adopted
  mark exactly as it checks one of its own run's: the head is pinned, a moved base relaunches the
  run, and a held review keeps the Ticket held.
- A *To recover* Ticket another orchestrator left is still taken over by its launch.
- The timeout stands for the holder's absence, not the run's age. An orchestrator holding a
  Ticket ready to land, Auto or not, rewrites the start time in its run facts at a check-in once
  half the timeout has passed since it, so another orchestrator adopts the mark only once the
  holder has stopped checking in.

## Alternatives Considered
- **Take it over and relaunch, as before**: a relaunch of finished work, and of a held pull
  request a redispatch the waiting rule forbids; every later orchestrator would launch it again.
- **Measure the timeout from the run's start alone**: a ready pull request held for review
  routinely waits longer than a run timeout, so a live orchestrator's held Ticket was adopted by
  another, its own landing turn then stopped at Landing step 1, and ownership changed hands every
  timeout.
- **Leave it to a person**: the work is finished and the landing procedure already checks it;
  sending it to a person adds a step nothing needs.
- **Let any orchestrator land a mark it did not write without rewriting the run facts**: the
  run-facts binding is what stops two orchestrators landing one Ticket at once, and what lets a
  relaunched run's earlier mark stop counting; dropping it reopens both races.

## Consequences

### Positive
- A Ticket whose orchestrator stopped after its run marked it ready lands at a later
  orchestrator's landing turn, or stays held for the review it waits on, and never runs again
  merely to change hands.
- Every open Ticket state fits an orchestrate category.

### Negative
- The ready mark has two writers, so the one-writer rule now names an exception.
- A held pull request waits a run timeout after its holder's last check-in before a new
  orchestrator can adopt it.
- The holder writes its run facts again about once every half timeout for each Ticket it holds.

## Enforced by
`tests/test_orchestrate_sort.py` enumerates every abstract state of an open Ticket against
orchestrate's sort, quoting each category, and fails on any state that fits none;
`verification/recipes/ticket-protocol-model.md` → `stopped` model-checks that the adopted mark
lands or stays held and that a held pull request is never relaunched (`HeldNotRedispatched`),
`races`, `race-landing` and `stopped` check that a mark is adopted only from a holder that stopped
(`AdoptsOnlyFromAStoppedHolder`), and
`prefix` → `prefix-stranded` shows the old sort stranding it; `tests/test_ticket_protocol_model.py`
fails when a sentence the model quotes for adoption leaves its file.

## Source
- Session: an audit of the skills' state machines and the fixes to its findings (2026-11-07).
- Related: amends 20261019-every-way-a-landing-cannot-merge-relaunches-or-escalates and
  20261019-the-comment-the-venue-created-first-decides-each-ticket-fact; see also
  20261019-a-model-checks-the-ticket-protocol-against-the-prose-it-quotes
