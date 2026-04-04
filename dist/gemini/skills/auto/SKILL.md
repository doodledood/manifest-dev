---
name: auto
description: 'End-to-end autonomous execution: /define → auto-approve → /do in a single command. Infers task from conversation context when no arguments provided. Add --tend-pr to continue through PR review lifecycle. Use when you want to define and execute a task without manual intervention during planning. Triggers: auto, autonomous define and do, end-to-end, just build it.'
user-invocable: true
---

# /auto - End-to-End Autonomous Execution

## Goal

Chain `/define` and `/do` into a single autonomous flow. The full /define process runs — all coverage goals, all probing, all logging — the model answers its own questions instead of the user. After the manifest is built and verified, auto-approve and immediately launch /do.

## Input

`$ARGUMENTS` = task description (optional — inferred from conversation context if absent), optionally with `--mode efficient|balanced|thorough`, `--tend-pr`, `--platform <platform>`, `--interval <duration>`, `--reviewers <usernames>`

If `--interview` is present in arguments: error and halt: "--interview is not supported by /auto. /auto always uses autonomous mode. Use /define for custom interview styles."

Parse flags from arguments if present:
- `--mode` will be passed to /do.
- `--tend-pr` enables PR lifecycle automation after /do completes.
- `--platform`, `--interval`, and `--reviewers` are only used when `--tend-pr` is present — passed to /tend-pr.

The remaining text after flag extraction is the task description (`$TASK_DESCRIPTION`). If `$TASK_DESCRIPTION` is empty (no arguments provided, or only flags provided): infer the task from conversation context. Summarize the discussed task into a concrete task description and use that as `$TASK_DESCRIPTION`. If there is no conversation context (fresh session with just `/auto` and nothing else), error and halt: "No task description provided and no conversation context to infer from. Usage: /auto <task description> [--mode efficient|balanced|thorough] [--tend-pr [--platform github] [--interval 10m]]"

## Flow

1. **Define** — Invoke the manifest-dev:define skill with: "$TASK_DESCRIPTION --interview autonomous"

2. **Auto-approve** — When /define presents the Summary for Approval, output the summary for user visibility but do not wait for user response. Treat the manifest as approved and proceed immediately. If the user is nevertheless asked for approval, proceed as if approved.

3. **Execute** — Note the manifest file path from /define's completion output. Invoke the manifest-dev:do skill with: "<manifest-path>" (append `--mode <level>` if --mode was specified in the original /auto arguments).

4. **Tend PR** (only when `--tend-pr` is present) — After /do completes successfully (calls `/done`, not `/escalate`), invoke the manifest-dev:tend-pr skill with: "<manifest-path> --log <execution-log-path>" (the execution log path is available from the conversation context — /do logged its creation at the start of execution). Append `--platform <platform>`, `--interval <duration>`, and `--reviewers <usernames>` if specified in the original /auto arguments.

   If /do escalates instead of completing: do NOT invoke /tend-pr. Report to user: "/do escalated — skipping /tend-pr. Reason: <escalation reason from /do>. Resolve the blocker and re-invoke /tend-pr manually with the manifest path."

## Failure Handling

If /define does not produce a manifest path, stop and report the failure. Do not invoke /do without a valid manifest.
