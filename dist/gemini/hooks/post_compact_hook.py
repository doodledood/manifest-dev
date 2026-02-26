#!/usr/bin/env python3
"""
Gemini CLI adaptation of post_compact_hook.

Restores /do workflow context after session compaction.
Registered as SessionStart hook.

Adapted from Claude Code version:
- Output format: top-level systemMessage (Gemini protocol)
"""

from __future__ import annotations

import json
import sys

from hook_utils import (
    build_system_reminder,
    parse_do_flow,
)

DO_WORKFLOW_RECOVERY_REMINDER = """This session was compacted during an active /do workflow. Context may have been lost.

CRITICAL: Before continuing, read the manifest and execution log in FULL.

The /do was invoked with: {do_args}

1. Read the manifest file - contains deliverables, acceptance criteria, and approach
2. Check /tmp/ for your execution log (do-log-*.md) and read it to recover progress

Do not restart completed work. Resume from where you left off."""

DO_WORKFLOW_RECOVERY_FALLBACK = """This session was compacted during an active /do workflow. Context may have been lost.

CRITICAL: Before continuing, recover your workflow context:

1. Check /tmp/ for execution logs matching do-log-*.md
2. The log references the manifest file path - read both in FULL

Do not restart completed work. Resume from where you left off."""


def main() -> None:
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        hook_input = {}

    transcript_path = hook_input.get("transcript_path", "")

    if not transcript_path:
        sys.exit(0)

    state = parse_do_flow(transcript_path)

    if not state.has_do:
        sys.exit(0)

    if state.has_done or state.has_escalate:
        sys.exit(0)

    if state.do_args:
        reminder = DO_WORKFLOW_RECOVERY_REMINDER.format(do_args=state.do_args)
    else:
        reminder = DO_WORKFLOW_RECOVERY_FALLBACK

    context = build_system_reminder(reminder)

    output = {"systemMessage": context}
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
