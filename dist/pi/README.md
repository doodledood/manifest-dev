# manifest-dev for Pi

Pi distribution of [manifest-dev](https://github.com/doodledood/manifest-dev). These skills keep three things in your project instead of in your head: what it's becoming, what's worth doing next, and what done means here. The agent checks its result against the last of those before reporting completion.

There is no separate skills payload for Pi. The package manifest at the repository root (`package.json`, under `pi.skills`) points Pi at the two source skill directories — `claude-plugins/manifest-dev/skills` and `claude-plugins/manifest-dev-tools/skills` — so Pi reads the same files every other host does. `dist/pi/prompts` holds only the three prompt aliases.

## Install

```bash
pi install git:github.com/doodledood/manifest-dev@main
```

From a local checkout, `pi install .` — or `pi install -l .` for a project-local install, or `pi -e .` for a single run.

Update by re-running the same install command for the newer revision.

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
| Prompt aliases | `/do`, `/auto`, and `/babysit-pr` expand to the matching skill |

Unattended runs use your host's goal-setting or continuation capability where it has one; where it doesn't, the workflow still runs turn by turn.

## Configuration

None required. The package manifest at the repository root declares the skill directories and prompt templates.
