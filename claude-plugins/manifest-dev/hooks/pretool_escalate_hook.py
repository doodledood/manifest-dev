#!/usr/bin/env python3
"""
PreToolUse hook that gates /escalate calls.

Blocks /escalate unless /verify was called first after /do.
This prevents lazy escalation without attempting verification.

Decision matrix:
- No /do: BLOCK (no flow to escalate from)
- /do + /verify: ALLOW (genuinely tried)
- /do only: BLOCK (must verify first)
"""

from __future__ import annotations

import json
import sys

from hook_utils import parse_do_flow


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        # On any error, allow (fail open)
        sys.exit(0)

    # This hook only applies to Skill tool calls for "escalate"
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Skill":
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    skill = tool_input.get("skill", "")

    # Only gate escalate skill
    if skill != "escalate" and not skill.endswith(":escalate"):
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    state = parse_do_flow(transcript_path)

    # No /do in progress - can't escalate from nothing
    if not state.has_do:
        output = {
            "decision": "block",
            "reason": "No /do in progress",
            "systemMessage": (
                "Cannot escalate - no /do workflow is active. "
                "/escalate is only valid during a /do workflow."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    # /verify was called - allow escalation
    if state.has_verify:
        sys.exit(0)

    # /do was called but /verify was not
    output = {
        "decision": "block",
        "reason": "Must verify before escalating",
        "systemMessage": (
            "Cannot escalate - must call /verify first. "
            "Run /verify to check acceptance criteria, then escalate if genuinely stuck."
        ),
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
