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
import sys

from hook_utils import (
    count_consecutive_idle_outputs,
    has_recent_api_error,
    parse_do_flow,
)


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
                "Self-Amendment in progress — the manifest needs updating "
                "before execution can continue. "
                "Run /define --amend <manifest-path> to apply the amendment, "
                "then resume /do with the updated manifest."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # Non-local medium: /verify was called and escalation posted to the medium.
    # The user will re-invoke /do when the external blocker clears.
    if state.has_collab_mode and state.has_verify:
        output = {
            "reason": "Non-local medium: escalation posted externally",
            "systemMessage": (
                "Verification results posted to the external review channel. "
                "The user will re-invoke /do with the execution log path "
                "once the blocker is resolved."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # /do was called but neither /done nor /escalate
    # Check for idle loop pattern before blocking
    consecutive_idle = count_consecutive_idle_outputs(transcript_path)

    # If we've had 3+ consecutive idle outputs (no tool use), we're stuck - allow
    if consecutive_idle >= 3:
        output = {
            "reason": "Idle loop detected — allowing stop",
            "systemMessage": (
                "Idle loop detected — stop allowed. "
                "If waiting for background agents, collect their results "
                "and resume with /verify. "
                "If genuinely blocked, call /escalate to formally pause."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # Provide guidance — clear directive toward /verify or /escalate
    system_message = (
        "Active /do workflow — formal exit required. "
        "If implementation is complete, run /verify to check criteria. "
        "If blocked or waiting for async work (background agents, external input), "
        "call /escalate to pause. "
        "Continuing without tool use will trigger the idle escape valve."
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
