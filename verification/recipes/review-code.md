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
- In a project, it loads the principles skills the project context file points to whose stated use covers the change, whatever their area word, and holds the change to them: the dimension that owns a principle's call reports an unchosen departure, and context-file-adherence covers every principle.

## Scenarios

### review
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-review.md`
Proves: a report naming the dimension, findings with severity and evidence, and one verdict. Every finding points at a line inside the change.
Check: read

### project-rule
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-project-rule.md`
Proves: with a context file naming a convention a dimension would flag (a shared module-level instance) and a change following it, there is no finding on the convention; the report names the rule applied.
Check: read

### principles-skills
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-principles.md --scaffold verification/scaffolds/principles-review`
Proves: graders, applied to the report: (1) both reviews load the principles skills the context file points to; (2) the maintainability review raises no finding for `poll_title` repeated in `src/exports` and `src/notify`, naming the architecture principle it applied; (3) the context-file-adherence review reports the green leading bar in the live results view, quoting the neutral-colour principle; (4) neither review offers to edit a principles skill. PASS when all four hold.
Check: read

### project-rule-critical
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-project-rule-critical.md`
Proves: with a rule whose result is a Critical finding (logging a login body with its password), the Critical finding is still reported, naming the rule that produced it.
Check: read

### test-quality-pinned
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-test-quality-pinned.md`
Proves: test-quality reports the test that asserts the order of `Invoice`'s private helper calls as pinned to the implementation — an edit to the internals that keeps the total would fail it — and names the behavior to assert instead, the total.
Check: read

### defect-class-extra-guard
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-defect-class-extra-guard.md`
Proves: defect-class passes the `not loan["returned"]` condition as the repair of the mechanism, and reports the added `None` checks as lines the mechanism does not need.
Check: read

### pre-existing
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-pre-existing.md`
Proves: asked for it on a fresh full look, the report carries a *Pre-existing* section naming the division by zero in `unit_price`, which the change does not touch, with its location. The verdict and the summary counts rest only on findings inside the change, and the division by zero is not among them.
Check: read

### follow-up
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-follow-up.md --scaffold verification/fixtures/review-continuity`
Proves: the report closes F1 because private notes no longer leak, retains F2 because the last line is still missing from the total, and reports the repair's conversion of identifier strings to integers. It does not add a finding about the unchanged sorting of line SKUs. The report names the prior reviewed state and current scope; broad contextual reading is allowed.
Check: read

### fresh
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-fresh.md --scaffold verification/fixtures/review-continuity`
Proves: this new explicit full review reports the input-order violation from sorting SKUs, as well as the identifier and total defects. Historical review files do not silently narrow the requested scope. The fixture is the same as follow-up, so the requested review scope explains the different eligible findings.
Check: read

### rare-correctness
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-rare-correctness.md`
Proves: code-bugs reports the lost item at page 99, size 1 as High or Critical and FAIL, with its concrete trigger and evidence. Rarity and a workaround do not make the wrong result Low. Inspect the report, not just its final verdict.
Check: read

### caller-policy
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-caller-policy.md --scaffold verification/fixtures/review-caller-policy`
Proves: the naming divergence from the declared advisory convention is Low, without correctness or broken-promise findings. With the first caller's Medium+ gate it passes; with the second caller's Low-inclusive gate the same Low fails without changing severity. The third turn returns classifications without inventing a gate verdict. The source and instructions remain byte-identical. Read the actual reports, not just a completion claim.
Check: read

### independent-replacement
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-independent-replacement.md --scaffold verification/fixtures/independent-replacement`
Proves: defect-class accepts the stateless lookup on independent contract evidence and inspection of its full supported string domain, while disclosing that the precise old provider cause is unknown. It does not invent a diagnosis requirement or infer adequacy from the replacement label or passing tests alone.
Check: read

### diagnosis-remains-required
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-diagnosis-required.md --scaffold verification/fixtures/independent-replacement`
Proves: the same valid replacement does not discharge the explicitly commissioned diagnosis. The verdict is BLOCKED on missing historical evidence, with no invented cause or weakened user requirement.
Check: read

### source-authority-and-evidence
Run: `scripts/drive-skill.sh review-code verification/prompts/acceptance/review-authority.md --scaffold verification/fixtures/acceptance-review`
Proves: The intentional one-row full export violates its source contract despite its comment. Its mocked test does not establish production behavior despite the unit-only pattern. The deliberately limited preview and its adequate real unit tests are acceptable without an integration-test mandate.
Check: read

<!-- The two state-machine scenarios hold docs/adr/20261107-review-checks-the-whole-state-machine-a-change-touches.md. -->
### state-machine-cross-file
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-state-machine-cross-file.md --scaffold verification/fixtures/review-state-machine-cross-file`
Proves: code-bugs rebuilds the order lifecycle from every writer, including the files the change does not touch, and reports that the new cancel lets an order end both refunded and delivered (pay, ship, cancel, the nightly refund, then the carrier's delivery), with each site by file and line and the confirmed sequence as its trigger, at High or Critical, and FAIL. The prompt names no bug and no state machine.
Check: read

### state-machine-sound
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-state-machine-sound.md --scaffold verification/fixtures/review-state-machine-sound`
Proves: a change that adds a paused state to an explicit machine, with every new transition in its table and every write through one function, draws no state-machine finding, and the verdict is PASS.
Check: read

### principles-depart
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-principles-depart.md --scaffold verification/scaffolds/principles-shelfmark-departs`
Proves: the project's context file points, in its own words, to `craft-principles`, an area word no dimension carries, whose lines are of several kinds. The change names and guards SMS reminders for one branch (`CentralBranchOverdueSms`, `CENTRAL_SMS_ENABLED`, `if branch.name == "central"`) beside a channel registry that would carry SMS as a setting. The registry would carry SMS as a setting for any of the three branches, whose members all have phone numbers in `data/members.csv`. The change's own decision 0002 declares North and Harbor out of scope, "a later decision for their managers", and claims the first line's yield on that ground alone. No other project document states a rule against the change. Graders, on both reports (code-design and context-file-adherence): (1) a finding quotes craft-principles' first line, names the changed code, and says the yield is not shown; (2) decision 0002 is taken neither as a person's choice of the departure nor as evidence that the yield holds; (3) that finding is graded above Low; (4) the verdict is FAIL. PASS when all four hold on both reports.
Check: read

### principles-hold
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-principles-hold.md --scaffold verification/scaffolds/principles-shelfmark-holds`
Proves: the same project, with a change that sends a monthly statement and touches the three craft-principles lines while owing nothing on any. Graders: (1) on both reports (code-design and context-file-adherence), no finding that counts against acceptance rests on any craft-principles line; (2) the code-design report gives the first line as followed, since the return address is a branch setting; on the context-file-adherence report, which covers every principle: (3) the first line is followed; (4) the long statement body's comparison with a reviewed snapshot file is the second line's yield, shown by the work itself; (5) the greeting test's partial check is a departure the maintainer chose in decision 0001; (6) the third line (paste the test summary before review) is not reported as followed or as a departure; (7) on both reports, no outreach-principles line draws a finding or appears as touched, though a comment writes "three" as a word; (8) both verdicts are PASS. PASS when all eight hold.
Check: read

### widen-catch
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-widen.md --scaffold verification/scaffolds/widen-presswork-catch`
Proves: Presswork's principles skills are the architecture and code starter sets as written. A print job takes one paper stock; the change meets "booklet covers on card" by adding a cover stock override to the customer profile, with its own service, a guard against proofs, a glossary term and a decision record whose five alternatives never mention the job's stock input; it extends the customer profile, an existing owner. The change is otherwise sound — one function owns the sheet split, flat jobs and proofs ignore the setting, it is checked where it is set, the quote cache keys on what is priced, and planning a run re-reserves its paper — so a review that faults it has to fault the placement. Grader, on the code-design report: on that main choice, the report raises a departure from a principle, or asks why the job's existing stock input could not take more than one stock (one per part of the booklet). PASS when it does. With `STARTER_SETS_AT` set to a revision before the starter line about widening before adding a concept, the review reads the line about extending what already does that job as followed and names no existing input to widen, though it may still fault the placement through another line; only the arm with the widen line names the job's stock input and asks to widen it. That reading was chosen after the first runs, on the maintainer's delegation, because this grader, fixed before them, did not tell the two arms apart; see `docs/adr/20261119-a-starter-line-is-held-only-where-one-line-states-all-of-it.md`.
Check: read

### widen-quiet
Run: `scripts/drive-skill.sh review-code verification/prompts/review-code-widen.md --scaffold verification/scaffolds/widen-presswork-quiet`
Proves: the same project, with a change that adds two named concepts where widening is wrong. Quiet hours: a shop setting nothing existing schedules. Lamination: a job setting beside `finish`, which looks close, but the glossary and decision 0001 say a finish is the press coating, and the change's record says why it does not widen `finish`. Graders, on the code-design report: (1) no finding that counts against acceptance rests on the starter line about widening before adding a concept, for either addition; (2) where the report lists that line's standing, it gives followed or yield shown for both. PASS when both hold.
Check: read

## Gotchas

- Each prompt builds its own scratch repository state: a commit on a branch ahead of its default branch.
- One dimension per call; asking for two gets one.
- `defect-class` needs a change that fixes a defect, or it reports none found.
- No comparison base resolves to BLOCKED.
- `tests/test_review_scope.py` exercises the scope commands; `tests/test_drive_scripts.py` checks convergence fixtures. The follow-up and fresh drives are unmeasured; fixture checks do not measure review behavior.
- Not yet driven: the description phrases, define's coding gates. review-pr's fleet runs these dimensions in the review-pr recipe's `principles` and `existing-owner` scenarios.
- The Presswork scaffolds (`widen-presswork*`) read the architecture and code starter sets from the checkout, or from the revision `STARTER_SETS_AT` names, so a drive with `STARTER_SETS_AT=origin/main` against one without compares two sets on one change. The quiet-change scaffold uses `tomllib` (Python 3.11 or newer).
- The Shelfmark scaffolds (`principles-shelfmark-departs`, `principles-shelfmark-holds`, used by the `principles-depart` and `principles-hold` scenarios) use `tomllib`, so their own tests need Python 3.11 or newer; the reviews do not depend on running them.
- The principles cases are caught on the merge-base skills too: today's models follow the context file's pointers. The discriminating evidence for the review rule is a replay on a real change kept outside this repository, on `code-design` and `context-file-adherence`: merge-base skills: not caught; branch: caught.

- The consequence/promise scenario ran once per arm through native GPT-6.1 Sol/xhigh contexts on 2026-11-05. The decision records dated that day name the outcomes and limits; scaffold checks alone do not establish behavior.
