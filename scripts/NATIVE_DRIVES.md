# Behavior drives in the running harness

Behavior drives use the model interface of the session that runs them. Under Claude Code,
`scripts/drive-skill.sh` and `scripts/walk.sh` use the Claude CLI. Under Codex cloud, they use
an isolated model context from the active Codex harness. Installing another provider's CLI
never changes this choice. Codex cloud requires neither Claude nor a separate Codex CLI login.
A standalone shell keeps the existing Claude path.

## Drive a skill under Codex cloud

Run the normal `scripts/verify drive RECIPE SCENARIO --yes` command. `MODEL` and
`MODEL_REASONING_EFFORT`, when set, travel with the request; otherwise the native context
inherits the running session's settings. `DRIVE_PLUGINS_AT` selects a committed before arm.

The shell prepares copied skills, a scratch project and a worker input, then emits
`NATIVE_SESSION_REQUEST` and exits 3. This is an incomplete handoff, not a completed drive.
The invoking session performs the following steps through its own native model capability:

1. Read `native-request.json`. Start an isolated context without the parent conversation,
   using the requested model and effort, and give it only `worker-prompt.md`. That input contains
   the target skill verbatim, paths into the copied catalog, the scenario and its scratch paths.
   Keep the recipe's expected outcome outside the worker's context.
2. Let the worker finish. For a request with several user turns, continue the same native
   context with each later `turns` entry, in order. Preserve the actual terminal replies and
   the native session identity returned by the host. The worker does not grade itself or write
   the completion receipt.
3. Save each actual reply to a file. Record it with the command the request prints:
   `python3 scripts/native_drive.py record RUN_DIRECTORY --session-id SESSION_ID --model MODEL
   --reasoning-effort EFFORT --reply-file REPLY_FILE --turn TURN_NUMBER`. Record a failed native
   turn with `--status failed`; never turn it into successful evidence.
4. Rerun the original verification recipe with `MANIFEST_DEV_NATIVE_RUN=RUN_DIRECTORY`.
   The driver verifies the request, source snapshot, worker input, native identity, settings and
   every turn before recording completion. A prepared, altered, mismatched, partial or failed
   result cannot pass.
5. Read the actual reply and scratch artifacts against the recipe. A completed drive establishes
   that a real session ran; it does not establish that the behavior passed its rubric.

`RUN_DIRECTORY` is outside the checkout, under `MANIFEST_DEV_FEATURES_EVIDENCE` or the existing
local evidence store. The request prints its exact path. Workflow records live under its
`records` directory; the worker must not read personal workflow records or installed skill copies.
The native host still supplies its ambient tools and system instructions. This is input isolation,
not an operating-system sandbox. The raw terminal replies are saved locally; the native host owns
its detailed session record. Native usage cost and a hard turn limit are not available through
all hosts, so the summary states those limits rather than reporting zero cost or an enforced cap.

## Walk documents

`scripts/verify walk RECIPE SCENARIO --yes` uses the same native handoff. Its worker receives
only the reader task and document snapshots, with no plugin catalog. After opening its input,
it answers from those documents without further tools.

## Missing capabilities and suites

A shell cannot invoke its parent's native model tool. If the running session has no isolated
model capability, the request remains incomplete and the caller reports the missing capability.
Do not replace it with a fabricated receipt, a stand-in, or another provider's sign-in.

The existing `claude plugin eval` suites are a distinct Claude-native measurement instrument.
Run them under Claude Code. In Codex cloud their launcher refuses before sign-in; individual
native skill drives are available there. No native suite result or uplift is implied by a skill drive.
