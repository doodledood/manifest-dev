# CLAUDE.md

## Project Overview

manifest-dev marketplace — manifest-driven workflows for Claude Code. `/define` interviews and writes a Manifest; `/do` executes it and evaluates every Acceptance Criterion and Global Invariant under a run-level verification mode. Ships skills, not custom agents.

## Public Repository Discipline

This repo is public. Everything committed or posted to it — docs, ADRs, READMEs, PR titles and descriptions, commit messages, issue text — must stand on its own merits. Keep out what a reader would be worse off for seeing: credentials and secrets, the contents of private planning or strategy documents, anything personal, and links into chat sessions or transcripts nobody outside can open. Also skip commentary on the repo's own adoption or popularity (star counts, usage levels, traction) — a positioning choice, not a secrecy one.

Set the bar there and no lower. Incidental working detail is fine and not worth policing: a branch name, a local path, the name of a workflow mode, a note on how a change was produced. Treating those as exposure costs more than it protects. ADRs state decisions with their technical grounds, not the deliberation history behind them. Temporary ops documents are allowed when clearly marked, but must read as neutral, forward-looking operations content.

## Development Commands

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Test plugin locally
/plugin marketplace add /path/to/manifest-dev
/plugin install manifest-dev@manifest-dev
```

## Foundational Documents

Read before building plugins:

- **@docs/CUSTOMER.md** - Who we build for, messaging guidelines
- **@CONTEXT.md** - Project language (Manifest, Deliverable, etc.) and relationships
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design

## Project Language and Decision Records

**The glossary is not optional reading.** `CONTEXT.md` is imported above, so it is already in context. Where a harness does not support imports, read it at the start of every session before doing anything else. It exists to stop silent misreading, and nobody looks up a term they already believe they understand — which is why it is resident rather than referenced.

**Read `docs/adr/` before re-deciding something.** Open the index at `docs/adr/README.md` when you are about to settle a question the project may already have settled, and when a change you are making contradicts or narrows an existing decision. Those two moments are the whole reason the corpus exists; outside them, leave it closed.

**Writing a decision record is one act, not three.** When a decision meets the bar in `docs/adr/CONVENTIONS.md`, the same change must:

1. write the new record;
2. update the Status of every record whose standing it changes — superseded, narrowed, or partly lifted;
3. rebuild `docs/adr/README.md` per the rebuild rules in `docs/adr/CONVENTIONS.md`.

Doing one or two leaves the corpus asserting something untrue, and step 2 is the one that gets dropped. `docs/adr/CONVENTIONS.md` carries the bar, the template, and the rules — consult it there rather than working from memory.

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

**Symlink note**: `.claude/` skills/agents are symlinked to their `claude-plugins/manifest-dev/` counterparts for local development on environments where plugins aren't supported yet. When modifying plugin components, **always edit the `claude-plugins/` version** — `.claude/` resolves through the symlink to the same file. `dist/` is different — those are real per-CLI copies, not links, and each carries a transform, so a plugin change is not propagated until they are regenerated or edited in place. (Previous revisions used hardlinks; Edit's atomic-replace routinely broke them, so the convention is symlinks now. New agents/skills should be added with `ln -s ../../claude-plugins/manifest-dev/agents/<name>.md .claude/agents/<name>.md`.)

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

## ADR Convention Ownership

`docs/adr/CONVENTIONS.md` is this project's ADR convention and governs here — the bar, the template and its `Area` field, naming, lifecycle, immutability, cross-references, and the index rebuild rules. Edit that file when the practice should change.

`claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md` is the plugin's shipped default, carrying the same content for projects that have no conventions file of their own; it also states the precedence rule. The two are kept in step — change one, change the other. figure-out's `WITH_DOCS.md` owns only *cadence*: when a session offers to record a decision. A project's conventions file has no say in cadence, and the plugin has no say in a project's conventions.

Distributed skill files stay repo-agnostic — maintainer/governance notes like this one belong here, not in skill references or in `docs/adr/CONVENTIONS.md`, which the init skill emits into other people's repositories.

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

- **`/define`'s task files** (`skills/define/tasks/`) carry **Quality Gates** (auto-encoded as INV-G*/AC-*) and **Defaults** (auto-encoded as PG-*, except one whose violation would be unsafe or irreversible, which routes to a Global Invariant) — encoder data for the manifest.
- **figure-out's task files** (`skills/figure-out/tasks/`) carry **probing fuel** — non-natural angles (`## Blind-spot probes`, `## Forced trade-offs`) that figure-out surfaces during understanding.

Each skill carries its own task-type detection index inline in its `SKILL.md` (not a separate `tasks/README.md`) and loads its own set. The two are deliberately decoupled so figure-out runs standalone — figure-out never reads define's task files, and vice versa.

**Composition** (within each set): base files provide domain-common content (e.g., `CODING.md` for code); overlay files add content-type specificity (`FEATURE` / `BUG` / `REFACTOR` compose onto `CODING`; in /define's set, `BLOG` / `DOCUMENT` compose onto `WRITING`, and Research composes `research/RESEARCH.md` with `research/sources/`).

**/define content types**:
- *Quality gates* (tables naming the aspect and threshold, plus a skill or reference only when the evaluation needs one) — auto-included as INV-G*/AC-* by `/define`. Omitted with logged reasoning if clearly inapplicable. User reviews manifest.
- *Defaults* (`## Defaults` section) — included in the manifest as PG-* without probing; user reviews. A Default whose violation would be unsafe or irreversible routes to a Global Invariant instead, so it binds.
- *Reference files* (`references/*.md`) — lookup data for gate evaluators. Not loaded during `/define`.

A define task-file item belongs in exactly one type: if you can verify it from the output, it's a Quality Gate; if it's a non-verifiable process practice, it's a Default. A safety rule whose violation would be unsafe or irreversible is a Default even when it is verifiable — a Quality Gate ships the gate text the task file authors, written with no sight of the repo, the branch, or the run, while a Default routed by `/define` gets its invariant written with that context. Don't prescribe manifest encoding (PG vs INV vs AC) in task files — that's `/define`'s job.

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

## Taste

Ratified steering preferences for this repo. Each states the preference, why it holds, and when it should yield — weigh them rather than obey them.

- **Default manifests here to no PR-lifecycle gates.** Pull requests in this repo run no CI and have a single maintainer as the only reviewer, so lifecycle criteria spend verification effort on nothing. Include them once a pull request carries required status checks, or a reviewer whose approval gates the merge.
