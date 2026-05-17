import type { Plugin } from "@opencode-ai/plugin"

/**
 * manifest-dev plugin for OpenCode CLI.
 *
 * Ported from Claude Code Python hooks. Implements:
 * - Stop enforcement for /do workflow (session.idle — CANNOT block, documented limitation)
 * - Post-compaction workflow recovery (experimental.session.compacting)
 *
 * KNOWN LIMITATIONS:
 * 1. Cannot block session stopping — session.idle is fire-and-forget (issue #12472).
 *    The stop_do_hook enforcement from Claude Code has NO equivalent in OpenCode.
 *    Workaround: inject strong system-level guidance via chat.system.transform.
 * 2. No JSONL transcript — workflow state must be tracked in-memory per session.
 *
 * See HOOK_SPEC.md for full behavioral specification.
 */

// ---------------------------------------------------------------------------
// In-memory workflow state (no JSONL transcript in OpenCode)
// ---------------------------------------------------------------------------

interface DoFlowState {
  active: boolean
  hasDone: boolean
  hasEscalate: boolean
  doArgs: string | null
  consecutiveIdleOutputs: number // loop detection counter
}

// Per-session state maps
const doStates = new Map<string, DoFlowState>()

function getDoState(sessionID: string): DoFlowState {
  if (!doStates.has(sessionID)) {
    doStates.set(sessionID, {
      active: false,
      hasDone: false,
      hasEscalate: false,
      doArgs: null,
      consecutiveIdleOutputs: 0,
    })
  }
  return doStates.get(sessionID)!
}

function extractSkillName(args: Record<string, unknown>): string | null {
  const skill = args?.skill as string | undefined
  if (!skill) return null
  return skill.includes(":") ? skill.split(":").pop()! : skill
}

// ---------------------------------------------------------------------------
// Plugin export
// ---------------------------------------------------------------------------

export const ManifestDevPlugin: Plugin = async (_ctx) => {
  return {

    // -----------------------------------------------------------------------
    // tool.execute.before — Pre-tool hooks
    // LIMITATION: Does NOT fire for subagent tool calls (issue #5894)
    // -----------------------------------------------------------------------
    "tool.execute.before": async ({ tool, sessionID }, { args }) => {
      // --- Detect skill invocations via the task tool ---
      if (tool === "task" || tool === "skill") {
        const skillName = extractSkillName(args as Record<string, unknown>)
        if (!skillName) return

        const skillArgs = (args as Record<string, unknown>)?.args as string | undefined

        // Track /do invocation
        if (skillName === "do") {
          const state = getDoState(sessionID)
          state.active = true
          state.hasDone = false
          state.hasEscalate = false
          state.doArgs = skillArgs ?? null
          state.consecutiveIdleOutputs = 0
        }

        // Track /done invocation
        if (skillName === "done") {
          const state = getDoState(sessionID)
          if (state.active) {
            state.hasDone = true
          }
        }

        // Track /escalate invocation
        if (skillName === "escalate") {
          const state = getDoState(sessionID)
          if (state.active) {
            state.hasEscalate = true
          }
        }
      }
    },

    // -----------------------------------------------------------------------
    // experimental.chat.system.transform — System context injection
    // Fires before every LLM request. Closest to Claude Code's additionalContext.
    // -----------------------------------------------------------------------
    "experimental.chat.system.transform": async ({ sessionID }, output) => {
      const doState = getDoState(sessionID)

      // --- /do workflow: stop enforcement ---
      if (doState.active && !doState.hasDone && !doState.hasEscalate) {
        // Stop enforcement guidance (cannot actually block — session.idle is fire-and-forget)
        // Decision matrix:
        // - /done: allow (verified complete) — handled by hasDone check above
        // - /escalate: allow (properly escalated) — handled by hasEscalate check above
        // - Otherwise: enforce: must /done or /escalate
        output.system.push(
          `<system-reminder>/do appears unfinished — no /done or /escalate ` +
          `detected since the last /do invocation. /do is responsible for ` +
          `verifying every Acceptance Criterion and Global Invariant inline ` +
          `by spawning a subagent per criterion using the verify prompt. ` +
          `When everything verifies PASS, call /done. When blocked, call ` +
          `/escalate. If the flow is already closed and this hook is ` +
          `misreading the transcript, proceed — the idle-loop escape valve ` +
          `will release the stop after 3 idle outputs.</system-reminder>`
        )
      }
    },

    // -----------------------------------------------------------------------
    // experimental.session.compacting — Post-compaction recovery
    // -----------------------------------------------------------------------
    "experimental.session.compacting": async ({ sessionID }, output) => {
      const doState = getDoState(sessionID)

      // /do workflow recovery
      if (doState.active && !doState.hasDone && !doState.hasEscalate) {
        if (doState.doArgs) {
          output.context.push(
            `This session appears to have been compacted during an active /do ` +
            `workflow — context from before compaction may be missing.\n\n` +
            `The /do was invoked with: ${doState.doArgs}\n\n` +
            `If deliverables or acceptance criteria aren't currently in context, ` +
            `re-reading the manifest restores progress and prevents restarting ` +
            `completed work. If it's already loaded from post-compact context, ` +
            `skip the re-read and resume from where you left off. If this hook ` +
            `is misreading and the session was never mid-/do, proceed normally.`
          )
        } else {
          output.context.push(
            `This session appears to have been compacted during an active /do ` +
            `workflow — context from before compaction may be missing.\n\n` +
            `If orientation is missing, the manifest path was passed to /do at ` +
            `invocation and re-reading it surfaces the deliverables, acceptance ` +
            `criteria, and global invariants needed to resume. If orientation is ` +
            `already intact, skip the re-read. If this hook is misreading and ` +
            `the session was never mid-/do, proceed normally.`
          )
        }
      }
    },

    // -----------------------------------------------------------------------
    // event — Bus events (fire-and-forget)
    // -----------------------------------------------------------------------
    event: async ({ event }) => {
      // session.idle: clear workflow state to avoid stale guidance
      if (event.type === "session.idle") {
        const sessionID = (event.properties as { sessionID?: string })?.sessionID
        if (sessionID) {
          doStates.delete(sessionID)
        }
      }
    },
  }
}
