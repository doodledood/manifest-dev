# manifest-dev for Codex CLI

Verification-first manifest workflows adapted for Codex CLI (v0.77.0).

## What's Included

| Component | Count | Status |
|-----------|-------|--------|
| Skills | 9 | Full compatibility (Agent Skills Open Standard) |
| Agents | 14 TOML stubs + reference AGENTS.md | Multi-agent config with full prompt bodies |
| Execution rules | 1 | Starlark .rules file |
| Config | 1 | Multi-agent TOML config |
| Hooks | 0 | Not available (Codex has no hook system -- Issue #2109) |

## Install

### Primary: Skills installer

```bash
npx skills add https://github.com/doodledood/manifest-dev --all
```

### Full install (skills + agents + config + rules)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash
```

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash -s -- uninstall
```

## Skills

| Skill | Description | User-invocable |
|-------|-------------|----------------|
| define | Interview-driven manifest builder with domain-specific task guidance | Yes |
| do | Manifest executor with mode-aware verification | Yes |
| verify | Parallel verification runner (spawns agents per criterion) | No |
| auto | End-to-end /define + /do in one command | Yes |
| done | Completion marker with execution summary | No |
| escalate | Structured escalation for blocking issues | No |
| learn-define-patterns | Extract user preferences from past /define sessions | Yes |
| understand | Collaborative deep understanding -- truth-convergent thinking partner | Yes |
| understand-done | End an active /understand session | Yes |

## Agents (TOML stubs)

| Agent | Role | Sandbox | Reasoning |
|-------|------|---------|-----------|
| criteria-checker | Criterion verification | read-only | high |
| change-intent-reviewer | Intent-behavior divergence analysis | read-only | xhigh |
| code-bugs-reviewer | Mechanical defect detection | read-only | xhigh |
| code-design-reviewer | Design fitness audit | read-only | xhigh |
| code-simplicity-reviewer | Complexity detection | read-only | high |
| code-maintainability-reviewer | Maintainability audit | read-only | xhigh |
| code-coverage-reviewer | Test coverage gaps | read-only | high |
| code-testability-reviewer | Testability issues | read-only | high |
| contracts-reviewer | API contract correctness | read-only | xhigh |
| type-safety-reviewer | Type safety audit | read-only | high |
| docs-reviewer | Documentation accuracy | read-only | high |
| context-file-adherence-reviewer | AGENTS.md compliance | read-only | high |
| manifest-verifier | Manifest gap detection | read-only | xhigh |
| define-session-analyzer | Session pattern extraction | workspace-write | high |

## Execution Modes

| Mode | Verification | Parallelism | Best For |
|------|-------------|-------------|----------|
| **thorough** (default) | Full reviewer agents, unlimited fix loops | All at once | Production-quality work |
| **balanced** | Full model capability, capped loops | Batched (max 4) | Standard development |
| **efficient** | Skips reviewer subagents, lighter checks | Sequential | Quick iterations, low-risk changes |

## Feature Parity

| Feature | Claude Code | Codex CLI |
|---------|------------|-----------|
| Skills | Full | Full (Agent Skills Open Standard) |
| Agents | Scoped subagents | TOML config stubs (full prompt bodies in developer_instructions) |
| Hooks | 3 Python hooks | None (no hook system) |
| Workflow enforcement | Hooks enforce chain | Advisory only |
| Model tier routing | haiku/sonnet/opus | Default model (inherit) |
| $ARGUMENTS | Supported | Not supported |
| Collaboration mode | --medium flag | Skills support it; no hooks to enforce |
| Amendment mode | --amend flag | Skills support it |
| Visualize mode | --visualize flag | Skills support it |

## Known Limitations

1. **Skills are the only fully compatible component** -- agents are TOML stubs, hooks impossible.
2. **No workflow enforcement** -- without hooks, the define->do->verify->done chain is advisory.
3. **6 default tools** -- `shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`. Experimental: `read_file`, `list_dir`, `grep_files`.
4. **Hooks not shipped** -- Issue #2109 (453+ upvotes). No timeline.
5. **$ARGUMENTS not supported** -- Claude Code skill extension only.
6. **Notify is fire-and-forget** -- Cannot block or modify agent behavior.
7. **Model tier routing is Claude Code-only** -- Budget modes reference Claude model names; replaced with `inherit` in this distribution.

## Source

Generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev) v0.77.0. The Claude Code plugin is the source of truth.
