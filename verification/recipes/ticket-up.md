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
- figure-out when questions stop depending on each other; `run-ticket` for follow-ups.
- From a Manifest it splits by Deliverable only when asked for delegation; follow-ups from another Ticket are grouped, each with its own Auto decision.
- Venues: a file store, GitHub Issues, or another tracker named in the store config.

## Scenarios

### direct-request
Run: `scripts/drive-skill.sh ticket-up verification/prompts/ticket-up-direct-request.md`
Proves: the summary's files include `tickets/store-config.md` and one `tickets/<effort>/NN-<slug>.md` with the convention's sections. Each Ticket stands alone: a reader with no Manifest knows what to do and how it is checked.
Check: read
Workload: varies

## Gotchas

- It reads `tickets/store-config.md` first; without a store it asks where Tickets live. The prompt asks for a file store so the drive creates `tickets/store-config.md` itself.
- A GitHub venue writes real Issues. Use a throwaway repository.
- File-store claims do not cross clones or branches.
- `tests/test_ticket_automation_prompts.py` checks its authoring boundary, Auto grants and venue mapping.
