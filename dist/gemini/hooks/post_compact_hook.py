#!/usr/bin/env python3
"""
Post-compact hook: restore /do workflow context after compaction.

When the session is compacted during an active /do workflow, context may be
lost. This hook injects a terse reminder to re-read the manifest.

Registered as SessionStart hook with "compact" matcher.
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder, parse_do_flow

DO_WORKFLOW_RECOVERY_REMINDER = (
    "Session compacted mid-/do — re-read the manifest at {do_args} to "
    "restore Deliverables and Acceptance Criteria before continuing."
)

DO_WORKFLOW_RECOVERY_FALLBACK = (
    "Session compacted mid-/do — re-read the manifest (path was passed "
    "as the first positional argument to /do) to restore Deliverables "
    "and Acceptance Criteria before continuing."
)


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)

        transcript_path = hook_input.get("transcript_path", "")
        if not transcript_path:
            sys.exit(0)

        do_state = parse_do_flow(transcript_path)

        # Only fire when /do is active and not yet completed
        if not (
            do_state.has_do and not do_state.has_done and not do_state.has_escalate
        ):
            sys.exit(0)

        if do_state.do_args:
            reminder = DO_WORKFLOW_RECOVERY_REMINDER.format(do_args=do_state.do_args)
        else:
            reminder = DO_WORKFLOW_RECOVERY_FALLBACK

        context = build_system_reminder(reminder)

        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
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
