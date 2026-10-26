# CLAUDE.md

## Project Overview

manifest-dev marketplace — manifest-driven workflows for Claude Code. `/define` interviews and writes a Manifest; `/do` executes it and makes every Acceptance Criterion and Global Invariant hold on fresh evidence. Ships skills, not custom agents.

## Public Repository Discipline

This repo is public. Everything committed or posted to it — docs, ADRs, READMEs, PR titles and descriptions, commit messages, issue text — must stand on its own merits. Keep out what a reader would be worse off for seeing: credentials and secrets, the contents of private planning or strategy documents, anything personal, and links into chat sessions or transcripts nobody outside can open. Also skip commentary on the repo's own adoption or popularity (star counts, usage levels, traction) — a positioning choice, not a secrecy one.

Set the bar there and no lower. Incidental working detail is fine and not worth policing: a branch name, a local path, the name of a workflow mode, a note on how a change was produced. Treating those as exposure costs more than it protects. ADRs state decisions with their technical grounds, not the deliberation history behind them. Temporary ops documents are allowed when clearly marked, but must read as neutral, forward-looking operations content.

## Development Commands

```bash
# While iterating: lint and format (fixing), typecheck, test across every CPU; `scripts/setup.sh` once
scripts/check.sh --fix        # or one group: scripts/check.sh lint|types|tests
# The evidence a change rests on: the same checks through the harness
scripts/verify drive property-suite

# Test plugin locally
/plugin marketplace add /path/to/manifest-dev
/plugin install manifest-dev@manifest-dev
```

`tests/` asserts properties of the shipped prompts themselves — that gate examples use the current
schema, and two host-neutrality invariants over every
shipped Markdown file: no file names a host primitive (a plugin qualifier outside an HTML comment,
a Claude Code tool name, `CLAUDE.md` outside a detection or comparison, the word
"subagent"), and every skill a shipped skill names ships beside it — never marked
`metadata.internal`, and `user-invocable: false` when it exists only to be called. Adding a skill,
a dimension, or a delegation site can therefore turn the suite red without any Python changing,
and that red is the signal working as intended. The same suite fails when `dist/codex` drifts from
the source tree it copies. It also fails when a shipped file points to a section of another
(`` `FILE.md` → *Section* ``) that no longer exists there under that name.

`claude-plugins/manifest-dev/evals/` holds behavioral eval suites for `figure-out` and, under
`evals/define/` with its own README, for `define`. Each run is many model sessions, so the
owner runs a suite, or an agent runs one after asking and naming the cases and why. Every model
session this repository starts — an eval suite, a skill drive (`scripts/drive-skill.sh`), or a
document walk (`scripts/walk.sh`) — runs the `claude` CLI directly, with no container, the same
way locally and in a cloud session. It needs only `claude` on PATH and signed in. Each session
starts from a scratch directory outside the checkout, on a copy of the plugin, without the user's
settings, installed plugins, MCP servers or — for a drive — `~/.manifest-dev` records, and
records the CLI version rather than pinning it.
Drives and walks run through their recipes (`scripts/verify drive|walk <recipe>`, ask-first). A
suite runs from the repository root with
`scripts/evals/run_eval.sh <name> <out-json> --tag <figure-out|define> --ablation with-without --scaffold`
and the judge model and cost ceiling each README names; it keeps running after the shell that
started it exits, which a cloud session's command timeout needs, and `--wait` blocks until it
ends. On macOS each eval child may raise a keychain dialog, so suites run best in a cloud session.
`evals/README.md` → *Running a suite* has the rest, and also covers hill-climbing a prompt with
the scripts beside `run_eval.sh`. The suite measures **uplift** — every case runs with the plugin
and without it, and the headline number is Δ, not pass rate — so a case both arms pass teaches nothing and is
removed. `tests/` is a property suite that must stay green; the eval suite is a measurement whose
numbers go stale whenever a prompt it covers is edited, and its `evals/README.md` carries the
baseline, the held-out split, and — most importantly before trusting any result from it — how
much run-to-run noise it has. Read that section before using a Δ to justify a prompt change.

## Foundational Documents

Read before building plugins:

- **@NORTH_STAR.md** - The project's standing direction: what it is for and for whom, its principles, how it measures progress, the bets it rests on
- **@CONTEXT.md** - Project language (Manifest, Deliverable, etc.) and relationships
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design

## Project Surfaces

<!-- setup-project surfaces v11 -->

This project keeps its direction, vocabulary, and decision memory in the repo — shared ground for every contributor and agent, regardless of tooling.

**The North Star is the standing direction.** `NORTH_STAR.md` — what this project is for and for whom, the principles it holds, how it measures progress, and the bets it rests on — is imported above, so it is already in context. Where a harness does not support imports, read it at the start of every session. Use it to decide scope, priority, outward-facing claims, and any call the work's own contract does not settle — a mid-run pivot, whether to act on a review comment, what to leave alone. The choices made along the way live in `docs/adr/`, never in it. Each position carries a dated state (evidence / hypothesis / ruled / empty): new evidence may lower a state, but a position changes only by an authorized ruling, recorded with its decider and any explicit delegation; owner-retained ends and bounds stay with the owner. A line gives grounds for a second look, not a veto: before it cuts an option, check that it covers the case. Where it does, a person decides; a run with no person present follows it and raises the challenge. The full form is `docs/NORTH_STAR_CONVENTIONS.md` — it is self-contained.

**The glossary is not optional reading.** `CONTEXT.md` is imported above, so it is already in context. Where a harness does not support imports, read it at the start of every session before doing anything else. It exists to stop silent misreading, and nobody looks up a term they already believe they understand — which is why it is resident rather than referenced. Read it before naming things; add a term when the project settles one.

**Read `docs/adr/` before re-deciding something.** Open the index at `docs/adr/README.md` when you are about to decide a question a record may already cover, and when a change you are making contradicts or narrows one. Those two moments are the whole reason the corpus exists; outside them, leave it closed. A record gives grounds, not a veto: follow it where its reasons still hold, and reopen it where a premise no longer holds or a need it did not weigh makes sense. Outside the `Strategy` area, a run with no person present decides for itself and lists each record it reopened first in its report and pull request.

**Writing a decision record is one act, not three** — the record, the restatus, and the index, in one change. Step two is the one that gets dropped, and dropping any of them leaves the corpus asserting something untrue. Open `docs/adr/CONVENTIONS.md` before you start: it carries the bar, the template, and what each step actually requires.

**Verification — `scripts/verify`: how this project checks that its work still does its job.** Run it before saying a change works, when reproducing a reported problem, and when a change touches something one of its recipes covers (`scripts/verify list` shows them); a change that needs a check no recipe has adds one. Every check this project keeps is a recipe, its lint, types and tests among them: call their commands directly while iterating, and drive the recipe for the evidence a change rests on. Recipes without the ask-first mark are free: run them as often as they help — `property-suite` after every change. Recipes marked ask-first cost money, quota, load on shared systems or effects outside the repository: run those only when a person runs them or has agreed — ask first, naming the recipe and why. `scripts/verify --help` gives the rest. The behavior suites its `eval` recipes start cover `figure-out` and `define` only, on purpose; a change to a prompt that a case covers updates that case where the change affects what it tests, and marks it stale or, with the owner's agreement, runs it, as `claude-plugins/manifest-dev/evals/README.md` describes. `scripts/design-evals/` is the harness for the code instruments the `design` skill ships; its README says how to run it and what it does not measure.

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json` and a Cursor manifest beside it, `.cursor-plugin/plugin.json`
- `.cursor-plugin/marketplace.json` - Cursor registry of the same plugins
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

**Plugin skills load through the installed plugins.** Edit their source under `claude-plugins/`; test local changes by installing this checkout as a plugin marketplace. `dist/` is packaging: OpenCode, Pi and Cursor read `claude-plugins/*/skills`, while `dist/codex` is regenerated by `python3 scripts/sync_dist.py` and checked for drift by the test suite.

**Repository-local maintenance skills** live under `.claude/skills/` with matching `.agents/skills/` symlinks. Published plugin skills have no entry in either local directory. `tests/test_local_skill_symlinks.py` checks this boundary and the maintenance links.

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

The trigger stays in the loading layer. `SKILL.md` says which mode applies and what that mode loads; the deferred file never carries its own trigger, since it can only be read after the load the trigger was meant to gate. State it where a reader already looks for it — a `Modes` or `What loads` table beside the flags, the way `figure-out/SKILL.md` does.

Extraction is for bulk, not tidiness. A mode whose mechanics run to a paragraph stays inline: an indirection costs a load and a reader's place, and it can strand a trigger too subtle to survive the hop. Extract when a default invocation would otherwise carry substantial content it never reads — and when the alternative is restating one rule in two files that drift, prefer the restatement only where the files genuinely cannot reach each other. See `docs/adr/20260703-progressive-disclosure-triggers-live-in-loading-layer.md`.

**A shipped skill stands alone — `CONTEXT.md` is not loaded where it runs.** The glossary is resident in *this* repo's sessions because the context file imports it. A skill installed in someone else's project has none of that: it gets its own `SKILL.md`, whatever references its loading layer names, and nothing else. So every term a skill's behavior depends on is defined where the skill first uses it, and no shipped file defers a definition to the glossary, to another skill, or to a section a reader may never reach. `figure-out`'s canonicalization of *fog* at first use is the pattern; a forward reference inside one always-loaded file is the mild version of the same fault and still worth a gloss.

Keep the two vocabularies apart. The workflow's own terms — Manifest, Deliverable, Acceptance Criterion, Global Invariant, Ticket — are the product's language and travel with it, defined at use wherever the exact meaning binds. The words this repo uses to *reason about* its prompts — Spine, Altitude, Re-host, Door, House — are maintainer vocabulary: they belong in `CONTEXT.md`, ADRs, and this file, not in anything under `claude-plugins/` or `dist/`. A skill neither speaks them nor defines them.

None of this touches the user's own context file. Reading it, seeding it, and capturing into it are real skill behaviors — `setup-project` installs one and `figure-out`'s docs mode writes to it. Those name *the project context file* resolved by detection, never a fixed filename, and the file they mean is the user's, never this repo's.

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

The same split holds for the North Star: `docs/NORTH_STAR_CONVENTIONS.md` is this project's convention and governs; `claude-plugins/manifest-dev/skills/setup-project/references/NORTH_STAR_FORMAT.md` is the plugin's shipped default carrying the same content plus the installer-facing emission templates, and states the precedence rule. The two are kept in step — change one, change the other. Cadence (when a session offers a North Star update) stays with figure-out's docs mode.

Distributed skill files stay repo-agnostic — maintainer/governance notes like this one belong here, not in skill references or in `docs/adr/CONVENTIONS.md` or `docs/NORTH_STAR_CONVENTIONS.md`, which setup-project emits into other people's repositories.

## Setup-Project Surfaces Version

Every file setup-project copies or emits into projects — `figure-out/references/ADR_FORMAT.md`, `setup-project/references/NORTH_STAR_FORMAT.md`, and the verification harness under `setup-project/references/harness/` (the tool and its example settings and recipes) — is pinned to the latest surfaces version. `setup-project/references/CHANGES.md` lists one line per version and `setup-project/references/changes/vN.md` holds each version's items, so an update reads only the versions it offers and the always-read list grows by a line, not by every version's items. A change to any emitted file needs a new `changes/vN.md` and its line in `CHANGES.md` in the same change. The file lists what an installed project gains and carries the digest the version test prints on failure, and the version comment in the surfaces template of `NORTH_STAR_FORMAT.md` moves to `vN`. Installed projects record the version they carry, and an update offers only the entries after it, so a change shipped without a version never reaches them. HTML comments are outside the digest, so maintainer notes need no version. Each change that adds a version moves the one-behind eval case to the version before it — replacing that case, never adding one beside it, since every such case tests the same offer and each run is paid — graded on offering only the entries after that version, and moves `45-current-setup-offers-nothing` to the newest. `tests/test_setup_project_versions.py` fails when `45` does not record the newest version, when no case records the version before it, and when a case records an older version or two cases record that one. The upgrade guides in `setup-project/references/upgrades/` hold one `vN-to-current.md` per older version, each saying only what the next version gives a project at vN; setup-project follows a project's own guide and every later one, and adds them up so the project goes straight to the newest shape (`setup-project/SKILL.md` → *The update pass*). A new version therefore adds the guide for the version it supersedes and edits no other version guide; `MOVE_TO_HARNESS.md`, the move of a pre-v4 surface into the harness, changes only when the new version changes that move. The same test fails when a guide is missing, exists for the newest version, names a version after the one it gives, or records a version. This repository's `scripts/verify` and `scripts/verify.mts` are copies of the shipped tool, and the eval scaffolds that seed a harness embed it, so edit the shipped copy and run `python3 scripts/sync_dist.py`, which copies it to the others; `tests/test_verify.py` and `sync_dist.py --check` fail when any differs. `scripts/tsconfig.json` type-checks both `verify.mts` copies in strict mode (`npm --prefix scripts run typecheck`), with its dev dependencies in `scripts/package.json`, never in the root `package.json`, which Pi installs from.

## Red-Flag Mirror Pairs

figure-out's task files and define's task files are decoupled, so a red-flag list both need lives in both. Change one, change the other:

- `figure-out/tasks/CODING.md` (*Shape before build*, *Already provided*, *Earned depth*, *A second shape*, *What the next agent copies*, *Design discipline*, *Recorded intent*, *Drivable and debuggable*, *Failure visibility*, *Silent regression*, *Verification design*'s independent expected values and whether example tests can reach the case that breaks, and *The verification harness*'s fit-to-trust question) ↔ `define/tasks/CODING.md` Defaults (*Sketch the shape before implementing*, *Use what is already provided*, *Earn each module's depth*, *Screen for what the next agent copies*, *Hold the design discipline*, *Read the intent before removing or adding a guard*, *Make failure visible and the result drivable*, *Name what could regress silently*, *Agree test seams before authoring tests*, *Reshape, don't patch*, *Trust the check before relying on it*).
- `figure-out/tasks/FEATURE.md` (*Bundled concerns*, *Remembered steps*, *Rollback*, *Orphaned resources*) ↔ `define/tasks/FEATURE.md` Defaults (*One concern per change*, *No step that depends on memory*, *Define rollback strategy*) and its *Bounded growth* gate.
- `figure-out/tasks/DOCUMENT.md` (*One mode*, *A fact restated*, *The same fact twice*) ↔ `define/tasks/DOCUMENT.md` Defaults (*One mode per document*, *Generate or link what code owns*, *One copy of each fact*).
- `figure-out/tasks/DOCUMENT.md` and `WRITING.md` (*Sources in hand*) ↔ `define/tasks/PROSE_FLOOR.md` *Accuracy* gate; `figure-out/tasks/WRITING.md` (*The author's own point*) ↔ `define/tasks/WRITING.md` gates.
- `figure-out/tasks/UI.md` (*Every state*, *Who and where*, *Honest figures*, *First look*) ↔ `define/tasks/UI.md`'s design gate, whose `review-design` standards cover functional states, access, medium, figure fidelity, and where the eye lands first and the path it follows.
- `figure-out/tasks/PROMPTING.md` (*A protocol on shared state*; *A rule in two files*, including a contradicted one; *An instruction where a check belongs*) ↔ `define/tasks/PROMPTING.md` Defaults (*Model a shared protocol before shipping it*, *One rule, one place*).
- `figure-out/tasks/PERF.md` ↔ `define/tasks/PERF.md` (limiter, noise floor, fair comparison, harness first, unlike scenarios, bounded gain).

## Slicing Discipline Ownership

The rule that a slice must be exercisable end-to-end on its own — put in front of its real use rather than inspected as present — lives in two shipped skills: `/define`'s Deliverable cutting and `ticket-up`'s Ticket cutting (stated in both its `SKILL.md` and `references/TICKET_CONVENTION.md`). The duplication is deliberate: a shipped skill stands alone, and `ticket-up` authors Tickets from direct requests and figure-out handoffs that never pass through `/define`, so it cannot defer the rule there. Change one, change the others — a sharpening that lands in only one home leaves the other paths cutting by layer, which is the defect the rule exists to prevent. What the rule governs is where a cut falls, never how many Deliverables or Tickets come out; count stays with each skill's own unit test.

## manifest-dev-help Glossary Ownership

`manifest-dev-help/references/GLOSSARY.md` restates `CONTEXT.md`'s product terms for users, close to ASD-STE100 (about 90% of it) and with the why behind each, because no installed skill can read this repository's glossary. Every change to a `CONTEXT.md` entry rereads its manifest-dev-help entry in the same change: each manifest-dev-help entry records the fingerprint of the `CONTEXT.md` entry it was written from, and `tests/test_manifest_dev_help_skill.py` fails — printing the new fingerprint — when the two differ, when a term is added or removed on one side only, or when manifest-dev-help breaks STE's counted limits. A term only maintainers use goes in that test's `MAINTAINER_TERMS` instead. See `docs/adr/20261015-manifest-dev-help-answers-questions-about-manifest-dev-in-simplified-english.md`.

## Project Definition Ownership

What counts as a project — a repository or working folder holding, or about to hold, work later sessions will change, with a new one counting — and what does not (a chat with no workspace, a home or scratch folder, a folder holding one finished artifact, a question that does not concern the folder the session runs in) is stated in four shipped skills: `figure-out/SKILL.md` (*Modes and what loads*), `define/SKILL.md`, `do/SKILL.md` and `setup-project/SKILL.md`. The first three also say that one-off work inside a project is still project work, so it keeps its recipe gates. The duplication is deliberate: a shipped skill stands alone, and each of the four decides on its own whether to offer, build, read for or gate on a project surface. Change one, change the others; `tests/test_projectless.py` fails when a copy loses a shared clause. See `docs/adr/20261014-project-surfaces-follow-the-context.md`.

## Versioning

When updating plugin files, bump that plugin's `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new skills/agents
- **Major** (x.0.0): Breaking changes

Pi has its own source-owned package version in the repo-root `package.json` (`@doodledood/manifest-dev-pi`). Bump it when changing Pi package metadata, the prompt templates under `dist/pi/`, or the skill directories it points at (including adding or removing a skill). The Codex plugin manifests under `dist/codex/plugins/*/.codex-plugin/plugin.json` carry the same version as their source plugin, and `dist/opencode/plugin/package.json` carries `manifest-dev`'s. Each Cursor manifest, `claude-plugins/*/.cursor-plugin/plugin.json`, carries its plugin's version too.

README-only changes don't require version bumps.

## Adding New Components

When adding agents or skills:
1. Create the component file in the appropriate directory
2. Bump plugin version (minor for new features)
3. Update affected plugin's `README.md` and repo root `README.md`
4. Update the plugin's `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json` description/keywords if the new component adds significant capability

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
5. For a figure-out probe, trade-off line or reference file added, renamed or removed, update its row in the eval README's *Coverage* table — graders in a case, or the reason the suite cannot reach it; `tests/test_figure_out_coverage.py` fails until the row matches.

## File Operations

Prefer `cp` and `mv` bash commands over the Write tool when duplicating or moving files. Much faster for large files. Use Edit after `cp`/`mv` if changes are needed.

## Before PR

```bash
scripts/check.sh --fix                # fix lint and format while iterating
scripts/verify drive property-suite   # lint, types and tests through the harness; show its output in the PR
```

Bump plugin version if plugin files changed.

## Taste

Ratified steering preferences for this repo. Each states the preference, why it holds, and when it should yield — weigh them rather than obey them.

- **Default manifests here to no `check-pr` lifecycle gate.** Pull requests in this repo run no CI and have a single maintainer as the only reviewer, so CI, review-thread and mergeability criteria spend verification effort on nothing. The gate that the pull request shows the change working still applies: the maintainer reads it before merging. Include the lifecycle gate once a pull request carries required status checks, or a reviewer whose approval gates the merge.
- **Prototype renderings ship as Artifacts where the harness offers them.** When a session renders a disposable draft for reaction — figure-out's prototyping, or any render-to-react flow — publish it as an Artifact page rather than loose .md/.html files: in remote and web sessions loose files are hard to open, and a page the user can actually look at is the whole point of rendering. Yield to a plain file when the session has no Artifact capability, or when the user asks for the file itself.
- **Check prompt wording by its behavior, not by the maintainer's reading.** When a change rewords a prompt, a skill or an agent, show the wording working by driving the behavior cases it touches, new or existing eval cases, through `scripts/verify drive`, instead of asking the maintainer to judge the words. The maintainer judges a prompt change by what it makes a run do, not by its wording, so a drive is the evidence they rely on. Run a whole eval suite only when they ask, because each run is many paid sessions. Yield when the text must be approved as written, such as a public post, or when no case can reach the behavior; then say so.

## Coding Conventions

### Solution design

In any domain — code, process, tooling, docs, prompts — prefer the design that prevents a class of problems over the quick one that merely works today. And treat every problem you touch as one you should not meet again: leave the system so that class of problem cannot return, or costs less when it does.

- The cheapest class of bugs to prevent is the code never written — before designing, ask whether the requirement itself is needed, and say so when it isn't.
- Design so a class of bugs cannot occur, whether or not one has occurred yet: illegal states unrepresentable, the invariant enforced where it cannot be bypassed, one source of truth instead of two that can disagree. This is the default for new code as much as for a fix — the design that closes the class beats the patch that handles the instance in front of you.
- Among designs that close the class, take the one with the fewest moving parts and the least hidden coupling — unless the user asks to optimize for a different priority. Machinery heavier than the class it closes is over-engineering, not design.
- Fail loud. No fallback, catch-and-continue, or default value that masks a failure unless degraded operation is explicitly wanted — silent wrong behavior costs more than a crash.
- When the structural fix is out of reach of the change at hand, fix the instance and name the design that would close the class — don't ship the patch as if it settled the matter.
- After fixing a bug, sweep for sibling instances of the same defect pattern before calling it done — the class includes the copies that already shipped.
- A rule that lives as a sentence someone must remember is a check waiting to be written — when a convention can be enforced by a type, lint, test, or CI gate, propose the enforcement. Price it like any machinery: worth building where failure is expensive or the surface is shared, not on a solo surface already verified locally.
- A new dependency is a recurring cost, not a one-time one — prefer the standard library or what the repo already uses, and justify any addition.
- Clean the touched area enough for a durable fix; propose broader refactors separately.

### What counts as verified

- Evidence ranks: unit/integration tests > a written verification script > manual checking. Prefer targeted checks to full-suite reruns, and exhaust the automated options before asking the user to verify by hand.
- Code with existing test files gets its tests added or updated there, covering the layers the change actually touches — unit and integration where both apply.
- For e2e or integration work, write the verification script inline when feasible.
- Say plainly what you did not verify.

### Git and pull requests

- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`. Branches `feature/*`, `fix/*` unless the project says otherwise.
- Prefer several coherent medium PRs to one monolith when the work naturally splits. Slice vertically — one feature stage end-to-end, handler + service + entity + tests — not horizontally, where each slice carries no logic of its own and only makes sense combined. Small mechanical changes (renames, config, migrations, boilerplate) ride along with the logic that needs them; a sweeping mechanical refactor can still earn its own PR for reviewability. Don't grow a PR past its natural scope — split instead.
- Open PRs substantially complete. The title names the real scope — the workflow and modules touched, not the immediate symptom. The description leads with what the change does and why it needed this design — the cross-module flow, the non-obvious decisions, the invariants preserved — not a file-by-file list.
