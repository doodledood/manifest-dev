# CLAUDE.md

## Project Overview

manifest-dev marketplace — manifest-driven workflows for Claude Code. `/define` interviews and writes a Manifest; `/do` establishes its Outcome and every current Acceptance Criterion and Global Invariant on fresh evidence, preserving hard requirements while revising working choices through amendment. Ships skills, not custom agents.

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
owner runs a suite, or an agent runs one after asking and naming the cases and why. Behavior drives and document walks use a fresh general agent in the running host, with the
scenario as its brief and copied skills available as resources. No CLI or provider marker chooses
execution, and no target skill body is injected. The parent keeps expected outcomes outside the
subject and grades real artifacts. `scripts/NATIVE_DRIVES.md` owns the snapshot, fixture and
input-bound evidence helpers. If the host has no general agents, warn and ask what to do; a
same-host script fallback needs explicit approval, never an automatic provider switch. The
retained Claude CLI adapters and the Claude-native plugin-eval suite are separate explicit
instruments; individual drives do not prove native plugin registration or suite uplift.
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

<!-- setup-project surfaces v15 -->

This project keeps its direction, vocabulary, and decision memory in the repo — shared ground for every contributor and agent, regardless of tooling.

**The North Star is the standing direction.** `NORTH_STAR.md` — what this project is for and for whom, the principles it holds, how it measures progress, and the bets it rests on — is imported above, so it is already in context. Where a harness does not support imports, read it at the start of every session. Use it to decide scope, priority, outward-facing claims, and any call the work's own contract does not settle — a mid-run pivot, whether to act on a review comment, what to leave alone. The choices made along the way live in `docs/adr/`, never in it. Each position carries a dated state (evidence / hypothesis / ruled / empty): new evidence may lower a state, but a position changes only by an authorized ruling, recorded with its decider and any explicit delegation; owner-retained ends and bounds stay with the owner. A line gives grounds for a second look, not a veto: before it cuts an option, check that it covers the case. Where it does, a person decides; a run with no person present follows it and raises the challenge. The full form is `docs/NORTH_STAR_CONVENTIONS.md` — it is self-contained.

**The glossary is not optional reading.** `CONTEXT.md` is imported above, so it is already in context. Where a harness does not support imports, read it at the start of every session before doing anything else. It exists to stop silent misreading, and nobody looks up a term they already believe they understand — which is why it is resident rather than referenced. Read it before naming things; add a term when the project settles one.

**Read `docs/adr/` before re-deciding something.** Open the index at `docs/adr/README.md` when you are about to decide a question a record may already cover, and when a change you are making contradicts or narrows one. Those two moments are the whole reason the corpus exists; outside them, leave it closed. A record gives grounds, not a veto: follow it where its reasons still hold, and reopen it where a premise no longer holds or a need it did not weigh makes sense. Outside the `Strategy` area, a run with no person present decides for itself and lists each record it reopened first in its report and pull request.

**Writing a decision record is one act, not three** — the record, the restatus, and the index, in one change. Step two is the one that gets dropped, and dropping any of them leaves the corpus asserting something untrue. Open `docs/adr/CONVENTIONS.md` before you start: it carries the bar, the template, and what each step actually requires.

**Verification — `scripts/verify`: how this project checks that its work still does its job.** Run it before saying a change works, when reproducing a reported problem, and when a change touches something one of its recipes covers (`scripts/verify list` shows them); a change that needs a check no recipe has adds one. Every check this project keeps is a recipe, its lint, types and tests among them: call their commands directly while iterating, and drive the recipe for the evidence a change rests on. Recipes without the ask-first mark are free: run them as often as they help — `property-suite` after every change. Recipes marked ask-first cost money, quota, load on shared systems or effects outside the repository: run those only when a person runs them or has agreed — ask first, naming the recipe and why. Driving the behavior cases a prompt change touches is already agreed, as `prompt-principles` says; a whole eval suite is not. `scripts/verify --help` gives the rest. The behavior suites its `eval` recipes start cover `figure-out` and `define` only, on purpose; a change to a prompt that a case covers updates that case where the change affects what it tests, and marks it stale or, with the owner's agreement, runs it, as `claude-plugins/manifest-dev/evals/README.md` describes. `scripts/design-evals/` is the harness for the code instruments the `design` skill ships; its README says how to run it and what it does not measure.

- **Prompt work** — load the `prompt-principles` skill (`.claude/skills/prompt-principles/SKILL.md`) before planning, writing, reviewing or verifying a change to a prompt, a skill or an agent.
- **Product work** — load the `product-principles` skill (`.claude/skills/product-principles/SKILL.md`) before planning, designing, building or reviewing behavior manifest-dev ships.
- **Architecture work** — load the `architecture-principles` skill (`.claude/skills/architecture-principles/SKILL.md`) before planning, designing, building or reviewing how skills, wrappers, state and the workflow are structured.
- **Design work** — load the `design-principles` skill (`.claude/skills/design-principles/SKILL.md`) before planning, writing, building or reviewing the design guidance manifest-dev ships or a surface a skill renders for a person.

## Repository Structure

**Plugin skills load through the installed plugins.** Edit their source under `claude-plugins/`; test local changes by installing this checkout as a plugin marketplace. `dist/` is packaging: OpenCode, Pi and Cursor read `claude-plugins/*/skills`, while `dist/codex` is regenerated by `python3 scripts/sync_dist.py` and checked for drift by the test suite.

**Repository-local maintenance skills** live under `.claude/skills/` with matching `.agents/skills/` symlinks. Published plugin skills have no entry in either local directory. `tests/test_local_skill_symlinks.py` checks this boundary and the maintenance links.

**Naming convention**: Use kebab-case (`-`) for all file and skill names (e.g., `bug-fixer.md`, `clean-slop`).

### Skills

**Keep `description` on one physical line**, however long it gets. Claude Code reads frontmatter leniently; Pi parses it with a strict YAML parser and drops the skill when the value does not parse — a startup warning names the file, but the skill is simply absent, and a Pi prompt template with the same fault is dropped with no diagnostic at all. A quoted value wrapped across lines parses only if its continuation lines are indented past the key, so a hard-wrapped description looks fine locally and disappears elsewhere, once per distribution copy. Two more shapes break the same way: an apostrophe inside a single-quoted value ends it early (double it — `''`), and in an unquoted value `: ` is read as a nested mapping while ` #` opens a comment that silently truncates the value.

`tests/test_skill_frontmatter.py` fails any shipped `SKILL.md` — and any Pi prompt template, which loads through the same parser — carrying one of these. It enforces the convention rather than the YAML spec: a validly indented continuation and a block scalar both parse everywhere and are still refused, because one physical line is the rule. It also takes a closed key vocabulary — `name`, `description`, `user-invocable`, `argument-hint`, `metadata` — since an unrecognised key at column 0 is nearly always a wrapped value; adding a frontmatter key a CLI supports means adding it to `KNOWN_KEYS` in the same change.

## ADR Convention Ownership

`docs/adr/CONVENTIONS.md` is this project's ADR convention and governs here — the bar, the template and its `Area` field, naming, lifecycle, immutability, cross-references, and the index rebuild rules. Edit that file when the practice should change.

`claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md` is the plugin's shipped default, carrying the same content for projects that have no conventions file of their own; it also states the precedence rule. The two are kept in step — change one, change the other. figure-out's `WITH_DOCS.md` owns only *cadence*: when a session offers to record a decision. A project's conventions file has no say in cadence, and the plugin has no say in a project's conventions.

The same split holds for the North Star: `docs/NORTH_STAR_CONVENTIONS.md` is this project's convention and governs; `claude-plugins/manifest-dev/skills/setup-project/references/NORTH_STAR_FORMAT.md` is the plugin's shipped default carrying the same content plus the installer-facing emission templates, and states the precedence rule. The two are kept in step — change one, change the other. Cadence (when a session offers a North Star update) stays with figure-out's docs mode.

Distributed skill files stay repo-agnostic — maintainer/governance notes like this one belong here, not in skill references or in `docs/adr/CONVENTIONS.md` or `docs/NORTH_STAR_CONVENTIONS.md`, which setup-project emits into other people's repositories.

## Setup-Project Surfaces Version

**Changing a file setup-project emits** — `figure-out/references/ADR_FORMAT.md`, `setup-project/references/NORTH_STAR_FORMAT.md`, or anything under `setup-project/references/harness/`, which this repository's `scripts/verify` copies: load the `bump-surfaces-version` skill first. It carries the version, changes, eval-case and upgrade-guide steps; `tests/test_setup_project_versions.py` and `tests/test_verify.py` fail when one is missed.

## Red-Flag Mirror Pairs

**Editing a task file under `figure-out/tasks/` or `define/tasks/`**: load the `mirror-pairs` skill. A red-flag list both skills need lives in both files, so a change to one side changes the other.

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

**Composition** (within each set): base files provide domain-common content (e.g., `CODING.md` for code); overlay files add content-type specificity (`FEATURE` / `BUG` / `REFACTOR` compose onto `CODING`; `PERF` and `HILLCLIMB` compose onto `MEASURE`, and `HILLCLIMB` onto the artifact's own file too; in /define's set, `BLOG` / `DOCUMENT` compose onto `WRITING`, and Research composes `research/RESEARCH.md` with `research/sources/`).

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

Run `scripts/verify drive property-suite` and show its output in the PR. Bump plugin version if plugin files changed.

## Taste

Ratified steering preferences for this repo. Each states the preference, why it holds, and when it should yield — weigh them rather than obey them.

- **Default manifests here to no `check-pr` lifecycle gate.** Pull requests in this repo run no CI and have a single maintainer as the only reviewer, so CI, review-thread and mergeability criteria spend verification effort on nothing. The gate that the pull request shows the change working still applies: the maintainer reads it before merging. Include the lifecycle gate once a pull request carries required status checks, or a reviewer whose approval gates the merge.
- **Prototype renderings ship as Artifacts where the harness offers them.** When a session renders a disposable draft for reaction — figure-out's prototyping, or any render-to-react flow — publish it as an Artifact page rather than loose .md/.html files: in remote and web sessions loose files are hard to open, and a page the user can actually look at is the whole point of rendering. Yield to a plain file when the session has no Artifact capability, or when the user asks for the file itself.

## Coding Conventions

### Solution design

In any domain — code, process, tooling, docs, prompts — prefer the design that prevents a class of problems over the quick one that merely works today. And treat every problem you touch as one you should not meet again: leave the system so that class of problem cannot return, or costs less when it does. At any size of change, also make the next change — by anyone, human or agent — easier to get right, in proportion to how often that area changes; sound existing structure needs no redesign. This is an investment, not polish: time spent up front making code harder to get wrong is repaid as speed on every later change.

- Be ambitious; you are not human (my rule, 2026-10-30). A "make it faster" ask aims at about 100x, not +20%, and starts by asking what would make that possible; a rewrite or new architecture is fair game when it serves the goal. Estimate in agent time, minutes or hours rather than human weeks, and never scope down, phase out or defer work for a human-speed estimate. State the target and the assumption it rests on, so it can be challenged.
- The cheapest class of bugs to prevent is the code never written — before designing, ask whether the requirement itself is needed, and say so when it isn't. That includes what you propose yourself: an extra mode, rival path, or option earns a place in the build only when the next decision needs it; otherwise name it as a later addition.
- Design so a class of bugs cannot occur, whether or not one has occurred yet: illegal states unrepresentable, the invariant enforced where it cannot be bypassed, one source of truth instead of two that can disagree. This is the default for new code as much as for a fix — the design that closes the class beats the patch that handles the instance in front of you.
- Among designs that close the class, take the one with the fewest moving parts and the least hidden coupling. Reshaping a widely used type earns its churn when ordinary callers could otherwise get the next change wrong — which is usually why the bug happened; when every caller already passes through one owning operation, enforcing the invariant there is enough. Machinery heavier than the burden it removes is over-engineering, not design — unless the user asks to optimize for a different priority.
- Fail loud. No fallback, catch-and-continue, or default value that masks a failure unless degraded operation is explicitly wanted — silent wrong behavior costs more than a crash.
- A bug fix closes its class across the whole codebase by default, not only where the bug surfaced: if a loose string should have been a strict type, the type changes everywhere that value flows, and every sibling instance gets the same structural fix rather than its own patch. The wider diff is the point, not scope creep. Once the class is closed, delete what it made redundant — defensive checks and tests that only guarded the now-impossible state — but validation of untyped input (API payloads, database rows, user input) moves to the boundary where that input enters rather than disappearing. When the fix is urgent or the sweep is large, land the instance fix first and close the class in the change right after — sequenced, not dropped.
- When closing the class is genuinely out of reach, fix the instance and name the design that would close it — don't ship the patch as if it settled the matter.
- A rule that lives as a sentence someone must remember is a check waiting to be written — when a convention can be enforced by a type, lint, test, or CI gate, propose the enforcement. Price it like any machinery: worth building where failure is expensive or the surface is shared, not on a solo surface already verified locally.
- A new dependency is a recurring cost, not a one-time one — prefer the standard library or what the repo already uses, and justify any addition.
- Favor locality: keep what changes together in one place, so a change, a fix, or a check is made once rather than at every site. Work that has to be repeated across many sites points to a missing seam — close it when the work already passes through those sites or a bug class runs through it, and propose it separately otherwise. Clean the touched area enough for a durable fix either way.
- Unused is off. When a change removes or narrows something, delete what it leaves unused — code, config, flags, tests, docs, and mentions of the removed concept — rather than keeping or explaining it; keep an unused part only when the user explicitly asks for it. Leftovers mislead the next session about what is live.

### What counts as verified

- Evidence ranks: unit/integration tests > a written verification script > manual checking. Prefer targeted checks to full-suite reruns, and exhaust the automated options before asking the user to verify by hand.
- Code with existing test files gets its tests added or updated there, covering the layers the change actually touches — unit and integration where both apply.
- For e2e or integration work, write the verification script inline when feasible.
- Say plainly what you did not verify.

### Every pull request leaves the repository better

Each pull request must move the repository to a better place (my rule, 2026-10-28, for every repository, bot and coding session).

- Fix the debt on the pull request itself: what the work leaves behind or its review finds, not flagged for later. Pre-existing issues the work runs into get fixed there too, related or not. Only a gigantic one, a project of its own, stays out: ticket or report it with the reason.
- Nothing merges until everything passes, tests included. A test that cannot run is a failure of the app or its harness: fix the harness.
- Fix failures for real. Never reach green by removing, skipping or loosening a test, unless the test is useless or tautological; then say so in the description.

### Git and pull requests

- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`. Branches `feature/*`, `fix/*` unless the project says otherwise.
- Ship work as vertical slices (my rule, 2026-10-31). A ticket lands as small PRs off main, each a thin end-to-end slice — one feature stage through every layer it touches, handler + service + entity + tests — that is safe to land on its own. Vertical PRs, not layer PRs that carry no logic of their own and only make sense combined.
  - Don't over-split: each PR is a meaningful slice a reviewer can understand on its own, and a simple feature stays one PR rather than a pile of tiny ones. Aim for the fewest PRs that each land safely on their own.
  - Unfinished UI stays unreachable from the app's navigation or behind a flag. The final PR only wires the feature in so users can see it.
  - Stack PRs only when slices truly depend on each other, as deep as those dependencies need; otherwise each slice branches off main.
  - Small mechanical changes (renames, config, migrations, boilerplate) ride along with the logic that needs them; a sweeping mechanical refactor can still earn its own PR for reviewability. A PR's debt and the non-gigantic pre-existing issues it runs into are within its scope (see above).
- Open PRs substantially complete. The title names the real scope — the workflow and modules touched, not the immediate symptom. The description leads with what the change does and why it needed this design — the cross-module flow, the non-obvious decisions, the invariants preserved — not a file-by-file list.

### Browser automation

Scripts and tests that drive a browser (screenshots, Playwright, Puppeteer, CDP) launch Playwright's bundled Chromium or Chrome for Testing, never the installed `/Applications/Google Chrome.app`, and close the browser cleanly. Each launch of the installed Chrome copies the whole app (about 750 MB) into `/private/var/folders`, and a killed launch leaves that copy behind, which filled about 78 GB on my Mac in hours (2026-10-26).
