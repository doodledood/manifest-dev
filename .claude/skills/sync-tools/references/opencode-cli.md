# OpenCode CLI Conversion Guide

Reference for converting Claude Code plugin components to OpenCode format (anomalyco/opencode v1.2.15, March 2026).

## Conversion Summary

| Component | Phase 1 (Deterministic) | Phase 2 (LLM) |
|-----------|------------------------|----------------|
| Skills | Copy unchanged | — |
| Agents | Frontmatter conversion (tool map + format) | Temperature/mode inference, description enrichment |
| Hooks | Generate complete plugin module placed in the local plugin directory | Adapt behavioral logic to OpenCode's event model |
| Commands | Map skill → command markdown | Adapt prompt body |
| MCP config | Generate opencode.json snippet | — |
| Instructions | Rename CLAUDE.md → AGENTS.md | — |

## Phase 1: Deterministic Conversions

### Tool Name Mapping (Lookup Table)

| Claude Code Tool | OpenCode Tool Key | Notes |
|-----------------|-------------------|-------|
| Bash | `bash` | Direct equivalent |
| BashOutput | `bash` | Same tool — deduplicate |
| Read | `read` | Direct equivalent |
| Write | `write` | Direct equivalent (create/overwrite) |
| Edit | `edit` | Both do string replacement |
| Grep | `grep` | Both use ripgrep |
| Glob | `glob` | Direct equivalent |
| WebFetch | `webfetch` | Lowercase, no space |
| WebSearch | `websearch` | Lowercase, no space (requires Exa AI key) |
| Agent | `task` | Subagent spawning |
| TaskCreate / TaskUpdate | `todowrite` | Task/todo management (create and update) |
| TaskGet / TaskList | `todoread` | Task/todo management (read) |
| TaskOutput | `bash` | No direct equivalent — approximate via shell |
| TaskStop | (no equivalent) | No background task management |
| Skill | `skill` | Both load skills |
| TodoWrite | `todowrite` | Direct equivalent (legacy name for TaskCreate) |
| TodoRead | `todoread` | Direct equivalent (legacy name for TaskGet/TaskList) |
| NotebookEdit | (no equivalent) | Not available in OpenCode |
| AskUserQuestion | `question` | User interaction (conditional — interactive clients only) |
| EnterPlanMode / ExitPlanMode | (no equivalent) | `plan_exit` exists but experimental |
| EnterWorktree | (no equivalent) | No worktree support |
| TeamCreate / TeamDelete / SendMessage | (no equivalent) | No team management |
| ListMcpResourcesTool / ReadMcpResourceTool | (no equivalent) | MCP handled differently |

OpenCode-only tools (no Claude Code equivalent):
- `list` — directory listing (file is ls.ts but tool name is `list`)
- `lsp` — Language Server Protocol (experimental, requires `OPENCODE_EXPERIMENTAL_LSP_TOOL`)
- `apply_patch` — unified diff application (conditional — GPT models only, replaces edit/write)
- `multiedit` — batch multi-file editing (present in source, may be behind flag)
- `codesearch` — semantic code search (requires Exa AI or OpenCode provider)
- `batch` — parallel tool calls up to 25 (experimental, requires `config.experimental.batch_tool`)
- `plan_exit` — exit plan mode (experimental, requires `OPENCODE_EXPERIMENTAL_PLAN_MODE`)

Meta-permission keys (permission-only, not tool toggles):
- `external_directory` — access outside project workspace
- `doom_loop` — repeated identical tool calls (3+)

### Agent Frontmatter Conversion

Claude Code agent format:
```yaml
---
description: Agent purpose description
tools: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill
model: inherit
---
```

OpenCode agent format:
```yaml
---
description: Agent purpose description
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.2
tools:
  bash: true
  glob: true
  grep: true
  read: true
  webfetch: true
  task: true
  todowrite: true
  todoread: true
  websearch: true
  skill: true
---
```

**Complete OpenCode agent frontmatter fields**:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `description` | string | REQUIRED | Brief description of agent purpose |
| `mode` | "primary" / "subagent" / "all" | "all" | How agent can be invoked |
| `model` | string | global config | Provider/model-id format (e.g., `anthropic/claude-sonnet-4-20250514`) |
| `temperature` | number (0.0-1.0) | model default | Response randomness |
| `top_p` | number (0.0-1.0) | model default | Nucleus sampling |
| `steps` | positive integer | unlimited | Max agentic iterations |
| `color` | string | none | Hex (`"#FF5733"`) or theme (primary/secondary/accent/success/warning/error/info) |
| `hidden` | boolean | false | Hide from @ autocomplete (subagents only) |
| `disable` | boolean | false | Disable agent entirely |
| `prompt` | string | none | Custom system prompt (file path or inline text) |
| `tools` | object | all enabled | Tool enablement (boolean per tool key) |
| `permission` | object | global config | Permission rules per tool |

**Phase 1 conversion rules** (deterministic):
1. Keep `description` as-is
2. Convert `tools` from comma-separated string to boolean object with lowercase keys
3. Deduplicate: BashOutput → bash (just set `bash: true` once). Map TaskCreate/TaskUpdate → todowrite, TaskGet/TaskList → todoread, Agent → task
4. Add `mode: subagent` for agents spawned by other agents, `mode: primary` for top-level
5. Keep prompt body (everything below frontmatter) unchanged
6. Write to `.opencode/agents/` (project) or `~/.config/opencode/agents/` (global)

**Phase 2 enrichment** (LLM):
- Infer `temperature` from agent purpose: 0.1-0.2 for deterministic (QA, verification), 0.3 for balanced (code review), 0.5-0.7 for creative
- Infer `mode` (primary vs subagent) from agent's role in workflow
- Design `permission` block for granular per-command access control:
  ```yaml
  permission:
    bash:
      "git push": "ask"
      "rm -rf *": "deny"
      "*": "allow"
  ```
- Enrich `description` if Claude Code version is too terse for OpenCode's auto-matching

### Tool Restriction Pattern

Claude Code uses explicit allow-list (only declared tools available). OpenCode's boolean object works the same:
```yaml
tools:
  bash: true
  read: true
  write: false    # explicitly disabled
  # edit not listed = not available
```

Glob patterns for MCP tools: `"mcp-name*": true` enables all tools from an MCP server.

### Skills Handling

SKILL.md files copy unchanged. OpenCode reads `.claude/skills/` natively (priority 2), so Claude Code skills already work without conversion.

**OpenCode skill discovery paths** (precedence order, walks UP from cwd):
1. `.opencode/skills/<name>/SKILL.md` — Native OpenCode
2. `.claude/skills/<name>/SKILL.md` — Claude Code compatible
3. `.agents/skills/<name>/SKILL.md` — Agent standard compatible
4. `~/.config/opencode/skills/<name>/SKILL.md` — Global native
5. `~/.claude/skills/<name>/SKILL.md` — Global Claude compatible
6. `~/.agents/skills/<name>/SKILL.md` — Global agent standard

**OpenCode skill frontmatter** (superset of open standard):
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | 1-64 chars, regex: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| `description` | string | Yes | 1-1024 chars |
| `license` | string | No | License identifier |
| `compatibility` | string | No | Compatibility tags |
| `metadata` | Record<string,string> | No | Arbitrary key-value pairs |

Directory name MUST match declared `name`. Claude Code extensions (`user-invocable`, `tools`, `context`, `agent`, `hooks`) are silently ignored.

Skill subdirectories (`scripts/`, `references/`, `assets/`, `tasks/`) copy recursively.

### Command Conversion

Claude Code user-invoked skills map to OpenCode custom commands.

**OpenCode command format** (`.opencode/commands/<name>.md`):
```yaml
---
description: Command description
agent: build           # optional: which agent executes
model: anthropic/...   # optional: override model
subtask: true          # optional: force subagent
---

Command prompt template with $ARGUMENTS placeholder.

$1, $2, $3 for positional args.
@filename for file inclusion.
!`command` for bash output injection.
```

**Phase 1 conversion**:
- For each user-invoked skill, generate a command markdown file
- Copy `description` from skill frontmatter
- Copy prompt body as command template
- Replace skill-specific invocation patterns with command syntax

**Phase 2 enrichment** (LLM):
- Adapt `$ARGUMENTS` usage (not standardized outside Claude Code — may need rewriting)
- Set appropriate `agent` and `model` fields
- Decide on `subtask: true` for skills that should run in isolation

### MCP Config Generation

Generate `opencode.json` snippet:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "server-name": {
      "type": "local",
      "command": ["npx", "-y", "package-name"],
      "environment": { "KEY": "{env:VAR_NAME}" },
      "enabled": true,
      "timeout": 5000
    },
    "remote-server": {
      "type": "remote",
      "url": "https://server.example.com",
      "headers": { "Authorization": "Bearer {env:API_KEY}" }
    }
  }
}
```

Variable substitution: `{env:VARIABLE_NAME}` and `{file:path/to/file}`.

### Instructions / Rules

- CLAUDE.md → rename to AGENTS.md (or keep both — OpenCode falls back to CLAUDE.md)
- Global: `~/.claude/CLAUDE.md` → `~/.config/opencode/AGENTS.md`
- Additional instructions via `opencode.json`: `"instructions": ["CONTRIBUTING.md", "docs/guidelines.md"]`
- Disable Claude Code compat: `OPENCODE_DISABLE_CLAUDE_CODE=1`, `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1`, `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1`

## Phase 2: LLM-Required Conversions

### Hook Porting (Python → TypeScript)

Claude Code hooks are Python scripts using JSON stdin/stdout. OpenCode hooks are TypeScript modules using `@opencode-ai/plugin`, run by Bun.

**Plugin skeleton** (CORRECTED — blocking via throw, not args.abort):
```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const ManifestDevPlugin: Plugin = async (ctx) => {
  // ctx.project — { id, worktree, vcs }
  // ctx.client — SDK client (HTTP to localhost:4096)
  // ctx.$ — Bun shell API
  // ctx.directory — current working directory
  // ctx.worktree — git worktree root
  // ctx.serverUrl — server URL
  return {
    "tool.execute.before": async ({ tool, sessionID, callID }, { args }) => {
      // Block: throw new Error("reason") — error message becomes tool result seen by LLM
      // Modify args: mutate output.args object
      // LIMITATION: Does NOT fire for subagent tool calls (issue #5894)
    },
    "tool.execute.after": async ({ tool, sessionID, callID, args }, { title, output, metadata }) => {
      // Mutate output.output to change what LLM sees as tool result
      // Mutate output.title, output.metadata as needed
    },
    "experimental.chat.system.transform": async ({ sessionID, model }, output) => {
      // Inject system-level context: output.system.push("your context here")
      // Called before every LLM request
    },
    "experimental.session.compacting": async ({ sessionID }, output) => {
      // Inject context to preserve across compaction: output.context.push("context")
      // Optionally replace compaction prompt: output.prompt = "custom prompt"
    },
    event: async ({ event }) => {
      // Catch-all for bus events (session.idle, todo.updated, etc.)
      // Fire-and-forget — cannot block anything
      if (event.type === "session.idle") {
        // Session stopped — CANNOT prevent stopping
        // Workaround: ctx.client.session.prompt(sessionID, { parts: [...] }) — fragile, race condition
      }
      if (event.type === "todo.updated") {
        // Track workflow progress via todo state changes
        // event.properties.todos = [{id, content, status, priority}]
      }
    },
  }
}
```

**Hook execution model**: `Plugin.trigger()` calls hooks sequentially across all loaded plugins. Each hook receives the SAME mutable `output` object — mutations accumulate (middleware chain pattern).

**Event mapping (Claude Code → OpenCode)**:

| Claude Code Event | OpenCode Hook/Event | Blocking | Notes |
|-------------------|-------------------|----------|-------|
| PreToolUse | `tool.execute.before` (hook) | Yes — **throw Error** to block | Error message becomes tool result. Does NOT fire in subagents (issue #5894) |
| PostToolUse | `tool.execute.after` (hook) | No (mutate output) | Mutate `output.output` to change what LLM sees |
| Stop | `session.idle` (event) | **NO — fire-and-forget** | Cannot prevent stopping. Workaround: `client.session.prompt()` creates NEW turn (fragile, race condition in `run` mode — issue #15267) |
| SessionStart | `session.created` (event) | No | Fire-and-forget bus event |
| PreCompact | `experimental.session.compacting` (hook) | No — inject context only | Push to `output.context[]`, optionally replace `output.prompt` |
| Notification | (no equivalent) | — | Gap |
| SubagentStart/Stop | (no equivalent) | — | Gap — tool.execute.before also doesn't fire in subagents |

**Context injection mechanisms (3 options):**

| Mechanism | When | How | Best For |
|-----------|------|-----|----------|
| `experimental.chat.system.transform` | Before every LLM request | `output.system.push("context")` | Persistent context injection (closest to Claude Code's additionalContext) |
| `experimental.session.compacting` | During compaction | `output.context.push("context")` | Preserving workflow state across compaction |
| `chat.message` | Before user message is processed | Mutate `output.message` or `output.parts` | Modifying user input |

**IMPORTANT**: `tui.prompt.append` only fills the TUI input field — it does NOT inject system messages. Use `experimental.chat.system.transform` for system context injection.

**Session storage**: SQLite at `~/.local/share/opencode/opencode.db` (WAL mode, Drizzle ORM). **No JSONL transcript file.** Plugin access via SDK client API only:
- `client.session.list()` — list sessions
- `client.session.get(id)` — get session metadata
- SSE event stream for real-time updates
- POST `/session/{id}/message` — send message to session

Tables: SessionTable, MessageTable (role, time_created, data), PartTable (type, content). Part types: TextPart, ToolPart, AgentPart, CompactionPart, etc.

**Skill invocation detection**: Skills in OpenCode are NOT tools — they are agent definitions activated via the `task` tool. In `tool.execute.before`, `input.tool` = `"task"` when a subagent (skill) is spawned. However, due to the subagent bypass, tool calls WITHIN the subagent won't trigger hooks.

**todo.updated event**: Fires through bus with full todo array:
```typescript
{ type: "todo.updated", properties: { sessionID: string, todos: Array<{id, content, status, priority}> } }
```
Useful for workflow tracking — monitor todo status transitions in the `event` handler.

Additional OpenCode events (no Claude Code equivalent):
- `command.executed`, `file.edited`, `file.watcher.updated`
- `message.updated`, `message.removed`, `message.part.updated`, `message.part.removed`
- `permission.asked`, `permission.replied`
- `session.compacted`, `session.deleted`, `session.diff`, `session.error`, `session.status`, `session.updated`
- `shell.env` — inject environment variables: `output.env.KEY = "value"`
- `todo.updated`, `server.connected`, `installation.updated`
- `lsp.client.diagnostics`, `lsp.updated`
- `tui.prompt.append` — fills TUI input field (NOT system messages)
- `tui.command.execute`, `tui.toast.show`
- `chat.message`, `chat.params`, `chat.headers` — modify messages/model params/headers
- `tool.definition` — mutate tool descriptions/schemas
- `permission.ask` — intercept permission prompts (`output.status = "deny" | "allow"`)

**Plugin installation**:
- Local plugins are auto-loaded from top-level JavaScript/TypeScript files in `.opencode/plugins/` or `~/.config/opencode/plugins/`
- Install manifest-dev as its own top-level file (for example `plugins/manifest-dev.ts`) so it loads alongside a user's existing `plugins/index.ts`
- Do not require changes to a user's existing root `plugins/index.ts`, root `package.json`, or `opencode.json`

**Custom tools** (`.opencode/tools/`):
```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Tool description",
  args: {
    input: tool.schema.string().describe("Input parameter"),
  },
  async execute(args, context) {
    // context.agent, context.sessionID, context.directory, context.worktree, context.abort
    return "result"
  }
})
```

### Prompt Body Adaptation

LLM should review agent prompt bodies for:
- Tool name references ("Use the Read tool" → "Use the read tool")
- Tool capability assumptions (Claude's Bash is sandboxed differently)
- Output format expectations
- Implicit tool references ("run this command" → "use the bash tool")

## Directory Structure

```
dist/opencode/
├── agents/                     # Agents (converted frontmatter)
│   ├── code-bugs-reviewer.md
│   └── criteria-checker.md
├── commands/                   # Commands (from user-invoked skills)
│   └── define.md
├── skills/                     # Skills (SKILL.md copied unchanged)
│   ├── define/
│   │   └── SKILL.md
│   ├── do/
│   │   └── SKILL.md
│   └── verify/
│       └── SKILL.md
├── plugins/
│   ├── index.ts                # Hook plugin (complete installable implementation)
│   └── HOOK_SPEC.md            # Behavioral specification / maintenance reference
├── tools/                      # Custom tools (if any)
└── README.md
```

## Installation

For skills only (universal installer):
```bash
npx skills add <github-url> --all -a opencode
```

For the full distribution:
```bash
# Skills (already work from .claude/ natively, but for standalone):
cp -r dist/opencode/skills/* .opencode/skills/

# Agents
cp -r dist/opencode/agents/* .opencode/agents/

# Commands
cp -r dist/opencode/commands/* .opencode/commands/

# Plugin payload (auto-loaded)
cp dist/opencode/plugins/index.ts .opencode/plugins/manifest-dev.ts
cp dist/opencode/plugins/HOOK_SPEC.md .opencode/plugins/manifest-dev.HOOK_SPEC.md
```

## Skill Chaining

Claude Code's define → do → verify → done chain uses the Skill tool. OpenCode has a `skill` tool with same semantics. Skill chaining works — agents invoke skills via `skill({ name: "skill-name" })`.

OpenCode's `task` tool also supports subagent delegation, compatible with Claude Code's Task-based spawning.

## Namespacing

Install scripts handle all component renaming at install time via `install_helpers.py`. The `dist/opencode/` directory keeps original names — sync-tools writes originals, install scripts namespace.

**Pattern**: All components get `-manifest-dev` suffix:
- Skill dirs: `skills/define/` → `skills/define-manifest-dev/`
- Agent files: `code-bugs-reviewer.md` → `code-bugs-reviewer-manifest-dev.md`
- Command files: `define.md` → `define-manifest-dev.md`
- SKILL.md `name:` field patched to match directory name
- Content cross-references patched (slash commands, quoted strings, paths, agent names)

**Selective cleanup** (replaces `rm -rf` of shared dirs):
```bash
find "$TARGET/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
find "$TARGET/commands" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
```

Component names on disk will have `-manifest-dev` suffix after install.

## Context File Adaptation

During sync, replace remaining `CLAUDE.md` references that mean "this CLI's context file" with `AGENTS.md`:
- Agent content: any "CLAUDE.md" that refers to the project context file → `AGENTS.md`
- Context file (AGENTS.md): references to context file names
- README: references to context file names
- Skills (operational only): instructions like "write to CLAUDE.md" → "write to AGENTS.md". Leave research/reference content unchanged.
- Do NOT replace "CLAUDE.md" when it refers to Claude Code's own file (e.g., in comparative text or research).

The `context-file-adherence-reviewer` agent already uses generic "context file" language — no special handling needed for its content.

## Known Limitations

1. **Block pattern** — **Throw an Error** to block tool calls, NOT `args.abort`. Error message becomes tool result seen by LLM. Confirmed from source code and issue #5894.
2. **No Stop hook** — `session.idle` is fire-and-forget. **Cannot prevent session stopping.** Workaround (`client.session.prompt()`) is fragile with race conditions in `run` mode (issue #15267). Feature request exists (issue #12472).
3. **Subagent hook bypass** — `tool.execute.before`/`after` does NOT fire for tool calls within subagents (issue #5894). Security/guardrail gap.
4. **No JSONL transcript** — Session data in SQLite (`~/.local/share/opencode/opencode.db`), not JSONL files. Access via SDK client API only. Cannot reuse Claude Code's transcript parsing logic directly.
5. **Compaction hook is experimental** — `experimental.session.compacting` prefix means it may change without notice.
6. **Context injection is experimental** — `experimental.chat.system.transform` is the recommended approach but is also experimental.
7. **No Notification hooks** — No equivalent to Claude Code's Notification event.
8. **Plugin API may evolve** — v1.2.x is stable but plugin API could change.
9. **Native .claude/ compat** — Users may not need dist/ for skills at all.
10. **$ARGUMENTS not standardized** — Skills using `$ARGUMENTS` work in Claude Code but behavior undefined in OpenCode.
11. **BashOutput deduplicated** — OpenCode uses `bash` for both; set `bash: true` once.
12. **Agent mode field** — `all` (default) = everywhere; `subagent` = spawned only; `primary` = top-level only.
13. **TaskCreate ≠ Agent** — Claude Code's TaskCreate/TaskUpdate/TaskGet/TaskList are todo management tools (map to `todowrite`/`todoread`), NOT subagent tools. Only `Agent` maps to `task`.
14. **apply_patch vs edit/write** — GPT models get `apply_patch` instead of `edit`/`write`. Non-GPT models (Anthropic, etc.) get `edit`/`write`. The swap is automatic in OpenCode's registry.
15. **tui.prompt.append is NOT context injection** — It fills the TUI input field, not system messages. Use `experimental.chat.system.transform` for system context.
16. **Model tier routing is Claude Code-only** — `execution-modes/efficient.md` references Claude model names (haiku, sonnet, opus). Replace all with `inherit` during sync. OpenCode is provider-agnostic — all tiers use the session model. Execution mode parallelism, loop limits, and gate-skipping still apply.
