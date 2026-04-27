# Codex CLI Conversion Guide

Reference for converting Claude Code plugin components to Codex CLI format (v0.107.0, March 2026).

## Conversion Summary

| Component | Phase 1 (Deterministic) | Phase 2 (LLM) |
|-----------|------------------------|----------------|
| Skills | Copy unchanged | — |
| Agents | Generate TOML with full prompt body as developer_instructions | — |
| Hooks | Impossible (no hook system) | — |
| Multi-agent | Generate role TOML files with full prompt bodies | — |
| AGENTS.md | Generate from agents/CLAUDE.md | Enrich with workflow descriptions |
| Execution rules | Generate .rules stubs | — |
| MCP config | Generate config.toml snippet | — |

## Component Compatibility

| Component | Codex Support | Why |
|-----------|--------------|-----|
| Skills (SKILL.md) | YES — copy unchanged | Same open standard (agentskills.io) |
| Agents (markdown) | TOML stubs only | Codex uses TOML config. Default tools are broader than previously assumed (6 default + experimental), but agent paradigm differs. |
| Hooks (Python) | NO | Not shipped as of v0.107.0. Issue #2109 (453+ upvotes). Multiple community PRs rejected ("by invitation only"). |
| Commands | NO | Deprecated "custom prompts" replaced by skills. No command system. |

## Codex CLI Tool Inventory

Codex has significantly more tools than just `shell` + `apply_patch`. Tool availability depends on model and feature flags.

### Tool Name Mapping (Claude Code → Codex)

| Claude Code Tool | Codex Tool | Notes |
|-----------------|------------|-------|
| Bash / BashOutput | `shell_command` | Default for codex models. Alternatives: `shell` (execvp), `exec_command` (PTY) |
| Read | `read_file` | Experimental — gated by model's `experimental_supported_tools` |
| Write | `shell_command` | No dedicated write tool — use shell `cat > file` |
| Edit | `apply_patch` | Freeform or JSON patch format |
| Grep | `grep_files` | Experimental — gated by model's `experimental_supported_tools` |
| Glob | `shell_command` | No dedicated glob — use shell `find`/`ls` |
| WebFetch | `shell_command` | No dedicated fetch — use shell `curl` |
| WebSearch | `web_search` | Default tool, cached or live mode |
| Skill | (skill system) | `$skillname` syntax or implicit activation |
| Agent | `spawn_agent` | Requires Feature::Collab flag |
| TaskCreate / TaskUpdate | `update_plan` | Always-on planning tool (simpler than Claude Code tasks) |
| TaskGet / TaskList | `update_plan` | Same tool — flat step list with status |
| TaskOutput | `wait` | Blocks on agent completion (requires Collab) |
| TaskStop | `close_agent` | Terminate agents (requires Collab) |
| TodoWrite / TodoRead | `update_plan` | `update_plan` is Codex's todo equivalent |
| AskUserQuestion | `request_user_input` | Always-on, structured user choice collection |
| NotebookEdit | (no equivalent) | Not available |
| EnterPlanMode / ExitPlanMode | (no equivalent) | No plan mode |
| EnterWorktree | (no equivalent) | No worktree support |
| TeamCreate / TeamDelete | (no equivalent) | Multi-agent uses spawn_agent, not teams |
| SendMessage | `send_input` | Message agents (requires Collab) |

### Default Tools (codex-optimized models: gpt-5-codex, gpt-5.1-codex)

These 6 tools are available by default without any feature flags:
1. **`shell_command`** — shell execution in user's default shell
2. **`update_plan`** — task planning/todo (flat step list with pending/in_progress/completed)
3. **`request_user_input`** — structured user interaction
4. **`apply_patch`** — code patch application (freeform or JSON)
5. **`web_search`** — web search (cached by default, configurable: disabled/cached/live)
6. **`view_image`** — local filesystem image viewing

### Experimental Tools (gated by model's `experimental_supported_tools`)

- **`read_file`** — file reading with 1-indexed lines, slice/block modes
- **`list_dir`** — directory listing with depth control
- **`grep_files`** — regex pattern search with glob filtering

These are NOT in the default tool set — availability controlled server-side per model config.

### Feature-Gated Tools

| Tool | Feature Flag | Purpose |
|------|-------------|---------|
| `spawn_agent` | Feature::Collab | Create sub-agent with optional role |
| `send_input` | Feature::Collab | Message agents (with interrupt) |
| `resume_agent` | Feature::Collab | Reactivate closed agents |
| `wait` | Feature::Collab | Block on agent completion (up to 1hr) |
| `close_agent` | Feature::Collab | Terminate agents |
| `spawn_agents_on_csv` | Collab + Sqlite | CSV-based batch agent processing |
| `report_agent_job_result` | Collab + Sqlite | Worker result reporting |
| `js_repl` / `js_repl_reset` | Feature::JsRepl | Persistent Node.js REPL (experimental since v0.106) |
| `get_memory` | Feature::MemoryTool | Memory read (under development, default disabled) |
| `presentation_artifact` | Feature::Artifact | Interactive artifact management |

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
name = "code-reviewer"
description = "Reviews code for bugs, design issues, and test coverage"
sandbox_mode = "read-only"
developer_instructions = """
<full Claude Code agent prompt body here — embedded verbatim>

# Code Review Agent

## Review Categories
...all categories, actionability filters, severity guidelines, output formats...

## Out of Scope
...cross-reviewer boundaries...
"""
```

**Required fields**: `name`, `description`, `developer_instructions`. All three are mandatory — Codex rejects agent TOMLs missing any of them.

**Omit `model` and `model_reasoning_effort`** — they inherit from the parent session when absent. This ensures agents always use whatever model the user configured, without hardcoding versions that go stale.

The `developer_instructions` field holds the **full** agent prompt body as a multi-line TOML string. Do not summarize or truncate.

**Built-in roles** (user-defined override these):
| Role | Purpose |
|------|---------|
| `default` | General-purpose fallback |
| `worker` | Execution-focused implementation |
| `explorer` | Read-heavy codebase exploration |
| `monitor` | Long-running task monitoring |

**Per-role optional fields** (all inherit from parent session when omitted):
- `model` — model ID (omit to inherit)
- `model_reasoning_effort` — minimal/low/medium/high/xhigh (omit to inherit)
- `sandbox_mode` — read-only/workspace-write/danger-full-access
- `nickname_candidates`, `mcp_servers`, `skills.config` — also inherit

**Phase 1** (deterministic): Generate TOML with `name`, `description` from Claude Code agent frontmatter, and full prompt body as `developer_instructions`. Omit `model` and `model_reasoning_effort` (inherit from session). Set `sandbox_mode: "read-only"` for review agents.

**Phase 2** (LLM): Embed the Claude Code agent's full prompt body into `developer_instructions` as a multi-line TOML string (`"""\n...\n"""`). Keep the prompt body as identical as possible — categories, actionability filters, severity guidelines, output formats, out-of-scope sections are the core value. Only changes allowed: tool name references (use Codex names: `shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`; experimental: `read_file`, `list_dir`, `grep_files`), and genuinely unsupported features (document as limitation, don't remove). Do NOT summarize, truncate, or rewrite the prompt body.

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

**NOT shipped** as of v0.107.0 (March 3, 2026).
- Issue reopened Feb 27, 2026 — 453+ upvotes, 54+ comments
- Multiple community PRs attempted and rejected:
  - PR #2904 (Aug 2025) — closed
  - PR #4522 (MVP prehook) — closed
  - PR #9796 (comprehensive hooks, Jan 2026) — closed
  - PR #11067 (lifecycle events + steering) — rejected: "code contributions are by invitation only"
- **Proposed events** (from PR #11067): `pre_tool_use`, `post_tool_use`, `session_stop`, `user_prompt_submit`, `after_agent`
- Issue #12208 also requests `PreCompact` hook event
- **OpenAI appears to want to build this internally** based on the "by invitation only" rejection
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

## Namespacing

Install scripts handle all component renaming at install time via `install_helpers.py`. The `dist/codex/` directory keeps original names — sync-tools writes originals, install scripts namespace.

**Pattern**: All components get `-manifest-dev` suffix:
- Skill dirs: `skills/define/` → `skills/define-manifest-dev/`
- Agent TOML files: `code-bugs-reviewer.toml` → `code-bugs-reviewer-manifest-dev.toml`
- SKILL.md `name:` field patched to match directory name
- Content cross-references patched (slash commands, quoted strings, paths, agent names)
- `config.toml` section headers and `config_file` paths patched automatically

**Selective cleanup** (replaces `rm -rf` of shared dirs):
```bash
find ".agents/skills" -maxdepth 1 -name "*-manifest-dev" -type d -exec rm -rf {} + 2>/dev/null || true
find ".codex/agents" -maxdepth 1 -name "*-manifest-dev*" -exec rm -rf {} + 2>/dev/null || true
```

Component names on disk will have `-manifest-dev` suffix after install.

## Context File Adaptation

During sync, replace remaining `CLAUDE.md` references that mean "this CLI's context file" with `AGENTS.md`:
- Agent content: any "CLAUDE.md" that refers to the project context file → `AGENTS.md`
- Context file (AGENTS.md): references to context file names
- README: references to context file names
- config.toml: update `project_doc_fallback_filenames` to not reference CLAUDE.md
- Skills (operational only): instructions like "write to CLAUDE.md" → "write to AGENTS.md". Leave research/reference content unchanged.
- Do NOT replace "CLAUDE.md" when it refers to Claude Code's own file (e.g., in comparative text or research).

The `context-file-adherence-reviewer` agent already uses generic "context file" language — no special handling needed for its content.

## Session File Adaptation

Source skills that surface a session file path to the user (e.g. `Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl` in `define/SKILL.md`'s completion template, and the `Session JSONL files live at ...` line in `learn-define-patterns/SKILL.md`) reference Claude Code's per-session JSONL file.

**Verdict for Codex**: OMIT the Session line. Codex *does* persist per-session JSONL on disk, but the agent has no way to compute its own current path at runtime.

- **On-disk path**: `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<timestamp>-<session-id>.jsonl` (default `$CODEX_HOME` = `~/.codex/`). May be stored as `.jsonl.zst` compressed archives.
- **No agent-visible session ID env var**: There is no standard `CODEX_SESSION_ID` exposed to the agent runtime. Surfacing the active session ID programmatically is an open feature request (issue #8923, "Feature request: expose current Codex session ID programmatically (env var or JSON)"). Without it, the running agent cannot construct a path that resolves to the current session — only the user can, by browsing `~/.codex/sessions/` or using `/status`.
- **Sync rule for `define/SKILL.md` Session line**: drop the line entirely from the completion template until Codex exposes a session-id env var. Re-add when issue #8923 ships.
- **Sync rule for `learn-define-patterns/SKILL.md`**: discovery path on line 31 also can't be safely retargeted because the date-sharded directory and per-rollout filename can't be derived from anything the agent sees. Document as a known limitation. The user-config substitution for lines 25/54 is still applied: `~/.claude/CLAUDE.md` → `~/.codex/AGENTS.md`.

## Known Limitations

1. **Skills only for full compatibility** — Agents are TOML stubs, hooks impossible.
2. **No workflow enforcement** — Without hooks, the chain is advisory.
3. **6 default tools, more experimental** — Default: `shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`. Experimental: `read_file`, `list_dir`, `grep_files` (gated by model config). Multi-agent: `spawn_agent` etc. (requires Feature::Collab).
4. **Sandbox restrictions per role, not tool restrictions** — Roles can have different `sandbox_mode` (read-only/workspace-write/danger-full-access) and MCP tools, but base tool set is not configurable per role.
5. **Skills may not chain reliably** — `$skillname` invocation less documented.
6. **AGENTS.md is informational only** — Describes agents but doesn't execute them as scoped subagents.
7. **Hooks not shipped** — Issue #2109 still open. Community PRs rejected. No timeline.
8. **$ARGUMENTS not supported** — Claude Code extension only.
9. **Notify is fire-and-forget** — Cannot block or modify agent behavior.
10. **Experimental tools availability** — `read_file`, `list_dir`, `grep_files` are gated server-side by model's `experimental_supported_tools`. Not all users may have access.
11. **TaskCreate ≠ Agent** — Claude Code's TaskCreate/TaskUpdate/TaskGet/TaskList map to `update_plan` (todo), NOT to `spawn_agent` (multi-agent).
12. **Model tier routing is Claude Code-only** — `execution-modes/efficient.md` references Claude model names (haiku, sonnet, opus). Replace all with `inherit` during sync. In per-role TOMLs, omit `model` and `model_reasoning_effort` to inherit from the parent session. Execution mode parallelism, loop limits, and gate-skipping still apply.
