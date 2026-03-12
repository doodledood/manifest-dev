# manifest-dev for Codex CLI

Verification-first manifest workflows adapted for Codex CLI. Define tasks, execute them, verify acceptance criteria, and complete with confidence.

## What's Included

| Component | Count | Status |
|-----------|-------|--------|
| Skills | 6 | Full compatibility (Agent Skills Open Standard) |
| Agents | 12 TOML stubs + reference AGENTS.md | Multi-agent config + bundled reference guide |
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

Bundled as a reference document in `dist/codex/AGENTS.md`. It is not installed into `~/.codex/` by the installer.

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
| context-file-adherence-reviewer | Compliance with AGENTS.md project rules | read-only |
| manifest-verifier | Manifest completeness during /define | read-only |
| define-session-analyzer | User preference patterns from /define sessions | workspace-write |

### Execution Rules

`rules/default.rules` is the bundled rules source. The installer copies it to `~/.codex/rules/manifest-dev.rules` to avoid clobbering an existing `default.rules`:
- **Allow**: git operations, npm/yarn/pnpm, pytest, ruff, black, mypy, cat, ls, find, head, tail, grep
- **Prompt**: rm, mv, cp, tee, git push
- **Forbidden**: iptables, ip6tables, ifconfig, route (network modification)

### Config

`config.toml` enables multi-agent with all 12 agents registered, `max_threads = 6`, `max_depth = 1`, and `project_doc_fallback_filenames = ["CLAUDE.md"]`.

## Install / Update / Uninstall

### Everything (one command, no clone needed)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash
```

Installs skills, agent TOML stubs, execution rules, and config into `~/.codex/` by default, or `$CODEX_HOME` if set. It does not write `AGENTS.md`. Run again to update. Existing `config.toml` is backed up and merged with the manifest-dev sections.

After install, invoke the namespaced skills directly on Codex: `$define-manifest-dev`, `$do-manifest-dev`, `$verify-manifest-dev`, `$done-manifest-dev`, `$escalate-manifest-dev`, and `$learn-define-patterns-manifest-dev`.

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash -s -- uninstall
```

This removes only manifest-dev-managed Codex files: the suffixed skills, suffixed agent TOML stubs, `rules/manifest-dev.rules`, and the manifest-dev-managed sections in `~/.codex/config.toml`. Before unmerging shared config, the script backs it up to `config.toml.pre-manifest-dev-uninstall.bak`.

### Skills only

```bash
npx skills add doodledood/manifest-dev --all -a codex
```

### Manual

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
TMP_DIR=$(mktemp -d)
mkdir -p "$TMP_DIR/codex"
cp -R dist/codex/. "$TMP_DIR/codex"
python3 "$TMP_DIR/codex/install_helpers.py" namespace "$TMP_DIR/codex" codex

# Skills
mkdir -p "$CODEX_HOME/skills"
cp -r "$TMP_DIR/codex/skills/"* "$CODEX_HOME/skills/"

# Agent TOML stubs
mkdir -p "$CODEX_HOME/agents"
cp "$TMP_DIR/codex/agents/"*.toml "$CODEX_HOME/agents/"

# Execution rules
mkdir -p "$CODEX_HOME/rules"
cp "$TMP_DIR/codex/rules/default.rules" "$CODEX_HOME/rules/manifest-dev.rules"

# Config
if [ -f "$CODEX_HOME/config.toml" ]; then
  cp "$CODEX_HOME/config.toml" "$CODEX_HOME/config.toml.bak"
fi
python3 "$TMP_DIR/codex/install_helpers.py" merge-config "$TMP_DIR/codex/config.toml" "$CODEX_HOME/config.toml"

rm -rf "$TMP_DIR"
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

## Execution Modes

Control verification intensity with `--mode`:

| Mode | Verification | Parallelism | Best For |
|------|-------------|-------------|----------|
| **thorough** (default) | Full reviewer agents, unlimited fix loops | All at once | Production-quality work |
| **balanced** | Full model capability, capped loops | Batched (max 4) | Standard development |
| **efficient** | Skips reviewer subagents, lighter checks | Sequential | Quick iterations, low-risk changes |

Usage: `/do <manifest> [log] --mode balanced`

Mode can also be set in the manifest's `mode:` field during `/define`. The `--mode` flag on `/do` takes precedence.

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
│   │       ├── BUDGET_MODES.md
│   │       └── COLLABORATION_MODE.md
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
│   ├── context-file-adherence-reviewer.toml
│   ├── manifest-verifier.toml
│   └── define-session-analyzer.toml
├── rules/                            # Execution policy
│   └── default.rules
├── config.toml                       # Multi-agent + project config
├── AGENTS.md                         # Agent descriptions + workflow guide
├── install.sh                        # Idempotent installer
├── install_helpers.py                # Namespace helper for install
└── README.md                         # This file
```

## Source

This is a generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev) for Claude Code. The Claude Code plugin is the source of truth. This Codex distribution adapts the components to work within Codex CLI's capabilities.
