---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/review-pr
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# review-pr

Reviews a pull request and posts high-signal comments in the user's voice under their account — a reviewer fleet, a premise check, thread follow-up — in one batched review per pass.

## How a user reaches it

- `/review-pr [pr-url] [--manifest <path>] [--bundle <urls>] [--loop]`.
- Phrases its description matches: "review this PR", "post a review", "watch this PR".
- No other skill calls it.
- With no Manifest it runs one review-code per relevant dimension, plus review-prompt for prompts; `--manifest <path>` verifies only that Manifest's contract; `--bundle <urls>` and linked pull requests cover coupled changes; `--loop` checkpoints and wakes for later passes, re-judging its own earlier threads against the new code.

## Scenarios

### review
Run: `scripts/drive-skill.sh review-pr verification/prompts/review-pr-review.md --tools`
Proves: one GitHub review whose comments each carry `<!-- manifest-dev:review-pr -->`. No `REQUEST_CHANGES` review; approval only after the user confirmed it.
Check: read
Workload: varies

## Gotchas

- The prompt file carries the placeholder `THROWAWAY_PR_URL`; replace it with a throwaway pull request in a repository the run owns before driving.
- Needs `gh auth status` to succeed in the session.
- Posting is public and does not undo. Never drive it on someone else's pull request to test it.
- A drive through `scripts/drive-skill.sh` runs as you, with whatever GitHub access the driving machine has, so drive it only with a prompt naming a throwaway repository the run owns; where `gh` is not signed in, its GitHub entry points are `unreachable`.
- Manifest mode needs the checkout at the pull request's head.
- Continued Manifest-mode loop wakes pass the applicable checkpoint and reporting scope to each evaluator. A fresh explicit invocation retains its requested independent review scope. This handoff remains unmeasured by a live review drive.
- `tests/test_dist_skill_references.py` checks its markers, Manifest mode and fleet references. No behavior case.
