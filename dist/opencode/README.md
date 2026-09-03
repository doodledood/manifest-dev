# manifest-dev for OpenCode

OpenCode distribution of [manifest-dev](https://github.com/doodledood/manifest-dev). These skills keep three things in your project instead of in your head: what it's becoming, what's worth doing next, and what done means here. The agent checks its result against the last of those before reporting completion.

There is no separate skills payload for OpenCode. The plugin at `dist/opencode/plugin/index.js` registers the two source skill directories of your clone — `claude-plugins/manifest-dev/skills` and `claude-plugins/manifest-dev-tools/skills` — as skill paths, so OpenCode reads the same files every other host does.

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
| `manifest-dev` | `auto`, `check-pr`, `define`, `design`, `do`, `done`, `escalate`, `figure-out`, `figure-out-team`, `init-context`, `just-auto`, `just-define`, `just-do`, `just-figure-out`, `next-ticket`, `poll-slack`, `review-code`, `review-design`, `review-writing`, `run-ticket`, `sweep-tickets`, `ticket-up` |
| `manifest-dev-tools` | `babysit-pr`, `eli5`, `handoff`, `prompt-engineering`, `review-pr`, `review-pr-holistic`, `review-pr-judgment`, `review-pr-thread-verify`, `review-prompt`, `teach-me`, `walk-pr` |

Six of these are dependencies other skills invoke rather than entry points: `done`, `escalate`, and `poll-slack` are called by the ticket workflows, and the three `review-pr-*` skills are called by `review-pr`. They ship so the calling skill resolves on every host; they are not meant to be invoked by hand.

Start with `figure-out` on a problem you already have; the rest of the workflow follows from it. The [repository README](https://github.com/doodledood/manifest-dev) covers what each part is for.

## Parity with Claude Code

The workflow is the same; the packaging differs:

| Component | Status |
|-----------|--------|
| Skills | All 33, read from the source tree under their original names |
| Agents | None — manifest-dev ships no agents on any host. Delegated work is a skill activated in an isolated execution context, with an inline fallback where the host has none. |
| Hooks | Not shipped |
| Slash commands | Registered at startup by the plugin, for every skill that is user-invocable |

Unattended runs use your host's goal-setting or continuation capability where it has one; where it doesn't, the workflow still runs turn by turn.

## Configuration

The single `plugin` array entry is the whole of it.
