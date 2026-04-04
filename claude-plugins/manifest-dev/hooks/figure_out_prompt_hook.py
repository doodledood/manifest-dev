#!/usr/bin/env python3
"""
UserPromptSubmit hook that reinforces /figure-out principles.

When user submits a message during an active /figure-out session, this hook
injects a concise system reminder to combat sycophantic drift and premature
convergence. The full skill is already in context — this is a nudge, not
re-teaching.

Registered as UserPromptSubmit hook (no matcher — fires on every prompt).
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder, parse_figure_out_flow

FIGURE_OUT_PRINCIPLES_REMINDER = """/figure-out active. Self-check before responding:
- Are you asking the user something you could investigate yourself?
- Are you claiming something you haven't verified?
- Do your claims and findings actually fit together, or are you smoothing over a contradiction?
- Are you agreeing just to be agreeable?
- Are you jumping to solutions before the problem is figured out?
- Are you filling the user's uncertainty with your confidence?

Principles: come prepared, name verified vs inferred, incoherence is a signal, sit with fog."""


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)

        transcript_path = hook_input.get("transcript_path", "")
        if not transcript_path:
            sys.exit(0)

        state = parse_figure_out_flow(transcript_path)

        # Only inject when /figure-out is active and not completed
        if not state.has_figure_out or state.is_complete:
            sys.exit(0)

        context = build_system_reminder(FIGURE_OUT_PRINCIPLES_REMINDER)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    except Exception:
        # Fail open — never block normal operation on error
        sys.exit(0)


if __name__ == "__main__":
    main()
