# ADR: Each item waiting on the person carries its recommendation, risk and evidence

## Status
Accepted — narrowed by 20261109-a-check-in-posts-only-what-changed-and-puts-new-asks-first: the conversation puts what newly waits on the person first and no longer reposts unchanged items, which stay on the page

## Area
Ticketing

## Decided by
The user

## Context
20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep gave `orchestrate` one list
of what waits on the person, ordered by what waiting costs. Each item said what was asked and
linked the pull request or Ticket. With several runs at once, the person then opened each link to
decide, and a count such as "3 held pull requests" stood in for items.

## Decision
- Each item on the list has its own bullet, never a count standing in for items, with what the
  person is asked, the answer `orchestrate` recommends, the risk of taking it, and the evidence it
  rests on: the gates that passed and what they did not check, the failing check, the blocker.
- The status page shows the whole list, with the same fields in the "Needs you" panel and each
  Ticket's detail. In the conversation, a check-in reports only what changed since the last one
  and the items still waiting.

## Alternatives Considered
- **Links only**: shorter, but every decision costs the person a trip into the pull request.
- **The whole list at every check-in in the conversation too**: repeats unchanged items each ten
  minutes, so the new ones are harder to see.

## Consequences

### Positive
- The person can decide most items from the list alone.

### Negative
- Each item costs `orchestrate` a recommendation and a risk it must work out, and the page's data
  block grows.

## Enforced by
partly — `tests/test_orchestrate_status_page.py` fails if the page's data check stops accepting
an item's recommendation, risk and evidence or accepts them as anything but text, and
`tests/test_ticket_automation_prompts.py` — `test_each_item_waiting_on_the_person_can_be_decided_from_the_list`
fails if `orchestrate` or the page reference drops an item's fields or lets a count stand in for
items, or if a check-in reposts unchanged items (20261109-a-check-in-posts-only-what-changed-and-puts-new-asks-first); whether a recommendation is sound stays judgment.

## Source
- Session: figure-out and define reviewing manifest-dev's verification practice (2026-10-19).
- Related: amends 20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep
