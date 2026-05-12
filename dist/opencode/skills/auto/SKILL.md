---
name: auto
description: 'End-to-end autonomous execution: /define → auto-approve → /do in a single command. Infers task from conversation context when no arguments provided. Add --babysit <pr-url> to tend an existing PR through review and CI without manifest-dev setup. Use when you want to define and execute a task without manual intervention during planning. Triggers: auto, autonomous define and do, end-to-end, just build it, tend pr, babysit pr.'
user-invocable: true
---

# /auto - End-to-End Autonomous Execution

## Goal

Chain `/define` and `/do` into a single autonomous flow. The full /define process runs — all coverage goals, all probing, all logging — the model answers its own questions instead of the user. After the manifest is built and verified, auto-approve and immediately launch /do.

Two entry modes:

- **Task mode** (default) — task description (or inferred from conversation context) feeds /define for a fresh manifest.
- **Babysit mode** — `--babysit <pr-url>` skips fresh-manifest synthesis; /define synthesizes a lifecycle-only manifest from the existing PR, then /do tends it to mergeable. Useful for PRs in repos that don't use manifest-dev.

## Input

`$ARGUMENTS` = task description (optional in task mode — inferred from conversation context if absent), optionally with `--mode efficient|balanced|thorough`, `--platform github|none`, `--babysit <pr-url>`

If `--interview` is present in arguments: error and halt: "--interview is not supported by /auto. /auto always uses autonomous mode. Use /define for custom interview styles."

Parse flags from arguments if present:

- `--mode` is passed to /do.
- `--platform` is passed to /define. When omitted, /define's own auto-detection applies (origin remote in task mode; PR URL host in babysit mode).
- `--babysit <pr-url>` triggers babysit mode — /define is invoked with `--babysit <pr-url>` and /do follows on the resulting lifecycle manifest.

### Babysit mode

When `--babysit <pr-url>` is set:

- Missing URL argument → halt: "--babysit requires a PR URL. Usage: /auto --babysit <pr-url>."
- `--babysit` + free-form task description in `$ARGUMENTS` → the babysit URL wins; the task description is ignored with a one-line log note (babysit's intent comes from the PR, not from $ARGUMENTS).
- **Platform inference from PR URL.** When `--platform` is not explicitly passed and `--babysit` is set, /auto derives platform from the PR URL host (`github.com` → `github`). This differs from /define's task-mode inference (which uses `origin` remote) because babysit's use case is repos that may not be locally cloned.
- **Conflict detection.** When both `--platform` and `--babysit` are passed and the platform disagrees with the URL host (e.g., `--platform github` with a non-github URL), halt: "--platform <value> disagrees with PR URL host <host>. Pass a matching platform or omit --platform to infer from the URL."

### Task mode (no babysit)

`$TASK_DESCRIPTION` = remaining text after flag extraction. If empty: infer the task from conversation context. Summarize the discussed task into a concrete task description and use that as `$TASK_DESCRIPTION`. If there is no conversation context (fresh session with just `/auto` and nothing else), error and halt: "No task description provided and no conversation context to infer from. Usage: /auto <task description> [--mode efficient|balanced|thorough] [--platform github|none] | /auto --babysit <pr-url> [--mode ...] [--platform github|none]"

## Flow

### Task mode

1. **Define** — Invoke the manifest-dev:define skill with: "$TASK_DESCRIPTION --interview autonomous" (append `--platform <value>` if --platform was specified).

2. **Auto-approve** — When /define presents the Summary for Approval, output the summary for user visibility but do not wait for user response. Treat the manifest as approved and proceed immediately. If the user is nevertheless asked for approval, proceed as if approved.

3. **Execute** — Note the manifest file path from /define's completion output. Invoke the manifest-dev:do skill with: "<manifest-path>" (append `--mode <level>` if --mode was specified in the original /auto arguments).

### Babysit mode

1. **Define (babysit)** — Invoke the manifest-dev:define skill with: "--babysit <pr-url> --interview autonomous --platform <resolved-platform>". The resolved platform is the explicit `--platform` if passed, otherwise inferred from the PR URL host.

2. **Auto-approve** — Same as task mode: surface the summary; proceed without waiting.

3. **Execute** — Invoke the manifest-dev:do skill with: "<manifest-path>" (append `--mode <level>` if specified).

## Multi-Repo Behavior

If `/define` produces a multi-repo manifest (Intent declares `Repos:`), `/auto`'s `/do` invocation **navigates all repos** declared in `Repos:` — `/do` reads the path map and uses absolute paths natively (no filter logic). A single `/auto` invocation can therefore complete the whole multi-repo implementation phase.

Babysit mode is single-PR by construction — it takes one PR URL. A user with a multi-repo changeset uses task-mode /auto with `Repos:` declared, not babysit.

See `manifest-dev:define/references/MULTI_REPO.md`.

## Failure Handling

If /define does not produce a manifest path, stop and report the failure. Do not invoke /do without a valid manifest.

If /do escalates with **"Deferred-Auto Pending"**: this is a coordination handoff, not a blocker — the implementation is green; the user just needs to run `/verify --deferred` later when prerequisites are ready. Surface the reminder: "/auto: implementation green. Deferred-auto criteria pending — run `/verify <manifest-path> <log-path> --deferred` when prerequisites are in place to reach /done."

If /do escalates with any other type: report to user with the escalation reason. The user resolves and re-invokes /do (or /auto) as appropriate.
