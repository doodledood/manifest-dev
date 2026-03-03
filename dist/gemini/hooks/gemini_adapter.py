#!/usr/bin/env python3
"""
Gemini CLI hook adapter.

Thin translation layer between Gemini CLI hook protocol and existing
Claude Code hook scripts. Maps events, tool names, and output formats
so the same Python hook logic works on both CLIs.

Usage:
    python3 gemini_adapter.py <event>

Events:
    BeforeTool   - maps to pretool_verify_hook (PreToolUse equivalent)
    AfterAgent   - maps to stop_do_hook (Stop equivalent)
    SessionStart - maps to post_compact_hook (SessionStart equivalent)

Protocol:
    Input:  JSON on stdin (Gemini hook format)
    Output: JSON on stdout (Gemini hook format)
    Exit:   0 = success, 2 = system block
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

# --------------------------------------------------------------------------- #
# Tool-name mapping (Gemini -> Claude Code)
# --------------------------------------------------------------------------- #

GEMINI_TO_CLAUDE_TOOLS: dict[str, str] = {
    "run_shell_command": "Bash",
    "read_file": "Read",
    "write_file": "Write",
    "replace": "Edit",
    "grep_search": "Grep",
    "glob": "Glob",
    "web_fetch": "WebFetch",
    "google_web_search": "WebSearch",
    "activate_skill": "Skill",
    "write_todos": "TaskCreate",
    "ask_user": "AskUserQuestion",
    "enter_plan_mode": "EnterPlanMode",
    "exit_plan_mode": "ExitPlanMode",
}

CLAUDE_TO_GEMINI_TOOLS: dict[str, str] = {v: k for k, v in GEMINI_TO_CLAUDE_TOOLS.items()}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _translate_input(gemini_input: dict[str, Any], event: str) -> dict[str, Any]:
    """Convert Gemini hook input to the format Claude Code hooks expect."""
    claude_input: dict[str, Any] = {}

    # Universal fields
    claude_input["transcript_path"] = gemini_input.get("transcript_path", "")
    claude_input["cwd"] = gemini_input.get("cwd", os.getcwd())
    claude_input["session_id"] = gemini_input.get("session_id", "")

    if event == "BeforeTool":
        # Map tool_name back to Claude Code names
        gemini_tool = gemini_input.get("tool_name", "")
        claude_input["tool_name"] = GEMINI_TO_CLAUDE_TOOLS.get(gemini_tool, gemini_tool)
        claude_input["tool_input"] = gemini_input.get("tool_input", {})

    elif event == "AfterAgent":
        # Stop equivalent -- pass through prompt info
        claude_input["prompt"] = gemini_input.get("prompt", "")
        claude_input["prompt_response"] = gemini_input.get("prompt_response", "")

    elif event == "SessionStart":
        claude_input["source"] = gemini_input.get("source", "startup")

    return claude_input


def _translate_output(claude_output: dict[str, Any], event: str) -> dict[str, Any]:
    """Convert Claude Code hook output to Gemini hook format."""
    gemini_output: dict[str, Any] = {}

    # Map permission decision to Gemini's decision field
    hook_specific = claude_output.get("hookSpecificOutput", {})

    if event == "BeforeTool":
        perm = hook_specific.get("permissionDecision", "")
        if perm == "deny":
            gemini_output["decision"] = "deny"
            gemini_output["reason"] = hook_specific.get(
                "permissionDecisionReason", "Blocked by hook"
            )
        # Pass through additionalContext
        ctx = hook_specific.get("additionalContext", "")
        if ctx:
            gemini_output["hookSpecificOutput"] = {"additionalContext": ctx}

    elif event == "AfterAgent":
        decision = claude_output.get("decision", "")
        if decision == "block":
            gemini_output["decision"] = "deny"
            gemini_output["reason"] = claude_output.get("reason", "")
        elif decision == "allow":
            gemini_output["decision"] = "allow"

        msg = claude_output.get("systemMessage", "")
        if msg:
            gemini_output["systemMessage"] = msg

    elif event == "SessionStart":
        ctx = hook_specific.get("additionalContext", "")
        if ctx:
            gemini_output["hookSpecificOutput"] = {"additionalContext": ctx}

    return gemini_output


# --------------------------------------------------------------------------- #
# Event dispatchers
# --------------------------------------------------------------------------- #


def _run_before_tool(gemini_input: dict[str, Any]) -> None:
    """Dispatch BeforeTool -> pretool_verify_hook."""
    claude_input = _translate_input(gemini_input, "BeforeTool")

    # Only process activate_skill (Skill) calls
    if claude_input.get("tool_name") != "Skill":
        sys.exit(0)

    # Import and delegate to the existing hook
    from pretool_verify_hook import main as _pretool_main
    from unittest.mock import patch
    import io

    stdin_data = json.dumps(claude_input)
    captured = io.StringIO()

    try:
        with patch("sys.stdin", io.StringIO(stdin_data)), \
             patch("sys.stdout", captured), \
             patch("sys.exit") as mock_exit:
            _pretool_main()
    except SystemExit:
        pass

    claude_output_str = captured.getvalue().strip()
    if claude_output_str:
        try:
            claude_output = json.loads(claude_output_str)
            gemini_output = _translate_output(claude_output, "BeforeTool")
            if gemini_output:
                print(json.dumps(gemini_output))
        except json.JSONDecodeError:
            pass

    sys.exit(0)


def _run_after_agent(gemini_input: dict[str, Any]) -> None:
    """Dispatch AfterAgent -> stop_do_hook."""
    claude_input = _translate_input(gemini_input, "AfterAgent")

    from stop_do_hook import main as _stop_main
    from unittest.mock import patch
    import io

    stdin_data = json.dumps(claude_input)
    captured = io.StringIO()

    try:
        with patch("sys.stdin", io.StringIO(stdin_data)), \
             patch("sys.stdout", captured), \
             patch("sys.exit") as mock_exit:
            _stop_main()
    except SystemExit:
        pass

    claude_output_str = captured.getvalue().strip()
    if claude_output_str:
        try:
            claude_output = json.loads(claude_output_str)
            gemini_output = _translate_output(claude_output, "AfterAgent")
            if gemini_output:
                print(json.dumps(gemini_output))
                # If blocking, exit 2 so Gemini retries
                if gemini_output.get("decision") == "deny":
                    sys.exit(2)
        except json.JSONDecodeError:
            pass

    sys.exit(0)


def _run_session_start(gemini_input: dict[str, Any]) -> None:
    """Dispatch SessionStart -> post_compact_hook."""
    claude_input = _translate_input(gemini_input, "SessionStart")

    from post_compact_hook import main as _compact_main
    from unittest.mock import patch
    import io

    stdin_data = json.dumps(claude_input)
    captured = io.StringIO()

    try:
        with patch("sys.stdin", io.StringIO(stdin_data)), \
             patch("sys.stdout", captured), \
             patch("sys.exit") as mock_exit:
            _compact_main()
    except SystemExit:
        pass

    claude_output_str = captured.getvalue().strip()
    if claude_output_str:
        try:
            claude_output = json.loads(claude_output_str)
            gemini_output = _translate_output(claude_output, "SessionStart")
            if gemini_output:
                print(json.dumps(gemini_output))
        except json.JSONDecodeError:
            pass

    sys.exit(0)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> None:
    """Entry point. First CLI arg is the Gemini event name."""
    if len(sys.argv) < 2:
        print("Usage: gemini_adapter.py <event>", file=sys.stderr)
        sys.exit(1)

    event = sys.argv[1]

    try:
        stdin_data = sys.stdin.read()
        gemini_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except (json.JSONDecodeError, OSError):
        gemini_input = {}

    # Add the hooks directory to sys.path so imports work
    hooks_dir = os.path.dirname(os.path.abspath(__file__))
    if hooks_dir not in sys.path:
        sys.path.insert(0, hooks_dir)

    if event == "BeforeTool":
        _run_before_tool(gemini_input)
    elif event == "AfterAgent":
        _run_after_agent(gemini_input)
    elif event == "SessionStart":
        _run_session_start(gemini_input)
    else:
        # Unknown event -- pass through silently
        sys.exit(0)


if __name__ == "__main__":
    main()
