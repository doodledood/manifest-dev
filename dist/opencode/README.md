# manifest-dev for OpenCode CLI

Verification-first manifest workflows for OpenCode. Use the `/define`, `/do`, `/auto`, and `/learn-define-patterns` commands, and let the workflow invoke the `verify`, `done`, and `escalate` skills as needed.

Version: 0.74.0

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 7 | auto, define, do, done, escalate, learn-define-patterns, verify |
| Agents | 14 | criteria-checker, 10 code reviewers, manifest-verifier, context-file-adherence-reviewer, define-session-analyzer |
| Commands | 4 | /auto, /define, /do, /learn-define-patterns |
| Plugin | 1 | Workflow enforcement hooks (stop-do, verify-context, post-compact, amendment-check, log-reminder) |

## Install

### Primary: npx skills

```bash
npx skills add https://github.com/doodledood/manifest-dev --all -a opencode
```

### Alternative: install.sh (full distribution)

```bash
# Install globally
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash

# Install to project
OPENCODE_INSTALL_TARGET=project curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash

# Uninstall
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- uninstall
```

### Manual install

```bash
# Clone the repo
git clone https://github.com/doodledood/manifest-dev.git
cd manifest-dev

# Copy components to project
cp -r dist/opencode/skills/* .opencode/skills/
cp -r dist/opencode/agents/* .opencode/agents/
cp -r dist/opencode/commands/* .opencode/commands/
cp dist/opencode/plugins/index.ts .opencode/plugins/manifest-dev.ts
cp dist/opencode/plugins/HOOK_SPEC.md .opencode/plugins/manifest-dev.HOOK_SPEC.md
```

## Feature Parity

| Feature | Claude Code | OpenCode |
|---------|-------------|----------|
| Skills (define, do, verify, auto, done, escalate, learn-define-patterns) | Full | Full |
| Agents (14 reviewers + verifiers) | Full | Full |
| User-invocable commands | Slash commands | Commands (`.opencode/commands/`) |
| Stop enforcement | Blocking hook | Best-effort re-engagement (fire-and-forget) |
| Verify context injection | PreToolUse additionalContext | experimental.chat.system.transform |
| Post-compact recovery | SessionStart additionalContext | experimental.session.compacting |
| Amendment check | UserPromptSubmit additionalContext | experimental.chat.system.transform |
| Post-tool log reminder | PostToolUse additionalContext | tool.execute.after output mutation |
| Subagent hook coverage | Full | Partial (hooks don't fire in subagents) |

## Execution Modes

| Mode | Verification | Parallelism | Best For |
|------|-------------|-------------|----------|
| **thorough** (default) | Full reviewer agents, unlimited fix loops | All at once | Production-quality work |
| **balanced** | Full model capability, capped loops | Batched (max 4) | Standard development |
| **efficient** | Skips reviewer subagents, lighter checks | Sequential | Quick iterations, low-risk changes |

## Known Limitations

1. **Stop-do enforcement has no blocking equivalent** -- `session.idle` is fire-and-forget. Cannot prevent the session from stopping during /do.
2. **Subagent hook bypass** -- `tool.execute.before`/`after` does NOT fire for tool calls within subagents (issue #5894). Verification hooks won't trigger inside spawned agents.
3. **Context injection is experimental** -- `experimental.chat.system.transform` and `experimental.session.compacting` APIs may change without notice.
4. **Session storage is SQLite, not JSONL** -- Plugin uses in-memory state tracking instead of transcript parsing.
5. **WebSearch requires Exa AI API key** in OpenCode.
6. **Plugin state is ephemeral** -- Lost on server restart. Long sessions may lose workflow state.

## Source

Generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev). The Claude Code plugin (`claude-plugins/manifest-dev/`) is the source of truth.
