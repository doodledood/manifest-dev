# ADR: Automation writes beside what a person wrote, never over it

## Status
Accepted

## Area
Ticketing

## Decided by
An agent in an unattended run, with no review — under the owner's delegation to fix the
findings of an audit of the skills' state machines

## Context
`orchestrate` wrote three things into text a person also edits. Its own `Paused:` line and the
`Status page:` line went into an effort's front item. A directive the person gave in the
orchestrator's conversation went into each Ticket's body. On GitHub the front item is the
tracking issue's body and a Ticket is an issue body, and an edit there replaces the whole body.
20261019-one-cause-failing-several-runs-pauses-the-effort-once relied on a re-read just before
the edit, "so a person's `Paused:` line is never erased". That premise does not hold. A re-read
narrows the race to the one write after it and cannot close it, as
`AUTOMATED_EXECUTION.md` already said of comments. A person's pause added in that window was
lost, and automation could then launch and land in an effort the person had paused. Two
orchestrators naming repair Tickets in one shared body could also overwrite each other.
20261102-a-landing-fixes-what-it-meets names the repair Ticket "in the line". The decision sits
inside the North Star's Purpose: the person keeps control of the choices they retain.

## Decision
- A person's text and automation's writes live apart. A person still pauses an effort with a
  `Paused:` line on its front item, and only a person removes it.
- A person's pause stops everything in the effort, the repair Ticket an orchestrator's pause names
  included. That Ticket runs and lands during a pause only while no person's `Paused:` line
  holds, and the status page marks it as the repair Ticket only then.
- An orchestrator's pause is its own record, one per cause. It names the cause, the orchestrator
  and the repair Ticket once one is named, and any orchestrator lifts it once that cause is fixed;
  the effort stays paused while any stands. The status-page link is a record too. On GitHub each
  is a marked comment on the tracking issue (`<!-- manifest-dev-orchestrate-pause: <cause> -->`,
  `<!-- manifest-dev-orchestrate-status-page -->`), under the first-created rule, which for the
  pause applies per cause, and automation never edits the tracking issue's body. In a file
  store, an orchestrator adds, edits or removes only lines an orchestrator wrote, one at a time.
- A repair Ticket's name is re-read after it is written into the pause. An orchestrator whose
  Ticket the pause does not name closes the one it created as a duplicate.
- A person's answer recorded from the orchestrator's conversation is an answer record. That is
  its own comment carrying `<!-- manifest-dev-person-answer -->`, never edited, and never written
  into the Ticket's body. Every answer record counts, so they are an exception to the
  first-created rule, read in order. A run reads each as the person's instruction within the
  authority it states.

## Alternatives Considered
- **One pause comment per effort, causes added to it**: two orchestrators adding causes at once
  edit one comment and the last writer wins, so a cause is lost and the effort unpauses while it
  persists; a second cause written as its own comment under one marker removed itself as not the
  first.
- **Let the repair Ticket run under any pause**: automation would launch and merge in an effort
  the person had stopped, the opposite of the person keeping the choices they retain.
- **Keep the re-read before the edit**: the venue has no compare-and-set on a body, so the window
  stays and a person's line can still be lost.
- **Make a person's pause a comment too**: anyone who can comment on a public issue could then
  pause an effort; a body edit needs the access the person already has.
- **One answer record per Ticket, edited in place**: two orchestrators recording answers at once
  would overwrite each other, the same race in a new place.

## Consequences

### Positive
- No write of automation's can remove a person's pause or a person's edit to a Ticket.
- A directive recorded by the automation identity reads as the person's instruction, rather than
  as untrusted body text.

### Negative
- An effort's standing settings are spread across the front item and its comments, so a reader
  of the body alone no longer sees an orchestrator's pause.
- Answer records accumulate on a Ticket. A later answer that replaces an earlier one has to say
  so.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` — `test_no_automation_write_replaces_a_persons_pause`
fails, on the source and the Codex copy, if a venue loses the pause or page-link record or the
GitHub body edit returns. `test_the_pause_line_is_never_erased_and_one_cause_pauses_once` fails if
the old re-read claim comes back. `test_a_persons_answer_is_recorded_beside_the_ticket_body` fails
if answers go back into a Ticket's body. `test_a_red_base_gets_one_repair_ticket` and
`tests/test_orchestrate_status_page.py` → `test_a_persons_pause_stops_the_repair_ticket_on_the_page`
fail if the repair Ticket's exception stops yielding to a person's pause.
`test_an_orchestrators_pause_is_one_record_per_cause` fails if a venue goes back to one pause
record per effort. Whether two failures
share a cause stays judgment.

## Source
- Session: an audit of the skills' state machines and the fixes to its findings (2026-11-07).
- Related: amends 20261019-one-cause-failing-several-runs-pauses-the-effort-once,
  20261102-a-landing-fixes-what-it-meets and
  20261019-the-comment-the-venue-created-first-decides-each-ticket-fact
