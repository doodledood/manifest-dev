import type { Plugin } from "opencode"

/**
 * manifest-dev hooks for OpenCode CLI.
 *
 * IMPORTANT: These are stubs requiring manual implementation.
 * The behavioral logic must be ported from the Python source hooks.
 * See HOOK_SPEC.md for the complete behavioral specification.
 *
 * Source: claude-plugins/manifest-dev/hooks/
 * Runtime: Bun (JS/TS only — Python hooks cannot run directly)
 */

export const ManifestDevPlugin: Plugin = async ({
  project,
  client,
  $,
  directory,
  worktree,
}) => {
  return {
    event: {
      /**
       * Stop hook: Blocks premature stops during /do workflow.
       * Source: hooks/stop_do_hook.py | Claude Code event: Stop
       *
       * Decision matrix:
       * - API error -> allow (system failure)
       * - No /do -> allow (not in flow)
       * - /do + /done -> allow (verified complete)
       * - /do + /escalate -> allow (properly escalated)
       * - /do only -> block (must verify first)
       * - 3+ consecutive short outputs -> allow (loop break)
       */
      "session.complete": async (input, output) => {
        // TODO: Port stop_do_hook.py logic
        // 1. Read transcript, parse /do workflow state
        // 2. Block if in /do without /done or /escalate
        // 3. Loop detection: allow after 3+ short outputs
        // output.abort = "reason" to block
      },

      /**
       * PreToolUse hook: Adds context reminder before /verify.
       * Source: hooks/pretool_verify_hook.py | Claude Code event: PreToolUse
       *
       * When /verify skill is about to be called, reminds the model
       * to read manifest and execution log for accurate verification.
       */
      "tool.execute.before": async (input, output) => {
        // TODO: Port pretool_verify_hook.py logic
        // 1. Check if input.tool === "skill" and skill name is "verify"
        // 2. Inject system reminder about reading manifest/log
        // Note: OpenCode may need message.transform for context injection
      },

      /**
       * Post-compact hook: Restores /do context after compaction.
       * Source: hooks/post_compact_hook.py | Claude Code event: SessionStart
       *
       * When session is compacted during /do, reminds the model
       * to re-read manifest and execution log.
       */
      "session.created": async (input, output) => {
        // TODO: Port post_compact_hook.py logic
        // 1. Detect if session was compacted (vs new session)
        // 2. Parse transcript for active /do workflow
        // 3. Inject recovery reminder if /do is active
        // Note: May need experimental.session.compacting event instead
      },
    },
  }
}
