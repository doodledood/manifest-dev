---
name: define
description: 'Manifest builder. Plan work, scope tasks, spec out requirements, break down complex tasks before implementation. Converts needs into Deliverables + Invariants with verification criteria. Use when planning features, debugging complex issues, scoping refactors, or whenever a task needs structured thinking before coding.'
---

# /define - Manifest Builder

## Goal

Build **shared understanding** between you and the user about the work, then encode it as a **Manifest** capturing:
- **What we build** — Deliverables with Acceptance Criteria
- **How we'll get there** — Approach (initial direction, expect adjustment)
- **Rules we must follow** — Global Invariants

**Every criterion discovered now is one fewer rejection later.** Comprehensive means surfacing latent criteria: requirements the user doesn't know they have until probed. Coverage converges when the five Coverage Goal tests pass (see Convergence); amendments handle what emerges during implementation.

Output: `/tmp/manifest-{timestamp}.md` where `{timestamp}` is `YYYYMMDD-HHMMSS` in UTC. Use the same `{timestamp}` for the discovery log (`/tmp/define-discovery-{timestamp}.md`) so the two files can be linked as a pair.

## Prerequisites

Invoke `manifest-dev:thinking-disciplines` at the start of /define, before any other action. Apply throughout: every question, assessment, synthesis. (Idempotent — safe if already active.)

## Input

`$ARGUMENTS` = task description, optionally with context, plus any of:

| Flag | Values | Default | Behavior |
|------|--------|---------|----------|
| `--interview` | `minimal` \| `autonomous` \| `thorough` | `thorough` | Sets interview mode (see Interview Style). Invalid value → halt: "Invalid interview style '<value>'. Valid styles: minimal \| autonomous \| thorough". |
| `--mode` | `efficient` \| `balanced` \| `thorough` | `thorough` | Sets verification intensity (consumed by /do and the Verification Loop). Recorded in the manifest's `Mode` field. Invalid value → halt: "Invalid mode '<value>'. Valid modes: efficient \| balanced \| thorough". |
| `--medium` | `local` | `local` | Sets communication channel. Other values → halt: "Medium '<value>' not yet supported. Currently supported: local". |
| `--amend <path>` | manifest path | — | Amend an existing manifest (see Pre-flight). Missing argument → halt: "Cannot amend: --amend requires a manifest path." Path doesn't exist → halt: "Cannot amend: '<path>' not found." |
| `--from-do` | boolean flag (used with `--amend`) | — | Marks amendment as triggered by `/do`. Accepts no value. See `references/AMENDMENT_MODE.md` Three Contexts §2 (From /do). |
| `--canvas` | boolean flag | — | When present, follow `references/CANVAS_MODE.md` (it owns its own activation gate, lifecycle, and run-order placement). Accepts no value. |

Flags can appear anywhere in `$ARGUMENTS`. If `$ARGUMENTS` contains no task description (empty, or only flags with no free-form text), ask: "What would you like to build or change?" Exception: skip this prompt when **any** amend trigger applies — `--amend` is set, OR `$ARGUMENTS` contains a `/tmp/manifest-*.md` path (a bare path counts as routing, not as task text). Pre-flight handles amend context: the task description may live in conversation, the prior manifest, or be elaborated during the amendment interview.

## Pre-flight: Resolve Manifest Context

Pre-flight resolves to **amend** or **fresh**. When amend is selected, follow `references/AMENDMENT_MODE.md` for amendment rules.

- `--amend <path>` set, OR `$ARGUMENTS` contains any `/tmp/manifest-*.md` path → **amend** that manifest. Confirm approach with the user only if the referenced manifest's relationship to the new task is unclear.
- Transcript contains a prior `Manifest complete: /tmp/manifest-*.md` line, or such a path is mentioned in the conversation → read `references/AMENDMENT_MODE.md` "Session-Default Detection"; that section's branch determines amend or fresh.
- Else → **fresh**.

## Branch-Diff Seeding

**Trigger:** Pre-flight resolved to fresh AND the current branch has commits ahead of its base.

**Why:** Work already on the branch belongs in the manifest (Cumulative Manifest Rule — see `references/AMENDMENT_MODE.md`).

**Base inference** (first hit wins): upstream tracking branch → `origin/main` → `origin/master` → ask the user once.

If the user declines to identify a base, proceed with a **fresh** manifest and log the existing branch commits as a Known Assumption: `[ASM-N] Branch has commits ahead of an unidentified base | Default: treat as out of manifest scope | Impact if wrong: existing work isn't tracked or verified by this manifest.`

When base is identified, diff branch against base, read the diff and commit messages. Incorporate the existing changeset into the new manifest's Intent (what's already done) and starting Deliverables (work-in-progress as prior context, with new ACs added on top for completion + the new task). The interview confirms or adjusts what was inferred.

**Skip cleanly when:** no commits ahead of base, or Pre-flight resolved to amend.

## Domain Guidance

**Where this fits in the run order:** Pre-flight → Branch-Diff Seeding → Read task files (this section) → Multi-Repo detection → Encode quality gates + Defaults → Load interview mode file → Context Assessment → Interview → Approach Section → manifest write → Verification Loop → Summary → Complete.

Domain-specific guidance lives in `tasks/`:

| Domain | Indicators | File |
|--------|------------|------|
| **Coding** | Any code change (base for Feature, Bug, Refactor) | `tasks/CODING.md` |
| **Feature** | New functionality, APIs, enhancements | `tasks/FEATURE.md` |
| **Bug** | Defects, errors, regressions, "not working", "broken" | `tasks/BUG.md` |
| **Refactor** | Restructuring, "clean up", pattern changes | `tasks/REFACTOR.md` |
| **Prompting** | LLM prompts, skills, agents, system instructions | `tasks/PROMPTING.md` |
| **Writing** | Prose, articles, emails, copy, social, creative (base for Blog, Document) | `tasks/WRITING.md` |
| **Document** | Specs, proposals, reports, formal docs (base: Writing) | `tasks/DOCUMENT.md` |
| **Research** | Investigations, analyses, comparisons | `tasks/research/RESEARCH.md` |
| **Blog** | Blog posts, articles, tutorials (base: Writing) | `tasks/BLOG.md` |

**Composition.** Code-change tasks combine CODING.md (base quality gates) with domain specifics. Text-authoring tasks combine WRITING.md with content-type guidance. Research composes RESEARCH.md with source-type files in `tasks/research/sources/` (RESEARCH.md's Data Sources table lists what's available and probes which sources apply). Domains aren't mutually exclusive: a "bug fix that requires refactoring" benefits from both BUG.md and REFACTOR.md.

**Exception.** PROMPTING tasks do NOT compose with CODING.md unless the task also changes executable code. PROMPTING.md has its own quality gates. When a task changes both prompts AND code, apply both, scoping each to the relevant files.

**Task file structures are presumed relevant.** They contain quality gates (with their reviewer-agent fields), risks, scenarios, and trade-offs — domain-specific angles outside your default coverage. Quality gates auto-include; Resolvable structures (risks, scenarios, trade-offs) must be **resolved** per interview mode, or explicitly skipped with logged reasoning (e.g., "CODING.md concurrency risk skipped: single-threaded CLI tool"). Silent drops are the failure mode, not over-asking.

**Task file content types:**
- **Quality gates** (`## Quality Gates` section, any structured format with thresholds/criteria) — auto-include as INV-G*. Omit clearly inapplicable with logged reasoning. User reviews manifest.
- **Resolvable** (tables/checklists: risks, scenarios, trade-offs) — resolve via interview, encode as INV/AC, or explicitly skip.
- **Compressed awareness** (bold-labeled one-line summaries) — informs probing; no resolution needed.
- **Process guidance hints** (counter-instinctive practices LLMs would miss). Two modes:
  - **Defaults** (`## Defaults` section in the task file) — encoded pre-interview alongside Quality Gates; included in manifest without probing; user reviews and removes if not applicable.
  - **Candidates** — held until Failure Modes scenarios resolve, then presented as a single batch and resolved per interview mode.
  - Both become PG-*.
- **Reference files** (`references/*.md`) — lookup data for `/verify` agents. Do not load during interview.

**Encode quality gates and Defaults immediately after reading task files — before the interview.** Log each as `- [x]` RESOLVED.

Task files set the floor, not the ceiling — probe beyond when domain understanding warrants.

## Multi-Repo Scope

Detection rides on Domain Understanding (no separate probe). When conversation, task description, or branch context indicates multiple repos, read `references/MULTI_REPO.md` for schema additions and cross-repo verification rules.

## Principles

1. **Verifiable** — every Invariant and AC has automated verification. Constraints not verifiable from output go in Process Guidance. Manual only as last resort.
2. **Validated** — generate concrete candidates; learn from user reactions. The interview mode file defines behavioral specifics.
3. **Domain-grounded** — understand the domain before probing. You can't surface what you don't know.
4. **Complete** — surface hidden requirements through five coverage goals. Understanding from any source counts equally.
5. **Directed** — for complex tasks, establish initial Approach. Architecture defines starting direction, not step-by-step script.
6. **Question quality** — every question must change the manifest, lock an assumption, or choose between meaningful trade-offs. Never ask trivia.
7. **Err toward asking** — one missed criterion costs more than one extra question.

## Coverage Goals

Five goals that must be met before convergence. Each defines WHAT must be true and a convergence test. Items resolved from any source (conversation, prior research, task files, exploration) count equally — the interview probes gaps, not territory already covered. The active interview mode defines how gaps are probed and decisions are made.

| Goal | Convergence test |
|------|------------------|
| Domain Understanding | Can you generate project-specific (not generic) failure scenarios? |
| Reference Class | Can you name the task type and its common failure modes? |
| Failure Modes | All scenarios have dispositions (encoded, scoped out, or mitigated)? |
| Positive Dependencies | Load-bearing assumptions surfaced and each has a disposition? |
| Process Self-Audit | Every identified scope-creep pattern has a disposition (PG, INV, accepted, already-covered). Skippable for narrow scopes — see Process Self-Audit § Skip rule. |

### Domain Understanding

**What must be true:** you understand the affected area well enough to generate project-specific (not generic) failure scenarios. You know existing patterns, structure, constraints, and prior decisions relevant to the task.

When understanding is insufficient, fill gaps through whatever fits: explore code, search docs, ask the user what exploration can't reveal. Scope to what's relevant, not the entire domain.

Starting points: existing patterns (how similar things are done), structure (components, dependencies, boundaries in the affected area), constraints (implicit conventions, assumed invariants, existing contracts), prior decisions (why things are the way they are, when discoverable).

### Reference Class Awareness

**What must be true:** you know what type of task this is, what fails in that class, and those base-rate failures inform failure mode coverage.

Ground the reference class in domain understanding: "refactor of a tightly-coupled module with no tests" is useful; "refactor" is too generic. Task file warnings are a source.

### Failure Mode Coverage

**What must be true:** failure modes anticipated with concrete scenarios, each with a disposition. No dangling scenarios. Mental model alignment checked — your "done" matches the user's expectation.

**Failure dimensions** — starting lenses. Use these and any others relevant to the task:

| Dimension | What to imagine |
|-----------|-----------------|
| **Technical** | What breaks at the code/system level? |
| **Integration** | What breaks at boundaries? |
| **Stakeholder** | What causes rejection even if technically correct? |
| **Timing** | What fails later that works now? |
| **Edge cases** | What inputs/conditions weren't considered? |
| **Dependencies** | What external factors cause failure? |

Task files add domain-specific scenarios. Prefer domain-grounded scenarios over generic templates.

**Scenario disposition** — every scenario resolves to one of:
1. **Encoded as criterion** — INV-G*, AC-*, or Risk Area with detection.
2. **Explicitly out of scope** — user confirmed acceptable risk.
3. **Mitigated by approach** — architecture choice eliminates the failure mode.

The active interview mode defines how scenarios are presented and dispositions resolved.

### Positive Dependency Coverage

**What must be true:** load-bearing assumptions — what must go right for the task to succeed — are surfaced and each is resolved: verified, encoded as invariant, or logged as Known Assumption.

Where Failure Modes asks "what broke?", Positive Dependencies asks "what held?" Reveals assumptions you haven't examined.

Starting points: existing infrastructure/tooling you're relying on, user behavior you're assuming, things that need to stay stable but could change.

### Process Self-Audit

**What must be true:** process self-sabotage patterns — decisions reasonable individually but compounding into failure — are identified and resolved.

**Skip rule:** scope is bounded to a single deliverable with no incremental-addition risk.

Common patterns (not exhaustive): small scope additions ("just one more thing"), edge cases deferred ("we'll handle that later"), "temporary" solutions that become permanent, process shortcuts that erode quality.

For each pattern, resolve disposition: Process Guidance, verifiable Invariant, accept as low risk, or note already covered. The active interview mode defines how patterns are presented and resolved.

## Interview Style

Resolve from `--interview` argument; default `thorough`. Load the mode file:
- `thorough` (default): `references/interview-modes/thorough.md`
- `minimal`: `references/interview-modes/minimal.md`
- `autonomous`: `references/interview-modes/autonomous.md`

Follow the loaded mode's rules for question format, flow, checkpoints, finding-sharing, and convergence for the rest of the run.

**Style switches only on explicit user request.** The flag sets starting posture; the mode stays until the user explicitly asks to switch (e.g., "be more concise", "switch to autonomous", "ask everything"). Don't infer mode shifts from tone or terseness alone — terse answers within a mode are valid mode-internal signals, not switches. After a switch, follow the new mode from that point and log it to the discovery file.

**Auto-switch variant.** When the user signals "enough" / "ship it" / "good enough" / "stop asking", a one-way switch to `autonomous` fires with auto-decide semantics on remaining `[ ]` items — see Convergence § Termination & escalation rules — Mode-switch escalation.

## Discovery & Question Disciplines

### Discovery log

Write to `/tmp/define-discovery-{timestamp}.md` immediately after each discovery — same `{timestamp}` as the manifest. The log is source of truth: another agent reading only the log could resume the interview.

Seed with a Context Assessment before probing — what's already understood and what's missing:

```
## Context Assessment
ALREADY UNDERSTOOD:
- [x] RESOLVED (from context): [item] — [source]
GAPS IDENTIFIED:
- [ ] PENDING: [what's missing and why it matters]
```

The interview begins at the gaps. Before marking a coverage goal as met from context, verify with concrete evidence — vague confidence doesn't count.

Every actionable item gets logged with status:
- `- [ ]` PENDING — needs resolution
- `- [x]` RESOLVED — encoded as INV/AC/PG/ASM, confirmed, or answered
- `- [~]` SKIPPED — explicitly scoped out with reasoning

**Read full log before synthesis.** Unresolved `- [ ]` items are addressed first.

### When to ask

**Search before asking.** Don't ask the user about facts you could discover through exploration. Only ask when multiple plausible candidates exist, searches yield nothing, or the ambiguity is about intent not fact.

**Ask early on preferences.** Trade-offs, priorities, and scope decisions cannot be discovered. Ask directly with concrete options and a recommended default.

**Probe approach constraints.** Beyond WHAT to build, ask HOW: tools to use or avoid, methods required or forbidden, automation vs manual. These become process invariants.

**Probe input artifacts.** When input references external documents (URLs, file paths, named documents), determine whether they should be verification sources. If yes, encode as Global Invariant.

**Resolve all Resolvable task file structures.** After reading task files, extract every Resolvable table and checklist. Items already resolved in conversation context are logged as `- [x]` RESOLVED with source — not re-probed. Remaining items are `- [ ]` PENDING. Resolve each per interview mode, or skip with logged justification. Don't defer to synthesis.

### How to ask

**Decisions lock through structured options.** Questions that lock manifest content present concrete options. The messaging file defines the tool and format; the interview mode defines when and how.

**Batch related questions.** Group questions into a single turn covering one coherent topic; don't drip-feed.

**Confirm before encoding.** Exploration-discovered constraints require confirmation per interview mode before becoming invariants. Exception: task-file quality gates and Defaults are auto-included per Domain Guidance.

**Encode explicit constraints.** User-stated preferences, requirements, and constraints must map to an INV or AC.

## Encoding Disciplines

**Insights become criteria.** Every discovery must be encoded — as INV-G*, AC-*, PG-*, R-*, T-*, or ASM-* — or explicitly scoped out with logged reasoning. Unencoded insights are aspirational, not enforced. (See ID Scheme for the full encoding catalog.)

**Auto-decided items.** When interview style causes an item to be auto-decided (agent picks recommended option instead of asking), encode it normally as INV/AC/PG with an "(auto)" annotation, AND list it in Known Assumptions with the reasoning for the chosen option.

**Automate verification.** When a criterion seems to require manual verification, push back: suggest how it could be automated, or ask the user for ideas. Manual only as last resort or when the user explicitly requests it.

**Verification phases.** Each criterion's verify block has an optional `phase` field — an unquoted integer, default 1 (e.g., `phase: 2`, not `phase: "2"`). **Group by iteration speed — faster feedback loops run first.** Fast checks (agent reviewers, bash) stay in default phase. Slow checks (e2e tests, deploy-dependent) go in later phases. Manual goes last. Omit `phase` for phase 1; non-contiguous phases are valid.

## Convergence

The interview mode defines probing aggressiveness. Convergence requires:
- All applicable Coverage Goal convergence tests pass (Process Self-Audit may be skipped per its own rule)
- No unresolved `- [ ]` items in the discovery log
- Quality gates from task files encoded as INV-G* (or omitted with logged reasoning)
- Defaults encoded as PG-*

Low-impact unknowns become Known Assumptions.

### Termination & escalation rules

Two distinct kinds of trigger:

#### Stop conditions

These end /define:

1. Verifier returns COMPLETE and the user approves the summary.
2. User explicitly invokes `/do`. Behavior depends on where /define is in the run:
   - **Before synthesis is complete** (interview still has unresolved items, or manifest not yet written): switch to `autonomous` interview mode, finish synthesis and the Verification Loop with auto-decisions (each remaining `[ ]` item gets the recommended default, encoded with `(auto)` annotation and logged in Known Assumptions), write the manifest, then hand off to /do without waiting for summary approval.
   - **At the summary stage** (manifest already written, awaiting approval): do not redo synthesis. Print `Manifest complete: ...` per Complete and hand off to /do immediately.

#### Mode-switch escalation

/define continues — only the interview mode changes:

- User signals "enough" (or equivalent: "ship it", "good enough", "stop asking"). Effect: switch interview mode to `autonomous` from this point. Auto-decide remaining `[ ]` items per autonomous mode rules (recommended default chosen, encoded with `(auto)` annotation, logged in Known Assumptions). Continue through synthesis and the Verification Loop; expect to terminate via Stop condition 1.

## Approach Section (Complex Tasks)

After defining deliverables, probe for **initial** implementation direction when the inclusion rule below applies.

**Why "initial":** Approach provides starting direction, not a rigid plan. Plans break on reality — unexpected constraints, better patterns, surprising dependencies. The goal is enough direction to start confidently, with trade-offs documented so implementation can adjust autonomously when reality diverges.

**Architecture** — generate concrete options based on existing patterns. "Given the intent, here are approaches: [A], [B], [C]. Which fits best?" Architecture is direction (structure, patterns, flow), not script. When a choice affects multiple deliverables, surface which deliverables depend on it and what would need to change if the choice proves wrong during implementation.

**Execution Order** — propose order based on dependencies. "Suggested: D1 → D2 → D3. Rationale: [X]. Adjust?" Include why (dependencies, risk reduction).

**Risk Areas** — pre-mortem outputs. "What could cause this to fail? Candidates: [R1], [R2], [R3]." Each risk has detection criteria. Focus on likely/high-impact, not exhaustive.

**Trade-offs** — decision criteria for competing concerns. "When facing [tension], priority? [A] vs [B]?" Format: `[T-N] A vs B → Prefer A because X`. Enables autonomous adjustment during /do.

**Inclusion rule (the one source of truth).** Include the Approach Section when ANY of: the task is multi-deliverable, the domain is unfamiliar, there's an architectural decision to make, or the implementation is high-risk. Skip only when none apply. The interview surfaces which triggers are present.

**Architecture vs Process Guidance.** Architecture = structural decisions (components, patterns, structure). Process Guidance = methodology constraints (tools, manual vs automated). "Add executive summary covering X, Y, Z" is Architecture. "No bullet points in summary sections" is Process Guidance.

## What the Manifest Captures

Three categories, each covering output or process:

- **Global Invariants** — "don't do X" (negative constraints, ongoing, verifiable). Output: "No breaking changes to public API." Process: "Don't edit files in /legacy."
- **Process Guidance** — non-verifiable constraints on HOW to work (approach requirements, methodology, tool preferences not checkable from output alone, e.g., "manual optimization only"). Guides the implementer; not gates.
- **Deliverables + ACs** — "must have done X" (positive milestones). Three types:
  - *Functional:* "Section X explains concept Y"
  - *Non-Functional:* "Document under 2000 words", "All sections follow template structure"
  - *Process:* "Deliverable contains section 'Executive Summary'"

## The Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]
- **Mode:** efficient | balanced | thorough *(default: thorough — controls verification intensity during /do; set via `--mode`)*
- **Interview:** minimal | autonomous | thorough *(default: thorough — recorded so --amend can inherit the original interview style)*
- **Medium:** local *(default: local)*

## 2. Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Provides enough to start confidently; expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW - starting direction, not step-by-step]

- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: [why this order — dependencies, risk reduction]

- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
  - [R-2] [What could go wrong] | Detect: [how you'd know]

- **Trade-offs:**
  - [T-1] [Priority A] vs [Priority B] → Prefer [A] because [reason]
  - [T-2] [Priority X] vs [Priority Y] → Prefer [Y] because [reason]

## 3. Global Invariants (The Constitution)
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Description: ... | Verify: [Method]
  ```yaml
  verify:
    method: bash | codebase | subagent | research | manual | deferred-auto
    phase: 1                       # optional integer, default 1; higher phases run after lower pass
    command: "[if bash]"
    agent: "[if subagent]"
    model: "[if subagent, default inherit]"
    prompt: "[if subagent or research]"
  ```

*`deferred-auto`: user-triggered; runs only via `/verify --deferred`. See `references/MULTI_REPO.md` §e for cross-repo semantics.*

*Auto-decided items (Encoding Disciplines § Auto-decided items) carry an `(auto)` annotation immediately after the ID, e.g. `- [INV-G2] (auto) Description: ...`. The same convention applies to AC-* and PG-* entries that were auto-decided. Each auto-decided item also appears in Known Assumptions with its reasoning.*

## 4. Process Guidance (Non-Verifiable)
*Constraints on HOW to work. Not gates—guidance for the implementer.*

- [PG-1] Description: ...

## 5. Known Assumptions
*Low-impact items where a reasonable default was chosen without explicit user confirmation. If any assumption is wrong, amend the manifest.*

- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables (The Work)
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: ... | Verify: ...
  ```yaml
  verify:
    method: bash | codebase | subagent | research | manual | deferred-auto
    phase: 1                       # optional integer, default 1
    command: "[if bash]"
    agent: "[if subagent]"
    model: "[if subagent, default inherit]"
    prompt: "[if subagent or research]"
  ```
  *AC verify blocks accept the same fields as INV-G verify blocks above.*

### Deliverable 2: [Name]
...
````

## ID Scheme

| Type | Format | Example | Used By |
|------|--------|---------|---------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 | /verify (verified) |
| Process Guidance | PG-{N} | PG-1, PG-2 | /do (followed) |
| Risk Area | R-{N} | R-1, R-2 | /do (watched) |
| Trade-off | T-{N} | T-1, T-2 | /do (consulted) |
| Known Assumption | ASM-{N} | ASM-1, ASM-2 | /verify (audited) |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1, AC-2.3 | /verify (verified) |

## Verification Loop

After writing the manifest, read the manifest's `Mode` field and load the execution mode file from `../do/references/execution-modes/` for the resolved mode (default: `thorough`). Load once at loop entry; the same mode applies to every cycle in this loop. Follow that mode's "Manifest Verification (/define)" section for whether to run the manifest-verifier and how many cycles.

When invoking the verifier, pass only the file paths (with `Manifest:` / `Log:` labels for disambiguation). No summary of contents, no framing, no commentary on the manifest itself. The verifier sees what you may have missed; let it assess independently.

```
Invoke the manifest-dev:manifest-verifier agent with: "Manifest: /tmp/manifest-{timestamp}.md | Log: /tmp/define-discovery-{timestamp}.md"
```

The verifier returns **CONTINUE** or **COMPLETE**:

- **CONTINUE** — interview mode defines whether to present findings to the user or auto-resolve. **When presenting verifier findings to the user, present verbatim — do not paraphrase, filter, or editorialize.** Log answers to discovery file, update manifest, invoke verifier again.
- **COMPLETE** — proceed to summary for approval.

Repeat until a Stop condition fires (see Convergence § Termination & escalation rules — Stop conditions). The cycle cap is defined per execution mode in `../do/references/execution-modes/`; this loop respects that cap.

## Summary for Approval

Digest the manifest into a scannable summary the user can approve at a glance. The summary answers "do you understand and agree with this plan?" — not "review every acceptance criterion." The manifest has the details; the summary is the human-readable version.

**Voice:** plain language. No manifest codes (D1, AC-1.1, INV-G3), no YAML blocks, no structured-document vocabulary.

**Default structure** (adapt if the task calls for something different):
- **The plan** — one-line headline of what's being done and why.
- **What I'll build** — bullet list of work items. Group related items naturally; don't enumerate every sub-task.
- **Guardrails** — bullet list of invariants as plain rules. Example: "Existing behavior untouched when --auto is absent. Explicit flags always override --auto defaults."
- **How I'll verify** — brief description of verification approach. Example: "criteria-checker cross-references docs for contradictions, prompt-reviewer checks prompt quality."

Include an ASCII architecture diagram when the task has multiple components with inter-component flow. Skip for single-deliverable tasks.

**The test:** if it reads like a compressed manifest (codes, YAML, structured labels dressed up as prose; enumerated criteria; counts hiding detail; abstractions hiding content), rewrite it. If it reads like something you'd say to a colleague, it's right.

**After presenting the summary**, wait for the user's response:
- **Approval** ("looks good", "approved") → proceed to Complete (Stop condition 1).
- **Feedback** ("also add X", "change Y", "use Z skill in process") → revise manifest, re-present summary. Do not implement.
- **Explicit /do invocation** → Stop condition 2 fires; /define is done; /do takes over.
- **Decline** ("scrap this", "never mind", "cancel") → exit /define silently. Do not write the manifest. The user can re-invoke /define if they want to retry.

## Medium Routing

Load the messaging file for the resolved medium:
- `local` (default): `references/messaging/LOCAL.md`

The messaging file defines HOW to interact (tool, format, polling). The interview mode file defines WHAT to interact about (questions, flow, convergence).

The medium is encoded in the manifest's Intent section as `Medium: <value>` so downstream skills know the communication channel.

## Complete

/define ends here. Output the manifest path and stop. Substitute the placeholders before printing:
- `{timestamp}` → the value used for the manifest filename.
- `<dir>` → the current project directory in the slug form used by `~/.claude/projects/` (path separators replaced with `-`, e.g., `-home-user-manifest-dev` for `/home/user/manifest-dev`).
- `${CLAUDE_SESSION_ID}` → the value of the `CLAUDE_SESSION_ID` environment variable.
- `[log-file-path if iterating]` → if this run iterated on a previous manifest that had an execution log, substitute the actual log path; otherwise omit the bracketed clause entirely (including the trailing space).

```text
Manifest complete: /tmp/manifest-{timestamp}.md
Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl

To execute: /do /tmp/manifest-{timestamp}.md [log-file-path if iterating]
```
