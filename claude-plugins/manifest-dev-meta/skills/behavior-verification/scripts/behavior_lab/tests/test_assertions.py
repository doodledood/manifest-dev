from __future__ import annotations

from behavior_lab.assertions import assert_tool_invoked, diff_arms

_CALLS_WITH_SKILL = [
    {"response_blocks": [{"type": "text", "text": "ok, let me check"}]},
    {
        "response_blocks": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": "do"}},
        ]
    },
]

_CALLS_WITHOUT_SKILL = [
    {"response_blocks": [{"type": "text", "text": "just answering directly"}]},
]


def test_assert_tool_invoked_positive() -> None:
    assert assert_tool_invoked(_CALLS_WITH_SKILL, "Skill") is True


def test_assert_tool_invoked_negative_tool_not_called() -> None:
    assert assert_tool_invoked(_CALLS_WITHOUT_SKILL, "Skill") is False


def test_assert_tool_invoked_with_input_predicate() -> None:
    assert (
        assert_tool_invoked(
            _CALLS_WITH_SKILL, "Skill", input_predicate=lambda i: i.get("skill") == "do"
        )
        is True
    )
    assert (
        assert_tool_invoked(
            _CALLS_WITH_SKILL,
            "Skill",
            input_predicate=lambda i: i.get("skill") == "define",
        )
        is False
    )


def test_assert_tool_invoked_is_not_hardcoded_to_skill_tool() -> None:
    calls = [
        {
            "response_blocks": [
                {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}
            ]
        }
    ]
    assert assert_tool_invoked(calls, "Bash") is True
    assert assert_tool_invoked(calls, "Skill") is False


def test_diff_arms_reports_per_arm_compliance() -> None:
    results_by_arm = {"baseline": _CALLS_WITHOUT_SKILL, "amended": _CALLS_WITH_SKILL}

    diff = diff_arms(results_by_arm, lambda calls: assert_tool_invoked(calls, "Skill"))

    assert diff == {"baseline": False, "amended": True}
