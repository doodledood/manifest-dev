# manifest-dev-tools

Utilities that complement manifest workflows — prompt engineering, PR babysitting, PR walkthroughs and reviews, ADR synthesis, and cross-boundary context handoff.

## Skills

| Skill | Description |
|-------|-------------|
| `/adr` | Synthesize Architecture Decision Records from session transcripts. Extracts decisions via multi-agent pipeline and writes MADR files. |
| `/babysit-pr` | Thin wrapper for PR lifecycle babysitting. Synthesizes a `define --babysit` manifest when needed, then hands off to `/goal /do <manifest-path>`. |
| `/handoff` | Produce a self-contained context payload that lets a fresh agent continue without re-deriving understanding. Two triggers: cross-boundary transfer (tool switch, fresh session, another agent) and DIY sub-agent (spin off a focused side-session and hand back). Manually invoked. |
| `/prompt-engineering` | Create, update, or review an LLM prompt — system prompt, skill, or agent. State the goal, trust the model, add only what closes a real gap in natural behavior. |
| `/review-pr` | Autonomous PR review that posts high-signal, human-voiced comments under your account. Advances existing review threads, verifies fixes/replies/stale comments, runs the reviewer fleet on the relevant diff range, and posts one GitHub review. `--loop` schedules repeated one-shot passes with backoff. |
| `/walk-pr` | Walk through a PR or large diff together, one sub-changeset at a time. |

## Agents

| Agent | Description |
|-------|-------------|
| `prompt-reviewer` | Reviews LLM prompts against the `/prompt-engineering` skill's gap-calibration principles. Reports issues without modifying files, tagging each `NEEDS_USER_INPUT` or `AUTO_FIXABLE` so an optimization loop can act on them. Use when reviewing prompt quality, auditing a prompt, or evaluating a system prompt. |

## How It Works

These tools sit alongside the manifest workflow (`/define` → `/do` → `/done`). `/adr` operates on the *outputs* (session transcript + manifest). `/handoff` produces a context payload for two use cases: cross-boundary transfer (tool switch, fresh session, multi-agent transfer) and DIY sub-agent flows (spin off a focused side-session and hand back to the parent without polluting its context). `/prompt-engineering`, `/walk-pr`, `/review-pr`, and `/babysit-pr` are stand-alone collaboration tools — `/walk-pr` is the collaborative review surface, `/review-pr` is the autonomous reviewer, and `/babysit-pr` is the author-side PR lifecycle entrypoint.

## Installation

```bash
/plugin install manifest-dev-tools@manifest-dev-marketplace
```
