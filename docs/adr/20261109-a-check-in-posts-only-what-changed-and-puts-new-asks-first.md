# ADR: A check-in posts only what changed and puts new asks first

## Status
Accepted

## Area
Ticketing

## Decided by
An agent in an unattended run, with no review — under the owner's instruction to apply the fixes
an audit of the shipped skills against the project's principles skills found

## Context
20261019-each-item-waiting-on-the-person-carries-its-recommendation-risk-and-evidence had a
check-in report in the conversation "only what changed since the last one and the items still
waiting". The second half reposted every unchanged item at each check-in, every ten minutes, which
is the repetition that record rejected for the whole list, since it buries the new items. The
project's product principles budget what a skill writes by the person's attention: no repeat of an
unchanged item, and the ask set apart. The decision sits inside the North Star's Purpose: the
person keeps the choices they retain without supervising every step.

## Decision
- In the conversation, a check-in puts first what newly waits on the person, then what else
  changed since the last check-in. An item still waiting unchanged stays on the status page, which
  shows the whole list at every check-in, and is not posted again.
- Each item keeps its own bullet with what the person is asked, the recommended answer, its risk
  and its evidence.

## Alternatives Considered
- **Keep reposting the items still waiting**: the standing text; the new items drown among the old.
- **Post nothing until something needs the person**: hides landings and failures the person may
  want to see as they happen.

## Consequences

### Positive
- What newly needs the person is the first thing each check-in says.

### Negative
- A person who reads only the conversation sees an older waiting item only where it was first
  posted, or on the page.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` —
`test_each_item_waiting_on_the_person_can_be_decided_from_the_list` pins the new ordering and the
rule against reposting; whether a report repeats an item stays judgment.

## Source
- Session: an unattended run applying the principles audit of manifest-dev's skills (2026-11-09).
- Related: narrows 20261019-each-item-waiting-on-the-person-carries-its-recommendation-risk-and-evidence
