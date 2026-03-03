/**
 * manifest-dev plugin for OpenCode CLI
 *
 * Hook stubs — behavioral logic must be ported manually from the Python
 * originals in claude-plugins/manifest-dev/hooks/. See HOOK_SPEC.md for
 * the full behavioral specification.
 *
 * Source hooks:
 *   pretool_verify_hook.py  -> tool.execute.before (Skill tool, verify skill)
 *   stop_do_hook.py         -> session.idle
 *   post_compact_hook.py    -> experimental.session.compacting
 */

import type { Plugin } from "@opencode-ai/plugin"

export const ManifestDevPlugin: Plugin = async (ctx) => {
  return {
    // ---------------------------------------------------------------
    // pretool_verify_hook: Remind agent to read manifest/log before
    // running /verify. Fires on tool.execute.before for the "skill"
    // tool when the skill name is "verify".
    // ---------------------------------------------------------------
    "tool.execute.before": async ({ tool, sessionID, callID }, { args }) => {
      // TODO: Port from pretool_verify_hook.py
      // 1. Check if tool === "skill" and args.name === "verify"
      // 2. If match, inject system reminder:
      //    "VERIFICATION CONTEXT CHECK: Read the manifest and execution
      //     log in FULL before spawning verifiers."
      // 3. To inject context, mutate args or use ctx.client to send
      //    a system message (API TBD — see HOOK_SPEC.md).
      //
      // NOTE: OpenCode's tool.execute.before can block by setting
      //   args.abort = "reason"
      // but this hook should NOT abort — only inject context.
    },

    // ---------------------------------------------------------------
    // stop_do_hook: Block premature stops during /do workflow.
    // Fires on session.idle. If /do was invoked but neither /done nor
    // /escalate was called, prevent the session from ending.
    // ---------------------------------------------------------------
    "session.idle": async (event) => {
      // TODO: Port from stop_do_hook.py
      // 1. Read session transcript/history to detect /do invocation
      // 2. Check if /done or /escalate was subsequently called
      // 3. If /do active but no /done or /escalate:
      //    - Check for infinite loop (3+ consecutive short outputs)
      //    - If loop detected: allow with warning
      //    - Otherwise: inject system message blocking the stop
      //      "Stop blocked: /do workflow requires formal exit.
      //       Options: (1) Run /verify (2) Call /escalate"
      //
      // NOTE: session.idle is NOT blocking in OpenCode. To prevent
      // premature stops, use tui.toast.show or inject a follow-up
      // message via ctx.client. The exact mechanism may require
      // OpenCode plugin API extensions. See HOOK_SPEC.md.
    },

    // ---------------------------------------------------------------
    // post_compact_hook: Restore /do workflow context after session
    // compaction. Fires on experimental.session.compacting.
    // ---------------------------------------------------------------
    "experimental.session.compacting": async (event) => {
      // TODO: Port from post_compact_hook.py
      // 1. Detect if an active /do workflow exists (session history)
      // 2. If /do active and neither /done nor /escalate called:
      //    Inject recovery reminder:
      //    "This session was compacted during an active /do workflow.
      //     CRITICAL: Read the manifest and execution log in FULL
      //     before continuing. Resume from where you left off."
      //
      // NOTE: experimental.session.compacting is experimental in
      // OpenCode. Behavior may change between releases.
    },
  }
}

export default ManifestDevPlugin
