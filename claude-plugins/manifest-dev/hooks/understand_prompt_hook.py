#!/usr/bin/env python3
"""
UserPromptSubmit hook that reinforces /understand principles.

When user submits a message during an active /understand session, this hook
injects a concise system reminder to combat sycophantic drift and premature
convergence. The full skill is already in context — this is a nudge, not
re-teaching.

Registered as UserPromptSubmit hook (no matcher — fires on every prompt).
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder, parse_understand_flow

UNDERSTAND_PRINCIPLES_REMINDER = """Active /understand session. Truth-convergence is your north star.

Investigate before claiming. Name what you verified vs what you're inferring. If something doesn't fit, surface it. If the user flags something feels off, investigate — don't reassure. Resist the pull to solve or synthesize prematurely."""


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)

        transcript_path = hook_input.get("transcript_path", "")
        if not transcript_path:
            sys.exit(0)

        state = parse_understand_flow(transcript_path)

        # Only inject when /understand is active and not completed
        if not state.has_understand or state.is_complete:
            sys.exit(0)

        context = build_system_reminder(UNDERSTAND_PRINCIPLES_REMINDER)

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
