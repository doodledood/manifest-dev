import type { Plugin } from "@opencode-ai/plugin"

/**
 * manifest-dev plugin for OpenCode CLI.
 *
 * Ported from Claude Code Python hooks. Implements:
 * - Stop enforcement for /do workflow (session.idle — CANNOT block, documented limitation)
 * - Post-compaction workflow recovery (experimental.session.compacting)
 * - Pre-verify context refresh (tool.execute.before on task tool)
 * - Post-milestone log reminder (tool.execute.after on task/todowrite tools)
 * - Amendment check on user prompt during /do (experimental.chat.system.transform)
 * - /understand principles reinforcement (experimental.chat.system.transform)
 *
 * KNOWN LIMITATIONS:
 * 1. Cannot block session stopping — session.idle is fire-and-forget (issue #12472).
 *    The stop_do_hook enforcement from Claude Code has NO equivalent in OpenCode.
 *    Workaround: inject strong system-level guidance via chat.system.transform.
 * 2. tool.execute.before does NOT fire for subagent tool calls (issue #5894).
 *    Hooks within spawned agents (e.g., criteria-checker, reviewers) won't trigger.
 * 3. No JSONL transcript — workflow state must be tracked in-memory per session.
 *
 * See HOOK_SPEC.md for full behavioral specification.
 */

// ---------------------------------------------------------------------------
// In-memory workflow state (no JSONL transcript in OpenCode)
// ---------------------------------------------------------------------------

interface DoFlowState {
  active: boolean
  hasVerify: boolean
  hasDone: boolean
  hasEscalate: boolean
  hasSelfAmendment: boolean
  doArgs: string | null
}

interface UnderstandFlowState {
  active: boolean
  isComplete: boolean
  understandArgs: string | null
}

// Per-session state maps
const doStates = new Map<string, DoFlowState>()
const understandStates = new Map<string, UnderstandFlowState>()

function getDoState(sessionID: string): DoFlowState {
  if (!doStates.has(sessionID)) {
    doStates.set(sessionID, {
      active: false,
      hasVerify: false,
      hasDone: false,
      hasEscalate: false,
      hasSelfAmendment: false,
      doArgs: null,
    })
  }
  return doStates.get(sessionID)!
}

function getUnderstandState(sessionID: string): UnderstandFlowState {
  if (!understandStates.has(sessionID)) {
    understandStates.set(sessionID, {
      active: false,
      isComplete: false,
      understandArgs: null,
    })
  }
  return understandStates.get(sessionID)!
}

// Workflow skills that end an /understand session
const WORKFLOW_SKILLS = new Set(["define", "do", "auto"])

// Skills that represent workflow transitions worth logging
const LOG_WORKFLOW_SKILLS = new Set(["verify", "escalate", "done", "define"])

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
          state.hasVerify = false
          state.hasDone = false
          state.hasEscalate = false
          state.hasSelfAmendment = false
          state.doArgs = skillArgs ?? null
        }

        // Track /verify invocation
        if (skillName === "verify") {
          const state = getDoState(sessionID)
          if (state.active) {
            state.hasVerify = true
          }
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
            if (skillArgs && skillArgs.toLowerCase().includes("self-amendment")) {
              state.hasSelfAmendment = true
            }
          }
        }

        // Track /understand invocation
        if (skillName === "understand") {
          const uState = getUnderstandState(sessionID)
          uState.active = true
          uState.isComplete = false
          uState.understandArgs = skillArgs ?? null
        }

        // Track /understand-done
        if (skillName === "understand-done") {
          const uState = getUnderstandState(sessionID)
          if (uState.active) {
            uState.isComplete = true
          }
        }

        // Workflow skills end /understand
        if (WORKFLOW_SKILLS.has(skillName)) {
          const uState = getUnderstandState(sessionID)
          if (uState.active && !uState.isComplete) {
            uState.isComplete = true
          }
        }

        // --- Pre-verify context refresh (pretool_verify_hook) ---
        if (skillName === "verify") {
          const verifyArgs = skillArgs ?? ""
          throw new Error(
            `VERIFICATION CONTEXT CHECK: You are about to run /verify.\n\n` +
            (verifyArgs ? `Arguments: ${verifyArgs}\n\n` : "") +
            `BEFORE spawning verifiers, read the manifest and execution log in FULL ` +
            `if not recently loaded. You need ALL acceptance criteria (AC-*) and ` +
            `global invariants (INV-G*) in context to spawn the correct verifiers.\n\n` +
            `This is a context reminder, not a blocker. Proceed with /verify after ` +
            `confirming files are loaded.`
          )
          // NOTE: In OpenCode, throwing an Error blocks the tool call and the
          // error message becomes the tool result. This is more aggressive than
          // Claude Code's additionalContext approach. The agent will see the
          // reminder and can re-invoke /verify. If this causes friction, convert
          // to experimental.chat.system.transform injection instead.
        }
      }
    },

    // -----------------------------------------------------------------------
    // tool.execute.after — Post-tool hooks
    // -----------------------------------------------------------------------
    "tool.execute.after": async ({ tool, sessionID, args }) => {
      // --- Post-milestone log reminder (posttool_log_hook) ---
      const doState = getDoState(sessionID)
      if (!doState.active || doState.hasDone) return

      let shouldRemind = false
      let skillDetail = ""

      // TodoWrite / task management milestones
      if (tool === "todowrite" || tool === "todoread") {
        shouldRemind = true
      }

      // Skill/task calls for workflow transitions
      if (tool === "task" || tool === "skill") {
        const skillName = extractSkillName(args as Record<string, unknown>)
        if (skillName && LOG_WORKFLOW_SKILLS.has(skillName)) {
          shouldRemind = true
          skillDetail = ` (skill: ${skillName})`
        }
      }

      if (!shouldRemind) return

      // We cannot inject additionalContext in tool.execute.after in OpenCode.
      // Instead we mutate the output to append the reminder.
      // The `output` parameter in the hook signature allows mutation.
      // However, since we're in a fire-and-forget position here,
      // the reminder is best delivered via chat.system.transform.
      // This is a known gap — the log reminder is handled there instead.
    },

    // -----------------------------------------------------------------------
    // experimental.chat.system.transform — System context injection
    // Fires before every LLM request. Closest to Claude Code's additionalContext.
    // -----------------------------------------------------------------------
    "experimental.chat.system.transform": async ({ sessionID }, output) => {
      const doState = getDoState(sessionID)
      const uState = getUnderstandState(sessionID)

      // --- /do workflow: stop enforcement + amendment check + log reminder ---
      if (doState.active && !doState.hasDone) {
        // Stop enforcement guidance (cannot actually block — session.idle is fire-and-forget)
        if (!doState.hasEscalate || doState.hasSelfAmendment) {
          output.system.push(
            `<system-reminder>WORKFLOW ENFORCEMENT: /do is active. ` +
            `You MUST NOT stop without calling /verify → /done or /escalate. ` +
            `Options: (1) Run /verify to check criteria — if all pass, /verify calls /done. ` +
            `(2) Call /escalate — for blocking issues OR user-requested pauses. ` +
            `Short outputs will violate the workflow contract.</system-reminder>`
          )
        }

        // Self-amendment continuation
        if (doState.hasSelfAmendment) {
          output.system.push(
            `<system-reminder>Self-Amendment in progress. ` +
            `You must invoke /define --amend before stopping.</system-reminder>`
          )
        }

        // Amendment check on user input (prompt_submit_hook equivalent)
        output.system.push(
          `<system-reminder>AMENDMENT CHECK: You are in an active /do workflow. ` +
          `If the user's latest input contradicts, extends, or amends the manifest, ` +
          `call /escalate with Self-Amendment type, then invoke /define --amend. ` +
          `If the input is a clarification or confirmation, continue normally.</system-reminder>`
        )

        // Log reminder (posttool_log_hook equivalent — injected as persistent context)
        output.system.push(
          `<system-reminder>LOG REMINDER: After every milestone (task updates, ` +
          `workflow skill calls), update the execution log immediately. ` +
          `The log is disaster recovery — if context is lost, only the log survives.</system-reminder>`
        )
      }

      // --- /understand workflow: principles reinforcement ---
      if (uState.active && !uState.isComplete) {
        output.system.push(
          `<system-reminder>/understand active. Self-check before responding:\n` +
          `- Are you claiming something you haven't verified?\n` +
          `- Are you agreeing just to be agreeable?\n` +
          `- Are you proposing when you should be exploring?\n` +
          `- Are you filling the user's uncertainty with your confidence?\n\n` +
          `Principles: investigate before claiming, name verified vs inferred, ` +
          `surface seams, sit with fog.</system-reminder>`
        )
      }
    },

    // -----------------------------------------------------------------------
    // experimental.session.compacting — Post-compaction recovery
    // -----------------------------------------------------------------------
    "experimental.session.compacting": async ({ sessionID }, output) => {
      const doState = getDoState(sessionID)
      const uState = getUnderstandState(sessionID)

      // /do workflow recovery
      if (doState.active && !doState.hasDone && !doState.hasEscalate) {
        if (doState.doArgs) {
          output.context.push(
            `This session was compacted during an active /do workflow. Context may have been lost.\n\n` +
            `CRITICAL: Before continuing, read the manifest and execution log in FULL.\n\n` +
            `The /do was invoked with: ${doState.doArgs}\n\n` +
            `1. Read the manifest file — contains deliverables, acceptance criteria, and approach\n` +
            `2. Check /tmp/ for your execution log (do-log-*.md) and read it to recover progress\n\n` +
            `Do not restart completed work. Resume from where you left off.`
          )
        } else {
          output.context.push(
            `This session was compacted during an active /do workflow. Context may have been lost.\n\n` +
            `CRITICAL: Before continuing, recover your workflow context:\n\n` +
            `1. Check /tmp/ for execution logs matching do-log-*.md\n` +
            `2. The log references the manifest file path — read both in FULL\n\n` +
            `Do not restart completed work. Resume from where you left off.`
          )
        }
      }

      // /understand session recovery
      if (uState.active && !uState.isComplete) {
        if (uState.understandArgs) {
          output.context.push(
            `This session was compacted during an active /understand session. Context may have been lost.\n\n` +
            `You are in an /understand session about: ${uState.understandArgs}\n\n` +
            `Re-read the /understand skill to restore your cognitive stance. ` +
            `Truth-convergence is your north star — investigate before claiming, surface seams, resist premature synthesis.`
          )
        } else {
          output.context.push(
            `This session was compacted during an active /understand session. Context may have been lost.\n\n` +
            `Re-read the /understand skill to restore your cognitive stance. ` +
            `Truth-convergence is your north star — investigate before claiming, surface seams, resist premature synthesis.`
          )
        }
      }
    },

    // -----------------------------------------------------------------------
    // event — Bus events (fire-and-forget)
    // -----------------------------------------------------------------------
    event: async ({ event }) => {
      // session.idle — CANNOT prevent stopping (documented limitation)
      // The stop enforcement is done via chat.system.transform instead
      if (event.type === "session.idle") {
        // No-op. In Claude Code, the Stop hook blocks stopping.
        // In OpenCode, session.idle is fire-and-forget — we cannot block.
        // The workaround (client.session.prompt) is fragile and race-prone.
        // Enforcement is approximated via persistent system context instead.
      }
    },
  }
}
