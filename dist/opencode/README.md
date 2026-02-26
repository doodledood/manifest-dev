# manifest-dev for OpenCode

Verification-first manifest workflows adapted for OpenCode CLI.

## Installation

For skills only (universal installer):
```bash
npx skills add https://github.com/doodledood/manifest-dev --all -a opencode
```

For the full distribution (skills + agents + hook stubs):
```bash
# Copy skills
cp -r dist/opencode/skills/* .opencode/skills/

# Copy agents
cp -r dist/opencode/agents/* .opencode/agents/

# Hook stubs require manual JS/TS implementation
# See hooks/HOOK_SPEC.md for behavioral specification
```

## Feature Parity

| Component | Status | Notes |
|-----------|--------|-------|
| Skills (define, do, verify, done, escalate) | Full | SKILL.md copied unchanged — universal format |
| Agents (11 reviewers + checkers) | Full | Frontmatter converted (boolean tools object, lowercase names) |
| Hooks (stop, verify-gate, compact-recovery) | Stubs only | JS/TS rewrite required — Python hooks cannot run in Bun |
| Skill chaining (define -> do -> verify -> done) | Full | OpenCode's skill tool has same semantics as Claude Code |

## Components

### Skills
Copied unchanged. OpenCode reads `.claude/skills/` natively, so Claude Code skills already work without this distribution. The dist/ provides standalone copies for `.opencode/skills/` placement.

### Agents
11 agents with tool names converted to OpenCode lowercase format:

| Claude Code Tool | OpenCode Tool |
|-----------------|---------------|
| Bash/BashOutput | bash |
| Read | read |
| Grep | grep |
| Glob | glob |
| WebFetch | webfetch |
| WebSearch | websearch |
| Task/TaskCreate | task |
| Skill | skill |

Agent mode set to `subagent` (spawned by other agents). Model set to `claude-sonnet-4-20250514`.

### Hooks
**Stubs only** — OpenCode plugins are JS/TS (Bun runtime). The Python hooks cannot be directly converted.

Provided:
- `hooks/index.ts` — Plugin skeleton with event bindings and behavioral comments
- `hooks/HOOK_SPEC.md` — Complete behavioral specification for manual porting

The spec covers: decision matrices, transcript parsing logic, state tracking, and OpenCode-specific implementation notes.

## Known Limitations

1. **Hooks require manual JS/TS rewrite** — The most significant limitation. Generated stubs provide structure but need implementation.
2. **No PreCompact equivalent** — OpenCode has `experimental.session.compacting` but it's experimental.
3. **No Notification hooks** — No equivalent to Claude Code's Notification event.
4. **Plugin API may evolve** — Generated stubs target the current API.
5. **Native .claude/ compat** — Users may not need this dist for skills at all (OpenCode reads .claude/ natively).
6. **Block pattern** — Use `output.abort = "reason"` (not throw) to block tool calls.

## Keeping Up to Date

This distribution is generated from the Claude Code plugin source. When the source changes, regenerate by running `/sync-tools` in the Claude Code plugin, or manually copy updated files. Note: hook stubs will be overwritten — save manual implementations separately.
