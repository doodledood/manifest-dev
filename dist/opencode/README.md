# manifest-dev for OpenCode CLI

Verification-first manifest workflows for OpenCode. Use the `/define`, `/do`, and `/learn-define-patterns` commands, and let the workflow invoke the `verify`, `done`, and `escalate` skills as needed.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 6 | define, do, done, escalate, learn-define-patterns, verify |
| Agents | 12 | criteria-checker, 8 code reviewers, manifest-verifier, context-file-adherence-reviewer, define-session-analyzer |
| Commands | 3 | /define, /do, /learn-define-patterns |
| Plugin | 1 | OpenCode hook plugin implementing pretool-verify, stop-do, post-compact, and todo tracking |

Only `/define`, `/do`, and `/learn-define-patterns` are exposed as user commands. The `verify`, `done`, and `escalate` skills remain internal workflow steps.

## Install

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
```

This downloads the latest release and installs skills, agents, commands, and the OpenCode plugin into `~/.config/opencode/` by default. Safe to re-run. The installer adds the plugin as `plugins/manifest-dev.ts`, so it loads alongside a user's existing `plugins/index.ts` without overwriting shared plugin entrypoints.
It does not write `AGENTS.md`, and it does not replace existing user plugins or unrelated `opencode.json` entries.

By default it installs globally into `~/.config/opencode/`, which is OpenCode's real config path. If you explicitly want a project-local install, run `OPENCODE_INSTALL_TARGET=project bash dist/opencode/install.sh`.

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- uninstall
```

This removes only manifest-dev-managed OpenCode files from the selected target: the suffixed skills, suffixed agents, suffixed commands, `plugins/manifest-dev.ts`, and the manifest-dev hook spec. It leaves user-owned `plugins/index.ts` and unrelated `opencode.json` settings alone.

### Skills only (via npx)

If you only want the skills (no agents, commands, or hooks):

```bash
npx skills add doodledood/manifest-dev --all -a opencode
```

OpenCode also reads `.claude/skills/` natively, so Claude Code skills work without conversion.

### Manual

```bash
git clone https://github.com/doodledood/manifest-dev.git /tmp/manifest-dev

# Skills
cp -r /tmp/manifest-dev/dist/opencode/skills/* .opencode/skills/

# Agents
cp -r /tmp/manifest-dev/dist/opencode/agents/* .opencode/agents/

# Commands
cp -r /tmp/manifest-dev/dist/opencode/commands/* .opencode/commands/

# Plugin (auto-loaded)
cp /tmp/manifest-dev/dist/opencode/plugins/index.ts .opencode/plugins/manifest-dev.ts
cp /tmp/manifest-dev/dist/opencode/plugins/HOOK_SPEC.md .opencode/plugins/manifest-dev.HOOK_SPEC.md
```

## Feature Parity

| Feature | Claude Code | OpenCode | Notes |
|---------|------------|----------|-------|
| Skills (define, do, verify, done, escalate, learn-define-patterns) | Native | Native | Skills copy unchanged; OpenCode reads `.claude/skills/` natively |
| Agents (12 code reviewers + orchestration) | Native | Converted | Frontmatter converted to OpenCode format (boolean tools, mode, temperature) |
| Commands (/define, /do, /learn-define-patterns) | Skills with `user-invocable: true` | `.opencode/commands/*.md` | Commands invoke the corresponding skill |
| Hook: pretool-verify (context injection) | Python PreToolUse + `additionalContext` | `experimental.chat.system.transform` + `output.system.push()` | Implemented in the bundled plugin |
| Hook: stop-do (block premature stop) | Python Stop hook + `decision: block` | `session.idle` (fire-and-forget) | **Cannot block** -- best-effort workaround via `client.session.prompt()` (fragile) |
| Hook: post-compact (context recovery) | Python PreCompact + `additionalContext` | `experimental.session.compacting` + `output.context.push()` | Implemented in the bundled plugin |
| Hook: todo tracking | N/A | `todo.updated` event | New -- tracks workflow progress via todo state changes |
| Tool blocking | PreToolUse returns `decision: block` | `throw new Error("reason")` in `tool.execute.before` | Error message becomes tool result seen by LLM |
| Subagent spawning | Agent tool | `task` tool | Mapped in agent frontmatter |
| Subagent hook coverage | Hooks fire for all tool calls | **Hooks do NOT fire in subagents** (#5894) | Known gap -- no workaround |
| Todo management | TaskCreate/TaskUpdate | `todowrite` tool | Mapped in agent frontmatter |
| Web research | WebFetch + WebSearch | `webfetch` + `websearch` | WebSearch requires Exa AI key in OpenCode |
| Session storage | JSONL transcript files | SQLite database | In-memory state tracking replaces transcript parsing |

## Execution Modes

Control verification intensity with `--mode`:

| Mode | Verification | Parallelism | Best For |
|------|-------------|-------------|----------|
| **thorough** (default) | Full reviewer agents, unlimited fix loops | All at once | Production-quality work |
| **balanced** | Full model capability, capped loops | Batched (max 4) | Standard development |
| **efficient** | Skips reviewer subagents, lighter checks | Sequential | Quick iterations, low-risk changes |

Usage: `/do <manifest> [log] --mode balanced`

Mode can also be set in the manifest's `mode:` field during `/define`. The `--mode` flag on `/do` takes precedence.

## Known Limitations

1. **Tool blocking uses throw, not abort.** To block a tool call in `tool.execute.before`, **throw new Error("reason")**. The error message becomes the tool result seen by the LLM. The `args.abort` pattern documented elsewhere is incorrect. Confirmed from source code and issue #5894.

2. **Stop-do enforcement has no blocking equivalent.** Claude Code's Stop hook can return `decision: block` to prevent the agent from stopping. OpenCode's `session.idle` event is **fire-and-forget and cannot prevent stopping**. The workaround `ctx.client.session.prompt()` creates a new turn but is fragile with race conditions in `run` mode (issue #15267). Feature request exists (issue #12472).

3. **Subagent hook bypass.** `tool.execute.before` and `tool.execute.after` do **NOT** fire for tool calls within subagents (issue #5894). This means skills invoked via the `task` tool run in isolation and their internal tool calls bypass all hooks. Security/guardrail gap with no workaround.

4. **Context injection is experimental.** `experimental.chat.system.transform` (push to `output.system[]`) is the correct mechanism for system-level context injection, replacing Claude Code's `additionalContext`. The `experimental.` prefix means the API may change without notice. Do NOT use `tui.prompt.append` for context injection -- it only fills the TUI input field.

5. **Session storage is SQLite, not JSONL.** Session data is stored in SQLite at `~/.local/share/opencode/opencode.db` (WAL mode, Drizzle ORM). There are no JSONL transcript files. Claude Code's transcript-parsing utilities (`hook_utils.py`) cannot be reused directly. The plugin tracks workflow state in-memory instead.

6. **`experimental.session.compacting` is experimental.** The post-compact hook uses an experimental OpenCode event that may change between releases. Context injection uses `output.context.push()`, not `additionalContext`.

7. **`$ARGUMENTS` behavior is undefined in OpenCode skills.** Skills using `$ARGUMENTS` work in Claude Code but the variable substitution behavior is not standardized in OpenCode. Commands use `$ARGUMENTS` natively.

8. **WebSearch requires an Exa AI API key** in OpenCode (configured via `OPENCODE_EXA_API_KEY` or provider config). Claude Code's WebSearch works without additional configuration.

9. **Native `.claude/` compatibility.** OpenCode reads `.claude/skills/` natively (priority 2), so users who already have the Claude Code plugin installed may not need `dist/opencode/skills/` at all -- the skills are already discovered.

## Directory Structure

```
dist/opencode/
  AGENTS.md              # Bundled reference guide (not installed by script)
  README.md              # This file
  install.sh             # Idempotent installer
  agents/                # 12 converted agents
    criteria-checker.md
    code-bugs-reviewer.md
    code-design-reviewer.md
    code-simplicity-reviewer.md
    code-maintainability-reviewer.md
    code-coverage-reviewer.md
    code-testability-reviewer.md
    type-safety-reviewer.md
    docs-reviewer.md
    context-file-adherence-reviewer.md
    manifest-verifier.md
    define-session-analyzer.md
  commands/              # 3 user-invoked commands
    define.md
    do.md
    learn-define-patterns.md
  plugins/
    index.ts             # OpenCode hook plugin source (installed as plugins/manifest-dev.ts)
    HOOK_SPEC.md         # Behavioral specification / maintenance reference
  skills/                # 6 skills (copied unchanged from source)
    define/
    do/
    done/
    escalate/
    learn-define-patterns/
    verify/
```

## Source

This is a generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev) for Claude Code. The Claude Code plugin is the source of truth.
