# ADR: every figure-out probe has an eval grader or a stated reason

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context

figure-out's behaviour comes from three places: its `SKILL.md`, the task files under `tasks/` (each a list of bold-labelled blind-spot probes and a few forced trade-offs), and the references it loads by mode. The behaviour suite under `claude-plugins/manifest-dev/evals/` had grown one case at a time, each written for whatever angle a change of the day added. Nothing tied the suite to the prompt it measured. When the decision probes arrived (20261019-figure-out-probes-decisions-and-plans-under-uncertain-futures), a read of every grader against every probe found that most of the task files' probes, and all thirteen decision probes, had no grader at all. The suite would have run, reported a number, and said nothing about them. Its README's *Known limits* listed some of the gaps by hand, and that list had already drifted from the cases on disk.

## Decision

- **A coverage table in the eval README maps every unit to the graders that judge it, or to a reason the suite cannot.** A unit is each probe label and each forced trade-off line in every figure-out task file, each file in `figure-out/references/`, and each paragraph and bullet of `SKILL.md`'s body. A reason is accepted only when the unit needs a service the suite cannot reach, several sessions, many user turns, a host capability the headless harness lacks, or a skill outside the copied plugin; anything else gets a case.
- **A property test fails when the table is out of step.** It reads the task files and the references directory as data and fails on a unit with no row, a row for a unit that no longer exists, a duplicate row, a row naming a case or grader that is not on disk, a row whose only graders are display-only, and a reason too short to check. `SKILL.md` rows are written by hand and are not derived, because a paragraph has no stable label to key on.
- **The gaps close with new grouped cases.** Probes that co-apply share one scenario, each with its own grader, numbered from 61. Each runs with and without the plugin like every other case.
- **A probe whose case passes in both arms is not retired silently.** Its row records that the base model covers the angle, which marks the probe as a candidate to cut from the task file, instead of the case being deleted and the probe left unmeasured.

## Alternatives Considered

- **Cover only the decision probes**: Rejected by the user — "every important part" of figure-out belongs in the suite.
- **Keep the hand-written *Known limits* list**: Rejected — it had already drifted from the cases on disk, and nothing failed when it did.
- **Pack several probes into one grader to hold cost down**: Rejected — a grader that judges two angles cannot say which one failed, and a both-arm pass on it hides which probe is redundant. The user accepted a full first run of about $220–230 instead.
- **Two tiers, a cheap core run and a full run**: Not taken — the suite has not had its first full run, so there is no data yet on which cases earn the core.
- **Derive `SKILL.md` units automatically**: Rejected — paragraphs reflow and have no label, so a derived key would break on every edit; the rows are kept by hand and reviewed with the change that edits the paragraph.

## Consequences

### Positive
- A probe added to a task file without a case fails the property suite the same day, instead of shipping unmeasured.
- The first full run will show, probe by probe, which angles the plugin draws out and which the base model already raises, so a task file can shrink on evidence.

### Negative
- A full first run of both figure-out suites now costs about $214 at the README's per-run bound, against $120 before.
- The table is long and every task-file edit touches it. A probe rename means a row rename.
- The test checks that a named grader exists, not that it judges the unit it is listed against; that stays review.

## Enforced by
partly — `tests/test_figure_out_coverage.py` fails on a probe, trade-off line or reference file with no row, a stale or duplicate row, a row naming a case or grader not on disk, a row with only display-only graders, and an empty reason. Whether a grader judges the unit it is listed for, and the `SKILL.md` rows, stay review.

## Source
- Session: a figure-out session on whether the eval suite covers what figure-out does (2026-10-20), followed by an autonomous run that built the table, the test and the cases.
- Related: 20261019-figure-out-probes-decisions-and-plans-under-uncertain-futures, 20261020-figure-out-decision-probes-read-other-parties-name-the-flip-chance-and-look-for-unnamed-aims
