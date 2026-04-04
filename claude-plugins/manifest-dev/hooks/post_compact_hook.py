#!/usr/bin/env python3
"""
Post-compact hook that restores workflow context after compaction.

When the session is compacted during an active /do or /figure-out workflow,
context may be lost. This hook detects active workflows and reminds Claude
to re-read relevant files and restore the correct cognitive stance.

Registered as SessionStart hook with "compact" matcher.
"""

from __future__ import annotations

import json
import sys

from hook_utils import (
    build_system_reminder,
    parse_do_flow,
    parse_figure_out_flow,
)

DO_WORKFLOW_RECOVERY_REMINDER = """This session was compacted during an active /do workflow. Context may have been lost.

CRITICAL: Before continuing, read the manifest and execution log in FULL.

The /do was invoked with: {do_args}

1. Read the manifest file - contains deliverables, acceptance criteria, and approach
2. Check /tmp/ for your execution log (do-log-*.md) and read it to recover progress

Do not restart completed work. Resume from where you left off."""


FIGURE_OUT_RECOVERY_REMINDER_PREFIX = """This session was compacted during an active /figure-out session. Context may have been lost.

You are in a /figure-out session about: """

FIGURE_OUT_RECOVERY_REMINDER_SUFFIX = """

Re-read the /figure-out skill to restore your cognitive stance. Truth-convergence is your north star — come prepared, incoherence is a signal, resist premature synthesis."""


FIGURE_OUT_RECOVERY_FALLBACK = """This session was compacted during an active /figure-out session. Context may have been lost.

Re-read the /figure-out skill to restore your cognitive stance. Truth-convergence is your north star — come prepared, incoherence is a signal, resist premature synthesis."""


DO_WORKFLOW_RECOVERY_FALLBACK = """This session was compacted during an active /do workflow. Context may have been lost.

CRITICAL: Before continuing, recover your workflow context:

1. Check /tmp/ for execution logs matching do-log-*.md
2. The log references the manifest file path - read both in FULL

Do not restart completed work. Resume from where you left off."""


def main() -> None:
    """Main hook entry point."""
    # Read hook input from stdin
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        hook_input = {}

    transcript_path = hook_input.get("transcript_path", "")

    # If no transcript, we can't detect /do workflow
    if not transcript_path:
        sys.exit(0)

    do_state = parse_do_flow(transcript_path)
    figure_out_state = parse_figure_out_flow(transcript_path)

    reminders: list[str] = []

    # Active /do workflow - build recovery reminder
    if do_state.has_do and not do_state.has_done and not do_state.has_escalate:
        if do_state.do_args:
            reminders.append(
                DO_WORKFLOW_RECOVERY_REMINDER.format(do_args=do_state.do_args)
            )
        else:
            reminders.append(DO_WORKFLOW_RECOVERY_FALLBACK)

    # Active /figure-out session - build re-grounding reminder
    if figure_out_state.has_figure_out and not figure_out_state.is_complete:
        if figure_out_state.figure_out_args:
            reminders.append(
                FIGURE_OUT_RECOVERY_REMINDER_PREFIX
                + figure_out_state.figure_out_args
                + FIGURE_OUT_RECOVERY_REMINDER_SUFFIX
            )
        else:
            reminders.append(FIGURE_OUT_RECOVERY_FALLBACK)

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


if __name__ == "__main__":
    main()
