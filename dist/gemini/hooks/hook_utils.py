#!/usr/bin/env python3
"""
Shared utilities for manifest-dev hooks (Gemini CLI adaptation).

Contains transcript parsing for skill invocation detection.
Adapted for Gemini CLI's JSONL transcript format where message types
are 'user' and 'gemini' instead of 'user' and 'assistant'.
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
    has_self_amendment: bool  # last /escalate was Self-Amendment (not blocking/pause)
    do_args: str | None  # raw arguments from /do invocation
    has_collab_mode: bool  # /do uses non-local medium (--medium not local)


@dataclass
class ThinkingDisciplinesState:
    """State of thinking disciplines from transcript parsing."""

    is_active: bool  # thinking-disciplines skill was invoked and not yet deactivated


def build_system_reminder(content: str) -> str:
    """Wrap content in a system-reminder tag."""
    return f"<system-reminder>{content}</system-reminder>"


def _normalize_type(msg_type: str) -> str:
    """Normalize Gemini message types to Claude Code equivalents.

    Gemini uses 'gemini' for model responses; Claude Code uses 'assistant'.
    """
    if msg_type == "gemini":
        return "assistant"
    return msg_type


def get_message_text(line_data: dict[str, Any]) -> str:
    """Extract text content from a message line.

    Handles both Claude Code format (message.content) and
    Gemini CLI format (content array at top level).
    """
    # Gemini format: content is at top level
    content = line_data.get("content", [])
    if not content:
        # Claude format fallback: content inside message
        message = line_data.get("message", {})
        content = message.get("content", [])

    if isinstance(content, str):
        return content

    text = ""
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text += block.get("text", "")
        elif isinstance(block, dict) and "text" in block:
            text += block.get("text", "")
    return text


def get_skill_call_args(line_data: dict[str, Any], skill_name: str) -> str | None:
    """
    Get arguments from a skill tool call for the given skill.

    Returns the args string if found, None otherwise.
    Matches both "skill-name" and "plugin:skill-name" formats.
    Handles both Claude Code (Skill tool_use) and Gemini CLI (activate_skill) formats.
    """
    msg_type = _normalize_type(line_data.get("type", ""))
    if msg_type != "assistant":
        return None

    content = line_data.get("content", [])
    if not content:
        message = line_data.get("message", {})
        content = message.get("content", [])

    if isinstance(content, str):
        return None

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue

        tool_name = block.get("name", "")
        # Match both Claude Code (Skill) and Gemini CLI (activate_skill)
        if tool_name not in ("Skill", "activate_skill"):
            continue

        tool_input = block.get("input", {})
        skill = tool_input.get("skill", "")

        if skill == skill_name or skill.endswith(f":{skill_name}"):
            args = tool_input.get("args", "")
            return args.strip() if args else None

    return None


def was_skill_invoked(line_data: dict[str, Any], skill_name: str) -> bool:
    """
    Check if this transcript line represents a skill invocation.

    Detects ALL invocation patterns:
    1. Model skill tool call (assistant/gemini message with tool_use)
    2. User isMeta skill expansion (isMeta=true with skills/{name} in path)
    3. User command-name tag (/<skill> or /plugin:skill format)

    Args:
        line_data: Parsed transcript line
        skill_name: Skill name to check (e.g., "do", "verify")

    Returns:
        True if this line invokes the specified skill
    """
    msg_type = _normalize_type(line_data.get("type", ""))

    # Pattern 1: Model skill tool call
    if msg_type == "assistant":
        return _is_skill_tool_call(line_data, skill_name)

    # Patterns 2 & 3: User invocations
    if msg_type == "user":
        return _is_user_skill_invocation(line_data, skill_name)

    return False


def _is_skill_tool_call(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if assistant/gemini message contains a skill tool call."""
    content = line_data.get("content", [])
    if not content:
        message = line_data.get("message", {})
        content = message.get("content", [])

    if isinstance(content, str):
        return False

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue

        tool_name = block.get("name", "")
        if tool_name not in ("Skill", "activate_skill"):
            continue

        tool_input = block.get("input", {})
        skill = tool_input.get("skill", "")

        # Match "skill-name" or "plugin:skill-name"
        if skill == skill_name or skill.endswith(f":{skill_name}"):
            return True

    return False


def _is_user_skill_invocation(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if user message represents a skill invocation."""
    text = get_message_text(line_data)

    # Pattern 2: isMeta skill expansion (most reliable for user-invoked)
    if line_data.get("isMeta"):
        if "Base directory for this skill:" in text:
            for line in text.split("\n"):
                if "Base directory for this skill:" in line:
                    pattern = rf"skills/{re.escape(skill_name)}(?:/|\s|$)"
                    if re.search(pattern, line):
                        return True
                    break

    # Pattern 3: command-name tags (various formats)
    # Match /<skill> or /manifest-dev:skill (only our plugin)
    return (
        f"<command-name>/{skill_name}</command-name>" in text
        or f"<command-name>/manifest-dev:{skill_name}</command-name>" in text
    )


def extract_user_command_args(line_data: dict[str, Any], skill_name: str) -> str | None:
    """
    Extract arguments from a user skill command.

    Returns the raw arguments string, or None if not the specified skill command.
    Handles both command-args tags and isMeta expansion formats.
    """
    msg_type = _normalize_type(line_data.get("type", ""))
    if msg_type != "user":
        return None

    text = get_message_text(line_data)

    has_command = (
        f"<command-name>/{skill_name}</command-name>" in text
        or f"<command-name>/manifest-dev:{skill_name}</command-name>" in text
    )

    if not has_command:
        return None

    match = re.search(r"<command-args>(.*?)</command-args>", text, re.DOTALL)
    if match:
        return match.group(1).strip() or None

    match = re.search(r"</command-name>\s*(.+?)(?:<|$)", text)
    if match:
        return match.group(1).strip() or None

    return None


def has_recent_api_error(transcript_path: str) -> bool:
    """
    Check if the most recent model message was an API error.

    API errors are marked with isApiErrorMessage=true.
    """
    last_model_is_error = False

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

                msg_type = _normalize_type(data.get("type", ""))
                if msg_type == "assistant":
                    last_model_is_error = data.get("isApiErrorMessage", False)

    except (FileNotFoundError, OSError):
        return False

    return last_model_is_error


def count_consecutive_short_outputs(transcript_path: str) -> int:
    """
    Count consecutive short model outputs at the end of the transcript.

    Detects infinite loop pattern where the agent outputs minimal content
    repeatedly because it's trying to stop but getting blocked by hooks.
    """
    output_types: list[str] = []

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

                msg_type = _normalize_type(data.get("type", ""))
                if msg_type != "assistant":
                    continue

                content = data.get("content", [])
                if not content:
                    message = data.get("message", {})
                    content = message.get("content", [])

                text_len = 0
                has_meaningful_tool = False

                if isinstance(content, str):
                    text_len = len(content.strip())
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") == "text":
                                text_len += len(block.get("text", "").strip())
                            elif "text" in block:
                                text_len += len(block.get("text", "").strip())
                            elif block.get("type") == "tool_use":
                                tool_name = block.get("name", "")
                                if tool_name not in ("Skill", "activate_skill"):
                                    has_meaningful_tool = True

                if has_meaningful_tool or text_len >= 100:
                    output_types.append("substantial")
                else:
                    output_types.append("short")

    except (FileNotFoundError, OSError):
        return 0

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
    has_self_amendment = False
    do_args: str | None = None
    has_collab_mode = False
    do_turn_has_response = False

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

                if was_skill_invoked(data, "do"):
                    args = extract_user_command_args(data, "do")
                    if not args:
                        args = get_skill_call_args(data, "do")

                    is_new_do = not has_do or args is not None

                    if is_new_do:
                        has_do = True
                        has_verify = False
                        has_done = False
                        has_escalate = False
                        has_self_amendment = False
                        do_turn_has_response = False
                        if args:
                            do_args = args
                            has_collab_mode = bool(
                                re.search(r"--medium\s+(?!local(?:\s|$))\S+", args)
                            )

                    msg_type = _normalize_type(data.get("type", ""))
                    if msg_type == "assistant":
                        do_turn_has_response = True

                msg_type = _normalize_type(data.get("type", ""))
                if has_do and not do_turn_has_response:
                    if msg_type == "assistant":
                        do_turn_has_response = True

                if has_do and not do_turn_has_response:
                    if msg_type == "user":
                        text = get_message_text(data)
                        if "[Request interrupted by user]" in text:
                            has_do = False
                            do_args = None
                            has_collab_mode = False

                if has_do and was_skill_invoked(data, "verify"):
                    has_verify = True

                if has_do and was_skill_invoked(data, "done"):
                    has_done = True

                if has_do and was_skill_invoked(data, "escalate"):
                    has_escalate = True
                    esc_args = get_skill_call_args(data, "escalate")
                    if not esc_args:
                        esc_args = extract_user_command_args(data, "escalate")
                    if esc_args and "self-amendment" in esc_args.lower():
                        has_self_amendment = True

    except OSError:
        return DoFlowState(
            has_do=False,
            has_verify=False,
            has_done=False,
            has_escalate=False,
            has_self_amendment=False,
            do_args=None,
            has_collab_mode=False,
        )

    return DoFlowState(
        has_do=has_do,
        has_verify=has_verify,
        has_done=has_done,
        has_escalate=has_escalate,
        has_self_amendment=has_self_amendment,
        do_args=do_args,
        has_collab_mode=has_collab_mode,
    )


# Skills that deactivate thinking disciplines
_THINKING_DEACTIVATORS = ("stop-thinking-disciplines", "do")


def parse_thinking_disciplines_flow(transcript_path: str) -> ThinkingDisciplinesState:
    """
    Parse transcript to determine the state of thinking disciplines.

    Activation: thinking-disciplines skill was invoked.
    Deactivation: stop-thinking-disciplines or do skill was invoked after activation.
    """
    is_active = False

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

                # Check for thinking-disciplines activation
                if was_skill_invoked(data, "thinking-disciplines"):
                    is_active = True

                # Check for deactivation
                if is_active:
                    for skill in _THINKING_DEACTIVATORS:
                        if was_skill_invoked(data, skill):
                            is_active = False
                            break

    except OSError:
        return ThinkingDisciplinesState(is_active=False)

    return ThinkingDisciplinesState(is_active=is_active)
