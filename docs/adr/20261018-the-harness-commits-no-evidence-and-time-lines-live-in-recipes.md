# ADR: The verification harness commits no evidence, and time lines live in recipes

## Status
Accepted — amended by 20261031-time-lines-are-removed-and-run-time-is-only-reported: time lines are removed, so no recipe carries a line and nothing moves one; the harness still commits no evidence and keeps no status

## Area
define / do

## Decided by
The user

## Context
Under 20261014-one-verification-harness-per-project, each scenario run writes a summary into the
harness's evidence directory, and the change commits it. Statuses, staleness and, under
20261015-check-run-time-is-held-by-an-alarm-against-creep, each scenario's time line are worked out
from those files. In use, evidence commits add files and diff noise to every pull request and to
the repository; this repository holds 29 of them. The owner's view: the harness exists to help
agents verify a change and reach confidence, not to keep a ledger. Choosing what to run for a
change needs only the diff and each recipe's `covers` list, which `affected` already reads. Once
20261018-every-pull-request-shows-the-change-working puts the proof in the pull request, committed
summaries repeat it for the reader. The one job only the evidence did was the speed alarm, on
which the North Star's ruling that verification speed binds depends.

## Decision
- The harness commits no evidence. A run still writes its output locally, in the harness's
  evidence directory, which git now ignores, so a failure still explains itself in the run that
  met it.
- Statuses and staleness go. `list` lists recipes, and `affected` picks what a change runs from
  the diff.
- A fixed-workload scenario's time line is a number in its recipe, with the kind of machine it was
  set on. Only a run that already changes that check changes its line: it lowers the line when it
  makes the check faster, raises it with its reason written beside it, or holds it at a frozen
  level that names a debt Ticket. A run on another kind of machine reports its time and does not
  compare. A crossing still counts only after one re-run confirms it, and speed is still never
  bought with proof.
- What every harness owes no longer includes statuses from evidence. One place to learn how to
  verify, ask-first following cost, and the Fit to Trust jobs remain.
- The change ships as a new surfaces version. Its upgrade first moves each timed scenario's
  current line from its latest evidence into its recipe, then removes committed evidence, ignores
  the evidence directory — found through the project's own tool, never assumed — and rewrites
  context-file lines that tell runs to commit evidence.

## Alternatives Considered
- **Keep committed evidence**: gives statuses without a rerun, staleness by fingerprint, and lines
  that move on their own. Its cost lands on every pull request and repository, while `affected`,
  the pull request's proof and the recipe's number serve the jobs that justified it.
- **Move the summaries onto the pull request beside its screenshots**: one home and clean diffs,
  but new machinery in the shipped tool to keep a ledger nobody reads.
- **Keep a small evidence record only for lines**: keeps lines that lower themselves, but keeps
  part of the noise.
- **Drop time lines**: removes the only guard against creep, which
  20261015-check-run-time-is-held-by-an-alarm-against-creep showed watching alone does not stop.

## Consequences

### Positive
- Pull requests and repositories carry no evidence files.
- The shipped tool loses its status and fingerprint machinery.

### Negative
- A line no longer drops on its own after a faster run; a speed gain is kept only when the run
  that makes it records it.
- Two branches that raise the same line meet as a one-line conflict in the recipe, which the
  2026-10-15 design avoided; the run that merges the base in resolves it.
- Nobody can see a recipe's last result without running it.

## Enforced by
partly — `tests/test_verify.py`: `test_a_drive_writes_only_under_an_evidence_directory_git_ignores`
(a drive in a fixture repository leaves nothing to commit),
`test_no_command_reports_or_records_a_status` (`list` and `help` show no status; `judge` is gone),
`test_a_whole_tree_recipe_is_selected_yet_covers_no_path_in_particular`,
`test_no_command_writes_a_recipe_or_the_settings`,
`test_the_upgrade_moves_lines_into_recipes_before_it_removes_evidence`, and
`test_this_repository_tracks_no_evidence` (this repository's evidence directory, read from
`verify --help`, holds no tracked file). Whether an upgrade found the project's own evidence
directory stays judgment.

## Source
- Session: figure-out on running unattended Ticket work with many agents at once (2026-10-18).
- Related: amends 20261014-one-verification-harness-per-project,
  20261015-check-run-time-is-held-by-an-alarm-against-creep,
  20261015-the-shipped-harness-is-a-default-shape-a-project-adapts,
  20261014-setup-project-audits-the-whole-setup-when-run; see also
  20261015-verification-speed-binds-like-cost-second-to-quality,
  20261018-every-pull-request-shows-the-change-working
