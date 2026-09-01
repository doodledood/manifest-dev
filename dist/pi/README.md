# manifest-dev for Pi

Pi distribution of [manifest-dev](https://github.com/doodledood/manifest-dev). These skills keep three things in your project instead of in your head: what it's becoming, what's worth doing next, and what done means here. The agent checks its result against the last of those before reporting completion.

Generated from the Claude Code plugins.

## Install

```bash
pi install git:github.com/doodledood/manifest-dev@main
```

From a local checkout, `pi install .` — or `pi install -l .` for a project-local install, or `pi -e .` for a single run.

## What ships

Two source plugins contribute skills:

| From | Skills |
|------|--------|
| `manifest-dev` | `auto`, `check-pr`, `define`, `design`, `do`, `done`, `escalate`, `figure-out`, `figure-out-team`, `init-context`, `just-auto`, `just-define`, `just-do`, `just-figure-out`, `next-ticket`, `poll-slack`, `review-code`, `review-design`, `review-writing`, `run-ticket`, `sweep-tickets`, `ticket-up` |
| `manifest-dev-tools` | `babysit-pr`, `eli5`, `handoff`, `prompt-engineering`, `review-pr`, `review-prompt`, `teach-me`, `walk-pr` |

Start with `figure-out` on a problem you already have; the rest of the workflow follows from it. The [repository README](https://github.com/doodledood/manifest-dev) covers what each part is for.

## Parity with Claude Code

The workflow is the same; the packaging differs:

| Component | Status |
|-----------|--------|
| Skills | All 30, under their original names |
| Agents | None — manifest-dev ships no agents on any host. Quality reviewers are dimensions of the `review-code` skill. |
| Hooks | Not shipped |
| Prompt aliases | `/do`, `/auto`, and `/babysit-pr` expand to the matching skill |

Unattended runs use your host's goal-setting or continuation capability where it has one; where it doesn't, the workflow still runs turn by turn.

## Configuration

None required. The package manifest at the repository root declares the skills and prompt templates.
