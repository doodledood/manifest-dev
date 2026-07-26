---
name: define
description: 'Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and an Initial Approach. Use when planning features, scoping refactors, debugging complex issues, or when the user asks to define, scope, plan, spec out, make a manifest, or break down a task.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>] [--canvas]'
user-invocable: true
---

## Where the manifest goes, and what runs first

Encode the conversation's shared understanding as a Manifest at `~/.manifest-dev/manifests/manifest-{ts}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so manifests survive OS temp cleanup across multi-day work. Fall back to a writable temp path (`/tmp/`, else `$TMPDIR` / `%TEMP%`) only when the home directory isn't writable. If the transcript lacks shared understanding, invoke `manifest-dev:figure-out` first; propagate `--autonomous` when invoked from `/auto` or `/do`'s amendment path. **Pre-flight:** if `--babysit <pr-url>`, load `references/BABYSIT_MODE.md` and follow its synthesis flow; if `$ARGUMENTS` contains a manifest file path, amend (see below); else fresh.

## Encoding discipline

figure-out reaches shared understanding of the *problem*; /define handles manifest-specific *encoding* judgment calls — invariant vs process guidance, AC scope and pass threshold, phase ordering (fast vs slow), trade-offs to record as `[T-N]`. Surface the load-bearing encoding decisions briefly with a recommended answer before encoding; auto-decide the rest and mark `(auto)` + matching ASM. The manifest is the acceptance contract — what the user accepts as *"I'd ship the outcome of executing this."*

**Cutting Deliverables.** A Deliverable is a slice that can be finished on its own and exercised end-to-end — put in front of its real use: run, read, or otherwise judged in the situation it is for, not merely inspected as present. That is what lets its Acceptance Criteria judge whether it works rather than whether it exists; a Deliverable cut along a layer ("the data model", "the endpoints", "the outline", "the sources") can only be gated on existence, the weakest thing a gate can check. Signs a cut is wrong: you can't say how done it is, the name is generic rather than specific to this work, or it's too large to finish soon.

**Ordering Deliverables.** Order by uncertainty — the Deliverable whose approach is least proven leads, so an unworkable direction surfaces while there is still room to change course; record why in the Order rationale line. Real dependencies still bind; uncertainty orders what they leave free. An amendment places a new Deliverable where uncertainty puts it rather than at the end by default.

**Safety-critical candidates.** Any candidate whose violation would be unsafe or irreversible — secrets and credentials, untrusted input, destructive or irreversible actions — becomes a Global Invariant — it must hold across every Deliverable, not only the one that happens to touch it — whatever its origin: a task-file Default, the interview, or a steering amendment. Sharpen it until a verifier can judge it against the best evidence available — the diff, the execution log, the run's own record — and never drop it for resisting verification, since dropping is the outcome this routing exists to prevent.

**Known Assumptions.** Consume `Known Assumption candidate` items from the latest figure-out Read: encode each still-unresolved candidate as an `ASM-*` entry with its default and impact if wrong; omit candidates that later evidence or the user resolved. Do not copy the full Evidence Ledger into the Manifest.

**Criteria pinned by reaction.** Criteria the user pinned by *reacting* to something concrete during figure-out — a mock, a reference, a chosen direction — are success criteria, not flavor: encode them as an Acceptance Criterion or Global Invariant, judged against the criterion the reaction named rather than the artifact that provoked it. Never route one to Process Guidance or the Initial Approach, where /do may weigh it away. This routes onto existing structure; it adds no new manifest section.

## Task files

Identify task type and load the matching file(s) from `tasks/` — their Quality Gates auto-encode as INV-G*/AC-* and Defaults as PG-* before the interview (surface each as it lands so the dialogue carries the encoding forward). These define task files carry **encoder data only**; probing fuel lives in figure-out's own parallel probe files (`skills/figure-out/tasks/`) — the two sets are decoupled. Per-repo for multi-repo manifests.

| Domain | Indicators | File |
|--------|------------|------|
| Coding | Any code change; base review-code dimension gates for intent, bugs, operational readiness, design, tests, docs, context adherence | `CODING.md` |
| Feature | New functionality, APIs, enhancements | `FEATURE.md` |
| Bug | Defects, errors, regressions, "not working", "broken" | `BUG.md` |
| Refactor | Restructuring, "clean up", pattern changes | `REFACTOR.md` |
| PR lifecycle | Shipping a change through CI, review, approvals | `PR_LIFECYCLE.md` |
| Prompting | LLM prompts, skills, agents, system instructions | `PROMPTING.md` |
| Writing | Prose, articles, copy, social, creative (base) | `WRITING.md` |
| Document | Specs, proposals, reports, formal docs (base: Writing) | `DOCUMENT.md` |
| Tech design | Design docs consolidating finished understanding into audience-fit standalone technical documentation (base: Document) | `TECH_DESIGN.md` |
| Research | Investigations, analyses, comparisons | `research/RESEARCH.md` |
| Blog | Blog posts, articles, tutorials (base: Writing) | `BLOG.md` |

*Composition:* code-change tasks combine `CODING.md` (base gates) with the specific FEATURE/BUG/REFACTOR; text-authoring combines `WRITING.md` with BLOG/DOCUMENT, and TECH_DESIGN composes onto DOCUMENT/WRITING; Research composes `research/RESEARCH.md` with `research/sources/`. Domains aren't mutually exclusive (a bug fix that refactors uses both). `PR_LIFECYCLE.md` composes when the output ships through a GitHub PR (auto-detected from a github.com `origin`; probe if origin is missing or a github-enterprise host), including tech-design docs shipped as PRs — it templates one AC per repo whose `verify.prompt:` spawns a general-purpose agent that activates the `check-pr` skill — the prompt is the steering surface for per-PR nuances (labels, approvers, flaky-CI/retrigger overrides). **Exception:** PROMPTING does not compose with CODING unless the task also changes executable code.

*Content types:* **Quality Gates** (`## Quality Gates`) → INV-G*/AC-* (omit clearly inapplicable with stated reasoning); **Defaults** (`## Defaults`) → PG-* pre-interview, user reviews and removes if N/A — a safety-critical Default routes to a gate instead, per **Safety-critical candidates** above, judged by consequence rather than wording; **Reference files** (`tasks/**/references/*.md`) → verifier-agent lookup data, not loaded during /define.

## Writing the gates

**Verifier prompt discipline.** Before writing `verify.prompt` fields, invoke the prompt-engineering skill if it is available; if not, apply its core discipline inline. Verifier prompts are prompts: state the verifier's goal, evidence to inspect, PASS/FAIL/BLOCKED contract, and non-obvious context. Do not run a separate prompt-engineering interview — /define owns the manifest interview.

**Encoding gates — always general-purpose + a skill.** There is no `verify.agent` field. Every gate is verified by a **general-purpose** subagent driven by `verify.prompt`; when a gate needs specialized behavior, the prompt tells that agent to **activate a skill**. Code-quality gates activate the `review-code` skill with a dimension; other specialized checks activate their skill (`check-pr`, `review-prompt`). Pattern:

```yaml
verify:
  prompt: |
    Activate the manifest-dev:review-code skill with dimension=<dimension> and review the change.
    PASS only if no <LOW|MEDIUM>-or-higher findings. Report findings with severity.
```

The 13 review-code dimensions are: change-intent, code-bugs, contracts, type-safety (defect-finders, no LOW+); operational-readiness, code-design, code-maintainability, code-simplicity, code-testability, test-quality, docs, prose-value, context-file-adherence (advisory, no MEDIUM+). The `verify.prompt` is already run by a general-purpose verifier execution context, so the prompt must tell *that* verifier to **activate** the skill — never to spawn another agent (a nested spawn bypasses the runtime's PASS/FAIL/BLOCKED contract). For a non-review-code specialized check, name its skill the same way, e.g. *"Activate the manifest-dev:check-pr skill. PR: …"*.

## Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]

## 2. Initial Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW — starting direction]
- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
- **Trade-offs:**
  - [T-1] [Priority A] vs [Priority B] → Prefer [A] because [reason]

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Description: ...
  ```yaml
  verify:
    prompt: "..."             # required, verbatim verifier instruction
    model: "..."              # optional, default = inherit from invoking context
    phase: 1                  # optional integer, default 1; higher phases run after lower pass
  ```

## 4. Process Guidance
*Advisory recommendations on HOW to work — /do weighs them and may depart, naming the departure on whichever terminal path the run reaches (and in the execution log when one is kept). Only Acceptance Criteria and Global Invariants bind; anything that must hold belongs in a gate.*

- [PG-1] Description: ...

## 5. Known Assumptions
- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables
*Ordered least-proven-first within dependency constraints; list order is the execution order, and Deliverable numbers are stable IDs rather than positions. Plan, not contract — /do may resequence when execution changes what the order was built on, recording the deviation.*

- **Order rationale:** [why this order; omit when there is only one Deliverable]

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: ...
  ```yaml
  verify:
    prompt: "..."             # required, verbatim verifier instruction
    model: "..."              # optional, default = inherit from invoking context
    phase: 1                  # optional integer, default 1; higher phases run after lower pass
  ```
````

**Verdicts.** Verifiers return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action — `/do` routes via `/escalate`). Automate verification. A criterion that resists it becomes a judgment-based gate whose prompt names the concrete evidence the verifier checks against — not a Process Guidance entry; if it genuinely cannot be written as a gate, sharpen or drop it — a criterion nothing checks is not a criterion. Safety-critical candidates are exempt from that branch: never drop one for resisting verification. Criteria that wait on human or external action (deploys, approvals, in-flight CI) stay ACs — the verifier surfaces the wait per its own contract, as BLOCKED or as a FAIL carrying a wait finding, until it clears. Auto-decided items carry `(auto)` after the ID with a matching ASM entry.

## Amendment

A manifest path in `$ARGUMENTS` means amend. Read it fully, apply targeted changes only — preserve unaffected items verbatim. IDs are stable and independent of list position (modify in place; insert or remove without renumbering). No `## Amendments` log — git is history. Autonomous when caller is `/auto` or `/do` — a mid-/do user message is fire-and-forget steering, so don't ask back or wait; interactive otherwise. In autonomous amendment, every judgment call the steering text doesn't settle is auto-decided per the `(auto)`/ASM discipline — the user's audit trail.

## Flags

`--babysit <pr-url>` — load `references/BABYSIT_MODE.md`; synthesizes a lifecycle-only manifest from a PR. `--canvas` — load `references/CANVAS_MODE.md`; generates a disposable Shared Understanding Canvas (temp-homed) during the interview. `--autonomous` skips summary approval and lets figure-out self-answer. When the task spans multiple repos (manifest declares `Repos:` in Intent), load `references/MULTI_REPO.md`.

## Summary for Approval

Before Complete, write a plain-language digest (plan / what / guardrails / how-verified) — no codes, no YAML, no schema vocab. **Test:** reads like talking to a colleague, not a compressed manifest. Approval → Complete; feedback → revise; `/do` → handoff; decline → exit silently. Skip the wait when caller is `/auto` or `/do` amendment, or the user signals "enough".

## Complete

Emit the load-bearing handoff (`<manifest-path>` is the absolute path you wrote; `<dir>` is the project directory in slug form, e.g. `-home-user-manifest-dev`):

```text
Manifest complete: <manifest-path>

To execute: /do <manifest-path>
For unattended execution, invoke /do <manifest-path> as the execution entrypoint. /do reads the manifest and owns the manifest-completion contract: it sets that completion contract when the active harness exposes a goal-setting or continuation capability, or prints the manual copy-paste contract when not. /define does not set a separate /do goal.
```
