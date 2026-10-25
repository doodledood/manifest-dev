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
Workload: varies

### fresh-review
Run: `scripts/drive-skill.sh manifest-to-goal verification/prompts/manifest-to-goal-fresh-review.md --tools`
Proves: on an 18-gate Manifest with one amendment, the goal block is at most 4,000 characters and keeps every pass condition. That includes the 64 MB peak-memory bound stated only in a gate's why, the 366-day range, the ten-per-hour rate limit, the exact JSON keys and their order, and the stop at a ready pull request with nothing merged or deployed. The removed CSV export appears nowhere, and neither does the Initial Approach's "then add CSV". The profiling, test-first and 40-line steps are not stated as requirements. The goal names no gate ID or Manifest. The goal came back from a fresh review, or the note under the fence says the review was self-graded.
Check: read
Workload: varies

## Gotchas

- A goal that refers back to the Manifest file is the defect it exists to avoid.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
