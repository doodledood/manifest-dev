# ADR: The feature map is a navigation contract over whatever users invoke, with a fixed shape and a proof run

## Status
Superseded by 20261014-one-verification-harness-per-project

## Area
define / do

## Decided by
The user

## Context
20261013-runs-build-and-maintain-a-project-verification-surface gave a feature map only to runnable products, described its entries in four loose bullets, and let setup hand over a map nobody had driven. The map's main job is to let a run go straight to the right place — place a vague report, then reach and drive the feature — and that job exists for any artifact people invoke, a plugin's skills included. Loose entries came out in a different shape each time, and an undriven map reads as proof it is not. pstack's create-verification-skill (`github.com/cursor/plugins`, `pstack/skills/create-verification-skill/`) shows a working shape: an index carrying preconditions, conventions and proof rules, one file per feature with fixed sections, a worked example, and one end-to-end run before handover.

## Decision
- A project whose artifact people invoke — routes, commands, public calls, skills — keeps one feature map over it, beside whichever verification forms it keeps. The forms check; the map navigates, and each entry names the check that holds it.
- The map describes the artifact from the user's side only. Where in the code a feature lives is read from the code at run time.
- The map is an index plus one file per feature, in the shape setup-project's `references/VERIFICATION_SURFACE.md` defines, with a worked example beside it. Statuses gain `unreachable`, naming the missing prerequisite, and an entry point is never reported verified because another one worked.
- Setup drives one entry end to end where existing assets reach, or says which entry it could not drive and why; it builds nothing more to get there.
- An existing verification surface is judged fit to trust by its jobs — a cold proof run, a health check, isolation, the real path exercised — not by its tooling, and only for the paths a run's work touches. A surface the work touches that is not fit is repaired as part of that work; nothing is built ahead of need.

## Alternatives Considered
- **A map only for runnable products**: leaves a skills plugin with nowhere to place a report, though its users invoke it the same way.
- **One map file with a section per feature**: harder to point a run at one feature, and harder for a check to keep each entry's shape.
- **Seed only the top few features, as pstack does**: the map could not place a report about a feature no run has touched; breadth is why the first build catalogs everything.
- **Code locations in each entry**: the first thing to go stale.

## Consequences

### Positive
- A run can go from a vague report to a driven feature without re-deriving entry points.
- Maps come out in one shape a check can hold.

### Negative
- One more surface to keep current in projects that only had an eval suite.
- Map entries that restate a description add upkeep without guiding anyone; the shape asks entries to carry only what the description does not.

## Enforced by
partly — `tests/test_feature_map.py` holds this repository's map: every user-invocable skill has an entry, each entry has the shape and a status, and every path it names exists. `tests/test_setup_project_versions.py` (`test_latest_version_matches_what_setup_project_emits`) fails when the emitted surface README changes without a new surfaces version. Whether an entry carries more than its description, and whether a project's map covers what users invoke, stays judgment.

## Source
- Session: investigation of setup-project's update behavior and of pstack's feature map.
- Narrows: 20261013-runs-build-and-maintain-a-project-verification-surface
- Related: 20261014-setup-project-audits-the-whole-setup-when-run
