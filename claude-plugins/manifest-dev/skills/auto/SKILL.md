---
name: auto
description: 'End-to-end autonomous execution: /define → auto-approve → /do in a single command. Use when you want to define and execute a task without manual intervention during planning. Triggers: auto, autonomous define and do, end-to-end, just build it.'
user-invocable: true
---

# /auto - End-to-End Autonomous Execution

## Goal

Chain `/define` and `/do` into a single autonomous flow. The full /define process runs — all protocols, all probing, all logging — the model answers its own questions instead of the user. After the manifest is built and verified, auto-approve and immediately launch /do.

## Input

`$ARGUMENTS` = task description (REQUIRED), optionally with `--mode efficient|balanced|thorough`

If `--interview` is present in arguments: error and halt: "--interview is not supported by /auto. /auto always uses autonomous mode. Use /define for custom interview styles."

If no arguments provided: error and halt: "Usage: /auto <task description> [--mode efficient|balanced|thorough]"

Parse `--mode` from arguments if present. `--mode` will be passed to /do. The remaining text after flag extraction is the task description.

## Flow

1. **Define** — Invoke the manifest-dev:define skill with: "$TASK_DESCRIPTION --interview autonomous"

2. **Auto-approve** — When /define presents the Summary for Approval, output the summary for user visibility but do not wait for user response. Treat the manifest as approved and proceed immediately. If the user is nevertheless asked for approval, proceed as if approved.

3. **Execute** — Note the manifest file path from /define's completion output. Invoke the manifest-dev:do skill with: "<manifest-path>" (append `--mode <level>` if --mode was specified in the original /auto arguments).

## Failure Handling

If /define does not produce a manifest path, stop and report the failure. Do not invoke /do without a valid manifest.
