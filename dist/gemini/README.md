# manifest-dev for Gemini CLI

Verification-first manifest workflows for Gemini CLI. Plan work with structured interviews, execute against acceptance criteria, verify with parallel agents.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 12 | Workflow skills: define, do, verify, auto, figure-out, escalate, done, tend-pr, tend-pr-tick, learn-define-patterns, thinking-disciplines, stop-thinking-disciplines |
| Agents | 14 | Specialized review agents for code quality verification |
| Hooks | 7 | Event-driven hooks enforcing workflow discipline |

## Installation

### Remote install (recommended)

```bash
npx skills add doodledood/manifest-dev --all -a gemini-cli
```

### Gemini extensions

```bash
gemini extensions install https://github.com/doodledood/manifest-dev/dist/gemini
```

### Manual install

```bash
git clone https://github.com/doodledood/manifest-dev.git
cd manifest-dev/dist/gemini
./install.sh              # Project-level (.gemini/)
./install.sh --global     # User-level (~/.gemini/)
```

## Required Configuration

Agents require the experimental flag in `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```

The `install.sh` script sets this automatically.

## Feature Parity with Claude Code

| Feature | Claude Code | Gemini CLI | Notes |
|---------|-------------|------------|-------|
| Skills | All 12 | All 12 | Copied unchanged |
| Agents | All 14 | All 14 | Frontmatter converted |
| Hooks | 8 hooks | 8 hooks | Adapted to Gemini event model |
| Stop enforcement | PreToolUse/Stop | BeforeTool/AfterAgent | Retry counter for loop prevention |
| Context injection | additionalContext | additionalContext | Same mechanism |
| Transcript parsing | JSONL (user/assistant) | JSONL (user/gemini) | Adapter normalizes |
| Model routing | haiku/sonnet/opus | inherit | Gemini uses session model |
| $ARGUMENTS | Supported | Not supported | Gemini CLI limitation |
| Subagents | Agent tool | Named tool per agent | Subagents are tools by name |

## Quick Start

```bash
# Define a task
/define Build a REST API for user management

# Execute the manifest
/do /tmp/manifest-*.md

# Or do it all at once
/auto Build a REST API for user management
```

## Workflow Overview

1. `/define` — Structured interview builds a manifest with deliverables, acceptance criteria, and global invariants
2. `/do` — Executes the manifest, logging progress for disaster recovery
3. `/verify` — Spawns parallel verifier agents for all criteria
4. `/auto` — Chains define and do autonomously

Supporting skills: `/figure-out` for deep investigation (end with `/stop-thinking-disciplines`), `/escalate` for blocking issues, `/tend-pr` for PR lifecycle automation.

## Repository

[github.com/doodledood/manifest-dev](https://github.com/doodledood/manifest-dev)
