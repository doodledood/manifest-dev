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
- **Run time:** follow `../../setup-project/references/VERIFICATION_HARNESS.md` → *Run time*.
  When a check the work touches has grown slow, find where the time went from the runner's own
  timings and speed it up where the cause is in what the change added, such as a slow new test or
  a sleep, or in code it already touches; otherwise say in the report which check is slow and
  where the time goes. Slowness is never a reason to stop, gate, freeze or open a Ticket, and it is
  not a debt item.
- **A stand-in is not the target:** where a check runs on a stand-in for where the work will run —
  a cloud container that already has tools a user's machine lacks, a fixture in place of the real
  service — the report names, as unverified, what the stand-in provided that the target will not.
- **Never weaken a check** to make it pass or run faster. A run that fails because the product
  is broken is reported as debt with its evidence.
