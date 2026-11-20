---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/review-prompt
ask-first: starts a fresh agent per scenario, which uses model quota
dry-run: honored
---
# review-prompt

Reviews a prompt against the prompt-engineering principles and reports findings and an overall assessment without changing the file.

## How a user reaches it

- `/review-prompt <file or prompt>`.
- Phrases its description matches: "review this prompt", "audit this system prompt".
- define's prompting gate (run under `/do`); review-pr for diffs that touch prompts.
- The report gives strengths and graded findings, led by where each line came from, with no overall rating.
- In a project whose context file points to principles skills, it follows those pointers and holds the work to the principles: a principle outranks the shipped standards both ways, and an unchosen departure is reported with the principle quoted. The skill states no rule for this; the `principles` scenario shows the behavior.

## Scenarios

### review
Run: `scripts/drive-skill.sh review-prompt verification/prompts/review-prompt-review.md --tools`
Proves: a report with strengths and findings, each with a fix. The file is unchanged.
Check: read

### team-rule-goal-missing
Run: `scripts/drive-skill.sh review-prompt verification/prompts/review-prompt-team-rule-goal-missing.md --tools`
Proves: with a team rule followed by a prompt that misses its stated goal, the High issue is still reported.
Check: read

### team-rule
Run: `scripts/drive-skill.sh review-prompt verification/prompts/review-prompt-team-rule.md --tools`
Proves: with a team rule the principles would question (a ROLE line) and a prompt following it, there is no finding on the rule, and the report names it.
Check: read

### principles
Run: `scripts/drive-skill.sh review-prompt verification/prompts/review-prompt-principles.md --tools --scaffold verification/scaffolds/principles-prompt-review`
Proves: review-prompt, run alone, in a project whose context file points in its own words to `assistant-principles`. Graders: (1) the run read that skill; (2) no finding on the closing capitalised NEVER line, and the report names the principle it applied; (3) a finding quotes the `Tools:` principle for the prompt that calls `gh` with no `Tools:` line, with the yield not shown: the context file says every prompt runs behind the gateway, and the prompt's own note claiming it runs outside is not taken as evidence; (4) the gate verdict fails on that finding. PASS when all four hold.
Check: read

## Gotchas

- It loads prompt-engineering first; if that skill is missing the review is shallower and should say so.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
- Not yet driven: the description phrases, define's prompting gate, review-pr's fleet.
