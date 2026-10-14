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
- **Touched recipes:** add a missing recipe for a touched path. Update each touched recipe to
  match the change and run it with the harness, committing its evidence; where its proof needs
  reading, read it and record the verdict with `judge`. A recipe marked ask-first runs only where
  the project's setting is `run` or the user agreed; otherwise update it, leave it unrun, and
  name the run it owes in the report. A change to a prompt that leaves its measured eval cases
  unrun marks them `stale`; unmeasured cases stay `unmeasured`.
- **Drift:** when a run fails because the recipe is wrong about the product, repair the recipe
  within scope, and remove its `Drift (…)` line when the repair lands. When a recipe the change does not touch is found drifting, add a dated
  `Drift (YYYY-MM-DD): <what differs>` line to it, and leave the repair to the next run that
  touches it.
- **Unfit harness:** when the work finds the harness not fit to trust for what it touches —
  `../../setup-project/references/VERIFICATION_HARNESS.md` → *Fit to trust* — repair it within
  scope, as for drift, and report the rest as debt.
- **Regressions:** when a run fails because the product is broken, report it as debt with the
  evidence. Never weaken a recipe or a scenario to make it pass.
- **Evidence:** keep the evidence the harness writes, so the completion report can link it for a
  person to open.
