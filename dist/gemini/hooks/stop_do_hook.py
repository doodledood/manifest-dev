#!/usr/bin/env python3
"""
AfterAgent hook that enforces definition completion workflow for /do.

Gemini CLI adaptation: Registered as AfterAgent hook.
Uses decision: "deny" with reason to force retry (Gemini's retry protocol).
Implements retry counter via file to prevent infinite loops (Gemini has no
built-in retry limit).

Decision matrix:
- API error: ALLOW (system failure, not voluntary stop)
- No /do: ALLOW (not in flow)
- /do + /done: ALLOW (verified complete)
- /do + /escalate: ALLOW (properly escalated)
- /do + /verify + non-local medium: ALLOW (escalation posted to medium)
- /do only: DENY (must verify first)
- /do + /verify only: DENY (verify returned failures, keep working)
"""

from __future__ import annotations

import json
import os
import sys

from hook_utils import (
    count_consecutive_short_outputs,
    has_recent_api_error,
    parse_do_flow,
)

# Retry counter file to prevent infinite loops
RETRY_COUNTER_FILE = "/tmp/manifest-dev-stop-retry-count"
MAX_RETRIES = 5


def _get_retry_count() -> int:
    """Get current retry count from file."""
    try:
        with open(RETRY_COUNTER_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def _set_retry_count(count: int) -> None:
    """Set retry count in file."""
    with open(RETRY_COUNTER_FILE, "w") as f:
        f.write(str(count))


def _reset_retry_count() -> None:
    """Reset retry counter."""
    try:
        os.remove(RETRY_COUNTER_FILE)
    except FileNotFoundError:
        pass


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        # On any error, allow stop (fail open)
        _reset_retry_count()
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        _reset_retry_count()
        sys.exit(0)

    # API errors are system failures, not voluntary stops - always allow
    if has_recent_api_error(transcript_path):
        _reset_retry_count()
        sys.exit(0)

    state = parse_do_flow(transcript_path)

    # Not in /do flow - allow stop
    if not state.has_do:
        _reset_retry_count()
        sys.exit(0)

    # /done was called - verified complete, allow stop
    if state.has_done:
        _reset_retry_count()
        sys.exit(0)

    # /escalate was called — but Self-Amendment must continue to /define --amend
    if state.has_escalate and not state.has_self_amendment:
        _reset_retry_count()
        sys.exit(0)

    # Self-Amendment escalation — deny, must continue to /define --amend
    if state.has_self_amendment:
        retry_count = _get_retry_count() + 1
        _set_retry_count(retry_count)

        if retry_count >= MAX_RETRIES:
            _reset_retry_count()
            sys.exit(0)  # Allow after max retries to prevent infinite loop

        output = {
            "decision": "deny",
            "reason": (
                "Self-Amendment in progress. "
                "Invoke /define --amend <manifest-path> to update the manifest, "
                "then resume /do."
            ),
            "systemMessage": (
                "Stop blocked: Self-Amendment escalation requires "
                "/define --amend before stopping."
            ),
        }
        print(json.dumps(output))
        sys.exit(2)

    # Non-local medium: /verify was called and escalation posted to the medium.
    if state.has_collab_mode and state.has_verify:
        _reset_retry_count()
        output = {
            "decision": "allow",
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

    if consecutive_short >= 3:
        _reset_retry_count()
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

    # Check retry counter
    retry_count = _get_retry_count() + 1
    _set_retry_count(retry_count)

    if retry_count >= MAX_RETRIES:
        _reset_retry_count()
        sys.exit(0)  # Allow after max retries

    # Deny with reason — becomes new prompt for retry
    reason = (
        "Stop blocked: /do workflow requires formal exit. "
        "Options: (1) Run /verify to check criteria - if all pass, /verify calls /done. "
        "(2) Call /escalate - for blocking issues OR user-requested pauses. "
        "Short outputs will be blocked. Choose one."
    )

    output = {
        "decision": "deny",
        "reason": reason,
        "systemMessage": reason,
    }
    print(json.dumps(output))
    sys.exit(2)


if __name__ == "__main__":
    main()
