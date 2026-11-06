---
kind: skill
covers: claude-plugins/manifest-dev/skills/check-pr
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# check-pr

Inspects one GitHub pull request — CI, review feedback (threads, review bodies, top-level comments), description sync, mergeability — and returns PASS or FAIL per gate, with the next action for each wait. It never merges and never writes.

## How a user reaches it

- `/check-pr <pr-url | owner/repo#N>`.
- Phrases its description matches: "is this PR ready to merge", "check mergeability".
- `babysit-pr` for its read-only lifecycle check; `run-ticket` before merge; `/do` through a pull-request lifecycle gate.
- Steering in the request adds gates, approvers, flaky-check guidance and wait overrides.

## Scenarios

### inspect
Run: `scripts/drive-skill.sh check-pr verification/prompts/check-pr-inspect.md`
Proves: one PASS or FAIL report with a line per gate; the report's mergeability matches GitHub's; no comment, label or merge appeared on the pull request.
Check: read

### feedback-snapshot
Run: `scripts/drive-skill.sh check-pr verification/prompts/check-pr-feedback-snapshot.md --scaffold verification/fixtures/pr-feedback`
Proves: the inspector reports the current unresolved thread IDs and outstanding required approval, even where a thread repeats an older claim. It reports action targets without judging the claims' validity or composing replies. No outbound action is recorded while the inspector is active. Its verdict remains FAIL; prior dispositions cannot clear current remote state.
Check: read

### item-specific-addressing
Run: `scripts/drive-skill.sh check-pr verification/prompts/acceptance/pr-feedback.md --tools --scaffold verification/fixtures/acceptance-feedback`
Proves: the unrelated logo reply does not address review-9; the item-specific response supplies an addressing signal without proving its substantive correctness. Review-pr's empty publication batch cannot turn the supported export failure into a clean assessment or approval offer. No remote action occurs. This local replay does not establish live hosting transport.
Check: read

## Gotchas

- The prompt file carries the placeholder `THROWAWAY_PR_URL`; replace it with a throwaway pull request the run may read before driving.
- Needs `gh auth status` to succeed in the session and a pull request the run may read.
- The live inspect scenario is unreachable without GitHub access. The feedback-snapshot scenario uses complete local observations instead and does not establish live transport or mutation behavior.
- The general agent has its host's ambient access. Drive remote actions only against a throwaway repository the scenario owns; missing GitHub capability leaves that entry point unreachable. A local snapshot scenario supplies its own state and performs no remote action.
- GitHub's `UNKNOWN` merge state is a wait, not a PASS.
- PASS means mergeable, not authorized to merge.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. The feedback-snapshot drive is unmeasured. define's pull-request lifecycle task file names it as a gate.
