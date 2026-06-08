# Changelog

## Unreleased — Codex plugin-native distribution, review-code skill, command rename

This release reworks how reviewers, the Codex distribution, and the Pi runtime are
packaged. It contains **breaking changes** — read the migration notes.

### Breaking changes & migration

- **manifest-dev ships ZERO agents — all agents are now skills, and `verify.agent` is
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
    is removed); verifiers always spawn general-purpose.

- **Codex installs via a plugin marketplace; the installer is retired.** The
  `dist/codex` `install.sh` / `install_helpers.py` / `config.toml` merge / `rules/` /
  `agents/*.toml` approach is gone. Codex now ships two native plugins
  (`manifest-dev`, `manifest-dev-tools`) registered by `.agents/plugins/marketplace.json`.
  - *Migrate*: `codex plugin marketplace add doodledood/manifest-dev`, then install the
    plugins. Plugin skills install into `~/.codex/plugins/cache/...` instead of the
    shared `~/.agents/skills/`, which is what stops manifest-dev skills from leaking into
    other Agent-Skills hosts (e.g. Pi). manifest-dev ships no agents on any target — the
    former functional agents are bundled skills.

- **Skills are verb-named; `criteria-checker` is dropped.** The former functional agents
  became verb-named skills: `github-pr-lifecycle` → `check-pr`, `slack-poller` →
  `poll-slack`, `prompt-reviewer` → `review-prompt`, and the reviewers' `code-review`
  skill → `review-code`. Instruction skills get verb names; knowledge skills (e.g.
  `prompt-engineering`) stay nouns. `criteria-checker` was removed entirely — with no
  `verify.agent` field, the default general-purpose verifier following `verify.prompt`
  already does single-criterion checks. The `prompt-engineering` skill now documents
  defaulting to a skill over an agent (cross-compatibility) and this naming convention.

- **Pi harness commands dropped the `manifest-` prefix.** `/manifest-do`, `/manifest-auto`,
  and `/manifest-babysit-pr` are now `/do`, `/auto`, and `/babysit-pr`.

- **The Pi runtime is now two packages.** `@doodledood/manifest-dev-pi` (core: `/do`,
  `/auto`) and `@doodledood/manifest-dev-pi-tools` (`/babysit-pr`, depends on core).

### Fixes

- **Clear verifier-spawn failure reporting.** Anchored in `@gotgenes/pi-subagents`
  `service-adapter.ts`: `spawn` reads the service's stored `currentCtx` (captured at
  `session_start`) to build the parent snapshot, and Pi's stale-context guard throws if that
  ctx was invalidated by a session replacement/reload. When no verifier spawns at all, Harness
  verification now reports a single harness/runtime orchestration BLOCKED — naming the
  underlying error, the current/executor session ids, and (for the stale-context signature)
  the session-replacement cause — instead of an identical BLOCKED on every gate that never
  ran. We do not retry the spawn: the stored ctx only refreshes on another session lifecycle
  event, so an immediate re-spawn would read the same stale ctx. The related
  custom-verifier-agent failure mode is gone independently: verifiers are always
  general-purpose (no `verify.agent`), so a missing reviewer agent type can no longer block.

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
  manifest `verify.prompt` — so it actually reaches the verifier subagent for synthesized and
  `--manifest` runs alike.

### Versions

- `manifest-dev` plugin: 2.4.0 → 2.8.3
- `manifest-dev-tools` plugin: 0.19.0 → 0.23.1
- `@doodledood/manifest-dev-pi` (and new `@doodledood/manifest-dev-pi-tools`): 0.8.9
