---
name: define
description: 'Experimental. Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and Approach. Auto-invokes /figure-out when the transcript lacks understanding. Use when planning features, scoping refactors, debugging complex issues, or whenever a task needs structured thinking before coding. Triggers: define, manifest, scope, plan, spec out, break down.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>] [--canvas]'
user-invocable: true
---

Take the conversation's shared understanding and encode it as a Manifest at `<scratch>/manifest-{ts}.md` — pick a writable scratch directory appropriate to the harness (`$TMPDIR`, `%TEMP%`, or equivalent). If the transcript lacks shared understanding, invoke `manifest-dev-experimental:figure-out` first ("no prior understanding detected — probing first"); when invoked from `/auto` or with `--autonomous`, propagate the flag so figure-out self-answers without user wait.

The manifest captures **what to build** (Deliverables + ACs), **how to get there** (Approach — initial direction, expect adjustment), **rules to follow** (Global Invariants + Process Guidance + Known Assumptions + Risks + Trade-offs). Every insight becomes an encoded criterion or is explicitly scoped out with stated reasoning. Automate verification — every AC and INV-G has a `verify:` block; criteria that genuinely require human action belong in Process Guidance or Known Assumptions, not as ACs.

**Pre-flight:** babysit (`--babysit <pr-url>` → `references/BABYSIT_MODE.md`); amend (args contain a manifest file path — any `.md` file path pointing to a previously-emitted manifest → apply the Amendment paragraph below); else fresh. **Domain Guidance** loads task-type files from `tasks/` per `tasks/README.md` composition rules. **Multi-repo** in `references/MULTI_REPO.md`. **Canvas** in `references/CANVAS_MODE.md`.

## Amendment

When `$ARGUMENTS` contains a manifest file path (any path to a previously-emitted manifest), you're amending that manifest. Read it fully first, then apply targeted changes — modify, add, or remove only the specific items the request names. Preserve everything else verbatim. IDs are stable: modifying INV-G1 keeps it as INV-G1 with new content; removing one drops it without renumbering the rest. The manifest reads as current state; git carries the history — no `## Amendments` log, no `INV-G1.1 amends INV-G1` chain. Autonomous (no summary wait, finish in place) when caller chain includes `/auto` or `/do`; interactive (full Summary for Approval flow) otherwise.

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

## Summary for Approval

Before emitting `Manifest complete:`, digest the manifest into a scannable summary the user can approve at a glance. Plain language. **No manifest codes** (D1, AC-1.1, INV-G3), **no YAML blocks**, **no structured-document vocabulary** ("acceptance criteria", "global invariants"). Default shape:

- **The plan** — one-line headline of what's being done and why.
- **What I'll build** — work items grouped naturally; don't enumerate every sub-task.
- **Guardrails** — invariants as plain rules.
- **How I'll verify** — brief description of verification approach.

Include an ASCII architecture diagram when the task has multiple components with inter-component flow.

**Test:** if it reads like a compressed manifest (codes, YAML, structured labels dressed up as prose; enumerated criteria; abstractions hiding content), rewrite. If it reads like something you'd say to a colleague, it's right.

After presenting, wait for the user's response:
- *Approval* ("looks good", "approved") → proceed to Complete.
- *Feedback* ("also add X", "change Y") → revise manifest, re-present summary. Do not implement.
- *Explicit /do invocation* → /define is done; /do takes over.
- *Decline* ("scrap this", "cancel") → exit silently without writing the manifest.

## Complete

Output the manifest path and stop. Use the actual path you wrote the manifest to (a writable scratch directory appropriate to the harness). Substitute placeholders before printing:
- `<manifest-path>` → the absolute path you wrote the manifest to (e.g., `$TMPDIR/manifest-{ts}.md`, `%TEMP%\manifest-{ts}.md`, `~/.cache/manifest-dev/manifest-{ts}.md` — whatever the harness's writable scratch is).
- `<dir>` → the current project directory in slug form (path separators → `-`, e.g., `-home-user-manifest-dev` for `/home/user/manifest-dev`).
- `${CLAUDE_SESSION_ID}` → the env value.

```text
Manifest complete: <manifest-path>
Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl

To execute: /do <manifest-path>
```

The `Manifest complete:` line is the load-bearing handoff signal for `/auto` and `/do` — they consume the actual path from this line, never from a prescribed directory. When the caller context is `/do`'s autonomous amendment path or the user signals "enough" / "ship it" / "good enough" mid-flow, finish autonomously — skip the Summary for Approval wait and emit Complete directly. Explicit `/do` invocation mid-flow → hand off without waiting.
