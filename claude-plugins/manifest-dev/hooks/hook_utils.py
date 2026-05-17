#!/usr/bin/env python3
"""
Shared utilities for manifest-dev hooks.

Contains transcript parsing for skill invocation detection.

Namespace-scoped: only `manifest-dev:<skill>` invocations register.
Bare `<skill>` and `manifest-dev:<skill>` invocations are ignored, so the
experimental plugin's hooks do not fire on the main plugin's skill calls when
both plugins are installed alongside.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

PLUGIN_NAMESPACE = "manifest-dev"


@dataclass
class DoFlowState:
    """State of the /do workflow from transcript parsing."""

    has_do: bool  # /do was invoked
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
    Matches ONLY the namespaced form `manifest-dev:<skill>`.
    """
    if line_data.get("type") != "assistant":
        return None

    message = line_data.get("message", {})
    content = message.get("content", [])

    if isinstance(content, str):
        return None

    target = f"{PLUGIN_NAMESPACE}:{skill_name}"

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        if block.get("name") != "Skill":
            continue

        tool_input = block.get("input", {})
        skill = tool_input.get("skill", "")

        if skill == target:
            args = tool_input.get("args", "")
            return args.strip() if args else None

    return None


def was_skill_invoked(line_data: dict[str, Any], skill_name: str) -> bool:
    """
    Check if this transcript line represents a skill invocation
    for this plugin.

    Detects invocation patterns scoped to `manifest-dev:<skill>`:
    1. Model Skill tool call (assistant message with Skill tool_use)
    2. User isMeta skill expansion (isMeta=true with the plugin's skill path)
    3. User command-name tag (/manifest-dev:<skill>)
    """
    msg_type = line_data.get("type")

    if msg_type == "assistant":
        return _is_skill_tool_call(line_data, skill_name)

    if msg_type == "user":
        return _is_user_skill_invocation(line_data, skill_name)

    return False


def _is_skill_tool_call(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if assistant message contains a Skill tool call for the given skill."""
    message = line_data.get("message", {})
    content = message.get("content", [])

    if isinstance(content, str):
        return False

    target = f"{PLUGIN_NAMESPACE}:{skill_name}"

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        if block.get("name") != "Skill":
            continue

        tool_input = block.get("input", {})
        skill = tool_input.get("skill", "")

        if skill == target:
            return True

    return False


def _is_user_skill_invocation(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if user message represents a skill invocation for this plugin."""
    text = get_message_text(line_data)

    # Pattern 2: isMeta skill expansion — require the plugin namespace
    # in the "Base directory" path (manifest-dev/skills/<name>/).
    if line_data.get("isMeta"):
        if "Base directory for this skill:" in text:
            # Only search the "Base directory" line — body may reference
            # other skills' files which would false-positive otherwise.
            for line in text.split("\n"):
                if "Base directory for this skill:" in line:
                    pattern = rf"{re.escape(PLUGIN_NAMESPACE)}/skills/{re.escape(skill_name)}(?:/|\s|$)"
                    if re.search(pattern, line):
                        return True
                    break

    # Pattern 3: command-name tag — only the namespaced form.
    return f"<command-name>/{PLUGIN_NAMESPACE}:{skill_name}</command-name>" in text


def extract_user_command_args(line_data: dict[str, Any], skill_name: str) -> str | None:
    """
    Extract arguments from a user skill command for this plugin.

    Returns the raw arguments string, or None if not the specified skill command.
    Matches ONLY the namespaced form `/manifest-dev:<skill>`.
    """
    if line_data.get("type") != "user":
        return None

    text = get_message_text(line_data)

    has_command = (
        f"<command-name>/{PLUGIN_NAMESPACE}:{skill_name}</command-name>" in text
    )
    if not has_command:
        return None

    # Try command-args tag first (most explicit)
    match = re.search(r"<command-args>(.*?)</command-args>", text, re.DOTALL)
    if match:
        return match.group(1).strip() or None

    # Fallback: content after command-name tag
    match = re.search(r"</command-name>\s*(.+?)(?:<|$)", text)
    if match:
        return match.group(1).strip() or None

    return None


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

                if data.get("type") == "assistant":
                    last_assistant_is_error = data.get("isApiErrorMessage", False)

    except (FileNotFoundError, OSError):
        return False

    return last_assistant_is_error


def count_consecutive_idle_outputs(transcript_path: str) -> int:
    """
    Count consecutive idle assistant outputs at the end of the transcript.

    An "idle" output is an assistant message with no meaningful tool use
    (only text, or text with Skill-only tool calls). Productive work means
    using tools (Read, Edit, Bash, Agent, etc.).

    Skill invocations are excluded from "meaningful" tool use because /escalate
    attempts are Skill calls and shouldn't mask the stuck pattern.

    Returns the count of consecutive idle outputs from the end.
    """
    output_types: list[str] = []  # 'idle' or 'productive'

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

                has_meaningful_tool = False

                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") == "tool_use":
                                tool_name = block.get("name", "")
                                if tool_name != "Skill":
                                    has_meaningful_tool = True

                if has_meaningful_tool:
                    output_types.append("productive")
                else:
                    output_types.append("idle")

    except (FileNotFoundError, OSError):
        return 0

    consecutive_idle = 0
    for output_type in reversed(output_types):
        if output_type == "idle":
            consecutive_idle += 1
        else:
            break

    return consecutive_idle


def parse_do_flow(transcript_path: str) -> DoFlowState:
    """
    Parse transcript to determine the state of /do workflow.

    Tracks the most recent /do invocation and what happened after it.
    Each new /do resets the flow state.

    Handles user interrupts: if /do is invoked but the user interrupts
    before the assistant responds, the /do is considered cancelled.
    """
    has_do = False
    has_done = False
    has_escalate = False
    do_args: str | None = None
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

                # Check for /do (namespace-scoped to this plugin only)
                if was_skill_invoked(data, "do"):
                    args = extract_user_command_args(data, "do")
                    if not args:
                        args = get_skill_call_args(data, "do")

                    # isMeta skill expansions follow command-name lines for the same /do
                    is_new_do = not has_do or args is not None

                    if is_new_do:
                        has_do = True
                        has_done = False
                        has_escalate = False
                        do_turn_has_response = False
                        if args:
                            do_args = args

                    if data.get("type") == "assistant":
                        do_turn_has_response = True

                # Track assistant responses after /do to detect interrupted /do
                if has_do and not do_turn_has_response:
                    if data.get("type") == "assistant":
                        do_turn_has_response = True

                # Detect user interrupt: /do invoked but assistant never responded
                if has_do and not do_turn_has_response:
                    if data.get("type") == "user":
                        text = get_message_text(data)
                        if "[Request interrupted by user]" in text:
                            has_do = False
                            do_args = None

                if has_do and was_skill_invoked(data, "done"):
                    has_done = True

                if has_do and was_skill_invoked(data, "escalate"):
                    has_escalate = True

    except OSError:
        return DoFlowState(
            has_do=False,
            has_done=False,
            has_escalate=False,
            do_args=None,
        )

    return DoFlowState(
        has_do=has_do,
        has_done=has_done,
        has_escalate=has_escalate,
        do_args=do_args,
    )
