---
description: 'Manifest builder implementation. Converts known requirements into Deliverables + Invariants with verification criteria.'
user-invocable: false
---

# /define - Manifest Builder

## Goal

Build a **comprehensive Manifest** that captures:
- **What we build** (Deliverables with Acceptance Criteria)
- **How we'll get there** (Approach - validated direction)
- **Rules we must follow** (Global Invariants)

**Why thoroughness matters**: Every criterion discovered NOW is one fewer rejection during implementation/review. The goal is a deliverable that passes review on first submission—no "oh, I also needed X" after the work is done.

Comprehensive means surfacing **latent criteria**—requirements the user doesn't know they have until probed. Users know their surface-level needs; your job is to discover the constraints and edge cases they haven't thought about.

100% upfront is impossible—some criteria only emerge during implementation. Aim for high coverage. The manifest supports amendments for what's discovered later.

Output: `/tmp/manifest-{timestamp}.md`

## Input

`$ARGUMENTS` = task description, optionally with context/research

If no arguments provided, ask: "What would you like to build or change?"

## Domain Guidance

| Domain | Indicators | Guidance File |
|--------|------------|---------------|
| **Coding** | Any code change (base for Feature, Bug, Refactor) | `tasks/CODING.md` |
| **Feature** | New functionality, APIs, enhancements | `tasks/FEATURE.md` |
| **Bug** | Defects, errors, regressions, "not working", "broken" | `tasks/BUG.md` |
| **Refactor** | Restructuring, reorganization, "clean up", pattern changes | `tasks/REFACTOR.md` |
| **Prompting** | LLM prompts, skills, agents, system instructions | `tasks/PROMPTING.md` |
| **Document** | Specs, proposals, reports, formal docs | `tasks/DOCUMENT.md` |
| **Research** | Investigations, analyses, comparisons | `tasks/RESEARCH.md` |
| **Blog** | Blog posts, articles, tutorials | `tasks/BLOG.md` |

**Composition**: Code-change tasks combine CODING.md (base quality gates) with domain-specific guidance. Domains aren't mutually exclusive—a "bug fix that requires refactoring" benefits from both BUG.md and REFACTOR.md. Related domains compound coverage.

**Task files are supplementary, not exhaustive**. Probing is adaptive—driven by the specific task, user responses, and what you discover. Task files add angles you might not think to check; they don't replace judgment about what matters for this task.

## Existing Manifest Feedback

If input references a previous manifest: **treat it as source of truth**. It contains validated decisions — default to building on it, preserving what's settled. Confirm approach with user if unclear.

## Multi-Repo Scope

When task spans multiple repositories, capture during intent:

- **Which repos** and their roles
- **Cross-repo constraints** (dependencies, coordination requirements)
- **Per-repo differences** (different rules, conventions, verification needs)

Scope deliverables and verification to repo context. Cross-repo invariants get explicit verification checking both sides.

## Principles

1. **Verifiable** - Every Invariant and AC has a verification method (bash, subagent, manual). Constraints that can't be verified from output go in Process Guidance.

2. **Validated** - You drive the interview. Generate concrete candidates; learn from user reactions.

3. **Domain-grounded** - Understand the domain before probing. Task files add angles to consider; exploration reveals patterns/constraints. Latent criteria emerge from domain understanding—you can't surface what you don't know.

4. **Complete** - Surface hidden requirements through outside view (what typically fails in similar projects?), pre-mortem (what could go wrong?), and non-obvious probing (what hasn't user considered?).

5. **Directed** - For complex tasks, establish validated implementation direction (Approach) before execution. Architecture defines direction, not step-by-step script. Trade-offs enable autonomous adjustment.

6. **Efficient** - Every question must pass a quality gate: it **materially changes the manifest**, **locks an assumption**, or **chooses between meaningful trade-offs**. If a question fails all three, don't ask it. One missed criterion costs more than one extra question—err toward asking, but never ask trivia. Prioritize questions that split the space—scope and constraints before details.

## Constraints

**Task files supplement probing** - Task files add domain-specific risks and trade-offs as prompts—angles you might not think to check. They don't constrain what to ask; probing adapts to the specific task.

**Discoverable unknowns — search first** - Facts about the project (existing structure, patterns, conventions, prior decisions) are discoverable. Exhaust exploration before asking the user. Only ask about discoverable facts when: multiple plausible candidates exist, searches yield nothing but the fact is needed, or the ambiguity is actually about intent not fact. When asking, present what you found and recommend one option.

**Preference unknowns — ask early** - Trade-offs, priorities, scope decisions, and style preferences cannot be discovered through exploration. Ask these directly. Provide concrete options with a recommended default. If genuinely low-impact and the user signals "enough", proceed with the recommended default and record as a Known Assumption in the manifest.

**Mark a recommended option** - Every question with options must include a recommended default. For single-select, mark exactly one "(Recommended)". For multi-select, mark sensible defaults or none if all equally valid. Reduces cognitive load — users accept, reject, or adjust rather than evaluating from scratch. AskUserQuestion supports max 4 options per question.

**Confirm before encoding** - When you discover constraints from exploration (structural patterns, conventions, existing boundaries), present them to the user before encoding as invariants. "I found X—should this be a hard constraint?" Discovered ≠ confirmed.

**Encode explicit constraints** - When users state preferences, requirements, or constraints (not clarifying remarks or exploratory responses), these must map to an INV or AC. "Single-author writing only" → process invariant. "Target < 1500 words" → acceptance criterion. Don't let explicit constraints get lost in the interview log.

**Probe for approach constraints** - Beyond WHAT to build, ask HOW it should be done. Tools to use or avoid? Methods required or forbidden? Automation vs manual? These become process invariants.

**Probe input artifacts** - When input references external documents (file paths, URLs), ask: "Should [document] be a verification source?" If yes, encode as Global Invariant.

**Log after every action** - Write to `/tmp/define-discovery-{timestamp}.md` immediately after each discovery (domain findings, interview answers, exploration insights). Goal: another agent reading only the log could resume the interview. Read full log before synthesis.

**Confirm understanding periodically** - Before transitioning to a new topic area or after resolving a cluster of related questions, synthesize your current understanding back to the user: "Here's what I've established so far: [summary]. Correct?" This catches interpretation drift early—a misunderstanding in round 2 compounds through round 8 if never checked.

**Batch related questions** - Group related questions into a single turn rather than asking one at a time. Batching keeps momentum and reduces round-trips without sacrificing depth. Each batch should cover a coherent topic area—don't mix unrelated concerns in one batch.

**Stop when converged** - Err on more probing. Convergence requires: pre-mortem checked, domain understood, edge cases probed, and no obvious areas left unexplored. Only then, if very confident further questions would yield nothing new, move to synthesis. Remaining low-impact unknowns that don't warrant further probing are recorded as Known Assumptions in the manifest. User can signal "enough" to override.

**Verify before finalizing** - After writing manifest, verify completeness using the manifest-verifier agent with the manifest and discovery log as input. If status is CONTINUE, ask the outputted questions, log new answers, update manifest, re-verify. Loop until COMPLETE or user signals "enough".

**Insights become criteria** - Outside view findings, pre-mortem risks, non-obvious discoveries → convert to INV-G* or AC-*. Don't include insights that aren't encoded as criteria.

**Automate verification** - Use automated methods (commands, subagent review). When using general-purpose subagent, default to opus model. When a criterion seems to require manual verification, probe the user: suggest how it could be made automatable, or ask if they have ideas. Manual only as a last resort or when the user explicitly requests it.

## Approach Section (Complex Tasks)

After defining deliverables, probe for implementation direction. Skip for simple tasks with obvious approach.

**Architecture** - Generate concrete options based on existing patterns. "Given the intent, here are approaches: [A], [B], [C]. Which fits best?" Architecture is direction (structure, patterns, flow), not step-by-step script.

**Execution Order** - Propose order based on dependencies. "Suggested order: D1 → D2 → D3. Rationale: [X]. Adjust?" Include why (dependencies, risk reduction, etc.).

**Risk Areas** - Pre-mortem outputs. "What could cause this to fail? Candidates: [R1], [R2], [R3]." Each risk has detection criteria. Not exhaustive—focus on likely/high-impact.

**Trade-offs** - Decision criteria for competing concerns. "When facing [tension], priority? [A] vs [B]?" Format: `[T-N] A vs B → Prefer A because X`. Enables autonomous adjustment during /do.

**When to include Approach**: Multi-deliverable tasks, unfamiliar domains, architectural decisions, high-risk implementations. The interview naturally reveals if it's needed.

**Architecture vs Process Guidance**: Architecture = structural decisions (components, patterns, structure). Process Guidance = methodology constraints (tools, manual vs automated). "Add executive summary section covering X, Y, Z" is Architecture. "No bullet points in summary sections" is Process Guidance.

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

## 2. Approach (Complex Tasks Only)
*Validated implementation direction. Omit for simple tasks.*

- **Architecture:** [High-level HOW - validated direction, not step-by-step]

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
    command: "[if bash]"
    agent: "[if subagent]"
    model: "[if subagent, default opus for general-purpose]"
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

## Summary for Approval

Before asking for approval, output a scannable summary that enables full manifest review without reading the structured document.

**Goal**: User can catch any mistake—wrong deliverable scope, missing AC, wrong verification method, bad assumption, incorrect flow—by scanning the summary alone.

**Requirements**:
- Expose all manifest content (deliverables, ACs, invariants, assumptions, verification methods)
- Show verification inline with what it verifies—user must judge if verification method fits the criterion
- Include ASCII diagram showing structure, flow, and dependencies
- Optimize for human scanning speed, not AI parsing
- Adapt presentation to the task—no fixed template

**Anti-patterns**:
- Hiding detail behind counts ("8 automated verifications")
- Abstracting instead of compressing ("3 deliverables covering auth")
- Omitting "obvious" things that could still be wrong

## Complete

```text
Manifest complete: /tmp/manifest-{timestamp}.md

To execute: /do /tmp/manifest-{timestamp}.md [log-file-path if iterating]
```

If this was an iteration on a previous manifest that had an execution log, include the log file path in the suggestion.
