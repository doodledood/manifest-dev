#!/usr/bin/env python3
"""
Shared utilities for manifest-dev hooks.

Contains transcript parsing for skill invocation detection.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


@dataclass
class DoFlowState:
    """State of the /do workflow from transcript parsing."""

    has_do: bool  # /do was invoked
    has_verify: bool  # /verify was called after last /do
    has_done: bool  # /done was called after last /do
    has_escalate: bool  # /escalate was called after last /do
    do_args: str | None  # raw arguments from /do invocation


def build_system_reminder(content: str) -> str:
    """Wrap content in a system-reminder tag."""
    return f"<system-reminder>{content}</system-reminder>"


def get_message_text(line_data: dict[str, Any]) -> str:
    """Extract text content from a message line."""
    message = line_data.get("message", {})
    content = message.get("content", [])

    if isinstance(content, str):
        return content

    text = ""
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text += block.get("text", "")
    return text


def get_skill_call_args(line_data: dict[str, Any], skill_name: str) -> str | None:
    """
    Get arguments from a Skill tool call for the given skill.

    Returns the args string if found, None otherwise.
    Matches both "skill-name" and "plugin:skill-name" formats.
    """
    if line_data.get("type") != "assistant":
        return None

    message = line_data.get("message", {})
    content = message.get("content", [])

    if isinstance(content, str):
        return None

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        if block.get("name") != "Skill":
            continue

        tool_input = block.get("input", {})
        skill = tool_input.get("skill", "")

        if skill == skill_name or skill.endswith(f":{skill_name}"):
            args = tool_input.get("args", "")
            return args.strip() if args else None

    return None


def is_skill_invocation(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if this line contains a Skill tool call for the given skill."""
    return get_skill_call_args(line_data, skill_name) is not None or (
        line_data.get("type") == "assistant"
        and _has_skill_call_without_args(line_data, skill_name)
    )


def _has_skill_call_without_args(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check for skill call that may have no args field at all."""
    message = line_data.get("message", {})
    content = message.get("content", [])

    if isinstance(content, str):
        return False

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        if block.get("name") != "Skill":
            continue

        tool_input = block.get("input", {})
        skill = tool_input.get("skill", "")

        if skill == skill_name or skill.endswith(f":{skill_name}"):
            return True

    return False


def is_user_skill_command(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if this line is a user command invoking the skill."""
    if line_data.get("type") != "user":
        return False

    text = get_message_text(line_data)
    return f"<command-name>/manifest-dev:{skill_name}" in text


def extract_user_command_args(line_data: dict[str, Any], skill_name: str) -> str | None:
    """
    Extract arguments from a user skill command.

    Returns the raw arguments string, or None if not the specified skill command.
    """
    if line_data.get("type") != "user":
        return None

    text = get_message_text(line_data)

    if f"<command-name>/manifest-dev:{skill_name}" not in text:
        return None

    # Extract arguments after the command tag
    match = re.search(r"</command-name>\s*(.+?)(?:<|$)", text)
    if not match:
        return None

    return match.group(1).strip()


def has_recent_api_error(transcript_path: str) -> bool:
    """
    Check if the most recent assistant message was an API error.

    API errors (like 529 Overloaded) are marked with isApiErrorMessage=true.
    These are system failures, not voluntary stops, so hooks should allow them.
    """
    last_assistant_is_error = False

    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Track if the last assistant message was an API error
                if data.get("type") == "assistant":
                    last_assistant_is_error = data.get("isApiErrorMessage", False)

    except (FileNotFoundError, OSError):
        return False

    return last_assistant_is_error


def count_consecutive_short_outputs(transcript_path: str) -> int:
    """
    Count consecutive short assistant outputs at the end of the transcript.

    This detects the infinite loop pattern where the agent outputs minimal
    content (like "." or "Done.") repeatedly because it's trying to stop
    but getting blocked by hooks.

    A "short output" is an assistant message with:
    - Less than 100 characters of text
    - No tool uses (or only Skill tool use which might be an /escalate attempt)

    Returns the count of consecutive short outputs from the end.
    """
    # Collect all assistant output classifications
    output_types: list[str] = []  # 'short' or 'substantial'

    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if data.get("type") != "assistant":
                    continue

                message = data.get("message", {})
                content = message.get("content", [])

                # Get text content length and check for meaningful tool uses
                text_len = 0
                has_meaningful_tool = False

                if isinstance(content, str):
                    text_len = len(content.strip())
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") == "text":
                                text_len += len(block.get("text", "").strip())
                            elif block.get("type") == "tool_use":
                                tool_name = block.get("name", "")
                                # Skill invocations don't count as "meaningful" for loop detection
                                # because /escalate attempts would be Skill calls
                                if tool_name != "Skill":
                                    has_meaningful_tool = True

                # Classify this output
                if has_meaningful_tool or text_len >= 100:
                    output_types.append("substantial")
                else:
                    output_types.append("short")

    except (FileNotFoundError, OSError):
        return 0

    # Count consecutive short outputs from the end
    consecutive_short = 0
    for output_type in reversed(output_types):
        if output_type == "short":
            consecutive_short += 1
        else:
            break

    return consecutive_short


def parse_do_flow(transcript_path: str) -> DoFlowState:
    """
    Parse transcript to determine the state of /do workflow.

    Tracks the most recent /do invocation and what happened after it.
    Each new /do resets the flow state.
    """
    has_do = False
    has_verify = False
    has_done = False
    has_escalate = False
    do_args: str | None = None

    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Check for /do (user command or skill call)
                if is_user_skill_command(data, "do") or is_skill_invocation(data, "do"):
                    # New /do resets the flow (including do_args)
                    has_do = True
                    has_verify = False
                    has_done = False
                    has_escalate = False
                    do_args = None

                    # Extract args from user command or skill call
                    args = extract_user_command_args(data, "do")
                    if not args:
                        args = get_skill_call_args(data, "do")
                    if args:
                        do_args = args

                # Check for /verify after /do
                if has_do and is_skill_invocation(data, "verify"):
                    has_verify = True

                # Check for /done after /do
                if has_do and is_skill_invocation(data, "done"):
                    has_done = True

                # Check for /escalate after /do
                if has_do and is_skill_invocation(data, "escalate"):
                    has_escalate = True

    except FileNotFoundError:
        return DoFlowState(
            has_do=False,
            has_verify=False,
            has_done=False,
            has_escalate=False,
            do_args=None,
        )
    except OSError:
        return DoFlowState(
            has_do=False,
            has_verify=False,
            has_done=False,
            has_escalate=False,
            do_args=None,
        )

    return DoFlowState(
        has_do=has_do,
        has_verify=has_verify,
        has_done=has_done,
        has_escalate=has_escalate,
        do_args=do_args,
    )
