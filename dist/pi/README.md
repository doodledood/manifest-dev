# manifest-dev for Pi

This is the Pi package target for manifest-dev. It currently ships the shared, Pi-compatible skills and the package metadata needed for repo-root install. The deterministic Pi Harness-level Do runtime is not included yet.

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

## Runtime Boundary

The Pi package does not currently install Harness-level Do. That means:

- `/do`, `/done`, and `/escalate` are intentionally absent as normal skills.
- `/auto` and `/babysit-pr` are intentionally absent until Pi-aware wrappers exist.
- `/skill:define` can write a manifest, but executing it with deterministic Pi verification waits for the future Harness-level Do extension.

The future runtime extension owns executor sessions, verifier sessions, PASS / FAIL / BLOCKED aggregation, repair routing, blocker escalation, and completion gating.

## Development

`sync-tools` owns this generated target. After changing source plugin skills or the Pi conversion reference, regenerate `dist/pi` through `/sync-tools pi` once the generator path exists.

The repo-root `package.json` is source-owned package metadata. Do not generate or overwrite it from `sync-tools`.
