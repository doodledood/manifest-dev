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
    SessionStart - maps to post_compact_hook (source=resume only)

Protocol (Gemini CLI):
    Input:  JSON on stdin
    Output: JSON on stdout (exit 0 only), debug/errors on stderr only
    Exit codes:
        0  = allow (parse stdout for output JSON)
        1  = non-blocking warning (stderr = warning text)
        2+ = blocking (stderr = reason for block)

AfterAgent deny/retry protocol:
    - decision: "deny" rejects the model's response
    - reason field becomes a new prompt for the agent to correct
    - hookSpecificOutput.clearContext: true clears LLM memory from rejected turn
    - Next AfterAgent input will have stop_hook_active: true (retry sequence)
    - Hooks must implement retry limits to avoid infinite loops

Transcript format:
    Gemini CLI uses JSONL at transcript_path with record types:
        user, gemini (not "assistant"), message_update
"""

from __future__ import annotations

import json
import os
import re
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

# Regex to strip <system-reminder> wrappers.
# Gemini additionalContext is plain text -- no XML tags needed.
_SYSTEM_REMINDER_RE = re.compile(
    r"<system-reminder>(.*?)</system-reminder>", re.DOTALL
)


def _strip_system_reminder(text: str) -> str:
    """Remove <system-reminder> wrapper tags from context text.

    Claude Code hooks use build_system_reminder() which wraps content in
    <system-reminder> tags.  Gemini CLI additionalContext is plain text --
    these tags would be passed literally and confuse the model.
    """
    match = _SYSTEM_REMINDER_RE.search(text)
    if match:
        return match.group(1).strip()
    return text


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
        # Pass through stop_hook_active so hooks can detect retry sequences
        if gemini_input.get("stop_hook_active"):
            claude_input["stop_hook_active"] = True

    elif event == "SessionStart":
        claude_input["source"] = gemini_input.get("source", "startup")

    return claude_input


def _translate_output(claude_output: dict[str, Any], event: str) -> dict[str, Any]:
    """Convert Claude Code hook output to Gemini hook format.

    Returns a tuple-like dict with a special '_exit_code' key for the caller
    to know which exit code to use.  The caller must pop this key before
    writing stdout.
    """
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
        # Pass through additionalContext (stripped of system-reminder wrappers)
        ctx = hook_specific.get("additionalContext", "")
        if ctx:
            ctx = _strip_system_reminder(ctx)
            gemini_output.setdefault("hookSpecificOutput", {})
            gemini_output["hookSpecificOutput"]["hookEventName"] = "BeforeTool"
            gemini_output["hookSpecificOutput"]["additionalContext"] = ctx
        # Support tool_input modification (BeforeTool can override model args)
        tool_input_override = hook_specific.get("tool_input")
        if tool_input_override:
            gemini_output.setdefault("hookSpecificOutput", {})
            gemini_output["hookSpecificOutput"]["hookEventName"] = "BeforeTool"
            gemini_output["hookSpecificOutput"]["tool_input"] = tool_input_override

    elif event == "AfterAgent":
        decision = claude_output.get("decision", "")
        if decision == "block":
            gemini_output["decision"] = "deny"
            reason = claude_output.get("reason", "")
            gemini_output["reason"] = reason
            # clearContext: force agent to reason from file state on retry
            gemini_output["hookSpecificOutput"] = {
                "hookEventName": "AfterAgent",
                "clearContext": True,
            }
            # Signal to caller: use exit code 2 with reason on stderr
            gemini_output["_block"] = True
            gemini_output["_block_reason"] = reason
        elif decision == "allow":
            gemini_output["decision"] = "allow"

        msg = claude_output.get("systemMessage", "")
        if msg:
            gemini_output["systemMessage"] = msg

    elif event == "SessionStart":
        ctx = hook_specific.get("additionalContext", "")
        if ctx:
            ctx = _strip_system_reminder(ctx)
            gemini_output["hookSpecificOutput"] = {
                "hookEventName": "SessionStart",
                "additionalContext": ctx,
            }

    return gemini_output


def _patch_transcript_for_claude(transcript_path: str) -> str:
    """Create a patched copy of the Gemini JSONL transcript for Claude hooks.

    Gemini CLI uses record type "gemini" for assistant messages while
    Claude Code hooks expect "assistant".  This creates a temp file with
    the type field patched so hook_utils parsing works correctly.

    Returns the path to the patched file (or the original if patching fails).
    """
    if not transcript_path or not os.path.isfile(transcript_path):
        return transcript_path

    import tempfile

    try:
        patched_lines: list[str] = []
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    patched_lines.append(line)
                    continue
                try:
                    record = json.loads(stripped)
                except json.JSONDecodeError:
                    patched_lines.append(line)
                    continue

                # Patch "gemini" -> "assistant" for Claude hook compatibility
                if record.get("type") == "gemini":
                    record["type"] = "assistant"
                    patched_lines.append(json.dumps(record) + "\n")
                else:
                    patched_lines.append(line)

        # Write to temp file in same directory for fast I/O
        dir_name = os.path.dirname(transcript_path) or "/tmp"
        fd, patched_path = tempfile.mkstemp(
            suffix=".jsonl", prefix="patched_", dir=dir_name
        )
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.writelines(patched_lines)

        return patched_path

    except (OSError, IOError):
        # Fall back to original on any error
        return transcript_path


def _cleanup_patched(patched_path: str, original_path: str) -> None:
    """Remove the patched transcript temp file if it differs from original."""
    if patched_path != original_path:
        try:
            os.unlink(patched_path)
        except OSError:
            pass


# --------------------------------------------------------------------------- #
# Event dispatchers
# --------------------------------------------------------------------------- #


def _run_before_tool(gemini_input: dict[str, Any]) -> None:
    """Dispatch BeforeTool -> pretool_verify_hook."""
    claude_input = _translate_input(gemini_input, "BeforeTool")

    # Only process activate_skill (Skill) calls
    if claude_input.get("tool_name") != "Skill":
        sys.exit(0)

    # Patch transcript for Claude hook compatibility (gemini -> assistant)
    original_transcript = claude_input.get("transcript_path", "")
    patched_transcript = _patch_transcript_for_claude(original_transcript)
    claude_input["transcript_path"] = patched_transcript

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
    finally:
        _cleanup_patched(patched_transcript, original_transcript)

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

    # Patch transcript for Claude hook compatibility (gemini -> assistant)
    original_transcript = claude_input.get("transcript_path", "")
    patched_transcript = _patch_transcript_for_claude(original_transcript)
    claude_input["transcript_path"] = patched_transcript

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
    finally:
        _cleanup_patched(patched_transcript, original_transcript)

    claude_output_str = captured.getvalue().strip()
    if claude_output_str:
        try:
            claude_output = json.loads(claude_output_str)
            gemini_output = _translate_output(claude_output, "AfterAgent")

            if gemini_output:
                # AfterAgent blocking: exit 2 with reason on stderr
                if gemini_output.pop("_block", False):
                    block_reason = gemini_output.pop("_block_reason", "Blocked by hook")
                    # Write allow/deny JSON to stdout for Gemini to parse
                    print(json.dumps(gemini_output))
                    # Write reason to stderr (Gemini uses this as feedback prompt)
                    print(block_reason, file=sys.stderr)
                    sys.exit(2)
                else:
                    # Remove internal keys if somehow present
                    gemini_output.pop("_block_reason", None)
                    print(json.dumps(gemini_output))
        except json.JSONDecodeError:
            pass

    sys.exit(0)


def _run_session_start(gemini_input: dict[str, Any]) -> None:
    """Dispatch SessionStart (source=resume) -> post_compact_hook."""
    # Only handle "resume" source (post-compaction recovery)
    # "startup" and "clear" don't need compact recovery
    source = gemini_input.get("source", "startup")
    if source != "resume":
        sys.exit(0)

    claude_input = _translate_input(gemini_input, "SessionStart")

    # Patch transcript for Claude hook compatibility (gemini -> assistant)
    original_transcript = claude_input.get("transcript_path", "")
    patched_transcript = _patch_transcript_for_claude(original_transcript)
    claude_input["transcript_path"] = patched_transcript

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
    finally:
        _cleanup_patched(patched_transcript, original_transcript)

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
        sys.exit(2)

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
