---
name: auto
description: 'End-to-end autonomous execution: figure-out → define → do, chained without manual approval gates. Use when you want to define and execute without intervention during planning, when the user asks for autonomous or end-to-end work, or asks to tend or babysit a PR.'
argument-hint: '[task] [--babysit <pr-url>] [--verification per-gate|consolidated|self] [--verifier-model <model>]'
user-invocable: true
---

Chain `figure-out --autonomous` (when the transcript lacks shared understanding) → `define --autonomous` → `do` on a single task. The `--autonomous` flag on figure-out makes the model self-answer with recommended answers instead of waiting on the user (see `figure-out/references/autonomous.md`). Surface define's Summary for Approval for visibility, then treat it as approved and proceed to /do.

**Task text** comes from `$ARGUMENTS`; if empty, infer from conversation context (summarize the discussed task into a concrete description). Fresh session with no context and no args → halt: `No task description provided and no conversation context to infer from. Usage: /auto <task description> | /auto --babysit <pr-url>`.

**Verification policy.** Parse only top-level option uses of `--verification` and `--verifier-model` as `/auto` flags; quoted or topic mentions remain task text. Omitted `--verification` means `per-gate`. After resolving that default, load the matching sibling `/do` reference under `../do/references/` and apply its policy validation before `/define`; the reference, not `/auto`, owns mode-specific model support and evidence provenance. Remove parsed flags from the task before `/define`, and forward them only to `/do`. Never write either option into the Manifest. Use the reference's required evidence/provenance wording when recording each gate's provenance in the ledger.

**Babysit mode** (`--babysit <pr-url>`) skips fresh synthesis. Invoke `define` with `--babysit <pr-url> --autonomous`, then /do with the parsed verification options. PR-lifecycle platform auto-detects from PR URL host (`github.com` → github composition); non-github host → halt. Multi-repo manifest produced by /define → single /do invocation navigates all repos.

**Failure handling.** /define returns no manifest path → stop, report. /do escalates (BLOCKED criterion or other blocker) → surface the escalation verbatim to the user with the action it requests.

**Continuation.** Do not set or print a continuation goal during understanding or definition. When invoking figure-out, keep its full Read bar as the checkpoint before define, without a phase goal. Pass the exact Manifest path define reports to /do; /do owns the completion backstop, including native goal-setting and the manual completion contract. No path → stop and report. Automatic continuation begins at execution; an interrupted earlier phase must be restarted by the caller.
