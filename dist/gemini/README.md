# manifest-dev for Gemini CLI

Verification-first manifest workflows adapted for Google's Gemini CLI.

## Installation

```bash
# Install as Gemini extension
gemini extensions install https://github.com/doodledood/manifest-dev/dist/gemini

# Or link locally for development
gemini extensions link ./dist/gemini
```

For skills only (universal installer):
```bash
npx skills add https://github.com/doodledood/manifest-dev --all -a gemini
```

## Feature Parity

| Component | Status | Notes |
|-----------|--------|-------|
| Skills (define, do, verify, done, escalate) | Full | SKILL.md copied unchanged — universal format |
| Agents (11 reviewers + checkers) | Full | Frontmatter converted, tool names mapped, prompts unchanged |
| Hooks (stop, verify-gate, compact-recovery) | Full | Adapted to Gemini JSON protocol (top-level decision/systemMessage) |
| Skill chaining (define -> do -> verify -> done) | Likely works | activate_skill is model-controlled; not explicitly documented by Gemini |

## Setup

Enable experimental agents in `.gemini/settings.json`:
```json
{
  "experimental": {
    "enableAgents": true
  }
}
```

Merge `hooks/hooks-config.json` into your `.gemini/settings.json` hooks section.

## Components

### Skills
Copied unchanged from Claude Code plugin. The Agent Skills Open Standard (agentskills.io) ensures universal compatibility.

### Agents
11 agents with tool names converted to Gemini equivalents:

| Claude Code Tool | Gemini Tool |
|-----------------|-------------|
| Bash/BashOutput | run_shell_command |
| Read | read_file |
| Grep | grep_search |
| Glob | glob |
| WebFetch | web_fetch |
| WebSearch | google_web_search |
| Skill | activate_skill |
| Task/TaskCreate | (dropped — subagents are named tools) |

### Hooks
Python hooks adapted for Gemini's JSON protocol:
- **stop_do_hook.py** — Blocks premature stops during /do workflow
- **pretool_verify_hook.py** — Context reminder before /verify
- **post_compact_hook.py** — Restores /do context after compaction
- **gemini_adapter.py** — General-purpose Claude-to-Gemini output adapter
- **hook_utils.py** — Shared transcript parsing utilities

## Known Limitations

1. **Agents are experimental** — Require `experimental.enableAgents: true`. API may change.
2. **YOLO mode** — Gemini subagents run without per-tool confirmation.
3. **No SubagentStart/Stop hooks** — Cannot intercept subagent lifecycle events.
4. **Task/TaskCreate dropped** — Agents that spawn subagents need each spawned agent as a separate file.
5. **Skill chaining undocumented** — define->do->verify->done chain may not work reliably.
6. **Progressive disclosure gaps** — Gemini loads all skill resources at activation, not on-demand.
7. **Hook adapter needed for custom hooks** — Use gemini_adapter.py for any new Claude Code hooks.

## Keeping Up to Date

This distribution is generated from the Claude Code plugin source. When the source changes, regenerate by running `/sync-tools` in the Claude Code plugin, or manually copy updated files.
