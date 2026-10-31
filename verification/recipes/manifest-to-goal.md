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

### fresh-review
Run: `scripts/drive-skill.sh manifest-to-goal verification/prompts/manifest-to-goal-fresh-review.md --tools`
Proves: on a 28-gate Manifest with one amendment that removes a gate, whose pass conditions come close to 4,000 characters, the goal block is at most 4,000 characters and keeps every pass condition. That includes the 64 MB peak-memory bound stated only in a gate's why, the 366-day range, the ten-per-hour rate limit, the exact JSON keys and their order, the 100,000-row page with its `Link` header, the p95 under 800 ms over 200 requests, the 404 without the `usage_export` flag, the `review-code` and `review-writing` checks by name, and the stop at a ready pull request with nothing merged or deployed. Nothing asks for the removed CSV export: no CSV gate, and no Initial Approach "then add CSV". A line excluding CSV, as the amendment says, is fine. The profiling, test-first and 40-line steps are not stated as requirements, and the Initial Approach's route and `usage_daily` table, where the goal mentions them, read as a plan rather than a requirement. The goal names no gate ID or Manifest. The goal came back from a fresh review, or the note under the fence says the review was self-graded.
Check: read

## Gotchas

- A goal that refers back to the Manifest file is the defect it exists to avoid.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
