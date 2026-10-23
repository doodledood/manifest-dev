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
- No other skill calls it; `run-ticket` and `orchestrate` deliberately do not.
- It ranks open Tickets across efforts.
- It reads each deferred Ticket's `Revisit when` condition, and each strategy signpost in the North Star, at the source the line names.

Selection remains selection only. A met signpost supplies evidence, not an assignment or authority to change strategy.

## Scenarios

### select
Run: `scripts/drive-skill.sh next-ticket verification/prompts/next-ticket-select.md`
Proves: one Ticket presented with a reason; the summary's files show only that Ticket gaining a claim line. Only the chosen Ticket changed, and only by its claim.
Check: read
Workload: varies

### deferred
Run: `scripts/drive-skill.sh next-ticket verification/prompts/next-ticket-deferred.md --scaffold verification/scaffolds/deferred-ticket-store`
Proves: it claims `01` or `02` (`02`'s condition reads as met in `signals/requests.md`), never `03` (unmet in `signals/clubs.md`) or `04`; it names `04` with its source, the mailing provider's dashboard, as unreadable; it reports the newsletter strategy signpost as met (`signals/website-visits.md`) and the monthly-note one as unreadable, and says nothing of the loans one as met; the summary's files show only the chosen Ticket gaining a claim line, and no record, list or `Revisit when` line changed.
Check: read
Workload: varies

## Gotchas

- The `select` prompt first has ticket-up file two small Tickets in a file store, then runs `/manifest-dev:next-ticket` in the same session.
- It claims at once; a GitHub venue assigns the Issue for real.
- "It didn't start the work" is intended: execution belongs to `run-ticket` or the person holding the claim.
- `tests/test_ticket_automation_prompts.py` covers the Ticket skills' boundaries; nothing exercises its ranking.
