# CLAUDE.md

## Project Overview

manifest-dev marketplace — manifest-driven workflows for Claude Code. `/define` interviews and writes a Manifest; `/do` executes it and evaluates every Acceptance Criterion and Global Invariant under a run-level verification mode. Ships skills, not custom agents.

## Public Repository Discipline

This repo is public. Everything committed or posted to it — docs, ADRs, READMEs, PR titles and descriptions, commit messages, issue text — must stand on its own merits. Keep out what a reader would be worse off for seeing: credentials and secrets, the contents of private planning or strategy documents, anything personal, and links into chat sessions or transcripts nobody outside can open. Also skip commentary on the repo's own adoption or popularity (star counts, usage levels, traction) — a positioning choice, not a secrecy one.

Set the bar there and no lower. Incidental working detail is fine and not worth policing: a branch name, a local path, the name of a workflow mode, a note on how a change was produced. Treating those as exposure costs more than it protects. ADRs state decisions with their technical grounds, not the deliberation history behind them. Temporary ops documents are allowed when clearly marked, but must read as neutral, forward-looking operations content.

## Development Commands

```bash
# Lint, format, typecheck, test
ruff check --fix claude-plugins/ tests/ && black claude-plugins/ tests/ && mypy && python3 -m pytest tests/

# Test plugin locally
/plugin marketplace add /path/to/manifest-dev
/plugin install manifest-dev@manifest-dev
```

`tests/` asserts properties of the shipped prompts themselves — that gate examples use the current
schema, that mode mechanics stay out of the spine, that the bare-name distributions carry the
qualifier strip their sync rules require. Adding a skill, a dimension, or a distribution can
therefore turn the suite red without any Python changing, and that red is the signal working as
intended.

It does not check the other direction. Whether a distribution carries a rewrite **no** rule
authorized is `/sync-tools`' own post-write check, not the suite's — so a green run is not evidence
that a `dist/` edit was authorized.

## Foundational Documents

Read before building plugins:

- **@NORTH_STAR.md** - The project's standing direction: who it's for, the promise, what winning means
- **@CONTEXT.md** - Project language (Manifest, Deliverable, etc.) and relationships
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design

## Project Surfaces

This project keeps its direction, vocabulary, and decision memory in the repo — shared ground for every contributor and agent, regardless of tooling.

**The North Star is the standing direction.** `NORTH_STAR.md` is imported above, so it is already in context; anchor scope, priority, and outward-facing claims on it. Each position carries a dated state (evidence / hypothesis / ruled / empty): new evidence may lower a state, but a position changes only by the owner's call, recorded as a decision record. The full form is `docs/NORTH_STAR_CONVENTIONS.md` — it is self-contained.

**The glossary is not optional reading.** `CONTEXT.md` is imported above, so it is already in context. Where a harness does not support imports, read it at the start of every session before doing anything else. It exists to stop silent misreading, and nobody looks up a term they already believe they understand — which is why it is resident rather than referenced.

**Read `docs/adr/` before re-deciding something.** Open the index at `docs/adr/README.md` when you are about to settle a question the project may already have settled, and when a change you are making contradicts or narrows an existing decision. Those two moments are the whole reason the corpus exists; outside them, leave it closed.

**Writing a decision record is one act, not three** — the record, the restatus, and the index, in one change. Step two is the one that gets dropped, and dropping any of them leaves the corpus asserting something untrue. Open `docs/adr/CONVENTIONS.md` before you start: it carries the bar, the template, and what each step actually requires.

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

**Symlink note**: `.claude/` skills/agents are symlinked to their `claude-plugins/manifest-dev/` counterparts for local development on environments where plugins aren't supported yet. When modifying plugin components, **always edit the `claude-plugins/` version** — `.claude/` resolves through the symlink to the same file. `dist/` is different — those are real per-CLI copies, not links, and each carries a transform, so a plugin change is not propagated until they are regenerated or edited in place. (Previous revisions used hardlinks; Edit's atomic-replace routinely broke them, so the convention is symlinks now. New agents/skills should be added with `ln -s ../../claude-plugins/manifest-dev/agents/<name>.md .claude/agents/<name>.md`.) `tests/test_local_skill_symlinks.py` fails a plugin skill with no `.claude/skills` link, a `.claude/skills` entry with no `.agents/skills` link, an `.agents/skills` entry whose counterpart is gone, and any link pointing at nothing.

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

**Keep `description` on one physical line**, however long it gets. Claude Code reads frontmatter leniently; Pi parses it with a strict YAML parser and drops the skill when the value does not parse — a startup warning names the file, but the skill is simply absent, and a Pi prompt template with the same fault is dropped with no diagnostic at all. A quoted value wrapped across lines parses only if its continuation lines are indented past the key, so a hard-wrapped description looks fine locally and disappears elsewhere, once per distribution copy. Two more shapes break the same way: an apostrophe inside a single-quoted value ends it early (double it — `''`), and in an unquoted value `: ` is read as a nested mapping while ` #` opens a comment that silently truncates the value.

`tests/test_skill_frontmatter.py` fails any shipped `SKILL.md` — and any Pi prompt template, which loads through the same parser — carrying one of these. It enforces the convention rather than the YAML spec: a validly indented continuation and a block scalar both parse everywhere and are still refused, because one physical line is the rule. It also takes a closed key vocabulary — `name`, `description`, `user-invocable`, `argument-hint`, `metadata` — since an unrecognised key at column 0 is nearly always a wrapped value; adding a frontmatter key a CLI supports means adding it to `KNOWN_KEYS` in the same change.

**A flag or a mode means progressive disclosure.** When a skill grows a flag or a mode, what every invocation needs stays inline in `SKILL.md`, and that mode's mechanics move to a companion file under `references/` loaded only when the mode resolves. Otherwise the default invocation — the one nobody passes a flag for, and the one most sessions run — carries the whole file to use a fraction of it.

The trigger stays in the loading layer. `SKILL.md` says which mode applies and what that mode loads; the deferred file never carries its own trigger, since it can only be read after the load the trigger was meant to gate. State it where a reader already looks for it — a `Modes` or `What loads` table beside the flags, the way `figure-out/SKILL.md` and `chat-surface/SKILL.md` do.

Extraction is for bulk, not tidiness. A mode whose mechanics run to a paragraph stays inline: an indirection costs a load and a reader's place, and it can strand a trigger too subtle to survive the hop. Extract when a default invocation would otherwise carry substantial content it never reads — and when the alternative is restating one rule in two files that drift, prefer the restatement only where the files genuinely cannot reach each other. See `docs/adr/20260703-progressive-disclosure-triggers-live-in-loading-layer.md`.

**A shipped skill stands alone — `CONTEXT.md` is not loaded where it runs.** The glossary is resident in *this* repo's sessions because the context file imports it. A skill installed in someone else's project has none of that: it gets its own `SKILL.md`, whatever references its loading layer names, and nothing else. So every term a skill's behavior depends on is defined where the skill first uses it, and no shipped file defers a definition to the glossary, to another skill, or to a section a reader may never reach. `figure-out`'s canonicalization of *fog* at first use is the pattern; a forward reference inside one always-loaded file is the mild version of the same fault and still worth a gloss.

Keep the two vocabularies apart. The workflow's own terms — Manifest, Deliverable, Acceptance Criterion, Global Invariant, Ticket — are the product's language and travel with it, defined at use wherever the exact meaning binds. The words this repo uses to *reason about* its prompts — Spine, Altitude, Re-host, Form Vocabulary, Door, House — are maintainer vocabulary: they belong in `CONTEXT.md`, ADRs, and this file, not in anything under `claude-plugins/` or `dist/`. A skill neither speaks them nor defines them.

None of this touches the user's own context file. Reading it, seeding it, and capturing into it are real skill behaviors — `init-context` installs one and `figure-out`'s docs mode writes to it. Those name *the project context file* resolved by detection, never a fixed filename, and the file they mean is the user's, never this repo's.

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

The same split holds for the North Star: `docs/NORTH_STAR_CONVENTIONS.md` is this project's convention and governs; `claude-plugins/manifest-dev/skills/init-context/references/NORTH_STAR_FORMAT.md` is the plugin's shipped default carrying the same content plus the installer-facing emission templates, and states the precedence rule. The two are kept in step — change one, change the other. Cadence (when a session offers a North Star update) stays with figure-out's docs mode.

Distributed skill files stay repo-agnostic — maintainer/governance notes like this one belong here, not in skill references or in `docs/adr/CONVENTIONS.md` or `docs/NORTH_STAR_CONVENTIONS.md`, which the init skill emits into other people's repositories.

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
- *Quality gates* (tables naming the aspect and threshold, plus a skill or reference only when the evaluation needs one) — auto-included as INV-G*/AC-* by `/define`. Omitted with logged reasoning if clearly inapplicable, or — advisory-tier gates only — on `/define`'s bearer test (the dimension's findings would have no bearer on the manifest's surface; the reasoning names the missing bearer as a fact). User reviews manifest.
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
# Lint, format, typecheck, test
ruff check --fix claude-plugins/ tests/ && black claude-plugins/ tests/ && mypy && python3 -m pytest tests/
```

Bump plugin version if plugin files changed.

## Taste

Ratified steering preferences for this repo. Each states the preference, why it holds, and when it should yield — weigh them rather than obey them.

- **Default manifests here to no PR-lifecycle gates.** Pull requests in this repo run no CI and have a single maintainer as the only reviewer, so lifecycle criteria spend verification effort on nothing. Include them once a pull request carries required status checks, or a reviewer whose approval gates the merge.
