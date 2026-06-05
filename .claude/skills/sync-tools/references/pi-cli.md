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
| `sendUserMessage` | Runtime extensions can resume or steer an executor session with verifier reports. |
| `appendEntry` / session manager | Runtime can persist run state outside LLM context. |
| `@gotgenes/pi-subagents` service | The current verifier fanout spawns clean Pi subagent sessions with inherited context disabled. |
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
| Reviewer/verifier agents | Use manifest `verify.prompt` blocks to steer clean Pi subagent verifier sessions; do not invent unsupported `pi.agents` manifest fields. |
| Claude hooks | Re-evaluate as Pi lifecycle/command/tool events; do not port hook names mechanically. |
| Slash commands | Prefer `/skill:<name>` for skills and extension commands for runtime actions. |
| CLAUDE.md context | Do not assume a package-level CLAUDE.md equivalent; package docs and skills carry their own context. |
| Installer scripts | Not generated. Pi package manager owns install, update, remove, and project-local scope. |

## Conversion Summary

| Component | Deterministic Output | Notes |
|-----------|----------------------|-------|
| Compatible skills | Copy to `dist/pi/skills/` | Agent Skills are portable. Apply only target-specific handoff substitutions. |
| Harness-level Do | Do not copy as a normal skill | `/do`, `/done`, and `/escalate` are runtime outcomes in Pi. |
| Chain skills | Expose as extension commands when Pi-aware | `/auto` and `/babysit-pr` invoke `/do` in Claude-style hosts; in Pi they map to `/manifest-auto` and `/manifest-babysit-pr`. |
| Agents | Copy as extension-private runtime prompts | Pi packages do not declare an `agents` resource in `package.json`; runtime code may load Markdown prompts from package-local files. |
| Extensions | Include hand-written Pi runtime code | The extension owns commands, executor/verifier orchestration, verdict aggregation, repair routing, escalation, and completion gating. |
| Prompt templates | Generate only intentionally user-invocable templates | Do not expose verifier/reviewer agent prompts as slash prompt templates by accident. |
| README | Generate install and feature-boundary docs | Explain what is generated, what is source-owned, and which commands are available. |

## Package Model

Pi packages bundle extensions, skills, prompt templates, and themes through a `package.json` `pi` key or convention directories. Package installs support npm, git URLs, raw URLs, and local paths. Git and npm installs run `npm install` when a package root has `package.json`.

The repo root owns Pi package metadata so users can install and update manifest-dev like a normal Pi package. `sync-tools` owns generated Pi assets consumed by that package. The generated Pi target is not a standalone replacement for the Pi-native runtime source surface; it is the shared asset payload the package loads.

```
package.json                         # source-owned Pi package metadata
pi/
└── extensions/manifest-dev.ts       # source-owned Pi runtime entrypoints
dist/pi/
├── README.md
├── skills/                      # compatible shared skills
├── runtime/
│   ├── agents/                  # extension-private agent prompts
│   └── prompts/                 # extension-private executor/verifier prompts
├── component-namespaces.json
└── .sync-meta.json
```

Do not silently generate or overwrite a repo-root package manifest from `/sync-tools`; that file is a source surface decision, not a dist artifact. `sync-tools` may update `dist/pi/**`, `dist/pi/.sync-meta.json`, and dist README/metadata.

Current package manifest shape:

```json
{
  "name": "@doodledood/manifest-dev-pi",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./pi/extensions/manifest-dev.ts"],
    "skills": ["./dist/pi/skills"]
  },
  "peerDependencies": {
    "@earendil-works/pi-coding-agent": "*",
    "@gotgenes/pi-subagents": "*",
    "typebox": "*"
  }
}
```

Keep `"extensions": [...]` source-owned. Extension code that imports Pi packages should declare Pi core packages as `peerDependencies` with `"*"` ranges and real runtime dependencies under `dependencies`. `@gotgenes/pi-subagents` is also a Pi package that must be installed/enabled (`pi install npm:@gotgenes/pi-subagents`) so its global service is published before manifest-dev requests verification.

## Skill Handling

Copy these core skills unchanged except for target-specific handoff wording:

- `figure-out`
- `define`
- `figure-out-team`

Copy manifest-dev-tools skills that do not directly invoke `/do` as ordinary skills:

- `adr`
- `handoff`
- `prompt-engineering`
- `review-pr`
- `walk-pr`

Handle these specially:

- `do`: exclude from `dist/pi/skills/`; expose Harness-level Do through the Pi extension.
- `done`: exclude from `dist/pi/skills/`; done is a runtime completion outcome.
- `escalate`: exclude from `dist/pi/skills/`; escalation is a runtime outcome with structured blocker payload.
- `auto`: exclude from `dist/pi/skills/`; expose as `/manifest-auto`, a Pi-aware wrapper that drives figure-out -> define -> Harness-level Do outcome gating.
- `babysit-pr`: exclude from `dist/pi/skills/`; expose as `/manifest-babysit-pr`, a Pi-aware wrapper that synthesizes PR lifecycle grounding and drives Harness-level Do outcome gating.

When adapting `define`, replace user-facing execution handoffs that say `/do <manifest-path>` or `/goal /do <manifest-path>` with `/manifest-do <manifest-path>`.

## Runtime Extension Boundary

The Pi extension owns Do/Verify Loop runtime behavior. The current runtime slice provides:

- `/manifest-do <manifest-path>` command registration
- `/manifest-auto <task>` wrapper command registration
- `/manifest-babysit-pr <github-pr-url>` wrapper command registration
- `manifest_dev_request_verification` as the structured verifier fanout tool
- `manifest_dev_report_outcome` as the structured done/escalate outcome tool
- parse the Manifest and enumerate Acceptance Criteria and Global Invariants
- run clean Pi subagent verifier sessions over every gate with `inheritContext: false`
- aggregate PASS / FAIL / BLOCKED verdicts
- mark done only when every gate returns PASS
- emit structured escalation only for external preconditions or unrecoverable blockers
- run, verification, and outcome persistence through `pi.appendEntry`
- active-session steering through `pi.sendUserMessage`

Remaining target architecture work:

- checkpoint the run boundary with executor session id and yield entry id when available
- persist a fuller state machine across extension reloads
- resume or fork executor sessions under runtime control rather than relying on the active session prompt
- add optional judge/fork handling for contested verifier reports or dubious blockers

Do not claim package-level verifier agent resources until Pi supports them. If runtime extension source is absent, produce a skills-only Pi target with `/do` explicitly unavailable and warnings in the progress log and README.

## Commands

Pi skills already register as `/skill:<name>` commands when skill commands are enabled. Extension commands should be used for native manifest-dev entrypoints:

- `/manifest-do <manifest-path>` for Harness-level Do
- `/manifest-auto <task>` for autonomous figure-out -> define -> Harness-level Do
- `/manifest-babysit-pr <github-pr-url>` for PR lifecycle synthesis -> Harness-level Do
- optional aliases such as `/define` and `/figure-out` only if collision behavior is acceptable

Pi allows multiple extensions to register the same command and disambiguates with numeric suffixes. Generated docs must mention that collisions are possible if aliases are installed.

## Extension and Runtime Affordances

Harness-level Do should use Pi extension/runtime primitives instead of asking the executor model to police itself.

Relevant primitives to account for in implementation docs:

- `pi.registerCommand(name, options)` registers `/manifest-do` and any future aliases.
- `pi.on("resources_discover", ...)` can expose generated skill or prompt paths when static package metadata is not enough.
- `pi.sendUserMessage(..., { deliverAs })` can resume or steer a session after verifier aggregation.
- `pi.appendEntry(customType, data)` can persist run state without putting it in the model context.
- `@gotgenes/pi-subagents` publishes `getSubagentsService()`, whose `spawn(...)` API can launch clean verifier subagent sessions when called with `inheritContext: false`.
- Session APIs and `pi --fork` can preserve executor context while isolating verifier or judge work.
- SDK sessions and `pi --mode json` subprocesses can run verifier fanout deterministically under a supervising runtime.

Do not port Claude Code hook names literally. For Pi, restate the event goal and choose the closest Pi extension/event primitive.

## Prompt and Agent Assets

Pi package manifests expose `prompts`, but manifest-dev verifier/reviewer prompts are runtime assets, not necessarily user-facing prompt templates. Keep them under an extension-private path such as `dist/pi/runtime/agents/` or `dist/pi/runtime/prompts/` until the runtime extension decides how to load them.

Do not add an unsupported `agents` key to `package.json`. If future Pi versions add package-level agents, update this reference with evidence and tests.

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

## Context File Adaptation

Pi reads skills directly and does not have a CLAUDE.md-equivalent distribution contract for package installs. Replace operational references to Claude Code-specific commands or context files only when they would be wrong during Pi execution. Leave comparative or historical text unchanged.

## Session File Adaptation

Pi sessions save under `~/.pi/agent/sessions/` and support `pi --session` and `pi --fork`, but the runtime extension should prefer Pi APIs/session manager access over asking the model to construct session-file paths. Omit Claude JSONL path instructions from generated Pi skills unless the extension supplies an exact Pi session reference.

## Known Uncertainties

- Do not assume git subdirectory package roots. Use repo-root package metadata for git install unless Pi docs/source prove subdirectory package install is supported.
- Do not assume package-level agent resources. Keep agent prompts extension-private until proven otherwise.
- Do not assume package peer dependency installation alone enables another Pi package's extension; document explicit `pi install npm:@gotgenes/pi-subagents`.
- Re-check Pi package and extension APIs before implementing Harness-level Do; this reference should stay evidence-backed rather than aspirational.
