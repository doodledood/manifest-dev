# Changelog

## Unreleased — Codex plugin-native distribution, code-review skill, command rename

This release reworks how reviewers, the Codex distribution, and the Pi runtime are
packaged. It contains **breaking changes** — read the migration notes.

### Breaking changes & migration

- **Reviewers are no longer addressable by agent name.** The 13 quality-dimension
  reviewer agents (`code-bugs-reviewer`, `code-design-reviewer`, `type-safety-reviewer`,
  …) have been removed and consolidated into a single `code-review` **skill** with one
  reference file per dimension (progressive disclosure).
  - *Migrate*: instead of `verify.agent: code-bugs-reviewer`, use a general-purpose
    verifier whose prompt activates the skill — e.g.
    *"Spawn a general-purpose review using the manifest-dev code-review skill with
    dimension=code-bugs. PASS only if no LOW-or-higher findings."* `/define` now encodes
    this automatically; manifests and task files authored against the old agent names
    must be updated. The surviving agents — `criteria-checker`, `github-pr-lifecycle`,
    `slack-poller`, `prompt-reviewer` — are unchanged.

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

- `manifest-dev` plugin: 2.4.0 → 2.5.0
- `manifest-dev-tools` plugin: 0.19.0 → 0.20.0
- `@doodledood/manifest-dev-pi` (and new `@doodledood/manifest-dev-pi-tools`): 0.5.0
