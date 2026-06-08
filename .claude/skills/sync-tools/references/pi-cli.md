# Pi CLI Package Conversion Guide

Reference for generating the Pi target from the Claude Code plugin sources.

## Capability Model

Pi is not only an Agent Skills host. It is a package/runtime host with a TypeScript extension API, package manager, skill discovery, prompt-template resources, session files, forks, and SDK/subprocess orchestration. Treat this target as a package conversion plus runtime composition target.

| Pi Capability | Why manifest-dev cares |
|---------------|------------------------|
| Repo-root package install | A repo-root package install lets users run `pi install git:github.com/doodledood/manifest-dev@ref` and update with Pi's package flow. |
| `package.json` `pi` manifest | Source-owned install contract for shared skills plus source-owned runtime extensions. |
| Agent Skills loading | `figure-out`, `define`, and compatible tools skills can ship as ordinary package skills. |
| `/skill:<name>` commands | Skills do not need generated slash-command shims just to be invocable. |
| `registerCommand` | Harness-level Do should be an extension command, not a copied skill. |
| `resources_discover` | Extensions can contribute generated skill, prompt, and theme paths at runtime if static `package.json` paths are insufficient. |
| `sendUserMessage` | Runtime extensions can inject failed verifier reports back into the Executor Session as follow-up repair work. |
| `appendEntry` / session manager | Runtime can persist run state outside LLM context. |
| `@gotgenes/pi-subagents` service | Verifier fanout spawns clean Pi subagent sessions with inherited context disabled from a runtime-owned verification attempt. |
| Session files and `--fork` | Verification/judge experiments can fork or isolate context instead of mutating the executor turn directly. |
| SDK / JSON-mode subprocesses | Verifier fanout can be implemented by controlled Pi sessions or subprocesses instead of prompt-only delegation. |
| Prompt resources | Verifier, executor, and reviewer prompts may be package-private runtime assets, not user-facing slash prompts. |

## Claude Code Component Mapping

| Claude Code Source | Pi Target |
|--------------------|-----------|
| Skills that do not own runtime state | Package skills under `dist/pi/skills/` or source-owned skill paths. |
| `/do` skill | Excluded. Reimplemented as Harness-level Do extension/runtime behavior. |
| `/done` skill | Excluded. Runtime completion outcome. |
| `/escalate` skill | Excluded. Runtime blocker outcome. |
| `/auto`, `/babysit-pr` | Excluded as ordinary skills. Provided by Pi-aware extension commands that run the lifecycle through Harness-level Do outcome gating. |
| Reviewer/verifier skills | manifest-dev ships no agents; `check-pr`, `poll-slack`, `review-prompt`, and `review-code` ship as ordinary skills under `dist/pi/skills/`. Steer clean Pi subagent verifier sessions via `verify.prompt` (which may activate one of these skills); there is no `verify.agent` field and no `pi.agents` manifest field. |
| Claude hooks | Re-evaluate as Pi lifecycle/command/tool events; do not port hook names mechanically. |
| Slash commands | Prefer `/skill:<name>` for skills and extension commands for runtime actions. |
| CLAUDE.md context | Do not assume a package-level CLAUDE.md equivalent; package docs and skills carry their own context. |
| Installer scripts | Not generated. Pi package manager owns install, update, remove, and project-local scope. |

## Conversion Summary

| Component | Deterministic Output | Notes |
|-----------|----------------------|-------|
| Compatible skills | Copy to `dist/pi/skills/` | Agent Skills are portable. Apply only target-specific handoff substitutions. |
| Harness-level Do | Do not copy as a normal skill | `/do`, `/done`, and `/escalate` are runtime outcomes in Pi. |
| Chain skills | Expose as extension commands when Pi-aware | `/auto` and `/babysit-pr` invoke `/do` in Claude-style hosts; in Pi they are registered as native extension commands of the same name (`/auto`, `/babysit-pr`). |
| Agents | None — manifest-dev ships no agents | The former agents are skills under `dist/pi/skills/`; verification is always a general-purpose subagent activating a skill via `verify.prompt`. |
| Extensions | Include hand-written Pi runtime code | The extension owns commands, executor/verifier orchestration, verdict aggregation, repair routing, escalation, and completion gating. |
| Prompt templates | Generate only intentionally user-invocable templates | Do not expose the runtime verifier prompt as a slash prompt template by accident. |
| README | Generate install and feature-boundary docs | Explain what is generated, what is source-owned, and which commands are available. |

## Package Model

Pi packages bundle extensions, skills, prompt templates, and themes through a `package.json` `pi` key or convention directories. Package installs support npm, git URLs, raw URLs, and local paths. Git and npm installs run `npm install` when a package root has `package.json`.

The repo root owns Pi package metadata so users can install and update manifest-dev like a normal Pi package. `sync-tools` owns generated Pi assets consumed by that package. The generated Pi target is not a standalone replacement for the Pi-native runtime source surface; it is the shared asset payload the package loads.

```
package.json                             # source-owned Pi package metadata
pi/
├── extensions/manifest-dev.ts           # source-owned runtime entrypoint (commands, tools, orchestration)
└── extensions/manifest-dev-runtime.ts   # source-owned pure runtime helpers (unit-tested)
dist/pi/
├── README.md
├── skills/                      # compatible shared skills
├── component-namespaces.json
└── .sync-meta.json
```

The verifier prompt is assembled inline at runtime (no `dist/pi/runtime/` asset directory exists).

Do not silently generate or overwrite a repo-root package manifest from `/sync-tools`; that file is a source surface decision, not a dist artifact. `sync-tools` may update `dist/pi/**`, `dist/pi/.sync-meta.json`, and dist README/metadata.

The Pi runtime ships as **two packages** mirroring the Claude/Codex plugin split:

- **`@doodledood/manifest-dev-pi`** (repo root) — core: registers `/do` and `/auto`, owns the shared Harness-level Do runtime, and exports its wiring (`createRuntimeState`, `registerVerifierFlags`, `wireRuntimeHooks`, `startWrapper`) for the tools package to reuse.
- **`@doodledood/manifest-dev-pi-tools`** (`packages/manifest-dev-pi-tools/`) — registers `/babysit-pr`, depends on the core package, and reuses the core runtime wiring (scoped to babysit-pr runs so it never double-verifies core's runs).

Current core package manifest shape:

```json
{
  "name": "@doodledood/manifest-dev-pi",
  "version": "0.7.0",
  "private": true,
  "type": "module",
  "workspaces": ["packages/*"],
  "keywords": ["pi-package", "manifest-dev", "agent-skills"],
  "exports": {
    "./extension": "./pi/extensions/manifest-dev.ts",
    "./runtime": "./pi/extensions/manifest-dev-runtime.ts"
  },
  "pi": {
    "extensions": ["./pi/extensions/manifest-dev.ts"],
    "skills": ["./dist/pi/skills"]
  },
  "peerDependencies": {
    "@earendil-works/pi-coding-agent": "*",
    "@gotgenes/pi-subagents": "*"
  }
}
```

The tools package declares `"dependencies": { "@doodledood/manifest-dev-pi": "<core version>" }` and its own `pi.extensions`. Keep both `version` fields here in sync with the real `package.json` files (lockstep); bump them when the runtime changes.

Keep `"extensions": [...]` source-owned. Extension code that imports Pi packages should declare Pi core packages as `peerDependencies` with `"*"` ranges and real runtime dependencies under `dependencies`. `@gotgenes/pi-subagents` is also a Pi package that must be installed/enabled (`pi install npm:@gotgenes/pi-subagents`) so its global service is published before manifest-dev requests verification.

## Skill Handling

Copy these core skills unchanged except for target-specific handoff wording:

- `figure-out`
- `define`
- `figure-out-team`
- `check-pr`
- `poll-slack`
- `review-code`

Copy manifest-dev-tools skills that do not directly invoke `/do` as ordinary skills:

- `adr`
- `handoff`
- `prompt-engineering`
- `review-prompt`
- `review-pr`
- `teach-me`
- `walk-pr`

Handle these specially:

- `do`: exclude from `dist/pi/skills/`; expose Harness-level Do through the Pi extension.
- `done`: exclude from `dist/pi/skills/`; done is a runtime completion outcome.
- `escalate`: exclude from `dist/pi/skills/`; escalation is a runtime outcome with structured blocker payload.
- `auto`: exclude from `dist/pi/skills/`; expose as `/auto`, a Pi-aware wrapper that drives figure-out -> define -> Harness-level Do outcome gating.
- `babysit-pr`: exclude from `dist/pi/skills/`; expose as `/babysit-pr`, a Pi-aware wrapper that synthesizes PR lifecycle grounding and drives Harness-level Do outcome gating.

Pi registers `/do` as a native extension command, so `define`'s `/do <manifest-path>` handoff resolves directly — no name substitution needed. Drop the `/goal /do <manifest-path>` unattended-execution line, which has no Pi equivalent.

## Runtime Extension Boundary

The Pi extension owns Do/Verify Loop runtime behavior. The current runtime slice provides:

- `/do`, `/auto`, `/babysit-pr` command registration; the chain wrappers invoke the installed `/skill:figure-out` and `/skill:define` rather than paraphrasing the chain.
- a simplified Executor Session prompt: implement Deliverables, run useful local checks, repair runtime-injected failed AC/INV reports, then stop.
- runtime-owned verification/outcome orchestration rather than LLM-visible verifier/outcome tools in the executor action space, including a clean verification orchestration session record per attempt.
- parse the Manifest and enumerate Acceptance Criteria and Global Invariants, honoring each gate's `verify.model` and `phase`. There is no `verify.agent` field — every gate is verified by a general-purpose subagent whose `verify.prompt` may activate a skill.
- record a clean verification orchestration session under `~/.manifest-dev/verification-sessions/`, then run clean Pi subagent verifier sessions (`inheritContext: false`) in ascending-phase batches — serial across phases, parallel within, short-circuiting later phases on FAIL/BLOCKED. Verifier spawns use `bypassQueue: true` and manifest-dev's own per-phase fanout cap so the community subagents package's default background queue does not silently cap large same-phase verifier sets. Verifiers are always general-purpose; absent `verify.model` -> the Executor Session's current model (`ctx.model`).
- multi-repo grounding: when the Manifest declares `Repos:`, each verifier prompt is prepended with the repo path map.
- aggregate PASS / FAIL / BLOCKED; FAIL verdicts are injected into the Executor Session as runtime-authored follow-up repair work; BLOCKED verdicts record and surface resumable blockers; PASS records done after freshness checks.
- a durable, freshness-bound done gate: each verification is persisted to `~/.manifest-dev/runs/<runId>.json`, rehydrated from runtime state, and `done` is refused unless an all-PASS verification still matches the current manifest SHA and workspace diff.
- resumable escalation: blocker outcomes surface structured blockers and leave the run resumable; only done terminates the run.
- run/verification/outcome persistence through `pi.appendEntry`; active-session repair injection through `pi.sendUserMessage`.

Configuration follows the Pi-native convention (`pi.registerFlag` / `pi.getFlag` with a `MANIFEST_DEV_*` environment-variable fallback; resolution order flag > env > default):

- `--manifest-verifier-max-turns` / `MANIFEST_DEV_VERIFIER_MAX_TURNS` (default 1000)
- `--manifest-verifier-timeout-ms` / `MANIFEST_DEV_VERIFIER_TIMEOUT_MS` (default 1800000)
- `--manifest-verifier-max-concurrent` / `MANIFEST_DEV_VERIFIER_MAX_CONCURRENT` (default 24)

Current runtime boundaries:

- Harness verification and outcome controls must not be registered as normal LLM-visible tools for `/do`.
- The runtime should hide or remove any compatibility scaffolding that would put harness verification/outcome calls in the Executor Session's active tool set.
- Verification attempts must be scoped to the Executor Session id and ignore child/subagent session completion events.

Remaining target architecture work:

- upgrade the lightweight persisted Verification Orchestrator Session record to a fully isolated SDK AgentSession if future verifier orchestration needs LLM reasoning
- optional judge/fork handling for contested verifier reports or dubious blockers

manifest-dev ships no agents, and verifiers are always general-purpose — do not claim package-level verifier agent resources. If runtime extension source is absent, produce a skills-only Pi target with `/do` explicitly unavailable and warnings in the progress log and README.

## Commands

Pi skills already register as `/skill:<name>` commands when skill commands are enabled. Extension commands should be used for native manifest-dev entrypoints:

- `/do <manifest-path>` for Harness-level Do
- `/auto <task>` for autonomous figure-out -> define -> Harness-level Do
- `/babysit-pr <github-pr-url>` for PR lifecycle synthesis -> Harness-level Do
- optional aliases such as `/define` and `/figure-out` only if collision behavior is acceptable

Pi allows multiple extensions to register the same command and disambiguates with numeric suffixes. Generated docs must mention that collisions are possible if aliases are installed.

## Extension and Runtime Affordances

Harness-level Do should use Pi extension/runtime primitives instead of asking the executor model to police itself.

Relevant primitives to account for in implementation docs:

- `pi.registerCommand(name, options)` registers `/do` and any future aliases.
- `pi.on("resources_discover", ...)` can expose generated skill or prompt paths when static package metadata is not enough.
- `pi.sendUserMessage(..., { deliverAs })` can inject verifier FAIL results into the Executor Session after runtime aggregation.
- `pi.appendEntry(customType, data)` can persist run state without putting it in the model context.
- `@gotgenes/pi-subagents` publishes `getSubagentsService()`, whose `spawn(...)` API can launch clean verifier subagent sessions when called with `inheritContext: false`.
- Session APIs and `pi --fork` can preserve executor context while isolating verifier or judge work.
- SDK sessions and `pi --mode json` subprocesses can run verifier fanout deterministically under a supervising runtime.

Do not port Claude Code hook names literally. For Pi, restate the event goal and choose the closest Pi extension/event primitive.

## Prompt and Skill Assets

Pi package manifests expose `prompts`, but manifest-dev's verifier prompt is assembled inline at runtime by `buildGateVerifierPrompt` in `manifest-dev-runtime.ts` (wrapping each gate's verbatim `verify.prompt`). There is no `dist/pi/runtime/agents|prompts` asset directory — do not assume one. The verifier prompt is not exposed as a user-facing prompt template. The former reviewer/verifier agents are skills under `dist/pi/skills/`.

Do not add an unsupported `agents` key to `package.json`; manifest-dev ships no agents. If future Pi versions add package-level agents, update this reference with evidence and tests.

## Namespacing

Pi package resources are scoped by package source, so install-time suffixing is not the default mechanism. Keep original skill names in `dist/pi/skills/` unless the reference is updated with evidence that Pi package installs need explicit suffixes.

Still generate `component-namespaces.json` for cross-target auditability. For Pi, it records source ownership and exclusion decisions rather than driving an installer helper. Use plugin names as ownership values, not install suffixes.

## Installation

Primary repo-root install from a local checkout:

```bash
pi install .
```

Temporary one-run install:

```bash
pi -e .
```

Project-local install:

```bash
pi install -l .
```

Git install from the repository root:

```bash
pi install git:github.com/doodledood/manifest-dev@<ref>
```

Update:

```bash
pi update
pi update --extensions
```

Remove:

```bash
pi remove git:github.com/doodledood/manifest-dev
```

Do not generate `install.sh` for Pi. Pi's package manager is the installer.

## README Requirements

Generated and source READMEs must document:

- repo-root local install
- git install
- project-local install with `-l`
- one-run trial with `pi -e`
- update via `pi update` / `pi update --extensions`
- remove via `pi remove`
- current Harness-level Do command/outcome-tool support and any remaining runtime limitations
- included `/skill:<name>` commands
- required `pi install npm:@gotgenes/pi-subagents` runtime prerequisite for verifier fanout
- verifier configuration flags / env vars and their defaults (max-turns, timeout-ms, max-concurrent)

## Context File Adaptation

Pi reads skills directly and does not have a CLAUDE.md-equivalent distribution contract for package installs. Replace operational references to Claude Code-specific commands or context files only when they would be wrong during Pi execution. Leave comparative or historical text unchanged.

## Session File Adaptation

Pi sessions save under `~/.pi/agent/sessions/` and support `pi --session` and `pi --fork`, but the runtime extension should prefer Pi APIs/session manager access over asking the model to construct session-file paths. Omit Claude JSONL path instructions from generated Pi skills unless the extension supplies an exact Pi session reference.

## Known Uncertainties

- Do not assume git subdirectory package roots. Use repo-root package metadata for git install unless Pi docs/source prove subdirectory package install is supported.
- Do not assume package-level agent resources. manifest-dev ships no agents; the former agents are skills under `dist/pi/skills/`.
- Do not assume package peer dependency installation alone enables another Pi package's extension; document explicit `pi install npm:@gotgenes/pi-subagents`.
- Re-check Pi package and extension APIs before implementing Harness-level Do; this reference should stay evidence-backed rather than aspirational.
