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
- **Drift:** when a run fails because the recipe is wrong about the product, repair the recipe,
  and remove its `Drift (…)` line when the repair lands. A recipe the change does not touch that
  the run finds drifting is repaired too, in a commit of its own; only where that repair is
  gigantic, or the project's own rules keep fixes unrelated to the change out (`../SKILL.md` →
  *What holds for every gate*), does it get a dated
  `Drift (YYYY-MM-DD): <what differs>` line, reported as debt — while no gate and no whole-tree
  check rests on it; otherwise it is a blocker.
- **Unfit harness:** when the harness is not fit to trust for what the work touches
  (`../../setup-project/references/VERIFICATION_HARNESS.md` → *Fit to trust*), repair it. A
  passing exit code cannot establish a claim the check does not actually test. If unfitness
  invalidates necessary evidence, establish adequate evidence through an authorized alternative
  or keep the obligation unresolved; a gigantic repair does not turn missing proof into debt.
  A gigantic maintenance improvement may be debt only when required checks still run and pass
  and the acceptance evidence remains valid (`../SKILL.md` → *What holds for every gate*).
- **Run time:** follow `../../setup-project/references/VERIFICATION_HARNESS.md` → *Run time*.
  When a check the work meets has grown slow, find where the time went from the runner's own
  timings and speed it up — a slow new test, a sleep, waste in shared code alike; where that is
  gigantic, say in the report which check is slow and where the time goes. Slowness is never debt
  and never a blocker.
- **A stand-in is not the target:** where a check runs on a stand-in for where the work will run —
  a cloud container that already has tools a user's machine lacks, a fixture in place of the real
  service — the report names, as unverified, what the stand-in provided that the target will not.
- **Never weaken a check** to make it pass or run faster; only a useless or tautological test may
  go, named in the pull request description with why. A check that fails because the product
  is broken, or that cannot run, is fixed as `../SKILL.md` → *What holds for every gate* says;
  only a gigantic fix is a blocker, escalated with its evidence.

## Host-owned general-agent drives

For a behavior drive or document walk, the running host starts a fresh general agent with the
scenario as its brief. Use the project's snapshot, fixture and evidence helpers where provided;
the scenario may invoke a skill or let the agent choose skills and their scripts. Keep expected
outcomes outside that agent's context. Supply the copied resources and scratch project, with no
parent conversation or injected target skill body. Continue the same agent for later user turns.

Preparation is incomplete evidence. Record the actual host session identity, terminal replies,
settings the host exposes and produced artifacts, then finalize through the project's recipe.
Wrong, changed, partial or failed inputs/results stay unverified. The subject writes no completion
receipt; the parent judges its actual output against the recipe. A completed session is not a
behavior verdict. Report unavailable tools or evidence; do not infer native plugin registration
or equal behavior across hosts from reading copied skills.

When the host has no general agents, warn and ask the user what to do, keeping the drive incomplete
while that choice is pending. A script calling the same host harness is a fallback only after
explicit user approval. Never choose another provider automatically or ask for foreign-provider
sign-in as the default path. Record the grant and actual execution if that fallback is chosen.
