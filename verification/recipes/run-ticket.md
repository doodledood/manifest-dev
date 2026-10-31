---
kind: skill
covers: claude-plugins/manifest-dev/skills/run-ticket
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# run-ticket

Takes one exact Ticket, recovers any earlier attempt from the Manifest and progress its attempt record carries, runs it to a ready pull request, and writes its completion record with its attempt record marked ready to land, or an escalation, back on that same Ticket. It lands only when told to.

## How a user reaches it

- `/run-ticket <ticket reference>`.
- Phrases its description matches: "run this ticket end to end", orchestrate, an agent runner or a person supplying an issue.
- `orchestrate`, which starts it in its own session for each Ticket it runs.
- It reconciles an earlier attempt's record, branch and pull request; it uses check-pr before marking the work ready; separate findings go to ticket-up as follow-ups.

A Question invokes inquiry only and returns its Read on the same Ticket. A repeated invocation at an unchanged drafted-answer wait does no new work. The implementation scenario below exercises the Shaped route, not the Question route.

## Scenarios

### run
Run: `scripts/drive-skill.sh run-ticket verification/prompts/run-ticket-run.md --max-turns 120`
Proves: the Ticket gains `<!-- manifest-dev-run-ticket-attempt -->` carrying the run's Manifest and progress, and, at the end, `<!-- manifest-dev-run-ticket-completion -->`, with the attempt record's run facts marked ready to land, or `<!-- manifest-dev-run-ticket-escalated -->`. Nothing is merged, since the prompt does not say to land.
Check: read

## Gotchas

- The prompt first has ticket-up file one small Ticket with a checkable end, then runs `/manifest-dev:run-ticket` on it in the same session.
- It does not pick from a backlog; a missing or ambiguous reference stops before any work.
- Running it by hand does not grant Auto.
- Everything auto and do may do, it may do — and a GitHub venue writes to real Issues.
- `tests/test_ticket_automation_prompts.py` checks the records, recovery, the ready-pull-request ending and follow-up routing.
