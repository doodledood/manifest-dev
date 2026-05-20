# manifest-dev — OpenCode CLI Distribution

Verification-first manifest workflows for OpenCode CLI. Ported from the Claude Code manifest-dev plugin.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 11 | Core workflow skills plus manifest-dev-tools utilities |
| Agents | 16 | Specialized reviewer and verification agents |
| Commands | 9 | User-invocable slash commands for core workflows and tools utilities |
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

This installs globally to `~/.config/opencode/`, which OpenCode loads from every project. Restart OpenCode after installing or updating so the running TUI reloads agents, commands, skills, and plugins.

Or clone and run locally:

```bash
git clone https://github.com/doodledood/manifest-dev.git
cd manifest-dev
bash dist/opencode/install.sh
```

The install script:
- Copies core skills to `~/.config/opencode/skills/` with `-manifest-dev` suffix
- Copies manifest-dev-tools skills to `~/.config/opencode/skills/` with `-manifest-dev-tools` suffix
- Copies agents to `~/.config/opencode/agents/` with `-manifest-dev` suffix
- Copies commands to `~/.config/opencode/commands/` with the same plugin-owned suffixes
- Installs plugin as `~/.config/opencode/plugins/manifest-dev.ts`
- Copies AGENTS.md context file
- Is idempotent — safe to re-run

To install only for the current project, pass `--local`:

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- --local
```

To install somewhere custom, set `OPENCODE_TARGET` or pass `--dir`:

```bash
OPENCODE_TARGET="$HOME/.config/opencode" bash dist/opencode/install.sh
bash dist/opencode/install.sh --dir /path/to/opencode-config
```

To uninstall only manifest-dev-managed files:

```bash
bash dist/opencode/install.sh uninstall
```

Use `bash dist/opencode/install.sh uninstall --local` to remove a project-local install.

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
/define-manifest-dev                    Plan and scope a task (--babysit <pr-url> to synthesize from existing PR)
/do-manifest-dev                        Execute a manifest and verify each criterion inline
/auto-manifest-dev                      End-to-end autonomous execution (--babysit <pr-url> to tend existing PR)
/figure-out-manifest-dev                Truth-convergent thinking partner
/figure-out-team-manifest-dev           Multi-party async deliberation in a Slack thread
/adr-manifest-dev-tools                 Post-hoc ADR synthesis
/handoff-manifest-dev-tools             Cross-boundary context handoff
/prompt-engineering-manifest-dev-tools  Slim-discipline prompt work
/walk-pr-manifest-dev-tools             Collaborative PR/diff walkthrough
```

## Feature Parity with Claude Code

| Feature | Claude Code | OpenCode | Notes |
|---------|------------|----------|-------|
| Skills | Full | Full | Copied unchanged |
| Agents | Full | Full | Frontmatter converted to OpenCode format |
| Commands | N/A | Full | Generated from user-invocable skills |
| Stop hook (block) | Full | Degraded | session.idle is fire-and-forget; enforced via system guidance |
| Compaction recovery | Full | Full | experimental.session.compacting |
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
├── agents/                          # 16 converted agents (16 files)
│   ├── change-intent-reviewer.md
│   ├── code-bugs-reviewer.md
│   ├── operational-readiness-reviewer.md
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
│   ├── github-pr-lifecycle.md
│   ├── slack-poller.md
│   └── type-safety-reviewer.md
├── commands/                        # 9 user commands
│   ├── auto.md
│   ├── adr.md
│   ├── define.md
│   ├── do.md
│   ├── handoff.md
│   ├── figure-out.md
│   ├── figure-out-team.md
│   ├── prompt-engineering.md
│   └── walk-pr.md
├── skills/                          # 11 skills (core + tools)
│   ├── adr/
│   ├── auto/
│   ├── define/
│   ├── do/
│   ├── done/
│   ├── escalate/
│   ├── figure-out/
│   ├── figure-out-team/
│   ├── handoff/
│   ├── prompt-engineering/
│   └── walk-pr/
├── plugins/
│   ├── index.ts                     # Hook plugin
│   └── HOOK_SPEC.md                 # Behavioral specification
├── AGENTS.md                        # Context file
├── README.md                        # This file
├── install.sh                       # Installation script
└── install_helpers.py               # Namespacing helper
```
