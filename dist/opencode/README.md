# manifest-dev for OpenCode CLI

Verification-first manifest workflows for OpenCode. Use the `/define`, `/do`, `/auto`, and `/learn-define-patterns` commands, and let the workflow invoke the `verify`, `done`, and `escalate` skills as needed.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 7 | auto, define, do, done, escalate, learn-define-patterns, verify |
| Agents | 14 | criteria-checker, 10 code reviewers, manifest-verifier, context-file-adherence-reviewer, define-session-analyzer |
| Commands | 4 | /auto, /define, /do, /learn-define-patterns |
| Plugin | 1 | OpenCode hook plugin implementing pretool-verify, stop-do, post-compact, and todo tracking |

## Install

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
```

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- uninstall
```

### Skills only (via npx)

```bash
npx skills add doodledood/manifest-dev --all -a opencode
```

## Execution Modes

| Mode | Verification | Parallelism | Best For |
|------|-------------|-------------|----------|
| **thorough** (default) | Full reviewer agents, unlimited fix loops | All at once | Production-quality work |
| **balanced** | Full model capability, capped loops | Batched (max 4) | Standard development |
| **efficient** | Skips reviewer subagents, lighter checks | Sequential | Quick iterations, low-risk changes |

## Known Limitations

1. **Stop-do enforcement has no blocking equivalent** -- `session.idle` is fire-and-forget.
2. **Subagent hook bypass** -- `tool.execute.before`/`after` does NOT fire in subagents (#5894).
3. **Context injection is experimental** -- `experimental.chat.system.transform` API may change.
4. **Session storage is SQLite, not JSONL** -- No JSONL transcript files.
5. **WebSearch requires Exa AI API key** in OpenCode.

## Source

Generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev). The Claude Code plugin is the source of truth.
