# manifest-dev for OpenCode

OpenCode distribution of [manifest-dev](https://github.com/doodledood/manifest-dev). These skills keep three things in your project instead of in your head: what it's becoming, what's worth doing next, and what done means here. The agent checks its result against the last of those before reporting completion.

Generated from the Claude Code plugins.

## Install

Clone the repository, then add the plugin directory to the `plugin` array in `~/.config/opencode/opencode.json`:

```json
{
  "plugin": ["/path/to/manifest-dev/dist/opencode/plugin"]
}
```

Update with `git pull` and restart OpenCode — configuration loads once at startup. Uninstall by removing the config line and deleting the clone. Nothing is copied into your OpenCode config or any shared skills directory.

## What ships

Two source plugins contribute skills:

| From | Skills |
|------|--------|
| `manifest-dev` | `auto`, `chat-surface`, `check-pr`, `define`, `do`, `done`, `escalate`, `figure-out`, `figure-out-team`, `init-context`, `just-auto`, `just-do`, `next-ticket`, `poll-slack`, `review-code`, `review-writing`, `run-ticket`, `sweep-tickets`, `ticket-up` |
| `manifest-dev-tools` | `babysit-pr`, `eli5`, `handoff`, `prompt-engineering`, `re-pitch`, `review-pr`, `review-prompt`, `teach-me`, `walk-pr` |

Start with `figure-out` on a problem you already have; the rest of the workflow follows from it. The [repository README](https://github.com/doodledood/manifest-dev) covers what each part is for.

## Parity with Claude Code

The workflow is the same; the packaging differs:

| Component | Status |
|-----------|--------|
| Skills | All 27, under their original names |
| Agents | None — manifest-dev ships no agents on any host. Quality reviewers are dimensions of the `review-code` skill. |
| Hooks | Not shipped |
| Slash commands | Registered at startup by the plugin, for every skill that is user-invocable |

Unattended runs use your host's goal-setting or continuation capability where it has one; where it doesn't, the workflow still runs turn by turn.

## Configuration

The single `plugin` array entry is the whole of it.
