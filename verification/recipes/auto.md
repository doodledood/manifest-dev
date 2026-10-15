---
kind: skill
covers: claude-plugins/manifest-dev/skills/auto
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# auto

Chains figure-out, define and do with no approval stops: understanding, then a Manifest, then execution, all in one run.

## How a user reaches it

- `/auto <task>`; the Pi template `dist/pi/prompts/auto.md`.
- Phrases its description matches: "autonomous", "end-to-end", "from idea to done".
- `run-ticket`, with the Ticket as the task.

## Scenarios

### chain
Run: `scripts/drive-skill.sh auto verification/prompts/auto-chain.md --max-turns 150`
Proves: the transcript shows define reporting a Manifest path and do starting on that same path in the same run; the run ends in `/done` or `/escalate`, not at a handoff waiting for the user.
Check: read
Workload: varies

## Gotchas

- Stopping after figure-out's read or define's handoff is the defect it exists to avoid.
- Everything do may do, auto may do. Scratch repository only.
- `tests/test_dist_skill_references.py` checks the chain and that do alone owns the continuation; no behavior case measures it.
