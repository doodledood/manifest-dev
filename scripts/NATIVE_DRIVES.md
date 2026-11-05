# Host-owned general-agent drives

The running host owns behavior drives and document walks. It starts a fresh general-purpose
agent whose brief is the scenario. That agent may load the supplied skill snapshots and call
scripts inside them. No provider name, environment marker or installed CLI selects execution.
The same contract applies to every host that offers general agents; no separate CLI login is
required. The host supplies its ambient tools and instructions, so this is context isolation,
not an operating-system sandbox or a claim of equal results across models.

## Prepare, dispatch and judge

1. Check that the running host can start a fresh general agent with the tools the scenario needs.
   Without that capability, warn and ask the user what to do; follow the fallback boundary below.
2. Run `scripts/verify drive RECIPE SCENARIO --yes` (or `walk`). The helper snapshots plugins
   from the checkout or `DRIVE_PLUGINS_AT`, creates a scratch project outside the checkout,
   applies the fixture, and saves the scenario and resource catalog. It emits `HOST_AGENT_REQUEST`
   and exits 3. Preparation is incomplete evidence, never a completed drive.
3. Read `native-request.json`. Start a fresh general agent without the parent conversation,
   giving it only `worker-prompt.md` and access to the copied resources it names. That brief holds
   the scenario, scratch paths and input boundaries; it injects no skill body or specialized
   agent role. An explicit skill invocation stays in the scenario. A discovery scenario lets the
   agent choose. Keep the recipe's expected outcome outside the agent's context.
4. Deliver later `turns` entries to the same agent, in order. Save its actual terminal replies
   and artifacts and the session identity the host returned. Use the requested `MODEL` and
   `MODEL_REASONING_EFFORT` when supplied; otherwise inherit the session settings and report
   what the host exposes. Do not invent cost, tool support or enforced limits.
5. The parent records each actual reply:
   `python3 scripts/native_drive.py record RUN_DIRECTORY --harness HOST --session-id SESSION_ID
   --model MODEL --reasoning-effort EFFORT --reply-file REPLY_FILE --turn TURN_NUMBER`.
   Use `--status failed` for a failed turn. The subject agent writes no completion receipt.
6. Resume the original recipe with `MANIFEST_DEV_DRIVE_RUN=RUN_DIRECTORY`. Matching input,
   snapshot, catalog, settings and ordered completed turns are required. Changed companions,
   wrong requests and partial/failed results cannot pass. **The parent then grades actual
   artifacts and replies against the recipe.** A completed session is not a behavior verdict.

`RUN_DIRECTORY` is under `MANIFEST_DEV_FEATURES_EVIDENCE` or the local evidence store outside
this checkout. Workflow records go in its `records` directory. The host retains its detailed
session record; local evidence keeps terminal replies, settings, snapshots and artifacts.
Recording is the parent's trust boundary: hashes catch input/result mismatches, not an invented
caller claim about having run an agent. Native plugin registration remains a separate instrument;
reading a copied skill alone does not prove that a host installed or registered the plugin.

Document walks use the same flow with only the task and document snapshots. After reading the
brief, their reader answers from those documents without further tools or a skill catalog.

## Missing general agents and approved fallback

Warn and ask what to do. Keep the drive incomplete while that decision is pending. When a request
has already been prepared, record the missing capability with:
`python3 scripts/native_drive.py unavailable RUN_DIRECTORY --harness HOST --reason REASON`.
This exits 3 and creates no successful result. Never select another provider automatically.

Only an explicit user grant permits a script that calls **that same host harness** as a fallback.
The parent still supplies the controlled scenario, keeps the rubric outside the subject, records
real replies and judges artifacts. After recording the missing capability, include the actual
user grant as `--fallback-approval TEXT` when recording the script's result. A missing grant or
a different harness is rejected. This records approval; it does not obtain approval for the parent.

The retained `scripts/drive-skill-claude.sh` and `scripts/walk-claude.sh` are explicit Claude CLI
instruments, never the default path. After approval on a Claude host, they require
`MANIFEST_DEV_FALLBACK_HARNESS=claude` and `MANIFEST_DEV_FALLBACK_APPROVAL` containing that grant.
They refuse a known foreign host before authentication. Their isolation, resume and stop/reap
checks remain. Another host may need its own ad-hoc script, after the user's choice; no generic
fallback launcher or provider broker is introduced.

The separate Claude-native plugin-eval suite remains its own instrument. Running an individual
general-agent drive does not establish suite uplift, native plugin loading or cross-host parity.
