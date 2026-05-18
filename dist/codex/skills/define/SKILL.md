---
name: define
description: 'Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and Approach. Use when planning features, scoping refactors, debugging complex issues, or whenever a task needs structured thinking before coding. Triggers: define, manifest, scope, plan, spec out, break down.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>] [--canvas]'
user-invocable: true
---

Encode the conversation's shared understanding as a Manifest at `<scratch>/manifest-{ts}.md` (writable scratch path — prefer `/tmp/` when writable, else `$TMPDIR` / `%TEMP%`). If the transcript lacks shared understanding, invoke `manifest-dev:figure-out` first; propagate `--autonomous` when invoked from `/auto` or `/do`'s amendment path. **Pre-flight:** babysit (`--babysit <pr-url>` → `references/BABYSIT_MODE.md`); amend (args contain a manifest file path → see Amendment below); else fresh.

**Encoding discipline.** figure-out reaches shared understanding of the *problem*; /define handles manifest-specific *encoding* judgment calls — invariant vs process guidance, AC scope and pass threshold, phase ordering (fast vs slow), trade-offs to lock as `[T-N]`. Surface the load-bearing encoding decisions briefly with a recommended answer before encoding; auto-decide the rest and mark `(auto)` + matching ASM. The manifest is the acceptance contract — what the user accepts as *"I'd ship the outcome of executing this."*

**Task files.** Identify task type; load applicable files from `tasks/` per `tasks/README.md` — their gates and Defaults auto-encode before the interview. For code tasks, also compose `tasks/PR_LIFECYCLE.md` when origin is on github.com; probe if origin is missing or a github-enterprise host. Per-repo for multi-repo manifests.

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
    agent: "..."              # optional, default = general-purpose subagent
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
    agent: "..."              # optional, default = general-purpose subagent
    model: "..."              # optional, default = inherit from invoking context
    phase: 1                  # optional integer, default 1; higher phases run after lower pass
  ```
````

Verifiers return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action — `/do` routes via `/escalate`). Automate verification — criteria that genuinely require human action belong in Process Guidance, not as ACs. Auto-decided items carry `(auto)` after the ID with a matching ASM entry.

**Amendment.** A manifest path in `$ARGUMENTS` means amend. Read it fully, apply targeted changes only — preserve unaffected items verbatim. IDs are stable (modify in place; remove without renumbering). No `## Amendments` log — git is history. Autonomous when caller is `/auto` or `/do`; interactive otherwise.

**Flags.** `--babysit <pr-url>` synthesizes a lifecycle-only manifest from a PR (`references/BABYSIT_MODE.md`). `--canvas` generates a Shared Understanding Canvas alongside the manifest (`references/CANVAS_MODE.md`). `--autonomous` skips summary approval and lets figure-out self-answer. Multi-repo: `references/MULTI_REPO.md`.

**Summary for Approval.** Before Complete, write a plain-language digest (plan / what / guardrails / how-verified) — no codes, no YAML, no schema vocab. **Test:** reads like talking to a colleague, not a compressed manifest. Approval → Complete; feedback → revise; `/do` → handoff; decline → exit silently. Skip the wait when caller is `/auto` or `/do` amendment, or the user signals "enough".

**Complete.** Emit the load-bearing handoff (`<manifest-path>` is the absolute path you wrote; `<dir>` is the project directory in slug form, e.g. `-home-user-manifest-dev`):

```text
Manifest complete: <manifest-path>
Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl

To execute: /do <manifest-path>
```
