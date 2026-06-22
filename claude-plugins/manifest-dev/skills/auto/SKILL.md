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

**Unattended launch.** At the start of a standalone run, before chaining, print the copy-pasteable full-chain backstop below so the user can relaunch under it — its argument is the full-chain completion condition, so the host's fresh-model evaluator re-opens the turn until the whole chain finishes, not just the first phase. `/auto` owns this goal as the chain entrypoint, so figure-out suppresses its own nested `/goal` print when it can see it's under `/auto`:
`/goal Run /auto <task> until the figure-out Read is named, the manifest is written, and /do reports /done with every Acceptance Criterion and Global Invariant PASS; don't stop while any phase is incomplete. Clear all fog you can without me — investigate to the truth rather than guessing, since trustworthiness outranks speed — recording an assumption only for what genuinely needs me, and halting only for a blocker that truly requires my input. Stop after N turns if it stalls.`
