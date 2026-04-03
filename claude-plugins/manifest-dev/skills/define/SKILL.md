---
name: define
description: 'Manifest builder. Plan work, scope tasks, spec out requirements, break down complex tasks before implementation. Converts needs into Deliverables + Invariants with verification criteria. Use when planning features, debugging complex issues, scoping refactors, or whenever a task needs structured thinking before coding.'
---

# /define - Manifest Builder

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

Parse `--amend <manifest-path>` from arguments (can appear anywhere). `--from-do` flag (optional, used with `--amend`) signals the autonomous fast path.

If no arguments provided, ask: "What would you like to build or change?"

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

**Task file structures are presumed relevant.** Task files contain quality gates, reviewer agents, risks, scenarios, and trade-offs. These are angles you won't think to check on your own — they exist precisely because they're easy to miss. Quality gates are auto-included; Resolvable structures (risks, scenarios, trade-offs) must be **resolved**: either presented to the user for selection, or explicitly skipped with logged reasoning (e.g., "CODING.md concurrency risk skipped: single-threaded CLI tool"). Silent drops are the failure mode — not over-asking.

**Task file content types.** Five categories, each handled differently:
- **Quality gates** (structured items under `## Quality Gates` — tables, bullet lists, or any format with thresholds/criteria) — auto-include as INV-G*, omit clearly inapplicable with logged reasoning. User reviews manifest.
- **Resolvable** (tables/checklists: risks, scenarios, trade-offs) — resolve via interview, encode as INV/AC or explicitly skip.
- **Compressed awareness** (bold-labeled one-line domain summaries, not tables/checklists) — informs your probing; no resolution needed.
- **Process guidance hints** (counter-instinctive practices) — practices LLMs would get wrong without explicit guidance. Two modes: **candidates** (labeled as PG candidates, presented as batch after scenarios, user selects) and **defaults** (`## Defaults` section, included in manifest without probing, user reviews manifest and removes if not applicable). Both become PG-* in the manifest.
- **Reference files** (`references/*.md`) — detailed lookup data for `/verify` agents. Do not load during the interview.

**Encode quality gates and Defaults immediately after reading task files — before the interview.** Log each as `- [x]` RESOLVED.

Probing beyond task files is adaptive — driven by the specific task, user responses, and what you discover. Task files don't cap what to ask; they set a floor.

## Existing Manifest Feedback

If input references a previous manifest: **treat it as source of truth**. It contains validated decisions — default to building on it, preserving what's settled. Confirm approach with user if unclear.

## Amendment Mode

When `--amend <manifest-path>` is present: read `references/AMENDMENT_MODE.md` for amendment rules.

## Multi-Repo Scope

When task spans multiple repositories, capture during intent:

- **Which repos** and their roles
- **Cross-repo constraints** (dependencies, coordination requirements)
- **Per-repo differences** (different rules, conventions, verification needs)

Scope deliverables and verification to repo context. Cross-repo invariants get explicit verification checking both sides.

## Principles

1. **Verifiable** - Every Invariant and AC has a verification method (bash, subagent, manual). Constraints that can't be verified from output go in Process Guidance.

2. **Validated** - Generate concrete candidates; learn from user reactions. The interview mode defines how findings are shared and decisions are made — see the active interview mode file for behavioral specifics.

3. **Domain-grounded** - Understand the domain before probing. Task files add angles to consider; exploration reveals patterns/constraints. Latent criteria emerge from domain understanding—you can't surface what you don't know.

4. **Complete** - Surface hidden requirements through domain grounding (what exists and constrains us?), outside view (what typically fails in similar projects?), pre-mortem (what could go wrong?), and non-obvious probing (what hasn't user considered?).

5. **Directed** - For complex tasks, establish initial implementation direction (Approach) before execution. Architecture defines starting direction, not step-by-step script. Trade-offs enable autonomous adjustment when reality diverges.

6. **Efficient** - Question quality, not brevity. Each question must: materially change the manifest, lock an assumption, or choose between meaningful trade-offs. If it fails all three, don't ask. One missed criterion costs more than one extra question—err toward asking, never ask trivia. Prioritize questions that split the space—scope and constraints before details.

## Interview Flow

The interview covers these protocols: Domain Grounding, Outside View, Pre-Mortem, Backcasting, Adversarial Self-Review (skip for simple tasks). The active interview mode defines the flow structure — whether protocols run sequentially, interleaved, or organically. See the interview mode file for flow specifics.

## Complexity Triage

After understanding the task, calibrate interview depth:

| Complexity | Indicators | Protocols |
|------------|-----------|-----------|
| **Simple** | Single file, obvious approach, low risk | Domain Grounding + quick Pre-Mortem |
| **Standard** | Multi-file, clear domain, moderate risk | All protocols, lightweight Adversarial |
| **Complex** | Multi-deliverable, unfamiliar domain, high risk, multi-repo | All protocols including Approach section |

When uncertain, default to Standard. User can signal "enough" to compress at any point.

## Interview Style

Resolve interview style from `--interview` argument → default `thorough`.

Load the interview mode file for behavioral specifics:
- `thorough` (default): read `references/interview-modes/thorough.md`
- `minimal`: read `references/interview-modes/minimal.md`
- `autonomous`: read `references/interview-modes/autonomous.md`

Follow the loaded interview mode's rules for question format, flow structure, checkpoint behavior, finding-sharing, and convergence for the remainder of this /define run.

**Auto-decided items**: When interview style causes an item to be auto-decided (agent picks recommended option instead of asking), encode it normally as INV/AC/PG with an "(auto)" annotation, AND list it in the Known Assumptions section with the reasoning for the chosen option.

**Style is dynamic**: The `--interview` flag sets the starting posture, not a rigid lock. Shift when the user's behavior signals a different mode: thorough user says "enough" or "just build it" → shift to autonomous. Autonomous user asks questions or requests probing → shift to thorough. When the user or verifier gives feedback on an autonomous manifest, auto-resolve the concerns and stay in autonomous mode unless the user explicitly requests more interaction. Log any style shift to the discovery file.

## Constraints

**Decisions lock through structured options** - Questions that lock manifest content (encoding decisions, scope boundaries, trade-offs) present 2-4 concrete options, one marked "(Recommended)". The messaging file defines the tool; the interview mode defines when to present options, how to share findings, and how to discuss before locking.

**Resolve all Resolvable task file structures** — After reading task files, extract every Resolvable table and checklist (risk lists, scenario prompts, trade-offs) and log each as a pending item. Quality gates and `## Defaults` are not Resolvable — auto-include them (quality gates as INV-G*, Defaults as PG-*), omitting clearly inapplicable ones with logged reasoning. Resolve each Resolvable item by either:
1. **Present to user** for selection with structured options — selected items encoded as INV-G* or AC-*, unselected items explicitly scoped out
2. **Skip with logged justification** — when a structure genuinely doesn't apply to this task, log why (e.g., "CODING.md concurrency risk: single-threaded CLI tool, no concurrent access")

Don't defer to synthesis — these are structural decisions that compound when missed. The flexibility is in justifying what to skip, not in whether to engage.

**Discoverable unknowns — search first** - Facts about the project (existing structure, patterns, conventions, prior decisions) are discoverable through Domain Grounding. Don't ask the user about facts you could discover. Only ask about discoverable facts when: multiple plausible candidates exist, searches yield nothing but the fact is needed, or the ambiguity is actually about intent not fact. When asking, present what you found and recommend one option.

**Preference unknowns — ask early** - Trade-offs, priorities, scope decisions, and style preferences cannot be discovered through exploration. Ask these directly. Provide concrete options with a recommended default. If genuinely low-impact and the user signals "enough", proceed with the recommended default and record as a Known Assumption in the manifest.

**Mark a recommended option** - Every question with options must include a recommended default. For single-select, mark exactly one "(Recommended)". For multi-select, mark sensible defaults or none if all equally valid. Reduces cognitive load — users accept, reject, or adjust rather than evaluating from scratch.

**Confirm before encoding** - When you discover constraints from exploration (structural patterns, conventions, existing boundaries), present them to the user before encoding as invariants. "I found X—should this be a hard constraint?" Discovered ≠ confirmed. This applies to exploration-discovered constraints, not to task-file quality gates and Defaults (which are auto-included per the rules above).

**Encode explicit constraints** - When users state preferences, requirements, or constraints (not clarifying remarks or exploratory responses), these must map to an INV or AC. "Single-author writing only" → process invariant. "Target < 1500 words" → acceptance criterion. Don't let explicit constraints get lost in the interview log.

**Probe for approach constraints** - Beyond WHAT to build, ask HOW it should be done. Tools to use or avoid? Methods required or forbidden? Automation vs manual? These become process invariants.

**Probe input artifacts** - When input references external documents (file paths, URLs), ask: "Should [document] be a verification source?" If yes, encode as Global Invariant.

**Log is working memory** - Write to `/tmp/define-discovery-{timestamp}.md` immediately after each discovery. The log is not a narrative record — it's the source of truth for what's been found and what still needs resolution. Another agent reading only the log could resume the interview.

Every actionable item gets logged with resolution status:
- `- [ ]` PENDING — needs resolution (present to user, probe further, or encode)
- `- [x]` RESOLVED — encoded as INV/AC/PG/ASM, confirmed by user, or answered
- `- [~]` SKIPPED — explicitly scoped out with reasoning

Log pending items as they emerge — from any source:
- Auto-included items after reading task files (quality gates as INV/AC, Defaults as PG — log as `- [x]` RESOLVED)
- Resolvable task file structures after reading task files (risks, scenarios, trade-offs)
- Domain grounding findings needing user confirmation before encoding
- Pre-mortem scenarios needing disposition (encode, scope out, or mitigate)
- User constraints needing INV/AC/PG mapping
- Backcasting assumptions needing resolution
- Follow-up questions triggered by earlier answers

Read full log before synthesis. Unresolved `- [ ]` items must be addressed first.

**Confirm understanding periodically** - Before transitioning to a new topic area or after resolving a cluster of related questions, synthesize your current understanding. The active interview mode defines the checkpoint format — how understanding is shared and what invitation for contribution is offered.

**Batch related questions** - Group related questions into a single turn rather than asking one at a time. Batching keeps momentum and reduces round-trips without sacrificing depth. Each batch should cover a coherent topic area—don't mix unrelated concerns in one batch.

**Stop when converged** - The checklist below defines WHAT must be true for convergence. The active interview mode defines HOW aggressively to pursue it (probing style, synthesis threshold). Convergence requires: domain grounded (pre-mortem scenarios are project-specific, not generic), pre-mortem scenarios logged with dispositions (see Pre-Mortem Protocol), edge cases probed, no unresolved `- [ ]` items in the log, quality gates from task files encoded as INV-G* (or omitted with logged reasoning), Defaults encoded as PG-*, and no obvious areas left unexplored. Remaining low-impact unknowns that don't warrant further probing are recorded as Known Assumptions in the manifest. User can signal "enough" to override.

**Insights become criteria** - Domain grounding findings, outside view findings, pre-mortem risks, non-obvious discoveries → convert to INV-G* or AC-*. Don't include insights that aren't encoded as criteria. This applies equally to Resolvable task file content — risks and scenario dispositions must be traceable to manifest criteria or they're aspirational, not enforced.

**Automate verification** - Use automated methods (commands, subagent review). When using general-purpose subagent, default to `inherit`. When a criterion seems to require manual verification, probe the user: suggest how it could be made automatable, or ask if they have ideas. Manual only as a last resort or when the user explicitly requests it.

**Assign verification phases** - Each criterion's verify block has an optional `phase:` field (numeric, default 1). /verify runs phases in ascending order — Phase N+1 only runs when all Phase N criteria pass.

The principle: **group criteria by iteration speed — faster feedback loops run first.** Criteria that fail fast and are cheap to re-run should be in earlier phases. Criteria that are slow, expensive, deploy-dependent, or require human judgment should be in later phases. The number of phases and their values depend on the task — use as many or as few as the iteration speed differences warrant.

Example reasoning for a typical coding task:
- **Fastest (default phase)**: Agent reviewers (code-bugs-reviewer, etc.) and criteria-checker bash/codebase checks — seconds to run, any code change can immediately be re-verified.
- **Slower (later phase)**: E2e tests — usually require deployment, any code change invalidates them, and they act as a seal on the whole system. Running them before cheaper checks pass wastes deploy cycles.
- **Slowest (even later phase)**: Manual verification — requires human judgment, can take hours or days. Only run after all automated verification passes.

Omit `phase:` for the fastest criteria (phase 1 is the default). Only set `phase:` explicitly for criteria that should run later. Non-contiguous phases are valid — /verify skips gaps.

## Approach Section (Complex Tasks)

After defining deliverables, probe for **initial** implementation direction. Skip for simple tasks with obvious approach.

**Why "initial"**: Approach provides starting direction, not a rigid plan. Plans break when hitting reality—unexpected constraints, better patterns discovered, dependencies that don't work as expected. The goal is enough direction to start confidently, with trade-offs documented so implementation can adjust autonomously when reality diverges.

**Architecture** - Generate concrete options based on existing patterns. "Given the intent, here are approaches: [A], [B], [C]. Which fits best?" Architecture is direction (structure, patterns, flow), not step-by-step script. When a choice affects multiple deliverables, surface which deliverables depend on it and what would need to change if the choice proves wrong during implementation.

**Execution Order** - Propose order based on dependencies. "Suggested order: D1 → D2 → D3. Rationale: [X]. Adjust?" Include why (dependencies, risk reduction, etc.).

**Risk Areas** - Pre-mortem outputs. "What could cause this to fail? Candidates: [R1], [R2], [R3]." Each risk has detection criteria. Not exhaustive—focus on likely/high-impact.

**Trade-offs** - Decision criteria for competing concerns. "When facing [tension], priority? [A] vs [B]?" Format: `[T-N] A vs B → Prefer A because X`. Enables autonomous adjustment during /do.

**When to include Approach**: Multi-deliverable tasks, unfamiliar domains, architectural decisions, high-risk implementations. The interview naturally reveals if it's needed.

**Architecture vs Process Guidance**: Architecture = structural decisions (components, patterns, structure). Process Guidance = methodology constraints (tools, manual vs automated). "Add executive summary section covering X, Y, Z" is Architecture. "No bullet points in summary sections" is Process Guidance.

## Domain Grounding Protocol

Understand what exists in the affected area. Latent criteria emerge from domain understanding—you can't surface what you don't know.

**The exercise**: "What already exists in the relevant area? What patterns, conventions, and constraints are in place?"

Explore the areas relevant to the task. Surface:
- **Existing patterns** — how similar things are currently done
- **Structure** — components, dependencies, boundaries in the affected area
- **Constraints** — implicit conventions, assumed invariants, existing contracts
- **Prior decisions** — why things are the way they are, when discoverable

What "exploration" means depends on the domain. For code tasks, explore the codebase. For research, the existing knowledge landscape. For content, the audience and existing publications. Task files add domain-specific exploration angles.

**Scoping**: Explore what's relevant to the task description, not the entire domain. Focus on the affected area and its immediate context.

Log findings to the discovery file — both narrative context and pending items:
```
DOMAIN GROUNDING: [area explored]
PATTERNS FOUND: [existing conventions, approaches]
CONSTRAINTS FOUND: [what the existing context assumes or requires]
IMPLICATIONS FOR TASK: [how this shapes what we build]

Pending:
- [ ] Confirm: [pattern X] as constraint?
- [ ] Confirm: [convention Y] as invariant?
```

**Convergence**: Domain grounding converges when you understand the affected area well enough to generate project-specific failure scenarios—not generic ones. If you can only imagine generic failures, you haven't grounded enough. If you can imagine failures that reference specific components, patterns, or conventions in this context, you have.

## Outside View Protocol

Establish what typically fails in this class of task.

**The exercise**: "What's the reference class? What usually goes wrong?"

Identify the task type (refactor, feature, bug fix, etc.). Ground the reference class in what domain grounding revealed—"refactor of a tightly-coupled module with no tests" is a better reference class than "refactor." Search for evidence: prior similar tasks, domain knowledge, task file warnings. What issues emerged post-delivery? What patterns caused rejection?

Log the reference class and its known failure modes. Pre-mortem scenarios inherit these as priors—a refactor that "typically introduces regressions" starts with that as high-likelihood.

```
REFERENCE CLASS: [task type]
BASE RATE FAILURES: [what typically goes wrong]
SOURCE: [prior tasks | domain knowledge | task file]
```

## Pre-Mortem Protocol

Pre-mortems surface latent criteria—requirements users don't know they have until the right failure scenario makes them obvious. This isn't a checkbox; it's the backbone of comprehensive probing.

**The exercise**: "Imagine this task has failed, or the deliverable was rejected. What went wrong?"

### Failure Dimensions

These are lenses for generating scenarios—prompts to activate failure imagination, not a checklist to complete. Apply whichever dimensions are relevant; skip those that genuinely don't apply. If no scenarios emerge from one dimension, move to another—the goal is coverage, not completeness per dimension.

| Dimension | What to imagine | Example scenario |
|-----------|-----------------|------------------|
| **Technical** | What breaks at the code/system level? | Race condition under concurrent access; memory leak at scale |
| **Integration** | What breaks at boundaries? | API contract violated; schema migration breaks consumers |
| **Stakeholder** | What causes rejection even if technically correct? | Doesn't match reviewer's mental model; solves stated problem but not underlying need; correct scope but wrong emphasis |
| **Timing** | What fails later that works now? | Works today, breaks at scale; passes review, fails in production |
| **Edge cases** | What inputs/conditions weren't considered? | Empty input, unicode, malformed data, timeout, concurrent modification |
| **Dependencies** | What external factors cause failure? | Upstream API changes; library deprecation; environment drift |

Task files add domain-specific failure scenarios. Use them as fuel for imagination—pick what's relevant, skip what isn't. They're not exhaustive or mandatory. Scenarios grounded in domain grounding findings are higher signal than generic templates—task file prompts + domain context = project-specific failure modes.

### Generating and Presenting Scenarios

For each relevant dimension, generate concrete failure scenarios. Be specific—"something breaks" is useless; "the scheduler runs a job twice when the server restarts mid-execution" is actionable.

**Present scenarios and resolve dispositions.** The active interview mode defines how scenarios are presented — question format, discussion style, and how the user engages with dispositions.

**Mental model alignment**: Before finalizing deliverables, check for mismatch between your understanding and the user's expectation. Mismatches are latent criteria — expectations they didn't state. The active interview mode defines the format for this alignment check.

When logging scenarios, capture what matters:
- **What fails** (the specific scenario)
- **Likelihood and impact** (to prioritize probing)
- **What question this raises** (what to ask the user)

Example log entry:
```
DIMENSION: Timing
SCENARIO: Feature works in dev but rate limits hit in production due to external API calls
LIKELIHOOD: Medium | IMPACT: High
- [ ] Ask user: External API rate limits — resolve disposition
```

### Scenario Disposition

Every scenario worth logging must resolve to one of:

1. **Encoded as criterion** — becomes INV-G*, AC-*, or Risk Area with detection
2. **Explicitly out of scope** — user confirmed it's acceptable risk for this task
3. **Mitigated by approach** — architecture choice eliminates the failure mode

No dangling scenarios. If you logged it, resolve it.

### When Is Pre-Mortem Complete?

Pre-mortem probing converges when:
- Relevant dimensions have been considered (not all—relevant)
- Generated scenarios have dispositions (encoded, out of scope, or mitigated)
- User confirms no major failure modes were missed

"I can't think of more scenarios" after trying multiple dimensions = converged. "I haven't tried thinking about it" = not converged.

## Backcasting Protocol

Surface positive dependencies — what has to go right for the task to succeed.

**The exercise**: "Imagine this task succeeded on first review. What had to go right?"

Where pre-mortem asks "what broke?", backcasting asks "what held?" This reveals load-bearing assumptions you haven't examined.

Focus on implicit assumptions:
- What existing infrastructure/tooling are you relying on?
- What user behavior are you assuming?
- What needs to stay stable that could change?

For each positive dependency, resolve its disposition — whether it's a safe assumption, needs verification, should be encoded as an invariant, or is actually a risk. The active interview mode defines how dependencies are presented and resolved.

Converges when load-bearing assumptions are surfaced and each is verified, encoded, or logged as Known Assumption.

## Adversarial Self-Review

Red-team yourself: if you wanted this task to fail subtly, what decisions would you make that look reasonable individually?

Pre-mortem imagines external failures. Adversarial self-review imagines process self-sabotage—patterns that compound:
- Small scope additions ("just one more thing")
- Edge cases deferred ("we'll handle that later")
- "Temporary" solutions that become permanent
- Process shortcuts that erode quality

For each pattern identified, resolve its disposition — whether to add as Process Guidance, encode as a verifiable Invariant, accept as low risk, or note it's already covered. The active interview mode defines how patterns are presented and resolved.

Skip for simple tasks. Use for tasks with scope risk, process complexity, or history of scope creep.

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

## Amendment Protocol

Manifests support amendments during execution:
- Reference original ID: "INV-G1.1 amends INV-G1"
- Track in manifest: `## Amendments`

## Verification Loop

After writing the manifest, check the manifest's `mode:` field and load the execution mode file from `../do/references/execution-modes/` for the resolved mode (default: `thorough`). Follow the mode's "Manifest Verification (/define)" section for whether to run the manifest-verifier and how many cycles.

When running the verifier, pass only the file paths — no summary, framing, or commentary:

```
Invoke the manifest-dev:manifest-verifier agent with: "Manifest: /tmp/manifest-{timestamp}.md | Log: /tmp/define-discovery-{timestamp}.md"
```

The verifier returns **CONTINUE** or **COMPLETE**:

- **CONTINUE**: Present the verifier's questions to the user, log answers to the discovery file, update the manifest, then invoke the verifier again.
- **COMPLETE**: Proceed to summary for approval.

Repeat until COMPLETE or user signals "enough".

Do not paraphrase, filter, or editorialize the verifier's questions — present them directly. Do not add context, justification, or steering to the invocation. The verifier sees what you may have missed; let it assess independently.

## Summary for Approval

Before asking for approval, explain the plan the way you'd explain it to a senior engineer over Slack. They need to know what you're building, what could go wrong, and how you'll know it's right.

**Voice**: Plain language. No manifest codes (D1, AC-1.1, INV-G3), no YAML blocks, no structured-document vocabulary. Write prose — the manifest is the structured document, the summary is the human conversation about it.

**Structure the explanation around three things**:

1. **What I'll do** — Walk through each piece of work in execution order. For each, state what it is and how you'll verify it's correct (parenthetical or inline — verification is present but not dominant). Example: "I'll create a reference doc for auto-mode behavior, covering what changes per phase. I'll verify it doesn't contradict SKILL.md (criteria-checker reads both files for conflicts)."

2. **Rules that always hold** — State the invariants as plain rules, not coded entries. Example: "Explicit flags always override --auto defaults. Every owner-replacing decision gets logged with reasoning. Auto mode halts on truly unresolvable issues — it's not silent-failure mode."

3. **Architecture sketch** — Include an ASCII diagram when the task has multiple components with inter-component flow or dependencies. Skip for single-deliverable tasks.

**The test**: If the summary reads like a compressed manifest, rewrite it. If it reads like something you'd actually say to a colleague, it's right.

**Anti-patterns**:
- Manifest cosplay — codes, YAML, structured labels dressed up as prose
- Hiding detail behind counts ("8 automated verifications")
- Abstracting instead of showing ("3 deliverables covering auth")
- Omitting "obvious" things that could still be wrong
- Listing verification methods without the thing they verify

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
