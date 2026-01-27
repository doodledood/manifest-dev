"""
Tests for manifest-dev pretool_escalate_hook.

Tests the PreToolUse hook that gates /escalate calls.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

# Add manifest-dev hooks directory to path
EXPERIMENTAL_HOOKS_DIR = (
    Path(__file__).parent.parent.parent
    / "claude-plugins"
    / "manifest-dev"
    / "hooks"
)


@pytest.fixture
def experimental_hook_path() -> Path:
    """Path to the pretool_escalate_hook.py script."""
    return EXPERIMENTAL_HOOKS_DIR / "pretool_escalate_hook.py"


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
def assistant_skill_verify() -> dict[str, Any]:
    """Assistant Skill tool call for verify."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:verify", "args": "/tmp/define.md"},
                }
            ]
        },
    }


def run_hook(hook_path: Path, hook_input: dict[str, Any]) -> dict[str, Any] | None:
    """Run the hook script and return parsed output, or None if no output."""
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
        cwd=str(EXPERIMENTAL_HOOKS_DIR),
    )
    if result.stdout.strip():
        return json.loads(result.stdout)
    return None


class TestEscalateHookBlocking:
    """Tests for escalate hook blocking behavior."""

    def test_blocks_without_verify(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """/escalate should be blocked when /verify not called first."""
        transcript_path = temp_transcript([user_do_command])
        hook_input = {
            "transcript_path": transcript_path,
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:escalate", "args": "AC-5 blocking"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "block"
        assert "verify" in result["systemMessage"].lower()

    def test_blocks_no_do(
        self,
        experimental_hook_path: Path,
        temp_transcript,
    ):
        """/escalate should be blocked when no /do in progress."""
        transcript_path = temp_transcript([
            {"type": "user", "message": {"content": "Hello"}}
        ])
        hook_input = {
            "transcript_path": transcript_path,
            "tool_name": "Skill",
            "tool_input": {"skill": "escalate"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "block"
        assert "no /do" in result["systemMessage"].lower()


class TestEscalateHookAllowing:
    """Tests for escalate hook allowing behavior."""

    def test_allows_after_verify(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
    ):
        """/escalate should be allowed after /verify was called."""
        transcript_path = temp_transcript([
            user_do_command,
            assistant_skill_verify,
        ])
        hook_input = {
            "transcript_path": transcript_path,
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:escalate", "args": "AC-5 blocking"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        # None means no output, which means allow
        assert result is None

    def test_ignores_non_skill_tools(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Hook should not block non-Skill tool calls."""
        transcript_path = temp_transcript([user_do_command])
        hook_input = {
            "transcript_path": transcript_path,
            "tool_name": "Bash",
            "tool_input": {"command": "echo test"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_ignores_non_escalate_skills(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Hook should not block other skill calls."""
        transcript_path = temp_transcript([user_do_command])
        hook_input = {
            "transcript_path": transcript_path,
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:verify"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None


class TestEscalateHookEdgeCases:
    """Tests for edge cases and error handling."""

    def test_short_skill_name(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
    ):
        """Should work with short skill name 'escalate' (no plugin prefix)."""
        transcript_path = temp_transcript([
            user_do_command,
            assistant_skill_verify,
        ])
        hook_input = {
            "transcript_path": transcript_path,
            "tool_name": "Skill",
            "tool_input": {"skill": "escalate"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_missing_transcript(
        self,
        experimental_hook_path: Path,
    ):
        """Should allow on missing transcript (fail open)."""
        hook_input = {
            "transcript_path": "/nonexistent/path.jsonl",
            "tool_name": "Skill",
            "tool_input": {"skill": "escalate"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        # Missing transcript means no /do, so should block
        assert result is not None
        assert result["decision"] == "block"

    def test_no_transcript_path(
        self,
        experimental_hook_path: Path,
    ):
        """Should allow when no transcript_path provided."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "escalate"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        # No path means fail open
        assert result is None

    def test_verify_resets_on_new_do(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
    ):
        """New /do should reset /verify state."""
        second_do = {
            "type": "user",
            "message": {
                "content": "<command-name>/manifest-dev:do</command-name> /tmp/define2.md"
            },
        }
        # First /do + /verify, then second /do (no /verify after)
        transcript_path = temp_transcript([
            user_do_command,
            assistant_skill_verify,
            second_do,
        ])
        hook_input = {
            "transcript_path": transcript_path,
            "tool_name": "Skill",
            "tool_input": {"skill": "escalate"},
        }

        result = run_hook(experimental_hook_path, hook_input)

        # Should block because second /do has no /verify after
        assert result is not None
        assert result["decision"] == "block"
