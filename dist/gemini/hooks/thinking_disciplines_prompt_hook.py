#!/usr/bin/env python3
"""
BeforeAgent hook that reinforces thinking disciplines.

Gemini CLI adaptation: Registered as BeforeAgent hook (no matcher).
Uses Gemini's additionalContext for context injection.
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder, parse_thinking_disciplines_flow

THINKING_DISCIPLINES_REMINDER = """Thinking disciplines active. Truth over helpfulness. Investigate before engaging. Verified and inferred are different — name which. Contradictions are leads, not noise. Partial pictures produce confident-sounding wrong answers — map the territory before forming a view. Don't advocate for an approach you haven't verified. If you still disagree after genuine exchange, say so. If the user flags something, investigate — don't reassure."""


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
                "hookEventName": "BeforeAgent",
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
