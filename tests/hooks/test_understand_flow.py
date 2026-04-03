"""
Tests for /understand flow detection and the understand_prompt_hook.

Tests parse_understand_flow() for transcript parsing and the
UserPromptSubmit hook for principles reinforcement injection.
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

from hook_utils import parse_understand_flow


# -- Fixtures --


@pytest.fixture
def user_understand_command() -> dict[str, Any]:
    """User message invoking /understand."""
    return {
        "type": "user",
        "message": {
            "content": (
                "<command-name>/manifest-dev:understand</command-name>"
                "<command-args>the latency problem in our API</command-args>"
            )
        },
    }


@pytest.fixture
def user_understand_no_args() -> dict[str, Any]:
    """User message invoking /understand without arguments."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:understand</command-name>"
        },
    }


@pytest.fixture
def assistant_skill_understand() -> dict[str, Any]:
    """Assistant Skill tool call for understand."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {
                        "skill": "manifest-dev:understand",
                        "args": "the auth flow",
                    },
                }
            ]
        },
    }


@pytest.fixture
def user_understand_done_command() -> dict[str, Any]:
    """User message invoking /understand-done."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:understand-done</command-name>"
        },
    }


@pytest.fixture
def assistant_skill_understand_done() -> dict[str, Any]:
    """Assistant Skill tool call for understand-done."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:understand-done"},
                }
            ]
        },
    }


@pytest.fixture
def user_do_command() -> dict[str, Any]:
    """User message invoking /do (workflow skill)."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:do</command-name> /tmp/manifest.md"
        },
    }


@pytest.fixture
def user_define_command() -> dict[str, Any]:
    """User message invoking /define (workflow skill)."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:define</command-name> build a widget"
        },
    }


@pytest.fixture
def assistant_text() -> dict[str, Any]:
    """Simple assistant text response."""
    return {
        "type": "assistant",
        "message": {"content": "Investigating the latency issue..."},
    }


def run_understand_prompt_hook(
    hook_input: dict[str, Any],
) -> subprocess.CompletedProcess:
    """Helper to run the understand_prompt_hook with given input."""
    return run_hook_raw("understand_prompt_hook.py", hook_input)


# -- parse_understand_flow tests --


class TestParseUnderstandFlowBasic:
    """Basic detection tests for parse_understand_flow."""

    def test_no_understand(self, temp_transcript, assistant_text):
        """No /understand in transcript -> has_understand=False."""
        path = temp_transcript([assistant_text])
        state = parse_understand_flow(path)
        assert not state.has_understand
        assert not state.is_complete
        assert state.understand_args is None

    def test_understand_user_command(
        self, temp_transcript, user_understand_command, assistant_text
    ):
        """User /understand command detected."""
        path = temp_transcript([user_understand_command, assistant_text])
        state = parse_understand_flow(path)
        assert state.has_understand
        assert not state.is_complete
        assert state.understand_args == "the latency problem in our API"

    def test_understand_skill_call(
        self, temp_transcript, assistant_skill_understand
    ):
        """Assistant Skill tool call for understand detected."""
        path = temp_transcript([assistant_skill_understand])
        state = parse_understand_flow(path)
        assert state.has_understand
        assert not state.is_complete
        assert state.understand_args == "the auth flow"

    def test_understand_no_args(
        self, temp_transcript, user_understand_no_args, assistant_text
    ):
        """Understand without args -> has_understand=True, args=None."""
        path = temp_transcript([user_understand_no_args, assistant_text])
        state = parse_understand_flow(path)
        assert state.has_understand
        assert state.understand_args is None

    def test_empty_transcript(self, tmp_path):
        """Empty transcript -> no understand flow."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("")
        state = parse_understand_flow(str(transcript))
        assert not state.has_understand

    def test_missing_transcript(self):
        """Missing file -> no understand flow (fail open)."""
        state = parse_understand_flow("/nonexistent/transcript.jsonl")
        assert not state.has_understand


class TestParseUnderstandFlowCompletion:
    """Completion detection tests."""

    def test_complete_via_understand_done_user(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        user_understand_done_command,
    ):
        """Complete when user invokes /understand-done."""
        path = temp_transcript(
            [user_understand_command, assistant_text, user_understand_done_command]
        )
        state = parse_understand_flow(path)
        assert state.has_understand
        assert state.is_complete

    def test_complete_via_understand_done_skill(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        assistant_skill_understand_done,
    ):
        """Complete when assistant Skill calls understand-done."""
        path = temp_transcript(
            [user_understand_command, assistant_text, assistant_skill_understand_done]
        )
        state = parse_understand_flow(path)
        assert state.has_understand
        assert state.is_complete

    def test_complete_via_define(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        user_define_command,
    ):
        """Complete when /define starts after /understand."""
        path = temp_transcript(
            [user_understand_command, assistant_text, user_define_command]
        )
        state = parse_understand_flow(path)
        assert state.has_understand
        assert state.is_complete

    def test_complete_via_do(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        user_do_command,
    ):
        """Complete when /do starts after /understand."""
        path = temp_transcript(
            [user_understand_command, assistant_text, user_do_command]
        )
        state = parse_understand_flow(path)
        assert state.has_understand
        assert state.is_complete

    def test_complete_via_auto(self, temp_transcript, user_understand_command):
        """Complete when /auto starts after /understand."""
        auto_command = {
            "type": "user",
            "message": {
                "content": "<command-name>/manifest-dev:auto</command-name> build it"
            },
        }
        path = temp_transcript([user_understand_command, auto_command])
        state = parse_understand_flow(path)
        assert state.has_understand
        assert state.is_complete


class TestParseUnderstandFlowReset:
    """Reset behavior tests."""

    def test_reset_on_new_understand(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        user_understand_done_command,
    ):
        """New /understand after /understand-done resets state."""
        second_understand = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:understand</command-name>"
                    "<command-args>a different topic</command-args>"
                )
            },
        }
        path = temp_transcript(
            [
                user_understand_command,
                assistant_text,
                user_understand_done_command,
                second_understand,
                assistant_text,
            ]
        )
        state = parse_understand_flow(path)
        assert state.has_understand
        assert not state.is_complete
        assert state.understand_args == "a different topic"

    def test_reset_after_workflow_skill(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        user_define_command,
    ):
        """New /understand after /define resets state."""
        second_understand = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:understand</command-name>"
                    "<command-args>something new</command-args>"
                )
            },
        }
        path = temp_transcript(
            [
                user_understand_command,
                assistant_text,
                user_define_command,
                second_understand,
                assistant_text,
            ]
        )
        state = parse_understand_flow(path)
        assert state.has_understand
        assert not state.is_complete
        assert state.understand_args == "something new"


class TestParseUnderstandFlowEdgeCases:
    """Edge case tests."""

    def test_malformed_lines(self, tmp_path):
        """Malformed JSONL lines are skipped gracefully."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("not json\n{broken\n")
        state = parse_understand_flow(str(transcript))
        assert not state.has_understand

    def test_understand_done_without_understand(
        self, temp_transcript, user_understand_done_command
    ):
        """/understand-done without prior /understand -> no effect."""
        path = temp_transcript([user_understand_done_command])
        state = parse_understand_flow(path)
        assert not state.has_understand
        assert not state.is_complete


# -- understand_prompt_hook tests --


class TestUnderstandPromptHookOutput:
    """Tests for cases where the hook SHOULD inject a reminder."""

    def test_reminder_when_understand_active(
        self, temp_transcript, user_understand_command, assistant_text
    ):
        """Should inject principles reminder when /understand is active."""
        transcript_path = temp_transcript([user_understand_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_understand_prompt_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "system-reminder" in context
        assert "Truth-convergence" in context

    def test_reminder_content(
        self, temp_transcript, user_understand_command, assistant_text
    ):
        """Reminder should contain key principles."""
        transcript_path = temp_transcript([user_understand_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_understand_prompt_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "Investigate before claiming" in context
        assert "don't reassure" in context.lower() or "reassure" in context.lower()


class TestUnderstandPromptHookNoOutput:
    """Tests for cases where the hook should NOT output anything."""

    def test_no_output_when_no_understand(self, temp_transcript, assistant_text):
        """Should not output when /understand hasn't been invoked."""
        transcript_path = temp_transcript([assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_understand_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_understand_done(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        user_understand_done_command,
    ):
        """Should not output after /understand-done."""
        transcript_path = temp_transcript(
            [user_understand_command, assistant_text, user_understand_done_command]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_understand_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_workflow_skill(
        self,
        temp_transcript,
        user_understand_command,
        assistant_text,
        user_define_command,
    ):
        """Should not output after /define starts."""
        transcript_path = temp_transcript(
            [user_understand_command, assistant_text, user_define_command]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_understand_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_missing_transcript(self):
        """Should not output when transcript doesn't exist."""
        hook_input = {"transcript_path": "/nonexistent/transcript.jsonl"}

        result = run_understand_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_no_transcript_path(self):
        """Should not output when transcript_path missing from input."""
        hook_input = {}

        result = run_understand_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_invalid_json_input(self):
        """Should not output for invalid JSON input (fail open)."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "understand_prompt_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_stderr_output(
        self, temp_transcript, user_understand_command, assistant_text
    ):
        """Hook should never write to stderr on success."""
        transcript_path = temp_transcript([user_understand_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_understand_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stderr.strip() == ""
