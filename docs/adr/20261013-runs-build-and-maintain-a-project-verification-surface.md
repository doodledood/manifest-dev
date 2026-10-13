# ADR: Runs build and maintain a project verification surface — a harness and a feature map

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
Each Manifest designs its own verification, and nothing durable remains after the run. So each run works out again how to launch the project, drive it, and observe the result. A durable harness lets every run verify the same way: launch to a usable state, a read-only doctor that says whether an instance is worth driving, drive, evidence, and cleanup that keeps the evidence. A feature map — one entry per user-facing feature, saying how to reach it, how to drive it, what proves it works, and its gotchas — also lets a run understand a vague report. A map that nobody maintains goes stale, and a maintenance pass that someone must remember or schedule does not run.

## Decision
- figure-out decides, read-only: does a verification surface exist, which entries does the change touch, how will each be driven, are any stale, and is building needed. It may run a throwaway drive to test feasibility.
- define encodes building or repairing the surface as the first Deliverable when it is needed, scoped to the features the change touches, with gates that drive those entries. A Manifest that touches a mapped user-facing feature carries a gate: that feature's entry is updated and driven live.
- do builds and maintains the surface. When a drive fails because the map or the harness drifted, the run fixes the surface within scope. A product regression is reported as debt, and a journey is never weakened to make it pass.
- A repository check that map entries still reference existing routes, commands, or selectors is part of the surface, so structural drift fails even for contributors who do not use this workflow.
- The creation mechanics live in a core init-context reference. init-context can seed the surface when it runs.
- No scheduled sweep. An entry that no run touches may go stale; the next run that touches it repairs it.

## Alternatives Considered
- **Verification designed per Manifest only**: each run works out the same steps again.
- **User-invoked skills to create and maintain the surface**: they depend on memory.
- **A scheduled maintenance pass**: it needs infrastructure the user may not have.
- **A tools-plugin skill**: core can depend on it only when it is installed.

## Consequences

### Positive
- Verification is reused across runs, and the shared launch and doctor steps stay current because every run uses them.
- A run can resolve vague reports against the map.

### Negative
- The first run in a project without a surface is heavier.
- One more gate on each Manifest that touches a mapped feature.
- Entries that no run touches can go stale.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20261013-new-capabilities-live-inside-the-four-workflow-entry-points
- Related: 20260809-init-context-skill-lives-in-core
