# ADR: Whoever reads the store names what it meets and records a person's merge

## Status
Accepted

## Area
Ticketing

## Decided by
An agent in an unattended run, with no review — under the owner's instruction to apply the fixes
an audit of the shipped skills against the project's principles skills found

## Context
The ticket convention's tidy pass ran "occasionally — after a few closes, or when the store feels
stale", so it ran only when someone remembered it. `orchestrate`'s outcome reference retired
superseded candidates "in the existing tidy pass". And a Ticket whose pull request a person merged
after a hand run stayed open until the person ran `run-ticket` on it again: an orchestrator's
check-in recorded such a merge only at a landing turn, which a person's claim keeps it from, and a
picker recorded nothing. The project's product principles say nothing the workflow relies on may
depend on a person remembering to run it, and that upkeep rides the runs that already touch a
surface. The decision sits inside the North Star's Purpose: a person returns without restoring
context, and the store tells the truth about what landed.

## Decision
- Whoever reads every open Ticket in a scope (a picker comparing candidates, an orchestrator
  sorting its scope, a session asked to tidy) names what it meets: a claim that looks abandoned,
  a Ticket events made moot, an escalation whose blocker looks resolved, a status that no longer
  tells the truth, a priority no longer pointing at the effort's goal. A picker or an orchestrator
  leaves fixing those to a person, in the report or list it already gives; a session asked to tidy
  makes them, within the rows that own them.
- An open Ticket whose pull request a person merged, not reopened after it and not escalated, is
  recorded and closed by whichever session meets that landing first, whoever holds the claim: an
  orchestrator's check-in, a picker's read of the store, a session tidying it, or a run that starts
  on it. The Close move gains the picker and the tidying session for this case only.
- Unchanged: a Ticket closes only once its landing is observed; a merge on a Ticket reopened after
  it is new work; an escalated Ticket is named, not cleared; venue items never written as Tickets
  are never touched; releasing a stale claim stays with a person or a session tidying for one.
- No scheduler, Ticket state or state record is added.

## Alternatives Considered
- **Keep the occasional pass**: nothing triggers it, so stale claims and merged Tickets stay as
  they are until someone remembers.
- **Only orchestrators record a person's merge**: a project that runs Tickets by hand and has no
  orchestrator still needs the person to rerun the skill.
- **Let the readers fix everything they name**: a picker or an unattended orchestrator would
  release a person's claim or close a Ticket on its own judgment that events made it moot, which
  the rows keep with a person.

## Consequences

### Positive
- A merged hand-run Ticket closes the next time any session reads the store.
- What needs tidying is named on surfaces people already read, so nobody has to remember a pass.

### Negative
- A picker now writes a close as well as a claim, so a read of the store can leave more state.
- A Ticket a person still holds closes once its pull request merges; one meant to carry more work
  needs reopening.

## Enforced by
partly — `verification/models/ticket-protocol/TicketProtocol.tla`, run by
`scripts/verify drive ticket-protocol-model`: `PersonMergeIsRecorded` on the `handoff`
configuration, with a picker, a run that starts on the Ticket and the orchestrator as closers, and
`prefix-handclose` restoring the claim-blocked close and expecting TLC to report it;
`tests/test_ticket_automation_prompts.py` — `test_whoever_reads_the_store_records_a_persons_merge`
pins the row, the Close move and the convention's text. What counts as moot or abandoned stays
judgment.

## Source
- Session: an unattended run applying the principles audit of manifest-dev's skills (2026-11-09).
- Related: see also 20261108-the-ticket-protocols-moves-have-one-owning-table,
  20260810-next-ticket-claims-the-ticket-it-picks,
  20261018-orchestrate-lands-and-run-ticket-stops-at-a-ready-pull-request
