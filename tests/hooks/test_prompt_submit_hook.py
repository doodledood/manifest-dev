"""
Tests for manifest-dev prompt_submit_hook.

Tests the UserPromptSubmit hook that reminds Claude to check for manifest
amendments when user provides input during an active /do workflow.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

# Path to the hooks directory
HOOKS_DIR = (
    Path(__file__).parent.parent.parent / "claude-plugins" / "manifest-dev" / "hooks"
)


@pytest.fixture
def temp_transcript(tmp_path: Path):
    """Factory fixture for creating temporary transcript files."""

    def _create_transcript(lines: list[dict[str, Any]]) -> str:
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(json.dumps(line) + "\n")
        return str(transcript_file)

    return _create_transcript


@pytest.fixture
def user_do_command() -> dict[str, Any]:
    """User message invoking /do."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:do</command-name> /tmp/define.md"
        },
    }


@pytest.fixture
def assistant_skill_do() -> dict[str, Any]:
    """Assistant Skill tool call for do."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:do", "args": "/tmp/define.md"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_skill_done() -> dict[str, Any]:
    """Assistant Skill tool call for done."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:done"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_text() -> dict[str, Any]:
    """Simple assistant text response."""
    return {
        "type": "assistant",
        "message": {"content": "Working on AC-1.1..."},
    }


def run_prompt_submit_hook(
    hook_input: dict[str, Any],
) -> subprocess.CompletedProcess:
    """Helper to run the prompt_submit_hook with given input."""
    stdin_data = json.dumps(hook_input)

    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "prompt_submit_hook.py")],
        input=stdin_data,
        capture_output=True,
        text=True,
        cwd=str(HOOKS_DIR),
    )
    return result


class TestPromptSubmitHookOutput:
    """Tests for cases where the hook SHOULD inject a reminder."""

    def test_reminder_when_do_active_user_command(
        self, temp_transcript, user_do_command, assistant_text
    ):
        """Should inject amendment reminder when /do is active (user command)."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
        assert "AMENDMENT CHECK" in output["hookSpecificOutput"]["additionalContext"]

    def test_reminder_when_do_active_skill_call(
        self, temp_transcript, assistant_skill_do
    ):
        """Should inject amendment reminder when /do is active (Skill tool call)."""
        transcript_path = temp_transcript([assistant_skill_do])
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "AMENDMENT CHECK" in output["hookSpecificOutput"]["additionalContext"]

    def test_reminder_contains_amendment_instructions(
        self, temp_transcript, user_do_command, assistant_text
    ):
        """Reminder should contain instructions about escalate and /define --amend."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "Contradicts" in context
        assert "Extends" in context
        assert "/escalate" in context
        assert "/define --amend" in context


class TestPromptSubmitHookNoOutput:
    """Tests for cases where the hook should NOT output anything."""

    def test_no_output_when_no_do(self, temp_transcript):
        """Should not output when /do hasn't been invoked."""
        transcript_path = temp_transcript(
            [
                {
                    "type": "user",
                    "message": {"content": "Hello, can you help me?"},
                }
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_done(
        self, temp_transcript, user_do_command, assistant_text, assistant_skill_done
    ):
        """Should not output when /do completed (after /done)."""
        transcript_path = temp_transcript(
            [user_do_command, assistant_text, assistant_skill_done]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_empty_transcript(self, tmp_path):
        """Should not output for empty transcript."""
        transcript_file = tmp_path / "transcript.jsonl"
        transcript_file.write_text("")
        hook_input = {"transcript_path": str(transcript_file)}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_missing_transcript(self):
        """Should not output when transcript file doesn't exist."""
        hook_input = {"transcript_path": "/nonexistent/transcript.jsonl"}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_no_transcript_path(self):
        """Should not output when transcript_path is missing from input."""
        hook_input = {}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_invalid_json_input(self):
        """Should not output for invalid JSON input."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "prompt_submit_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )

        assert result.returncode == 0
        assert result.stdout.strip() == ""


class TestPromptSubmitHookEdgeCases:
    """Edge case tests."""

    def test_malformed_transcript_lines(self, tmp_path):
        """Should handle malformed JSONL gracefully."""
        transcript_file = tmp_path / "transcript.jsonl"
        transcript_file.write_text("not json\n{broken\n")
        hook_input = {"transcript_path": str(transcript_file)}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_do_then_done_then_new_do(
        self, temp_transcript, user_do_command, assistant_text, assistant_skill_done
    ):
        """Second /do after /done should trigger reminder."""
        second_do = {
            "type": "user",
            "message": {
                "content": "<command-name>/manifest-dev:do</command-name> /tmp/manifest2.md"
            },
        }
        transcript_path = temp_transcript(
            [
                user_do_command,
                assistant_text,
                assistant_skill_done,
                second_do,
                assistant_text,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "AMENDMENT CHECK" in output["hookSpecificOutput"]["additionalContext"]

    def test_no_stderr_output(self, temp_transcript, user_do_command, assistant_text):
        """Hook should never write to stderr on success."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        assert result.stderr.strip() == ""

    def test_still_active_after_escalate(self, temp_transcript, user_do_command):
        """After /escalate (Self-Amendment), /do is still active — hook should fire.

        The Self-Amendment flow: /do → /escalate → /define --amend → /do resume.
        After /escalate, the /do workflow is still active (escalate is an exit point
        recognized by stop_do_hook, but the workflow hasn't ended with /done).
        The prompt_submit_hook should still inject reminders.
        """
        escalate_call = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {
                            "skill": "manifest-dev:escalate",
                            "args": "Self-Amendment",
                        },
                    }
                ]
            },
        }
        transcript_path = temp_transcript([user_do_command, escalate_call])
        hook_input = {"transcript_path": transcript_path}

        result = run_prompt_submit_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "AMENDMENT CHECK" in output["hookSpecificOutput"]["additionalContext"]
