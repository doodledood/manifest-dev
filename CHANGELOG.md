# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project follows semantic versioning for released packages.

Add new entries under `## [Unreleased]` using these sections, in this order when
present: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`,
`Migration Notes`, `Versions`. Mark breaking entries inline with `**BREAKING:**`
and include migration guidance in the same bullet or under `Migration Notes`.

## [Unreleased]

This release reworks how reviewers, the Codex distribution, and the Pi runtime are
packaged. It contains breaking changes; read the migration notes in the bullets
marked `BREAKING`.

### Changed

- **BREAKING: manifest-dev ships ZERO agents; all agents are now skills, and `verify.agent` is
  removed from the manifest schema.** The 13 quality-dimension reviewer agents became the
  `review-code` skill (one reference per dimension, progressive disclosure), and the
  remaining functional agents — `check-pr`, `poll-slack`,
  `review-prompt` — are now skills too (`check-pr`/
  `poll-slack` under `manifest-dev`, `review-prompt` under `manifest-dev-tools`).
  - *Migrate*: there is no `verify.agent` field anymore. Every gate is verified by a
    **general-purpose** subagent whose `verify.prompt` activates a skill when specialized
    behavior is needed — e.g. *"Activate the manifest-dev:review-code skill with
    dimension=code-bugs and review the change. PASS only if no LOW-or-higher findings."*
    or *"Activate the manifest-dev:check-pr skill. PR: …"*. The prompt tells the current
    general-purpose verifier to activate the skill directly — it must not spawn a nested
    agent. `/define` encodes this automatically; manifests/task files authored
    against old agent names or `verify.agent` must be updated. The Pi runtime no longer
    reads a per-gate or configurable verifier agent (the `--manifest-verifier-agent` flag
    is removed); Pi runs the same per-gate verifier prompt in a JSON subprocess.

- **BREAKING: Codex installs via a plugin marketplace; the installer is retired.** The
  `dist/codex` `install.sh` / `install_helpers.py` / `config.toml` merge / `rules/` /
  `agents/*.toml` approach is gone. Codex now ships two native plugins
  (`manifest-dev`, `manifest-dev-tools`) registered by `.agents/plugins/marketplace.json`.
  - *Migrate*: `codex plugin marketplace add doodledood/manifest-dev`, then install the
    plugins. Plugin skills install into `~/.codex/plugins/cache/...` instead of the
    shared `~/.agents/skills/`, which is what stops manifest-dev skills from leaking into
    other Agent-Skills hosts (e.g. Pi). manifest-dev ships no agents on any target — the
    former functional agents are bundled skills.

- **BREAKING: Skills are verb-named; `criteria-checker` is dropped.** The former functional agents
  became verb-named skills: `github-pr-lifecycle` → `check-pr`, `slack-poller` →
  `poll-slack`, `prompt-reviewer` → `review-prompt`, and the reviewers' `code-review`
  skill → `review-code`. Instruction skills get verb names; knowledge skills (e.g.
  `prompt-engineering`) stay nouns. `criteria-checker` was removed entirely — with no
  `verify.agent` field, the default general-purpose verifier following `verify.prompt`
  already does single-criterion checks. The `prompt-engineering` skill now documents
  defaulting to a skill over an agent (cross-compatibility) and this naming convention.

- **BREAKING: Pi harness commands dropped the `manifest-` prefix.** `/manifest-do`, `/manifest-auto`,
  and `/manifest-babysit-pr` are now `/do`, `/auto`, and `/babysit-pr`.

- **The Pi runtime is now two packages.** `@doodledood/manifest-dev-pi` (core: `/do`,
  `/auto`) and `@doodledood/manifest-dev-pi-tools` (`/babysit-pr`, depends on core).

- **Pi no longer requires a separate verifier fanout package.** Harness-level verification
  now spawns manifest-dev-owned `pi --mode json` subprocesses, so Pi users install only the
  repo-root manifest-dev package.

### Fixed

- **Pi verifier fanout is owned by manifest-dev.** Harness verification now runs one
  `pi --mode json` subprocess per AC/INV gate, passes the exact `buildGateVerifierPrompt`
  text over stdin, parses the final assistant JSONL message, and keeps the existing
  `VERDICT` / `EVIDENCE` / `DETAILS` parser authoritative. Child process spawn errors,
  non-zero exits, and missing final assistant output become BLOCKED-compatible verifier
  records with stdout/stderr diagnostics. This removes the stale extension-context failure
  class from the old external fanout path.

- **Verifier-flag ownership simplified (repo-root-only tools package).** Anchored in Pi's
  `loader.js`: `getFlag` returns a value only if the calling extension registered the flag,
  values live in a per-load-cycle `runtime.flagValues` map. Only the core extension registers
  the `--manifest-verifier-*` flags (unconditionally, no process-global marker that a later
  load cycle would see); `/babysit-pr` reads them via a `process.argv` fallback. The tools
  package no longer declares its own `pi.extensions` — it loads only from the repo-root
  manifest, so it is never installed standalone (which couldn't resolve its relatively-imported
  core runtime) and core is always present to own the flags.

- **Per-target skill-activation naming.** Verifier-activation/chain prose is canonicalized to
  the plugin-qualified `manifest-dev:<skill>` colon form in source (Claude-native; OpenCode's
  installer rewrites it to suffixed names). The Pi dist strips the qualifier to the bare
  `/skill:<name>` form Pi actually invokes; Codex keeps the qualifier.

- **`/babysit-pr --ci` honors its one-shot contract.** `--ci` is now persisted on the run, and
  a lifecycle verification that FAILs only on external waits exits **pending** (resumable)
  instead of being looped back into repair. `check-pr` stays workflow-neutral; the `--ci`
  lifecycle verifier derives wait-only from check-pr's structured `sleep; reinvoke` directives
  and emits a `WAIT-PENDING` token the runtime routes to pending. A genuinely fixable failure
  still routes to repair. The derivation rule is injected by the runtime into the **gate
  verifier prompt** (`buildGateVerifierPrompt({ ciOneShot })`) — not the executor prompt or the
  manifest `verify.prompt` — so it actually reaches the verifier execution context for synthesized and
  `--manifest` runs alike. A reviewer/CI wait reads as BLOCKED under the base verdict
  rules, so the runtime routes `ciOneShot` `WAIT-PENDING` on either FAIL or BLOCKED status to
  pending — not just FAIL.

### Versions

- `manifest-dev` plugin: 2.4.0 → 2.8.4
- `manifest-dev-tools` plugin: 0.19.0 → 0.23.1
- `@doodledood/manifest-dev-pi` (and new `@doodledood/manifest-dev-pi-tools`): 0.8.11
