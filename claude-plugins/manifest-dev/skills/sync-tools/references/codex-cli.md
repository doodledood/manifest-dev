# Codex CLI Conversion Guide

Reference for converting Claude Code plugin components to Codex CLI format. Codex has the most limited compatibility — **skills only**.

## Scope: Skills Only

Codex CLI supports only SKILL.md-based skills from the Agent Skills Open Standard. The following Claude Code components CANNOT be converted:

| Component | Codex Support | Why |
|-----------|--------------|-----|
| Skills (SKILL.md) | YES — copy unchanged | Same open standard (agentskills.io) |
| Agents (markdown) | NO | Codex uses TOML config, not markdown. Only 2 tools (shell, apply_patch). Fundamentally incompatible paradigm. |
| Hooks (Python) | NO | Codex has NO hook system. GitHub Issue #2109 (434 upvotes, Aug 2025) — four PRs opened and closed (#2904, #4522, #9796, #11067). Feature not shipped as of v0.105.0 (Feb 2026). |

### Why Agents Are Incompatible

Claude Code agents are markdown files with YAML frontmatter declaring named tools:
```yaml
---
description: Reviews code for bugs
tools: Bash, Glob, Grep, Read, WebFetch, TaskCreate, WebSearch, BashOutput, Skill
---
Prompt instructions...
```

Codex agents are TOML config entries:
```toml
[agents.reviewer]
description = "Find security, correctness, and test risks in code."
config_file = "./agents/reviewer.toml"
```

Key incompatibilities:
- Codex has only 2 internal tools: `shell` (command execution) and `apply_patch` (file editing with custom patch format)
- No named tools like Read/Write/Grep/Glob — all file operations go through shell commands
- No per-agent tool scoping (sandbox policy is global)
- Multi-agent uses `agents.max_threads` and `agents.max_depth` config in config.toml, with built-in roles (default, worker, explorer, monitor) and separate TOML config files per agent
- AGENTS.md in Codex is general instructions (like CLAUDE.md), NOT agent definitions — managed by the Linux Foundation (60,000+ projects)

### Why Hooks Are Impossible

Codex CLI does NOT have a hook system comparable to Claude Code or Gemini CLI:
- **No PreToolUse/PostToolUse** — cannot intercept or block tool calls
- **No block/allow semantics** — nothing can gate agent behavior
- **notify only** — fire-and-forget command on `agent-turn-complete` event. JSON passed as argv[1] (NOT stdin). No return channel.
- **MCP cannot substitute** — MCP servers add new tools but cannot intercept existing tool calls (shell, apply_patch)

Reference: [GitHub Issue #2109](https://github.com/openai/codex/issues/2109) — 434 upvotes requesting event hooks following Claude Code's schema. Four PRs (#2904, #4522, #9796, #11067) opened and closed.

## AGENTS.md Approach

Since Codex agents are incompatible, the /sync-tools skill generates an AGENTS.md file containing human-readable descriptions of all manifest-dev agents. This gives Codex users awareness of what the agents do, even though they can't run them as scoped subagents.

The AGENTS.md file contains:
- Agent name and description (from frontmatter)
- What the agent does (from prompt body summary)
- Which tools it uses (informational — Codex can't scope tools)
- Suggested manual approach (how a Codex user might achieve similar results)

This follows Codex conventions where AGENTS.md is the primary project instructions file.

## Skill Handling

SKILL.md files are copied unchanged. This is the entire conversion — Codex implements the same Agent Skills Open Standard as Claude Code.

Skill subdirectories (scripts/, references/, assets/) are copied recursively.

### Codex-Specific Skill Behavior

- Discovery: `.agents/skills/` (walks from CWD to repo root), `~/.agents/skills/`, `~/.codex/skills/`
- Activation: explicit (`$skillname` or `/skills` menu) or implicit (auto-selected by description matching)
- Enable: `codex --enable skills` or config.toml (skills are enabled by default since v0.97.0; disable per-skill via `[[skills.config]]` entries)
- Live detection: since v0.97.0, new skills are detected without restarting the CLI
- Progressive disclosure: metadata loaded at startup, full SKILL.md on activation
- Optional `agents/openai.yaml` for Codex-specific metadata (interface, policy, dependencies — e.g., display_name, icon, brand_color, invocation policy)

### Claude Code Frontmatter Compatibility

Claude Code SKILL.md files may contain extensions not in the open standard:
- `user-invocable` — Codex silently ignores (uses agents/openai.yaml policy instead)
- `tools` — Codex silently ignores (not supported)
- `context` — Codex silently ignores (no equivalent)
- `agent` — Codex silently ignores (no equivalent)
- `hooks` — Codex silently ignores (no hook system)

Unknown frontmatter fields are silently ignored by Codex. Claude Code SKILL.md files load without modification.

## Directory Structure

```
manifest-dev-codex/
├── skills/                     # Skills (SKILL.md copied unchanged)
│   ├── define/
│   │   ├── SKILL.md
│   │   └── tasks/             # Subdirectories copied recursively
│   ├── do/
│   │   └── SKILL.md
│   └── verify/
│       └── SKILL.md
├── AGENTS.md                   # Agent descriptions (informational, not executable)
└── README.md
```

## Installation

Using npx skills (universal installer):
```bash
npx skills add <github-url> --all
```

Using Codex's $skill-installer (within Codex session):
```
$skill-installer --repo <github-url> --path skills/<skill-name>
```

Manual installation:
```bash
cp -r dist/codex/skills/* .agents/skills/
```

## Skill Chaining

Claude Code's define → do → verify → done chain relies on the Skill tool to invoke skills by name. Codex has skill invocation via `$skillname` syntax and implicit activation via description matching. Skills can reference other skills in their instructions and Codex will activate them.

However, the full manifest workflow (define → do → verify with hooks enforcing completion) fundamentally depends on hooks for enforcement. Without hooks, Codex users get the skills but not the verification enforcement. The workflow is advisory, not enforced.

## Known Limitations

1. **Skills only** — no agents, no hooks. This is the most restricted distribution target.
2. **No workflow enforcement** — without hooks, the define→do→verify→done chain is advisory. Codex can't block premature stops or enforce verification before completion.
3. **No scoped subagents** — Claude Code agents with restricted tool sets have no Codex equivalent. Codex's multi-agent system uses global sandbox policies.
4. **Only 2 tools** — Codex has shell and apply_patch. Agent conversion is impossible because the tool paradigm is fundamentally different.
5. **Skills may not chain reliably** — Codex's skill-to-skill invocation behavior is less documented than Claude Code's.
6. **Skills enabled by default** — since v0.97.0; disable per-skill via `[[skills.config]]` in config.toml. Live detection means no restart needed for new skills.
7. **Codex may add hooks eventually** — GitHub Issue #2109 is highly upvoted. If hooks ship, the Codex distribution could expand significantly. Monitor for updates.
8. **AGENTS.md is informational only** — the generated AGENTS.md describes agents but doesn't make them executable. Users must understand this is documentation, not functionality.
