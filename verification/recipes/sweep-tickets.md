---
kind: skill
covers: claude-plugins/manifest-dev/skills/sweep-tickets
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# sweep-tickets

From a scheduled trigger, recovers one interrupted automation-owned Auto Ticket or starts one ready Auto Ticket through run-ticket, then stops.

## How a user reaches it

- `/sweep-tickets`, normally from a scheduler.
- Phrases its description matches: "scheduled agent trigger", "resume one interrupted".
- The automation setup in ticket-up's `references/AUTOMATED_EXECUTION.md`.
- With nothing to recover, it starts the ready Auto Ticket whose delay costs most.

## Scenarios

### sweep
Run: `scripts/drive-skill.sh sweep-tickets verification/prompts/sweep-tickets-sweep.md --max-turns 120`
Proves: exactly one `run-ticket` invocation in the transcript, then the run stops. No second Ticket was touched.
Check: read

## Gotchas

- The prompt first has ticket-up file one Ticket granted Auto in a file store, then runs `/manifest-dev:sweep-tickets`.
- It is not a batch runner: one Ticket, then stop.
- Only Tickets granted Auto are eligible.
- `tests/test_ticket_automation_prompts.py` checks the sweep and its hand-off to run-ticket.
