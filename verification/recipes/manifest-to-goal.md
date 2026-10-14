---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/manifest-to-goal
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# manifest-to-goal

Turns a Manifest into one standalone goal of at most 4,000 characters, for pasting into a goal field with no Manifest file behind it.

## How a user reaches it

- `/manifest-to-goal <manifest path or text>`.
- Phrases its description matches: "turn this into a goal", "paste into the goal field".
- No other skill calls it.

## Scenarios

### convert
Run: `scripts/drive-skill.sh manifest-to-goal verification/prompts/manifest-to-goal-convert.md --tools`
Proves: one goal block in the reply. At most 4,000 characters; every gate's threshold survives; nothing new is invented.
Check: read

## Gotchas

- A goal that refers back to the Manifest file is the defect it exists to avoid.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
