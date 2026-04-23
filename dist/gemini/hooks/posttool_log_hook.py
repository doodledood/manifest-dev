#!/usr/bin/env python3
"""
AfterTool hook that reminds the model to update the execution log.

Gemini CLI adaptation: Registered as AfterTool hook with matchers
for activate_skill and write_todos.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from hook_utils import build_system_reminder, parse_do_flow

# Skills that represent workflow transitions worth logging
WORKFLOW_SKILLS = {"verify", "escalate", "done", "define"}

LOG_REMINDER = """A milestone-shaped tool call appears to have just completed during /do.

Tool: {tool_name}{skill_detail}

If this call introduced new state, decisions, or outcomes not already in the execution log, writing them preserves the record — the log is disaster recovery if context is lost. If the call was routine and already reflected there (or nothing meaningful changed), skip this reminder."""


def _is_workflow_skill(tool_input: dict[str, Any]) -> bool:
    """Check if a skill call is a workflow-significant skill."""
    skill = tool_input.get("skill", "")
    skill_base = skill.split(":")[-1] if ":" in skill else skill
    return skill_base in WORKFLOW_SKILLS


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    transcript_path = hook_input.get("transcript_path", "")

    if not transcript_path:
        sys.exit(0)

    # For skill calls (activate_skill), only remind for workflow-significant skills
    if tool_name == "activate_skill":
        tool_input = hook_input.get("tool_input", {})
        if not _is_workflow_skill(tool_input):
            sys.exit(0)

    # Check if /do is active
    state = parse_do_flow(transcript_path)

    if not state.has_do or state.has_done:
        sys.exit(0)

    # Build skill detail for the reminder
    skill_detail = ""
    if tool_name == "activate_skill":
        tool_input = hook_input.get("tool_input", {})
        skill = tool_input.get("skill", "")
        skill_detail = f" (skill: {skill})"

    reminder = LOG_REMINDER.format(tool_name=tool_name, skill_detail=skill_detail)
    context = build_system_reminder(reminder)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "AfterTool",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
