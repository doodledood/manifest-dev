# manifest-dev-tools

Post-processing utilities for manifest workflows.

## Skills

| Skill | Description |
|-------|-------------|
| `/adr` | Synthesize Architecture Decision Records from session transcripts. Extracts decisions via multi-agent pipeline and writes MADR files. |

## How It Works

These tools operate on the *outputs* of the manifest workflow (`/define` → `/do` → `/done`) — not during it. The session transcript is the richest data source; manifest and logs provide supplementary context.

## Installation

```bash
/plugin install manifest-dev-tools@manifest-dev-marketplace
```
