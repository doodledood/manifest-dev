# ADR: Behavior drives use the model harness running the session

## Status
Accepted

## Area
Verification harness

## Decided by
The user, for host-native model access; an agent implements the local request and result boundary under that instruction. Merging remains with the maintainer.

## Context
The repository required the Claude CLI for every skill drive and document walk. In a Codex cloud session the behavior cases stopped at Claude authentication, although the running harness could already start isolated native model contexts. Installing the Claude CLI did not supply sign-in. A standalone Codex CLI probe also failed its own authentication despite reporting a logged-in state.

The North Star calls for trusted progress with less unnecessary supervision. Requiring another provider's login to exercise the current harness's model creates avoidable access and measurement friction.

## Decision
Behavior drives follow the running session: Claude CLI under Claude Code, and the active native model-session capability under Codex cloud. CLI installation does not select a host. A nested Claude session's own marker selects Claude; a standalone shell retains the existing Claude path.

The shell cannot directly call its parent harness's native model tool. Under Codex it therefore prepares copied source, a scratch project and a worker input, then exits 3 with a structured request. This is incomplete evidence. The invoking session dispatches the input through an isolated native context, without its parent conversation or the recipe's rubric, and records the actual terminal reply and native identity. Later user turns continue that same context.

The caller then resumes the same verification recipe. Finalization requires matching request and turn identities, model settings, intact copied entrypoints and companions, intact worker input, and completed results for every turn. Partial, failed or mismatched records cannot pass. The worker neither writes its own receipt nor grades its own behavior. The result is still read against the recipe: a completed model session is not itself a successful behavior verdict.

Native evidence retains the copied inputs, source revision, scratch artifacts, actual replies, session identity and requested model settings. The native host owns its detailed session record and ambient tool catalog. Cost and a hard turn limit are not available through every native capability; summaries state those limits instead of inventing zero cost or an enforced cap. Input isolation is not an operating-system sandbox.

Claude launch, isolation, multi-turn and cancellation behavior remain. The separate Claude-native plugin-eval suite is not translated into a different instrument: its launcher refuses in Codex before asking for foreign sign-in. Individual native drives run there. No cross-host score equivalence or uplift is implied.

## Alternatives Considered
- **Require Claude login in Codex:** contradicts the host-native requirement and adds an unrelated access dependency.
- **Call a separately authenticated Codex CLI:** tests a different credential and runtime path; its failed probe does not negate the active harness's working native model capability.
- **Report preparation as success:** substitutes a file fixture for an actual model session.
- **Let the worker write its own completion receipt:** confuses its account with the invoking harness's observed terminal result.
- **Add a persistent broker:** unnecessary when the invoking session already owns native dispatch and the local files can bind input to result.

## Consequences

### Positive
- Codex cloud can exercise copied skills without any Claude sign-in.
- Both hosts retain observable inputs and outcomes through the same verification recipes.
- Missing native capability remains an explicit failure rather than a silent provider fallback.

### Negative
- Codex drives require the invoking session to dispatch and finalize a local handoff; a shell alone cannot do it.
- Detailed native transcripts, usage and hard limits differ from Claude CLI evidence and must be disclosed.
- Full plugin-eval suites remain tied to their Claude-native instrument.

## Enforced by
partly — `tests/test_native_drive.py` rejects incomplete, mismatched, failed and mutated input/result records and checks host choice without a foreign CLI. `tests/test_drive_scripts.py` retains the Claude path and signal-reaping checks. `verification/recipes/model-drives.md` runs these free contracts. Real native GPT-6.1 Sol/xhigh sessions exercised the review-code and /do pairs and the prompt-review, walkthrough, PR-snapshot, autonomous-inquiry and writing-review controls. Their artifacts and terminal results were read against the recipes; native cost was not reported. The invoking session's truthful recording of its native tool result remains a trust boundary.

## Source
- The owner's instruction to use the running harness for behavior drives in the combined work request for [Issue 356](https://github.com/doodledood/manifest-dev/issues/356) and [Issue 419](https://github.com/doodledood/manifest-dev/issues/419).
- Related: 20261105-review-severity-follows-consequence and 20261105-repairs-track-the-accepted-promise.
