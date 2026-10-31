---
kind: skill
covers: plugin/skills/summarize
ask-first: starts an agent session per scenario, which uses model quota
---
# Summarize notes

A coding agent with the Notes plugin installed summarizes a set of notes into one short brief,
citing each note it used.

## How a user reaches it

- The `/summarize <query or titles>` slash command.
- Asking the agent to "sum up my notes on …" or "brief me on the plan", which matches the skill's
  description.
- The `weekly-review` skill, which calls it for the past week's notes.

## Scenarios

### direct
Run: `scripts/agent-session --plugin plugin --prompt '/summarize "Quarterly plan"'`
Proves: the reply is a brief citing `Quarterly plan` and no other note.
Check: read

### empty
Run: `scripts/agent-session --plugin plugin --prompt '/summarize volcano'`
Proves: the reply says no note matched and offers no summary.
Check: read

## Gotchas

- The agent may answer from memory of an earlier run. Each scenario starts a fresh session.
- A reply that describes running `notes search` is not evidence that it ran. Read the transcript
  the session leaves, not its own account.
- Behavior cases `evals/summarize-cites-sources/` measure it against a no-plugin baseline.
