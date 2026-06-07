# manifest-dev for Codex CLI

Codex distribution of [manifest-dev](https://github.com/doodledood/manifest-dev), shipped as **native Codex plugins** installed from a repo marketplace. Plugin skills install into Codex's private plugin cache (`~/.codex/plugins/cache/...`), so nothing lands in the shared `~/.agents/skills/` directory.

## Install

```bash
# Add the marketplace, then install the plugins from the Codex /plugins UI:
codex plugin marketplace add doodledood/manifest-dev
```

This registers two plugins:

| Plugin | Skills |
|--------|--------|
| `manifest-dev` | `define`, `do`, `auto`, `done`, `escalate`, `figure-out`, `figure-out-team`, `code-review` |
| `manifest-dev-tools` | `babysit-pr`, `review-pr`, `walk-pr`, `teach-me`, `adr`, `handoff`, `prompt-engineering` |

Local development against a checkout:

```bash
codex plugin marketplace add ./   # reads .agents/plugins/marketplace.json at the repo root
```

## What's generated vs. retired

- **Generated**: `plugins/<name>/.codex-plugin/plugin.json` + bundled `skills/`, registered by the repo-root `.agents/plugins/marketplace.json`.
- **Retired**: the previous `install.sh` / `install_helpers.py` / `config.toml` merge / `rules/` / `agents/*.toml` installer is gone. Codex now installs via the plugin marketplace.

## Reviewers

The quality reviewers (bugs, design, simplicity, types, contracts, …) are **dimensions of the `code-review` skill**, not standalone agents — Codex plugins bundle skills, not agents. A verifier activates `code-review` with a dimension (e.g. `dimension=code-bugs`) and it loads exactly that dimension's reference.

The remaining functional agents (`criteria-checker`, `github-pr-lifecycle`, `slack-poller`, `prompt-reviewer`) cannot be plugin-bundled; on Codex they degrade to the general-purpose subagent driven by the gate's `verify.prompt`.

## Limitations

- No agent bundling (see Reviewers above).
- `/auto` and `/babysit-pr` ship as skills that chain `/do`; only Pi has native runtime wrappers.
- Hooks are not shipped (Codex hook execution remains limited).
