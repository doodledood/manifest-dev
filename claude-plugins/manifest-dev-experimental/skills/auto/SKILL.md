---
name: auto
description: 'End-to-end autonomous execution: figure-out (when needed) → define → do, chained without manual approval gates. Add --babysit <pr-url> to tend an existing PR through review and CI without a fresh manifest. Use when you want to define and execute without intervention during planning. Triggers: auto, autonomous, end-to-end, just build it, tend pr, babysit pr.'
user-invocable: true
---

Chain figure-out, define, and do autonomously on a single task. When `/define` presents its Summary for Approval, surface it for visibility but don't wait — treat as approved, immediately proceed to `/do`.

**Input.** `$ARGUMENTS` = task description (optional in task mode), optionally with `--platform github|none`, `--babysit <pr-url>`, `--canvas`. Other unsupported flags pass through to `/define`. (Note: `--interview` and `--mode` are not supported in experimental — there's one mode.)

**Task mode (default).** Task text comes from `$ARGUMENTS`. If empty, infer from conversation context — summarize the discussed task into a concrete description. Fresh session with no context and no `$ARGUMENTS` → halt: `No task description provided and no conversation context to infer from. Usage: /auto <task description> [--platform ...] | /auto --babysit <pr-url> [--platform ...]`.

Flow:
1. If conversation lacks figure-out understanding for this task, invoke `manifest-dev-experimental:figure-out` to build shared understanding first.
2. Invoke `manifest-dev-experimental:define` with `<task>` (append `--platform <value>` and/or `--canvas` if passed). When define presents its Summary for Approval, surface it for visibility but do not wait — treat as approved, proceed immediately.
3. When define emits its Summary for Approval, surface it; do not wait.
4. Note the manifest path from define's completion output. Invoke `manifest-dev-experimental:do` with `<manifest-path>`.

**Babysit mode.** `--babysit <pr-url>` skips fresh-manifest synthesis. Flow:
1. Missing PR URL → halt: `--babysit requires a PR URL. Usage: /auto --babysit <pr-url> [--platform ...]`
2. `--babysit` + free-form task text in `$ARGUMENTS` → URL wins; task text logged and ignored.
3. Platform inference: when `--platform` not explicit, derive from PR URL host (`github.com` → `github`). Babysit's use case is repos that may not be locally cloned.
4. Conflict — `--platform <X>` disagrees with PR URL host → halt: `--platform <X> disagrees with PR URL host <host>. Pass a matching platform or omit --platform to infer from URL.`
5. Invoke `manifest-dev-experimental:define` with `--babysit <pr-url> --platform <resolved>`. Auto-approve the summary as in task mode.
6. Surface define's summary; don't wait.
7. Invoke `manifest-dev-experimental:do` with the manifest path.

**Multi-repo.** If define produces a manifest with `Repos:`, the single `/do` invocation navigates all repos declared in the path map.

**Failure handling.** /define returns no manifest path → stop and report; do not invoke /do without a valid manifest. /do escalates "Deferred-Auto Pending" → surface reminder: implementation green, run `/verify <manifest> <log> --deferred` when prerequisites are ready. Any other /do escalation → report to user with the escalation reason.
