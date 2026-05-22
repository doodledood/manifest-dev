# manifest-dev-tools

Utilities that complement manifest workflows — prompt engineering, PR walkthroughs and reviews, ADR synthesis, and cross-boundary context handoff.

## Skills

| Skill | Description |
|-------|-------------|
| `/adr` | Synthesize Architecture Decision Records from session transcripts. Extracts decisions via multi-agent pipeline and writes MADR files. |
| `/handoff` | Produce a self-contained context payload that lets a fresh agent continue without re-deriving understanding. Two triggers: cross-boundary transfer (tool switch, fresh session, another agent) and DIY sub-agent (spin off a focused side-session and hand back). Manually invoked. |
| `/prompt-engineering` | Create, update, or review an LLM prompt — system prompt, skill, or agent. State the goal, trust the model, add only what closes a real gap in natural behavior. |
| `/review` | Autonomous PR review that posts high-signal, human-voiced comments under your account. Tiered reviewer fleet + holistic coherence pass grounded against PR history, bundle context, and the author's manifest. `--loop` watches the PR, verifies addressing per comment, reruns on success, terminates at 3 cycles or 24h. |
| `/walk-pr` | Walk through a PR or large diff together, one sub-changeset at a time. |

## Agents

| Agent | Description |
|-------|-------------|
| `prompt-reviewer` | Reviews an LLM prompt against the `/prompt-engineering` skill's gap-calibration principles. Reports issues without modifying files; tags each as `NEEDS_USER_INPUT` or `AUTO_FIXABLE` for downstream consumption by `/auto-optimize-prompt`. |

## How It Works

These tools sit alongside the manifest workflow (`/define` → `/do` → `/done`). `/adr` operates on the *outputs* (session transcript + manifest). `/handoff` produces a context payload for two use cases: cross-boundary transfer (tool switch, fresh session, multi-agent transfer) and DIY sub-agent flows (spin off a focused side-session and hand back to the parent without polluting its context). `/prompt-engineering`, `/walk-pr`, and `/review` are stand-alone collaboration tools — `/walk-pr` is the collaborative version, `/review` is the autonomous version.

## Installation

```bash
/plugin install manifest-dev-tools@manifest-dev-marketplace
```
