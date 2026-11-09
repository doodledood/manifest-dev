# ADR: A pause only a person can clear ends the check-ins

## Status
Accepted

## Area
Ticketing

## Decided by
An agent in an unattended run, with no review — under the owner's instruction to apply the fixes
an audit of the shipped skills against the project's principles skills found

## Context
20261019-one-cause-failing-several-runs-pauses-the-effort-once ruled that an orchestrator's pause
"keeps the check-ins going" until its cause is fixed and any orchestrator lifts it. That holds
while something other than a person can fix the cause: an outage ends on its own, and a repair
Ticket the orchestrator may launch and land fixes a red base check. It did not weigh a pause whose
cause waits on the person: a repair Ticket awaiting their grant, their plan approval or their
review, or escalated. There the check-ins went on every ten minutes without end, and an
autonomous orchestrator's stop condition never held, since ready Tickets stayed in the held
effort. The project's architecture principle asks every wait or loop to have a stated exit, and
its product principles ask that a run started unattended not wait. The decision sits inside the
North Star's Purpose: delegated work proceeds without the person supervising every step.

## Decision
- An orchestrator's pause keeps the check-ins going only while its cause can clear without the
  person: an outage that may end on its own, or a code-fixable cause whose repair Ticket this
  orchestrator can still launch, run or land.
- Once every pause still standing waits on the person, and nothing else keeps the check-ins
  going, the orchestrator stops as its mode says: the default mode proposes the next plan and
  stops without an answer; `--autonomous` reports, naming each pause left standing and what it
  waits on. The pause stays, so the effort stays held.
- Any later orchestrator checks a standing pause's cause when it starts and lifts it once fixed,
  as before. The ten-minute interval and every other pause rule are unchanged.
- An outage keeps its one item on the list of what waits on the person, now worded as a cause
  that gets no repair Ticket rather than one that waits for the person.

## Alternatives Considered
- **Keep checking in until the pause lifts**: the standing rule; an unattended orchestrator never
  ends while its next step needs a person, and a scheduler that starts orchestrators stacks them.
- **Stop after a number of check-ins or a length of time**: a count nobody can source, which
  stops too early on an outage and too late on a review the person has not seen.
- **Treat an outage as waiting on the person too**: stops runs that would resume on their own when
  the service returns, and puts restarting them on the person or their scheduler.

## Consequences

### Positive
- An orchestrator facing only the person's part of a pause ends and says what it waits on.
- An outage still clears and resumes work with nobody involved.

### Negative
- After the person answers, work resumes only when an orchestrator next runs: the default mode's
  conversation, the person, or their scheduler.

## Enforced by
partly — `verification/models/ticket-protocol/TicketProtocol.tla`, run by
`scripts/verify drive ticket-protocol-model`: `CheckInsEnd` and `LiftedOnceFixed` on the
`pause-person` configuration, with `prefix-checkins` restoring check-ins without end and expecting
TLC to report it; `tests/test_ticket_automation_prompts.py` —
`test_the_pause_line_is_never_erased_and_one_cause_pauses_once` and
`test_orchestrate_proposes_and_waits_by_default` pin the narrowed sentences. Judging whether a
cause can clear without the person stays judgment.

## Source
- Session: an unattended run applying the principles audit of manifest-dev's skills (2026-11-09).
- Related: narrows 20261019-one-cause-failing-several-runs-pauses-the-effort-once; see also
  20261102-a-landing-fixes-what-it-meets
