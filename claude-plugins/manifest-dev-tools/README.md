# manifest-dev-tools

Utilities that complement manifest workflows — prompt engineering, PR walkthroughs, ADR synthesis, and cross-boundary context handoff.

## Skills

| Skill | Description |
|-------|-------------|
| `/adr` | Synthesize Architecture Decision Records from session transcripts. Extracts decisions via multi-agent pipeline and writes MADR files. |
| `/handoff` | Produce a self-contained context payload that lets a fresh agent continue without re-deriving understanding. Two triggers: cross-boundary transfer (tool switch, fresh session, another agent) and DIY sub-agent (spin off a focused side-session and hand back). Manually invoked. |
| `/prompt-engineering` | Create, update, slim, or review LLM prompts in the slim discipline. |
| `/walk-pr` | Walk through a PR or large diff together, one sub-changeset at a time. |

## How It Works

These tools sit alongside the manifest workflow (`/define` → `/do` → `/done`). `/adr` operates on the *outputs* (session transcript + manifest). `/handoff` produces a context payload for two use cases: cross-boundary transfer (tool switch, fresh session, multi-agent transfer) and DIY sub-agent flows (spin off a focused side-session and hand back to the parent without polluting its context). `/prompt-engineering` and `/walk-pr` are stand-alone collaboration tools.

## Installation

```bash
/plugin install manifest-dev-tools@manifest-dev-marketplace
```
