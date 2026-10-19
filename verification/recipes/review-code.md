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

### test-quality-unreached-guarantee
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-test-quality-unreached-guarantee.md`
Proves: test-quality reports, at Medium or above, that no kept test reaches the case that breaks the at-most-once guarantee of `send_invoice`: a crash after the send and before `mark_sent`, then the job reclaimed and sent again. It names a later change that would break it with both tests still passing (a fresh key on each attempt, say, since `FakeProvider` ignores the key), and names a kind of check that reaches it, such as a test that drives that sequence against a fake provider that drops a repeated key. It reports no race in the code itself, which keeps the guarantee.
Check: read
Workload: varies

### defect-class-extra-guard
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-defect-class-extra-guard.md`
Proves: defect-class passes the `not loan["returned"]` condition as the repair of the mechanism, and reports the added `None` checks as lines the mechanism does not need.
Check: read
Workload: varies

## Gotchas

- Each prompt builds its own scratch repository state: a commit on a branch ahead of its default branch.
- One dimension per call; asking for two gets one.
- `defect-class` needs a change that fixes a defect, or it reports none found.
- `test-quality-unreached-guarantee` was seen to fail by driving the same prompt from a worktree at the commit before test-quality asked whether a kept test reaches the case that breaks a guarantee; repeat that when changing the scenario.
- No comparison base resolves to BLOCKED.
- `tests/test_review_scope.py` pins how scope is resolved. No behavior case measures the review.
- Not yet driven: the description phrases, define's coding gates, review-pr's fleet.
