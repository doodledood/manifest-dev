"""Behavior-compliance assertions over decoded calls, and per-arm diffing.

Generalizes the originating investigation's scratch ``skill_activation_check.py``
prototype (which only checked whether the Skill tool was invoked) into a
reusable check applicable to any tool name or behavior.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any


def assert_tool_invoked(
    calls: Sequence[Mapping[str, Any]],
    tool_name: str,
    input_predicate: Callable[[Any], bool] | None = None,
) -> bool:
    """True if any decoded call's response contains a ``tool_use`` block named
    ``tool_name`` — and, when given, ``input_predicate(input)`` also holds for
    that block. Works for any tool name (e.g. ``"Skill"``, ``"Bash"``,
    ``"Edit"``), not hardcoded to Skill-tool activation."""
    for call in calls:
        for block in call.get("response_blocks", []) or []:
            if block.get("type") != "tool_use" or block.get("name") != tool_name:
                continue
            if input_predicate is None or input_predicate(block.get("input")):
                return True
    return False


def diff_arms(
    results_by_arm: Mapping[str, Sequence[Mapping[str, Any]]],
    assertion: Callable[[Sequence[Mapping[str, Any]]], bool],
) -> dict[str, bool]:
    """Apply ``assertion`` to each arm's decoded calls, so a baseline-vs-amended
    compliance comparison is a single call:

        diff_arms(results_by_arm, lambda calls: assert_tool_invoked(calls, "Skill"))
    """
    return {arm: assertion(calls) for arm, calls in results_by_arm.items()}
