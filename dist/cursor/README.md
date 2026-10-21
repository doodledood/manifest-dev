# manifest-dev for Cursor

Cursor distribution of [manifest-dev](https://github.com/doodledood/manifest-dev). These skills keep three things in your project instead of in your head: what it's becoming, what's worth doing next, and what done means here. The agent checks its result against the last of those before reporting completion.

The same plugins also serve Grok Bot, whose plugin store lists plugins from the [Cursor Marketplace](https://cursor.com/marketplace).

There is no separate skills payload for Cursor. Each source plugin directory carries a [Cursor plugin manifest](https://cursor.com/docs/reference/plugins) beside its Claude Code one — `claude-plugins/manifest-dev/.cursor-plugin/plugin.json` and `claude-plugins/manifest-dev-tools/.cursor-plugin/plugin.json` — and the repo-root `.cursor-plugin/marketplace.json` lists the two. Neither manifest names a skills path, so Cursor's default discovery reads each plugin's `skills/` directory: the same files every other host reads. This folder holds only these instructions.

## Install

**From the Cursor Marketplace:** not listed yet. Every listing is [reviewed by Cursor](https://cursor.com/help/security-and-privacy/marketplace-security) before it appears; once it does, install `manifest-dev` (and `manifest-dev-tools` if you want it) from **Customize** or [cursor.com/marketplace](https://cursor.com/marketplace).

**Locally**, following Cursor's [Test plugins locally](https://cursor.com/docs/plugins#test-plugins-locally):

```bash
git clone https://github.com/doodledood/manifest-dev.git
mkdir -p ~/.cursor/plugins/local
cp -R manifest-dev/claude-plugins/manifest-dev ~/.cursor/plugins/local/manifest-dev
cp -R manifest-dev/claude-plugins/manifest-dev-tools ~/.cursor/plugins/local/manifest-dev-tools
```

Then restart Cursor or run **Developer: Reload Window**, and open **Customize** to see the skills. Copy the folders rather than linking them: Cursor skips a symlink in `~/.cursor/plugins/local` whose target lies outside that folder. On Teams and Enterprise plans, local plugins load only when an admin allows local plugin imports, and a marketplace install of the same name takes precedence over the local copy.

Update with `git pull` in the clone and copy the two folders again (remove the old copies first). Uninstall by deleting them from `~/.cursor/plugins/local` and reloading.

## What ships

| Plugin | Skills |
|--------|--------|
| `manifest-dev` | `auto`, `check-pr`, `define`, `design`, `do`, `done`, `escalate`, `figure-out`, `figure-out-team`, `manifest-dev-help`, `next-ticket`, `orchestrate`, `poll-slack`, `review-code`, `review-design`, `review-writing`, `run-ticket`, `setup-project`, `ticket-up` |
| `manifest-dev-tools` | `babysit-pr`, `eli5`, `handoff`, `manifest-to-goal`, `prompt-engineering`, `review-pr`, `review-pr-holistic`, `review-pr-judgment`, `review-pr-thread-verify`, `review-prompt`, `teach-me`, `walk-pr` |

Six of these are dependencies other skills invoke rather than entry points: `done` and `escalate` are called by `do`, `poll-slack` by `figure-out-team`, and the three `review-pr-*` skills by `review-pr`. They ship so the calling skill resolves. Their `user-invocable: false` marker hides them from the slash menu on hosts that read it; Cursor's skill format has no such field, so Cursor lists them alongside the rest. They are not meant to be invoked by hand.

Start with `figure-out` on a problem you already have; the rest of the workflow follows from it. The [repository README](https://github.com/doodledood/manifest-dev) covers what each part is for.

## Parity with Claude Code

The workflow is the same; the packaging differs:

| Component | Status |
|-----------|--------|
| Skills | All skills, read from the source plugin directories under their original names |
| Agents | None — manifest-dev ships no agents on any host. Delegated work is a skill activated in an isolated execution context, with an inline fallback where the host has none. |
| Rules, commands, hooks, MCP servers | Not shipped |
| Slash commands | Cursor's own skill invocation; the six dependency skills appear too (see above) |

Unattended runs use your host's goal-setting or continuation capability where it has one; where it doesn't, the workflow still runs turn by turn.
