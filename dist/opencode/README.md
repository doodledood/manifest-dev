# manifest-dev — OpenCode CLI Distribution

Verification-first manifest workflows for OpenCode CLI. Ported from the Claude Code manifest-dev plugin.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 9 | Core workflow skills (auto, define, do, done, drive, drive-tick, escalate, figure-out, verify) |
| Agents | 14 | Specialized reviewer and verification agents |
| Commands | 7 | User-invocable slash commands |
| Plugin | 1 | TypeScript hook plugin for workflow enforcement |
| Context | 1 | AGENTS.md workflow overview |

## Installation

### Option 1: Remote Install via npx skills (Skills Only)

```bash
npx skills add doodledood/manifest-dev --all -a opencode
```

This installs skills into `.opencode/skills/`. For agents, commands, and the plugin, use the full distribution install below.

### Option 2: Full Distribution Install

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
```

Or clone and run locally:

```bash
git clone https://github.com/doodledood/manifest-dev.git
cd manifest-dev
bash dist/opencode/install.sh
```

The install script:
- Copies skills to `.opencode/skills/` with `-manifest-dev` suffix
- Copies agents to `.opencode/agents/` with `-manifest-dev` suffix
- Copies commands to `.opencode/commands/` with `-manifest-dev` suffix
- Installs plugin as `.opencode/plugins/manifest-dev.ts`
- Copies AGENTS.md context file
- Is idempotent — safe to re-run

### Manual Install

```bash
# Skills
cp -r dist/opencode/skills/* .opencode/skills/

# Agents
cp -r dist/opencode/agents/* .opencode/agents/

# Commands
cp -r dist/opencode/commands/* .opencode/commands/

# Plugin (auto-loaded from .opencode/plugins/)
cp dist/opencode/plugins/index.ts .opencode/plugins/manifest-dev.ts

# Context file
cp dist/opencode/AGENTS.md .opencode/AGENTS.md
```

## Usage

After installation, invoke workflows via slash commands:

```
/define-manifest-dev                    Plan and scope a task
/do-manifest-dev                        Execute a manifest
/auto-manifest-dev                      End-to-end autonomous execution
/verify-manifest-dev                    Run parallel verifiers (use --deferred for deferred-auto criteria)
/figure-out-manifest-dev                Deep collaborative understanding
/drive-manifest-dev                     Cron-driven manifest-to-green loop / PR lifecycle automation
/drive-tick-manifest-dev                Single drive iteration (called by /loop via /drive)
```

## Feature Parity with Claude Code

| Feature | Claude Code | OpenCode | Notes |
|---------|------------|----------|-------|
| Skills | Full | Full | Copied unchanged |
| Agents | Full | Full | Frontmatter converted to OpenCode format |
| Commands | N/A | Full | Generated from user-invocable skills |
| Stop hook (block) | Full | Degraded | session.idle is fire-and-forget; enforced via system guidance |
| Compaction recovery | Full | Full | experimental.session.compacting |
| Pre-verify refresh | Full | Full | tool.execute.before (main agent only) |
| Log reminders | Full | Approximate | Persistent system context vs event-driven |
| Amendment check | Full | Approximate | Persistent system context vs per-prompt |
| Subagent hooks | Full | Missing | tool.execute.before/after don't fire in subagents |

## Known Limitations

1. **No stop blocking** — OpenCode's `session.idle` is fire-and-forget. The /do workflow contract is advisory, not enforced. (OpenCode issue #12472)
2. **Subagent hook bypass** — `tool.execute.before`/`after` don't fire for subagent tool calls. (OpenCode issue #5894)
3. **No JSONL transcript** — Workflow state tracked in-memory; lost on plugin reload.
4. **Compaction hook is experimental** — `experimental.session.compacting` may change.
5. **System transform is experimental** — `experimental.chat.system.transform` may change.
6. **$ARGUMENTS handling** — Skills using `$ARGUMENTS` work in Claude Code; behavior in OpenCode may vary.

## Directory Structure

```
dist/opencode/
├── agents/                          # 14 converted agents
│   ├── change-intent-reviewer.md
│   ├── code-bugs-reviewer.md
│   ├── test-quality-reviewer.md
│   ├── prose-value-reviewer.md
│   ├── code-design-reviewer.md
│   ├── code-maintainability-reviewer.md
│   ├── code-simplicity-reviewer.md
│   ├── code-testability-reviewer.md
│   ├── context-file-adherence-reviewer.md
│   ├── contracts-reviewer.md
│   ├── criteria-checker.md
│   ├── docs-reviewer.md
│   ├── manifest-verifier.md
│   └── type-safety-reviewer.md
├── commands/                        # 7 user commands
│   ├── auto.md
│   ├── define.md
│   ├── do.md
│   ├── figure-out.md
│   ├── drive.md
│   ├── drive-tick.md
│   └── verify.md
├── skills/                          # 9 skills (with subdirectories)
│   ├── auto/
│   ├── define/
│   ├── do/
│   ├── done/
│   ├── escalate/
│   ├── figure-out/
│   ├── drive/
│   ├── drive-tick/
│   └── verify/
├── plugins/
│   ├── index.ts                     # Hook plugin
│   └── HOOK_SPEC.md                 # Behavioral specification
├── AGENTS.md                        # Context file
├── README.md                        # This file
├── install.sh                       # Installation script
└── install_helpers.py               # Namespacing helper
```
