# Gemini CLI Conversion Guide

Reference for converting Claude Code plugin components to Gemini CLI format.

## Tool Name Mapping

Claude Code agents declare tools in YAML frontmatter arrays. Gemini CLI agents use different tool names in arrays.

| Claude Code Tool | Gemini CLI Tool | Notes |
|-----------------|----------------|-------|
| Bash | run_shell_command | Command execution |
| BashOutput | run_shell_command | Same tool, Gemini doesn't distinguish |
| Read | read_file | File reading |
| Write | write_file | File creation/overwrite |
| Edit | replace | String replacement editing |
| Grep | grep_search | Ripgrep-based content search (grep_search is current name; search_file_content is deprecated alias) |
| Glob | glob | Identical name |
| WebFetch | web_fetch | URL content fetching |
| WebSearch | google_web_search | Web search |
| Task | (subagent name) | Subagents are exposed as callable tools by name |
| TaskCreate | (subagent name) | Same as Task — subagent invocation |
| Skill | activate_skill | Skill loading |
| TodoWrite | write_todos | Todo/task management |
| TodoRead | (no equivalent) | Not available in Gemini |
| NotebookEdit | (no equivalent) | Not available in Gemini |
| AskUserQuestion | ask_user | User interaction |

Additional Gemini-only tools (available but no Claude equivalent):
- `list_directory` — directory listing
- `save_memory` — persistent memory across sessions
- `read_many_files` — batch file reading (user-triggered via @)
- `get_internal_docs` — internal documentation access
- `browser_agent` — web browsing
- `codebase_investigator` — built-in subagent for code analysis

## Agent Frontmatter Conversion

Claude Code agent format:
```yaml
---
description: Agent purpose description
tools: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill
---
```

Gemini CLI agent format:
```yaml
---
name: agent-slug
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
model: gemini-2.5-pro
temperature: 0.2
max_turns: 15
timeout_mins: 5
---
```

Remote agents (also experimental):
```yaml
---
kind: remote
name: my-remote-agent
agent_card_url: https://example.com/agent-card
---
```
Remote agents communicate via Agent-to-Agent (A2A) protocol. Not relevant for conversion but mentioned for completeness.

Conversion rules:
1. Add `name` field — kebab-case slug derived from filename (strip `.md`)
2. Keep `description` as-is
3. Add `kind: local` (required, all converted agents are local)
4. Convert `tools` from comma-separated string to YAML array with mapped names
5. Map each tool name per the table above
6. BashOutput maps to run_shell_command (deduplicate if Bash also present)
7. Task/TaskCreate → drop from tools list; instead, the agents this agent spawns must exist as separate agent files (Gemini subagents are tools by name)
8. Add `model`, `temperature`, `max_turns`, `timeout_mins` with sensible defaults
9. Agents require `experimental.enableAgents: true` in Gemini settings.json
10. Gemini agents run in YOLO mode (no per-tool confirmation) — warn in README
11. Management via `/agents list|refresh|enable|disable` commands

## Hook Protocol Adaptation

Claude Code and Gemini CLI hooks share the same execution model: JSON on stdin, JSON on stdout, any executable (Python, bash, Node.js), exit code 0 = success, exit code 2 = block.

### Input Fields (Nearly Identical)

| Field | Claude Code | Gemini CLI | Adaptation |
|-------|------------|------------|------------|
| session_id | session_id | session_id | None needed |
| transcript_path | transcript_path | transcript_path | None needed |
| cwd | cwd | cwd | None needed |
| event name | hook_event_name | hook_event_name | None needed |
| tool name | tool_name | tool_name | None needed |
| tool args | tool_input | tool_input | None needed |
| permission mode | permission_mode | (not present) | Ignore — not available |
| tool ID | tool_use_id | (not present) | Ignore — not available |
| timestamp | (not present) | timestamp | Extra field available |

### Output Fields (Key Divergence)

The critical difference is in how block/allow decisions are structured:

Claude Code output:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Blocked by manifest workflow"
  }
}
```

Gemini CLI output:
```json
{
  "decision": "deny",
  "reason": "Blocked by manifest workflow"
}
```

For context injection (non-blocking hooks), Claude Code uses:
```json
{
  "hookSpecificOutput": {
    "additionalContext": "Extra information for the model"
  }
}
```

Gemini CLI uses:
```json
{
  "systemMessage": "Extra information for the model"
}
```

### Adapter Pattern

A thin Python wrapper (~20 lines) normalizes Claude Code hook output to Gemini format:

```python
import json, sys, subprocess

# Run the original Claude Code hook
result = subprocess.run([sys.argv[1]], input=sys.stdin.read(), capture_output=True, text=True)

if result.returncode != 0:
    sys.exit(result.returncode)

claude_output = json.loads(result.stdout)
hook_specific = claude_output.get("hookSpecificOutput", {})

gemini_output = {}
if hook_specific.get("permissionDecision") == "deny":
    gemini_output["decision"] = "deny"
    gemini_output["reason"] = hook_specific.get("permissionDecisionReason", "")
if "additionalContext" in hook_specific:
    gemini_output["systemMessage"] = hook_specific["additionalContext"]
if "continue" in claude_output:
    gemini_output["continue"] = claude_output["continue"]

print(json.dumps(gemini_output))
```

### Event Name Mapping

| Claude Code Event | Gemini CLI Event | Notes |
|-------------------|-----------------|-------|
| PreToolUse | BeforeTool | Identical semantics — block/allow tool calls |
| PostToolUse | AfterTool | Identical semantics — react to results |
| Stop | AfterAgent | Gemini equivalent for agent completion |
| SessionStart | SessionStart | Identical |
| SessionEnd | SessionEnd | Identical |
| Notification | Notification | Identical |
| PreCompact | PreCompress | Same concept, different name |
| UserPromptSubmit | BeforeAgent | Gemini equivalent |
| (no equivalent) | BeforeModel | Gemini-only: fires before LLM API request |
| (no equivalent) | AfterModel | Gemini-only: fires after LLM API response |
| (no equivalent) | BeforeToolSelection | Gemini-only: fires before LLM selects tools |
| SubagentStart | (no equivalent) | Gap — Gemini has no subagent lifecycle hooks |
| SubagentStop | (no equivalent) | Gap |
| PermissionRequest | (no equivalent) | Gap |
| PostToolUseFailure | (no equivalent) | Gap |

### Hook Configuration

Claude Code hooks are in `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash", "hooks": ["python hooks/my_hook.py"] }]
  }
}
```

Gemini CLI hooks are in `.gemini/settings.json`:
```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "run_shell_command|replace",
        "sequential": true,
        "hooks": [
          {
            "type": "command",
            "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/my_hook.py",
            "name": "my-hook-name",
            "timeout": 60000,
            "description": "What this hook does"
          }
        ]
      }
    ]
  }
}
```

Key differences from Claude Code hook config:
- Gemini matchers use **regex** patterns (not exact tool names)
- Gemini matchers use Gemini tool names (run_shell_command, not Bash)
- Each hook entry has `type`, `command`, `name`, `timeout`, `description` fields
- `sequential: true` ensures hooks run in order (not parallel)
- `$GEMINI_PROJECT_DIR` env var available for path resolution
- Timeout default: 60000ms

## Directory Structure

Gemini CLI extension layout for converted manifest-dev components:

```
manifest-dev-gemini/
├── gemini-extension.json       # Extension manifest (required)
├── GEMINI.md                   # Context instructions
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
│   ├── hooks.json              # Hook configuration
│   ├── gemini_adapter.py       # Output format adapter
│   └── stop_do_hook.py         # Adapted hook scripts
└── README.md
```

The `gemini-extension.json` manifest:
```json
{
  "name": "manifest-dev",
  "version": "0.1.0",
  "description": "Verification-first manifest workflows for Gemini CLI"
}
```

## Settings Required

For agents (experimental):
```json
{
  "experimental": {
    "enableAgents": true
  }
}
```

Hooks are enabled by default (`hooksConfig.enabled: true`). Skills enabled by default (`skills.enabled: true`).

Full settings.json reference: tools.core (allowlist), tools.allowed (bypass confirmation), tools.exclude (block), security.disableYoloMode, security.blockGitExtensions.

## Installation

```bash
gemini extensions install <github-url-to-dist/gemini>
```

Or for local development:
```bash
gemini extensions link ./dist/gemini
```

## Skill Handling

SKILL.md files are copied unchanged per the Agent Skills Open Standard (agentskills.io). Both Claude Code and Gemini CLI implement the same spec.

Skill subdirectories (scripts/, references/, assets/) are copied recursively. Note: Gemini CLI has known interoperability gaps (GitHub Issue #15895):
- Flattens file structure, losing semantic distinction between scripts/references/assets
- Only implements progressive disclosure Levels 1-2 (dumps all resources at activation instead of on-demand Level 3)
- Ignores optional frontmatter fields (compatibility, allowed-tools, metadata)

These gaps don't block functionality — skills still load and work. The experience is slightly degraded (more tokens loaded upfront than necessary).

## Skill Chaining

Claude Code's define → do → verify → done skill chain relies on the Skill tool invoking skills by name. Gemini CLI has `activate_skill` which is model-controlled. Skill chaining likely works (the skill prompt is in conversation context and the model can call activate_skill again), but this is NOT explicitly documented by Gemini CLI. Monitor for issues.

## Known Limitations

1. **Agents are experimental** — require `experimental.enableAgents: true`. API may change.
2. **YOLO mode** — Gemini subagents run without per-tool confirmation. Users cannot gate individual tool calls within agents.
3. **No SubagentStart/Stop hooks** — cannot intercept subagent lifecycle events.
4. **No PermissionRequest hook** — cannot intercept permission prompts.
5. **Progressive disclosure gaps** — Gemini dumps all skill resources at activation rather than loading on demand.
6. **Skill chaining undocumented** — define→do→verify→done chain may not work reliably.
7. **Hook output format requires adapter** — cannot run Claude Code hooks directly; need the JSON output normalization wrapper.
8. **Task/TaskCreate tool has no direct equivalent** — agents that spawn subagents need restructuring; each spawned agent must be a named Gemini agent file.
9. **BashOutput not a separate tool** — Gemini uses run_shell_command for both Bash and BashOutput; deduplicate in tool lists.
