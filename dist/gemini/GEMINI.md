# GEMINI.md

## Extension Overview

manifest-dev -- verification-first manifest workflows for Gemini CLI, with agents, skills, and hooks.

## Workflow

The core loop: **define -> do -> verify -> done/escalate**

1. `define` -- Interview-driven task specification producing a manifest with acceptance criteria, invariants, and verification methods
2. `do` -- Execute against the manifest, tracking progress in an execution log
3. `verify` -- Parallel verification of all criteria using specialized agents
4. `done` -- Formal completion after all criteria pass
5. `escalate` -- Structured handoff when blocked

## Components

### Skills (7)

Skills live in `skills/{skill-name}/SKILL.md`. Gemini activates them via `activate_skill`; this extension does not rely on user-facing slash commands.

| Skill | Description |
|-------|-------------|
| `auto` | End-to-end autonomous execution: define then do in one command |
| `define` | Interactive interview producing a verification manifest |
| `do` | Execute implementation against a manifest |
| `verify` | Parallel verification of manifest criteria |
| `done` | Formal completion with summary |
| `escalate` | Structured escalation when blocked |
| `learn-define-patterns` | Analyze past sessions to learn user preferences |

### Agents (14)

Agents run as subagents callable by tool name. The installer enables `"experimental": { "enableAgents": true }` automatically in `~/.gemini/settings.json`; manual installs must make the equivalent settings change.

| Agent | Purpose |
|-------|---------|
| `criteria-checker` | Validates a single criterion (PASS/FAIL) |
| `manifest-verifier` | Reviews manifests for gaps |
| `change-intent-reviewer` | Intent-behavior divergence -- does the change achieve its goal |
| `code-bugs-reviewer` | Mechanical defects -- runtime failures, resource issues, structural flaws |
| `code-design-reviewer` | Design fitness -- right approach given what exists |
| `code-simplicity-reviewer` | Unnecessary complexity, over-engineering |
| `code-maintainability-reviewer` | DRY, coupling, cohesion, consistency, dead code |
| `code-coverage-reviewer` | Test coverage with proactive edge case enumeration |
| `code-testability-reviewer` | Testability design -- mock friction, logic buried in IO |
| `contracts-reviewer` | API and interface contract correctness with evidence |
| `type-safety-reviewer` | Type holes, invalid states, narrowing gaps |
| `docs-reviewer` | Documentation accuracy against code changes |
| `context-file-adherence-reviewer` | Context file / project rule compliance |
| `define-session-analyzer` | Extracts user preference patterns from `define` sessions |

### Hooks (3)

Hooks enforce workflow discipline via the Gemini CLI hook protocol. The installer merges the `hooks/hooks.json` registrations into `~/.gemini/settings.json` automatically; manual installs must make the equivalent settings change.

| Hook | Event | Purpose |
|------|-------|---------|
| `pretool-verify` | BeforeTool (activate_skill) | Reminds the agent to load the manifest before `verify` |
| `stop-do-enforcement` | AfterAgent | Blocks premature stops during `do` |
| `post-compact-recovery` | SessionStart (resume) | Recovers `do` context after compaction |

## Tool Mapping

Agent tools use Gemini CLI internal names:

| Gemini CLI Tool | Purpose |
|-----------------|---------|
| `run_shell_command` | Execute shell commands |
| `read_file` | Read file contents |
| `write_file` | Write file contents |
| `replace` | Edit file (old_string/new_string) |
| `grep_search` | Search file contents |
| `glob` | Find files by pattern |
| `web_fetch` | Fetch web content |
| `google_web_search` | Google search |
| `activate_skill` | Invoke a skill |
| `write_todos` | Todo/task management |

## Manifest Archival

After the `define` skill completes, copy the final manifest from `/tmp/` to `.manifest/` with a descriptive name:

```bash
cp /tmp/manifest-{timestamp}.md .manifest/{descriptive-kebab-name}-{YYYY-MM-DD}.md
```

Manifests are committed to the repo for future reference. Discovery and execution logs stay in `/tmp/`.
