# Gemini CLI Conversion Guide

Reference for converting Claude Code plugin components to Gemini CLI format (v0.31.0 stable, March 2026).

## Conversion Summary

| Component | Phase 1 (Deterministic) | Phase 2 (LLM) |
|-----------|------------------------|----------------|
| Skills | Copy unchanged | — |
| Agents | Frontmatter conversion (tool map + add fields) | — |
| Hooks | Generate adapter + hooks.json config | Adapt complex hook logic |
| Commands | Convert to TOML format | — |
| Extension manifest | Generate gemini-extension.json | — |
| Context file | Rename CLAUDE.md → GEMINI.md | — |

## Phase 1: Deterministic Conversions

### Tool Name Mapping (Lookup Table)

| Claude Code Tool | Gemini CLI Tool | Notes |
|-----------------|-----------------|-------|
| Bash / BashOutput | `run_shell_command` | Requires approval |
| Read | `read_file` | 1-based lines (`start_line`/`end_line` params) |
| Write | `write_file` | Requires approval |
| Edit | `replace` | Uses `old_string`/`new_string` + `allow_multiple` |
| Grep | `grep_search` | Canonical name from source code. Docs index may show stale `search_file_content` — ignore that |
| Glob | `glob` | Same |
| WebFetch | `web_fetch` | Rate-limited |
| WebSearch | `google_web_search` | Google Search |
| Skill | `activate_skill` | Agent-only, not manually invocable |
| TodoWrite / TodoRead | `write_todos` | Single tool for both read and write |
| TaskCreate / TaskUpdate | `write_todos` | Task management maps to todos (single tool) |
| TaskGet / TaskList | `write_todos` | Task reads also via `write_todos` |
| TaskOutput | (no equivalent) | No background task output retrieval |
| TaskStop | (no equivalent) | No background task management |
| Agent | (subagent name as tool) | Subagents become tools by their registered name |
| AskUserQuestion | `ask_user` | Interactive dialog |
| EnterPlanMode | `enter_plan_mode` | Direct equivalent |
| ExitPlanMode | `exit_plan_mode` | Direct equivalent |
| EnterWorktree | (no equivalent) | No worktree support |
| TeamCreate / TeamDelete / SendMessage | (no equivalent) | No team management |
| ListMcpResourcesTool / ReadMcpResourceTool | (no equivalent) | MCP handled differently |

Gemini-only tools (no Claude Code equivalent):
- `list_directory` — directory listing with ignore/filter options
- `read_many_files` — read/concatenate multiple files (user-triggered via @ syntax)
- `save_memory` — saves facts to GEMINI.md
- `get_internal_docs` — Gemini CLI's own docs

Gemini built-in subagents (registered as tools by name):
- `codebase_investigator` — deep repo analysis subagent (enabled by default)
- `cli_help` — CLI help subagent (enabled by default)
- `generalist` — general-purpose subagent (enabled by default). NOTE: tool name is `generalist`, NOT `generalist_agent`
- `browser_agent` — web browser automation (experimental, disabled by default, requires Chrome 144+)

### Agent Frontmatter Conversion

Claude Code agent format:
```yaml
---
description: Agent purpose description
tools: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill
model: inherit
---
```

Gemini CLI agent format:
```yaml
---
name: agent-name
description: Agent purpose description
kind: local
tools:
  - run_shell_command
  - glob
  - grep_search
  - read_file
  - web_fetch
  - google_web_search
  - activate_skill
  - write_todos
model: inherit
temperature: 0.2
max_turns: 15
timeout_mins: 5
---
```

**Complete Gemini CLI local agent frontmatter fields**:

| Field | Type | Required | Default | Valid Values |
|-------|------|----------|---------|--------------|
| `name` | string | Yes | — | Lowercase letters, numbers, hyphens, underscores |
| `description` | string | Yes | — | Free text |
| `kind` | string | No | `local` | `local`, `remote` |
| `tools` | string[] | No | all tools | List of internal tool names |
| `model` | string | No | `inherit` | Model ID or `inherit` |
| `temperature` | number | No | model default | 0.0 - 2.0 |
| `max_turns` | number | No | 15 | Positive integer |
| `timeout_mins` | number | No | 5 | Positive number |

**Phase 1 conversion rules** (deterministic):
1. Add `name` field from filename (lowercase, hyphens OK)
2. Keep `description` as-is
3. Add `kind: local`
4. Convert `tools` from comma-separated PascalCase string to YAML list of internal tool names
5. Deduplicate: BashOutput → run_shell_command (listed once). Map TaskCreate/TaskUpdate/TaskGet/TaskList → `write_todos`. Map Agent → (dropped — subagents are registered as named tools, not via a generic tool)
6. Set `model: inherit` (or specific Gemini model if needed)
7. Add `max_turns: 15` and `timeout_mins: 5` (defaults)
8. Keep prompt body unchanged
9. Write to `agents/` in extension directory

**Subagent mechanism**: Subagents become tools by name. A subagent `security-auditor` becomes callable as tool `security-auditor`. No generic `delegate_to_agent` tool.

**File locations**: Project `.gemini/agents/*.md`, User `~/.gemini/agents/*.md`, Extension `agents/*.md`.

**Activation**: Requires `"experimental": { "enableAgents": true }` in settings.json.

### Hook Conversion

Gemini CLI hooks are external scripts communicating via JSON on stdin/stdout with exit code semantics.

**Event mapping (Claude Code → Gemini CLI)**:

| Claude Code Event | Gemini CLI Event | Can Block? | Notes |
|-------------------|-----------------|------------|-------|
| PreToolUse | `BeforeTool` | Yes (decision: deny) | Matcher: regex on tool names |
| PostToolUse | `AfterTool` | Yes (deny hides result) | Can chain tools via tailToolCallRequest |
| Stop | `AfterAgent` | Yes (deny forces retry) | reason becomes new prompt |
| SessionStart | `SessionStart` | No (advisory) | source: startup/resume/clear |
| PreCompact | `PreCompress` | No (advisory) | trigger: auto/manual |
| Notification | `Notification` | No | notification_type, message, details |

Additional Gemini events (no Claude Code equivalent):
- `SessionEnd` — reason: exit/clear/logout/prompt_input_exit/other
- `BeforeAgent` — after user prompt, before planning. Can block or inject context via additionalContext.
- `BeforeModel` — before LLM API request. Can mock LLM response via hookSpecificOutput.llm_response.
- `AfterModel` — after LLM response chunk. Can replace chunk via hookSpecificOutput.llm_response.
- `BeforeToolSelection` — filter available tools via hookSpecificOutput.toolConfig.allowedFunctionNames.

**Protocol**:
- Input: JSON on `stdin`
- Output: JSON on `stdout` (NOTHING else — debug on stderr only)
- Exit codes: 0 = success (parse stdout), 1 = non-blocking warning, 2+ = blocking (stderr = reason)

**Exit code 2+ behavior per event:**

| Event | Exit 2+ Behavior |
|-------|-----------------|
| BeforeTool | Blocks tool; stderr becomes deny reason sent to agent as tool error |
| AfterTool | Hides real tool output; stderr becomes replacement content |
| BeforeAgent | Blocks prompt; erases prompt from history |
| AfterAgent | **Triggers automatic retry**; stderr becomes feedback prompt for correction |
| BeforeModel | Aborts the turn; stderr used as error message |
| AfterModel | Discards response chunk; blocks the turn |

**Universal input** (all events):
```json
{
  "session_id": "string",
  "transcript_path": "string (path to JSONL session file)",
  "cwd": "string",
  "hook_event_name": "string",
  "timestamp": "string (ISO 8601)"
}
```

**Event-specific input fields:**

| Event | Additional Input Fields |
|-------|----------------------|
| BeforeTool | `tool_name`, `tool_input`, `mcp_context?`, `original_request_name?` |
| AfterTool | `tool_name`, `tool_input`, `tool_response: {llmContent, returnDisplay, error?}`, `mcp_context?` |
| BeforeAgent | `prompt` |
| AfterAgent | `prompt`, `prompt_response`, `stop_hook_active: boolean` |
| SessionStart | `source: "startup" \| "resume" \| "clear"` |
| SessionEnd | `reason: "exit" \| "clear" \| "logout" \| "prompt_input_exit" \| "other"` |
| PreCompress | `trigger: "manual" \| "auto"` |

**Universal output** (all optional):
```json
{
  "decision": "allow | deny | block | ask | approve",
  "reason": "string (feedback when denying — for AfterAgent, becomes new prompt)",
  "systemMessage": "string (displayed to user in terminal, NOT injected into model)",
  "continue": false,
  "stopReason": "string",
  "suppressOutput": true,
  "hookSpecificOutput": {}
}
```

**hookSpecificOutput by event:**

| Event | hookSpecificOutput Fields |
|-------|--------------------------|
| BeforeTool | `{hookEventName: "BeforeTool", tool_input?: Record}` — tool_input merges with/overrides model args |
| AfterTool | `{hookEventName: "AfterTool", additionalContext?: string, tailToolCallRequest?: {name, args}}` |
| BeforeAgent | `{hookEventName: "BeforeAgent", additionalContext?: string}` — appended to prompt for this turn |
| AfterAgent | `{hookEventName: "AfterAgent", clearContext?: boolean}` — clears LLM memory if true |
| SessionStart | `{hookEventName: "SessionStart", additionalContext?: string}` |

**Context injection (additionalContext) behavior:**

| Event | How additionalContext is injected |
|-------|----------------------------------|
| BeforeAgent | Appended to user's prompt for that turn only |
| AfterTool | Appended to tool result (alongside llmContent) |
| SessionStart | Interactive: injected as first turn in conversation history. Non-interactive: prepended to prompt |

Plain text format — no special tags needed. HTML-escaped by Gemini internally.

**AfterAgent deny/retry protocol:**
1. `decision: "deny"` rejects the model's response for that turn
2. `reason` field is sent as a **new prompt** to the agent for correction
3. `hookSpecificOutput.clearContext: true` clears LLM memory from rejected turn (forces reasoning from file state)
4. Next AfterAgent input will have `stop_hook_active: true` indicating retry sequence
5. **No built-in retry limit** — hooks must implement their own counter to avoid infinite loops

**Matcher syntax in hooks.json (settings.json):**

| Event Type | Matcher Behavior |
|------------|-----------------|
| Tool events (BeforeTool, AfterTool) | **Regex** against `tool_name`. Falls back to exact match if regex invalid. Examples: `"activate_skill"`, `"write_file\|replace"`, `"mcp__.*"` |
| Lifecycle events (SessionStart, etc.) | **Exact string equality** against trigger/source/reason field. Example: `"startup"` matches only source="startup" |
| Empty or `"*"` | Matches ALL events of that type |
| No matcher field | Matches ALL events of that type |

**Hook configuration** (`hooks/hooks.json` or `settings.json`):
```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "activate_skill",
        "sequential": true,
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${extensionPath}/hooks/script.py",
            "name": "friendly-name",
            "timeout": 60000,
            "description": "Purpose"
          }
        ]
      }
    ]
  }
}
```

**Transcript format (JSONL):**
Path: `~/.gemini/tmp/<project_hash>/chats/session-*.jsonl`
Record types (one JSON per line, append-only):
```
{"type":"session_metadata","sessionId":"...","projectHash":"...","startTime":"..."}
{"type":"user","id":"msg1","content":[{"text":"Hello"}]}
{"type":"gemini","id":"msg2","content":[{"text":"Hi there"}]}
{"type":"message_update","id":"msg2","tokens":{"input":10,"output":5}}
```
Note: JSONL transition (issue #15292) may still be in progress. Older sessions may use monolithic JSON. Tool call records within messages not fully documented yet.

**Env vars**: `GEMINI_PROJECT_DIR`, `GEMINI_SESSION_ID`, `GEMINI_CWD`, `CLAUDE_PROJECT_DIR` (compat).

**Precedence**: Project > User > System > Extension hooks.

**Adapter pattern for Claude Code hooks:**
Claude Code hooks can be wrapped with a thin adapter that:
- Translates Claude's `hookSpecificOutput.permissionDecision: "deny"` → Gemini's top-level `decision: "deny"`
- Maps Claude's `hookSpecificOutput.permissionDecisionReason` → Gemini's `reason`
- Passes Claude's `hookSpecificOutput.additionalContext` → Gemini's `hookSpecificOutput.additionalContext`
- For AfterAgent (stop hook): translates Claude's `decision: "block"` → Gemini's `decision: "deny"` with reason
- Maps Claude's `transcript_path` parsing to Gemini's JSONL format (message types: `user`/`gemini` instead of `user`/`assistant`)

### Skills Handling

SKILL.md files copy unchanged. Only `name` and `description` frontmatter recognized. Claude Code extensions silently ignored.

**Discovery**: Workspace `.gemini/skills/` or `.agents/skills/` → User `~/.gemini/skills/` → Extensions `skills/`.

### Extension Manifest

Generate `gemini-extension.json`:
```json
{
  "name": "manifest-dev",
  "version": "0.1.0",
  "description": "Verification-first manifest workflows for Gemini CLI",
  "mcpServers": {},
  "excludeTools": [],
  "settings": []
}
```

### Context File

Rename CLAUDE.md → GEMINI.md. Supports `@file.md` imports. AGENTS.md configurable as alternative via `context.fileName` in settings.json.

## Extension Directory Structure

```
dist/gemini/
├── gemini-extension.json
├── GEMINI.md
├── agents/
│   ├── code-bugs-reviewer.md
│   └── criteria-checker.md
├── hooks/
│   ├── hooks.json
│   ├── gemini_adapter.py
│   ├── hook_utils.py
│   ├── stop_do_hook.py
│   ├── pretool_verify_hook.py
│   └── post_compact_hook.py
├── skills/
│   ├── define/
│   │   └── SKILL.md
│   └── do/
│       └── SKILL.md
└── README.md
```

## Installation

```bash
gemini extensions install https://github.com/<org>/<repo>/dist/gemini
# Or link locally:
gemini extensions link ./dist/gemini
```

Skills only: `npx skills add <url> --all -a gemini-cli`

`install.sh` must merge `"experimental": { "enableAgents": true }` and the generated `hooks.json` entries into `~/.gemini/settings.json` additively. If users install via Gemini's native extension command instead of `install.sh`, document the equivalent manual settings changes separately.

## Extensions Gallery

Automated publishing: public GitHub repo + `gemini-cli-extension` topic + `gemini-extension.json` at root → daily crawler → gallery at geminicli.com/extensions/browse/.

## Namespacing

Install scripts handle all component renaming at install time via `install_helpers.py`. The `dist/gemini/` directory keeps original names — sync-tools writes originals, install scripts namespace.

**Pattern**: All components get `-manifest-dev` suffix:
- Skill dirs: `skills/define/` → `skills/define-manifest-dev/`
- Agent files: `code-bugs-reviewer.md` → `code-bugs-reviewer-manifest-dev.md`
- SKILL.md `name:` field patched to match directory name
- Content cross-references patched (slash commands, quoted strings, paths, agent names)

**Selective cleanup** (replaces `rm -rf` of shared dirs):
```bash
find "$DIR/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
find "$DIR/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
```

Component names on disk will have `-manifest-dev` suffix after install. The hooks directory is extension-private and doesn't need selective cleanup.
The installer must also merge Gemini settings additively: preserve existing settings, set `experimental.enableAgents = true`, and add manifest-dev hook registrations without duplicating existing user hooks.

## Context File Adaptation

During sync, replace remaining `CLAUDE.md` references that mean "this CLI's context file" with `GEMINI.md`:
- Agent content: any "CLAUDE.md" that refers to the project context file → `GEMINI.md`
- Context file (GEMINI.md): references to context file names
- README: references to context file names
- Skills (operational only): instructions like "write to CLAUDE.md" → "write to GEMINI.md". Leave research/reference content unchanged.
- Do NOT replace "CLAUDE.md" when it refers to Claude Code's own file (e.g., in comparative text or research).

The `context-file-adherence-reviewer` agent already uses generic "context file" language — no special handling needed for its content.

## Known Limitations

1. **Agents experimental** — Require enableAgents flag. API may change.
2. **No SubagentStart/Stop hooks** — Cannot intercept subagent lifecycle.
3. **Agent tool is name-based** — Each subagent becomes a tool by its registered name. No generic `delegate_to_agent` tool.
4. **Commands are TOML** — Not markdown.
5. **$ARGUMENTS not supported** — Claude Code extension only.
6. **`grep_search` is canonical** — Source code (`base-declarations.ts`) defines `GREP_TOOL_NAME = 'grep_search'`. The docs index page showing `search_file_content` is stale. Always use `grep_search`.
7. **`generalist` not `generalist_agent`** — The built-in subagent tool name is `generalist`, not `generalist_agent`.
8. **TaskCreate ≠ Agent** — Claude Code's TaskCreate/TaskUpdate/TaskGet/TaskList are todo management tools (map to `write_todos`), NOT subagent tools. Only `Agent` maps to subagent names.
9. **Model tier routing is Claude Code-only** — `BUDGET_MODES.md` references Claude model names (haiku, sonnet, opus). Replace all with `inherit` during sync. Gemini supports `model: inherit` natively. Execution mode parallelism, loop limits, and gate-skipping still apply.
