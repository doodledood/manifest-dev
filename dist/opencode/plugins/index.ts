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
 * - Thinking disciplines reinforcement (experimental.chat.system.transform)
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
  hasCollabMode: boolean // --medium not local (non-local collaboration)
  consecutiveShortOutputs: number // loop detection counter
}

interface ThinkingDisciplinesState {
  active: boolean  // thinking-disciplines skill invoked and not yet deactivated
}

// Per-session state maps
const doStates = new Map<string, DoFlowState>()
const thinkingStates = new Map<string, ThinkingDisciplinesState>()

function getDoState(sessionID: string): DoFlowState {
  if (!doStates.has(sessionID)) {
    doStates.set(sessionID, {
      active: false,
      hasVerify: false,
      hasDone: false,
      hasEscalate: false,
      hasSelfAmendment: false,
      doArgs: null,
      hasCollabMode: false,
      consecutiveShortOutputs: 0,
    })
  }
  return doStates.get(sessionID)!
}

function getThinkingState(sessionID: string): ThinkingDisciplinesState {
  if (!thinkingStates.has(sessionID)) {
    thinkingStates.set(sessionID, { active: false })
  }
  return thinkingStates.get(sessionID)!
}

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
          state.consecutiveShortOutputs = 0
          // Detect --medium flag for non-local collaboration mode
          state.hasCollabMode = skillArgs
            ? /--medium\s+(?!local(?:\s|$))\S+/.test(skillArgs)
            : false
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

        // Track thinking-disciplines activation
        if (skillName === "thinking-disciplines") {
          const tState = getThinkingState(sessionID)
          tState.active = true
        }

        // Deactivate thinking disciplines on /stop-thinking-disciplines or /do
        if (skillName === "stop-thinking-disciplines" || skillName === "do") {
          const tState = getThinkingState(sessionID)
          tState.active = false
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

      // --- /do workflow: stop enforcement + amendment check + log reminder ---
      if (doState.active && !doState.hasDone) {
        // Stop enforcement guidance (cannot actually block — session.idle is fire-and-forget)
        // Decision matrix from stop_do_hook.py:
        // - /done: allow (verified complete) — handled by hasDone check above
        // - /escalate (non-self-amendment): allow (properly escalated)
        // - /escalate (self-amendment): block (must /define --amend)
        // - /verify + collab mode: allow (escalation posted to medium)
        // - No exit: block (must verify or escalate)

        if (doState.hasSelfAmendment) {
          // Self-Amendment escalation — must continue to /define --amend
          output.system.push(
            `<system-reminder>Stop blocked: Self-Amendment escalation requires ` +
            `/define --amend before stopping. Invoke ` +
            `/define --amend <manifest-path> to update the manifest, ` +
            `then resume /do.</system-reminder>`
          )
        } else if (doState.hasEscalate) {
          // Non-self-amendment escalation — properly escalated, allow stop
          // No enforcement message needed
        } else if (doState.hasCollabMode && doState.hasVerify) {
          // Non-local medium: /verify posted escalation to the medium
          output.system.push(
            `<system-reminder>Escalation posted to the communication medium. ` +
            `The user will re-invoke /do with the execution log path ` +
            `when the external blocker clears.</system-reminder>`
          )
        } else {
          // No exit condition met — enforce workflow
          output.system.push(
            `<system-reminder>WORKFLOW ENFORCEMENT: /do is active. ` +
            `You MUST NOT stop without calling /verify → /done or /escalate. ` +
            `Options: (1) Run /verify to check criteria — if all pass, /verify calls /done. ` +
            `(2) Call /escalate — for blocking issues OR user-requested pauses. ` +
            `Short outputs will be blocked. Choose one.</system-reminder>`
          )
        }

        // Amendment check on user input (prompt_submit_hook equivalent)
        output.system.push(
          `<system-reminder>AMENDMENT CHECK: You are in an active /do workflow. ` +
          `If the user's latest input contradicts, extends, or amends the manifest: ` +
          `(1) Contradicts an existing AC, INV, or PG in the manifest, ` +
          `(2) Extends the manifest with new requirements not currently covered, or ` +
          `(3) Amends the scope or approach in a way that changes what "done" means — ` +
          `call /escalate with Self-Amendment type, then invoke /define --amend <manifest-path>. ` +
          `After /define returns, resume /do with the updated manifest. ` +
          `If the input is a clarification or confirmation, continue normally.</system-reminder>`
        )

        // Log reminder (posttool_log_hook equivalent — injected as persistent context)
        output.system.push(
          `<system-reminder>LOG REMINDER: After every milestone (task updates, ` +
          `workflow skill calls), update the execution log immediately with what ` +
          `just happened, decisions made, and outcomes. ` +
          `The log is disaster recovery — if context is lost, only the log survives.</system-reminder>`
        )
      }

      // --- Thinking disciplines reinforcement ---
      const tState = getThinkingState(sessionID)
      if (tState.active) {
        output.system.push(
          `<system-reminder>Thinking disciplines active. Truth over helpfulness. ` +
          `Investigate before engaging. Verified and inferred are different — name which. ` +
          `Contradictions are leads, not noise. Partial pictures produce confident-sounding ` +
          `wrong answers — map the territory before forming a view. Don't advocate for an ` +
          `approach you haven't verified. If you still disagree after genuine exchange, say so. ` +
          `If the user flags something, investigate — don't reassure.</system-reminder>`
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

      // Thinking disciplines recovery
      const tState = getThinkingState(sessionID)
      if (tState.active) {
        output.context.push(
          `Thinking disciplines are active. Re-read the thinking-disciplines skill to restore your cognitive stance.`
        )
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
