# ADR: Pi-native runtime package as a source surface

## Status
Accepted

## Context

manifest-dev has treated Claude Code plugin components as the source of truth, with other CLI distributions generated under `dist/`. That model works for prompt and skill assets because Agent Skills are portable and the core methodology can be expressed in shared Markdown.

Pi changes the trade-off for runtime orchestration. Pi packages can bundle skills, prompts, and TypeScript extensions; extensions can register commands and tools, intercept lifecycle and tool events, persist custom session entries, control active tools, and coordinate other Pi sessions through JSON/RPC or the SDK. Those primitives are especially relevant to manifest-dev's `/do` semantics, where correctness depends on stateful enforcement of verifier verdicts rather than on the executor agent's self-assessment.

The user chose a Pi package as a second source surface and clarified the intended boundary: `/figure-out` and `/define` are similar enough to the existing Claude Code behavior that they do not need special Pi-native behavior now. The area that needs attention is the `/do` and verification loop.

## Decision

Create and maintain a **Pi-native runtime package** as a second source surface for deterministic `/do` and verification orchestration.

Shared manifest-dev prompt and skill assets remain sourced from the existing plugin surfaces and may be reused or generated into the Pi package. The Pi-native source surface is for runtime code: run state, manifest parsing, phase ordering, verifier session fanout, verdict aggregation, repair routing, blocker handling, and the done gate.

The Pi runtime package should not fork `/figure-out` or `/define` behavior unless a concrete Pi-specific gap appears. Those remain shared prompt and skill behavior.

The package should be installable from the repository root, so users can install and update it like a normal Pi package. A repo-root package manifest is source-owned package metadata, while generated `dist/pi` assets are produced by `sync-tools` and consumed by that package. README surfaces must document install, update, local-development, and removal flows wherever the repo documents multi-CLI distribution.

The `sync-tools` Pi reference should be a capability model, not only a file mapping table: it must document how Claude Code plugin concepts map to Pi package resources and which Pi-only affordances matter for manifest-dev, including extension commands, resource discovery, package install/update, prompt resources, sessions/forks, and SDK or subprocess orchestration.

Initial implementation landed the runtime entrypoint slice first: `/manifest-do` starts Harness-level Do for an existing manifest, `/manifest-auto` and `/manifest-babysit-pr` replace the omitted portable wrapper skills, and `manifest_dev_report_outcome` records final `done` or `escalate` outcomes.

The next slice adds `manifest_dev_request_verification`: when the executor believes implementation is ready, it calls this tool with the manifest path and run id. The extension parses Acceptance Criteria and Global Invariants, spawns one clean Pi subagent verifier session per gate through `@gotgenes/pi-subagents` with inherited context disabled, aggregates PASS / FAIL / BLOCKED reports, persists the verification entry, and rejects `outcome="done"` unless the latest verification for that run is all PASS.

Repair-session resumption remains executor-mediated for now: failed verification returns a report to the active executor, which repairs and calls verification again. A fuller persisted state machine, executor checkpointing, and optional judge/fork handling for contested verifier reports remain future runtime work.

## Alternatives Considered

- **Generated Pi distribution only**: rejected because it would port the prompt surface without using Pi's strongest affordance, deterministic extension code. The `/do` completeness contract would remain mostly prompt discipline.
- **Full Pi-native fork of the methodology**: rejected because it would duplicate `/figure-out` and `/define` without a known behavioral gap, increasing drift risk for little benefit.
- **External orchestrator outside a Pi package**: rejected for now because Pi packages are the native composition unit for extensions, skills, prompts, and project-local installability.

## Consequences

### Positive

- The `/do` completion invariant can be enforced by code: no done state until every Acceptance Criterion and Global Invariant verifies PASS.
- Executor and verifier sessions can be isolated while a deterministic parent owns authority over verdict aggregation and repair routing.
- Shared prompts and skills avoid unnecessary fork drift, while Pi-specific runtime code can use Pi's extension and session primitives directly.
- The architecture matches the user's intent: no special Pi behavior for `/figure-out` and `/define`; focus engineering effort on the Do/Verify Loop.

### Negative

- manifest-dev now has a second maintained source surface, so sync boundaries must be explicit and tested.
- The repo root will gain package metadata for Pi install/update, which must be maintained deliberately rather than regenerated as anonymous `dist` output.
- Pi package implementation will need its own tests and release path, not just `sync-tools` output checks.
- README and distribution docs must stay synchronized so Pi has the same easy upgrade story as the other plugin targets.
- Runtime semantics can drift from Claude/Codex `/do` if shared invariants are not represented as tests or conformance fixtures.
- The Pi target reference will carry more implementation knowledge than simpler generated targets, so it must be kept evidence-backed and updated when Pi package/runtime APIs change.
- The current verifier fanout depends on `@gotgenes/pi-subagents` being installed and enabled in Pi; package peer dependency alone does not publish the service.
- Repair routing is still prompt-mediated through the active executor session rather than a fully persisted runtime state machine.

## Source

- Session: `manifest-dev:figure-out --logs --with-docs`, 2026-06-05.
- Log: `~/.manifest-dev/logs/figure-out-log-20260605-071040.md`
- Related: `20260531-codex-plugin-native-distribution`
