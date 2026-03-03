# manifest-dev for OpenCode CLI

Verification-first manifest workflows for OpenCode. Plan work thoroughly with `/define`, execute against criteria with `/do`, verify everything passes with `/verify`.

## Components

| Type | Count | Description |
|------|-------|-------------|
| Skills | 6 | define, do, done, escalate, learn-define-patterns, verify |
| Agents | 12 | criteria-checker, 8 code reviewers, manifest-verifier, claude-md-adherence-reviewer, define-session-analyzer |
| Commands | 3 | /define, /do, /learn-define-patterns |
| Hook stubs | 3 | pretool-verify, stop-do, post-compact (require manual TS porting) |

## Install

### One-liner (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash
```

This downloads the latest release, copies skills, agents, commands, and plugin stubs into `.opencode/` in your current directory. Safe to re-run; won't overwrite a manually ported `index.ts`.

### Skills only (via npx)

If you only want the skills (no agents, commands, or hooks):

```bash
npx skills add doodledood/manifest-dev --all -a opencode
```

OpenCode also reads `.claude/skills/` natively, so Claude Code skills work without conversion.

### Manual

```bash
git clone https://github.com/doodledood/manifest-dev.git /tmp/manifest-dev

# Skills
cp -r /tmp/manifest-dev/dist/opencode/skills/* .opencode/skills/

# Agents
cp -r /tmp/manifest-dev/dist/opencode/agents/* .opencode/agents/

# Commands
cp -r /tmp/manifest-dev/dist/opencode/commands/* .opencode/commands/

# Plugin stubs
cp -r /tmp/manifest-dev/dist/opencode/plugins/* .opencode/plugins/
cd .opencode/plugins && bun install
```

## Feature Parity

| Feature | Claude Code | OpenCode | Notes |
|---------|------------|----------|-------|
| Skills (define, do, verify, done, escalate, learn-define-patterns) | Native | Native | Skills copy unchanged; OpenCode reads `.claude/skills/` natively |
| Agents (12 code reviewers + orchestration) | Native | Converted | Frontmatter converted to OpenCode format (boolean tools, mode, temperature) |
| Commands (/define, /do, /learn-define-patterns) | Skills with `user-invocable: true` | `.opencode/commands/*.md` | Commands invoke the corresponding skill |
| Hook: pretool-verify (context injection) | Python PreToolUse hook | Stub only | Needs manual TS port -- see HOOK_SPEC.md |
| Hook: stop-do (block premature stop) | Python Stop hook | Stub only | Needs manual TS port -- session.idle is non-blocking in OpenCode |
| Hook: post-compact (context recovery) | Python PreCompact hook | Stub only | Needs manual TS port -- experimental event |
| Subagent spawning | Agent tool | `task` tool | Mapped in agent frontmatter |
| Todo management | TaskCreate/TaskUpdate | `todowrite` tool | Mapped in agent frontmatter |
| Web research | WebFetch + WebSearch | `webfetch` + `websearch` | WebSearch requires Exa AI key in OpenCode |

## Known Limitations

1. **Hooks require manual TypeScript porting.** The Python hooks cannot run in Bun. Generated stubs in `plugins/index.ts` provide the structure; `plugins/HOOK_SPEC.md` provides the full behavioral specification for each hook.

2. **Stop-do enforcement has no blocking equivalent.** Claude Code's Stop hook can return `decision: block` to prevent the agent from stopping. OpenCode's `session.idle` event is non-blocking. A workaround using `tui.prompt.append` or `chat.message` may be needed.

3. **`experimental.session.compacting` is experimental.** The post-compact hook uses an experimental OpenCode event that may change between releases.

4. **`$ARGUMENTS` behavior is undefined in OpenCode skills.** Skills using `$ARGUMENTS` work in Claude Code but the variable substitution behavior is not standardized in OpenCode. Commands use `$ARGUMENTS` natively.

5. **WebSearch requires an Exa AI API key** in OpenCode (configured via `OPENCODE_EXA_API_KEY` or provider config). Claude Code's WebSearch works without additional configuration.

6. **Native `.claude/` compatibility.** OpenCode reads `.claude/skills/` natively (priority 2), so users who already have the Claude Code plugin installed may not need `dist/opencode/skills/` at all -- the skills are already discovered.

## Directory Structure

```
dist/opencode/
  AGENTS.md              # Workflow overview and agent descriptions
  README.md              # This file
  install.sh             # Idempotent installer
  agents/                # 12 converted agents
    criteria-checker.md
    code-bugs-reviewer.md
    code-design-reviewer.md
    code-simplicity-reviewer.md
    code-maintainability-reviewer.md
    code-coverage-reviewer.md
    code-testability-reviewer.md
    type-safety-reviewer.md
    docs-reviewer.md
    claude-md-adherence-reviewer.md
    manifest-verifier.md
    define-session-analyzer.md
  commands/              # 3 user-invoked commands
    define.md
    do.md
    learn-define-patterns.md
  plugins/               # Hook stubs (manual port needed)
    index.ts
    HOOK_SPEC.md
    package.json
  skills/                # 6 skills (copied unchanged from source)
    define/
    do/
    done/
    escalate/
    learn-define-patterns/
    verify/
```

## Source

This is a generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev) for Claude Code. The Claude Code plugin is the source of truth.
