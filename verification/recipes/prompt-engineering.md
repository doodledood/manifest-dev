---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/prompt-engineering
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# prompt-engineering

Guides creating, updating, reviewing or discussing an LLM prompt, skill or agent, leading with where each line came from.

## How a user reaches it

- `/prompt-engineering <request>`.
- Phrases its description matches: "improve this prompt", "this skill needs work".
- define and figure-out before prompt-shaped work; review-prompt first; manifest-to-goal.

## Scenarios

### diagnose
Run: `scripts/drive-skill.sh prompt-engineering verification/prompts/prompt-engineering-diagnose.md --tools`
Proves: an answer that traces lines to their source and proposes specific edits. It cites lines from the prompt, not general advice.
Check: read
Workload: varies

## Gotchas

- It is guidance; it edits only when asked to.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it. review-prompt applies its principles as a gate.
