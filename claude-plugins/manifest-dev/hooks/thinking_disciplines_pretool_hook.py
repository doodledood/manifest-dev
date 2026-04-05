#!/usr/bin/env python3
"""
PreToolUse hook that reinforces thinking disciplines before AskUserQuestion.

When thinking disciplines are active, injects a compressed principles reminder
before Claude asks the user a question — the moment where sycophantic drift
and premature convergence are most likely.

Registered as PreToolUse hook matched on AskUserQuestion.
"""

from __future__ import annotations

import json
import sys

from thinking_disciplines_prompt_hook import THINKING_DISCIPLINES_REMINDER

from hook_utils import build_system_reminder, parse_thinking_disciplines_flow


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)

        transcript_path = hook_input.get("transcript_path", "")
        if not transcript_path:
            sys.exit(0)

        state = parse_thinking_disciplines_flow(transcript_path)

        if not state.is_active:
            sys.exit(0)

        context = build_system_reminder(THINKING_DISCIPLINES_REMINDER)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
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
