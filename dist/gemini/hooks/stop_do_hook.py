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
- /do only: BLOCK (must verify first)
- /do + /verify only: BLOCK (verify returned failures, keep working)
"""

from __future__ import annotations

import json
import sys

from hook_utils import (
    count_consecutive_short_outputs,
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

    # /escalate was called - properly escalated, allow stop
    if state.has_escalate:
        sys.exit(0)

    # /do was called but neither /done nor /escalate
    # Check for infinite loop pattern before blocking
    consecutive_short = count_consecutive_short_outputs(transcript_path)

    # If we've had 3+ consecutive short outputs, we're in a loop - allow with warning
    if consecutive_short >= 3:
        output = {
            "decision": "allow",
            "reason": "Loop detected - allowing stop to prevent infinite loop",
            "systemMessage": (
                "WARNING: Stop allowed to break infinite loop. "
                "The /do workflow was NOT properly completed. "
                "Next time, call /escalate when blocked instead of minimal outputs."
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
