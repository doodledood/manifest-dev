# ADR: Time lines are removed, and a check's run time is only reported

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
Under 20261015-check-run-time-is-held-by-an-alarm-against-creep, as amended by
20261018-the-harness-commits-no-evidence-and-time-lines-live-in-recipes, every fixed-workload
scenario carries a time line in its recipe: `Line: <seconds> s on <kind of machine>`, with
headroom for noise. When two runs in a row cross it, `verify drive` exits 5, and the run that met
it must pay the time down, raise the line with a written reason (which a project may reserve to a
person), or freeze the overshoot under a debt Ticket. A *fast enough* job in *Fit to trust*, added
by 20261015-runs-keep-the-harness-fit-for-speed-control-and-diagnosis, made a touched check over
its line a reason the check could not be trusted.

The purpose was to keep the harness from becoming the bottleneck, which
20261015-verification-speed-binds-like-cost-second-to-quality asks of it. In use the lines did the
opposite: a check run on a busier machine, or a suite that grew by a few honest tests, crossed its
line, and real work stopped to argue about seconds, wrote reasons for raises nobody read, and
opened debt Tickets about noise. The alarm cost more attention than the creep it caught.

## Decision
- Time lines are removed, not made warning-only. The tool has no `line`, `raise` or `freeze`
  command and no exit 5; a passing drive exits 0 however long it took, and runs each scenario
  once. Recipes carry no `Line:` or `Workload:` field and the settings no `headroom:` or `raise:`;
  the tool refuses a leftover one, naming it, so it cannot read as live.
- One advisory principle takes their place, stated once in the shipped harness guidance
  (`VERIFICATION_HARNESS.md` → *Run time*) and pointed to wherever runs met lines: every run
  reports how long it took, and that is the only time signal. Keep checks fast and treat a slow
  harness as friction to fix; never block, gate, fail, ticket or exit non-zero on run time, and
  never make a check faster by having it check less. A slow check a run cannot speed up is named
  in its report, never listed as debt.
- *Fit to trust* loses its *fast enough* job. Run time alone is still not a reason for the
  ask-first mark.
- The removal ships as surfaces v12. Its upgrade offers one item for a kept harness — the tool
  update, every recipe's `Line:` and `Workload:` fields, the two settings, and text about lines —
  done when the project's `verify check` passes, and it replaces the time-line items of the v4 and
  v6 upgrade guides, so a project updating from any earlier version never writes a line on the way.

## Alternatives Considered
- **Warning-only lines**: keep the number and print a warning instead of exiting 5 — a warning
  every run learns to ignore is noise with upkeep, and the line, its headroom and its raises
  would still need maintaining.
- **Keep the lines with more headroom**: fewer false crossings, but the same machinery and the
  same stops when one comes.

## Consequences

### Positive
- No run stops, fails or opens a Ticket over timing noise.
- The tool, the recipes and the guidance lose a whole mechanism: three commands, two settings,
  two recipe fields, a confirming re-run and the rules for moving a number.

### Negative
- A check that slowly gets slower is caught only by the durations runs report and the people
  and agents reading them; nothing compares a run with the last one.

## Enforced by
`tests/test_verify.py`: `test_a_passing_drive_exits_0_however_long_it_took_and_runs_once`,
`test_the_removed_line_commands_are_unknown`, `test_help_names_no_time_line_and_no_exit_5`,
`test_a_leftover_scenario_field_fails_check_naming_it`,
`test_a_leftover_setting_fails_check_naming_it`, and
`test_the_shipped_example_harness_carries_no_removed_field`;
`tests/test_upgrade_removes_time_lines.py`, which runs the v11 setup case's scaffold, applies the
removals `upgrades/v11-to-current.md` names, and finds no time line left. Whether a run noticed a
slow check and named it stays judgment.

## Source
- Session: an owner ruling, executed unattended (2026-10-31).
- Related: supersedes 20261015-check-run-time-is-held-by-an-alarm-against-creep; amends
  20261018-the-harness-commits-no-evidence-and-time-lines-live-in-recipes and
  20261015-runs-keep-the-harness-fit-for-speed-control-and-diagnosis; see also
  20261015-verification-speed-binds-like-cost-second-to-quality
