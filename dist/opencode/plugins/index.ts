/**
 * manifest-dev plugin for OpenCode CLI
 *
 * Complete OpenCode hook implementation adapted from the Claude Code
 * workflow hooks in claude-plugins/manifest-dev/hooks/.
 *
 * Version: 0.74.0
 *
 * Source hooks → OpenCode events:
 *   stop_do_hook.py         → session.idle (event — CANNOT block, see notes)
 *   pretool_verify_hook.py  → tool.execute.before (task tool, verify skill)
 *   post_compact_hook.py    → experimental.session.compacting
 *   prompt_submit_hook.py   → experimental.chat.system.transform
 *   posttool_log_hook.py    → tool.execute.after
 *
 * Corrected for OpenCode v1.2.15 (March 2026):
 *   - Blocking: throw new Error("reason"), NOT args.abort
 *   - Context injection: experimental.chat.system.transform (push to output.system[])
 *   - Compaction: experimental.session.compacting with output.context.push()
 *   - session.idle: fire-and-forget, CANNOT prevent stopping
 *   - Subagent bypass: tool.execute.before/after does NOT fire for subagent tool calls (#5894)
 *
 * Plugin input context:
 *   ctx.client     — SDK client (HTTP to localhost:4096)
 *   ctx.project    — { id, worktree, vcs }
 *   ctx.directory  — current working directory
 *   ctx.worktree   — git worktree root
 *   ctx.serverUrl  — server URL
 *   ctx.$          — Bun shell API
 */

import type { Plugin } from "@opencode-ai/plugin"

/**
 * Workflow state tracked across the session.
 * Replaces Claude Code's transcript parsing (hook_utils.parse_do_flow).
 * Reset on each new /do invocation.
 */
interface DoFlowState {
  hasDo: boolean
  hasDone: boolean
  hasEscalate: boolean
  hasSelfAmendment: boolean
  hasVerify: boolean
  doArgs: string | null
  hasCollabMode: boolean
}

// -- Verify context reminder (pretool_verify_hook.py) --

const VERIFY_CONTEXT_REMINDER = `VERIFICATION CONTEXT CHECK: You are about to run /verify.

Arguments: {verify_args}

BEFORE spawning verifiers, read the manifest and execution log in FULL if not recently loaded. You need ALL acceptance criteria (AC-*) and global invariants (INV-G*) in context to spawn the correct verifiers.`

const VERIFY_CONTEXT_REMINDER_MINIMAL = `VERIFICATION CONTEXT CHECK: You are about to run /verify.

BEFORE spawning verifiers, read the manifest and execution log in FULL if not recently loaded. You need ALL acceptance criteria (AC-*) and global invariants (INV-G*) in context to spawn the correct verifiers.`

// -- Post-compact recovery (post_compact_hook.py) --

const DO_WORKFLOW_RECOVERY_REMINDER = `This session was compacted during an active /do workflow. Context may have been lost.

CRITICAL: Before continuing, read the manifest and execution log in FULL.

The /do was invoked with: {do_args}

1. Read the manifest file - contains deliverables, acceptance criteria, and approach
2. Check /tmp/ for your execution log (do-log-*.md) and read it to recover progress

Do not restart completed work. Resume from where you left off.`

const DO_WORKFLOW_RECOVERY_FALLBACK = `This session was compacted during an active /do workflow. Context may have been lost.

CRITICAL: Before continuing, recover your workflow context:

1. Check /tmp/ for execution logs matching do-log-*.md
2. The log references the manifest file path - read both in FULL

Do not restart completed work. Resume from where you left off.`

// -- Amendment check (prompt_submit_hook.py) --

const AMENDMENT_CHECK_REMINDER = `AMENDMENT CHECK: You are in an active /do workflow and the user just submitted input.

Before continuing execution, check if this user input:
1. **Contradicts** an existing AC, INV, or PG in the manifest
2. **Extends** the manifest with new requirements not currently covered
3. **Amends** the scope or approach in a way that changes what "done" means

If YES to any: Call /escalate with Self-Amendment type, then immediately invoke /define --amend <manifest-path>. After /define returns, resume /do with the updated manifest.

If NO (clarification, confirmation, or unrelated): Continue execution normally.`

// -- Log reminder (posttool_log_hook.py) --

const LOG_REMINDER = `LOG REMINDER: A milestone just completed during /do.

Tool: {tool_detail}

Update the execution log NOW with what just happened, decisions made, and outcomes. The log is disaster recovery — if context is lost, only the log survives.`

// -- Stop enforcement messages (stop_do_hook.py) --

const STOP_BLOCKED_MESSAGE = `Stop blocked: /do workflow requires formal exit. Options: (1) Run /verify to check criteria - if all pass, /verify calls /done. (2) Call /escalate - for blocking issues OR user-requested pauses. Short outputs will be blocked. Choose one.`

const SELF_AMENDMENT_BLOCKED_MESSAGE = `Stop blocked: Self-Amendment escalation requires /define --amend before stopping. Invoke /define --amend <manifest-path> to update the manifest, then resume /do.`

// -- Workflow skill names that trigger log reminders --

const WORKFLOW_SKILLS = new Set(["verify", "escalate", "done", "define"])

export const ManifestDevPlugin: Plugin = async (ctx) => {
  // Session-scoped workflow state. Reset on each new /do invocation.
  const flowState: DoFlowState = {
    hasDo: false,
    hasDone: false,
    hasEscalate: false,
    hasSelfAmendment: false,
    hasVerify: false,
    doArgs: null,
    hasCollabMode: false,
  }

  // Track consecutive short outputs for loop detection (stop_do_hook.py)
  let consecutiveShortOutputs = 0

  // Pending verify reminder to inject via system transform
  let pendingVerifyReminder: string | null = null

  /**
   * Check if a tool call targets a specific skill.
   * Matches both "skill-name" and "plugin:skill-name" formats.
   * OpenCode uses "task" tool for subagent/skill spawning.
   */
  function isSkillCall(tool: string, args: any, skillName: string): boolean {
    if (tool !== "skill" && tool !== "task") return false
    const name: string = args?.name ?? args?.skill ?? ""
    return name === skillName || name.endsWith(`:${skillName}`)
  }

  /**
   * Get the base skill name from tool args.
   */
  function getSkillBaseName(args: any): string | null {
    const name: string = args?.name ?? args?.skill ?? ""
    if (!name) return null
    return name.includes(":") ? name.split(":").pop()! : name
  }

  return {
    // ---------------------------------------------------------------
    // tool.execute.before — Replaces pretool_verify_hook.py
    //
    // When /verify is about to be called, prepare a context reminder.
    // Also tracks /do, /done, /escalate, /verify invocations for
    // workflow state.
    //
    // BLOCKING: throw new Error("reason") — error message becomes
    //   the tool result seen by the LLM.
    // LIMITATION: Does NOT fire for subagent tool calls (issue #5894).
    // ---------------------------------------------------------------
    "tool.execute.before": async ({ tool, sessionID, callID }, { args }) => {
      // --- Workflow state tracking ---

      // Track /do invocations (resets state)
      if (isSkillCall(tool, args.args, "do")) {
        flowState.hasDo = true
        flowState.hasDone = false
        flowState.hasEscalate = false
        flowState.hasSelfAmendment = false
        flowState.hasVerify = false
        const doArgs = (args.args as any)?.args?.trim?.() || null
        flowState.doArgs = doArgs
        flowState.hasCollabMode = doArgs
          ? /--medium\s+(?!local(?:\s|$))\S+/.test(doArgs)
          : false
        consecutiveShortOutputs = 0
      }

      // Track /done, /escalate, /verify after /do
      if (flowState.hasDo) {
        if (isSkillCall(tool, args.args, "done")) {
          flowState.hasDone = true
        }
        if (isSkillCall(tool, args.args, "escalate")) {
          flowState.hasEscalate = true
          const escArgs: string = (args.args as any)?.args ?? ""
          if (escArgs.toLowerCase().includes("self-amendment")) {
            flowState.hasSelfAmendment = true
          }
        }
        if (isSkillCall(tool, args.args, "verify")) {
          flowState.hasVerify = true

          // Prepare verify context reminder for system transform injection
          const verifyArgs: string = (args.args as any)?.args?.trim?.() ?? ""
          pendingVerifyReminder = verifyArgs
            ? VERIFY_CONTEXT_REMINDER.replace("{verify_args}", verifyArgs)
            : VERIFY_CONTEXT_REMINDER_MINIMAL
        }
      }
    },

    // ---------------------------------------------------------------
    // tool.execute.after — Replaces posttool_log_hook.py
    //
    // After milestone tool calls during /do, append a log reminder
    // to the tool output. Targets:
    //   - todowrite (TaskCreate/TaskUpdate equivalents)
    //   - task/skill calls for workflow skills (verify, escalate, done, define)
    //
    // Also tracks output length for loop detection (stop_do_hook.py).
    //
    // LIMITATION: Does NOT fire for subagent tool calls (issue #5894).
    // ---------------------------------------------------------------
    "tool.execute.after": async (
      { tool, sessionID, callID, args },
      { title, output, metadata }
    ) => {
      // Track output length for loop detection
      const outputStr =
        typeof output.output === "string"
          ? output.output
          : JSON.stringify(output.output ?? "")
      if (outputStr.length < 100) {
        consecutiveShortOutputs++
      } else {
        consecutiveShortOutputs = 0
      }

      // Only inject log reminders during active /do
      if (!flowState.hasDo || flowState.hasDone) return

      let shouldRemind = false
      let toolDetail = tool

      // TodoWrite milestones (task management)
      if (tool === "todowrite") {
        shouldRemind = true
      }

      // Workflow skill calls
      if (tool === "task" || tool === "skill") {
        const skillName = getSkillBaseName(args)
        if (skillName && WORKFLOW_SKILLS.has(skillName)) {
          shouldRemind = true
          toolDetail = `${tool} (skill: ${skillName})`
        }
      }

      if (shouldRemind) {
        const reminder = LOG_REMINDER.replace("{tool_detail}", toolDetail)
        // Mutate output to append the reminder
        if (typeof output.output === "string") {
          output.output += `\n\n<system-reminder>${reminder}</system-reminder>`
        }
      }
    },

    // ---------------------------------------------------------------
    // experimental.chat.system.transform — Replaces prompt_submit_hook.py
    // and pretool_verify_hook.py (context injection part)
    //
    // Called before every LLM request. During active /do workflow:
    //   1. Injects amendment check reminder (prompt_submit_hook)
    //   2. Injects verify context reminder if pending (pretool_verify_hook)
    //
    // NOTE: This replaces Claude Code's UserPromptSubmit additionalContext
    // and PreToolUse additionalContext patterns.
    // ---------------------------------------------------------------
    "experimental.chat.system.transform": async (
      { sessionID, model },
      output
    ) => {
      if (!flowState.hasDo || flowState.hasDone) return

      // Amendment check reminder (prompt_submit_hook.py)
      output.system.push(AMENDMENT_CHECK_REMINDER)

      // Verify context reminder if pending (pretool_verify_hook.py)
      if (pendingVerifyReminder) {
        output.system.push(pendingVerifyReminder)
        pendingVerifyReminder = null
      }

      // Active /do enforcement context (stop_do_hook.py — soft enforcement)
      if (!flowState.hasEscalate) {
        output.system.push(
          "ACTIVE DO WORKFLOW: You must complete this workflow by running " +
            "/verify (which calls /done on success) or /escalate before " +
            "stopping. Do not attempt to end the session without one of these."
        )
      }
    },

    // ---------------------------------------------------------------
    // experimental.session.compacting — Replaces post_compact_hook.py
    //
    // When session compacts during active /do, inject recovery context
    // so the agent re-reads manifest and execution log.
    //
    // NOTE: This event is experimental and may change between releases.
    // ---------------------------------------------------------------
    "experimental.session.compacting": async ({ sessionID }, output) => {
      if (!flowState.hasDo) return
      if (flowState.hasDone || flowState.hasEscalate) return

      const reminder = flowState.doArgs
        ? DO_WORKFLOW_RECOVERY_REMINDER.replace("{do_args}", flowState.doArgs)
        : DO_WORKFLOW_RECOVERY_FALLBACK

      output.context.push(reminder)
    },

    // ---------------------------------------------------------------
    // Event handler — Replaces stop_do_hook.py (partially)
    //
    // session.idle: Session stopped. CANNOT prevent stopping — this is
    //   fire-and-forget. Workaround: ctx.client.session.prompt() to
    //   inject a follow-up message. FRAGILE: race condition in `run`
    //   mode (issue #15267). Feature request: issue #12472.
    //
    // todo.updated: Tracks workflow progress via todo state changes.
    //
    // Decision matrix (from stop_do_hook.py):
    //   - No /do active: do nothing
    //   - /do + /done: do nothing (properly completed)
    //   - /do + /escalate (non-self-amendment): do nothing
    //   - /do + self-amendment: attempt re-engage
    //   - /do + /verify + non-local medium: do nothing (posted externally)
    //   - /do without exit: attempt re-engage
    //   - 3+ consecutive short outputs (loop): do nothing (break loop)
    // ---------------------------------------------------------------
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        const sessionID = (event.properties as any)?.sessionID as
          | string
          | undefined
        if (!sessionID) return
        if (!flowState.hasDo) return

        // Properly completed
        if (flowState.hasDone) return

        // Properly escalated (non-self-amendment)
        if (flowState.hasEscalate && !flowState.hasSelfAmendment) return

        // Non-local medium with verify done — escalation posted externally
        if (flowState.hasCollabMode && flowState.hasVerify) return

        // Loop detection — allow stop to break infinite loop
        if (consecutiveShortOutputs >= 3) {
          console.warn(
            "[manifest-dev] WARNING: Stop allowed to break infinite loop. " +
              "The /do workflow was NOT properly completed. " +
              "Next time, call /escalate when blocked instead of minimal outputs."
          )
          return
        }

        // Attempt to re-engage (FRAGILE — may race or fail silently)
        try {
          const message = flowState.hasSelfAmendment
            ? SELF_AMENDMENT_BLOCKED_MESSAGE
            : STOP_BLOCKED_MESSAGE

          await ctx.client.session.prompt(sessionID, {
            parts: [{ type: "text", text: message }],
          })
        } catch (err) {
          // Re-engagement failed — log but don't crash
          console.warn(
            "[manifest-dev] Failed to re-engage after session.idle:",
            err
          )
        }
      }

      if (event.type === "todo.updated") {
        // Track workflow progress via todo state changes.
        // event.properties.todos = [{id, content, status, priority}]
        // Future: analyze todo status transitions for workflow tracking
      }
    },
  }
}

export default ManifestDevPlugin
