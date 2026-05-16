---
name: define
description: 'Experimental. Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and Approach. Auto-invokes /figure-out when the transcript lacks understanding. Use when planning features, scoping refactors, debugging complex issues, or whenever a task needs structured thinking before coding. Triggers: define, manifest, scope, plan, spec out, break down.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>] [--canvas]'
user-invocable: true
---

Encode the conversation's shared understanding as a Manifest at `<scratch>/manifest-{ts}.md` (writable scratch path appropriate to the harness — `$TMPDIR`, `%TEMP%`, etc.). If the transcript lacks shared understanding, invoke `manifest-dev-experimental:figure-out` first; propagate `--autonomous` when invoked from `/auto` or `/do`'s amendment path. **Pre-flight:** babysit (`--babysit <pr-url>` → `references/BABYSIT_MODE.md`); amend (args contain a manifest file path → see Amendment below); else fresh.

**Manifest shape.** Markdown with Intent (Goal, Mental Model); Approach (Architecture, Execution Order, `[R-N]` risks, `[T-N]` trade-offs) for complex tasks; Global Invariants `[INV-G{N}]` with `verify:` blocks; Process Guidance `[PG-{N}]` (non-verifiable HOW); Known Assumptions `[ASM-{N}]` (default + impact); Deliverables with Acceptance Criteria `[AC-{D}.{N}]` with `verify:` blocks. Auto-decided items carry `(auto)` + matching ASM. Every `verify:`:

```yaml
verify:
  prompt: "..."     # required, verbatim verifier instruction
  agent: "..."      # optional, default general-purpose
  model: "..."      # optional, default inherit
  phase: 1          # optional integer, default 1
```

Verifiers return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action — `/do` routes via `/escalate`). Automate verification — criteria that genuinely require human action belong in Process Guidance, not as ACs.

**Amendment.** A manifest path in `$ARGUMENTS` means amend. Read it fully, apply targeted changes only — preserve unaffected items verbatim. IDs are stable (modify in place; remove without renumbering). No `## Amendments` log — git is history. Autonomous when caller is `/auto` or `/do`; interactive otherwise.

**Flags.** `--babysit <pr-url>` synthesizes a lifecycle-only manifest from a PR (`references/BABYSIT_MODE.md`). `--canvas` generates a Shared Understanding Canvas alongside the manifest (`references/CANVAS_MODE.md`). `--autonomous` skips summary approval and lets figure-out self-answer. Multi-repo: `references/MULTI_REPO.md`. PR-lifecycle composition auto-detects from `origin` (`github.com`).

**Summary for Approval.** Before Complete, write a plain-language digest (plan / what / guardrails / how-verified) — no codes, no YAML, no schema vocab. **Test:** reads like talking to a colleague, not a compressed manifest. Approval → Complete; feedback → revise; `/do` → handoff; decline → exit silently. Skip the wait when caller is `/auto` or `/do` amendment, or the user signals "enough".

**Complete.** Emit the load-bearing handoff (`<manifest-path>` is the absolute path you wrote; `<dir>` is the project directory in slug form, e.g. `-home-user-manifest-dev`):

```text
Manifest complete: <manifest-path>
Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl

To execute: /do <manifest-path>
```
