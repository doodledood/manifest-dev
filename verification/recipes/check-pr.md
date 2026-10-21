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
- Phrases its description matches: "is this PR ready to merge", "check mergeability", "babysit a PR".
- `run-ticket` before merge; `/do` through a pull-request lifecycle gate (and so `babysit-pr`).
- Steering in the request adds gates, approvers, flaky-check guidance and wait overrides.

## Scenarios

### inspect
Run: `scripts/drive-skill.sh check-pr verification/prompts/check-pr-inspect.md`
Proves: one PASS or FAIL report with a line per gate; the report's mergeability matches GitHub's; no comment, label or merge appeared on the pull request.
Check: read
Workload: varies

## Gotchas

- The prompt file carries the placeholder `THROWAWAY_PR_URL`; replace it with a throwaway pull request the run may read before driving.
- Needs `gh auth status` to succeed in the session and a pull request the run may read.
- Without GitHub access every entry point is `unreachable`.
- A drive through `scripts/drive-skill.sh` runs as you, with whatever GitHub access the driving machine has, so drive it only with a prompt naming a throwaway repository the run owns; where `gh` is not signed in, its GitHub entry points are `unreachable`.
- GitHub's `UNKNOWN` merge state is a wait, not a PASS.
- PASS means mergeable, not authorized to merge.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it. define's pull-request lifecycle task file names it as a gate.
