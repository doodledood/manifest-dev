#!/usr/bin/env python3
"""
Shared utilities for manifest-dev hooks.

Contains transcript parsing for skill invocation detection.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
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


def was_skill_invoked(line_data: dict[str, Any], skill_name: str) -> bool:
    """
    Check if this transcript line represents a skill invocation.

    Detects ALL invocation patterns:
    1. Model Skill tool call (assistant message with Skill tool_use)
    2. User isMeta skill expansion (isMeta=true with skills/{name} in path)
    3. User command-name tag (/<skill> or /plugin:skill format)

    Args:
        line_data: Parsed transcript line
        skill_name: Skill name to check (e.g., "do", "verify")

    Returns:
        True if this line invokes the specified skill
    """
    msg_type = line_data.get("type")

    # Pattern 1: Model Skill tool call
    if msg_type == "assistant":
        return _is_skill_tool_call(line_data, skill_name)

    # Patterns 2 & 3: User invocations
    if msg_type == "user":
        return _is_user_skill_invocation(line_data, skill_name)

    return False


def _is_skill_tool_call(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if assistant message contains a Skill tool call for the given skill."""
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
            # Only search the "Base directory" line — the body may reference
            # other skills' files (e.g., skills/do/references/...) which would
            # false-positive if we searched the entire text.
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
    if line_data.get("type") != "user":
        return None

    text = get_message_text(line_data)

    # Check if this is a command with matching skill name (only our plugin)
    has_command = (
        f"<command-name>/{skill_name}</command-name>" in text
        or f"<command-name>/manifest-dev:{skill_name}</command-name>" in text
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


def record_stop_block(
    session_id: str,
    transcript_path: str,
    state_dir: str | None = None,
) -> int:
    """
    Track consecutive stop-hook blocks per session, keyed on transcript mtime.

    Each call increments a per-session counter stored at
    ``{state_dir}/manifest-dev-stop-blocks-{session_id}.json``. The counter
    resets to 1 when the transcript's on-disk mtime advances between
    invocations.

    This independence from transcript content matters: the existing
    ``count_consecutive_short_outputs`` helper relies on the model's
    short-output pattern being visible in the transcript, but Claude Code
    flushes assistant output to disk only at user-prompt boundaries. During
    a long ``/do → /verify → /done`` chain with no intervening user prompt,
    the model's recent invocations remain buffered in memory and are
    invisible to the hook. Counting blocks (which the hook itself observes)
    rather than transcript content makes the loop-escape independent of
    that flush timing.

    Args:
        session_id: Stable identifier for the current Claude Code session.
            Hook input typically provides this as ``hook_input["session_id"]``.
        transcript_path: Path to the on-disk transcript file. Used only for
            its mtime — not parsed.
        state_dir: Directory for the per-session counter file. Defaults to
            ``/tmp``; tests override.

    Returns:
        The number of consecutive blocks observed without the transcript
        advancing. ``1`` on the first block of a fresh stretch.
    """
    if state_dir is None:
        state_dir = tempfile.gettempdir()
    # Sanitize session_id to prevent path traversal (defense-in-depth;
    # session_id comes from Claude Code's hook runtime, not user input).
    safe_id = os.path.basename(session_id) or "default"
    state_path = os.path.join(state_dir, f"manifest-dev-stop-blocks-{safe_id}.json")

    try:
        tx_mtime = os.path.getmtime(transcript_path)
    except OSError:
        tx_mtime = 0.0

    state: dict[str, Any] = {"count": 0, "transcript_mtime": 0.0}
    if os.path.exists(state_path):
        try:
            with open(state_path, encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                state = loaded
        except (json.JSONDecodeError, OSError) as exc:
            print(
                f"manifest-dev: corrupt stop-block state, resetting: {exc}",
                file=sys.stderr,
            )

    prior_mtime = state.get("transcript_mtime", 0.0)
    # Float equality is stable here: json roundtrips preserve float64, and
    # APFS/ext4/tmpfs have sub-second mtime resolution.  On coarse-resolution
    # filesystems (FAT32, some NFS), two writes within the same second would
    # look identical — the counter wouldn't reset even though the transcript
    # genuinely advanced.  In practice this is unlikely to cause a false
    # escape (would need N blocks within one second).
    if isinstance(prior_mtime, (int, float)) and prior_mtime == tx_mtime:
        # Transcript has not advanced since the previous block — keep counting
        prior_count = state.get("count", 0)
        if not isinstance(prior_count, int):
            prior_count = 0
        new_count = prior_count + 1
    else:
        # Transcript advanced (model output reached disk) — fresh stretch
        new_count = 1

    new_state = {"count": new_count, "transcript_mtime": tx_mtime}
    try:
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(new_state, f)
    except OSError as exc:
        print(
            f"manifest-dev: failed to write stop-block state: {exc}",
            file=sys.stderr,
        )

    return new_count


def parse_do_flow(transcript_path: str) -> DoFlowState:
    """
    Parse transcript to determine the state of /do workflow.

    Tracks the most recent /do invocation and what happened after it.
    Each new /do resets the flow state.

    Handles user interrupts: if /do is invoked but the user interrupts
    before the assistant responds, the /do is considered cancelled.
    """
    has_do = False
    has_verify = False
    has_done = False
    has_escalate = False
    has_self_amendment = False
    do_args: str | None = None
    has_collab_mode = False
    # Tracks whether assistant has responded since the last /do invocation.
    # Used to detect interrupted /do: if the user interrupts before the
    # assistant responds, /do never started processing.
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

                # Check for /do (any invocation pattern)
                if was_skill_invoked(data, "do"):
                    # Extract args first before deciding if this is a new /do
                    args = extract_user_command_args(data, "do")
                    if not args:
                        args = get_skill_call_args(data, "do")

                    # isMeta skill expansions follow command-name lines for the same /do
                    # Only reset state if this line has args OR we don't have /do yet
                    # This prevents the isMeta line from clearing args set by command-name line
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

                    # For assistant Skill tool calls (Pattern 1), the /do
                    # invocation IS an assistant message — mark as responded.
                    if data.get("type") == "assistant":
                        do_turn_has_response = True

                # Track assistant responses after /do to detect interrupted /do
                if has_do and not do_turn_has_response:
                    if data.get("type") == "assistant":
                        do_turn_has_response = True

                # Detect user interrupt: if /do was invoked but the assistant
                # never responded, the /do was cancelled by the interrupt.
                if has_do and not do_turn_has_response:
                    if data.get("type") == "user":
                        text = get_message_text(data)
                        if "[Request interrupted by user]" in text:
                            has_do = False
                            do_args = None
                            has_collab_mode = False

                # Check for /verify, /done, /escalate after /do (any invocation pattern)
                if has_do and was_skill_invoked(data, "verify"):
                    has_verify = True

                if has_do and was_skill_invoked(data, "done"):
                    has_done = True

                if has_do and was_skill_invoked(data, "escalate"):
                    has_escalate = True
                    # Detect Self-Amendment by checking escalate args
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


def parse_thinking_disciplines_flow(
    transcript_path: str,
) -> ThinkingDisciplinesState:
    """
    Parse transcript to determine if thinking disciplines are active.

    Activates when thinking-disciplines skill is invoked (by any skill).
    Deactivates when /stop-thinking-disciplines or /do is invoked.
    Reactivates if thinking-disciplines is invoked again after deactivation.
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
                    # isMeta expansion follows the initial invocation —
                    # don't toggle off/on, just ensure active
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
