---
name: define
description: 'Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and Approach. Use when planning features, scoping refactors, debugging complex issues, or when the user asks to define, scope, plan, spec out, make a manifest, or break down a task.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>] [--canvas]'
user-invocable: true
---

Encode the conversation's shared understanding as a Manifest at `~/.manifest-dev/manifests/manifest-{ts}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so manifests survive OS temp cleanup across multi-day work. Fall back to a writable temp path (`/tmp/`, else `$TMPDIR` / `%TEMP%`) only when the home directory isn't writable. If the transcript lacks shared understanding, invoke `manifest-dev:figure-out` first; propagate `--autonomous` when invoked from `/auto` or `/do`'s amendment path. **Pre-flight:** if `--babysit <pr-url>`, load `references/BABYSIT_MODE.md` and follow its synthesis flow; if `$ARGUMENTS` contains a manifest file path, amend (see below); else fresh.

**Encoding discipline.** figure-out reaches shared understanding of the *problem*; /define handles manifest-specific *encoding* judgment calls — invariant vs process guidance, AC scope and pass threshold, phase ordering (fast vs slow), trade-offs to lock as `[T-N]`. Surface the load-bearing encoding decisions briefly with a recommended answer before encoding; auto-decide the rest and mark `(auto)` + matching ASM. The manifest is the acceptance contract — what the user accepts as *"I'd ship the outcome of executing this."*

**Task files.** Identify task type and load the matching file(s) from `tasks/` — their Quality Gates auto-encode as INV-G*/AC-* and Defaults as PG-* before the interview (surface each as it lands so the dialogue carries the encoding forward). These define task files carry **encoder data only**; probing fuel lives in figure-out's own parallel probe files (`skills/figure-out/tasks/`) — the two sets are decoupled. Per-repo for multi-repo manifests.

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
| Research | Investigations, analyses, comparisons | `research/RESEARCH.md` |
| Blog | Blog posts, articles, tutorials (base: Writing) | `BLOG.md` |

*Composition:* code-change tasks combine `CODING.md` (base gates) with the specific FEATURE/BUG/REFACTOR; text-authoring combines `WRITING.md` with BLOG/DOCUMENT; Research composes `research/RESEARCH.md` with `research/sources/`. Domains aren't mutually exclusive (a bug fix that refactors uses both). `PR_LIFECYCLE.md` composes onto `CODING.md` when the local `origin` points at github.com (auto-detected; probe if origin is missing or a github-enterprise host) — it templates one AC per repo whose `verify.prompt:` spawns a general-purpose agent that activates the `check-pr` skill — the prompt is the steering surface for per-PR nuances (labels, approvers, flaky-CI/retrigger overrides). **Exception:** PROMPTING does not compose with CODING unless the task also changes executable code.

*Content types:* **Quality Gates** (`## Quality Gates`) → INV-G*/AC-* (omit clearly inapplicable with stated reasoning); **Defaults** (`## Defaults`) → PG-* pre-interview, user reviews and removes if N/A; **Reference files** (`tasks/**/references/*.md`) → verifier-agent lookup data, not loaded during /define.

**Verifier prompt discipline.** Before writing `verify.prompt` fields, invoke the prompt-engineering skill if it is available; if not, apply its core discipline inline. Verifier prompts are prompts: state the verifier's goal, evidence to inspect, PASS/FAIL/BLOCKED contract, and non-obvious context. Do not run a separate prompt-engineering interview — /define owns the manifest interview.

**Encoding gates — always general-purpose + a skill.** There is no `verify.agent` field. Every gate is verified by a **general-purpose** subagent driven by `verify.prompt`; when a gate needs specialized behavior, the prompt tells that agent to **activate a skill**. Code-quality gates activate the `review-code` skill with a dimension; other specialized checks activate their skill (`check-pr`, `review-prompt`). Pattern:

```yaml
verify:
  prompt: |
    Spawn a general-purpose review using the manifest-dev review-code skill with dimension=<dimension> against the change.
    PASS only if no <LOW|MEDIUM>-or-higher findings. Report findings with severity.
```

The 13 review-code dimensions are: change-intent, code-bugs, contracts, type-safety (defect-finders, no LOW+); operational-readiness, code-design, code-maintainability, code-simplicity, code-testability, test-quality, docs, prose-value, context-file-adherence (advisory, no MEDIUM+). For a non-review-code specialized check, name its skill in the prompt instead, e.g. *"Spawn a general-purpose agent and activate the manifest-dev check-pr skill. PR: …"*.

## Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]

## 2. Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW — starting direction]
- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: [why this order]
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
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Description: ...

## 5. Known Assumptions
- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

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

Verifiers return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action — `/do` routes via `/escalate`). Automate verification — criteria that genuinely require human action belong in Process Guidance, not as ACs. Auto-decided items carry `(auto)` after the ID with a matching ASM entry.

**Amendment.** A manifest path in `$ARGUMENTS` means amend. Read it fully, apply targeted changes only — preserve unaffected items verbatim. IDs are stable (modify in place; remove without renumbering). No `## Amendments` log — git is history. Autonomous when caller is `/auto` or `/do`; interactive otherwise.

**Flags.** `--babysit <pr-url>` — load `references/BABYSIT_MODE.md`; synthesizes a lifecycle-only manifest from a PR. `--canvas` — load `references/CANVAS_MODE.md`; generates a Shared Understanding Canvas alongside the manifest. `--autonomous` skips summary approval and lets figure-out self-answer. When the task spans multiple repos (manifest declares `Repos:` in Intent), load `references/MULTI_REPO.md`.

**Summary for Approval.** Before Complete, write a plain-language digest (plan / what / guardrails / how-verified) — no codes, no YAML, no schema vocab. **Test:** reads like talking to a colleague, not a compressed manifest. Approval → Complete; feedback → revise; `/do` → handoff; decline → exit silently. Skip the wait when caller is `/auto` or `/do` amendment, or the user signals "enough".

**Complete.** Emit the load-bearing handoff (`<manifest-path>` is the absolute path you wrote; `<dir>` is the project directory in slug form, e.g. `-home-user-manifest-dev`):

```text
Manifest complete: <manifest-path>

To execute: /do <manifest-path>
```
