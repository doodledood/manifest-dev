#!/usr/bin/env python3
"""
Post-compact hook that restores /do workflow context after compaction.

When the session is compacted during an active /do workflow, context may be
lost. This hook detects an active /do and reminds Claude to re-read the
manifest.

Registered as SessionStart hook with "compact" matcher.
"""

from __future__ import annotations

import json
import sys

from hook_utils import build_system_reminder, parse_do_flow

DO_WORKFLOW_RECOVERY_REMINDER = """This session appears to have been compacted during an active /do workflow — context from before compaction may be missing.

The /do was invoked with: {do_args}

If deliverables or acceptance criteria aren't currently in context, reading the manifest restores the plan and prevents restarting completed work. If it's already loaded from post-compact context, skip the re-read and resume from where you left off. If this hook is misreading and the session was never mid-/do, proceed normally."""


DO_WORKFLOW_RECOVERY_FALLBACK = """This session appears to have been compacted during an active /do workflow — context from before compaction may be missing.

If orientation is missing, the manifest path was passed as the first positional argument to /do — re-reading the manifest surfaces deliverables and acceptance criteria. If orientation is already intact, skip the re-read. If this hook is misreading and the session was never mid-/do, proceed normally."""


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)

        transcript_path = hook_input.get("transcript_path", "")

        # If no transcript, we can't detect workflows
        if not transcript_path:
            sys.exit(0)

        do_state = parse_do_flow(transcript_path)

        # Active /do workflow - build recovery reminder
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
