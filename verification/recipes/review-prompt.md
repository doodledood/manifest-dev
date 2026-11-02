---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/review-prompt
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# review-prompt

Reviews a prompt against the prompt-engineering principles and reports findings and an overall assessment without changing the file.

## How a user reaches it

- `/review-prompt <file or prompt>`.
- Phrases its description matches: "review this prompt", "audit this system prompt".
- define's prompting gate (run under `/do`); review-pr for diffs that touch prompts.
- The assessment is Excellent, Good with Minor Issues, or Needs Work, with findings led by where each line came from.

## Scenarios

### review
Run: `scripts/drive-skill.sh review-prompt verification/prompts/review-prompt-review.md --tools`
Proves: a report with an assessment and findings, each with a fix. The file is unchanged.
Check: read

### team-rule-goal-missing
Run: `scripts/drive-skill.sh review-prompt verification/prompts/review-prompt-team-rule-goal-missing.md --tools`
Proves: with a team rule followed by a prompt that misses its stated goal, the High issue is still reported.
Check: read

### team-rule
Run: `scripts/drive-skill.sh review-prompt verification/prompts/review-prompt-team-rule.md --tools`
Proves: with a team rule the principles would question (a ROLE line) and a prompt following it, there is no finding on the rule, and the report names it.
Check: read

## Gotchas

- It loads prompt-engineering first; if that skill is missing the review is shallower and should say so.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
- Not yet driven: the description phrases, define's prompting gate, review-pr's fleet.
