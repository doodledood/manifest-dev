---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/walk-pr
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# walk-pr

Walks the user through a pull request or large diff one sub-change and one review topic at a time, and posts the comments they approve as one review.

## How a user reaches it

- `/walk-pr [pr-url | range] [--canvas]`; `--canvas` runs the walk in a live HTML page, styled through design.
- Phrases its description matches: "walk me through this PR", "review this together".
- No other skill calls it.

## Scenarios

### walk-a-range
Run: `scripts/drive-skill.sh walk-pr verification/prompts/walk-pr-walk-a-range.md --tools`
Proves: the first turn covers one sub-change and asks about one topic. Nothing posts until the user confirms each comment.
Check: read
Workload: varies

## Gotchas

- Posting needs GitHub access to a throwaway pull request; the range scenario needs none.
- It is interactive by design; a headless drive shows only the first turn.
- Posted comments are public.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
