---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/teach-me
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# teach-me

Teaches the user a body of work — this session's changes, a pull request, a decision record, a topic — stage by stage, confirming understanding before moving on.

## How a user reaches it

- `/teach-me [topic]`; with no argument it teaches the current session's changes.
- Phrases its description matches: "teach me what we did", "explain this ADR".
- No other skill calls it.

## Scenarios

### teach
Run: `scripts/drive-skill.sh teach-me verification/prompts/teach-me-teach.md --tools`
Proves: the first turn explains the problem the record solved and ends with a check question. It does not move on before the check is answered.
Check: read
Workload: varies

## Gotchas

- A decision record is the easiest topic.
- Interactive by design; a headless drive shows only the first stage.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
