# do: building and keeping the verification harness

What a harness is, what it owes and what shape it takes by default are in
`../../setup-project/references/VERIFICATION_HARNESS.md`; how to use this project's harness is in
its own `--help`.

- **Missing parts:** this file applies where the project keeps a verification harness, which is
  the project's choice and never the run's, as `../SKILL.md` says. Build what the change needs that the harness lacks, scoped to what the change touches, as
  `../../setup-project/references/VERIFICATION_HARNESS.md` → *What setup creates, and what runs build*
  describes, unattended too: it is verification for the change, like a regression test.
- **Touched recipes:** `verify affected` lists the recipes the change touches and the changed
  paths no recipe covers; an uncovered path a user reaches gets a recipe. A recipe covering the whole
  tree, for the project's lint, types or test suite, never counts as covering such a path, and
  where one exists `affected` lists no uncovered path, so check each changed path a user reaches
  against the other recipes' `covers`. Update each touched
  recipe to match the change and run it; what the run found goes in the report, and its evidence
  stays where the harness keeps it, uncommitted. A recipe marked ask-first runs
  only with the agreement `../../setup-project/references/VERIFICATION_HARNESS.md` → *Ask first*
  describes; otherwise update it, leave it unrun, and name the run it owes in the report. A
  change to a prompt that leaves its measured eval cases unrun marks them `stale`; unmeasured
  cases stay `unmeasured`.
- **Drift:** when a run fails because the recipe is wrong about the product, repair the recipe
  within scope, and remove its `Drift (…)` line when the repair lands. When a recipe the change
  does not touch is found drifting, add a dated `Drift (YYYY-MM-DD): <what differs>` line to it,
  and leave the repair to the next run that touches it.
- **Unfit harness:** when the harness is not fit to trust for what the work touches
  (`../../setup-project/references/VERIFICATION_HARNESS.md` → *Fit to trust*), repair it within
  scope, and report the rest as debt.
- **Time lines:** a line is written into its recipe only by the change that changes that check.
  A fixed-workload scenario the change adds gets its first line from a passing run (`verify
  line`), and a change that made a check faster keeps the gain the same way; no other run moves a
  line. Before a lower line is written, compare the work the check did — tests collected, cases
  run — with a run of the same check at the base commit: a speedup that comes from doing less work
  keeps the old line, and the lost work is a finding.
- **Over its line:** when a check the work touches is over its time line, find where the time
  went from the runner's own timings. Pay it down before the run is done when growth did not earn
  the time — it came from what the change added, such as a slow new test or a sleep — or when the
  fix lies in code the change already touches. When the fix needs shared code the change does not
  touch, or a broad refactor, open or join one debt Ticket, freeze the overshoot with it, and
  report it as debt. Raise the line only when the new time is in new tests for new behavior, the
  existing tests are no slower, and no cheap waste remains, with that reason on the raise and one
  line in the pull request.
- **A stand-in is not the target:** where a check runs on a stand-in for where the work will run —
  a cloud container that already has tools a user's machine lacks, a fixture in place of the real
  service — the report names, as unverified, what the stand-in provided that the target will not.
- **Never weaken a check** to make it pass or run faster. A run that fails because the product
  is broken is reported as debt with its evidence.
