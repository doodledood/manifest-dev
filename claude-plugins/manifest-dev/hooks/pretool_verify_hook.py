#!/usr/bin/env python3
"""
PreToolUse hook that reminds Claude to read manifest/log for verification.

When /verify is about to be called, this hook adds a system reminder to ensure
the manifest and execution log are in full context for accurate verification.
This is especially important after long sessions where manifest details may have
drifted from memory.

Registered as PreToolUse hook with "Skill" matcher.
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder

VERIFY_CONTEXT_REMINDER = """VERIFICATION CONTEXT CHECK: You are about to run /verify.

Arguments: {verify_args}

BEFORE spawning verifiers, read the manifest and execution log in FULL if not recently loaded. You need ALL acceptance criteria (AC-*) and global invariants (INV-G*) in context to spawn the correct verifiers."""


VERIFY_CONTEXT_REMINDER_MINIMAL = """VERIFICATION CONTEXT CHECK: You are about to run /verify.

BEFORE spawning verifiers, read the manifest and execution log in FULL if not recently loaded. You need ALL acceptance criteria (AC-*) and global invariants (INV-G*) in context to spawn the correct verifiers."""


def main() -> None:
    """Main hook entry point."""
    # Read hook input from stdin
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        sys.exit(0)

    # Only apply to Skill tool calls
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Skill":
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    skill = tool_input.get("skill", "")

    # Only gate verify skill
    if skill != "verify" and not skill.endswith(":verify"):
        sys.exit(0)

    # Get the raw arguments
    args = tool_input.get("args", "").strip()

    if args:
        reminder = VERIFY_CONTEXT_REMINDER.format(verify_args=args)
    else:
        reminder = VERIFY_CONTEXT_REMINDER_MINIMAL

    context = build_system_reminder(reminder)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
