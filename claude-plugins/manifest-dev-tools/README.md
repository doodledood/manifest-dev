# manifest-dev-tools

Utilities that sit alongside the define → do → verify workflow — prompt engineering, PR babysitting, PR walkthroughs and reviews, cross-boundary context handoff, incremental teaching for session work, and a re-pitch corrective for messages that didn't land.

## Skills

| Skill | Description |
|-------|-------------|
| `/babysit-pr` | Author-side PR lifecycle babysitter and companion to `/review-pr`. Uses manifest grounding when available, synthesizes PR grounding when not, then runs the manifest lifecycle toward green and mergeable without pressing merge. Forwards `/do`'s opt-in `--verification` and `--verifier-model` execution policy; supports CI one-shot advancement via `--ci`; keeps a continuity journal by default under the user's home `.manifest-dev/logs/` directory, with `--no-log` to disable it. |
| `/handoff` | Produce a self-contained context payload that lets a fresh agent continue without re-deriving understanding. Two triggers: cross-boundary transfer (tool switch, fresh session, another agent) and DIY sub-agent (spin off a focused side-session and hand back). Manually invoked. |
| `/prompt-engineering` | Create, update, or review an LLM prompt — system prompt, skill, or agent. State the goal, trust the model, add only what closes a real gap in natural behavior. |
| `/review-pr` | Autonomous PR review that posts high-signal, human-voiced comments under your account. Advances existing review threads, verifies fixes/replies/stale comments, and posts one GitHub review. Polymorphic on `--manifest`: without it, runs the generic reviewer fleet on the relevant diff range; with it, skips the fleet and independently verifies *only* the manifest — running each Acceptance Criterion and Global Invariant `verify.instructions` against the PR head with one fresh verifier per gate and posting PASS/FAIL. `--loop` schedules repeated one-shot passes with backoff. |
| `/teach-me` | Teach the learner to deeply understand a body of work — the current session, a PR, an ADR, or any topic. Builds a three-pillar checklist, teaches incrementally, and quizzes for demonstrated mastery before wrapping up. |
| `/wait-what` | Stop and re-pitch the last message — it didn't land. Re-explains with the context the reader was missing, in plain words and the project's own vocabulary, cutting every line that isn't value while keeping every fact that is. |
| `/walk-pr` | Walk through a PR or large diff together, one sub-changeset at a time. |
| `review-prompt` | Reviews LLM prompts against the `/prompt-engineering` skill's gap-calibration principles. Reports issues without modifying files, tagging each `NEEDS_USER_INPUT` or `AUTO_FIXABLE` so an optimization loop can act on them. Use when reviewing prompt quality, auditing a prompt, or evaluating a system prompt. Gate evaluation instructions activate it when needed. |

## How It Works

These tools sit alongside the manifest workflow (`/define` → `/do` → `/done`). `/handoff` produces a context payload for two use cases: cross-boundary transfer (tool switch, fresh session, multi-agent transfer) and DIY sub-agent flows (spin off a focused side-session and hand back to the parent without polluting its context). `/teach-me` turns a body of work — the session, a PR, an ADR, or any topic — into an incremental learning loop that verifies understanding before ending. `/prompt-engineering`, `/walk-pr`, `/review-pr`, and `/babysit-pr` are stand-alone collaboration tools — `/walk-pr` is the collaborative review surface, `/review-pr` is the autonomous reviewer, and `/babysit-pr` is the author-side PR lifecycle actor that orchestrates core manifest-dev skills.

## Installation

```bash
/plugin install manifest-dev-tools@manifest-dev
```

For OpenCode, Codex, and Pi package installs, use the repo-level distribution instructions. Pi installs from the repository root and includes compatible shared tools skills plus `/auto` and `/babysit-pr` prompt aliases that invoke the same portable skills.
