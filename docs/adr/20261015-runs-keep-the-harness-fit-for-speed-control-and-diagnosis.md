# ADR: Runs keep the harness fit to trust for speed, control and diagnosis, through one list

## Status
Accepted — amended by 20261019-a-check-counts-only-after-it-was-seen-to-fail: *Fit to trust* gains a job, that the check was seen to fail on a scratch break of what it proves; amended by 20261031-time-lines-are-removed-and-run-time-is-only-reported: the *fast enough* job is removed, and a slow check is friction to fix, never a reason the check cannot be trusted

## Area
define / do

## Decided by
The user

## Context
20261013-runs-build-and-maintain-a-project-verification-surface made normal runs build and
repair the verification harness where their work touches it, with no maintenance pass. What a
run checks before relying on the harness is its *Fit to trust* list in setup-project's harness
reference: a cold proof run passes, health is checkable, runs are isolated, and PASS means the
real path. figure-out's coding probes, define's verification rule and coding Defaults, and do's
harness reference all judge the harness against that list for the recipes their work touches.

Those four jobs keep the harness correct. They do not keep it fast, controllable or helpful
when something fails. The owner wants every task to keep all of that healthy, so each task moves
the project one step toward a codebase agents can work in on their own. That is the North
Star's hypothesis that a codebase converges when debt is paid on the path of the next change.

## Decision
- *Fit to trust* gains three jobs. **Fast enough**: no check the work touches sits over its time
  line without a reason (20261015-check-run-time-is-held-by-an-alarm-against-creep).
  **Controllable**: what the work touches can be started in a known state, observed and stopped
  through the harness or the project's own scripts, each run on its own
  (20261015-the-verification-harness-controls-what-it-checks). **A failure explains itself**:
  failed evidence carries what locates the cause.
- That list is the hook, and no skill gets a rule of its own. figure-out asks about these jobs,
  define cuts the repair as the first Deliverable when one fails for what the work touches, and
  do repairs within scope and reports the rest as debt, as each already does for the existing
  jobs.
- Friction becomes a harness command, beside "a correction becomes a lock". When a run had to
  start something by hand, add a print to see its state, or wait on something slow, it leaves
  the harness able to do that within scope — or the project's own scripts, where it verifies its
  own way (20261015-the-verification-harness-is-optional) — or names the gap as debt.

## Alternatives Considered
- **A rule in each skill**: the same rule in several prompts, read on every run and free to
  drift apart.
- **A scheduled maintenance pass**: rejected in 20261013 because it needs infrastructure and
  depends on someone remembering.
- **Leave upkeep to the user**: that produces the periodic large clean-ups the owner already
  knows.

## Consequences

### Positive
- Every task leaves the harness a little faster, more controllable or clearer where it touched.
- No new skill, schedule or per-skill rule.

### Negative
- Judging fit to trust takes a run a little longer.
- Noticing friction is judgment, and a run can miss it.

## Enforced by
partly — eval cases `54-touched-recipe-not-fit` (figure-out folds the repair into
the work) and `d23-unfit-recipe-repaired-first` (define cuts the repair as the first Deliverable)
measure the repair once run. Whether a run noticed friction and whether a failure explains itself
stay judgment.

## Source
- Session: figure-out investigation of the verification harness's control, speed and
  confidence, 2026-10-15.
- Related: amends 20261013-runs-build-and-maintain-a-project-verification-surface
