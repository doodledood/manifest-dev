---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/eli5
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# eli5

Explains a topic as a dead-simple picture explainer page: big pictures, few words.

## How a user reaches it

- `/eli5 <topic>`.
- Phrases its description matches: "explain like I'm five", "a dead-simple picture".
- No other skill calls it.

## Scenarios

### explain
Run: `scripts/drive-skill.sh eli5 verification/prompts/eli5-explain.md --tools`
Proves: one HTML page, styled through design, whose path or Artifact the reply names. Nothing the topic needs is hidden behind interaction.
Check: read

## Gotchas

- Needs a host that can write files or Artifacts.
- Without design available it styles by hand; contrast should still read.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
