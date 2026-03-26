# manifest-dev for Gemini CLI

Verification-first manifest workflows for Gemini CLI, delivered as extension-managed skills, agents, and hooks.

## Components

| Type | Count | Details |
|------|-------|---------|
| Skills | 7 | auto, define, do, verify, done, escalate, learn-define-patterns |
| Agents | 14 | criteria-checker, manifest-verifier, 10 code reviewers, docs-reviewer, define-session-analyzer |
| Hooks | 3 | pretool-verify, stop-do-enforcement, post-compact-recovery |

## Install

### Option 1: Remote installer (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash
```

Re-running the installer updates the extension in `~/.gemini/extensions/manifest-dev/`. The installer merges `experimental.enableAgents = true` and the manifest-dev hook registrations into `~/.gemini/settings.json` additively. No post-install edits are required.

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash -s -- uninstall
```

### Option 2: Skills only (via npx)

```bash
npx skills add https://github.com/doodledood/manifest-dev --all -a gemini-cli
```

## Workflow

```
`define` -> produces a manifest with acceptance criteria
    |
`do` -> executes against the manifest and tracks progress
    |
`verify` -> parallel verification with 12 specialized agents
    |
`done` (all pass) or `escalate` (blocked)
```

## Execution Modes

| Mode | Verification | Parallelism | Best For |
|------|-------------|-------------|----------|
| **thorough** (default) | Full reviewer agents, unlimited fix loops | All at once | Production-quality work |
| **balanced** | Full model capability, capped loops | Batched (max 4) | Standard development |
| **efficient** | Skips reviewer subagents, lighter checks | Sequential | Quick iterations, low-risk changes |

## Known Limitations

1. **Agents are experimental** -- Require `enableAgents` flag. API may change.
2. **No SubagentStart/Stop hooks** -- Cannot intercept subagent lifecycle.
3. **Agent tool is name-based** -- Each subagent becomes a tool by its registered name.
4. **$ARGUMENTS not supported** -- Claude Code skill extension only.
5. **`grep_search` is canonical** -- Source code defines `GREP_TOOL_NAME = 'grep_search'`.
6. **`generalist` not `generalist_agent`** -- Built-in subagent tool name is `generalist`.

## Repository

Main repo: [github.com/doodledood/manifest-dev](https://github.com/doodledood/manifest-dev)

This distribution is auto-generated from the Claude Code plugin source.
