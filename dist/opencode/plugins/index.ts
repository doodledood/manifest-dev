/**
 * manifest-dev plugin for OpenCode CLI
 *
 * Hook stubs — behavioral logic must be ported manually from the Python
 * originals in claude-plugins/manifest-dev/hooks/. See HOOK_SPEC.md for
 * the full behavioral specification.
 *
 * Source hooks:
 *   pretool_verify_hook.py  -> tool.execute.before (Skill tool, verify skill)
 *   stop_do_hook.py         -> session.idle (event — CANNOT block, see notes)
 *   post_compact_hook.py    -> experimental.session.compacting
 *
 * Corrected for OpenCode v1.2.15 (March 2026):
 *   - Blocking: throw new Error("reason"), NOT args.abort
 *   - Context injection: experimental.chat.system.transform (push to output.system[])
 *   - Compaction: experimental.session.compacting with output.context.push()
 *   - session.idle: fire-and-forget, CANNOT prevent stopping
 *   - Subagent bypass: tool.execute.before does NOT fire for subagent tool calls (#5894)
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
 * Updated by tool.execute.before (skill invocations) and todo.updated events.
 */
interface DoFlowState {
  hasDo: boolean
  hasDone: boolean
  hasEscalate: boolean
  hasVerify: boolean
  doArgs: string | null
  hasTeamContext: boolean
}

const VERIFY_CONTEXT_REMINDER = `VERIFICATION CONTEXT CHECK: You are about to run /verify.

Arguments: {verify_args}

BEFORE spawning verifiers, read the manifest and execution log in FULL if not recently loaded. You need ALL acceptance criteria (AC-*) and global invariants (INV-G*) in context to spawn the correct verifiers.`

const VERIFY_CONTEXT_REMINDER_MINIMAL = `VERIFICATION CONTEXT CHECK: You are about to run /verify.

BEFORE spawning verifiers, read the manifest and execution log in FULL if not recently loaded. You need ALL acceptance criteria (AC-*) and global invariants (INV-G*) in context to spawn the correct verifiers.`

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

const STOP_BLOCKED_MESSAGE = `Stop blocked: /do workflow requires formal exit. Options: (1) Run /verify to check criteria - if all pass, /verify calls /done. (2) Call /escalate - for blocking issues OR user-requested pauses. Short outputs will be blocked. Choose one.`

const LOOP_WARNING_MESSAGE = `WARNING: Stop allowed to break infinite loop. The /do workflow was NOT properly completed. Next time, call /escalate when blocked instead of minimal outputs.`

const TEAM_MODE_VERIFY_MESSAGE = `Verification delegated to the team lead. The lead will spawn verification teammates and relay results. You will receive a message with VERIFICATION_RESULT when complete.`

export const ManifestDevPlugin: Plugin = async (ctx) => {
  // Session-scoped workflow state. Reset on each new /do invocation.
  const flowState: DoFlowState = {
    hasDo: false,
    hasDone: false,
    hasEscalate: false,
    hasVerify: false,
    doArgs: null,
    hasTeamContext: false,
  }

  // Track consecutive short outputs for loop detection
  let consecutiveShortOutputs = 0

  /**
   * Helper: check if a tool call is for a specific skill.
   * Matches both "skill-name" and "plugin:skill-name" formats.
   */
  function isSkillCall(tool: string, args: any, skillName: string): boolean {
    if (tool !== "skill" && tool !== "task") return false
    const name: string = args?.name ?? args?.skill ?? ""
    return name === skillName || name.endsWith(`:${skillName}`)
  }

  return {
    // ---------------------------------------------------------------
    // pretool_verify_hook: Remind agent to read manifest/log before
    // running /verify. Fires on tool.execute.before for the "skill"
    // tool when the skill name is "verify".
    //
    // Also tracks /do, /done, /escalate, /verify invocations for
    // workflow state.
    //
    // BLOCKING: throw new Error("reason") — error message becomes
    //   the tool result seen by the LLM.
    // LIMITATION: Does NOT fire for subagent tool calls (issue #5894).
    //   This means skill invocations WITHIN a subagent won't be
    //   tracked here.
    // ---------------------------------------------------------------
    "tool.execute.before": async ({ tool, sessionID, callID }, { args }) => {
      // --- Workflow state tracking ---
      // Track /do invocations (resets state)
      if (isSkillCall(tool, args, "do")) {
        flowState.hasDo = true
        flowState.hasDone = false
        flowState.hasEscalate = false
        flowState.hasVerify = false
        const doArgs = args?.args?.trim() || null
        flowState.doArgs = doArgs
        flowState.hasTeamContext = doArgs ? doArgs.includes("TEAM_CONTEXT") : false
        consecutiveShortOutputs = 0
      }

      // Track /done, /escalate, /verify after /do
      if (flowState.hasDo) {
        if (isSkillCall(tool, args, "done")) flowState.hasDone = true
        if (isSkillCall(tool, args, "escalate")) flowState.hasEscalate = true
        if (isSkillCall(tool, args, "verify")) flowState.hasVerify = true
      }

      // --- Pre-verify context injection ---
      // This hook does NOT block — it only provides a reminder.
      // Context injection happens via experimental.chat.system.transform
      // (see below). Here we just mark that verify was called so the
      // system transform can include the reminder on the next LLM call.
      //
      // NOTE: If you need to block a tool call, use:
      //   throw new Error("Reason shown to LLM as tool result")
      // This hook intentionally does NOT throw.
    },

    // ---------------------------------------------------------------
    // tool.execute.after: Track output length for loop detection.
    // Used by stop-do enforcement to detect infinite loop patterns.
    // ---------------------------------------------------------------
    "tool.execute.after": async ({ tool, sessionID, callID, args }, { title, output, metadata }) => {
      // Track output length for loop detection
      const outputStr = typeof output === "string" ? output : JSON.stringify(output ?? "")
      if (outputStr.length < 100) {
        consecutiveShortOutputs++
      } else {
        consecutiveShortOutputs = 0
      }
    },

    // ---------------------------------------------------------------
    // Context injection via system transform.
    // Called before every LLM request. Pushes context strings into
    // output.system[] which become system-level messages.
    //
    // This is the correct mechanism for context injection in OpenCode,
    // replacing Claude Code's additionalContext pattern.
    // ---------------------------------------------------------------
    "experimental.chat.system.transform": async ({ sessionID, model }, output) => {
      // Inject verify reminder if /verify was just invoked
      if (flowState.hasVerify && flowState.hasDo) {
        const reminder = flowState.doArgs
          ? VERIFY_CONTEXT_REMINDER.replace("{verify_args}", flowState.doArgs)
          : VERIFY_CONTEXT_REMINDER_MINIMAL
        output.system.push(reminder)
      }

      // Inject stop-do enforcement context if in active /do workflow
      if (flowState.hasDo && !flowState.hasDone && !flowState.hasEscalate) {
        output.system.push(
          "ACTIVE /do WORKFLOW: You must complete this workflow with /verify " +
          "(which calls /done on success) or /escalate before stopping. " +
          "Do not attempt to end the session without one of these."
        )
      }
    },

    // ---------------------------------------------------------------
    // post_compact_hook: Restore /do workflow context after session
    // compaction. Fires on experimental.session.compacting.
    //
    // Injects context via output.context.push() to preserve workflow
    // state across compaction. Optionally replace the compaction prompt
    // via output.prompt.
    //
    // NOTE: This event is experimental and may change between releases.
    // ---------------------------------------------------------------
    "experimental.session.compacting": async ({ sessionID }, output) => {
      // Not in /do workflow — nothing to preserve
      if (!flowState.hasDo) return

      // Workflow already completed — no recovery needed
      if (flowState.hasDone || flowState.hasEscalate) return

      // Active /do workflow — inject recovery context
      const reminder = flowState.doArgs
        ? DO_WORKFLOW_RECOVERY_REMINDER.replace("{do_args}", flowState.doArgs)
        : DO_WORKFLOW_RECOVERY_FALLBACK

      output.context.push(reminder)
    },

    // ---------------------------------------------------------------
    // Event handler: catch-all for bus events.
    //
    // session.idle: Session stopped. CANNOT prevent stopping — this is
    //   fire-and-forget. The workaround ctx.client.session.prompt() to
    //   inject a follow-up message is fragile and has race conditions
    //   in `run` mode (issue #15267). Feature request for blocking
    //   session.idle exists (issue #12472).
    //
    // todo.updated: Tracks workflow progress via todo state changes.
    //   Useful for monitoring /do workflow progress without relying
    //   on transcript parsing.
    // ---------------------------------------------------------------
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        // LIMITATION: Cannot prevent the session from stopping.
        // Claude Code's Stop hook can return decision: "block" but
        // OpenCode's session.idle is fire-and-forget.
        //
        // Best-effort workaround: use ctx.client.session.prompt()
        // to create a NEW turn with the stop-blocked message.
        // WARNING: This is fragile — race condition in `run` mode
        // where the session may have already exited before the prompt
        // is processed (issue #15267).
        if (flowState.hasDo && !flowState.hasDone && !flowState.hasEscalate) {
          // Team mode: /verify was called and verification is delegated to the lead.
          if (flowState.hasTeamContext && flowState.hasVerify) {
            console.info(TEAM_MODE_VERIFY_MESSAGE)
            return
          }
          if (consecutiveShortOutputs >= 3) {
            // Loop detected — allow stop but log warning.
            // In Claude Code this would be decision: "allow" with systemMessage.
            // Here we can only attempt to log or show a toast.
            console.warn(LOOP_WARNING_MESSAGE)
          } else {
            // Would block in Claude Code. Best-effort: inject follow-up prompt.
            // This creates a NEW conversation turn, not a true block.
            try {
              // ctx.client.session.prompt(event.properties?.sessionID, {
              //   parts: [{ type: "text", text: STOP_BLOCKED_MESSAGE }]
              // })
              console.warn(
                "STOP-DO: Session idle during active /do workflow. " +
                "Cannot block — session.idle is fire-and-forget. " +
                "Uncomment ctx.client.session.prompt() call to attempt fragile workaround."
              )
            } catch {
              // Silently fail — this is best-effort only
            }
          }
        }
      }

      if (event.type === "todo.updated") {
        // Track workflow progress via todo state changes.
        // event.properties.todos = [{id, content, status, priority}]
        // This can be used to detect /do workflow progress without
        // relying on transcript parsing — e.g., monitoring when all
        // acceptance criteria todos are marked complete.
        const todos = (event as any).properties?.todos
        if (Array.isArray(todos)) {
          // Future: analyze todo status transitions for workflow tracking
          // e.g., all AC-* items complete -> suggest running /verify
        }
      }
    },
  }
}

export default ManifestDevPlugin
