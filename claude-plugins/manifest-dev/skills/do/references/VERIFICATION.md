# do: building and keeping the verification harness

The harness's parts — the tool, recipes, settings, evidence, statuses, the ask-first mark and the
repository check — are in setup-project's `references/VERIFICATION_HARNESS.md`.

- **Missing harness:** only in a project, as `SKILL.md` defines it. When the context file's
  project-surfaces section names none, look among
  the verification assets the project keeps. Build the harness from what is found, or from
  nothing, scoped to what the change touches: the tool copied from
  `../../setup-project/references/harness/`, settings with `ask-first: ask`, recipes for the
  touched features that delegate to existing assets rather than duplicate them, and the
  repository check. Record it with the verification bullet of the surfaces template in
  `../../setup-project/references/NORTH_STAR_FORMAT.md` → *The project-surfaces section*, in the
  project-surfaces section of the project-level context file the detected host reads, resolved
  per `../../review-code/references/context-file-adherence.md`; create the file or the section,
  holding only that bullet, where it is missing. Build it unattended too: it is verification for
  the change, like a regression test. Name it in the completion report as a new project surface
  the user can remove.
- **Touched recipes:** `verify affected` lists the recipes the change touches and the changed
  paths no recipe covers; an uncovered path a user reaches gets a recipe. Update each touched
  recipe to match the change and run it with the harness, committing its evidence; where its
  proof needs reading, read it and record the verdict with `judge`. Free recipes run as often as
  they help. A recipe marked ask-first runs only with agreement — the project's setting is `run`,
  the user agreed, or the approved Manifest has a gate that runs it; otherwise update it, leave
  it unrun, and name the run it owes in the report. A change to a prompt that leaves its measured eval cases
  unrun marks them `stale`; unmeasured cases stay `unmeasured`.
- **Drift:** when a run fails because the recipe is wrong about the product, repair the recipe
  within scope, and remove its `Drift (…)` line when the repair lands. When a recipe the change does not touch is found drifting, add a dated
  `Drift (YYYY-MM-DD): <what differs>` line to it, and leave the repair to the next run that
  touches it.
- **Unfit harness:** when the work finds the harness not fit to trust for what it touches —
  `../../setup-project/references/VERIFICATION_HARNESS.md` → *Fit to trust* — repair it within
  scope, as for drift, and report the rest as debt.
- **Over its line:** when a check the work touches is over its time line, find where the time
  went from the runner's own timings. Pay it down before the run is done when the time came from
  what the change added — a slow new test, a sleep — or the fix lies in code the change already
  touches. When the fix needs shared code the change does not touch, or a broad refactor, open
  or join one debt Ticket, `verify freeze` the overshoot with it, and report it as debt. Raise
  the line only when the new time is in new tests for new behavior and the existing tests are no
  slower, with that reason in `verify raise` and one line in the pull request. Never weaken a
  check to make it faster.
- **Regressions:** when a run fails because the product is broken, report it as debt with the
  evidence. Never weaken a recipe or a scenario to make it pass.
- **Evidence:** keep the evidence the harness writes, so the completion report can link it for a
  person to open.
