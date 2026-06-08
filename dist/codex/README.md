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
| `manifest-dev` | `define`, `do`, `auto`, `done`, `escalate`, `figure-out`, `figure-out-team`, `review-code` |
| `manifest-dev-tools` | `babysit-pr`, `review-pr`, `walk-pr`, `teach-me`, `adr`, `handoff`, `prompt-engineering` |

Local development against a checkout:

```bash
codex plugin marketplace add ./   # reads .agents/plugins/marketplace.json at the repo root
```

## What's generated vs. retired

- **Generated**: `plugins/<name>/.codex-plugin/plugin.json` + bundled `skills/`, registered by the repo-root `.agents/plugins/marketplace.json`.
- **Retired**: the previous `install.sh` / `install_helpers.py` / `config.toml` merge / `rules/` / `agents/*.toml` installer is gone. Codex now installs via the plugin marketplace.

## Reviewers and verification skills

manifest-dev ships **zero agents** — everything is a skill. The quality reviewers (bugs, design, simplicity, types, contracts, …) are **dimensions of the `review-code` skill**: a verifier activates `review-code` with a dimension (e.g. `dimension=code-bugs`) and it loads exactly that dimension's reference. The former functional agents are now their own bundled skills too — `check-pr` (PR lifecycle), `poll-slack` (Slack deltas), and the tools-side `review-prompt` (prompt quality). Verification is always a general-purpose subagent whose `verify.prompt` activates the relevant skill — there is no `verify.agent` field.

## Limitations

- manifest-dev ships no agents; all capabilities are skills (see above).
- `/auto` and `/babysit-pr` ship as skills that chain `/do`; only Pi has native runtime wrappers.
- Hooks are not shipped (Codex hook execution remains limited).
