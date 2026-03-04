# manifest-dev for OpenCode CLI

Verification-first manifest workflows for OpenCode. Plan work thoroughly with `/define`, execute against criteria with `/do`, verify everything passes with `/verify`.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 6 | define, do, done, escalate, learn-define-patterns, verify |
| Agents | 12 | criteria-checker, 8 code reviewers, manifest-verifier, context-file-adherence-reviewer, define-session-analyzer |
| Commands | 3 | /define, /do, /learn-define-patterns |
| Hook stubs | 4 | pretool-verify, stop-do, post-compact, todo-tracking (require manual TS porting) |

## Install

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
```

This downloads the latest release, copies skills, agents, commands, and plugin stubs into `.opencode/` in your current directory. Safe to re-run; won't overwrite a manually ported `index.ts`.

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

# Plugin stubs
cp -r /tmp/manifest-dev/dist/opencode/plugins/* .opencode/plugins/
cd .opencode/plugins && bun install
```

## Feature Parity

| Feature | Claude Code | OpenCode | Notes |
|---------|------------|----------|-------|
| Skills (define, do, verify, done, escalate, learn-define-patterns) | Native | Native | Skills copy unchanged; OpenCode reads `.claude/skills/` natively |
| Agents (12 code reviewers + orchestration) | Native | Converted | Frontmatter converted to OpenCode format (boolean tools, mode, temperature) |
| Commands (/define, /do, /learn-define-patterns) | Skills with `user-invocable: true` | `.opencode/commands/*.md` | Commands invoke the corresponding skill |
| Hook: pretool-verify (context injection) | Python PreToolUse + `additionalContext` | `experimental.chat.system.transform` + `output.system.push()` | Stub provided -- context injection via system transform, not additionalContext |
| Hook: stop-do (block premature stop) | Python Stop hook + `decision: block` | `session.idle` (fire-and-forget) | **Cannot block** -- best-effort workaround via `client.session.prompt()` (fragile) |
| Hook: post-compact (context recovery) | Python PreCompact + `additionalContext` | `experimental.session.compacting` + `output.context.push()` | Stub provided -- experimental event |
| Hook: todo tracking | N/A | `todo.updated` event | New -- tracks workflow progress via todo state changes |
| Tool blocking | PreToolUse returns `decision: block` | `throw new Error("reason")` in `tool.execute.before` | Error message becomes tool result seen by LLM |
| Subagent spawning | Agent tool | `task` tool | Mapped in agent frontmatter |
| Subagent hook coverage | Hooks fire for all tool calls | **Hooks do NOT fire in subagents** (#5894) | Known gap -- no workaround |
| Todo management | TaskCreate/TaskUpdate | `todowrite` tool | Mapped in agent frontmatter |
| Web research | WebFetch + WebSearch | `webfetch` + `websearch` | WebSearch requires Exa AI key in OpenCode |
| Session storage | JSONL transcript files | SQLite database | In-memory state tracking replaces transcript parsing |

## Known Limitations

1. **Hooks require manual TypeScript porting.** The Python hooks cannot run in Bun. Generated stubs in `plugins/index.ts` provide the structure and corrected API patterns; `plugins/HOOK_SPEC.md` provides the full behavioral specification for each hook.

2. **Tool blocking uses throw, not abort.** To block a tool call in `tool.execute.before`, **throw new Error("reason")**. The error message becomes the tool result seen by the LLM. The `args.abort` pattern documented elsewhere is incorrect. Confirmed from source code and issue #5894.

3. **Stop-do enforcement has no blocking equivalent.** Claude Code's Stop hook can return `decision: block` to prevent the agent from stopping. OpenCode's `session.idle` event is **fire-and-forget and cannot prevent stopping**. The workaround `ctx.client.session.prompt()` creates a new turn but is fragile with race conditions in `run` mode (issue #15267). Feature request exists (issue #12472).

4. **Subagent hook bypass.** `tool.execute.before` and `tool.execute.after` do **NOT** fire for tool calls within subagents (issue #5894). This means skills invoked via the `task` tool run in isolation and their internal tool calls bypass all hooks. Security/guardrail gap with no workaround.

5. **Context injection is experimental.** `experimental.chat.system.transform` (push to `output.system[]`) is the correct mechanism for system-level context injection, replacing Claude Code's `additionalContext`. The `experimental.` prefix means the API may change without notice. Do NOT use `tui.prompt.append` for context injection -- it only fills the TUI input field.

6. **Session storage is SQLite, not JSONL.** Session data is stored in SQLite at `~/.local/share/opencode/opencode.db` (WAL mode, Drizzle ORM). There are no JSONL transcript files. Claude Code's transcript-parsing utilities (`hook_utils.py`) cannot be reused directly. The plugin tracks workflow state in-memory instead.

7. **`experimental.session.compacting` is experimental.** The post-compact hook uses an experimental OpenCode event that may change between releases. Context injection uses `output.context.push()`, not `additionalContext`.

8. **`$ARGUMENTS` behavior is undefined in OpenCode skills.** Skills using `$ARGUMENTS` work in Claude Code but the variable substitution behavior is not standardized in OpenCode. Commands use `$ARGUMENTS` natively.

9. **WebSearch requires an Exa AI API key** in OpenCode (configured via `OPENCODE_EXA_API_KEY` or provider config). Claude Code's WebSearch works without additional configuration.

10. **Native `.claude/` compatibility.** OpenCode reads `.claude/skills/` natively (priority 2), so users who already have the Claude Code plugin installed may not need `dist/opencode/skills/` at all -- the skills are already discovered.

## Directory Structure

```
dist/opencode/
  AGENTS.md              # Workflow overview and agent descriptions
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
  plugins/               # Hook stubs (manual port needed)
    index.ts
    HOOK_SPEC.md
    package.json
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
