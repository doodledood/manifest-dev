---
name: define
description: 'Manifest builder. Plan work, scope tasks, spec out requirements, break down complex tasks before implementation. Converts needs into Deliverables + Invariants with verification criteria. Use when planning features, debugging complex issues, scoping refactors, or whenever a task needs structured thinking before coding.'
---

# /define - Manifest Builder

## Prerequisites

If thinking disciplines are not already active in this session, invoke the manifest-dev:thinking-disciplines skill. Do not begin the interview until disciplines are active. Apply throughout — every question, assessment, and synthesis.

## Goal

Build a **comprehensive Manifest** that captures:
- **What we build** (Deliverables with Acceptance Criteria)
- **How we'll get there** (Approach - initial direction, expect adjustment)
- **Rules we must follow** (Global Invariants)

**Why thoroughness matters**: Every criterion discovered NOW is one fewer rejection during implementation/review. The goal is a deliverable that passes review on first submission—no "oh, I also needed X" after the work is done.

Comprehensive means surfacing **latent criteria**—requirements the user doesn't know they have until probed. Users know their surface-level needs; your job is to discover the constraints and edge cases they haven't thought about.

Aim for high coverage. Amendments handle what emerges during implementation.

Output: `/tmp/manifest-{timestamp}.md`

## Input

`$ARGUMENTS` = task description, optionally with context/research, `--interview <level>`, `--medium <type>`, `--amend <manifest-path>`

Parse `--interview` from arguments (can appear anywhere). Valid values: `minimal`, `autonomous`, `thorough`. Default: `thorough`. Invalid value → error and halt: "Invalid interview style '<value>'. Valid styles: minimal | autonomous | thorough"

Parse `--medium` from arguments (can appear anywhere). Currently only `local` is supported (default). Other mediums may be added in the future. If a non-local value is provided, error and halt: "Medium '<value>' not yet supported. Currently supported: local". See Medium Routing section below.

Parse `--amend <manifest-path>` from arguments (can appear anywhere). `--from-do` flag (optional, used with `--amend`) — see `references/AMENDMENT_MODE.md` for behavior.

If no arguments provided, ask: "What would you like to build or change?"

## Session-Default Amendment

After parsing arguments (above) and before any other workflow step (Domain Guidance, interview, etc.), check whether this session already produced a manifest. The goal is **one manifest per related change set** — follow-up bug fixes, feature extensions, and polish on the same surface should accumulate criteria into the existing manifest rather than start over and silently lose prior INVs/ACs/PGs.

**Skip this section entirely when the user has already pointed at a specific manifest.** Explicit signals always win over session-default detection:
- `--amend <path>` was passed (preserves `/do --from-do`, which always passes `--amend`, and any explicit user `/define --amend <path>` invocation).
- Input arguments contain a `/tmp/manifest-*.md` path or otherwise plainly point at a specific manifest file — proceed past this section and let the workflow reach **Existing Manifest Feedback** below, which already treats the referenced manifest as source of truth.

**Otherwise**, determine whether a relevant prior manifest exists. Check signals in this order; the first hit wins:

1. **In-session completion signal.** A line of the form `Manifest complete: /tmp/manifest-{timestamp}.md` (defined in the `## Complete` section below; the only cross-invocation signal that survives reliably across `/define` runs). If multiple such lines appear in the conversation context, the **most recent in transcript order wins** (this handles the case where the user manually amended an older manifest mid-session — transcript order, not the path's timestamp, is authoritative).

2. **Conversation reference.** A `/tmp/manifest-*.md` or `.manifest/*.md` path mentioned in the current conversation (user message, prior tool result, summary). The path implies the user already has a manifest in mind for the current work.

3. **Branch-archived manifest.** If `.manifest/` contains a file modified during the current branch's commit-history time range (i.e., file mtime falls between the branch's first commit time and now, computed via `git log --format=%cI <base>..HEAD` — `<base>` resolved per the Base inference order in Branch-Diff Seeding below), that file is a candidate. Among multiple candidates, the most recently modified wins. When two candidates were modified within ~1 hour of each other (genuinely ambiguous), ask the user once which one is authoritative. When `.manifest/` is empty or no file's mtime intersects the branch's time range, signal #3 produces no candidate (fall through to a fresh manifest).

If no signal hits, you'll land in the No Prior Manifest Found branch — proceed fresh; the user can recover with explicit `/define --amend <path>` if needed.

**Detection is judgment-based, not mechanical.** When a signal is ambiguous (e.g., transcript references an unrelated manifest from a different concern, or branch maps to multiple plausible archives), ask the user once: "I see manifest X in scope — amend it, pick a different one, or start fresh?" Don't silently choose. The Cumulative Manifest Rule (`references/AMENDMENT_MODE.md`) means a wrong choice here either pollutes an unrelated manifest or fragments the PR's source of truth — both are worse than asking once.

### No Prior Manifest Found

Behavior is unchanged from a normal fresh `/define`. No announcement is emitted. Proceed with the remaining workflow as written.

### Prior Manifest Found

Read the prior manifest at the matched path. Compare its **Goal** and **Deliverables** (titles and acceptance criteria) against the new task description.

**Amendment is the default — not a 50/50 judgment call.** Operational test for "truly unrelated": the new task's intent does **not** extend, fix, or polish anything in the prior manifest's Goal + Deliverables — it targets a clearly different problem space. Truly unrelated work in the same session is rare; anything else — continuation, refinement, follow-up, polish, bug fix on something the prior manifest covered — is related and should amend. **When the test is genuinely ambiguous, default to amendment.** The asymmetry is intentional: the announcement gives the user a one-line escape hatch, while a wrong "fresh" decision silently loses prior INVs/ACs/PGs.

#### When Related (default)

Announce the decision to the user, then proceed as if `--amend <prior-path>` had been passed. Follow `references/AMENDMENT_MODE.md` from that point — the new "Session-Default" trigger context documented there describes this path; behavior follows the Standalone amendment flow, respecting the active interview mode (a `/auto` invocation, for example, still runs autonomously — only the trigger differs from explicit `--amend`).

**Post-archival commits surface when signal #3 fires.** When the matched manifest came from signal #3 (branch-archived in `.manifest/`), additionally inspect commits made on the branch *after* the manifest's archival mtime: `git log --format=%H --since="<manifest-mtime>" <base>..HEAD` (`<base>` resolved per the Base inference order in Branch-Diff Seeding below). If any such commits exist, run `git diff <archive-commit-or-mtime>...HEAD` and incorporate the post-archival changeset as discovery context for the amendment — same as Branch-Diff Seeding does for fresh /define on a non-empty branch. This preserves the Cumulative Manifest Rule (`references/AMENDMENT_MODE.md`): post-archival work made outside the manifest workflow is surfaced into the amendment, not silently lost.

Announcement format (substantively):

> Detected prior manifest in session: `/tmp/manifest-{ts}.md` (`<title from manifest's H1>`). Defaulting to amendment mode — interrupt me if this is actually unrelated work and I'll start fresh.

Emit the announcement regardless of interview mode (including `--interview autonomous` and `/auto` invocations) — this preserves the audit trail in the transcript. The announcement is one line and non-blocking; the interview proceeds without waiting for confirmation. The "interrupt me" phrasing matches that behavior — the user can redirect mid-interview if needed.

#### When Truly Unrelated

Proceed fresh with a one-line note explaining the decision so the user can correct if needed. Example:

> Found prior manifest `<path>` (`<title>`), but new task targets `<different problem space>`. Starting fresh — interrupt me to amend instead if I read this wrong.

#### When Prior Manifest File Cannot Be Read

If the matched path no longer exists or fails to read, fall back to a fresh manifest with a one-line note: "Prior manifest `<path>` is no longer available; starting fresh."

## Branch-Diff Seeding (Fresh /define on a Non-Empty Branch)

**Trigger:** Fresh `/define` (no `--amend`, no Session-Default Amendment, no referenced manifest) AND the current branch has commits ahead of its base.

**Why:** The manifest is the canonical source of truth for the PR/branch lifetime (per `references/AMENDMENT_MODE.md` Cumulative Manifest Rule). When work already exists on the branch — commits made before /define ran, or work-in-progress accumulated outside the manifest workflow — that work belongs in the manifest. Ignoring it produces a manifest that doesn't reflect the actual PR.

**Base inference order:**
1. Upstream tracking branch (`git rev-parse --abbrev-ref @{upstream}`).
2. `origin/main` if it exists.
3. `origin/master` if it exists.
4. Ask the user once for the base ref. Halt seeding if they decline.

**What to do:** Run `git diff <base>...HEAD` and `git log --oneline <base>..HEAD`. Read the diff and commit messages. Incorporate the existing changeset into the new manifest's Intent (mention what's already done) and starting Deliverables (the work-in-progress becomes prior context, with new ACs added on top for completion + the new task). The interview confirms or adjusts what was inferred from the diff.

**Skip cleanly when:** No commits ahead of base (fresh branch), or `--amend` was passed (existing manifest already covers the prior state), or Session-Default Amendment fired (in-session manifest is being amended).

## Domain Guidance

Domain-specific guidance available in:

| Domain | Indicators | Guidance File |
|--------|------------|---------------|
| **Coding** | Any code change (base for Feature, Bug, Refactor) | `tasks/CODING.md` |
| **Feature** | New functionality, APIs, enhancements | `tasks/FEATURE.md` |
| **Bug** | Defects, errors, regressions, "not working", "broken" | `tasks/BUG.md` |
| **Refactor** | Restructuring, reorganization, "clean up", pattern changes | `tasks/REFACTOR.md` |
| **Prompting** | LLM prompts, skills, agents, system instructions | `tasks/PROMPTING.md` |
| **Writing** | Prose, articles, emails, marketing copy, social media, creative writing (base for Blog, Document) | `tasks/WRITING.md` |
| **Document** | Specs, proposals, reports, formal docs (base: Writing) | `tasks/DOCUMENT.md` |
| **Research** | Investigations, analyses, comparisons | `tasks/research/RESEARCH.md` |
| **Blog** | Blog posts, articles, tutorials (base: Writing) | `tasks/BLOG.md` |

**Composition**: Code-change tasks combine CODING.md (base quality gates) with domain-specific guidance. Text-authoring tasks combine WRITING.md (base prose quality) with content-type guidance—a "blog post" benefits from both WRITING.md and BLOG.md, a "technical proposal" from both WRITING.md and DOCUMENT.md. Research tasks compose RESEARCH.md (base research methodology) with source-type files—when web research is identified as relevant, load `tasks/research/sources/SOURCE_WEB.md` alongside `tasks/research/RESEARCH.md`. RESEARCH.md's Data Sources table lists available source files and probes which sources apply. Domains aren't mutually exclusive—a "bug fix that requires refactoring" benefits from both BUG.md and REFACTOR.md. Related domains compound coverage.

**Exception**: PROMPTING tasks do NOT compose with CODING.md unless the task also changes executable code. PROMPTING.md has its own quality gates (prompt-reviewer, clarity, structure, etc.). When a task changes both prompts AND code, apply both PROMPTING.md and CODING.md gates, scoping each to the relevant files.

**Task file structures are presumed relevant.** Task files contain quality gates, reviewer agents, risks, scenarios, and trade-offs. These are angles you won't think to check on your own — they exist precisely because they're easy to miss. Quality gates are auto-included; Resolvable structures (risks, scenarios, trade-offs) must be **resolved**: either resolved per the interview mode's decision authority, or explicitly skipped with logged reasoning (e.g., "CODING.md concurrency risk skipped: single-threaded CLI tool"). Silent drops are the failure mode — not over-asking.

**Task file content types.** Five categories, each handled differently:
- **Quality gates** (structured items under `## Quality Gates` — tables, bullet lists, or any format with thresholds/criteria) — auto-include as INV-G*, omit clearly inapplicable with logged reasoning. User reviews manifest.
- **Resolvable** (tables/checklists: risks, scenarios, trade-offs) — resolve via interview, encode as INV/AC or explicitly skip.
- **Compressed awareness** (bold-labeled one-line domain summaries, not tables/checklists) — informs your probing; no resolution needed.
- **Process guidance hints** (counter-instinctive practices) — practices LLMs would get wrong without explicit guidance. Two modes: **candidates** (labeled as PG candidates, presented as a batch after scenarios, resolved per interview mode) and **defaults** (`## Defaults` section, included in manifest without probing, user reviews manifest and removes if not applicable). Both become PG-* in the manifest.
- **Reference files** (`references/*.md`) — detailed lookup data for `/verify` agents. Do not load during the interview.

**Encode quality gates and Defaults immediately after reading task files — before the interview.** Log each as `- [x]` RESOLVED.

Probing beyond task files is adaptive — driven by the specific task, user responses, and what you discover. Task files don't cap what to ask; they set a floor.

## Existing Manifest Feedback

If input references a previous manifest: **treat it as source of truth**. It contains validated decisions — default to building on it, preserving what's settled. Confirm approach with user if unclear.

## Amendment Mode

When `--amend <manifest-path>` is present: read `references/AMENDMENT_MODE.md` for amendment rules.

## Multi-Repo Scope

When task spans multiple repositories, capture during intent (starting points):

- **Which repos** and their roles
- **Cross-repo constraints** (dependencies, coordination requirements)
- **Per-repo differences** (different rules, conventions, verification needs)

Scope deliverables and verification to repo context. Cross-repo invariants get explicit verification checking both sides.

## Principles

1. **Verifiable** - Every Invariant and AC has an automated verification method. Constraints that can't be verified from output go in Process Guidance. Manual only as last resort.

2. **Validated** - Generate concrete candidates; learn from user reactions. The interview mode file defines behavioral specifics.

3. **Domain-grounded** - Understand the domain before probing. Latent criteria emerge from domain understanding — you can't surface what you don't know.

4. **Complete** - Surface hidden requirements through five coverage goals. Understanding from any source counts equally.

5. **Directed** - For complex tasks, establish initial implementation direction (Approach). Architecture defines starting direction, not step-by-step script.

6. **Efficient** - Each question must: materially change the manifest, lock an assumption, or choose between meaningful trade-offs. If it fails all three, don't ask. One missed criterion costs more than one extra question — err toward asking, never ask trivia.

## Coverage Goals

Five goals that must be met before convergence. Each defines WHAT must be true and a convergence test. Items resolved from any source (conversation, prior research, task files, exploration) count equally. The interview probes gaps, not territory already covered. The active interview mode defines how gaps are probed and decisions are made.

| Goal | Convergence test |
|------|-----------------|
| Domain Understanding | Can you generate project-specific (not generic) failure scenarios? |
| Reference Class | Can you name the task type and its common failure modes? |
| Failure Modes | All scenarios have dispositions (encoded, scoped out, or mitigated)? |
| Positive Dependencies | Load-bearing assumptions surfaced and each has a disposition? |
| Process Self-Audit | Scope-creep risks identified and resolved? (skip if straightforward) |

### Domain Understanding

**What must be true:** You understand the affected area well enough to generate project-specific failure scenarios — not generic ones. You know existing patterns, structure, constraints, and prior decisions relevant to the task.

Understanding comes from any source — conversation context, prior research, code exploration, documentation, user-provided arguments, task files. Don't re-discover what's already known. When understanding is insufficient, fill gaps through whatever means fits the domain — explore code, search docs, ask the user what exploration can't reveal. Scope to what's relevant, not the entire domain.

**What to assess** (starting points — adapt to the task):
- **Existing patterns** — how similar things are currently done
- **Structure** — components, dependencies, boundaries in the affected area
- **Constraints** — implicit conventions, assumed invariants, existing contracts
- **Prior decisions** — why things are the way they are, when discoverable

**Convergence test:** Can you generate failure scenarios that reference specific components, patterns, or conventions in this context? If yes, sufficient. If only generic failures, gaps remain.

### Reference Class Awareness

**What must be true:** You know what type of task this is, what typically fails in that class, and those base-rate failures inform your failure mode coverage.

Ground the reference class in domain understanding — "refactor of a tightly-coupled module with no tests" is useful; "refactor" is too generic. The reference class should be specific enough that its failure patterns are actionable. Task file warnings are a source.

**Convergence test:** Can you name the reference class and its most common failure modes? Often satisfiable in a single assessment step.

### Failure Mode Coverage

**What must be true:** Failure modes have been anticipated with concrete scenarios, and each has a disposition — encoded as criterion, explicitly scoped out, or mitigated by approach. No dangling scenarios. Mental model alignment checked — your understanding of "done" matches the user's expectation.

**Failure dimensions** — starting lenses for generating scenarios when gaps exist. Use these and any others relevant to the task:

| Dimension | What to imagine |
|-----------|-----------------|
| **Technical** | What breaks at the code/system level? |
| **Integration** | What breaks at boundaries? |
| **Stakeholder** | What causes rejection even if technically correct? |
| **Timing** | What fails later that works now? |
| **Edge cases** | What inputs/conditions weren't considered? |
| **Dependencies** | What external factors cause failure? |

Task files add domain-specific failure scenarios. Scenarios grounded in domain understanding are higher signal than generic templates.

**Scenario disposition** — every scenario resolves to one of:
1. **Encoded as criterion** — becomes INV-G*, AC-*, or Risk Area with detection
2. **Explicitly out of scope** — user confirmed it's acceptable risk
3. **Mitigated by approach** — architecture choice eliminates the failure mode

The active interview mode defines how scenarios are presented and dispositions resolved.

**Convergence test:** Relevant failure dimensions considered, all scenarios have dispositions, and user confirms no major failure modes were missed.

### Positive Dependency Coverage

**What must be true:** Load-bearing assumptions — what must go right for the task to succeed — are surfaced and each is resolved: verified, encoded as invariant, or logged as Known Assumption.

Where failure mode coverage asks "what broke?", positive dependencies ask "what held?" This reveals assumptions you haven't examined.

**What to assess** (starting points — the task may surface others):
- What existing infrastructure/tooling are you relying on?
- What user behavior are you assuming?
- What needs to stay stable that could change?

The active interview mode defines how dependencies are presented and resolved.

**Convergence test:** Load-bearing assumptions surfaced and each has a disposition.

### Process Self-Audit

**What must be true:** Process self-sabotage patterns — decisions that look reasonable individually but compound into failure — are identified and resolved. **Skip for simple tasks.**

Common patterns (not exhaustive — the task may have its own):
- Small scope additions ("just one more thing")
- Edge cases deferred ("we'll handle that later")
- "Temporary" solutions that become permanent
- Process shortcuts that erode quality

For each pattern, resolve its disposition — add as Process Guidance, encode as verifiable Invariant, accept as low risk, or note it's already covered. The active interview mode defines how patterns are presented and resolved.

**Convergence test:** Tasks with scope-creep risk have process risks identified and resolved. Skip when the task is straightforward enough that process sabotage is unlikely.

## Interview Style

Resolve interview style from `--interview` argument → default `thorough`.

Load the interview mode file for behavioral specifics:
- `thorough` (default): read `references/interview-modes/thorough.md`
- `minimal`: read `references/interview-modes/minimal.md`
- `autonomous`: read `references/interview-modes/autonomous.md`

Follow the loaded interview mode's rules for question format, flow structure, checkpoint behavior, finding-sharing, and convergence for the remainder of this /define run.

**Auto-decided items**: When interview style causes an item to be auto-decided (agent picks recommended option instead of asking), encode it normally as INV/AC/PG with an "(auto)" annotation, AND list it in the Known Assumptions section with the reasoning for the chosen option.

**Style is dynamic**: The `--interview` flag sets the starting posture, not a rigid lock. Shift when the user's behavior signals a different mode. After a style shift, follow the new mode's rules from that point forward. Log any style shift to the discovery file.

## Constraints

**Decisions lock through structured options** — Questions that lock manifest content present 2-4 concrete options, one marked "(Recommended)". The messaging file defines the tool; the interview mode defines when and how.

**Resolve all Resolvable task file structures** — After reading task files, extract every Resolvable table and checklist (risk lists, scenario prompts, trade-offs) and log each. Items already resolved in conversation context are logged as `- [x]` RESOLVED (from context) with source — not re-probed. Remaining items are logged as `- [ ]` PENDING. Resolve each per the interview mode's decision authority, or skip with logged justification. Don't defer to synthesis — these are structural decisions that compound when missed.

**Discoverable unknowns — search first** — Don't ask the user about facts you could discover through exploration. Only ask when: multiple plausible candidates exist, searches yield nothing, or the ambiguity is about intent not fact.

**Preference unknowns — ask early** — Trade-offs, priorities, scope decisions cannot be discovered. Ask directly with concrete options and a recommended default.

**Confirm before encoding** — Exploration-discovered constraints require confirmation per the interview mode before becoming invariants. This does not apply to task-file quality gates and Defaults (auto-included per Domain Guidance rules).

**Encode explicit constraints** — User-stated preferences, requirements, and constraints must map to an INV or AC. Don't let them get lost in the interview log.

**Probe for approach constraints** — Beyond WHAT to build, ask HOW it should be done. Tools to use or avoid? Methods required or forbidden? Automation vs manual? These become process invariants.

**Probe input artifacts** — When input references external documents, determine whether they should be verification sources. If yes, encode as Global Invariant.

**Discovery log** — Write to `/tmp/define-discovery-{timestamp}.md` immediately after each discovery. The log is the source of truth — another agent reading only the log could resume the interview.

Seed with a Context Assessment before probing — what's already understood and what's missing:

```
## Context Assessment
ALREADY UNDERSTOOD:
- [x] RESOLVED (from context): [item] — [source]
GAPS IDENTIFIED:
- [ ] PENDING: [what's missing and why it matters]
```

The interview begins at the gaps. Before marking a coverage goal as met from context, verify with concrete evidence — vague confidence doesn't count.

Every actionable item gets logged with resolution status:
- `- [ ]` PENDING — needs resolution
- `- [x]` RESOLVED — encoded as INV/AC/PG/ASM, confirmed, or answered
- `- [~]` SKIPPED — explicitly scoped out with reasoning

**Read full log before synthesis.** Unresolved `- [ ]` items must be addressed first. This is a memento-pattern discipline — the model will skip it without explicit instruction.

**Batch related questions** — Group related questions into a single turn. Each batch covers a coherent topic area.

**Convergence** — The interview mode defines probing aggressiveness. Convergence requires all five coverage goal convergence tests passing, plus:
- No unresolved `- [ ]` items in the log
- Quality gates from task files encoded as INV-G* (or omitted with logged reasoning)
- Defaults encoded as PG-*

Low-impact unknowns become Known Assumptions. User can signal "enough" to override.

**Insights become criteria** — Every discovery must be encoded as INV-G*, AC-*, or explicitly scoped out. Unencoded insights are aspirational, not enforced.

**Automate verification** — When a criterion seems to require manual verification, push back: suggest how it could be automated, or ask the user for ideas. Manual only as last resort or when user explicitly requests it.

**Verification phases** — Each criterion's verify block has an optional `phase:` field (numeric, default 1). The principle: **group by iteration speed — faster feedback loops run first.** Fast checks (agent reviewers, bash) stay in default phase. Slow checks (e2e tests, deploy-dependent) go in later phases. Manual verification goes last. Omit `phase:` for phase 1. Non-contiguous phases are valid.

## Approach Section (Complex Tasks)

After defining deliverables, probe for **initial** implementation direction. Skip for simple tasks with obvious approach.

**Why "initial"**: Approach provides starting direction, not a rigid plan. Plans break when hitting reality—unexpected constraints, better patterns discovered, dependencies that don't work as expected. The goal is enough direction to start confidently, with trade-offs documented so implementation can adjust autonomously when reality diverges.

**Architecture** - Generate concrete options based on existing patterns. "Given the intent, here are approaches: [A], [B], [C]. Which fits best?" Architecture is direction (structure, patterns, flow), not step-by-step script. When a choice affects multiple deliverables, surface which deliverables depend on it and what would need to change if the choice proves wrong during implementation.

**Execution Order** - Propose order based on dependencies. "Suggested order: D1 → D2 → D3. Rationale: [X]. Adjust?" Include why (dependencies, risk reduction, etc.).

**Risk Areas** - Pre-mortem outputs. "What could cause this to fail? Candidates: [R1], [R2], [R3]." Each risk has detection criteria. Not exhaustive—focus on likely/high-impact.

**Trade-offs** - Decision criteria for competing concerns. "When facing [tension], priority? [A] vs [B]?" Format: `[T-N] A vs B → Prefer A because X`. Enables autonomous adjustment during /do.

**When to include Approach**: Multi-deliverable tasks, unfamiliar domains, architectural decisions, high-risk implementations. The interview naturally reveals if it's needed.

**Architecture vs Process Guidance**: Architecture = structural decisions (components, patterns, structure). Process Guidance = methodology constraints (tools, manual vs automated). "Add executive summary section covering X, Y, Z" is Architecture. "No bullet points in summary sections" is Process Guidance.

## Delegation Map

| File | Owns |
|------|------|
| **Interview mode files** (`references/interview-modes/`) | Question format, flow structure, checkpoint behavior, finding-sharing, convergence aggressiveness |
| **Messaging files** (`references/messaging/`) | Interaction tooling (which tool to use, format constraints) |
| **Task files** (`tasks/`) | Domain-specific quality gates, risks, scenarios, trade-offs, defaults |
| **Amendment mode** (`references/AMENDMENT_MODE.md`) | Rules for modifying existing manifests |
| **Execution mode files** (`../do/references/execution-modes/`) | Verification loop behavior (how many cycles, whether to run verifier) |

## What the Manifest Needs

Three categories, each covering **output** or **process**:

- **Global Invariants** - "Don't do X" (negative constraints, ongoing, verifiable). Output: "No breaking changes to public API." Process: "Don't edit files in /legacy."
- **Process Guidance** - Non-verifiable constraints on HOW to work. Approach requirements, methodology, tool preferences that cannot be checked from the output alone (e.g., "manual optimization only" - you can't tell from the output whether it was manually crafted or generated). These guide the implementer but aren't gates.
- **Deliverables + ACs** - "Must have done X" (positive milestones). Three types:
  - *Functional*: "Section X explains concept Y"
  - *Non-Functional*: "Document under 2000 words", "All sections follow template structure"
  - *Process*: "Deliverable contains section 'Executive Summary'"

## The Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]
- **Mode:** efficient | balanced | thorough *(optional, default: thorough — controls verification intensity during /do)*
- **Interview:** minimal | autonomous | thorough *(optional, default: thorough — recorded so --amend can inherit the original interview style)*
- **Medium:** local *(optional, default: local — currently only local is supported)*

## 2. Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Provides enough to start confidently; expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW - starting direction, not step-by-step]

- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: [why this order - dependencies, risk reduction, etc.]

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
    method: bash | codebase | subagent | research | manual
    phase: "[numeric, optional, default 1 — higher phases run after lower phases pass]"
    command: "[if bash]"
    agent: "[if subagent]"
    model: "[if subagent, default inherit]"
    prompt: "[if subagent or research]"
  ```

## 4. Process Guidance (Non-Verifiable)
*Constraints on HOW to work. Not gates—guidance for the implementer.*

- [PG-1] Description: ...

## 5. Known Assumptions
*Low-impact items where a reasonable default was chosen without explicit user confirmation. If any assumption is wrong, amend the manifest.*

- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables (The Work)
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: [Name]
*[If multi-repo: specify repo scope]*

**Acceptance Criteria:**
- [AC-1.1] Description: ... | Verify: ...
  ```yaml
  verify:
    method: bash | codebase | subagent | research | manual
    phase: "[numeric, optional, default 1]"
    [details]
  ```

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

After writing the manifest, check the manifest's `mode:` field and load the execution mode file from `../do/references/execution-modes/` for the resolved mode (default: `thorough`). Follow the mode's "Manifest Verification (/define)" section for whether to run the manifest-verifier and how many cycles.

When running the verifier, pass only the file paths — no summary, framing, or commentary:

```
Invoke the manifest-dev:manifest-verifier agent with: "Manifest: /tmp/manifest-{timestamp}.md | Log: /tmp/define-discovery-{timestamp}.md"
```

The verifier returns **CONTINUE** or **COMPLETE**:

- **CONTINUE**: The active interview mode defines how to handle this — see the mode file for whether to present to the user or auto-resolve. Log answers/resolutions to the discovery file, update the manifest, then invoke the verifier again.
- **COMPLETE**: Proceed to summary for approval.

Repeat until COMPLETE or user signals "enough".

Do not add context, justification, or steering to the verifier invocation. The verifier sees what you may have missed; let it assess independently. When relaying verifier output, do not paraphrase, filter, or editorialize.

## Summary for Approval

Digest the manifest into a scannable summary the user can approve at a glance. The summary answers "do you understand and agree with this plan?" — not "review every acceptance criterion." The manifest has the details; the summary is the human-readable version.

**Voice**: Plain language. No manifest codes (D1, AC-1.1, INV-G3), no YAML blocks, no structured-document vocabulary.

**Default structure** (adapt if the task calls for something different):

- **The plan** — One-line headline of what's being done and why.
- **What I'll build** — Bullet list of work items. Group related items naturally; don't enumerate every sub-task.
- **Guardrails** — Bullet list of invariants as plain rules. Example: "Existing behavior untouched when --auto is absent. Explicit flags always override --auto defaults. Agent halts on truly unresolvable issues — not silent-failure mode."
- **How I'll verify** — Brief description of verification approach. Example: "criteria-checker cross-references docs for contradictions, prompt-reviewer checks prompt quality."

Include an ASCII architecture diagram when the task has multiple components with inter-component flow. Skip for single-deliverable tasks.

**The test**: If the summary reads like a compressed manifest, rewrite it. If it reads like something you'd say to a colleague, it's right.

**Anti-patterns**:
- Manifest cosplay — codes, YAML, structured labels dressed up as prose
- Enumerating every acceptance criterion instead of digesting
- Hiding detail behind counts ("8 automated verifications")
- Abstracting instead of showing ("3 deliverables covering auth")

**After presenting the summary**, wait for the user's response. User responses mean:
- **Approval** (e.g., "looks good", "approved") → proceed to Complete
- **Feedback** (e.g., "also add X", "change Y", "use Z skill in process") → revise the manifest, re-present summary. Do not implement.
- **Explicit /do invocation** → /define is done; /do takes over

## Medium Routing

Load the messaging file for the resolved medium:
- `local` (default): read `references/messaging/LOCAL.md`

The messaging file defines HOW to interact (tool, format, polling). The interview mode file defines WHAT to interact about (questions, flow, convergence).

The medium is encoded in the manifest's Intent section as `Medium: <value>` so downstream skills know the communication channel.

## Complete

/define ends here. Output the manifest path and stop.

```text
Manifest complete: /tmp/manifest-{timestamp}.md

To execute: /do /tmp/manifest-{timestamp}.md [log-file-path if iterating]
```

If this was an iteration on a previous manifest that had an execution log, include the log file path in the suggestion.
