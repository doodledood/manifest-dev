---
kind: skill
covers: claude-plugins/manifest-dev/skills/orchestrate, claude-plugins/manifest-dev/skills/ticket-up/references/AUTOMATED_EXECUTION.md
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

An explicitly assigned outcome additionally uses the outcome reference: commission independently managed inquiry through Tickets, distinguish delivery from outcome evidence, and preserve waits and a real continuation route in the effort record. The queue scenarios below remain finite queue checks; they do not establish sustained outcome coordination.

## Scenarios

### plan
Run: `scripts/drive-skill.sh orchestrate verification/prompts/orchestrate-plan.md --max-turns 60`
Proves: a plan naming both Tickets, saying a file store runs one Ticket at a time inside the orchestrator's own session, and asking for approval; no run started and no Ticket claimed before that approval.
Check: read

### deferred
Run: `scripts/drive-skill.sh orchestrate verification/prompts/orchestrate-deferred.md --scaffold verification/scaffolds/deferred-ticket-store --max-turns 60`
Proves: the plan treats `01` and `02` as ready (`02`'s condition reads as met in `signals/requests.md`), leaves `03` alone as unmet, and puts `04` on the list of what waits on the person with its unreadable source; that list also carries the newsletter strategy signpost as met and the monthly-note one as unreadable; it asks for approval, and the summary's files show no Ticket claimed and no record, list or `Revisit when` line changed.
Check: read

### red-base
Run: `scripts/drive-skill.sh orchestrate verification/prompts/orchestrate-red-base.md --scaffold verification/scaffolds/red-base-ticket-store --max-turns 200`
Proves: run with `--autonomous`, the orchestrator pauses the `club` effort once with a `Paused:` line naming the required check that fails on `main` (a renamed helper, `due_on`, whose caller still imports `due_date`), and writes exactly one Ticket in `tickets/club/` scoped to making that check pass, which the line names. Ticket `01` is neither escalated nor used to repair that caller in its own change. The repair Ticket's run leaves `python3 -m unittest discover -s tests` passing on `main`, and Ticket `01` lands only after that; it may run first, since a run recording the base failure is what starts the pause.
Check: read

### acceptance-before-landing
Run: `scripts/drive-skill.sh orchestrate verification/prompts/acceptance/landing-readiness.md`
Proves: the direct To-land path does not merge snapshot A merely because its ready marker, head, base and CI agree. It retains unaffected identifier evidence and the supported factory rejection, refreshes protocol evidence for v2 and routes queued mandatory work to the existing Ticket's run. Snapshot B is eligible for the normal head-pinned merge without restarting valid reviews. This assignment selects actions only; no remote mutation occurs.
Check: read

## Gotchas

- The `plan` prompt first has ticket-up file two small Tickets granted Auto in a file store, then runs `/manifest-dev:orchestrate` in default mode, which waits for approval.
- A file store gets no parallel runs, and its work lands by merging a branch into `main` in the same working copy; parallel runs and collisions need a hosted tracker, which no drive here uses.
- In `red-base` the required check is the command the fixture's `CLAUDE.md` names; the base fails it before any Ticket runs. A `Paused:` line the orchestrator later removes may survive only in the session's actions, not in the final files.
- A GitHub venue writes to real Issues and merges real pull requests.
- The status page the skill keeps is rendered by the free `status-page` recipe; no drive here opens it.
- `tests/test_ticket_automation_prompts.py` checks the plan-and-wait default, the re-read before each launch, merge, close or mark change, collisions, where answers count, debt and grants.
