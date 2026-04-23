#!/usr/bin/env python3
"""
BeforeAgent hook that reminds the model to check for manifest amendments.

Gemini CLI adaptation: Registered as BeforeAgent hook (no matcher).
Uses Gemini's additionalContext for context injection.
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder, parse_do_flow

AMENDMENT_CHECK_REMINDER = """A user message arrived during what looks like an active /do workflow.

Before continuing execution, it's worth checking whether the input might:
- **contradict** an existing AC, INV, or PG in the manifest
- **extend** the manifest with new requirements not currently covered
- **amend** the scope or approach in a way that changes what "done" means

If any of those look likely: /escalate with Self-Amendment type, then invoke /define --amend <manifest-path>. After /define returns, resume /do with the updated manifest.

If the input reads more like clarification, confirmation, or unrelated context (or if this hook is misreading the state and /do is already closed), continue execution normally."""


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
            "hookEventName": "BeforeAgent",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
