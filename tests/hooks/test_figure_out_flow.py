"""
Tests for /figure-out flow detection and the figure_out_prompt_hook.

Tests parse_figure_out_flow() for transcript parsing and the
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

from hook_utils import parse_figure_out_flow


# -- Fixtures --


@pytest.fixture
def user_figure_out_command() -> dict[str, Any]:
    """User message invoking /figure-out."""
    return {
        "type": "user",
        "message": {
            "content": (
                "<command-name>/manifest-dev:figure-out</command-name>"
                "<command-args>the latency problem in our API</command-args>"
            )
        },
    }


@pytest.fixture
def user_figure_out_no_args() -> dict[str, Any]:
    """User message invoking /figure-out without arguments."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:figure-out</command-name>"
        },
    }


@pytest.fixture
def assistant_skill_figure_out() -> dict[str, Any]:
    """Assistant Skill tool call for figure-out."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {
                        "skill": "manifest-dev:figure-out",
                        "args": "the auth flow",
                    },
                }
            ]
        },
    }


@pytest.fixture
def user_figure_out_done_command() -> dict[str, Any]:
    """User message invoking /figure-out-done."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:figure-out-done</command-name>"
        },
    }


@pytest.fixture
def assistant_skill_figure_out_done() -> dict[str, Any]:
    """Assistant Skill tool call for figure-out-done."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:figure-out-done"},
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


def run_figure_out_prompt_hook(
    hook_input: dict[str, Any],
) -> subprocess.CompletedProcess:
    """Helper to run the figure_out_prompt_hook with given input."""
    return run_hook_raw("figure_out_prompt_hook.py", hook_input)


# -- parse_figure_out_flow tests --


class TestParseFigureOutFlowBasic:
    """Basic detection tests for parse_figure_out_flow."""

    def test_no_figure_out(self, temp_transcript, assistant_text):
        """No /figure-out in transcript -> has_figure_out=False."""
        path = temp_transcript([assistant_text])
        state = parse_figure_out_flow(path)
        assert not state.has_figure_out
        assert not state.is_complete
        assert state.figure_out_args is None

    def test_figure_out_user_command(
        self, temp_transcript, user_figure_out_command, assistant_text
    ):
        """User /figure-out command detected."""
        path = temp_transcript([user_figure_out_command, assistant_text])
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert not state.is_complete
        assert state.figure_out_args == "the latency problem in our API"

    def test_figure_out_skill_call(
        self, temp_transcript, assistant_skill_figure_out
    ):
        """Assistant Skill tool call for figure-out detected."""
        path = temp_transcript([assistant_skill_figure_out])
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert not state.is_complete
        assert state.figure_out_args == "the auth flow"

    def test_figure_out_no_args(
        self, temp_transcript, user_figure_out_no_args, assistant_text
    ):
        """Figure-out without args -> has_figure_out=True, args=None."""
        path = temp_transcript([user_figure_out_no_args, assistant_text])
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert state.figure_out_args is None

    def test_empty_transcript(self, tmp_path):
        """Empty transcript -> no figure-out flow."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("")
        state = parse_figure_out_flow(str(transcript))
        assert not state.has_figure_out

    def test_missing_transcript(self):
        """Missing file -> no figure-out flow (fail open)."""
        state = parse_figure_out_flow("/nonexistent/transcript.jsonl")
        assert not state.has_figure_out


class TestParseFigureOutFlowCompletion:
    """Completion detection tests."""

    def test_complete_via_figure_out_done_user(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        user_figure_out_done_command,
    ):
        """Complete when user invokes /figure-out-done."""
        path = temp_transcript(
            [user_figure_out_command, assistant_text, user_figure_out_done_command]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert state.is_complete

    def test_complete_via_figure_out_done_skill(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        assistant_skill_figure_out_done,
    ):
        """Complete when assistant Skill calls figure-out-done."""
        path = temp_transcript(
            [user_figure_out_command, assistant_text, assistant_skill_figure_out_done]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert state.is_complete

    def test_complete_via_define(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        user_define_command,
    ):
        """Complete when /define starts after /figure-out."""
        path = temp_transcript(
            [user_figure_out_command, assistant_text, user_define_command]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert state.is_complete

    def test_complete_via_do(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        user_do_command,
    ):
        """Complete when /do starts after /figure-out."""
        path = temp_transcript(
            [user_figure_out_command, assistant_text, user_do_command]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert state.is_complete

    def test_complete_via_auto(self, temp_transcript, user_figure_out_command):
        """Complete when /auto starts after /figure-out."""
        auto_command = {
            "type": "user",
            "message": {
                "content": "<command-name>/manifest-dev:auto</command-name> build it"
            },
        }
        path = temp_transcript([user_figure_out_command, auto_command])
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert state.is_complete


class TestParseFigureOutFlowReset:
    """Reset behavior tests."""

    def test_reset_on_new_figure_out(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        user_figure_out_done_command,
    ):
        """New /figure-out after /figure-out-done resets state."""
        second_figure_out = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:figure-out</command-name>"
                    "<command-args>a different topic</command-args>"
                )
            },
        }
        path = temp_transcript(
            [
                user_figure_out_command,
                assistant_text,
                user_figure_out_done_command,
                second_figure_out,
                assistant_text,
            ]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert not state.is_complete
        assert state.figure_out_args == "a different topic"

    def test_reset_after_workflow_skill(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        user_define_command,
    ):
        """New /figure-out after /define resets state."""
        second_figure_out = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:figure-out</command-name>"
                    "<command-args>something new</command-args>"
                )
            },
        }
        path = temp_transcript(
            [
                user_figure_out_command,
                assistant_text,
                user_define_command,
                second_figure_out,
                assistant_text,
            ]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert not state.is_complete
        assert state.figure_out_args == "something new"


class TestParseFigureOutFlowEdgeCases:
    """Edge case tests."""

    def test_malformed_lines(self, tmp_path):
        """Malformed JSONL lines are skipped gracefully."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text("not json\n{broken\n")
        state = parse_figure_out_flow(str(transcript))
        assert not state.has_figure_out

    def test_figure_out_done_without_figure_out(
        self, temp_transcript, user_figure_out_done_command
    ):
        """/figure-out-done without prior /figure-out -> no effect."""
        path = temp_transcript([user_figure_out_done_command])
        state = parse_figure_out_flow(path)
        assert not state.has_figure_out
        assert not state.is_complete

    def test_ismeta_expansion_does_not_reset(
        self, temp_transcript, user_figure_out_command, assistant_text
    ):
        """isMeta skill expansion after user /figure-out should not reset args."""
        ismeta_expansion = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": (
                    "Base directory for this skill: "
                    "/home/user/manifest-dev/claude-plugins/manifest-dev/skills/figure-out\n\n"
                    "Skill content here..."
                )
            },
        }
        path = temp_transcript(
            [user_figure_out_command, ismeta_expansion, assistant_text]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert not state.is_complete
        assert state.figure_out_args == "the latency problem in our API"

    def test_bare_figure_out_after_done_resets(
        self, temp_transcript, user_figure_out_command, assistant_text, user_figure_out_done_command
    ):
        """Bare /figure-out (no args) after /figure-out-done should start a new session."""
        bare_figure_out = {
            "type": "user",
            "message": {
                "content": "<command-name>/manifest-dev:figure-out</command-name>"
            },
        }
        path = temp_transcript(
            [
                user_figure_out_command,
                assistant_text,
                user_figure_out_done_command,
                bare_figure_out,
                assistant_text,
            ]
        )
        state = parse_figure_out_flow(path)
        assert state.has_figure_out
        assert not state.is_complete
        assert state.figure_out_args is None


# -- figure_out_prompt_hook tests --


class TestFigureOutPromptHookOutput:
    """Tests for cases where the hook SHOULD inject a reminder."""

    def test_reminder_when_figure_out_active(
        self, temp_transcript, user_figure_out_command, assistant_text
    ):
        """Should inject principles reminder when /figure-out is active."""
        transcript_path = temp_transcript([user_figure_out_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_figure_out_prompt_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "system-reminder" in context
        assert "figure-out" in context.lower()

    def test_reminder_content(
        self, temp_transcript, user_figure_out_command, assistant_text
    ):
        """Reminder should contain self-check questions and principles."""
        transcript_path = temp_transcript([user_figure_out_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_figure_out_prompt_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "verified" in context.lower()
        assert "come prepared" in context.lower()


class TestFigureOutPromptHookNoOutput:
    """Tests for cases where the hook should NOT output anything."""

    def test_no_output_when_no_figure_out(self, temp_transcript, assistant_text):
        """Should not output when /figure-out hasn't been invoked."""
        transcript_path = temp_transcript([assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_figure_out_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_figure_out_done(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        user_figure_out_done_command,
    ):
        """Should not output after /figure-out-done."""
        transcript_path = temp_transcript(
            [user_figure_out_command, assistant_text, user_figure_out_done_command]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_figure_out_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_workflow_skill(
        self,
        temp_transcript,
        user_figure_out_command,
        assistant_text,
        user_define_command,
    ):
        """Should not output after /define starts."""
        transcript_path = temp_transcript(
            [user_figure_out_command, assistant_text, user_define_command]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_figure_out_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_missing_transcript(self):
        """Should not output when transcript doesn't exist."""
        hook_input = {"transcript_path": "/nonexistent/transcript.jsonl"}

        result = run_figure_out_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_no_transcript_path(self):
        """Should not output when transcript_path missing from input."""
        hook_input = {}

        result = run_figure_out_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_invalid_json_input(self):
        """Should not output for invalid JSON input (fail open)."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "figure_out_prompt_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_stderr_output(
        self, temp_transcript, user_figure_out_command, assistant_text
    ):
        """Hook should never write to stderr on success."""
        transcript_path = temp_transcript([user_figure_out_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_figure_out_prompt_hook(hook_input)

        assert result.returncode == 0
        assert result.stderr.strip() == ""
