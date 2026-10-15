# do: building and keeping the verification harness

What a harness is, what it owes and what shape it takes by default are in
`../../setup-project/references/VERIFICATION_HARNESS.md`; how to use this project's harness is in
its own `--help`.

- **Missing harness:** only in a project, as `SKILL.md` defines it. When the context file's
  project-surfaces section names none, look among the verification assets the project keeps,
  and build one from what is found, or from nothing, scoped to what the change touches, as
  `../../setup-project/references/VERIFICATION_HARNESS.md` → *What setup creates, and what runs build*
  describes. Record it with the verification bullet of the surfaces template in
  `../../setup-project/references/NORTH_STAR_FORMAT.md` → *The project-surfaces section*, in the
  project-surfaces section of the project-level context file the detected host reads, resolved
  per `../../review-code/references/context-file-adherence.md`; create the file or the section,
  holding only that bullet, where it is missing. Build it unattended too: it is verification for
  the change, like a regression test. Name it in the completion report as a new project surface
  the user can remove.
- **Touched recipes:** `verify affected` lists the recipes the change touches and the changed
  paths no recipe covers; an uncovered path a user reaches gets a recipe. Update each touched
  recipe to match the change, run it, and commit its evidence. A recipe marked ask-first runs
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
- **Over its line:** when a check the work touches is over its time line, find where the time
  went from the runner's own timings. Pay it down before the run is done when growth did not earn
  the time — it came from what the change added, such as a slow new test or a sleep — or when the
  fix lies in code the change already touches. When the fix needs shared code the change does not
  touch, or a broad refactor, open or join one debt Ticket, freeze the overshoot with it, and
  report it as debt. Raise the line only when the new time is in new tests for new behavior, the
  existing tests are no slower, and no cheap waste remains, with that reason on the raise and one
  line in the pull request.
- **Never weaken a check** to make it pass or run faster. A run that fails because the product
  is broken is reported as debt with its evidence.
