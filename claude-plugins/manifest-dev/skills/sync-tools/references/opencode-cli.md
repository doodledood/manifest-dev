# OpenCode CLI Conversion Guide

Reference for converting Claude Code plugin components to OpenCode format (anomalyco/opencode v1.2.15, March 2026).

## Conversion Summary

| Component | Phase 1 (Deterministic) | Phase 2 (LLM) |
|-----------|------------------------|----------------|
| Skills | Copy unchanged | — |
| Agents | Frontmatter conversion (tool map + format) | Temperature/mode inference, description enrichment |
| Hooks | Generate plugin skeleton with event bindings | Port Python logic to TypeScript |
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
| Agent / Task / TaskCreate | `task` | All map to task (subagent spawning) |
| Skill | `skill` | Both load skills |
| TodoWrite | `todowrite` | Direct equivalent |
| TodoRead | `todoread` | Direct equivalent |
| NotebookEdit | (no equivalent) | Not available in OpenCode |
| AskUserQuestion | `question` | User interaction |

OpenCode-only tools (no Claude Code equivalent):
- `list` — directory listing
- `lsp` — Language Server Protocol (experimental)
- `patch` — patch application
- `multiedit` — batch multi-file editing
- `codesearch` — semantic code search (requires Exa AI)

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
3. Deduplicate: BashOutput → bash (just set `bash: true` once), TaskCreate → task
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

Claude Code hooks are Python scripts using JSON stdin/stdout. OpenCode hooks are JS/TS modules using `@opencode-ai/plugin`.

**Plugin skeleton**:
```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const ManifestDevPlugin: Plugin = async (ctx) => {
  // ctx.project, ctx.client, ctx.$, ctx.directory
  return {
    "tool.execute.before": async ({ tool, sessionID, callID }, { args }) => {
      // Block: set args.abort = "reason"
      // Modify args: mutate args object
    },
    "tool.execute.after": async ({ tool, sessionID, callID }, { title, output, metadata }) => {
      // React to tool result
    },
    "session.created": async (event) => {
      // Session lifecycle
    },
    "session.idle": async (event) => {
      // Session went idle
    },
  }
}
```

**Event mapping (Claude Code → OpenCode)**:

| Claude Code Event | OpenCode Event | Blocking | Notes |
|-------------------|---------------|----------|-------|
| PreToolUse | `tool.execute.before` | Yes (mutate args to abort) | Check `tool` name, modify `args` |
| PostToolUse | `tool.execute.after` | No (react only) | Read `output`, `metadata` |
| Stop | `session.idle` | No | Session completion |
| SessionStart | `session.created` | No | Session lifecycle |
| PreCompact | `experimental.session.compacting` | No | Experimental |
| Notification | (no equivalent) | — | Gap |
| SubagentStart/Stop | (no equivalent) | — | Gap |

Additional OpenCode events (no Claude Code equivalent):
- `command.executed`, `file.edited`, `file.watcher.updated`
- `message.updated`, `message.removed`, `message.part.updated`, `message.part.removed`
- `permission.asked`, `permission.replied`
- `session.compacted`, `session.deleted`, `session.diff`, `session.error`, `session.status`, `session.updated`
- `shell.env` — inject environment variables: `output.env.KEY = "value"`
- `todo.updated`, `server.connected`, `installation.updated`
- `lsp.client.diagnostics`, `lsp.updated`
- `tui.prompt.append`, `tui.command.execute`, `tui.toast.show`
- `chat.message`, `chat.params` — modify messages/model params
- `tool.definition` — mutate tool descriptions/schemas

**Plugin installation**:
```json
// opencode.json
{ "plugin": ["./plugins/manifest-dev/index.ts"] }
```
Or: `.opencode/plugins/index.ts` (auto-discovered).

Dependencies: `.opencode/package.json` with `@opencode-ai/plugin` — OpenCode auto-installs via Bun.

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
│   ├── index.ts                # Hook plugin (manual implementation)
│   └── HOOK_SPEC.md            # Behavioral specification
├── tools/                      # Custom tools (if any)
├── opencode.json               # MCP config snippet
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

# Plugins (hook stubs — manual implementation needed)
cp -r dist/opencode/plugins/* .opencode/plugins/
# Then: cd .opencode && bun install @opencode-ai/plugin
```

## Skill Chaining

Claude Code's define → do → verify → done chain uses the Skill tool. OpenCode has a `skill` tool with same semantics. Skill chaining works — agents invoke skills via `skill({ name: "skill-name" })`.

OpenCode's `task` tool also supports subagent delegation, compatible with Claude Code's Task-based spawning.

## Known Limitations

1. **Hooks require manual JS/TS rewrite** — Python hooks cannot run in Bun. Generated stubs provide structure; HOOK_SPEC.md provides behavioral intent.
2. **No PreCompact equivalent** — `experimental.session.compacting` exists but is experimental.
3. **No Notification hooks** — No equivalent to Claude Code's Notification event.
4. **Plugin API may evolve** — v1.2.x is stable but plugin API could change.
5. **Native .claude/ compat** — Users may not need dist/ for skills at all.
6. **Block pattern** — Use `args.abort = "reason"` or mutate args to block tool calls (NOT throw).
7. **$ARGUMENTS not standardized** — Skills using `$ARGUMENTS` work in Claude Code but behavior undefined in OpenCode.
8. **BashOutput deduplicated** — OpenCode uses `bash` for both; set `bash: true` once.
9. **Agent mode field** — `all` (default) = everywhere; `subagent` = spawned only; `primary` = top-level only.
