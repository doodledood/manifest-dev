---
name: define
description: 'Experimental. Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and Approach. Auto-invokes /figure-out when the transcript lacks understanding. Use when planning features, scoping refactors, debugging complex issues, or whenever a task needs structured thinking before coding. Triggers: define, manifest, scope, plan, spec out, break down.'
argument-hint: '[task] [--babysit <pr-url>] [--canvas]'
user-invocable: true
---

Take the conversation's shared understanding and encode it as a Manifest at `/tmp/manifest-{ts}.md`. If the transcript lacks shared understanding, invoke `manifest-dev-experimental:figure-out` first ("no prior understanding detected — probing first"); when invoked from `/auto` or with `--autonomous`, propagate the flag so figure-out self-answers without user wait. Chat-derived amendment intent (e.g., "also handle X", "change Y") + Session-Default Detection of a prior `Manifest complete:` line skip this front-door and route to amendment instead.

The manifest captures **what to build** (Deliverables + ACs), **how to get there** (Approach — initial direction, expect adjustment), **rules to follow** (Global Invariants + Process Guidance + Known Assumptions + Risks + Trade-offs). Every insight becomes an encoded criterion or is explicitly scoped out with stated reasoning. Automate verification — every AC and INV-G has a `verify:` block; criteria that genuinely require human action belong in Process Guidance or Known Assumptions, not as ACs.

**Output contract.** After writing, emit a plain-language Summary for Approval (no codes, no YAML, no schema vocabulary; reads like talking to a colleague). On approval, output `Manifest complete:` per `references/COMPLETE.md` — this line is the load-bearing handoff signal for `/auto`, `/do`, and Session-Default Detection. When the caller context is `/do`'s autonomous amendment path or the user signals "enough" / "ship it" / "good enough" mid-flow, finish autonomously without summary approval. Explicit `/do` invocation mid-flow → hand off without waiting.

**Pre-flight** resolves babysit (`--babysit <pr-url>` → `references/BABYSIT_MODE.md`) / amend (chat-derived amendment intent + Session-Default Detection of a prior `Manifest complete:` line → `references/AMENDMENT_MODE.md`; ambiguous-multiple-candidates → ask once) / fresh. **Domain Guidance** loads task-type files from `tasks/` per `tasks/README.md` composition rules. **Multi-repo** in `references/MULTI_REPO.md`. **Canvas** in `references/CANVAS_MODE.md`.

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
    prompt: "..."
    agent: "..."
    model: "..."
    phase: 1
  ```
````

**Verifier subagents return one of three states: PASS, FAIL, or BLOCKED.** PASS = criterion holds. FAIL = criterion violated, includes evidence and fix hint. BLOCKED = criterion can't be evaluated yet because of an external action / state pending (e.g., deploy hasn't happened, human approval pending) — `/do` routes BLOCKED via `/escalate`.

**Auto-decided items** carry an `(auto)` annotation immediately after the ID (e.g. `[INV-G2] (auto) Description: ...`). Same convention applies to AC-* and PG-* entries that were auto-decided. Each auto-decided item also appears in Known Assumptions with reasoning.

## ID Scheme

| Type | Format | Example |
|------|--------|---------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 |
| Process Guidance | PG-{N} | PG-1, PG-2 |
| Risk Area | R-{N} | R-1, R-2 |
| Trade-off | T-{N} | T-1, T-2 |
| Known Assumption | ASM-{N} | ASM-1, ASM-2 |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1, AC-2.3 |

## Flags

- `--babysit <pr-url>` — synthesize a lifecycle-only manifest from an existing PR. Routes to `references/BABYSIT_MODE.md`. Missing argument → halt with usage; inaccessible URL → halt naming the URL and the failure mode.
- `--canvas` — generate a Shared Understanding Canvas alongside the manifest (visual side-channel for chat-interview alignment). Routes to `references/CANVAS_MODE.md`.
- `--autonomous` — used internally by `/auto` chaining and `/do`'s amendment path; suppresses Summary for Approval wait and lets figure-out self-answer with recommended defaults.

PR-lifecycle composition is auto-detected from the local `origin` remote — `github.com` host adds the `github-pr-lifecycle` AC via `tasks/PR_LIFECYCLE.md`. Non-github remotes get no PR-lifecycle AC; user can add one manually if needed.
