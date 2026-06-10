---
name: auto
description: 'End-to-end autonomous execution: figure-out → define → do, chained without manual approval gates. Use when you want to define and execute without intervention during planning, when the user asks for autonomous or end-to-end work, says just build it, or asks to tend or babysit a PR.'
argument-hint: '[task] [--babysit <pr-url>]'
user-invocable: true
---

Chain `manifest-dev:figure-out --autonomous` (when the transcript lacks shared understanding) → `manifest-dev:define --autonomous` → `manifest-dev:do` on a single task. The `--autonomous` flag on figure-out makes the model self-answer with recommended answers instead of waiting on the user (see `figure-out/references/autonomous.md`). Surface define's Summary for Approval for visibility but don't wait — treat as approved and proceed to /do.

**Task text** comes from `$ARGUMENTS`; if empty, infer from conversation context (summarize the discussed task into a concrete description). Fresh session with no context and no args → halt: `No task description provided and no conversation context to infer from. Usage: /auto <task description> | /auto --babysit <pr-url>`.

**Babysit mode** (`--babysit <pr-url>`) skips fresh synthesis. Invoke `manifest-dev:define` with `--babysit <pr-url> --autonomous`, then /do. PR-lifecycle platform auto-detects from PR URL host (`github.com` → github composition); non-github host → halt. Multi-repo manifest produced by /define → single /do invocation navigates all repos.

**Failure handling.** /define returns no manifest path → stop, report. /do escalates (BLOCKED criterion or other blocker) → surface the escalation verbatim to the user with the action it requests.
