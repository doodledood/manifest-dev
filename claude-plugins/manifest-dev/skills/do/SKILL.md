---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass.'
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapting when reality diverges), then verify everything passes (including Global Invariants).

**Why quality execution matters**: The manifest front-loaded the thinking—criteria are already defined. Your job is implementation that passes verification on first attempt. Every verification failure is rework.

## Input

`$ARGUMENTS` = manifest file path (REQUIRED), optionally with execution log path

If no arguments: Output error "Usage: /do <manifest-file-path> [log-file-path]"

## Existing Execution Log

If input includes a log file path (iteration on previous work): **treat it as source of truth**. It contains prior execution history. Continue from where it left off—append to the same log, don't restart.

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Work toward acceptance criteria however makes sense. Manifest says WHAT, you decide HOW. |
| **Approach is initial, not rigid** | Approach provides starting direction, but plans break when hitting reality. Adapt freely when you discover better patterns, unexpected constraints, or dependencies that don't work as expected. Log adjustments with rationale. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart. Don't touch passing criteria. |
| **Verify fixes first** | After fixing a failure, confirm the fix works before re-running full verification. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Log adjustments with rationale. |

## Constraints

**Log after every action** - Write to execution log immediately after each AC attempt. No exceptions. This is disaster recovery—if context is lost, the log is the only record of what happened.

**Must call /verify** - Can't declare done without verification. Invoke manifest-dev:verify with manifest and log paths.

**Escalation boundary** - Escalate when: (1) ACs can't be met as written (contract broken), or (2) user requests a pause mid-workflow. If ACs remain achievable and no user interrupt, continue autonomously.

**Stop requires /escalate** - During /do, you cannot stop without calling /verify→/done or /escalate. If you need to pause (user requested, waiting on external action), call /escalate with "User-Requested Pause" format. Short outputs like "Done." or "Waiting." will be blocked.

**Refresh before verify** - Read full execution log before calling /verify to restore context.

## Memento Pattern

Externalize progress to survive context loss. The log IS the disaster recovery mechanism.

**Execution log**: Create `/tmp/do-log-{timestamp}.md` at start. After EACH AC attempt, append what happened and the outcome. Goal: another agent reading only the log could resume work.

**Todos**: Create from manifest (deliverables → ACs). Start with execution order from Approach (adjust if dependencies require). Update todo status after logging (log first, todo second).

## Collaboration Mode

When `$ARGUMENTS` contains a `COLLAB_CONTEXT:` block, execution logging and escalation run through Slack in addition to local files. If no `COLLAB_CONTEXT:` block is present, ignore this section entirely — all other sections apply as written.

### COLLAB_CONTEXT Format

```
COLLAB_CONTEXT:
  channel_id: <slack-channel-id>
  owner_handle: <@owner>
  poll_interval: <seconds, default 60>
  threads:
    execution: <thread-ts>
    verification: <thread-ts>
    stakeholders:
      <@handle>: <thread-ts>
  stakeholders:
    - handle: <@handle>
      name: <display-name>
      role: <role/expertise>
```

### Overrides When Active

**Execution log → dual-write.** Write to `/tmp/do-log-{timestamp}.md` as normal (needed by /verify, /escalate, and "Refresh before verify"). Additionally, post each AC attempt outcome as a thread reply to `threads.execution` — the Slack thread is the stakeholder-visible mirror. Both destinations get the same content.

**Escalation → Slack MCP tools.** Do NOT use AskUserQuestion for escalations. When escalating (ACs can't be met, or need owner decision), use Slack MCP tools to post the escalation to the main channel (`channel_id`) as a new message, tagging the owner with `owner_handle`. Include: what's blocked, what was tried, options for resolution. Poll at `poll_interval` for the owner's response. Continue after they respond.

**Verification results → dual-write.** After /verify completes, post results as thread replies to `threads.verification`. Include pass/fail status for each criterion.

**Todos remain local.** The Todos mechanism (create from manifest, update status after logging) continues to work locally as written. Todos are working memory, not stakeholder-visible artifacts.

**Everything else unchanged.** All Principles, other Constraints, the Memento Pattern, and the /verify→/done or /escalate requirement apply exactly as written. Only the escalation channel changes; all outputs are dual-written to both local files and Slack.
