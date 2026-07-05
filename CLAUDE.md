# CLAUDE.md

## Project Overview

manifest-dev marketplace — manifest-driven workflows for Claude Code. `/define` interviews and writes a Manifest; `/do` executes the Manifest and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant. Ships agents and skills.

## Public Repository Discipline

This repo is public. Everything committed or posted to it — docs, ADRs, READMEs, PR titles and descriptions, commit messages, issue text — must stand on its own merits and stay free of private working context. Never reference: chat sessions or session logs, private planning/strategy/handoff documents, investigation transcripts, or the repo's own adoption/popularity status (star counts, usage levels, traction commentary). ADRs state decisions with their technical grounds, not the deliberation history behind them. Temporary ops documents are allowed when clearly marked, but must read as neutral, forward-looking operations content.

## Development Commands

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Test plugin locally
/plugin marketplace add /path/to/manifest-dev
/plugin install manifest-dev@manifest-dev-marketplace
```

## Foundational Documents

Read before building plugins:

- **@docs/CUSTOMER.md** - Who we build for, messaging guidelines
- **@CONTEXT.md** - Project language (Manifest, Deliverable, etc.) and relationships
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design
- **docs/adr/** - Architecture Decision Records

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

**Symlink note**: `.claude/` skills/agents are symlinked to their `claude-plugins/manifest-dev/` counterparts for local development on environments where plugins aren't supported yet. When modifying plugin components, **always edit the `claude-plugins/` version** — `.claude/` resolves through the symlink to the same file. (Previous revisions used hardlinks; Edit's atomic-replace routinely broke them, so the convention is symlinks now. New agents/skills should be added with `ln -s ../../claude-plugins/manifest-dev/agents/<name>.md .claude/agents/<name>.md`.)

**Local Claude skills → `.agents/skills/`**: `.agents/skills/` mirrors `.claude/skills/` for the Agent Skills Open Standard (Codex CLI, etc.). **Whenever you add a new skill under `.claude/skills/`, also create the matching symlink in `.agents/skills/`**:

```bash
ln -sfn ../../.claude/skills/<skill-name> .agents/skills/<skill-name>
```

### Plugin Components

Each plugin can contain:
- `agents/` - Specialized agent definitions (markdown)
- `skills/` - Skills with `SKILL.md` files (replaces deprecated commands)

**Naming convention**: Use kebab-case (`-`) for all file and skill names (e.g., `bug-fixer.md`, `clean-slop`).

### Skills

Skills are the primary way to extend Claude Code. Each skill lives in `skills/{skill-name}/SKILL.md`.

**Invocation modes**:
- **Auto-invoked**: Claude discovers and invokes skills based on semantic matching with the description
- **User-invoked**: Users can explicitly invoke via `/skill-name` (controlled by `user-invocable` frontmatter, defaults to `true`)
- **Programmatic**: Other skills can invoke skills by referencing them (e.g., "invoke the spec skill with arguments")

**Skill frontmatter**:
```yaml
---
name: skill-name           # Required: lowercase, hyphens, max 64 chars
description: '...'         # Required: max 1024 chars, drives auto-discovery
user-invocable: true       # Optional: show in slash command menu (default: true)
---
```

### Tool Definitions

**Skills**: Omit `tools` frontmatter to inherit all tools from the invoking context (recommended default).

**Agents**: Agents run in isolation and don't inherit tools from the invoking context. Declaring tools in frontmatter is optional — when omitted, the agent receives its default tool set.

### Invoking Skills from Skills

When a skill needs to invoke another skill, use clear directive language:

```markdown
Invoke the <plugin>:<skill> skill with: "<arguments>"
```

Examples:
- `Invoke the manifest-dev:define skill with: "$ARGUMENTS"`
- `Invoke the manifest-dev:figure-out skill`

**Why**: Vague language like "consider using the X skill" is ambiguous -- Claude may just read the skill file instead of invoking it. Clear directives like "Invoke the X skill" ensure the skill is actually called.

**Common agent capabilities to declare in frontmatter**:
- Running commands -> needs command execution tools
- Tracking progress -> needs todo/task management tools
- Writing files (logs, notes) -> needs file writing tools
- Invoking other skills -> needs skill invocation tools
- Spawning sub-agents -> needs agent spawning tools
- Searching files -> needs file search tools

**Agent audit**: Read the skill/prompt the agent follows, identify every capability mentioned (explicit or implicit), verify all are declared in frontmatter.

See each plugin's README for architecture details.

## ADR Format Ownership

`claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md` is the sole ADR write-time reference (the offer gate lives in figure-out's `WITH_DOCS.md`); ADRs are created through figure-out docs-mode sessions. Distributed skill files stay repo-agnostic — maintainer/governance notes like this one belong here, not in skill references that ship to user repos.

## Versioning

When updating plugin files, bump that plugin's `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new skills/agents
- **Major** (x.0.0): Breaking changes

Pi has its own source-owned package version in the repo-root `package.json` (`@doodledood/manifest-dev-pi`). Bump it when changing Pi runtime code, Pi package metadata, or Pi-distributed shared assets under `dist/pi/` (including adding/removing compatible skills). Keep the package manifest example in `.claude/skills/sync-tools/references/pi-cli.md` in sync with the real `package.json` version.

README-only changes don't require version bumps.

## Adding New Components

When adding agents or skills:
1. Create the component file in the appropriate directory
2. Bump plugin version (minor for new features)
3. Update affected plugin's `README.md` and repo root `README.md`
4. Update `plugin.json` description/keywords if the new component adds significant capability

**README sync checklist** (when adding/renaming/removing components):
- `README.md` (root) - Available Plugins section, directory structure
- `claude-plugins/README.md` - Plugin table
- `claude-plugins/<plugin>/README.md` - Component lists

**README Guidelines**: Keep READMEs high-level (overview, what it does, how to use). Avoid implementation details that require frequent updates -- readers can explore code for specifics.

### Task Files

Task files provide domain-specific hints, kept as **two parallel sets** with different consumers:

- **`/define`'s task files** (`skills/define/tasks/`) carry **Quality Gates** (auto-encoded as INV-G*/AC-*) and **Defaults** (auto-encoded as PG-*) — encoder data for the manifest.
- **figure-out's task files** (`skills/figure-out/tasks/`) carry **probing fuel** — non-natural angles (`## Blind-spot probes`, `## Forced trade-offs`) that figure-out surfaces during understanding.

Each skill carries its own task-type detection index inline in its `SKILL.md` (not a separate `tasks/README.md`) and loads its own set. The two are deliberately decoupled so figure-out runs standalone — figure-out never reads define's task files, and vice versa.

**Composition** (within each set): base files provide domain-common content (e.g., `CODING.md` for code); overlay files add content-type specificity (`FEATURE` / `BUG` / `REFACTOR` compose onto `CODING`; in /define's set, `BLOG` / `DOCUMENT` compose onto `WRITING`, and Research composes `research/RESEARCH.md` with `research/sources/`).

**/define content types**:
- *Quality gates* (tables with Agent + Threshold) — auto-included as INV-G*/AC-* by `/define`. Omitted with logged reasoning if clearly inapplicable. User reviews manifest.
- *Defaults* (`## Defaults` section) — included in the manifest as PG-* without probing; user reviews.
- *Reference files* (`references/*.md`) — lookup data for the verifier subagents `/do` spawns. Not loaded during `/define`.

A define task-file item belongs in exactly one type: if you can verify it from the output, it's a Quality Gate; if it's a non-verifiable process practice, it's a Default. Don't prescribe manifest encoding (PG vs INV vs AC) in task files — that's `/define`'s job.

**figure-out probe content**: angles to check, not instructions for how to do the work — each phrased as the question that opens a branch. **Non-natural only**: include a probe only if the model skips it by default (don't restate what a capable model raises unprompted). Keep files terse so they read as awareness, not an agenda to complete.

**When creating/modifying task files**:
1. Read existing files for structural patterns — define's set (gates + Defaults) and figure-out's set (Blind-spot probes + Forced trade-offs) differ.
2. Update the relevant skill's own inline index in its `SKILL.md` (`define/SKILL.md` and/or `figure-out/SKILL.md`).
3. If creating a base file, update overlay files to remove content that moved to the base.
4. Bump plugin version, update READMEs per sync checklist.

## File Operations

Prefer `cp` and `mv` bash commands over the Write tool when duplicating or moving files. Much faster for large files. Use Edit after `cp`/`mv` if changes are needed.

## Before PR

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy
```

Bump plugin version if plugin files changed.
