---
kind: skill
covers: claude-plugins/manifest-dev/skills/orchestrate
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# orchestrate

Runs an effort's ready Tickets, or the whole store's, each through run-ticket in its own session; lands finished work one Ticket at a time, tickets up the debt runs leave, and keeps a status page and one list of what waits on the person. By default it proposes a plan and waits; `--autonomous` acts until no ready work is left.

## How a user reaches it

- `/orchestrate [<effort>]`, by hand; a scheduler the user already runs may start `/orchestrate --autonomous`.
- Phrases its description matches: "work through the queue", "run many Tickets at once".
- It reads the shared automation reference in ticket-up's `references/AUTOMATED_EXECUTION.md`, which owns the records on each Ticket and the one landing procedure.
- With no ready Ticket it says so and stops.
- It reads each deferred Ticket's `Revisit when` condition, and each strategy signpost in the North Star, at the source the line names.

## Scenarios

### plan
Run: `scripts/drive-skill.sh orchestrate verification/prompts/orchestrate-plan.md --max-turns 60`
Proves: a plan naming both Tickets, saying a file store runs one Ticket at a time inside the orchestrator's own session, and asking for approval; no run started and no Ticket claimed before that approval.
Check: read
Workload: varies

### deferred
Run: `scripts/drive-skill.sh orchestrate verification/prompts/orchestrate-deferred.md --scaffold verification/scaffolds/deferred-ticket-store --max-turns 60`
Proves: the plan treats `01` and `02` as ready (`02`'s condition reads as met in `signals/requests.md`), leaves `03` alone as unmet, and puts `04` on the list of what waits on the person with its unreadable source; that list also carries the newsletter strategy signpost as met and the monthly-note one as unreadable; it asks for approval, and the summary's files show no Ticket claimed and no record, list or `Revisit when` line changed.
Check: read
Workload: varies

## Gotchas

- The prompt first has ticket-up file two small Tickets granted Auto in a file store, then runs `/manifest-dev:orchestrate` in default mode, which waits for approval.
- A file store gets no parallel runs; parallel runs, collisions and landing turns need a hosted tracker, which no drive here uses.
- A GitHub venue writes to real Issues and merges real pull requests.
- `tests/test_ticket_automation_prompts.py` checks the plan-and-wait default, the re-read before each launch, merge, close or mark change, collisions, where answers count, debt and grants.
