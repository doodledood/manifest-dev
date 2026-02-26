# manifest-dev for Codex CLI

Verification-first manifest workflow skills for OpenAI's Codex CLI.

**Important**: This is a skills-only distribution. Codex CLI does not support markdown agents or event hooks.

## Installation

Using npx skills (universal installer):
```bash
npx skills add https://github.com/doodledood/manifest-dev --all
```

Using Codex's $skill-installer (within Codex session):
```
$skill-installer --repo https://github.com/doodledood/manifest-dev --path skills/<skill-name>
```

Manual installation:
```bash
cp -r dist/codex/skills/* .agents/skills/
```

## Feature Parity

| Component | Status | Notes |
|-----------|--------|-------|
| Skills (define, do, verify, done, escalate) | Full | SKILL.md copied unchanged — universal format |
| Agents (11 reviewers + checkers) | Descriptions only | See AGENTS.md — Codex agents are TOML, incompatible with markdown |
| Hooks | Not available | Codex has no hook system (GitHub Issue #2109, 434 upvotes) |
| Skill chaining (define -> do -> verify -> done) | Advisory only | Works via skill invocation but not enforced without hooks |

## Components

### Skills
Copied unchanged from Claude Code plugin. The Agent Skills Open Standard (agentskills.io) ensures universal compatibility. Skills are enabled by default since Codex v0.97.0 with live detection.

### AGENTS.md
Human-readable descriptions of all 11 manifest-dev agents. These cannot run as scoped subagents on Codex (incompatible paradigms) but understanding them helps when using the manifest workflow.

## Known Limitations

1. **Skills only** — No agents, no hooks. Most restricted distribution target.
2. **No workflow enforcement** — Without hooks, the define->do->verify->done chain is advisory only. Nothing prevents premature stops or skipping verification.
3. **No scoped subagents** — Codex has only 2 tools (shell, apply_patch). Agent conversion is impossible.
4. **Skill chaining may be unreliable** — Codex skill-to-skill invocation is less documented than Claude Code's.
5. **Hooks may come eventually** — GitHub Issue #2109 is highly upvoted. If hooks ship, this distribution could expand significantly.

## Keeping Up to Date

This distribution is generated from the Claude Code plugin source. When the source changes, regenerate by running `/sync-tools` in the Claude Code plugin, or manually copy updated files.
