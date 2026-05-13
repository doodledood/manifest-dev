---
name: auto
description: 'Experimental. End-to-end autonomous execution: figure-out (when needed) → define → do, chained without manual approval gates. Add --babysit <pr-url> to tend an existing PR through review and CI. Use when you want to define and execute without intervention during planning. Triggers: auto, autonomous, end-to-end, just build it, tend pr, babysit pr.'
user-invocable: true
---

Chain `manifest-dev-experimental:figure-out --autonomous` (when the transcript lacks shared understanding) → `manifest-dev-experimental:define --autonomous` → `manifest-dev-experimental:do` on a single task. The `--autonomous` flag on figure-out makes the model self-answer with recommended answers instead of waiting on the user (see `figure-out/references/autonomous.md`). Surface define's Summary for Approval for visibility but don't wait — treat as approved and proceed to /do.

**Task text** comes from `$ARGUMENTS`; if empty, infer from conversation context (summarize the discussed task into a concrete description). Fresh session with no context and no args → halt: `No task description provided and no conversation context to infer from. Usage: /auto <task description> [--platform ...] [--canvas] | /auto --babysit <pr-url> [--platform ...]`. `--interview` and `--mode` are not accepted (experimental has one mode); `--canvas` passes through to /define.

**Babysit mode** (`--babysit <pr-url>`) skips fresh synthesis. Invoke `manifest-dev-experimental:define` with `--babysit <pr-url> --autonomous --platform <resolved>`, then /do. Platform: explicit `--platform` wins; otherwise inferred from PR URL host (`github.com` → `github`); host conflict with explicit platform → halt; missing URL → halt with usage; free-form task text + URL → URL wins, task text noted and ignored. Multi-repo manifest produced by /define → single /do invocation navigates all repos.

**Failure handling.** /define returns no manifest path → stop, report. /do escalates "Deferred-Auto Pending" → surface reminder: implementation green, signal readiness in chat (e.g., "all deployed") and re-invoke /verify when prerequisites are ready. Any other /do escalation → report to user with reason.
