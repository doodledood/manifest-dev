---
kind: skill
covers: claude-plugins/manifest-dev/skills/run-ticket
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# run-ticket

Takes one exact Ticket, recovers any earlier attempt, runs it through auto and its required landing, and writes DONE or ESCALATED evidence back on that same Ticket.

## How a user reaches it

- `/run-ticket <ticket reference>`.
- Phrases its description matches: "run this ticket end to end", a hosted trigger or agent runner supplying an issue.
- `sweep-tickets` for the one Ticket it selects.
- It reconciles an earlier attempt's marker, branch and pull request; it uses check-pr before merge; separate findings go to ticket-up as follow-ups.

## Scenarios

### run
Run: `scripts/drive-skill.sh run-ticket verification/prompts/run-ticket-run.md --max-turns 120`
Proves: the Ticket gains `<!-- manifest-dev-run-ticket-attempt -->` and, at the end, a DONE section or `<!-- manifest-dev-run-ticket-escalated -->`. The landing the Ticket asks for is observed, not assumed.
Check: read

## Gotchas

- The prompt first has ticket-up file one small Ticket with a checkable end, then runs `/manifest-dev:run-ticket` on it in the same session.
- It does not pick from a backlog; a missing or ambiguous reference stops before any work.
- Running it by hand does not grant Auto.
- Everything auto and do may do, it may do — and a GitHub venue writes to real Issues.
- `tests/test_ticket_automation_prompts.py` checks markers, recovery and follow-up routing.
