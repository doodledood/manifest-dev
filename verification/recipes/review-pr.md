---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/review-pr, claude-plugins/manifest-dev-tools/skills/review-pr-holistic, claude-plugins/manifest-dev-tools/skills/review-pr-judgment, claude-plugins/manifest-dev-tools/skills/review-pr-thread-verify
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

### consolidation
Run: `scripts/drive-skill.sh review-pr verification/prompts/review-pr-consolidation.md --tools --scaffold verification/fixtures/pr-consolidation`
Proves: a resumed reviewer consolidates the supplied inspections through review-pr-holistic without repeating the fleet or accessing GitHub. In the follow-up packet, R1/R2 become one identifier comment; R3 stays closed on the verified privacy repair, R4 is refuted by the empty-order path, R5 respects the required input order, and R6 is pruned as already covered by the open quantity thread. The waiting packet retains the blocked evaluation and its missing evidence in the cycle summary and cannot become a clean review. Each surviving comment retains the existing anchor and voice contract. The transcript shows where consolidation ran; inline consolidation is permitted without suppressing a finding or blocker.
Check: read
Workload: varies

## Gotchas

- The prompt file carries the placeholder `THROWAWAY_PR_URL`; replace it with a throwaway pull request in a repository the run owns before driving.
- Needs `gh auth status` to succeed in the session.
- Posting is public and does not undo. Never drive it on someone else's pull request to test it.
- A drive through `scripts/drive-skill.sh` runs as you, with whatever GitHub access the driving machine has, so drive it only with a prompt naming a throwaway repository the run owns; where `gh` is not signed in, its GitHub entry points are `unreachable`.
- Manifest mode needs the checkout at the pull request's head.
- Continued Manifest-mode loop wakes pass the applicable checkpoint and reporting scope to each evaluator. A fresh explicit invocation retains its requested independent review scope. This handoff remains unmeasured by a live review drive.
- The reviewer chooses context placement for thread assessments, dimensions, premise checks, consolidation, and Manifest gates. Required results and evidence remain per item; reporting names the actual context used.
- `consolidation` stops before posting and uses only a local snapshot. It does not establish live GitHub transport, the fleet's finding accuracy, or the quality difference between context choices. It is **unmeasured** until driven; the free cold fixture test only checks its inputs and runner wiring.
- `tests/test_dist_skill_references.py` checks its markers, Manifest mode, dimension references, context choice, and complete per-gate results. `tests/test_drive_scripts.py::test_consolidation_fixture_preserves_review_state_and_reproducible_findings` exercises the consolidation scaffold with a CLI stand-in.
