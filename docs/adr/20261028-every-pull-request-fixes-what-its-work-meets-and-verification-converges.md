# ADR: Every pull request fixes what its work meets, and verification still converges

## Status
Accepted

## Area
define / do

## Decided by
The user, for the rule and for the two rulings named in the decision. An agent under the user's
delegation of design and wording decided the rest; merging stays with the user.

## Context
The owner set a standing rule: every pull request leaves the repository better. A pull request
fixes the debt its work leaves and its review finds. It also fixes the pre-existing issues the work
runs into, related to the change or not. Only an issue whose fix is a project of its own stays out,
reported with the reason. Nothing merges until everything passes, tests included. A test that cannot
run is a failure of the harness, which the run fixes. A run never reaches green by removing,
skipping or loosening a test, unless the test is useless or tautological.

manifest-dev encoded the opposite. [Pull request 328](https://github.com/doodledood/manifest-dev/pull/328)
made `/do` record, not repair, a below-bar finding and a pre-existing issue unrelated to the change,
and made `/done` and `/escalate` hand them to the user as debt. The reason was convergence: one run
folded six rounds of Low findings on gates that had already passed, and every fold was a new delta.
[Issue 377](https://github.com/doodledood/manifest-dev/issues/377) found the same loop: runs went on
for days, and about 59% of repeat flags were in old code. It was closed by
20261024-gate-criteria-and-evidence-travel-with-execution, whose continued looks report only
outstanding findings and failures that the intervening changes introduced or exposed.

The loop did not come from the stock of pre-existing issues. It came from finding generators tied to
the round: a reviewer that re-sampled the whole change, and below-bar taste findings regenerated on
each repair's delta. A stock collected once and fixed as build work is finite, so it converges. So
the rule and convergence can both hold, if what enters the work is bounded.

## Decision
A pre-existing issue the work meets, related or not, and a finding below a gate's bar are build work,
never a verdict. Neither fails a gate nor starts a new full look. They come from three sources only:

- the path of the change the Manifest asks for: the checks it runs and the code it changes, calls
  into or reads to do its job;
- the *Pre-existing* list that `review-code` returns when its caller asks. `/do` asks on each
  judgment gate's first full look. The list is outside the verdict and the summary counts, and a
  follow-up review never returns it. `review-pr` does not ask. (The user's ruling.)
- review feedback on the pull request.

What fixing one of them, or repairing a finding, runs into joins only when it blocks that fix or a
check fails. So fixes do not chain. Path issues are fixed as part of the build. Issues from first
full looks and review are fixed in a batch. Then each judgment gate whose subject the batch changed
takes one continued look, which reports only failures the batch introduced or exposed. A continued
look lists no pre-existing issues. Each pre-existing fix lands as its own commit, and the pull
request lists it as fixed on the way.

Below-bar findings are not debt. `/do` applies those of a first full look that improve the work,
dismisses the rest with a reason, and hands none to the user. A below-bar finding that a continued
look reports on a repair is left: it re-samples taste on the repair, and chasing it is the loop that
#328 stopped. (The user's ruling.) External review follows the same split: a below-bar suggestion
on the change as first reviewed is applied or declined, and one that arrives on a repair is
declined. A request for new work outside the assignment, such as a feature, is declined.

Only a gigantic issue stays out: one whose fix is a project of its own, needing its own definition
of done. It is a design decision someone should weigh, a migration or rollout beyond the
repository's code, or a review that would bury the change the pull request exists for. Size,
relatedness and convenience do not make an issue gigantic. The principle carries examples on both
sides in `/do`, so it is judged by kind and never by a number. A gigantic issue is reported as debt
with why it is a project of its own. An issue that needs access, authority or a decision a person
retains is a blocker, not debt.

Before `/do` reports completion, every check the project keeps across the whole tree passes,
whether or not the change touched what fails. A check that cannot run is fixed. A test is removed,
skipped or loosened only when it is useless or tautological, and the pull request description says
so. A failing check whose fix is gigantic is a blocker, never a finished run.

Debt therefore narrows to what a run found and could not fix on its pull request: gigantic issues,
new suppressions, ask-first runs owed, and a time-line overshoot frozen under a debt Ticket. The same
narrowing reaches locks (their hits are fixed on the pull request in their own commit),
workaround comments (reshaped unless gigantic), constraint comments (encoded), recipe drift and
unfit checks (repaired), a time-line crossing (paid down unless gigantic), and a reshaping the
simplicity review finds (applied unless gigantic).

## Alternatives Considered
- **Keep recording and handing over (the rule of #328)**: it contradicts the owner's rule and leaves
  each finding for a person who rarely returns to it.
- **Let pre-existing issues fail a gate**: every fix becomes a delta that judgment gates re-read, and
  a reviewer re-sampling old code each round is the loop #377 measured.
- **Have every review, including follow-ups and `review-pr`, list pre-existing issues**: an
  open-ended source per round, which never settles. The user ruled for the first full look only.
- **Hand below-bar findings to the user as before**: they rarely get read, and the user ruled that
  none are handed over.
- **Define "gigantic" by a number of files, lines or hits**: a count misjudges both ways. A few
  dozen mechanical hits are cheap, and one module redesign is not. A principle with examples
  transfers across projects.
- **Fix everything the fixes run into**: fixes chain, and the stock stops being finite.

## Consequences

### Positive
- A pull request leaves its area better, including the pre-existing issues it met, without anyone
  coming back for them.
- Verification still converges: the stock is fixed, collected once, and each batch takes one
  continued look.
- Debt lists get short, so each item they keep is worth reading.

### Negative
- Pull requests grow by the fixes made on the way, each in its own commit, so reviews read more.
- Whether an issue is on the path, or gigantic, stays a judgment, and a run can misjudge it either
  way.
- Below-bar findings on repairs are lost by design.
- The North Star bet that a codebase converges "when debt is paid on the path of the next change"
  now rests on more paid on the current change too. The owner may want to restate that line.

## Enforced by
partly — `tests/test_dist_skill_references.py::test_fixing_what_the_work_meets_keeps_verification_converging`
fails when `/do` stops keeping pre-existing issues and below-bar findings out of the verdict, lets
fixes chain, or lets a continued look list pre-existing issues or chase its below-bar findings, and
when `review-code` counts its *Pre-existing* list toward the verdict or returns it on a follow-up,
in the source and the Codex copy; whether an issue is on the path, or gigantic, stays judgment.

## Source
- Session: a figure-out session on the owner's rule and verification convergence, 2026-10-28.
- Related: amends 20261013-corrections-become-scoped-locks-and-their-hits-become-reported-debt,
  20261013-debt-is-paid-on-the-path-of-work, 20261013-code-simplicity-asks-what-reshaping-removes,
  20261013-workaround-comments-become-refactor-flags-constraint-comments-become-checks,
  20261013-runs-build-and-maintain-a-project-verification-surface,
  20261015-runs-keep-the-harness-fit-for-speed-control-and-diagnosis,
  20261015-check-run-time-is-held-by-an-alarm-against-creep,
  20260926-durable-outcomes-include-subsequent-work and
  20261024-external-review-feedback-needs-an-adoption-decision. See also
  20261024-gate-criteria-and-evidence-travel-with-execution and
  20260805-ratchet-judgment-gate-reverification, whose continued looks this keeps, and
  20261018-orchestrate-tickets-up-debt-and-grants-auto-where-the-criterion-holds, which still tickets
  up the debt runs leave, now only what is gigantic.
- [Pull request 328](https://github.com/doodledood/manifest-dev/pull/328)
- [Issue 377](https://github.com/doodledood/manifest-dev/issues/377)
