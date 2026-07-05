# ADR: Own Pi verifier execution with JSON subprocesses

## Status
Superseded by 20260623-use-host-continuation-as-optional-do-backstop

## Context

The now-superseded Pi Harness-level Do runtime verified a Manifest by deterministically parsing Acceptance Criteria and Global Invariants with `verify.prompt` blocks, grouping them by `phase`, and running one clean verifier per gate. The verifier model judged exactly one assigned gate and returned `VERDICT`, `EVIDENCE`, and `DETAILS`; it did not choose which gates existed or which gates should run.

The initial Pi runtime implementation delegated verifier fanout to `@gotgenes/pi-subagents`. That dependency exposed a stale extension-context failure in multi-phase verification: earlier verifier child sessions could leave the published subagents service holding or exposing a stale session-bound context, so later phase spawns failed with Pi's `This extension ctx is stale after session replacement or reload` guard. The observed failure blocked real manifest runs even though earlier phase verifier sessions had spawned and completed successfully.

At the time, the team wanted the verifier selection and execution contract to stay runtime-owned and deterministic, not agent-selected, and wanted to remove `@gotgenes/pi-subagents` from manifest-dev's Pi runtime dependency surface.

## Decision

The superseded decision was to replace `@gotgenes/pi-subagents` in manifest-dev's Pi Harness-level Do verification path with a manifest-dev-owned **JSON subprocess verifier runner**.

The runtime would continue to deterministically extract every AC/INV gate that has a `verify.prompt`, preserve manifest order within each phase, group gates by `phase`, and short-circuit later phases on FAIL or BLOCKED. No agent would decide which verifier prompts to run.

For each gate, manifest-dev would spawn a separate Pi subprocess in JSON mode and send the exact verifier prompt built by `buildGateVerifierPrompt`. JSON mode was the only verifier execution mode in that slice; there was no backend switch or `--mode` configuration surface. The child Pi process would load resources normally so verifier prompts could activate skills and use extension/MCP tools available in the user's Pi environment.

The verifier runner would keep the existing runtime result contract by producing the same minimal record shape the aggregation code needed: id, type/description, status, result text, and error. Existing parsing and aggregation (`parseVerifierReport`, `toGateVerificationResult`, phase status aggregation, wait-pending marker routing, repair injection, and done freshness checks) remained the authoritative post-processing path for that superseded runtime.

The subprocess runner will not add per-verifier transcript persistence in this slice. The existing verification orchestration/run records remain the durable runtime evidence. A timeout mechanism is also deferred; if a verifier hangs, timeout/kill behavior can be added later as a focused runtime hardening change.

Concurrency defaulted to 10 verifier subprocesses per phase chunk, while staying configurable through the manifest verifier concurrency flag/environment-variable path. Gate-level `verify.model` was passed through to the child process when present; otherwise the child verifier used the model from the `/do`/verification parent session. The parent session's current thinking/reasoning level was propagated as well.

The slice removed `@gotgenes/pi-subagents` from manifest-dev Pi package peer dependencies and updated installation/docs/tests so Pi users installed only manifest-dev for that then-current Harness-level Do verification runtime.

## Alternatives Considered

- **Keep `@gotgenes/pi-subagents` and refresh context between phases**: rejected as brittle. Manifest-dev does not own the subagents service's internal session context or global service publication, and a refresh workaround would couple manifest-dev to another extension's internals.
- **Patch `@gotgenes/pi-subagents` upstream only**: useful for that package, but rejected as manifest-dev's primary path because Harness-level Do verification is runtime-critical and only needs a small purpose-built verifier runner, not a general subagent system.
- **In-process SDK verifier sessions**: rejected for the first replacement slice. An in-process no-extension session would avoid stale context but could lose extension/MCP tools needed by real verifier prompts; loading extensions in-process risks returning to shared extension-state problems. A subprocess boundary is simpler and safer.
- **Configurable verifier backend (`pi-subagents`, SDK, JSON, RPC)**: rejected for now as unnecessary complexity. JSON subprocesses are the chosen implementation, and additional backends should be justified by concrete need.
- **Agent-selected verifier orchestration**: rejected because the Manifest is the execution contract. Gate discovery, phase ordering, and skip behavior must remain deterministic runtime behavior.
- **Eager-spawn all phases before waiting for earlier phases**: rejected because it violates phase semantics and wastes slow verifier work when cheap gates fail.
- **Add explicit BLOCKED results for AC/INV headings without `verify.prompt`**: rejected for now. The current `/define` contract emits supported verifier prompts; if the verify schema changes later, the deterministic parser and tests will be updated then.

## Consequences

### Positive

- Removes the stale `pi-subagents` session-context failure class from manifest-dev's verifier fanout.
- Removes an external runtime dependency and its separate install step from Pi usage.
- Keeps verifier selection fully deterministic and auditable from the Manifest.
- Preserves normal Pi resource loading for verifier capabilities while isolating each verifier in its own process.
- Keeps the implementation intentionally small: no backend matrix, no new persistence layer, no timeout subsystem in this slice.

### Negative

- Spawning Pi subprocesses is heavier than in-process subagent spawning; the default concurrency is reduced to 10 to keep this operationally safer.
- Process output parsing becomes manifest-dev-owned code and must be tested against Pi JSON-mode event shapes.
- Without a timeout in the first slice, a stuck verifier can still hang a verification attempt until a later hardening change adds kill behavior.
- Removing the dependency requires synchronized package metadata, README/dist docs, sync-tools references, and tests.
- The previous ADR and docs that described `@gotgenes/pi-subagents` as the verifier fanout mechanism become historical context rather than current implementation detail.

## Source

- Related: `20260605-pi-native-runtime-package-source-surface`.
