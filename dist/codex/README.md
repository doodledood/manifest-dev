# manifest-dev for Codex CLI

Verification-first manifest workflows adapted for Codex CLI. Define tasks, execute them, verify acceptance criteria, and complete with confidence.

## What's Included

| Component | Count | Status |
|-----------|-------|--------|
| Skills | 6 | Full compatibility (Agent Skills Open Standard) |
| Agents | AGENTS.md + 12 TOML stubs | Informational + multi-agent config |
| Execution rules | 1 | Starlark .rules file |
| Config | 1 | Multi-agent TOML config |
| Hooks | 0 | Not available (Codex has no hook system yet) |

### Skills (copied unchanged)

| Skill | Purpose |
|-------|---------|
| **define** | Interview-driven manifest builder with task scoping |
| **do** | Manifest executor, iterates through deliverables |
| **verify** | Spawns parallel verification agents for acceptance criteria |
| **done** | Completion marker with execution summary |
| **escalate** | Structured escalation with evidence |
| **learn-define-patterns** | Extracts user preference patterns from /define sessions |

### AGENTS.md

Describes all 12 agents, their purposes, the define-do-verify-done workflow, and how to approximate their behavior using Codex's multi-agent system.

### TOML Agent Stubs (12 total)

Per-agent TOML configuration files for Codex's multi-agent system. Each agent has access to 6 default tools (`shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`) plus experimental tools (`read_file`, `list_dir`, `grep_files`) if available on your model.

| Agent | Purpose | Sandbox |
|-------|---------|---------|
| criteria-checker | Validates single criterion (PASS/FAIL) | read-only |
| code-bugs-reviewer | Race conditions, data loss, edge cases, logic errors | read-only |
| code-design-reviewer | Reinvented wheels, code vs config, under-engineering | read-only |
| code-simplicity-reviewer | Over-engineering, premature optimization, cognitive load | read-only |
| code-maintainability-reviewer | DRY, coupling, cohesion, dead code, consistency | read-only |
| code-coverage-reviewer | Test coverage gaps in changed code | read-only |
| code-testability-reviewer | Excessive mocking, logic buried in IO, hidden deps | read-only |
| type-safety-reviewer | any abuse, invalid states, narrowing gaps, nullability | read-only |
| docs-reviewer | Documentation accuracy against code changes | read-only |
| claude-md-adherence-reviewer | Compliance with CLAUDE.md project rules | read-only |
| manifest-verifier | Manifest completeness during /define | read-only |
| define-session-analyzer | User preference patterns from /define sessions | workspace-write |

### Execution Rules

`rules/default.rules` provides safe defaults in Starlark:
- **Allow**: git operations, npm/yarn/pnpm, pytest, ruff, black, mypy, cat, ls, find, head, tail, grep
- **Prompt**: rm, mv, cp, tee, git push
- **Forbidden**: iptables, ip6tables, ifconfig, route (network modification)

### Config

`config.toml` enables multi-agent with all 12 agents registered, `max_threads = 6`, `max_depth = 1`, and `project_doc_fallback_filenames = ["CLAUDE.md"]`.

## Install / Update

### Everything (one command, no clone needed)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash
```

Installs skills, AGENTS.md, agent TOML stubs, execution rules, and config. Run again to update. Will not overwrite existing `.codex/config.toml`.

### Skills only

```bash
npx skills add doodledood/manifest-dev --all -a codex
```

### Manual

```bash
# Skills
cp -r dist/codex/skills/* .agents/skills/

# AGENTS.md
cp dist/codex/AGENTS.md ./AGENTS.md

# Agent TOML stubs
mkdir -p .codex/agents
cp dist/codex/agents/*.toml .codex/agents/

# Execution rules
mkdir -p .codex/rules
cp dist/codex/rules/default.rules .codex/rules/

# Config (merge into existing or copy fresh)
cp dist/codex/config.toml .codex/config.toml
```

## Feature Parity

| Feature | Claude Code | Codex CLI | Notes |
|---------|-------------|-----------|-------|
| Skills (define/do/verify/done/escalate/learn) | Full | Full | Agent Skills Open Standard |
| Default tools | 15+ specialized | 6 default | shell_command, apply_patch, update_plan, request_user_input, web_search, view_image |
| Experimental tools | N/A | 3 gated | read_file, list_dir, grep_files (model-dependent) |
| Multi-agent tools | Agent, Task*, SendMessage | spawn_agent, send_input, wait, close_agent | Requires Feature::Collab flag |
| Verification agents | Scoped subagents | TOML role stubs | Agents get 6 default tools; sandbox_mode per role |
| Stop enforcement hook | Full | Missing | No hook system in Codex (Issue #2109) |
| Verify context hook | Full | Missing | No hook system |
| Post-compact recovery | Full | Missing | No hook system |
| Workflow enforcement | Enforced via hooks | Advisory | Without hooks, chain is not enforced |
| $ARGUMENTS in skills | Supported | Not supported | Claude Code extension only |
| Scoped subagents | Per-agent tool sets | Per-role sandbox mode | Codex roles can set read-only/workspace-write/full-access |
| Project context | CLAUDE.md | AGENTS.md + CLAUDE.md fallback | project_doc_fallback_filenames config |
| Notify (fire-and-forget) | N/A | agent-turn-complete event | Observability only, no blocking |

## Known Limitations

1. **Skills are the only fully compatible component** -- agents are TOML stubs with approximated instructions, hooks are impossible without a hook system.
2. **No workflow enforcement** -- without hooks, the define-do-verify-done chain is advisory. Nothing prevents skipping steps.
3. **6 default tools, not Claude Code's 15+** -- Codex agents have `shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`. Experimental tools (`read_file`, `list_dir`, `grep_files`) are gated server-side by model config. Multi-agent tools (`spawn_agent`, `send_input`, `wait`, `close_agent`) require Feature::Collab flag.
4. **Sandbox restrictions per role, not tool restrictions** -- Codex roles can have different `sandbox_mode` (read-only / workspace-write / danger-full-access) but the base tool set is not configurable per role.
5. **Hooks not shipped** -- Issue #2109 (453+ upvotes, March 2026). Multiple community PRs rejected ("by invitation only"). No timeline. When hooks ship, this distribution should expand significantly.
6. **$ARGUMENTS not supported** -- Claude Code skill extension only. Skills that reference $ARGUMENTS will not receive arguments on Codex.
7. **Notify is fire-and-forget** -- The only event hook (`agent-turn-complete`) cannot block, modify, or intercept agent behavior. Observability only.
8. **Skills may not chain reliably** -- `$skillname` invocation in Codex is less documented than Claude Code's skill system.
9. **Experimental tools not guaranteed** -- `read_file`, `list_dir`, `grep_files` availability is controlled server-side per model. Not all users may have access.

## Directory Structure

```
dist/codex/
├── skills/                           # Skills (unchanged from Claude Code)
│   ├── define/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── tasks/
│   ├── do/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── verify/
│   │   └── SKILL.md
│   ├── done/
│   │   └── SKILL.md
│   ├── escalate/
│   │   └── SKILL.md
│   └── learn-define-patterns/
│       └── SKILL.md
├── agents/                           # TOML config per agent role
│   ├── criteria-checker.toml
│   ├── code-bugs-reviewer.toml
│   ├── code-design-reviewer.toml
│   ├── code-simplicity-reviewer.toml
│   ├── code-maintainability-reviewer.toml
│   ├── code-coverage-reviewer.toml
│   ├── code-testability-reviewer.toml
│   ├── type-safety-reviewer.toml
│   ├── docs-reviewer.toml
│   ├── claude-md-adherence-reviewer.toml
│   ├── manifest-verifier.toml
│   └── define-session-analyzer.toml
├── rules/                            # Execution policy
│   └── default.rules
├── config.toml                       # Multi-agent + project config
├── AGENTS.md                         # Agent descriptions + workflow guide
├── install.sh                        # Idempotent installer
└── README.md                         # This file
```

## Source

This is a generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev) for Claude Code. The Claude Code plugin is the source of truth. This Codex distribution adapts the components to work within Codex CLI's capabilities.
