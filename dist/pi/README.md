# manifest-dev for Pi

This is the Pi package target for manifest-dev. It ships the shared, Pi-compatible skills plus a source-owned Pi extension for Harness-level Do entrypoints, clean verifier subagent fanout, and structured done/escalate outcomes.

Repository: [doodledood/manifest-dev](https://github.com/doodledood/manifest-dev). Pi's package manager is the installer — there is no `install.sh` for this target.

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

The extension owns Harness-level verification and outcome routing internally:

- When the Executor Session stops after implementation or repair work, the runtime records a clean verification orchestration session under `~/.manifest-dev/verification-sessions/` and spawns one clean `@gotgenes/pi-subagents` verifier subagent session per Acceptance Criterion and Global Invariant, honoring each gate's `verify.agent` (subagent type), `verify.model`, and `phase`. Gates run in ascending-phase batches (serial across phases, parallel within), short-circuiting later phases on FAIL/BLOCKED. Manifest-dev bypasses the community subagents extension's global background-agent queue and enforces its own verifier fanout cap (default 24 per phase), so manifests with 20+ same-phase gates can actually run 20+ clean verifier sessions at once instead of being limited by the subagents package default of 4. When a gate omits `verify.agent` the verifier uses `general-purpose`; when it omits `verify.model` it inherits the Executor Session's current model. Multi-repo manifests (`Repos:`) prepend a repo path map to each verifier prompt.
- FAIL verdicts are injected back into the Executor Session as runtime-authored follow-up repair work. PASS records a runtime done outcome after freshness checks. BLOCKED records and surfaces a resumable blocker. The executor is not asked to call verification or outcome tools.

Completion, escalation, and authoritative verification are runtime outcomes in Pi; they are not exposed as normal skills or executor-callable tools.

### Verifier configuration

Configure the verifier the Pi-native way — CLI flags (`pi.registerFlag` / `pi.getFlag`) with a `MANIFEST_DEV_*` environment-variable fallback. Resolution order is flag > env > default:

| Flag | Env var | Default |
|------|---------|---------|
| `--manifest-verifier-max-turns` | `MANIFEST_DEV_VERIFIER_MAX_TURNS` | `1000` |
| `--manifest-verifier-agent` | `MANIFEST_DEV_VERIFIER_AGENT` | `general-purpose` |
| `--manifest-verifier-timeout-ms` | `MANIFEST_DEV_VERIFIER_TIMEOUT_MS` | `1800000` |
| `--manifest-verifier-max-concurrent` | `MANIFEST_DEV_VERIFIER_MAX_CONCURRENT` | `24` |

A per-gate `verify.agent` / `verify.model` always overrides these defaults. `manifest-verifier-max-concurrent` is manifest-dev's own cap; verifier spawns use `@gotgenes/pi-subagents` with `bypassQueue: true` so this value is not silently reduced by the subagents package's global `maxConcurrent` setting.

## Runtime Boundary

`/do`, `/done`, and `/escalate` remain intentionally absent from `dist/pi/skills/`:

- `/do` is represented by `/manifest-do`.
- `/done` is represented by a runtime-owned done outcome after all verifier gates pass.
- `/escalate` is represented by a runtime-owned blocked/escalation outcome with blocker details.

This runtime slice starts and gates the run in Pi, records run/verification/outcome entries with the extension API, keeps `/auto` plus `/babysit-pr` usable through Pi-aware wrappers (which invoke the installed `/skill:figure-out` and `/skill:define`), records a clean verification orchestration session per attempt, and performs verifier fanout through clean Pi subagent sessions (`inheritContext: false`) that honor each gate's agent/model/phase. The Executor Session prompt stays implementation-focused; runtime lifecycle hooks trigger verification after executor checkpoints and inject failed-gate results back as follow-up work. The done gate is durable (verification state persists to `~/.manifest-dev/runs/<runId>.json` and is rehydrated on reload) and freshness-bound (a stale pass is rejected once the manifest or workspace changes). The remaining future runtime work is optional judge/fork handling for contested verifier reports.

## Development

`sync-tools` owns the generated skill/docs payload under `dist/pi`. After changing source plugin skills or the Pi conversion reference, regenerate `dist/pi` through `/sync-tools pi` once the generator path exists.

The repo-root `package.json` and `pi/extensions/` are source-owned Pi package surfaces. Do not generate or overwrite them from `sync-tools`.
