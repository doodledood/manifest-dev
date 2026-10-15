# ADR: A check's run time is held by an alarm against creep, set from measurement and moved only on purpose

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
Verification speed binds like cost, second to quality
(20261015-verification-speed-binds-like-cost-second-to-quality). The common way it is lost is
creep: each change adds a few seconds, each step is too small to notice, and the suite
becomes the bottleneck before anyone acts. The owner's projects went through that more than
once, and seeing that the suite was slow did not stop it. Nothing in the v4 harness measures
run time, so creep is invisible until it dominates.

A number a person picks is arbitrary, and a growing app cannot keep a small number forever.
Comparing each run to the one before misses creep, because each step sits inside the timing
noise. The owner also does not want slowness to decide when a check runs: fast and slow are
something the agent is aware of, not a rule. And the owner runs many agents at once on one
project, working on different things but sharing one harness and one suite. A rule that makes
every crossing run rewrite shared test code would have those agents collide.

## Decision
- Every run records its wall-clock duration in its evidence, with the kind of machine it ran on.
- A scenario whose workload is fixed gets a line: its first measured time on that kind of
  machine, plus headroom for noise. Nobody picks the number. A scenario whose work varies with
  the change, such as the affected tests, gets none. Its speed comes from the cost of each test,
  which the fixed-workload runs guard.
- The line is an alarm against creep, and nothing else. It means "no slower than the last
  accepted state without a reason". It never decides when a check runs or who may run it.
- The line moves only on purpose. It goes down when a run makes the check faster, so the gain is
  kept. It goes up when the run that crosses it shows, from the test runner's own timings, that
  the new time is in new tests for new behavior, the existing tests are no slower, and no cheap
  waste remains. That run then writes one line in its pull request saying why. By default the
  agent may raise a line. A project can require a person instead, with one setting.
- Where its fix lives decides what happens to a crossing that growth did not earn, not its size.
  When the time came from what this change added, such as a slow new test or a sleep, or the fix
  lies in code the change already touches, the run that crosses the line pays it down before it
  is done. When the fix needs shared code the change does not touch, such as fixtures, test
  infrastructure or the harness itself, or needs a broad refactor, the run does not fold it in.
  It opens or joins one debt Ticket instead. The Ticket freezes the overshoot at its current
  level. Other runs are not held up by it, but time past that level is new creep, and the run
  that causes it pays. One owner pays the Ticket as its own change. This is the same scope line
  runs already follow for lock hits and pre-existing issues, and it is also where agents working
  side by side would collide.
- A line, its raises and lowerings, and the Ticket that freezes an overshoot are derived from
  each run's own evidence, like a status. They are never kept in a file every run edits, so runs
  side by side never conflict over them.
- A crossing counts only after one re-run confirms it.
- Speed is never bought with proof. Mocking past a real boundary, or deleting or skipping a slow
  test, weakens a check, and runs never weaken a check to make it pass.

## Alternatives Considered
- **Awareness only: record durations and let nothing fire.** That is what the owner's projects
  had while their suites crept up.
- **Compare each run with the previous one**: misses creep, because every step is inside the noise.
- **Numbers a person chooses**: arbitrary, and they cannot follow an app that grows.
- **Only a person may raise a line**: the strongest guard against an agent explaining waste away,
  but every step of growth waits for a person, which does not scale to many agents. It stays
  available as the project setting.
- **CPU time instead of wall time**: steadier, but it hides waiting. Waiting was most of this
  repository's suite: 94 s of wall time against 36.5 s of CPU.
- **Report a crossing as debt and finish**: the creep stays visible but builds up again.
- **Pay every crossing in the change that finds it**: whichever agent crosses first rewrites
  shared test code, many pull requests do it at once and collide, and unrelated changes widen.
- **Defer above a size threshold**: an arbitrary number, and it does not follow where agents
  collide.
- **Reuse results across runs when the covered files are unchanged**: the largest saving at
  scale, but `covers` lists are written by hand, so a cache hit can vouch for a dependency
  nobody tested. Left for later, and never for the check before done.

## Consequences

### Positive
- Creep fails at the change that causes it and is paid in small steps, not in a large clean-up.
- Growth is allowed, and the history says why each check got slower.

### Negative
- Timing noise and differences between machines need headroom and a line for each kind of
  machine, and a crossing costs one confirming re-run.
- Deciding whether growth earned the time is a judgment that review has to hold.
- A frozen overshoot leaves the suite slower until its Ticket is paid.

## Enforced by
not yet — `tests/test_verify.py` cases that evidence records duration and machine, that a
fixed-workload scenario over its line shows in the recipe's status until it is paid, raised or
frozen by a Ticket, that a raise without a recorded reason is refused, and that a frozen
overshoot fails a run only once time passes the frozen level.

## Source
- Session: figure-out investigation of the verification harness's control, speed and
  confidence, 2026-10-15.
- Related: see also 20261015-verification-speed-binds-like-cost-second-to-quality,
  20261015-ask-first-marks-cost-not-slowness
