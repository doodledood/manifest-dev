#!/usr/bin/env python3
"""
Shared utilities for manifest-dev hooks.

Contains transcript parsing for skill invocation detection.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class DoFlowState:
    """State of the /do workflow from transcript parsing."""

    has_do: bool  # /do was invoked
    has_verify: bool  # /verify was called after last /do
    has_done: bool  # /done was called after last /do
    has_escalate: bool  # /escalate was called after last /do


def is_skill_invocation(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if this line contains a Skill tool call for the given skill."""
    if line_data.get("type") != "assistant":
        return False

    message = line_data.get("message", {})
    content = message.get("content", [])

    # String content won't contain tool_use blocks
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
        # Match both "skill-name" and "plugin:skill-name" formats
        if skill == skill_name or skill.endswith(f":{skill_name}"):
            return True

    return False


def is_user_skill_command(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if this line is a user command invoking the skill."""
    if line_data.get("type") != "user":
        return False

    message = line_data.get("message", {})
    content = message.get("content", [])

    # Handle string content format
    if isinstance(content, str):
        return f"<command-name>/manifest-dev:{skill_name}" in content

    # Handle array content format
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "text":
            continue
        text = block.get("text", "")
        if f"<command-name>/manifest-dev:{skill_name}" in text:
            return True

    return False


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
                    # New /do resets the flow
                    has_do = True
                    has_verify = False
                    has_done = False
                    has_escalate = False

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
        )
    except OSError:
        return DoFlowState(
            has_do=False,
            has_verify=False,
            has_done=False,
            has_escalate=False,
        )

    return DoFlowState(
        has_do=has_do,
        has_verify=has_verify,
        has_done=has_done,
        has_escalate=has_escalate,
    )
