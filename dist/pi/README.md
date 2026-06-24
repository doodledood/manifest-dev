# manifest-dev for Pi

This is the Pi package target for manifest-dev. It ships the portable manifest-dev skills plus prompt-template aliases for the main entrypoints. There is no manifest-dev TypeScript extension in this target: `/do` follows the same main-agent verifier protocol used on the other skill-based hosts, and host goal/continuation support is an optional outer backstop.

Repository: [doodledood/manifest-dev](https://github.com/doodledood/manifest-dev). Pi's package manager is the installer — there is no `install.sh` for this target.

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
- `/skill:do`
- `/skill:done`
- `/skill:escalate`
- `/skill:auto`
- `/skill:figure-out-team`
- `/skill:check-pr`
- `/skill:poll-slack`
- `/skill:review-code`
- `/skill:babysit-pr`
- `/skill:adr`
- `/skill:handoff`
- `/skill:prompt-engineering`
- `/skill:review-prompt`
- `/skill:review-pr`
- `/skill:teach-me`
- `/skill:walk-pr`

## Slash Aliases

The package also ships prompt-template aliases for the common entrypoints:

- `/do <manifest-path>` expands to the `do` skill.
- `/auto <task>` expands to the `auto` skill.
- `/babysit-pr <github-pr-url> [--ci] [--manifest <path>] [--log [path]]` expands to the `babysit-pr` skill.

The aliases are convenience templates. The skills own behavior.

## Execution and Verification

`/do` is prompt-level in Pi, matching the portable manifest-dev workflow:

1. The main agent reads the Manifest and treats it as the acceptance contract.
2. It implements Deliverables.
3. It enumerates every Acceptance Criterion and Global Invariant with a `verify.prompt`.
4. It launches an independent verifier execution for each gate using that prompt verbatim.
5. It repairs FAILs and reruns the affected verifier.
6. It reports genuine BLOCKED gates with the missing external input or state.
7. It calls `done` only after every gate has fresh PASS evidence in a manifest gate ledger.

Pi does **not** include a package-owned verifier scheduler, verdict aggregator, done gate, or verifier concurrency flag. The trust mechanism is still independent verifier execution per Manifest gate; the orchestration is the normal `/do` skill protocol.

## Optional Host Continuation

For unattended work, use a host goal-setting or continuation capability when available. For `/do`, the goal should say that the run is complete only after every Manifest AC/GI is listed in a gate ledger with fresh independent verifier PASS evidence, FAILs have been repaired and reverified, blockers are genuine, and no required verification is missing or stale. For `/auto`, use one full-chain parent goal whose terminal condition is manifest written plus `/do` gate-ledger PASS; when figure-out runs first, its full autonomous Read anatomy is a checkpoint before `/define`. It should also say that unverified, FAIL, stale after a relevant change, BLOCKED/actionable, or escalation-pending gates are non-terminal. Do not accept self-attestation, "looks done", or a summary claim in place of verifier output.

One Pi-compatible continuation provider is the [`goal-controller` package in doodledood/pi-plugins](https://github.com/doodledood/pi-plugins/tree/main/packages/extensions/goal-controller). Install it using that package's instructions and Pi's normal package install flow.

The continuation provider is optional. Without one, `/do`, `/auto`, and `/babysit-pr` still run, but Pi will not automatically reopen turns if the model stops before the contract is complete.

## Development

`sync-tools` owns the generated skill/docs payload under `dist/pi`. After changing source plugin skills or the Pi conversion reference, regenerate or hand-align `dist/pi` according to `.claude/skills/sync-tools/references/pi-cli.md`.

The repo-root `package.json` is source-owned Pi package metadata. `dist/pi/skills`, `dist/pi/prompts`, `dist/pi/component-namespaces.json`, and this README are generated/distribution assets.
