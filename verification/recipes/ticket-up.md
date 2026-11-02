---
kind: skill
covers: claude-plugins/manifest-dev/skills/ticket-up
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# ticket-up

Writes self-sufficient Tickets into the project's Ticket store — from a Manifest (one Shaped Ticket by default), a direct request, an open question, or follow-ups from another Ticket.

## How a user reaches it

- `/ticket-up <manifest path | request | question>`.
- Phrases its description matches: "create tickets", "ticket up the plan", "hand this to a teammate".
- figure-out when questions stop depending on each other; `run-ticket` for follow-ups; `orchestrate` for the debt Tickets it writes and the Auto grants it makes.
- From a Manifest it splits by Deliverable only when asked for delegation; follow-ups from another Ticket are grouped, and carry Auto only when a person, or `orchestrate --autonomous` under the grant criterion, grants it at that step, whatever the source carries; the run that found the work never does.
- Venues: a file store, GitHub Issues, or another tracker named in the store config.

Assignments preserve useful intent, evidence, delegated decisions and retained acceptance. The grant criterion requires full completion authority; setup may reuse the store resolver without creating a Ticket.

## Scenarios

### direct-request
Run: `scripts/drive-skill.sh ticket-up verification/prompts/ticket-up-direct-request.md`
Proves: the summary's files include `tickets/store-config.md` and one `tickets/<effort>/NN-<slug>.md` with the convention's sections. Each Ticket stands alone: a reader with no Manifest knows what to do and how it is checked.
Check: read

### follow-up
Run: `scripts/drive-skill.sh ticket-up verification/prompts/ticket-up-follow-up.md`
Proves: a follow-up an unattended run found, from a source that carries Auto, is written as a Ticket with no Auto, because neither a person nor `orchestrate --autonomous` granted it at this step. The Ticket names its source.
Check: read

### deferred
Run: `scripts/drive-skill.sh ticket-up verification/prompts/ticket-up-deferred.md`
Proves: the Ticket carries a `Revisit when:` line naming the weekly sign-up count passing 50 and the analytics dashboard it is read on, among its opening lines after `Depends on:`, and no `Depends on:` entry for it.
Check: read

## Gotchas

- It reads `tickets/store-config.md` first; without a store it asks where Tickets live. The prompt asks for a file store so the drive creates `tickets/store-config.md` itself.
- A GitHub venue writes real Issues. Use a throwaway repository.
- File-store claims do not cross clones or branches.
- `tests/test_ticket_automation_prompts.py` checks its authoring boundary, Auto grants and venue mapping.
