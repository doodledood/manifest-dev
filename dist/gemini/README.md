# manifest-dev for Gemini CLI

Verification-first manifest workflows for Gemini CLI. Define tasks with acceptance criteria, execute against them, verify with parallel agents.

## Components

| Type | Count | Details |
|------|-------|---------|
| Skills | 6 | define, do, verify, done, escalate, learn-define-patterns |
| Agents | 12 | criteria-checker, manifest-verifier, 8 code reviewers, docs-reviewer, define-session-analyzer |
| Hooks | 3 | pretool-verify, stop-do-enforcement, post-compact-recovery |

## Install

### Option 1: Remote installer (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash
```

### Option 2: Skills only (via npx)

```bash
npx skills add https://github.com/doodledood/manifest-dev --all -a gemini-cli
```

### Option 3: Gemini extensions

```bash
gemini extensions install https://github.com/doodledood/manifest-dev/dist/gemini
# Or link locally:
gemini extensions link ./dist/gemini
```

## Required Configuration

Enable agents in your `~/.gemini/settings.json`:

```json
{
  "experimental": {
    "enableAgents": true
  }
}
```

Merge `hooks/hooks.json` into your settings.json hooks section for full workflow enforcement.

## Feature Parity

| Feature | Claude Code | Gemini CLI | Notes |
|---------|------------|------------|-------|
| Skills (6) | Full | Full | Copied unchanged; `name` + `description` frontmatter only |
| Agents (12) | Full | Full | Frontmatter converted (tool mapping, added kind/temperature/max_turns/timeout_mins) |
| Hooks (3) | Full | Full | Adapter translates protocol; exit codes, matchers, transcript format handled |
| Subagent spawning | `Agent` tool | Named tool per agent | Each agent becomes a callable tool by its registered name |
| Todo management | TaskCreate/Update/Get/List | `write_todos` | Single tool for all todo operations |
| File search | `Grep` | `grep_search` | Canonical name from source code (NOT `search_file_content`) |
| Web search | `WebSearch` | `google_web_search` | Google Search integration |
| Skill invocation | `Skill` | `activate_skill` | Agent-only; not manually invocable |
| Team management | TeamCreate/SendMessage | Not supported | No equivalent in Gemini CLI |
| Worktrees | EnterWorktree | Not supported | No equivalent in Gemini CLI |

## Hook Protocol Details

The adapter (`hooks/gemini_adapter.py`) translates between Claude Code and Gemini CLI hook protocols.

### Event Mapping

| Hook | Claude Event | Gemini Event | Matcher | Blocking |
|------|-------------|-------------|---------|----------|
| pretool-verify | PreToolUse | BeforeTool | `activate_skill` (regex) | Exit 0 always; injects additionalContext |
| stop-do-enforcement | Stop | AfterAgent | (all -- no matcher) | Exit 0=allow, Exit 2=block with retry |
| post-compact-recovery | SessionStart | SessionStart | `resume` (exact match on source field) | Exit 0 always; injects additionalContext |

### Exit Code Semantics

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| 0 | Allow | Parse stdout for JSON output |
| 1 | Non-blocking warning | stderr = warning text, execution continues |
| 2+ | Blocking | stderr = reason; behavior depends on event type |

### AfterAgent Deny/Retry Protocol

When `stop-do-enforcement` blocks a premature stop:

1. Exit code 2 with JSON on stdout (`decision: "deny"`, `hookSpecificOutput.clearContext: true`)
2. stderr contains the reason, which Gemini uses as a new prompt for the agent to correct
3. `clearContext: true` clears LLM memory from the rejected turn (forces re-reading file state)
4. Next AfterAgent input has `stop_hook_active: true` indicating a retry sequence
5. The hook implements loop detection (3+ consecutive short outputs) to avoid infinite retries

### Matcher Syntax

| Event Type | Matcher Behavior |
|------------|-----------------|
| Tool events (BeforeTool, AfterTool) | Regex against `tool_name`; falls back to exact match if regex invalid |
| Lifecycle events (SessionStart) | Exact string equality against source/reason field |
| Empty or `"*"` | Matches all events of that type |
| No matcher field | Matches all events of that type |

### Transcript Format

Gemini CLI uses JSONL at `transcript_path`:

```
{"type":"session_metadata","sessionId":"...","startTime":"..."}
{"type":"user","id":"msg1","content":[{"text":"Hello"}]}
{"type":"gemini","id":"msg2","content":[{"text":"Response"}]}
{"type":"message_update","id":"msg2","tokens":{"input":10,"output":5}}
```

The adapter patches `"gemini"` record types to `"assistant"` for Claude hook compatibility.

### Context Injection

- `additionalContext` is plain text (no XML tags needed)
- The adapter strips `<system-reminder>` wrappers that Claude hooks produce
- For SessionStart: injected as first turn in conversation history
- For BeforeTool: appended to tool context

## Agent Tool Mapping

Tools converted from Claude Code names to Gemini CLI equivalents:

| Claude Code | Gemini CLI | Notes |
|------------|------------|-------|
| Bash / BashOutput | `run_shell_command` | Deduplicated to single tool |
| Read | `read_file` | 1-based lines (start_line/end_line) |
| Write | `write_file` | Requires approval |
| Edit | `replace` | old_string/new_string + allow_multiple |
| Grep | `grep_search` | Canonical name (not search_file_content) |
| Glob | `glob` | Same |
| WebFetch | `web_fetch` | Rate-limited |
| WebSearch | `google_web_search` | Google Search |
| Skill | `activate_skill` | Agent-only |
| TaskCreate/Update/Get/List | `write_todos` | Single tool for all todo ops |

## Workflow

```
/define -> produces manifest with acceptance criteria
    |
/do -> executes against manifest, tracks progress
    |
/verify -> parallel verification with 12 specialized agents
    |
/done (all pass) or /escalate (blocked)
```

## Known Limitations

1. **Agents are experimental** -- Require `enableAgents` flag. API may change.
2. **No SubagentStart/Stop hooks** -- Cannot intercept subagent lifecycle.
3. **Agent tool is name-based** -- Each subagent becomes a tool by its registered name. No generic `delegate_to_agent`.
4. **$ARGUMENTS not supported** -- Claude Code skill extension only.
5. **`grep_search` is canonical** -- Source code defines `GREP_TOOL_NAME = 'grep_search'`. Docs showing `search_file_content` are stale.
6. **`generalist` not `generalist_agent`** -- Built-in subagent tool name is `generalist`.
7. **JSONL transition** -- Older sessions may use monolithic JSON format.

## Repository

Main repo: [github.com/doodledood/manifest-dev](https://github.com/doodledood/manifest-dev)

This distribution is auto-generated from the Claude Code plugin source. See the main repo for documentation, issues, and contributions.
