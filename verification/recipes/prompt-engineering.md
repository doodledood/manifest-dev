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
- define and figure-out before prompt-shaped work; review-prompt first.

## Scenarios

### diagnose
Run: `scripts/drive-skill.sh prompt-engineering verification/prompts/prompt-engineering-diagnose.md --tools`
Proves: an answer that traces lines to their source and proposes specific edits. It cites lines from the prompt, not general advice.
Check: read

### diagnose-input
Run: `scripts/drive-skill.sh prompt-engineering verification/prompts/prompt-engineering-diagnose-input.md --tools`
Proves: an answer that traces the wrong plan to the filled-in record rather than to the prompt's wording: the record's `plan` field is stale and conflicts with its own billing events. Its fix is to what the run is fed, such as filling `plan` from one source of truth or dropping the stale field. An answer whose main fix is rewording the prompt, telling the model to check the billing events or prefer recent data, or adding a self-check fails.
Check: read

### update-current-state
Run: `scripts/drive-skill.sh prompt-engineering verification/prompts/prompt-engineering-update-current-state.md --tools`
Proves: the returned skill reads as current state. It carries the requested ten-entry cap with the "and N more" line. The "Previously…" note and the dated "Per the maintainer" note are gone, and every existing rule remains: grouping, skipping `internal`, linking each pull request, and one past-tense line per entry naming the user-visible effect, which appears once. The vague "Keep each group short where you can, if possible" hedge, which the cap settles, is gone.
Check: read

## Gotchas

- It is guidance; it edits only when asked to.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it. review-prompt applies its principles as a gate.
