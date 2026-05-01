---
name: auto
description: 'End-to-end autonomous execution: /define → auto-approve → /do in a single command. Infers task from conversation context when no arguments provided. Add --drive to continue through PR review lifecycle (or local-only loop). Use when you want to define and execute a task without manual intervention during planning. Triggers: auto, autonomous define and do, end-to-end, just build it.'
user-invocable: true
---

# /auto - End-to-End Autonomous Execution

## Goal

Chain `/define` and `/do` into a single autonomous flow. The full /define process runs — all coverage goals, all probing, all logging — the model answers its own questions instead of the user. After the manifest is built and verified, auto-approve and immediately launch /do.

## Input

`$ARGUMENTS` = task description (optional — inferred from conversation context if absent), optionally with `--mode efficient|balanced|thorough`, `--drive`, `--platform <platform>`, `--interval <duration>`, `--max-ticks <N>`, `--sink <sink>`, `--base <branch>`

If `--interview` is present in arguments: error and halt: "--interview is not supported by /auto. /auto always uses autonomous mode. Use /define for custom interview styles."

Parse flags from arguments if present:
- `--mode` will be passed to /do.
- `--drive` enables PR/loop lifecycle automation after /do completes.
- `--platform`, `--interval`, `--max-ticks`, `--sink`, `--base` are only used when `--drive` is present — passed to /drive.

The remaining text after flag extraction is the task description (`$TASK_DESCRIPTION`). If `$TASK_DESCRIPTION` is empty (no arguments provided, or only flags provided): infer the task from conversation context. Summarize the discussed task into a concrete task description and use that as `$TASK_DESCRIPTION`. If there is no conversation context (fresh session with just `/auto` and nothing else), error and halt: "No task description provided and no conversation context to infer from. Usage: /auto <task description> [--mode efficient|balanced|thorough] [--drive [--platform none|github] [--interval 15m] [--max-ticks 100] [--sink local] [--base <branch>]]"

## Flow

1. **Define** — Invoke the manifest-dev:define skill with: "$TASK_DESCRIPTION --interview autonomous"

2. **Auto-approve** — When /define presents the Summary for Approval, output the summary for user visibility but do not wait for user response. Treat the manifest as approved and proceed immediately. If the user is nevertheless asked for approval, proceed as if approved.

3. **Execute** — Note the manifest file path from /define's completion output. Invoke the manifest-dev:do skill with: "<manifest-path>" (append `--mode <level>` if --mode was specified in the original /auto arguments).

4. **Drive** (only when `--drive` is present) — After /do completes successfully (calls `/done`, not `/escalate`), invoke the manifest-dev:drive skill with: "<manifest-path>" plus the resolved drive flags. **Default `--platform`**: when the user passes `--drive` without `--platform`, /auto passes `--platform github` to /drive — /auto is end-to-end shipping, so the natural continuation is the GitHub PR lifecycle. Users who want a local-only drive loop pass `--drive --platform none` explicitly. Append `--interval`, `--max-ticks`, `--sink`, `--base` if they were specified in the original /auto arguments; otherwise let /drive use its own defaults.

   If /do escalates with **"Deferred-Auto Pending"**: this is a coordination handoff, not a blocker — the implementation is green; the user just needs to run `/verify --deferred` later when prerequisites are ready. Still invoke /drive for cwd's PR (per §Multi-Repo Behavior). Surface the deferred-auto reminder to the user alongside the PR link: "/auto: implementation green; /drive started for cwd's PR. Deferred-auto criteria pending — run `/verify <manifest-path> <log-path> --deferred` when prerequisites are in place to reach /done."

   If /do escalates with any other type: do NOT invoke /drive. Report to user: "/do escalated — skipping /drive. Reason: <escalation reason from /do>. Resolve the blocker and re-invoke /drive manually with the manifest path."

## Multi-Repo Behavior

If `/define` produces a multi-repo manifest (Intent declares `Repos:`), `/auto`'s `/do` invocation **navigates all repos** declared in `Repos:` — `/do` reads the path map and uses absolute paths natively (no filter logic). A single `/auto` invocation can therefore complete the whole multi-repo implementation phase.

The per-cwd limitation is `/drive`: with `--drive`, only cwd's PR is set up for tending, because `/drive` is PR-bound by construction. To tend other repos' PRs, invoke `/drive` from each other repo's cwd. See `manifest-dev:define/references/MULTI_REPO.md` §i.

## Failure Handling

If /define does not produce a manifest path, stop and report the failure. Do not invoke /do without a valid manifest.
