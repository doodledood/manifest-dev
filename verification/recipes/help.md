---
kind: skill
covers: claude-plugins/manifest-dev/skills/help
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# help

Explains manifest-dev to a person in ASD-STE100: what it is for, the workflow, the autonomy ladder, every term a user meets with why it exists, how the parts relate, and good practice.

## How a user reaches it

- `/manifest-dev:help [question]` in Claude Code, whose own `/help` takes the bare name; `$help` in Codex; `/skill:help` in Pi.
- Phrases its description matches: "what is a recipe", "why is this verification folder here", "how do the manifest-dev skills fit together".
- No workflow skill calls it; it is an optional extra.

## Scenarios

### term
Run: `scripts/drive-skill.sh help verification/prompts/help-term.md`
Proves: the answer says what a recipe and the verification harness are and why each exists, and that ask-first marks a run with a cost a person accepts, from the glossary, in short plain sentences.
Check: read
Workload: varies

### ladder
Run: `scripts/drive-skill.sh help verification/prompts/help-ladder.md`
Proves: the answer names the five levels, says each works without the ones above it and without the team, and gives what each adds and costs and where to start.
Check: read
Workload: varies

### overview
Run: `scripts/drive-skill.sh help verification/prompts/help-overview.md`
Proves: with no question, the answer gives what manifest-dev is for, the workflow and the autonomy ladder, and stops there.
Check: read
Workload: varies

## Gotchas

- A bare `/help` in an interactive Claude Code session opens the host's own help, not this skill.
- `tests/test_help_skill.py` holds the term set and each entry's fingerprint against `CONTEXT.md`, the skill list against the plugin, and STE's counted limits. Whether an answer is right stays a read.
- An answer that goes beyond the skill's text is a failure, even when it is true: the skill says so when it does not know.
