#!/usr/bin/env python3
"""
PostToolUse hook that reminds Claude to update the execution log.

When a milestone tool call completes during an active /do workflow, this hook
injects a system reminder to log what just happened. Targets progress signals:
- TaskUpdate, TaskCreate, TodoWrite — task management milestones
- Skill calls (verify, escalate, done, define) — workflow transitions

Registered as PostToolUse hook with matchers for each target tool.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from hook_utils import build_system_reminder, parse_do_flow

# Skills that represent workflow transitions worth logging
WORKFLOW_SKILLS = {"verify", "escalate", "done", "define"}

LOG_REMINDER = """LOG REMINDER: A milestone just completed during /do.

Tool: {tool_name}{skill_detail}

Update the execution log NOW with what just happened, decisions made, and outcomes. The log is disaster recovery — if context is lost, only the log survives."""


def _is_workflow_skill(tool_input: dict[str, Any]) -> bool:
    """Check if a Skill call is a workflow-significant skill."""
    skill = tool_input.get("skill", "")
    # Match "skill-name" or "plugin:skill-name"
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

    # For Skill calls, only remind for workflow-significant skills
    if tool_name == "Skill":
        tool_input = hook_input.get("tool_input", {})
        if not _is_workflow_skill(tool_input):
            sys.exit(0)

    # Check if /do is active
    state = parse_do_flow(transcript_path)

    if not state.has_do or state.has_done:
        sys.exit(0)

    # Build skill detail for the reminder
    skill_detail = ""
    if tool_name == "Skill":
        tool_input = hook_input.get("tool_input", {})
        skill = tool_input.get("skill", "")
        skill_detail = f" (skill: {skill})"

    reminder = LOG_REMINDER.format(tool_name=tool_name, skill_detail=skill_detail)
    context = build_system_reminder(reminder)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
