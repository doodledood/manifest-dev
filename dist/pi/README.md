# manifest-dev for Pi

This is the Pi package target for manifest-dev. It ships the shared, Pi-compatible skills plus a source-owned Pi extension for Harness-level Do entrypoints and structured done/escalate outcomes.

## Install

From this repository checkout:

```bash
pi install .
```

From GitHub:

```bash
pi install git:github.com/doodledood/manifest-dev@main
```

For a project-local install that writes to `.pi/settings.json`:

```bash
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

The extension also registers `manifest_dev_report_outcome`, the structured runtime tool that reports final `done` or `escalate` outcomes. Completion and escalation are runtime outcomes in Pi; they are not exposed as normal skills.

## Runtime Boundary

`/do`, `/done`, and `/escalate` remain intentionally absent from `dist/pi/skills/`:

- `/do` is represented by `/manifest-do`.
- `/done` is represented by `manifest_dev_report_outcome` with `outcome="done"`.
- `/escalate` is represented by `manifest_dev_report_outcome` with `outcome="escalate"` and `blockers[]`.

This landed runtime slice starts and gates the run in Pi, records run/outcome entries with the extension API, and keeps `/auto` plus `/babysit-pr` usable through Pi-aware wrappers. Full deterministic verifier-session fanout, PASS / FAIL / BLOCKED aggregation across independent verifier sessions, and repair-session resumption remain future runtime work.

## Development

`sync-tools` owns the generated skill/docs payload under `dist/pi`. After changing source plugin skills or the Pi conversion reference, regenerate `dist/pi` through `/sync-tools pi` once the generator path exists.

The repo-root `package.json` and `pi/extensions/` are source-owned Pi package surfaces. Do not generate or overwrite them from `sync-tools`.
