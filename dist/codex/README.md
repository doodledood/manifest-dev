# manifest-dev -- Codex CLI Distribution

Verification-first manifest workflows for Codex CLI. Define specifications, execute against them, verify with parallel review agents, and confirm completion.

## Components

| Type | Count | Notes |
|------|-------|-------|
| Skills | 11 | Core workflow skills plus manifest-dev-tools utilities |
| Agents | 16 | TOML config stubs with full prompt bodies |
| Hooks | 0 | Not supported by Codex CLI (Issue #2109) |
| Rules | 1 | Starlark execution policy |

### Skills

| Skill | Description |
|-------|-------------|
| auto | Autonomous workflow orchestration (`--babysit <pr-url>` to tend existing PR) |
| define | Interview-driven manifest creation (`--babysit <pr-url>` to synthesize from existing PR) |
| do | Execute against a manifest |
| done | Completion checkpoint |
| escalate | Escalate blockers to the user |
| figure-out | Collaborative deep understanding |
| figure-out-team | Multi-party async deliberation |
| adr | Post-hoc Architecture Decision Record synthesis |
| handoff | Cross-boundary handoff or DIY sub-agent context payload |
| prompt-engineering | Slim-discipline prompt creation and review |
| review | Autonomous PR review with tiered reviewer fleet, holistic coherence pass, and `--loop` follow-through |
| walk-pr | Collaborative PR/diff walkthrough |

### Agents

| Agent | Sandbox | Purpose |
|-------|---------|---------|
| change-intent-reviewer | read-only | Intent-behavior divergence analysis |
| code-bugs-reviewer | read-only | Mechanical defect detection |
| operational-readiness-reviewer | read-only | Runtime and deployment readiness |
| test-quality-reviewer | read-only | Coverage gaps plus independent behavioral-oracle checks |
| prose-value-reviewer | read-only | Comments and repo doc files: AI-tells, narrating-the-obvious, puffery |
| code-design-reviewer | read-only | Design fitness and responsibility ownership audit |
| code-maintainability-reviewer | read-only | Maintainability audit |
| code-simplicity-reviewer | read-only | Complexity audit |
| code-testability-reviewer | read-only | Testability audit |
| context-file-adherence-reviewer | read-only | Context file compliance |
| contracts-reviewer | read-only | API contract verification with source-of-truth evidence |
| criteria-checker | read-only | Single criterion verification |
| docs-reviewer | read-only | Documentation accuracy audit |
| github-pr-lifecycle | read-only | Steerable GitHub PR lifecycle inspection; emits hints for /do dispatch |
| slack-poller | read-only | Slack thread delta narrator for /figure-out-team |
| type-safety-reviewer | read-only | Type safety audit |

## Installation

### Remote Install (recommended)

```bash
npx skills add doodledood/manifest-dev --all
```

### Manual Install

```bash
# Clone or download this directory, then run:
bash dist/codex/install.sh

# Optional: install into a non-default Codex home
CODEX_HOME=/path/to/.codex bash dist/codex/install.sh

# Uninstall only manifest-dev-managed files
bash dist/codex/install.sh uninstall

# Or install components individually:

# Skills (copy to .agents/skills/)
cp -r dist/codex/skills/* .agents/skills/

# Agents (copy to .codex/agents/)
cp -r dist/codex/agents/* .codex/agents/

# Rules (copy to .codex/rules/)
cp -r dist/codex/rules/* .codex/rules/

# Config (merge into your .codex/config.toml)
cat dist/codex/config.toml >> .codex/config.toml

# AGENTS.md (copy to project root)
cp dist/codex/AGENTS.md ./AGENTS.md
```

The install script handles namespacing automatically: core workflow components use `-manifest-dev`, and manifest-dev-tools skills use `-manifest-dev-tools`.

## Feature Parity with Claude Code

| Feature | Claude Code | Codex CLI |
|---------|------------|-----------|
| Skills (SKILL.md) | Full support | Full support (same open standard) |
| Agents (scoped subagents) | Full support | TOML stubs (multi-agent paradigm differs) |
| Hooks (event handlers) | Full support | Not available (Issue #2109) |
| Workflow enforcement | Hooks enforce chain | Advisory only (no enforcement) |
| Model tier routing | haiku/sonnet/opus | Uses configured model (inherit) |
| $ARGUMENTS in skills | Supported | Not supported |
| Context file | CLAUDE.md | AGENTS.md |

## Directory Structure

```
dist/codex/
├── skills/                          # 11 skills (core + tools)
│   ├── auto/
│   ├── define/
│   │   ├── SKILL.md
│   │   ├── tasks/
│   │   └── references/
│   ├── do/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── done/
│   ├── escalate/
│   ├── figure-out/
│   ├── figure-out-team/
│   ├── adr/
│   ├── handoff/
│   ├── prompt-engineering/
│   ├── review/
│   └── walk-pr/
├── agents/                          # 16 TOML config stubs
│   ├── change-intent-reviewer.toml
│   ├── code-bugs-reviewer.toml
│   ├── operational-readiness-reviewer.toml
│   ├── test-quality-reviewer.toml
│   ├── prose-value-reviewer.toml
│   ├── code-design-reviewer.toml
│   ├── code-maintainability-reviewer.toml
│   ├── code-simplicity-reviewer.toml
│   ├── code-testability-reviewer.toml
│   ├── context-file-adherence-reviewer.toml
│   ├── contracts-reviewer.toml
│   ├── criteria-checker.toml
│   ├── docs-reviewer.toml
│   ├── github-pr-lifecycle.toml
│   ├── slack-poller.toml
│   └── type-safety-reviewer.toml
├── rules/                           # Execution policy
│   └── default.rules
├── config.toml                      # Multi-agent + MCP config
├── AGENTS.md                        # Agent descriptions + workflow guide
├── install.sh                       # Idempotent installer
├── install_helpers.py               # Namespacing utilities
└── README.md                        # This file
```

## Known Limitations

1. **Skills are the only fully compatible component.** Agent TOML stubs approximate behavior but use a different paradigm. Hooks are impossible.
2. **No workflow enforcement.** Without hooks, the define -> do -> verify -> done chain is advisory. Nothing prevents skipping steps.
3. **Default tool set differs.** Codex provides 6 default tools (`shell_command`, `apply_patch`, `update_plan`, `request_user_input`, `web_search`, `view_image`) plus experimental tools (`read_file`, `list_dir`, `grep_files`). Tool restrictions are per-sandbox-mode, not per-agent.
4. **Skills may not chain reliably.** `$skillname` invocation is less documented than Claude Code's skill system.
5. **AGENTS.md is informational only.** Describes agents and workflow but does not execute them as scoped subagents.
6. **Hooks not shipped.** Issue #2109 (453+ upvotes) still open. Community PRs rejected. No timeline. When hooks ship, this distribution should expand.
7. **$ARGUMENTS not supported.** Claude Code extension only.
8. **Model tier routing is not available.** Execution modes use `inherit` (the configured model) rather than Claude-specific model names.
9. **Notify is fire-and-forget.** The only event hook (`agent-turn-complete`) cannot block or modify behavior.
