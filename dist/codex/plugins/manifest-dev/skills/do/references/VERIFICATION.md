# do: building and keeping the verification surface

The surface's forms and parts — harness, feature map, eval suite,
reader-task list, statuses, repository check — are in setup-project's
`references/VERIFICATION_SURFACE.md`.

- **Missing surface:** build it, scoped to what the change touches — the form the artifact
  needs, existing verification assets adopted rather than duplicated, the harness parts the
  change needs, entries for the touched features, the README and the repository check. Build it
  unattended too: it is verification for the change, like a regression test. Name it in the
  completion report as a new project surface the user can remove.
- **Touched entries:** add a missing entry for a touched path. Update each touched entry to match
  the change, exercise it, and mark it `verified` with the date.
- **Drift:** when an exercise fails because the entry is wrong about the product, repair the
  entry within scope. When an entry the change does not touch is found drifting, mark it `stale`
  with a dated line naming what differs, and leave the repair to the next run that touches it.
- **Regressions:** when an exercise fails because the product is broken, report it as debt with
  the evidence. Never weaken an entry or a journey to make it pass.
- **Evidence:** keep exercise evidence where the harness names it, so the completion report can
  link it for a person to open.
