#!/usr/bin/env python3
"""
UserPromptSubmit hook that reminds Claude to check for manifest amendments.

When user submits a message during an active /do workflow, this hook injects
a system reminder to check if the input contradicts or extends the manifest.
If so, /do should escalate and invoke /define --amend.

Registered as UserPromptSubmit hook (no matcher — fires on every prompt).
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder, parse_do_flow

AMENDMENT_CHECK_REMINDER = """AMENDMENT CHECK: You are in an active /do workflow and the user just submitted input.

Before continuing execution, check if this user input:
1. **Contradicts** an existing AC, INV, or PG in the manifest
2. **Extends** the manifest with new requirements not currently covered
3. **Amends** the scope or approach in a way that changes what "done" means

If YES to any: Call /escalate with Self-Amendment type, then immediately invoke /define --amend <manifest-path>. After /define returns, resume /do with the updated manifest.

If NO (clarification, confirmation, or unrelated): Continue execution normally."""


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    # Check if /do is active
    state = parse_do_flow(transcript_path)

    # Only inject when /do is active and not yet completed
    if not state.has_do or state.has_done:
        sys.exit(0)

    context = build_system_reminder(AMENDMENT_CHECK_REMINDER)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
