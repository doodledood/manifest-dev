# ADR: Runs build and maintain a verification surface for each artifact that future runs will change

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
Each Manifest designs its own verification, and nothing durable remains after the run. So each run works out again how to exercise the result and observe it. For a runnable product, a durable harness lets every run verify the same way: launch to a usable state, a read-only doctor that says whether an instance is worth driving, drive, debug, evidence, and cleanup that keeps the evidence. A feature map — one entry per user-facing feature, saying how to reach it, how to drive it, what proves it works, and its gotchas — also lets a run understand a vague report, which needs the map to cover the product, not only the parts one change touched.

The need is not limited to code. A prompt or skill is checked by behavior cases run against it; a living document is checked by whether a reader can do the tasks it exists for. In figure-out, the question of how a result will be checked was asked only for code changes, so for other work it first came up when a Manifest's gates were written. A map or suite that nobody maintains goes stale, and a maintenance pass that someone must remember or schedule does not run.

## Decision
- figure-out settles how the result will be checked for any work whose read implies making something, not only code. Its task files carry the domain wording.
- A durable verification surface exists for an artifact that future runs will change. Its form follows the artifact: a harness plus a feature map for a runnable product; a behavior eval suite for prompts, skills, and agents; a list of reader tasks, walked by a reader with fresh context, for a living document. One-shot work is checked in its own run and gets no durable surface.
- For a runnable product the harness is an agent-friendly command-line tool that also sets up the development environment (seed data, test users, configuration) and exposes debugging (traces, profiles, logs), and it carries its own checks.
- The first build of a feature map catalogs the product from its source — routes, commands, menus — with each entry marked unverified. An entry becomes verified when a run drives it, and stale when a run finds it drifting.
- figure-out decides, read-only: does a surface exist, which entries does the change touch, how will each be exercised, are any stale, and is building needed. It may run a throwaway drive to test feasibility.
- define encodes building or repairing the surface as the first Deliverable when it is needed, with gates that exercise the touched entries. A Manifest that touches a mapped entry carries a gate: that entry is updated and exercised live.
- do builds and maintains the surface. When an exercise fails because the surface drifted, the run fixes the surface within scope. A product regression is reported as debt, and a journey is never weakened to make it pass.
- A repository check that entries still reference existing routes, commands, selectors, or cases is part of the surface, so structural drift fails even for contributors who do not use this workflow.
- Unattended runs build a missing surface too, and the completion report lists it as a new project surface the user can remove. A surface for the work at hand is verification code for the change, like a regression test. It is not in the class of handoffs that install or rewire the project's context surfaces, which an unattended run only flags.
- The creation mechanics live in a core init-context reference. init-context can seed the surface when it runs.
- figure-out marks a drifting entry that the current work will not repair: it writes a dated stale line into the entry, naming what differs, the way docs mode lowers a North Star position on evidence. The next run that touches the entry repairs it. This is the one write figure-out makes to the verification surface.
- No scheduled sweep. An entry that no run touches may go stale; the next run that touches it repairs it.

## Alternatives Considered
- **Verification designed per Manifest only**: each run works out the same steps again.
- **A surface for runnable products only**: prompts and living documents keep being checked from scratch, and their verification first comes up at encoding time.
- **Map only the features a change touches**: the map cannot resolve a vague report about a feature no run has touched yet.
- **User-invoked skills to create and maintain the surface**: they depend on memory.
- **A scheduled maintenance pass**: it needs infrastructure the user may not have.
- **A tools-plugin skill**: core can depend on it only when it is installed.
- **Only flag a missing surface in unattended runs**: a project that runs unattended would never get one, and the surface is what lets a user trust output without reading it.

## Consequences

### Positive
- Verification is reused across runs, and the shared launch and doctor steps stay current because every run uses them.
- A run can resolve vague reports against the map.
- How a result will be checked is discussed before encoding for every kind of work.

### Negative
- The first build in a project is heavier, since it catalogs the whole product.
- One more gate on each Manifest that touches a mapped entry.
- Unverified and stale entries can mislead a run that ignores their status.
- The reader-task form for living documents is unproven.
- figure-out gains one more exception to its read-only stance: the stale marker.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20261013-new-capabilities-live-inside-the-four-workflow-entry-points
- Related: 20260809-init-context-skill-lives-in-core
- Related: 20260810-advisory-gates-omit-by-bearer-test
