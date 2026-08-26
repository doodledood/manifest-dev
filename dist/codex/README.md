# manifest-dev for Codex CLI

Codex distribution of [manifest-dev](https://github.com/doodledood/manifest-dev). These skills keep three things in your project instead of in your head: what it's becoming, what's worth doing next, and what done means here. The agent checks its result against the last of those before reporting completion.

Generated from the Claude Code plugins. Skills install into Codex's private plugin cache, so nothing lands in a shared skills directory.

## Install

Codex separates marketplace registration from plugin installation:

```bash
codex plugin marketplace add doodledood/manifest-dev
codex plugin add manifest-dev@manifest-dev
codex plugin add manifest-dev-tools@manifest-dev
```

From a local checkout, use `codex plugin marketplace add ./` in place of the first line.

Uninstall with `codex plugin remove <name>@manifest-dev` for each plugin, then `codex plugin marketplace remove manifest-dev`.

## What ships

Two source plugins contribute skills:

| Plugin | Skills |
|--------|--------|
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
| Command shims | None — skills are invoked directly |

Unattended runs use your host's goal-setting or continuation capability where it has one; where it doesn't, the workflow still runs turn by turn.

## Configuration

None required beyond the two install commands.
