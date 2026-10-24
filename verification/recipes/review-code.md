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
Workload: varies

### project-rule
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-project-rule.md`
Proves: with a context file naming a convention a dimension would flag (a shared module-level instance) and a change following it, there is no finding on the convention; the report names the rule applied.
Check: read
Workload: varies

### project-rule-critical
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-project-rule-critical.md`
Proves: with a rule whose result is a Critical finding (logging a login body with its password), the Critical finding is still reported, naming the rule that produced it.
Check: read
Workload: varies

### test-quality-pinned
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-test-quality-pinned.md`
Proves: test-quality reports the test that asserts the order of `Invoice`'s private helper calls as pinned to the implementation — an edit to the internals that keeps the total would fail it — and names the behavior to assert instead, the total.
Check: read
Workload: varies

### defect-class-extra-guard
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-defect-class-extra-guard.md`
Proves: defect-class passes the `not loan["returned"]` condition as the repair of the mechanism, and reports the added `None` checks as lines the mechanism does not need.
Check: read
Workload: varies

### follow-up
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-follow-up.md --scaffold verification/fixtures/review-continuity`
Proves: the report closes F1 because private notes no longer leak, retains F2 because the last line is still missing from the total, and reports the repair's conversion of identifier strings to integers. It does not add a finding about the unchanged sorting of line SKUs. The report names the prior reviewed state and current scope; broad contextual reading is allowed.
Check: read
Workload: varies

### fresh
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-fresh.md --scaffold verification/fixtures/review-continuity`
Proves: this new explicit full review reports the input-order violation from sorting SKUs, as well as the identifier and total defects. Historical review files do not silently narrow the requested scope. The fixture is the same as follow-up, so the requested review scope explains the different eligible findings.
Check: read
Workload: varies

## Gotchas

- Each prompt builds its own scratch repository state: a commit on a branch ahead of its default branch.
- One dimension per call; asking for two gets one.
- `defect-class` needs a change that fixes a defect, or it reports none found.
- No comparison base resolves to BLOCKED.
- `tests/test_review_scope.py` exercises the scope commands; `tests/test_drive_scripts.py` checks convergence fixtures. The follow-up and fresh drives are unmeasured; fixture checks do not measure review behavior.
- Not yet driven: the description phrases, define's coding gates, review-pr's fleet.
