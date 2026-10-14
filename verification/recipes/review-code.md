---
kind: skill
covers: claude-plugins/manifest-dev/skills/review-code
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# review-code

Reviews a change along exactly one quality dimension and returns PASS, FAIL or BLOCKED with graded findings.

## How a user reaches it

- `/review-code <dimension> [scope]`. The dimension is one of: change-intent, code-bugs, code-design, code-simplicity, code-maintainability, code-testability, test-quality, type-safety, contracts, operational-readiness, docs, prose-value, defect-class, context-file-adherence. The scope is a supplied range, or the diff against the remote default branch.
- Phrases its description matches: "review this diff for bugs", "audit the change for type safety".
- define's coding gates (run under `/do`); review-pr's reviewer fleet.

## Scenarios

### review
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-review.md`
Proves: a report naming the dimension, findings with severity and evidence, and one verdict. Every finding points at a line inside the change.
Check: read

### project-rule
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-project-rule.md`
Proves: with a context file naming a convention a dimension would flag (a shared module-level instance) and a change following it, there is no finding on the convention; the report names the rule applied.
Check: read

### project-rule-critical
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-project-rule-critical.md`
Proves: with a rule whose result is a Critical finding (logging a login body with its password), the Critical finding is still reported, naming the rule that produced it.
Check: read

## Gotchas

- Each prompt builds its own scratch repository state: a commit on a branch ahead of its default branch.
- One dimension per call; asking for two gets one.
- `defect-class` needs a change that fixes a defect, or it reports none found.
- No comparison base resolves to BLOCKED.
- `tests/test_review_scope.py` pins how scope is resolved. No behavior case measures the review.
- Not yet driven: the description phrases, define's coding gates, review-pr's fleet.
