#!/usr/bin/env python3
"""
Gemini CLI adapter for manifest-dev hooks.

Translates between Claude Code hook protocol and Gemini CLI hook protocol.
Wraps existing hook logic so the same behavioral intent works on both platforms.

Claude Code → Gemini CLI translations:
- hookSpecificOutput.permissionDecision: "deny" → top-level decision: "deny"
- hookSpecificOutput.permissionDecisionReason → reason
- hookSpecificOutput.additionalContext → hookSpecificOutput.additionalContext
- decision: "block" (Stop hook) → decision: "deny" with reason (AfterAgent)
- transcript_path parsing: JSONL with user/gemini types instead of user/assistant
- Tool names: Skill → activate_skill, Bash/BashOutput → run_shell_command, etc.

Gemini CLI protocol:
- Input: JSON on stdin
- Output: JSON on stdout (NOTHING else — debug on stderr only)
- Exit codes: 0 = success, 1 = non-blocking warning, 2+ = blocking
"""

from __future__ import annotations

import json
import sys
from typing import Any

# Claude Code → Gemini CLI tool name mapping
TOOL_NAME_MAP = {
    "Skill": "activate_skill",
    "Bash": "run_shell_command",
    "BashOutput": "run_shell_command",
    "Read": "read_file",
    "Write": "write_file",
    "Edit": "replace",
    "Grep": "grep_search",
    "Glob": "glob",
    "WebFetch": "web_fetch",
    "WebSearch": "google_web_search",
    "TodoWrite": "write_todos",
    "TodoRead": "write_todos",
    "TaskCreate": "write_todos",
    "TaskUpdate": "write_todos",
    "TaskGet": "write_todos",
    "TaskList": "write_todos",
    "AskUserQuestion": "ask_user",
}

# Reverse mapping for input translation
GEMINI_TO_CLAUDE_TOOL = {v: k for k, v in TOOL_NAME_MAP.items()}
# Fix: activate_skill should map to Skill
GEMINI_TO_CLAUDE_TOOL["activate_skill"] = "Skill"
GEMINI_TO_CLAUDE_TOOL["run_shell_command"] = "Bash"


def read_gemini_input() -> dict[str, Any]:
    """Read and parse Gemini CLI hook input from stdin."""
    try:
        stdin_data = sys.stdin.read()
        return json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        return {}


def translate_input_to_claude(gemini_input: dict[str, Any]) -> dict[str, Any]:
    """
    Translate Gemini CLI hook input to Claude Code hook input format.

    Gemini provides: session_id, transcript_path, cwd, hook_event_name, timestamp,
                     tool_name, tool_input, prompt, etc.
    Claude expects: tool_name (PascalCase), tool_input, transcript_path, etc.
    """
    claude_input = dict(gemini_input)

    # Translate tool names from Gemini to Claude format
    tool_name = gemini_input.get("tool_name", "")
    if tool_name in GEMINI_TO_CLAUDE_TOOL:
        claude_input["tool_name"] = GEMINI_TO_CLAUDE_TOOL[tool_name]

    return claude_input


def translate_output_to_gemini(
    claude_output: dict[str, Any],
    event_type: str,
) -> dict[str, Any]:
    """
    Translate Claude Code hook output to Gemini CLI hook output format.

    Key translations:
    - Claude's hookSpecificOutput.permissionDecision → Gemini's top-level decision
    - Claude's decision: "block" → Gemini's decision: "deny"
    - Claude's systemMessage stays as systemMessage
    - Claude's additionalContext → Gemini's hookSpecificOutput.additionalContext
    """
    gemini_output: dict[str, Any] = {}

    # Handle top-level decision
    decision = claude_output.get("decision")
    if decision == "block":
        gemini_output["decision"] = "deny"
    elif decision == "allow":
        gemini_output["decision"] = "allow"

    # Handle reason
    reason = claude_output.get("reason")
    if reason:
        gemini_output["reason"] = reason

    # Handle systemMessage (displayed to user, not injected into model)
    system_message = claude_output.get("systemMessage")
    if system_message:
        gemini_output["systemMessage"] = system_message

    # Handle hookSpecificOutput
    hook_specific = claude_output.get("hookSpecificOutput", {})

    if hook_specific:
        gemini_hook_specific: dict[str, Any] = {}

        # Map hookEventName
        claude_event = hook_specific.get("hookEventName", "")
        event_map = {
            "PreToolUse": "BeforeTool",
            "PostToolUse": "AfterTool",
            "SessionStart": "SessionStart",
            "UserPromptSubmit": "BeforeAgent",
        }
        gemini_event = event_map.get(claude_event, event_type)
        gemini_hook_specific["hookEventName"] = gemini_event

        # Permission decision → top-level decision
        perm_decision = hook_specific.get("permissionDecision")
        if perm_decision == "deny":
            gemini_output["decision"] = "deny"
        perm_reason = hook_specific.get("permissionDecisionReason")
        if perm_reason:
            gemini_output["reason"] = perm_reason

        # additionalContext passes through
        additional_context = hook_specific.get("additionalContext")
        if additional_context:
            gemini_hook_specific["additionalContext"] = additional_context

        # tool_input override passes through for BeforeTool
        tool_input = hook_specific.get("tool_input")
        if tool_input:
            gemini_hook_specific["tool_input"] = tool_input

        if gemini_hook_specific:
            gemini_output["hookSpecificOutput"] = gemini_hook_specific

    return gemini_output


def output_and_exit(output: dict[str, Any], blocking: bool = False) -> None:
    """Write JSON output to stdout and exit with appropriate code."""
    if output:
        print(json.dumps(output))

    # Exit code: 0 = success, 2 = blocking
    if blocking:
        sys.exit(2)
    else:
        sys.exit(0)
