# OpenCode CLI Conversion Guide

Reference for converting Claude Code plugin components to OpenCode format.

## Tool Name Mapping

Claude Code agents declare tools in comma-separated string arrays. OpenCode agents use a boolean object format with lowercase names.

| Claude Code Tool | OpenCode Tool | Notes |
|-----------------|--------------|-------|
| Bash | bash | Direct equivalent |
| BashOutput | bash | Same tool — OpenCode doesn't distinguish |
| Read | read | Direct equivalent |
| Write | write | Direct equivalent (create/overwrite) |
| Edit | edit | Both do string replacement |
| Grep | grep | Both use ripgrep |
| Glob | glob | Direct equivalent |
| WebFetch | webfetch | Lowercase, no space |
| WebSearch | websearch | Lowercase, no space |
| Task | task | Both spawn subagents |
| TaskCreate | task | Same as Task |
| Skill | skill | Both load skills |
| TodoWrite | todowrite | Direct equivalent |
| TodoRead | todoread | Direct equivalent |
| NotebookEdit | (no equivalent) | Not available in OpenCode |
| AskUserQuestion | question | User interaction |

Additional OpenCode-only tools:
- `list` — directory listing
- `lsp` — Language Server Protocol integration
- `patch` — patch application
- `codesearch` — semantic code search
- `multiedit` — batch multi-file editing

## Agent Frontmatter Conversion

Claude Code agent format:
```yaml
---
description: Agent purpose description
tools: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill
---
```

OpenCode agent format:
```yaml
---
description: Agent purpose description
mode: subagent
model: claude-sonnet-4-20250514
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
  todowrite: true
---
```

Additional optional agent fields:
- `prompt` — system prompt override (string)
- `steps` — max agentic turns (integer)
- `top_p` — nucleus sampling (float)
- `color` — terminal display color (string)
- `hidden` — hide from agent listings (boolean)
- `disable` — disable agent without deleting (boolean)
- `permission` — per-tool access control object

Conversion rules:
1. Keep `description` as-is
2. Add `mode` field — use `subagent` for agents spawned by other agents, `primary` for top-level agents, or `all` (default) for agents available in both contexts
3. Convert `tools` from comma-separated string to boolean object
4. Lowercase all tool names
5. BashOutput maps to bash (deduplicate — just set `bash: true` once)
6. Task and TaskCreate both map to `task: true`
7. Keep prompt body (everything below frontmatter) unchanged
8. Optionally add `permission` block for tool-level access control:
   ```yaml
   permission:
     bash: "ask"
   ```
9. Optionally add `model`, `temperature`, `steps`, and other overrides

### Tool Restriction Pattern

Claude Code uses an explicit allow-list (only declared tools available). OpenCode's boolean object works the same way — tools set to `true` are available, tools not listed or set to `false` are unavailable:

```yaml
tools:
  bash: true
  read: true
  write: false    # explicitly disabled
  # edit not listed = not available
```

## Hook Portability

**Critical: Claude Code Python hooks CANNOT run directly in OpenCode.** OpenCode plugins are JavaScript/TypeScript ONLY.

### Why Hooks Are Not Automatable

Claude Code hooks are Python scripts using JSON stdin/stdout. OpenCode hooks are JS/TS modules exporting async functions with a completely different API:

```typescript
import { Plugin } from "opencode"

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: {
      "tool.execute.before": async (input, output) => {
        // input.tool = tool name, input.args = tool arguments
        // output.abort = "reason" to block the tool call
        // return to allow
      },
      "tool.execute.after": async (input, output) => {
        // input.tool = tool name
        // output.title, output.output, output.metadata available
      }
    }
  }
}
```

**Blocking pattern**: Set `output.abort = "reason string"` to block a tool call (replaces throwing an error).

### Event Mapping

| Claude Code Event | OpenCode Event | Semantics |
|-------------------|---------------|-----------|
| PreToolUse | tool.execute.before | Block via `output.abort = "reason"` |
| PostToolUse | tool.execute.after | React to result |
| Stop | session.complete | Session completion |
| SessionStart | session.created | Session lifecycle |
| SessionEnd | session.ended | Session lifecycle |
| PreCompact | (no direct equivalent) | Gap |
| Notification | (no equivalent) | Gap |
| SubagentStart/Stop | (no equivalent) | Gap |
| PermissionRequest | permission.requested | Permission lifecycle |
| UserPromptSubmit | message.created | Before message processing |

Additional OpenCode events (no Claude Code equivalent):
- `tool.result.transform` — modify tool output before model sees it
- `message.transform` — modify messages before sending
- `model.request.before` / `model.request.after` — LLM API lifecycle
- `file.read.before` / `file.write.before` — file operation hooks
- `experimental.chat.system.transform` — modify system prompt
- `experimental.session.compacting` — context compression hook

### What Can Be Generated

For each Claude Code hook, the /sync-tools skill should generate:
1. A **hook stub** — JS/TS file with the correct OpenCode plugin structure, event bindings, and comments describing the behavioral intent
2. A **behavioral spec** — markdown document explaining what the hook does, what events it responds to, what decisions it makes, and what state it tracks

The actual JS/TS implementation requires manual porting by a developer. The stub + spec give them a head start.

### Hook Installation

OpenCode plugins are installed as npm packages or local file paths in `opencode.json`:

```json
{
  "plugins": {
    "manifest-dev-hooks": "./plugins/manifest-dev/index.ts"
  }
}
```

Or via npm:
```json
{
  "plugins": {
    "manifest-dev-hooks": "manifest-dev-opencode-hooks"
  }
}
```

## Directory Structure

OpenCode has native `.claude/` directory compatibility — it reads `.claude/skills/` and can use `.claude/agents/` with Claude-compatible markdown format. However, for a proper OpenCode distribution:

```
manifest-dev-opencode/
├── skills/                     # Skills (SKILL.md copied unchanged)
│   ├── define/
│   │   └── SKILL.md
│   ├── do/
│   │   └── SKILL.md
│   └── verify/
│       └── SKILL.md
├── agents/                     # Agents (converted frontmatter)
│   ├── code-bugs-reviewer.md
│   └── criteria-checker.md
├── hooks/
│   ├── index.ts                # Hook stubs (manual implementation needed)
│   └── HOOK_SPEC.md            # Behavioral specification for manual porting
└── README.md
```

OpenCode config directory: `.opencode/` (with plural subdirectory names: `skills/`, `agents/`, `plugins/`).

OpenCode skill discovery paths (in precedence order):
1. `.opencode/skills/` — OpenCode-specific project skills
2. `.claude/skills/` — Claude Code compatibility (read natively)
3. `.agents/skills/` — Agent Skills open standard path

OpenCode agent discovery:
1. `.opencode/agents/` — OpenCode-specific agents
2. `.claude/agents/` — reads Claude-format agents (but may not parse all frontmatter correctly)

## Installation

For skills only (using npx skills universal installer):
```bash
npx skills add <github-url> --skill <skill-name> -a opencode
```

For the full distribution (skills + converted agents + hook stubs):
Copy the dist/opencode/ directory contents to your project:
```bash
cp -r dist/opencode/skills/* .opencode/skills/
cp -r dist/opencode/agents/* .opencode/agents/
# Hook stubs require manual implementation — see hooks/HOOK_SPEC.md
```

## Skill Handling

SKILL.md files are copied unchanged per the Agent Skills Open Standard (agentskills.io). OpenCode implements the same spec as Claude Code.

Skill subdirectories (scripts/, references/, assets/) are copied recursively.

OpenCode reads `.claude/skills/` natively, so Claude Code SKILL.md files already work in OpenCode without any conversion. The dist/ output provides a standalone copy for users who prefer `.opencode/skills/` or `.agents/skills/` placement.

## Skill Chaining

Claude Code's define → do → verify → done chain uses the Skill tool to invoke skills by name. OpenCode has a `skill` tool with the same semantics. Skill chaining is supported — agents can load skills via `skill({ name: "git-release" })` during execution.

OpenCode's Task tool also supports category-based routing for subagent delegation, which is compatible with Claude Code's Task-based subagent spawning.

## Known Limitations

1. **Hooks require manual JS/TS rewrite** — the most significant limitation. Claude Code's Python hooks cannot be automatically converted. Generated stubs provide structure and behavioral spec, but implementation requires a developer. OpenCode plugins use Bun runtime (JS/TS only).
2. **25+ hook events vs Claude Code's ~17** — OpenCode has more hook events, including experimental ones. The mapping covers the core workflow hooks.
3. **No PreCompact equivalent** — OpenCode has `experimental.session.compacting` but it's experimental and may change.
4. **No Notification hooks** — OpenCode has no equivalent to Claude Code's Notification event.
5. **No SubagentStart/Stop** — subagent lifecycle not exposed via hooks.
6. **Plugin API stability** — OpenCode's plugin API may evolve; generated stubs target the current API. Block pattern uses `output.abort` (not throw).
7. **BashOutput not a separate tool** — OpenCode uses `bash` for both; deduplicate in tool objects.
8. **Native .claude/ compat means skills may already work** — users might not need the dist/ at all for skills. The value is in converted agents and hook behavioral specs.
9. **Agent mode field** — `mode: all` (default) makes agent available everywhere; `mode: subagent` restricts to spawned contexts; `mode: primary` restricts to top-level. Converted agents should use `subagent` unless they're meant to be user-facing.
