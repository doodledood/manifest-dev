"""
Tests for thinking disciplines state detection and hooks.

Tests parse_thinking_disciplines_flow() for transcript parsing,
the UserPromptSubmit hook for per-turn reminder injection, and
the PreToolUse hook on AskUserQuestion for pre-question reminder injection.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any

import pytest
from hook_test_helpers import HOOKS_DIR, run_hook_raw

# Add hooks dir to path for direct imports
sys.path.insert(0, str(HOOKS_DIR))

from hook_utils import parse_thinking_disciplines_flow

# -- Transcript building fixtures --


@pytest.fixture
def thinking_disciplines_skill_call() -> dict[str, Any]:
    """Assistant Skill tool call invoking thinking-disciplines."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:thinking-disciplines"},
                }
            ]
        },
    }


@pytest.fixture
def thinking_disciplines_ismeta() -> dict[str, Any]:
    """isMeta expansion for thinking-disciplines skill."""
    return {
        "type": "user",
        "isMeta": True,
        "message": {
            "content": (
                "Base directory for this skill: "
                "/home/user/manifest-dev/claude-plugins/manifest-dev/skills/thinking-disciplines\n\n"
                "Adopt these disciplines for the duration of this session..."
            )
        },
    }


@pytest.fixture
def user_figure_out_command() -> dict[str, Any]:
    """User message invoking /figure-out (triggers thinking-disciplines via skill chain)."""
    return {
        "type": "user",
        "message": {
            "content": (
                "<command-name>/manifest-dev:figure-out</command-name>"
                "<command-args>the latency problem</command-args>"
            )
        },
    }


@pytest.fixture
def user_define_command() -> dict[str, Any]:
    """User message invoking /define."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:define</command-name> build a widget"
        },
    }


@pytest.fixture
def user_do_command() -> dict[str, Any]:
    """User message invoking /do (deactivator)."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:do</command-name> /tmp/manifest.md"
        },
    }


@pytest.fixture
def user_stop_thinking_disciplines() -> dict[str, Any]:
    """User message invoking /stop-thinking-disciplines (deactivator)."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:stop-thinking-disciplines</command-name>"
        },
    }


@pytest.fixture
def stop_thinking_disciplines_skill_call() -> dict[str, Any]:
    """Assistant Skill tool call for stop-thinking-disciplines."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:stop-thinking-disciplines"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_text() -> dict[str, Any]:
    """Simple assistant text response."""
    return {
        "type": "assistant",
        "message": {"content": "Investigating the problem..."},
    }


def run_prompt_hook(
    hook_input: dict[str, Any],
) -> subprocess.CompletedProcess:
    """Run the thinking_disciplines_prompt_hook."""
    return run_hook_raw("thinking_disciplines_prompt_hook.py", hook_input)


def run_pretool_hook(
    hook_input: dict[str, Any],
) -> subprocess.CompletedProcess:
    """Run the thinking_disciplines_pretool_hook."""
    return run_hook_raw("thinking_disciplines_pretool_hook.py", hook_input)


# == parse_thinking_disciplines_flow tests ==


class TestParserActivation:
    """Thinking-disciplines activation detection."""

    def test_inactive_when_no_invocation(self, temp_transcript, assistant_text):
        """No thinking-disciplines invocation -> is_active=False."""
        path = temp_transcript([assistant_text])
        state = parse_thinking_disciplines_flow(path)
        assert not state.is_active

    def test_active_via_assistant_skill_call(
        self, temp_transcript, thinking_disciplines_skill_call
    ):
        """Assistant Skill tool call for thinking-disciplines activates state."""
        path = temp_transcript([thinking_disciplines_skill_call])
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active

    def test_active_via_ismeta_expansion(
        self, temp_transcript, thinking_disciplines_ismeta
    ):
        """isMeta expansion for thinking-disciplines activates state."""
        path = temp_transcript([thinking_disciplines_ismeta])
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active

    def test_active_after_figure_out_invokes_thinking_disciplines(
        self,
        temp_transcript,
        user_figure_out_command,
        thinking_disciplines_skill_call,
        thinking_disciplines_ismeta,
        assistant_text,
    ):
        """Realistic /figure-out flow: user command -> assistant invokes thinking-disciplines -> isMeta expansion."""
        path = temp_transcript(
            [
                user_figure_out_command,
                thinking_disciplines_skill_call,
                thinking_disciplines_ismeta,
                assistant_text,
            ]
        )
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active

    def test_active_after_define_invokes_thinking_disciplines(
        self,
        temp_transcript,
        user_define_command,
        thinking_disciplines_skill_call,
        thinking_disciplines_ismeta,
        assistant_text,
    ):
        """Realistic /define flow: user command -> assistant invokes thinking-disciplines."""
        path = temp_transcript(
            [
                user_define_command,
                thinking_disciplines_skill_call,
                thinking_disciplines_ismeta,
                assistant_text,
            ]
        )
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active


class TestParserDeactivation:
    """Thinking-disciplines deactivation detection."""

    def test_stop_thinking_disciplines_deactivates(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_stop_thinking_disciplines,
    ):
        """/stop-thinking-disciplines deactivates."""
        path = temp_transcript(
            [thinking_disciplines_skill_call, assistant_text, user_stop_thinking_disciplines]
        )
        state = parse_thinking_disciplines_flow(path)
        assert not state.is_active

    def test_stop_via_skill_call_deactivates(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        stop_thinking_disciplines_skill_call,
    ):
        """Assistant Skill tool call for stop-thinking-disciplines deactivates."""
        path = temp_transcript(
            [thinking_disciplines_skill_call, assistant_text, stop_thinking_disciplines_skill_call]
        )
        state = parse_thinking_disciplines_flow(path)
        assert not state.is_active

    def test_do_deactivates(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_do_command,
    ):
        """/do deactivates thinking disciplines."""
        path = temp_transcript(
            [thinking_disciplines_skill_call, assistant_text, user_do_command]
        )
        state = parse_thinking_disciplines_flow(path)
        assert not state.is_active

    def test_define_does_not_deactivate(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_define_command,
    ):
        """/define does NOT deactivate thinking disciplines."""
        path = temp_transcript(
            [thinking_disciplines_skill_call, assistant_text, user_define_command]
        )
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active

    def test_reactivation_after_deactivation(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_stop_thinking_disciplines,
    ):
        """Re-invoking thinking-disciplines after stop reactivates."""
        second_activation = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {"skill": "manifest-dev:thinking-disciplines"},
                    }
                ]
            },
        }
        path = temp_transcript(
            [
                thinking_disciplines_skill_call,
                assistant_text,
                user_stop_thinking_disciplines,
                second_activation,
                assistant_text,
            ]
        )
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active

    def test_reactivation_after_do(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_do_command,
    ):
        """/do deactivates, but re-invocation reactivates."""
        second_activation = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {"skill": "manifest-dev:thinking-disciplines"},
                    }
                ]
            },
        }
        path = temp_transcript(
            [
                thinking_disciplines_skill_call,
                assistant_text,
                user_do_command,
                second_activation,
                assistant_text,
            ]
        )
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active


class TestParserEdgeCases:
    """Edge cases for transcript parsing."""

    def test_empty_transcript(self, tmp_path):
        """Empty transcript -> not active."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("")
        state = parse_thinking_disciplines_flow(str(transcript))
        assert not state.is_active

    def test_missing_transcript(self):
        """Missing file -> not active (fail open)."""
        state = parse_thinking_disciplines_flow("/nonexistent/transcript.jsonl")
        assert not state.is_active

    def test_malformed_lines(self, tmp_path):
        """Malformed JSONL lines are skipped gracefully."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("not json\n{broken\n")
        state = parse_thinking_disciplines_flow(str(transcript))
        assert not state.is_active

    def test_ismeta_for_other_skill_does_not_activate(self, temp_transcript):
        """isMeta expansion for a different skill (e.g., /do) should not activate."""
        ismeta_other = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": (
                    "Base directory for this skill: "
                    "/home/user/manifest-dev/claude-plugins/manifest-dev/skills/do\n\n"
                    "Execute a manifest..."
                )
            },
        }
        path = temp_transcript([ismeta_other])
        state = parse_thinking_disciplines_flow(path)
        assert not state.is_active

    def test_ismeta_referencing_thinking_disciplines_in_body_does_not_activate(
        self, temp_transcript
    ):
        """isMeta for another skill that mentions thinking-disciplines in body should NOT activate.

        Only the 'Base directory' line matters for detection, not body references.
        """
        ismeta_with_ref = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": (
                    "Base directory for this skill: "
                    "/home/user/manifest-dev/claude-plugins/manifest-dev/skills/figure-out\n\n"
                    "Invoke the manifest-dev:thinking-disciplines skill."
                )
            },
        }
        path = temp_transcript([ismeta_with_ref])
        state = parse_thinking_disciplines_flow(path)
        # This should NOT activate — figure-out's isMeta expansion mentions
        # thinking-disciplines in the body, but the base directory is for figure-out.
        # The actual thinking-disciplines invocation will be a separate transcript line.
        assert not state.is_active

    def test_bare_skill_name_without_plugin_prefix(self, temp_transcript):
        """Skill call without plugin prefix also activates."""
        bare_call = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {"skill": "thinking-disciplines"},
                    }
                ]
            },
        }
        path = temp_transcript([bare_call])
        state = parse_thinking_disciplines_flow(path)
        assert state.is_active


# == UserPromptSubmit hook tests ==


class TestPromptHookOutput:
    """Tests for cases where the UserPromptSubmit hook SHOULD inject a reminder."""

    def test_reminder_when_active(
        self, temp_transcript, thinking_disciplines_skill_call, assistant_text
    ):
        """Should inject principles reminder when thinking disciplines are active."""
        transcript_path = temp_transcript([thinking_disciplines_skill_call, assistant_text])
        result = run_prompt_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "system-reminder" in context

    def test_reminder_content_is_principle_based(
        self, temp_transcript, thinking_disciplines_skill_call, assistant_text
    ):
        """Reminder should be principle-based, not checklist."""
        transcript_path = temp_transcript([thinking_disciplines_skill_call, assistant_text])
        result = run_prompt_hook({"transcript_path": transcript_path})

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        # Principle-based content
        assert "Truth over helpfulness" in context
        assert "Investigate before engaging" in context
        # Not checklist format
        assert "- Are you" not in context

    def test_reminder_does_not_mention_figure_out(
        self, temp_transcript, thinking_disciplines_skill_call, assistant_text
    ):
        """Reminder should be generic — no /figure-out or /define references."""
        transcript_path = temp_transcript([thinking_disciplines_skill_call, assistant_text])
        result = run_prompt_hook({"transcript_path": transcript_path})

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/figure-out" not in context
        assert "/define" not in context

    def test_active_after_define_invokes_thinking_disciplines(
        self,
        temp_transcript,
        user_define_command,
        thinking_disciplines_skill_call,
        thinking_disciplines_ismeta,
        assistant_text,
    ):
        """Reminder fires when /define invoked thinking-disciplines (NOT silent after /define)."""
        transcript_path = temp_transcript(
            [
                user_define_command,
                thinking_disciplines_skill_call,
                thinking_disciplines_ismeta,
                assistant_text,
            ]
        )
        result = run_prompt_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stdout.strip() != ""


class TestPromptHookNoOutput:
    """Tests for cases where the UserPromptSubmit hook should NOT output anything."""

    def test_silent_when_inactive(self, temp_transcript, assistant_text):
        """Silent when thinking disciplines not invoked."""
        transcript_path = temp_transcript([assistant_text])
        result = run_prompt_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_silent_after_stop_thinking_disciplines(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_stop_thinking_disciplines,
    ):
        """Silent after /stop-thinking-disciplines."""
        transcript_path = temp_transcript(
            [thinking_disciplines_skill_call, assistant_text, user_stop_thinking_disciplines]
        )
        result = run_prompt_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_silent_after_do(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_do_command,
    ):
        """Silent after /do deactivates."""
        transcript_path = temp_transcript(
            [thinking_disciplines_skill_call, assistant_text, user_do_command]
        )
        result = run_prompt_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_silent_missing_transcript(self):
        """Silent when transcript doesn't exist."""
        result = run_prompt_hook({"transcript_path": "/nonexistent/transcript.jsonl"})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_silent_no_transcript_path(self):
        """Silent when transcript_path missing from input."""
        result = run_prompt_hook({})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_silent_invalid_json_input(self):
        """Fail open for invalid JSON input."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "thinking_disciplines_prompt_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_stderr_output(
        self, temp_transcript, thinking_disciplines_skill_call, assistant_text
    ):
        """Hook should never write to stderr on success."""
        transcript_path = temp_transcript([thinking_disciplines_skill_call, assistant_text])
        result = run_prompt_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stderr.strip() == ""


# == PreToolUse AskUserQuestion hook tests ==


class TestPretoolHookActive:
    """Tests for when the PreToolUse AskUserQuestion hook SHOULD inject."""

    def test_ask_user_active_injects_reminder(
        self, temp_transcript, thinking_disciplines_skill_call, assistant_text
    ):
        """Injects reminder when thinking disciplines are active."""
        transcript_path = temp_transcript([thinking_disciplines_skill_call, assistant_text])
        result = run_pretool_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "system-reminder" in context
        assert "Truth over helpfulness" in context

    def test_ask_user_active_correct_event_name(
        self, temp_transcript, thinking_disciplines_skill_call, assistant_text
    ):
        """Correct hookEventName is PreToolUse."""
        transcript_path = temp_transcript([thinking_disciplines_skill_call, assistant_text])
        result = run_pretool_hook({"transcript_path": transcript_path})

        output = json.loads(result.stdout)
        assert output["hookSpecificOutput"]["hookEventName"] == "PreToolUse"


class TestPretoolHookInactive:
    """Tests for when the PreToolUse AskUserQuestion hook should NOT output."""

    def test_ask_user_inactive_silent(self, temp_transcript, assistant_text):
        """Silent when thinking disciplines not active."""
        transcript_path = temp_transcript([assistant_text])
        result = run_pretool_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_ask_user_no_transcript_path_silent(self):
        """Silent when no transcript_path in input."""
        result = run_pretool_hook({})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_ask_user_missing_transcript_silent(self):
        """Silent when transcript file missing."""
        result = run_pretool_hook({"transcript_path": "/nonexistent/transcript.jsonl"})

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_ask_user_invalid_json_fail_open(self):
        """Fail open for invalid JSON input."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "thinking_disciplines_pretool_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_ask_user_no_stderr_output(
        self, temp_transcript, thinking_disciplines_skill_call, assistant_text
    ):
        """No stderr on success."""
        transcript_path = temp_transcript([thinking_disciplines_skill_call, assistant_text])
        result = run_pretool_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stderr.strip() == ""

    def test_ask_user_after_deactivation_silent(
        self,
        temp_transcript,
        thinking_disciplines_skill_call,
        assistant_text,
        user_stop_thinking_disciplines,
    ):
        """Silent after /stop-thinking-disciplines."""
        transcript_path = temp_transcript(
            [thinking_disciplines_skill_call, assistant_text, user_stop_thinking_disciplines]
        )
        result = run_pretool_hook({"transcript_path": transcript_path})

        assert result.returncode == 0
        assert result.stdout.strip() == ""
