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

from hook_utils import has_recent_api_error, parse_do_flow


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
    # Block with guidance
    output = {
        "decision": "block",
        "reason": "Execution not verified",
        "systemMessage": (
            "Cannot stop - /do workflow is incomplete. "
            "Run /verify to check acceptance criteria. "
            "If all criteria pass, /verify will call /done. "
            "If genuinely stuck after /verify, call /escalate with evidence."
        ),
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
