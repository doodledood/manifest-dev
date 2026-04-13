#!/usr/bin/env python3
"""
Stop hook that enforces definition completion workflow for /do.

Blocks stop attempts unless /done or /escalate was called after /do.
This prevents the LLM from declaring "done" without verification.

Decision matrix:
- API error: ALLOW (system failure, not voluntary stop)
- No /do: ALLOW (not in flow)
- /do + /done: ALLOW (verified complete)
- /do + /escalate: ALLOW (properly escalated)
- /do + /verify + non-local medium: ALLOW (escalation posted to medium)
- /do only: BLOCK (must verify first)
- /do + /verify only: BLOCK (verify returned failures, keep working)
"""

from __future__ import annotations

import json
import os
import sys

from hook_utils import (
    count_consecutive_short_outputs,
    has_recent_api_error,
    parse_do_flow,
    record_stop_block,
)

# Maximum number of consecutive blocks to allow before escaping with a
# diagnostic warning when the transcript is not advancing. This is the
# independent-of-transcript-content escape valve. Override with the
# environment variable below.
MAX_STALE_BLOCKS_DEFAULT = 5


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        # On any error, allow stop (fail open)
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    # API errors are system failures, not voluntary stops - always allow
    if has_recent_api_error(transcript_path):
        sys.exit(0)

    state = parse_do_flow(transcript_path)

    # Not in /do flow - allow stop
    if not state.has_do:
        sys.exit(0)

    # /done was called - verified complete, allow stop
    if state.has_done:
        sys.exit(0)

    # /escalate was called — but Self-Amendment must continue to /define --amend
    if state.has_escalate and not state.has_self_amendment:
        sys.exit(0)

    # Self-Amendment escalation — block stop, must continue to /define --amend
    if state.has_self_amendment:
        output = {
            "decision": "block",
            "reason": "Self-Amendment in progress",
            "systemMessage": (
                "Stop blocked: Self-Amendment escalation requires "
                "/define --amend before stopping. Invoke "
                "/define --amend <manifest-path> to update the manifest, "
                "then resume /do."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # Non-local medium: /verify was called and escalation posted to the medium.
    # The user will re-invoke /do when the external blocker clears.
    if state.has_collab_mode and state.has_verify:
        output = {
            "reason": "Non-local medium: escalation posted to medium",
            "systemMessage": (
                "Escalation posted to the communication medium. "
                "The user will re-invoke /do with the execution log path "
                "when the external blocker clears."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # /do was called but neither /done nor /escalate
    # Check for infinite loop pattern before blocking
    consecutive_short = count_consecutive_short_outputs(transcript_path)

    # If we've had 3+ consecutive short outputs, we're in a loop - allow with warning
    if consecutive_short >= 3:
        output = {
            "reason": "Loop detected - allowing stop to prevent infinite loop",
            "systemMessage": (
                "WARNING: Stop allowed to break infinite loop. "
                "The /do workflow was NOT properly completed. "
                "Next time, call /escalate when blocked instead of minimal outputs."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # Transcript-stale escape valve. The short-output check above relies on
    # the model's `.` outputs being visible in the on-disk transcript, but
    # the transcript only flushes to disk at user-prompt boundaries — so a
    # long /do → /verify → /done chain with no user prompt between leaves
    # the model's recent invocations buffered in memory, invisible to this
    # hook. Counting our own block invocations (independent of transcript
    # content) catches that case: when we've blocked N times without the
    # transcript advancing, something needs human inspection regardless of
    # whether the buffered work succeeded or genuinely got stuck.
    session_id = hook_input.get("session_id", "default")
    max_stale_blocks = int(
        os.environ.get("MANIFEST_DEV_STOP_MAX_STALE_BLOCKS", MAX_STALE_BLOCKS_DEFAULT)
    )
    stale_blocks = record_stop_block(session_id, transcript_path)
    if stale_blocks >= max_stale_blocks:
        output = {
            "reason": (
                f"Allowed after {stale_blocks} blocks with no transcript movement"
            ),
            "systemMessage": (
                f"WARNING: Stop hook allowed after {stale_blocks} consecutive "
                "blocks without the on-disk transcript advancing. Two likely "
                "causes:\n"
                "  (a) The model's /verify or /done invocations completed but "
                "the transcript hasn't flushed them to disk (Claude Code "
                "flushes the .jsonl on user-prompt boundaries; long workflows "
                "with no user input keep the buffer in memory). Work may "
                "actually be complete — inspect the execution log "
                "(/tmp/do-log-*.md) for the /verify outcome.\n"
                "  (b) The model is genuinely stuck and not calling /done or "
                "/escalate. Treat the run as incomplete and check "
                "Deliverables.\n"
                "Override threshold via MANIFEST_DEV_STOP_MAX_STALE_BLOCKS "
                f"(default {MAX_STALE_BLOCKS_DEFAULT})."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # Provide guidance - same message regardless of attempt count
    # Clear directive: /verify or /escalate, nothing else
    system_message = (
        "Stop blocked: /do workflow requires formal exit. "
        "Options: (1) Run /verify to check criteria - if all pass, /verify calls /done. "
        "(2) Call /escalate - for blocking issues OR user-requested pauses. "
        "Short outputs will be blocked. Choose one."
    )

    output = {
        "decision": "block",
        "reason": "Execution not verified",
        "systemMessage": system_message,
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
