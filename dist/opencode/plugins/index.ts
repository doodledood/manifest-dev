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
  consecutiveIdleOutputs: number // loop detection counter
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
      consecutiveIdleOutputs: 0,
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
          state.consecutiveIdleOutputs = 0
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
            `/verify appears to be starting.\n\n` +
            (verifyArgs ? `Arguments: ${verifyArgs}\n\n` : "") +
            `Before spawning verifiers, the manifest and execution log may need ` +
            `to be in full context — if they haven't been read recently, loading ` +
            `them surfaces every acceptance criterion (AC-*) and global invariant ` +
            `(INV-G*) so the right verifiers get spawned. If they're already in ` +
            `context from recent work, proceed with /verify directly.\n\n` +
            `This is a context reminder, not a blocker.`
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
            `<system-reminder>A Self-Amendment escalation appears active — the ` +
            `manifest looks like it needs revision before /do can continue. ` +
            `/define --amend <manifest-path> applies the amendment; then resume ` +
            `/do with the updated manifest. If the escalation was already resolved ` +
            `and this hook is misreading the transcript, proceed — the flow will ` +
            `close on the next /done or /escalate.</system-reminder>`
          )
        } else if (doState.hasEscalate) {
          // Non-self-amendment escalation — properly escalated, allow stop
          // No enforcement message needed
        } else if (doState.hasCollabMode && doState.hasVerify) {
          // Non-local medium: /verify posted escalation externally
          output.system.push(
            `<system-reminder>Verification results posted to the external review channel. ` +
            `The user will re-invoke /do with the execution log path ` +
            `once the blocker is resolved.</system-reminder>`
          )
        } else {
          // No exit condition met — enforce workflow
          output.system.push(
            `<system-reminder>/do appears unfinished — no /verify, /done, or ` +
            `/escalate detected since the last /do invocation. If implementation ` +
            `looks complete, running /verify against the manifest will check the ` +
            `acceptance criteria. If waiting on async work or otherwise blocked, ` +
            `/escalate formally pauses the flow. If the flow is already closed ` +
            `and this hook is misreading the transcript, proceed — the idle-loop ` +
            `escape valve will release the stop after 3 idle outputs.</system-reminder>`
          )
        }

        // Amendment check on user input (prompt_submit_hook equivalent)
        output.system.push(
          `<system-reminder>A user message arrived during what looks like an ` +
          `active /do workflow. Before continuing execution, it's worth checking ` +
          `whether the input might: (1) contradict an existing AC, INV, or PG ` +
          `in the manifest, (2) extend the manifest with new requirements not ` +
          `currently covered, or (3) amend the scope or approach in a way that ` +
          `changes what "done" means. If any of those look likely: /escalate ` +
          `with Self-Amendment type, then invoke /define --amend <manifest-path>. ` +
          `After /define returns, resume /do with the updated manifest. If the ` +
          `input reads more like clarification, confirmation, or unrelated ` +
          `context (or if this hook is misreading the state and /do is already ` +
          `closed), continue execution normally.</system-reminder>`
        )

        // Log reminder (posttool_log_hook equivalent — injected as persistent context)
        output.system.push(
          `<system-reminder>After any milestone-shaped tool call during /do ` +
          `(task updates, workflow skill calls) that introduced new state, ` +
          `decisions, or outcomes not already in the execution log, writing ` +
          `them preserves the record — the log is disaster recovery if context ` +
          `is lost. If recent calls were routine and already reflected there, ` +
          `skip this reminder.</system-reminder>`
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
            `This session appears to have been compacted during an active /do ` +
            `workflow — context from before compaction may be missing.\n\n` +
            `The /do was invoked with: ${doState.doArgs}\n\n` +
            `If deliverables or acceptance criteria aren't currently in context, ` +
            `reading the manifest and any /tmp/do-log-*.md execution log restores ` +
            `progress and prevents restarting completed work. If both are already ` +
            `loaded from post-compact context, skip the re-read and resume from ` +
            `where you left off. If this hook is misreading and the session was ` +
            `never mid-/do, proceed normally.`
          )
        } else {
          output.context.push(
            `This session appears to have been compacted during an active /do ` +
            `workflow — context from before compaction may be missing.\n\n` +
            `If orientation is missing, checking /tmp/ for an execution log ` +
            `matching do-log-*.md should surface both the manifest path ` +
            `(referenced in the log) and progress so far. If orientation is ` +
            `already intact, skip the re-read. If this hook is misreading and ` +
            `the session was never mid-/do, proceed normally.`
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
