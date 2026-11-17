# ADR: A review gate states how it ends: look once, or look again

## Status
Accepted

## Area
define / do

## Decided by
The user, for the two-sided form, for operational readiness looking once by default and again on
high-stakes work, and for one more fresh defect-finder look at product behavior where no later
review exists. An agent chose the wording and where each rule lives.

## Context
After the first review of a change, review and repair often ran for many rounds. A review gate
states an open-ended claim, such as "the code is correct, simple and testable". Such a claim can
be shown false but never shown true. Done then means "a reviewer found nothing this time", and
each repair reopens the question. One claim also bundled promises the user is owed with qualities
that merit one careful look, so a polish finding kept the whole gate open.

The user's run records were mined before this decision: 25 `/do` runs, 13 in one product
repository whose pull requests get a second review by an automated reviewer, and 12 in
repositories with no reviewer after the run. One AI grader classified each run's findings: A for
a serious defect, B for a real issue with a concrete cost, C for polish, D for a false alarm.
Later rounds produced 465 code-review findings:

- 316 came from advisory dimensions alone, or concerned tests, fixtures, scripts or docs: A 0,
  B 89, C 226, D 1. The count of A was 0 in both groups of repositories.
- 149 came from defect-finders on product code and prompts: A 20, B 85, C 42, D 2.

In repositories with no later reviewer, full re-reads in later rounds were the only second look.
They found 10 serious defects in original work that the first look had missed.

The skill text already scoped continued looks to repairs
(20261024-gate-criteria-and-evidence-travel-with-execution,
20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges). The loop went on
for two reasons. First, the completion check reads only the goal block and the Manifest, never
`/do`'s rules, and asked for a fresh full review of each new head. Second, a defect-finder on test
scaffolding kept finding real holes in the code each repair added. On 2026-11-17 a ten-dimension
gate on test code ran six full looks. The user ended that loop by amending the gate's Evidence to
one full look, after which each repair gets a check rather than another review run. The
completion check accepted that wording at once.

## Decision
Every gate whose Evidence activates a review skill also states, in that Evidence, how it
re-verifies after repairs. `/define` puts each such gate on one of two sides by what is owed, and
splits a gate whose concerns fall on both sides. The claim stays about the artifact. No schema
field is added.

- **Look again** covers product behavior: the Outcome, behaviors the Manifest names, safety
  obligations, and defect-finding dimensions on code and prompts the project ships or deploys,
  never its tests, fixtures, scripts or tooling.
  - After each repair batch, the gate takes a continued look.
  - The Manifest may name no later review. A later review is a gate that sends defect findings
    back before merge, such as a pull-request lifecycle gate whose feedback includes a reviewer
    bot or agent, or a required reviewer approval. In that case the gate also takes one fresh
    full look by its defect-finding dimensions at the finished change, once its continued looks
    report nothing outstanding.
  - The fresh look's findings get fixes and repair checks. Its below-bar findings are left, as a
    continued look's are. No second fresh look follows.
- **Look once** covers advisory qualities, and every dimension on supporting code (tests,
  fixtures, scaffolds, scripts, tooling) and on docs.
  - The gate takes one full look at the change as built, once every Deliverable it covers is done.
  - Each finding is fixed, or rejected with a reason.
  - Each repair is checked. Where the finding names a behavior, the check is a test or
    reproduction that fails without the repair. Otherwise it is a read against the finding.
  - That look and those checks are the gate's evidence for the finished change, and no further
    review run is owed.
  - Work added later, such as a later Deliverable or an amendment that adds work, gets a full
    look of its own.
  - A repair that changes product behavior is seen by the look-again gates whose subject it
    changes.
- **Operational readiness** looks once. It looks again where the work is high-stakes, such as
  work that acts with a person's authority, reaches credentials, moves money or people's data,
  deletes what cannot be restored, or runs unattended in production. `/define` judges it; the
  examples are not a closed list.
- **A design review** splits the same way: what the person can do with the artifact (task fit,
  functional states, viewport behavior) looks again; composition, hierarchy, craft, copy and
  register fit look once.

`/do` follows the form a gate states. A gate that states no form, such as a gate in a Manifest
written before this decision, re-verifies as before.

## Alternatives Considered
- **Split by dimension role only (advisory looks once, defect-finders keep looking):** in the
  2026-11-17 run, `code-bugs` on test scaffolding drove every round after the first, so this
  split would not have ended that loop. What a gate judges matters, not only who judges it.
- **No reviewer after the first look; each repair gets only its own check:** in the first 14 runs
  mined, it would have lost 6 serious findings, 4 of them bugs that round-1 repairs introduced.
- **Enforce today's rules more strictly:** all 177 late polish findings in the first 14 runs mined
  were graded Medium by their reviewers, so the rule that leaves below-bar findings never applied
  to them. The
  completion check never read the rule.
- **A stop rule by a count of rounds:** rejected again, as in 20260805-ratchet-judgment-gate-reverification and
  20261106-review-evidence-serves-substantive-acceptance. A count
  cannot tell an unowed polish promise from an owed correctness repair.
- **A fresh second look at product behavior on every run:** the user chose to take it only where
  no later review exists. Where a reviewer follows the run, it repeats a layer the repository
  already has.
- **A schema field for the form:** the Evidence text already reaches every reader. A field would
  add migration and version skew for no reader that the text misses.

## Consequences

### Positive
- A look-once gate has a finish line that the executor, its evaluators and a completion check can
  all read from the gate.
- Product behavior keeps its re-looks. Where no reviewer follows the run, it also gets the second
  look that found serious defects the first look missed.
- The 2026-11-17 kind of loop on test scaffolding ends after one look and its repair checks.

### Negative
- Later rounds will no longer produce about 3 or 4 real minor findings per run. About one of those
  is a behavior failure, and half of those came from operational readiness.
- `/define` can put a quality on the wrong side. Repair checks and look-again gates are what catch
  a behavior failure filed under a look-once gate.
- Where no later review exists, the fresh look costs one more defect-finder pass per look-again
  gate.
- The evidence is one AI grader per run, and no run compared the two forms directly.

## Enforced by
partly — `tests/test_review_convergence.py::test_a_review_gate_states_how_it_ends` fails when the
rule's sentences leave `define/SKILL.md`, `define/tasks/CODING.md`, `define/tasks/PROMPTING.md`,
`define/tasks/UI.md`, `define/references/SCHEMA.md` or `do/SKILL.md`, or their Codex copies. Behavior cases in
`verification/recipes/define.md` (`review-gate-ends`, `review-gate-ends-with-reviewer`) and
`verification/recipes/do.md` (`look-once-settles`) exercise placement and execution. Whether
`/define` places a quality on the right side stays judgment.

## Revisit when
Real runs under this form still loop on look-again gates, or a serious defect is found after
completion in an area a look-once gate covered. Read the run log and the gate's Evidence before
changing the boundary.

## Source
- Issue: https://github.com/doodledood/manifest-dev/issues/445
- Amends 20260805-ratchet-judgment-gate-reverification, 20261024-gate-criteria-and-evidence-travel-with-execution, 20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges and 20261106-review-evidence-serves-substantive-acceptance
- Related: 20260810-advisory-gates-omit-by-bearer-test, 20261105-repairs-track-the-accepted-promise, 20261105-review-severity-follows-consequence
