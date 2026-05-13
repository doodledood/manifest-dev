# manifest-dev for Gemini CLI

Verification-first manifest workflows for Gemini CLI. Plan work with structured interviews, execute against acceptance criteria, verify with parallel agents.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 7 | Workflow skills: define, do, verify, auto, figure-out, escalate, done |
| Agents | 15 | Specialized agents for code review, manifest verification, and PR lifecycle |
| Hooks | 4 | Event-driven hooks enforcing workflow discipline (stop-do, pretool-verify, prompt-submit-amendment, post-compact) |

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
| Skills | All 7 | All 7 | Copied unchanged |
| Agents | All 15 | All 15 | Frontmatter converted |
| Hooks | 4 hooks | 4 hooks | Adapted to Gemini event model |
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
2. `/do` — Executes the manifest, satisfying each Deliverable's acceptance criteria
3. `/verify` — Spawns parallel verifier agents for all criteria
4. `/auto` — Chains define and do autonomously

Supporting skills: `/figure-out` for deep investigation, `/escalate` for blocking issues.

**PR lifecycle.** PR-lifecycle work composes the `github-pr-lifecycle` agent through `tasks/PR_LIFECYCLE.md` task guidance. `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. `/auto --babysit <pr-url>` chains synthesis and execution in one command.

## Repository

[github.com/doodledood/manifest-dev](https://github.com/doodledood/manifest-dev)
