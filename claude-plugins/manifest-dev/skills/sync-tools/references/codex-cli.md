# Codex CLI Conversion Guide

Reference for converting Claude Code plugin components to Codex CLI format (v0.107.0, March 2026).

## Conversion Summary

| Component | Phase 1 (Deterministic) | Phase 2 (LLM) |
|-----------|------------------------|----------------|
| Skills | Copy unchanged | — |
| Agents | Generate TOML config stubs | Generate developer_instructions content |
| Hooks | Impossible (no hook system) | — |
| Multi-agent | Generate role TOML files | Infer per-role instructions |
| AGENTS.md | Generate from agents/CLAUDE.md | Enrich with workflow descriptions |
| Execution rules | Generate .rules stubs | — |
| MCP config | Generate config.toml snippet | — |

## Component Compatibility

| Component | Codex Support | Why |
|-----------|--------------|-----|
| Skills (SKILL.md) | YES — copy unchanged | Same open standard (agentskills.io) |
| Agents (markdown) | TOML stubs only | Codex uses TOML config with 2 tools (shell, apply_patch). Fundamentally incompatible paradigm. |
| Hooks (Python) | NO | Not shipped as of v0.107.0. Issue #2109 (434+ upvotes). OpenAI actively developing — expected mid-March 2026 experimental. |
| Commands | NO | Deprecated "custom prompts" replaced by skills. No command system. |

## Phase 1: Deterministic Conversions

### Skill Handling

SKILL.md files copy unchanged. Codex implements the Agent Skills Open Standard.

**Discovery paths** (priority order):
| Scope | Location |
|-------|----------|
| REPO (CWD) | `$CWD/.agents/skills/<name>/` |
| REPO (Parent) | Parent directories up to repo root |
| REPO (Root) | `$REPO_ROOT/.agents/skills/<name>/` |
| USER | `$HOME/.agents/skills/<name>/` |
| ADMIN | `/etc/codex/skills/<name>/` |
| SYSTEM | Bundled with Codex |

**Skill frontmatter** (open standard):
- `name` (required), `description` (required)
- `license`, `compatibility`, `metadata` (optional)
- Claude Code extensions (`user-invocable`, `tools`, `context`, `agent`, `hooks`) silently ignored

**Skill activation**: Explicit (`$skillname` or `/skills` menu) or implicit (auto-matching by description). Enabled by default since v0.97.0 with live detection.

**openai.yaml metadata** (optional, per-skill):
```yaml
# agents/openai.yaml (inside skill directory)
interface:
  display_name: "User-facing name"
  short_description: "Brief description"
  icon_small: "./assets/small-logo.svg"
  icon_large: "./assets/large-logo.png"
  brand_color: "#3B82F6"
  default_prompt: "Optional surrounding prompt"

policy:
  allow_implicit_invocation: false  # default: true

dependencies:
  tools:
    - type: "mcp"
      value: "serverIdentifier"
      description: "Tool description"
      transport: "streamable_http"
      url: "https://example.com/mcp"
```

**Skills config** (enable/disable in config.toml):
```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

### Agent Conversion → TOML Config Stubs

Claude Code agents cannot run as-is on Codex. Generate TOML config stubs that approximate the agent's role using Codex's multi-agent system.

**Codex multi-agent config** (in `.codex/config.toml`):
```toml
[features]
multi_agent = true

[agents]
max_threads = 6
max_depth = 1

[agents.code-reviewer]
description = "Reviews code for bugs, design issues, and test coverage"
config_file = "agents/code-reviewer.toml"
```

**Per-role TOML** (`agents/code-reviewer.toml`):
```toml
model = "gpt-5.3-codex"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
You are a code reviewer focused on correctness, security, and test coverage.
Review the code changes and report findings with severity levels.
"""
```

**Built-in roles** (user-defined override these):
| Role | Purpose |
|------|---------|
| `default` | General-purpose fallback |
| `worker` | Execution-focused implementation |
| `explorer` | Read-heavy codebase exploration |
| `monitor` | Long-running task monitoring |

**Per-role override fields**:
- `model` — model ID
- `model_reasoning_effort` — minimal/low/medium/high/xhigh
- `sandbox_mode` — read-only/workspace-write/danger-full-access
- `developer_instructions` — multi-line string (system prompt equivalent)

**Phase 1** (deterministic): Generate skeleton TOML with name, description from Claude Code agent frontmatter. Set `sandbox_mode: "read-only"` for review agents.

**Phase 2** (LLM): Generate `developer_instructions` content by summarizing the Claude Code agent's prompt body into Codex-appropriate instructions. Key differences: Codex has only `shell` and `apply_patch` tools — instructions must be reframed for this constraint.

### AGENTS.md Generation

Generate AGENTS.md describing all agents and the workflow:

```markdown
# manifest-dev Agents

## Workflow
This project uses a define→do→verify→done workflow. Skills handle the workflow;
agents listed below are used for verification.

## Code Review Agents
- **code-bugs-reviewer**: Audits for race conditions, data loss, edge cases, logic errors
- **code-design-reviewer**: Design fitness, reinvented wheels, under-engineering
...

## How to Use
These agents are informational. On Codex, use the multi-agent system with
TOML config files in agents/ to approximate scoped subagent behavior.
```

**AGENTS.md hierarchy** (Codex reads these):
1. Global: `~/.codex/AGENTS.md` (or `AGENTS.override.md`)
2. Project: walks DOWNWARD from git root to CWD, one file per directory
3. Merged: root-to-current, blank-line separated, capped at `project_doc_max_bytes` (default 32 KiB)

**Key config**:
```toml
project_doc_max_bytes = 32768
project_doc_fallback_filenames = ["CLAUDE.md"]  # to also read CLAUDE.md
```

### Execution Policy Rules

Generate `.rules` files for command safety patterns.

**File location**: `.codex/rules/default.rules`
**Language**: Starlark (Python-like, safe execution)

```starlark
# Allow git operations
prefix_rule(
    pattern = ["git"],
    decision = "allow",
    justification = "Git operations are safe",
)

# Prompt for destructive operations
prefix_rule(
    pattern = ["rm", ["-rf", "-fr"]],
    decision = "prompt",
    justification = "Destructive deletion requires confirmation",
)

# Block network-modifying commands
prefix_rule(
    pattern = ["iptables"],
    decision = "forbidden",
    justification = "Network modification not allowed",
)
```

**prefix_rule() fields**:
- `pattern` (REQUIRED): non-empty list, elements are literal strings or unions (`["view", "list"]`)
- `decision` (default "allow"): "allow" / "prompt" / "forbidden". Most restrictive wins.
- `justification` (optional): human-readable, shown in prompts/rejections
- `match` / `not_match` (optional): validation examples checked at load time

**Test**: `codex execpolicy check --pretty --rules .codex/rules/default.rules -- <command>`

### MCP Config

Generate config.toml snippet:

**STDIO server**:
```toml
[mcp_servers.myserver]
command = "npx"
args = ["-y", "package-name"]
env = { API_KEY = "value" }
startup_timeout_sec = 10
tool_timeout_sec = 60
enabled = true
```

**HTTP server**:
```toml
[mcp_servers.remote]
url = "https://server.example.com/mcp"
bearer_token_env_var = "API_TOKEN"
```

**Universal options**: `startup_timeout_sec` (default 10), `tool_timeout_sec` (default 60), `enabled` (default true), `required` (default false), `enabled_tools`, `disabled_tools`.

### Notify System (Limited Hook Alternative)

Codex has ONE event: `agent-turn-complete`. Fire-and-forget, no return channel.

```toml
notify = ["python3", "/path/to/notify.py"]
```

**JSON payload** (passed as argv[1], NOT stdin):
```json
{
  "type": "agent-turn-complete",
  "thread-id": "session-id",
  "turn-id": "turn-id",
  "cwd": "/working/directory",
  "input-messages": ["array"],
  "last-assistant-message": "text"
}
```

Cannot block, modify, or intercept. Observability only.

## Hook Status (Issue #2109)

**NOT shipped** as of v0.107.0 (March 2, 2026).
- Issue open with 54+ comments, 434+ upvotes
- 4 community PRs submitted and closed (#2904, #4522, #9796, #11067)
- OpenAI staff confirmed Feb 23: "actively working on it"
- Community: scaffolding exists in codebase since ~v0.99
- **Proposed events**: PreToolUse, PostToolUse/AfterToolUse, AfterAgent, SessionStart, Stop, Notification, PostCompact
- **Workaround**: Session logging via `CODEX_TUI_RECORD_SESSION=1` + polling

**When hooks ship**, the Codex distribution should expand to include adapted hooks. Monitor the issue.

## Config Hierarchy

Priority (highest to lowest):
1. CLI flags (`--model`, `--config key=value`)
2. Profile settings (`codex --profile <name>`)
3. Project `.codex/config.toml` (trusted projects only)
4. User `~/.codex/config.toml`
5. Built-in defaults

Admin enforcement: `requirements.toml` with `allowed_approval_policies`, `allowed_sandbox_modes`, etc.

## Directory Structure

```
dist/codex/
├── skills/                        # Skills (unchanged)
│   ├── define/
│   │   ├── SKILL.md
│   │   └── tasks/
│   └── do/
│       └── SKILL.md
├── agents/                        # TOML config per role
│   ├── code-reviewer.toml
│   └── explorer.toml
├── rules/                         # Execution policy
│   └── default.rules
├── config.toml                    # MCP + multi-agent config snippet
├── AGENTS.md                      # Agent descriptions + workflow guide
└── README.md
```

## Installation

Skills (universal installer):
```bash
npx skills add <github-url> --all
```

Codex skill-installer (within session):
```
$skill-installer --repo <url> --path skills/<name>
```

Manual:
```bash
# Skills
cp -r dist/codex/skills/* .agents/skills/

# TOML config (merge into your .codex/config.toml)
cat dist/codex/config.toml

# Agents
cp -r dist/codex/agents/* .codex/agents/

# Rules
cp -r dist/codex/rules/* .codex/rules/

# AGENTS.md
cp dist/codex/AGENTS.md ./AGENTS.md
```

## Skill Chaining

Skills can reference other skills via `$skillname` syntax and implicit activation. The define→do→verify→done chain is advisory without hooks — nothing enforces completion.

## Known Limitations

1. **Skills only for full compatibility** — Agents are TOML stubs, hooks impossible.
2. **No workflow enforcement** — Without hooks, the chain is advisory.
3. **Only 2 tools** — `shell` and `apply_patch`. Agent instructions must be reframed.
4. **No scoped subagents** — Multi-agent uses global sandbox. Per-agent tool restriction impossible.
5. **Skills may not chain reliably** — `$skillname` invocation less documented.
6. **AGENTS.md is informational only** — Describes agents but doesn't execute them as scoped subagents.
7. **Hooks expected soon** — Mid-March 2026 experimental release predicted. Will expand distribution significantly.
8. **$ARGUMENTS not supported** — Claude Code extension only.
9. **Notify is fire-and-forget** — Cannot block or modify agent behavior.
