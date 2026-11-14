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

### consolidation
Run: `scripts/drive-skill.sh review-pr verification/prompts/review-pr-consolidation.md --tools --scaffold verification/fixtures/pr-consolidation`
Proves: a resumed reviewer consolidates the supplied inspections through review-pr-holistic without repeating the fleet or accessing GitHub. In the follow-up packet, R1/R2 become one identifier comment; R3 stays closed on the verified privacy repair, R4 is refuted by the empty-order path, R5 respects the required input order, and R6 is pruned as already covered by the open quantity thread. The waiting packet retains the blocked evaluation and its missing evidence in the cycle summary and cannot become a clean review. In the independent low-consequences packet, the caller's usual Medium+ publication policy filters naming R7 and structural R8 nits; R9 is retained and regraded High or Critical because the identifier conversion violates the binding contract and loses data, despite arriving as Low. In the low-inclusive packet, the caller explicitly includes Low and the full PR scope: R10 remains Low and is retained as a draft comment, without a hidden consolidation cutoff. Each surviving comment retains the existing anchor and voice contract. The transcript shows where consolidation ran; inline consolidation is permitted without suppressing a finding or blocker.
Check: read

### judgment
Run: `scripts/drive-skill.sh review-pr verification/prompts/review-pr-judgment.md --tools --scaffold verification/fixtures/pr-judgment`
Proves: a full no-Manifest review retrieves Shelf's project direction and identifies the supported discovery cost of the requested three-slot promotion. It distinguishes the replay's observable displacement from the uncertain effect on successful discovery. Consolidation retains one concrete recommendation, which can oppose shipping, without converting it into a defect or automatic veto. The authority-only reply does not settle that consequence. The product steward's informed three-slot pilot decision can settle discussion while the reviewer retains an independent recommendation; the summary distinguishes those states and does not imply endorsement from thread closure. The later five-slot change is assessed despite an earlier judgment marker and settled thread. It does not repeat an unchanged argument. All actions are drafts, with no remote posting, automatic approval or request_changes.
Check: read

### judgment-controls
Run: `scripts/drive-skill.sh review-pr verification/prompts/review-pr-judgment-controls.md --tools --scaffold verification/fixtures/pr-judgment-controls`
Proves: the exception snapshot weighs the actual sponsorship rule and accepts its justified use within relevance ties, rather than treating a broad reader-first principle as a veto. The speculation snapshot does not turn an unsupported stale-data-culture prediction into a judgment objection. The missing snapshot names the unavailable project direction and limits its conclusion instead of inventing strategy or treating absence alone as a reason not to ship. The Manifest snapshot verifies the explicit three-slot contract independently while still assessing its discovery consequences: all supplied contract claims can pass alongside an adverse advisory recommendation. Any independently demonstrated implementation defect remains separate. No case posts remotely or auto-approves.
Check: read

## Gotchas

- The prompt file carries the placeholder `THROWAWAY_PR_URL`; replace it with a throwaway pull request in a repository the run owns before driving.
- Needs the running host to expose the GitHub access the scenario requires.
- Posting is public and does not undo. Never drive it on someone else's pull request to test it.
- The general agent has its host's ambient access. Drive remote actions only against a throwaway repository the scenario owns; missing GitHub capability leaves that entry point unreachable. A local snapshot scenario supplies its own state and performs no remote action.
- Manifest mode needs the checkout at the pull request's head.
- Continued Manifest-mode loop wakes pass the applicable checkpoint and reporting scope to each evaluator. A fresh explicit invocation retains its requested independent review scope. This handoff remains unmeasured by a live review drive.
- The reviewer chooses context placement for thread assessments, dimensions, premise checks, consolidation, and Manifest gates. Required results and evidence remain per item; reporting names the actual context used.
- `consolidation` stops before posting and uses only a local snapshot. It does not establish live GitHub transport, the fleet's finding accuracy, or the quality difference between context choices. It is **unmeasured** until driven; the free cold fixture test only checks its inputs and runner wiring.
- `tests/test_dist_skill_references.py` checks its markers, Manifest mode, dimension references, context choice, and complete per-gate results. `tests/test_drive_scripts.py::test_consolidation_fixture_preserves_review_state_and_reproducible_findings` exercises the consolidation scaffold with a CLI stand-in.
- Existing-owner judgment and principles handoff are unmeasured by these scenarios. The owner deferred behavioral drives for this change; source review and property checks cover wiring, not finding accuracy.
