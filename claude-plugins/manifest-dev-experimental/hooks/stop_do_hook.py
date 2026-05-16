#!/usr/bin/env python3
"""
Stop hook for the experimental plugin.

Blocks stop attempts unless /done or /escalate was called after /do.
Injects a terse "reload /do" reminder so the model can resume.

Decision matrix:
- API error: ALLOW (system failure, not voluntary stop)
- No /do: ALLOW (not in flow)
- /do + /done: ALLOW (manifest verified complete)
- /do + /escalate: ALLOW (properly escalated)
- /do + idle loop (>= 3 consecutive idle outputs): ALLOW (stuck, let user re-invoke)
- /do only: BLOCK with reload reminder
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
        # Fail open on parse error
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

    # /done or /escalate fired - allow stop
    if state.has_done or state.has_escalate:
        sys.exit(0)

    # Idle loop escape valve: if we've had 3+ consecutive idle outputs,
    # the model is stuck and blocking further would just spin.
    consecutive_idle = count_consecutive_idle_outputs(transcript_path)
    if consecutive_idle >= 3:
        output = {
            "reason": "Idle loop detected — allowing stop",
            "systemMessage": (
                "Idle loop detected — stop allowed. Re-invoke "
                "`/manifest-dev-experimental:do` when ready to continue."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # /do is active but unfinished - inject terse reload reminder and block.
    output = {
        "decision": "block",
        "reason": "Not done. Reload `/manifest-dev-experimental:do` to continue.",
        "systemMessage": (
            "Stop intercepted: /do appears active and unfinished — "
            "reload /manifest-dev-experimental:do to continue."
        ),
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
