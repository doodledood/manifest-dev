# ADR: Every pull request fixes what its work meets, and verification still converges

## Status
Accepted

## Area
define / do

## Decided by
The user, for the rule and for the two rulings named in the decision. An agent under the user's
delegation of design and wording decided the rest; merging stays with the user.

## Context
The owner set a standing rule: every pull request leaves the repository better.

- A pull request fixes the debt its work leaves and the debt its review finds.
- It also fixes the pre-existing issues the work runs into, related to the change or not.
- Only an issue whose fix is a project of its own stays out, reported with the reason.
- Nothing merges until everything passes, tests included. A test that cannot run is a failure of
  the harness, and the run fixes it.
- A run never reaches green by removing, skipping or loosening a test, unless the test is useless
  or tautological.

manifest-dev encoded the opposite.
[Pull request 328](https://github.com/doodledood/manifest-dev/pull/328) made `/do` record a
below-bar finding and an unrelated pre-existing issue instead of repairing it. It made `/done` and
`/escalate` surface both for the user, with an offer to ticket them. The reason was convergence:
one run folded six rounds of Low findings on gates that had already passed, and every fold was a
new delta.

[Issue 377](https://github.com/doodledood/manifest-dev/issues/377) found repair-and-recheck
running "for many rounds instead of settling". It cites a published measurement of another team's
review loop, where about 59% of what the reviewer kept flagging was code there since the first
pass. It says that without a Pre-existing tag, "an old bug looks like the author's fault and
re-enters the change loop", and it kept the record-don't-repair rule. It was closed by
20261024-gate-criteria-and-evidence-travel-with-execution: continued looks report only outstanding
findings and failures that the intervening changes introduced or exposed.

The loop is inferred, not measured, to come from finding sources tied to the round: a reviewer that
re-sampled the whole change, and below-bar taste findings regenerated on each repair's delta. A
stock collected once is finite, and fixing it as build work ends. So the rule and convergence can
both hold if what enters the work is bounded and tagged apart from the verdict.

## Decision
A pre-existing issue the work meets, related or not, and a finding below a gate's bar are build
work, never a verdict. Neither fails a judgment gate nor starts a new full look. A pre-existing
test that fails still fails a deterministic gate, and the run fixes it. They come from three
sources only:

- The path of the change the Manifest asks for: the checks it runs, and the code it changes, calls
  into or reads to do its job.
- The *Pre-existing* list that `review-code` returns when its caller asks. The user ruled that
  `/do` asks on the first full look of each gate that activates `review-code`, and that `review-pr`
  does not ask. The list is outside the verdict and the summary counts. A follow-up review never
  returns it.
- Review feedback on the pull request.

Fixes do not chain. What fixing one of them, or repairing a finding, runs into joins only when it
blocks that fix or a check fails. The same holds for what a review raises about code that only such
a fix or repair touched. Path issues are fixed as part of the build. Issues from first full looks
and review are fixed in a batch. Then each judgment gate whose subject the batch changed takes one
continued look. That look reports only outstanding findings and failures the batch introduced or
exposed, and it lists no pre-existing issues. Each pre-existing fix lands as its own commit, and the
pull request lists it as fixed on the way.

The user ruled that below-bar findings are not debt. `/do` applies those of a first full look that
improve the work, dismisses the rest with a reason, and hands none to the user. A below-bar finding
that a continued look reports is left: it re-samples taste on the repair, and chasing it is the
loop #328 stopped. External review follows the same split. A below-bar suggestion on the change as
first reviewed is applied when it improves the work, and declined with a reason otherwise. One that
arrives on a repair is declined. A request for new work outside the assignment, such as a feature,
is declined.

Only a gigantic issue stays out: one whose fix is a project of its own, needing its own definition
of done. It is one of three kinds:

- a design decision someone should weigh;
- a migration or rollout beyond the repository's code;
- a review that would bury the change the pull request exists for.

Size, relatedness and convenience do not make an issue gigantic. Replacing a framework across the
codebase is gigantic; a failing test or a stale doc line is not. `/do` carries more examples on both
sides, so the call is made by kind and never by a number. A gigantic issue is reported as debt with
why it is a project of its own. An issue that needs access, authority or a decision a person
retains is debt that names what it needs, unless a gate depends on it; then it is a blocker.

Before `/do` reports completion, every check the project keeps across the whole tree passes,
whether or not the change touched what fails. A check that cannot run is fixed. A test is removed,
skipped or loosened only when it is useless or tautological, and the pull request description says
so. A failing check whose fix is gigantic is a blocker, never a finished run.

Debt therefore narrows to what a run found and could not fix on its pull request. That is a
gigantic issue, what needs a person (such as an ask-first run owed), a new suppression, and a
time-line overshoot frozen under a debt Ticket. The same narrowing reaches every rule that used to
leave work for later:

- A lock's hits are fixed on the pull request, in a commit of their own.
- A workaround comment is reshaped, and a constraint comment is encoded.
- A drifting recipe and a check not fit to trust are repaired.
- A time-line crossing is paid down.
- A reshaping the simplicity review finds is made.
- The scope ceiling every Manifest carries counts these fixes as required work.

Each yields to the gigantic rule above.

## Alternatives Considered
- **Keep recording and handing over (the rule of #328)**: it contradicts the owner's rule and leaves
  each finding for a person who rarely returns to it.
- **Let pre-existing issues fail a gate**: every fix becomes a delta that judgment gates re-read, and
  a reviewer re-sampling old code each round is the loop #377 describes.
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
- The North Star bet that a codebase converges "when every correction becomes a check, debt is paid
  on the path of the next change, and each long-lived artifact keeps a way to verify it" now rests
  on more debt paid on the current change too. The owner may want to restate that line.

## Enforced by
partly — `tests/test_dist_skill_references.py::test_fixing_what_the_work_meets_keeps_verification_converging`
fails when `/do` stops keeping pre-existing issues and below-bar findings out of the verdict, lets
fixes chain, or lets a continued look list pre-existing issues or chase its below-bar findings;
when external review stops declining taste on a repair or stops bounding pre-existing issues raised
on one; when `review-code` counts its *Pre-existing* list toward the verdict or returns it on a
follow-up; and when the scope ceiling stops counting these fixes as required — in the source and
the Codex copy; whether an issue is on the path, or gigantic, stays judgment.

## Source
- Session: a figure-out session on the owner's rule and verification convergence, 2026-10-28.
- Related: amends 20261013-corrections-become-scoped-locks-and-their-hits-become-reported-debt,
  20261013-debt-is-paid-on-the-path-of-work, 20261013-code-simplicity-asks-what-reshaping-removes,
  20261013-workaround-comments-become-refactor-flags-constraint-comments-become-checks,
  20261013-runs-build-and-maintain-a-project-verification-surface,
  20261015-runs-keep-the-harness-fit-for-speed-control-and-diagnosis,
  20261015-check-run-time-is-held-by-an-alarm-against-creep,
  20260926-durable-outcomes-include-subsequent-work,
  20261024-external-review-feedback-needs-an-adoption-decision,
  20260728-bound-the-acceptance-contract-from-above,
  20261015-do-states-the-goal-and-its-conventions-and-leaves-method-to-the-run,
  20260806-verification-is-bookkeeping-and-a-stop-condition,
  20261015-the-verification-harness-is-optional,
  20260602-deliberate-on-pr-review-comments-at-the-caller,
  20260812-ticket-identity-follows-work-across-automated-attempts and
  20260812-tickets-follow-independently-schedulable-work-units. See also
  20261024-gate-criteria-and-evidence-travel-with-execution and
  20260805-ratchet-judgment-gate-reverification, whose continued looks this keeps, and
  20261018-orchestrate-tickets-up-debt-and-grants-auto-where-the-criterion-holds, which still tickets
  up the debt runs leave, now only what they could not fix.
- [Pull request 328](https://github.com/doodledood/manifest-dev/pull/328)
- [Issue 377](https://github.com/doodledood/manifest-dev/issues/377)
