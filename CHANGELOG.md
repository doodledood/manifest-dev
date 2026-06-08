# Changelog

## Unreleased — Codex plugin-native distribution, code-review skill, command rename

This release reworks how reviewers, the Codex distribution, and the Pi runtime are
packaged. It contains **breaking changes** — read the migration notes.

### Breaking changes & migration

- **manifest-dev ships ZERO agents — all agents are now skills, and `verify.agent` is
  removed from the manifest schema.** The 13 quality-dimension reviewer agents became the
  `code-review` skill (one reference per dimension, progressive disclosure), and the four
  remaining functional agents — `criteria-checker`, `github-pr-lifecycle`, `slack-poller`,
  `prompt-reviewer` — are now skills too (`criteria-checker`/`github-pr-lifecycle`/
  `slack-poller` under `manifest-dev`, `prompt-reviewer` under `manifest-dev-tools`).
  - *Migrate*: there is no `verify.agent` field anymore. Every gate is verified by a
    **general-purpose** subagent whose `verify.prompt` activates a skill when specialized
    behavior is needed — e.g. *"Spawn a general-purpose review using the manifest-dev
    code-review skill with dimension=code-bugs. PASS only if no LOW-or-higher findings."*
    or *"Spawn a general-purpose agent and activate the manifest-dev github-pr-lifecycle
    skill. PR: …"*. `/define` encodes this automatically; manifests/task files authored
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
    other Agent-Skills hosts (e.g. Pi). On Codex, the surviving functional agents degrade
    to the general-purpose subagent (plugins cannot bundle agents).

- **Pi harness commands dropped the `manifest-` prefix.** `/manifest-do`, `/manifest-auto`,
  and `/manifest-babysit-pr` are now `/do`, `/auto`, and `/babysit-pr`.

- **The Pi runtime is now two packages.** `@doodledood/manifest-dev-pi` (core: `/do`,
  `/auto`) and `@doodledood/manifest-dev-pi-tools` (`/babysit-pr`, depends on core).

### Versions

- `manifest-dev` plugin: 2.4.0 → 2.6.0
- `manifest-dev-tools` plugin: 0.19.0 → 0.21.0
- `@doodledood/manifest-dev-pi` (and new `@doodledood/manifest-dev-pi-tools`): 0.6.0
