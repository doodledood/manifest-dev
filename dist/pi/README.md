# manifest-dev for Pi

This is the Pi package target for manifest-dev. It ships the shared, Pi-compatible skills plus a source-owned Pi extension for Harness-level Do entrypoints, clean verifier subagent fanout, and structured done/escalate outcomes.

## Install

From this repository checkout:

```bash
pi install npm:@gotgenes/pi-subagents
pi install .
```

From GitHub:

```bash
pi install npm:@gotgenes/pi-subagents
pi install git:github.com/doodledood/manifest-dev@main
```

For a project-local install that writes to `.pi/settings.json`:

```bash
pi install npm:@gotgenes/pi-subagents
pi install -l git:github.com/doodledood/manifest-dev@main
```

To try the package for one run without adding it to settings:

```bash
pi -e .
```

## Update

Pi owns package updates:

```bash
pi update
```

To update only this package after installing from git with a new pinned ref:

```bash
pi install git:github.com/doodledood/manifest-dev@<ref>
pi update --extensions
```

## Remove

```bash
pi remove git:github.com/doodledood/manifest-dev
```

If installed from a local checkout, remove the same source string that appears in `pi list`.

## Included Skills

Pi exposes installed skills as `/skill:<name>` commands when skill commands are enabled.

- `/skill:figure-out`
- `/skill:define`
- `/skill:figure-out-team`
- `/skill:adr`
- `/skill:handoff`
- `/skill:prompt-engineering`
- `/skill:review-pr`
- `/skill:walk-pr`

## Harness-level Commands

The Pi extension registers native commands for the runtime-owned parts of manifest-dev:

- `/manifest-do <manifest-path>` starts a Harness-level Do run for an existing manifest.
- `/manifest-auto <task>` runs the figure-out -> define -> Harness-level Do lifecycle without approval gates.
- `/manifest-babysit-pr <github-pr-url>` synthesizes PR lifecycle grounding and runs it through Harness-level Do.

The extension also registers two structured runtime tools:

- `manifest_dev_request_verification` parses the manifest and spawns one clean `@gotgenes/pi-subagents` verifier subagent session per Acceptance Criterion and Global Invariant, honoring each gate's `verify.agent` (subagent type), `verify.model`, and `phase`. Gates run in ascending-phase batches (serial across phases, parallel within), short-circuiting later phases on FAIL/BLOCKED. When a gate omits `verify.agent` the verifier uses `general-purpose`; when it omits `verify.model` it inherits the main session's current model. Multi-repo manifests (`Repos:`) prepend a repo path map to each verifier prompt. A BLOCKED verdict is returned to the executor for judgment (it never auto-escalates).
- `manifest_dev_report_outcome` reports final `done` or `escalate` outcomes. `outcome="done"` is rejected until an all-PASS verification still matches the current manifest and workspace (verifications persist to `~/.manifest-dev/runs/<runId>.json` and are rehydrated across reloads). `escalate` surfaces the structured blocker and leaves the run resumable; only `done` ends the run.

Completion and escalation are runtime outcomes in Pi; they are not exposed as normal skills.

### Verifier configuration

Configure the verifier the Pi-native way — CLI flags (`pi.registerFlag` / `pi.getFlag`) with a `MANIFEST_DEV_*` environment-variable fallback. Resolution order is flag > env > default:

| Flag | Env var | Default |
|------|---------|---------|
| `--manifest-verifier-max-turns` | `MANIFEST_DEV_VERIFIER_MAX_TURNS` | `1000` |
| `--manifest-verifier-agent` | `MANIFEST_DEV_VERIFIER_AGENT` | `general-purpose` |
| `--manifest-verifier-timeout-ms` | `MANIFEST_DEV_VERIFIER_TIMEOUT_MS` | `1800000` |

A per-gate `verify.agent` / `verify.model` always overrides these defaults.

## Runtime Boundary

`/do`, `/done`, and `/escalate` remain intentionally absent from `dist/pi/skills/`:

- `/do` is represented by `/manifest-do`.
- `/done` is represented by `manifest_dev_report_outcome` with `outcome="done"`.
- `/escalate` is represented by `manifest_dev_report_outcome` with `outcome="escalate"` and `blockers[]`.

This runtime slice starts and gates the run in Pi, records run/verification/outcome entries with the extension API, keeps `/auto` plus `/babysit-pr` usable through Pi-aware wrappers (which invoke the installed `/skill:figure-out` and `/skill:define`), and performs verifier fanout through clean Pi subagent sessions (`inheritContext: false`) that honor each gate's agent/model/phase. The done gate is durable (verification state persists to `~/.manifest-dev/runs/<runId>.json` and is rehydrated on reload) and freshness-bound (a stale pass is rejected once the manifest or workspace changes). The remaining future runtime work is executor session checkpointing/resume and optional judge/fork handling for contested verifier reports.

## Development

`sync-tools` owns the generated skill/docs payload under `dist/pi`. After changing source plugin skills or the Pi conversion reference, regenerate `dist/pi` through `/sync-tools pi` once the generator path exists.

The repo-root `package.json` and `pi/extensions/` are source-owned Pi package surfaces. Do not generate or overwrite them from `sync-tools`.
