---
kind: skill
covers: claude-plugins/manifest-dev/skills/next-ticket
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# next-ticket

Reads the Ticket store, picks the one Ticket whose delay would cost the project most, claims it, and presents it with why it leads. It does not run the Ticket.

## How a user reaches it

- `/next-ticket`.
- Phrases its description matches: "what's next", "what should I work on".
- No other skill calls it; `run-ticket` and `sweep-tickets` deliberately do not.
- It ranks open Tickets across efforts.

## Scenarios

### select
Run: `scripts/drive-skill.sh next-ticket verification/prompts/next-ticket-select.md`
Proves: one Ticket presented with a reason; the summary's files show only that Ticket gaining a claim line. Only the chosen Ticket changed, and only by its claim.
Check: read

## Gotchas

- The prompt first has ticket-up file two small Tickets in a file store, then runs `/manifest-dev:next-ticket` in the same session.
- It claims at once; a GitHub venue assigns the Issue for real.
- "It didn't start the work" is intended: execution belongs to `run-ticket` or the person holding the claim.
- `tests/test_ticket_automation_prompts.py` covers the Ticket skills' boundaries; nothing exercises its ranking.
