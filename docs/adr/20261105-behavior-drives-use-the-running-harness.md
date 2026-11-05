# ADR: The host owns general-agent drives with the scenario as the brief

## Status
Accepted

## Area
Verification harness

## Decided by
The user, for general-agent drives, parent grading and the approval-only same-host fallback boundary. An agent implements that contract. Merging remains with the maintainer.

## Context
Behavior verification previously launched Claude CLI sessions. The first native adapter on this branch still special-cased two hosts and injected a target skill body into the subject's prompt. That added a separate execution protocol even though the running host already knew how to start a general agent. Unrecognized hosts could still be sent toward Claude instead of using their own agent capability.

The North Star calls for trusted progress with less unnecessary supervision. Scenario execution should use the host the person already has, while keeping controlled inputs and reviewable evidence. A copied skill being read is distinct from proving native plugin registration.

## Decision
The running host starts a fresh general-purpose agent with the scenario as its brief. The agent may load the supplied skill snapshots and use their scripts. An explicit invocation remains in its scenario; a discovery scenario leaves the choice to the agent. Helpers inject neither a target skill body nor a specialized agent role. Provider names, installed CLIs and environment markers do not select the default execution path.

Helpers retain deterministic work: copy the selected source revision, create an isolated scratch project, apply fixtures, preserve scenario turns and resources, and bind recorded evidence to those inputs. The host dispatches the task and sends later turns to the same general agent. The parent records actual session identity, replies, settings available from the host and artifacts. The subject writes no completion receipt. Expected outcomes stay outside its context, and the parent grades actual behavior. Successful finalization means the records are complete and consistent, not that behavior passed.

Preparation exits 3 until actual completed results exist. Wrong requests, incomplete or failed turns, changed skill companions, changed catalogs and altered briefs cannot pass. Recording remains the parent's trust boundary: input hashes detect mismatches but cannot authenticate an invented caller claim. The host retains its detailed session record and ambient tool capabilities. Context isolation is not an operating-system sandbox or a claim of parity across models.

If the host has no general agents, warn and ask the user what to do. Keep the drive incomplete while that choice is pending. Only an explicit user grant permits a script calling the same host harness as a fallback; never automatically select another provider. The helpers can record the missing capability and reject unapproved or foreign-host fallback evidence. They launch no fallback themselves. The retained Claude CLI instruments have explicit approval and same-host guards, with their existing isolation, resume and cancellation protection. They are not default paths. Other hosts may use an ad-hoc script only after the user's choice.

The distinct Claude-native plugin-eval suite remains its own explicit instrument. General-agent drives do not establish native plugin installation, suite uplift or equal behavior across hosts. Missing cost and hard-limit telemetry remain explicit rather than guessed.

## Alternatives Considered
- **Keep provider-specific default runners:** requires another adapter for each host and preserves the wrong default for unrecognized hosts.
- **Give a general agent only a task in the shared checkout:** loses controlled source versions, scratch fixtures and evidence binding.
- **Preload the target skill into the brief:** changes what the scenario tests and bypasses discovery where discovery is part of the task.
- **Choose a CLI automatically without general agents:** bypasses the owner's fallback decision and can switch providers or require unrelated authentication.
- **Let the subject grade itself or write completion receipts:** confuses a subject's account with the parent's observed result and judgment.
- **Add a persistent broker or universal fallback launcher:** unnecessary when the host owns general agents and an exceptional fallback remains the user's choice.

## Consequences

### Positive
- Every host with general agents uses one drive contract without provider-specific dispatch or another login.
- Scenario briefs avoid injecting skill text and let agents use skills and scripts as resources.
- Controlled inputs, ordered replies and parent judgment remain reviewable.
- A missing capability prompts an explicit decision instead of an automatic provider switch.

### Negative
- A shell alone cannot start the parent host's agent tool; the host must orchestrate dispatch and continuation.
- Context, tool support and observability differ across hosts and require honest reporting.
- A fallback requires the user's attention and may need an ad-hoc same-host script.
- Actual behavior and native plugin registration require separate evidence from helper contract tests.

## Enforced by
partly — `tests/test_native_drive.py` checks the shared path under Claude, Codex, unknown and absent host markers without calling any installed provider; scenario-only briefs; input and catalog integrity; ordered results; and missing-capability/approval/same-host evidence. `tests/test_drive_scripts.py` retains the explicit CLI isolation, resume, source-version and signal-reaping checks, with added approval guards. `verification/recipes/model-drives.md` runs these free fixture contracts; its receipts are not model evidence. `verification/recipes/general-agent-drive.md` exercises real same-agent continuation. Skill and document recipes exercise actual task behavior, with expected outcomes kept by the parent. Runtime behavior on hosts other than the one driven remains unverified.

Actual GPT-6.1 Sol/xhigh general-agent sessions completed the new two-turn scenario, the document-only Manifest walk, PR consolidation and one do before/after pair with plugin baseline 6eac7070. The parent recorded the real replies and finalized every recipe. It verified the exact alpha/beta artifact, retained missing deployment evidence, regraded the identifier-contract Low High, and confirmed that both do arms changed only the fee expression with Manifest/check/label bytes intact. Both do arms passed, so this establishes conformance, not uplift. The do judgments were self-reviewed within their isolated sessions. The do initial brief decreased from 24,687 to 1,045 bytes (23.6 times smaller) by moving skill content into resources; this measures initial brief size, not total tokens, runtime or behavior quality. No live Claude fallback or other host was run from the Codex session.

## Source
- The owner's host-owned general-agent ruling for [PR 420](https://github.com/doodledood/manifest-dev/pull/420), including the missing-agent and approved same-host fallback boundary.
- Related: 20261105-review-severity-follows-consequence and 20261105-repairs-track-the-accepted-promise.
