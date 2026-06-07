# manifest-dev-tools

Utilities that complement manifest workflows — prompt engineering, PR babysitting, PR walkthroughs and reviews, ADR synthesis, cross-boundary context handoff, and incremental teaching for session work.

## Skills

| Skill | Description |
|-------|-------------|
| `/adr` | Synthesize Architecture Decision Records from session transcripts. Extracts decisions via multi-agent pipeline and writes MADR files. |
| `/babysit-pr` | Author-side PR lifecycle babysitter and companion to `/review-pr`. Uses manifest grounding when available, synthesizes PR grounding when not, then runs the manifest lifecycle toward green and mergeable without pressing merge. Supports CI one-shot advancement via `--ci`. |
| `/handoff` | Produce a self-contained context payload that lets a fresh agent continue without re-deriving understanding. Two triggers: cross-boundary transfer (tool switch, fresh session, another agent) and DIY sub-agent (spin off a focused side-session and hand back). Manually invoked. |
| `/prompt-engineering` | Create, update, or review an LLM prompt — system prompt, skill, or agent. State the goal, trust the model, add only what closes a real gap in natural behavior. |
| `/review-pr` | Autonomous PR review that posts high-signal, human-voiced comments under your account. Advances existing review threads, verifies fixes/replies/stale comments, runs the reviewer fleet on the relevant diff range, and posts one GitHub review. `--loop` schedules repeated one-shot passes with backoff. |
| `/teach-me` | Teach the learner to deeply understand a body of work — the current session, a PR, an ADR, or any topic. Builds a three-pillar checklist, teaches incrementally, and quizzes for demonstrated mastery before wrapping up. |
| `/walk-pr` | Walk through a PR or large diff together, one sub-changeset at a time. |

## Agents

| Agent | Description |
|-------|-------------|
| `prompt-reviewer` | Reviews LLM prompts against the `/prompt-engineering` skill's gap-calibration principles. Reports issues without modifying files, tagging each `NEEDS_USER_INPUT` or `AUTO_FIXABLE` so an optimization loop can act on them. Use when reviewing prompt quality, auditing a prompt, or evaluating a system prompt. |

## How It Works

These tools sit alongside the manifest workflow (`/define` → `/do` → `/done`). `/adr` operates on the *outputs* (session transcript + manifest). `/handoff` produces a context payload for two use cases: cross-boundary transfer (tool switch, fresh session, multi-agent transfer) and DIY sub-agent flows (spin off a focused side-session and hand back to the parent without polluting its context). `/teach-me` turns a body of work — the session, a PR, an ADR, or any topic — into an incremental learning loop that verifies understanding before ending. `/prompt-engineering`, `/walk-pr`, `/review-pr`, and `/babysit-pr` are stand-alone collaboration tools — `/walk-pr` is the collaborative review surface, `/review-pr` is the autonomous reviewer, and `/babysit-pr` is the author-side PR lifecycle actor that orchestrates core manifest-dev skills.

## Installation

```bash
/plugin install manifest-dev-tools@manifest-dev-marketplace
```

For OpenCode, Codex, and Pi package installs, use the repo-level distribution instructions. Pi installs from the repository root and includes compatible shared tools skills plus `/auto` and `/babysit-pr` wrappers that route through the Pi Harness-level Do outcome gate.
