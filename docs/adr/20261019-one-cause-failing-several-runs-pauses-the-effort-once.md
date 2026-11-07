# ADR: One cause failing several runs pauses the effort once

## Status
Accepted — amended by 20261102-a-landing-fixes-what-it-meets: a base check a code change can fix gets one repair Ticket, which alone may launch and land during the pause; amended by 20261107-automation-writes-beside-what-a-person-wrote-never-over-it: an orchestrator's pause and the status-page link are records kept apart from a person's `Paused:` line, not lines written after a re-read

## Area
Ticketing

## Decided by
The user

## Context
Under 20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep, a `Paused:` line on
an effort's front item stops new launches and landing turns, and only a person writes it. When the
base branch goes red, or CI or the venue is down, every live run fails on that one cause. Each run
then escalates or tries to repair its own Ticket, and the person gets one item per Ticket for one
problem, or runs spend quota repairing what is not theirs.

## Decision
- When Tickets in an effort fail on one cause outside them, whether a live run records it or a
  landing finds it, `orchestrate` pauses the effort instead — on one Ticket when a required check
  fails the same way on the base, which already proves the cause lies outside it, and on two or
  more for another cause: it writes a `Paused:` line
  naming the cause and its own ID, and raises one item naming the cause on the list of what waits
  on the person. A run whose required check fails the same way on the base names that cause and
  finishes rather than repairing or escalating, so the cause reaches `orchestrate` while the runs
  are still its to pause.
- A `Paused:` line naming an orchestrator keeps the check-ins going, and once its cause is fixed
  any orchestrator removes it, since the session that wrote it may have ended. None removes a line
  a person wrote.
  A status-page write re-reads the front item just before its edit and changes nothing else, so a
  person's `Paused:` line is never erased.

## Alternatives Considered
- **Escalate each Ticket**: the standing behavior; one cause becomes many items.
- **Retry until the cause clears**: spends quota on a failure no run can fix, with no one told.
- **Only the writing orchestrator lifts its pause**: a pause would outlive a session that ended,
  and the effort would stay stopped until a person found the line.

## Consequences

### Positive
- One cause reaches the person once, and the fleet stops spending on it.

### Negative
- `orchestrate` now writes a line a person used to own alone, and judges what counts as one cause.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` — `test_the_pause_line_is_never_erased_and_one_cause_pauses_once`
fails if the common-cause pause or the rule that any orchestrator lifts an orchestrator's pause
and only a person removes a person's is dropped, and
`test_no_automation_write_replaces_a_persons_pause` fails if a write of automation's moves back
onto the text a person edits (20261107-automation-writes-beside-what-a-person-wrote-never-over-it);
deciding that failures share a cause stays judgment.

## Source
- Session: figure-out and define reviewing manifest-dev's verification practice (2026-10-19).
- Related: amends 20261018-an-orchestrating-skill-runs-the-queue-and-replaces-the-sweep; see also
  20261019-each-item-waiting-on-the-person-carries-its-recommendation-risk-and-evidence
