#!/usr/bin/env python3
"""
Post-compact hook that restores workflow context after compaction.

Gemini CLI adaptation: Registered as PreCompress or SessionStart hook.
Uses Gemini's additionalContext for context injection.
"""

from __future__ import annotations

import json
import sys

from hook_utils import (
    build_system_reminder,
    parse_do_flow,
    parse_thinking_disciplines_flow,
)

DO_WORKFLOW_RECOVERY_REMINDER = """This session appears to have been compacted during an active /do workflow — context from before compaction may be missing.

The /do was invoked with: {do_args}

If deliverables or acceptance criteria aren't currently in context, reading the manifest and any `/tmp/do-log-*.md` execution log restores progress and prevents restarting completed work. If both are already loaded from post-compact context, skip the re-read and resume from where you left off. If this hook is misreading and the session was never mid-/do, proceed normally."""


DO_WORKFLOW_RECOVERY_FALLBACK = """This session appears to have been compacted during an active /do workflow — context from before compaction may be missing.

If orientation is missing, checking `/tmp/` for an execution log matching `do-log-*.md` should surface both the manifest path (referenced in the log) and progress so far. If orientation is already intact, skip the re-read. If this hook is misreading and the session was never mid-/do, proceed normally."""


THINKING_DISCIPLINES_RECOVERY_REMINDER = """Thinking disciplines are active. Re-read the thinking-disciplines skill to restore your cognitive stance."""


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)

        transcript_path = hook_input.get("transcript_path", "")

        if not transcript_path:
            sys.exit(0)

        do_state = parse_do_flow(transcript_path)
        thinking_state = parse_thinking_disciplines_flow(transcript_path)

        reminders: list[str] = []

        # Active /do workflow - build recovery reminder
        if do_state.has_do and not do_state.has_done and not do_state.has_escalate:
            if do_state.do_args:
                reminders.append(
                    DO_WORKFLOW_RECOVERY_REMINDER.format(do_args=do_state.do_args)
                )
            else:
                reminders.append(DO_WORKFLOW_RECOVERY_FALLBACK)

        # Active thinking disciplines - build re-grounding reminder
        if thinking_state.is_active:
            reminders.append(THINKING_DISCIPLINES_RECOVERY_REMINDER)

        if not reminders:
            sys.exit(0)

        context = build_system_reminder("\n\n".join(reminders))

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
