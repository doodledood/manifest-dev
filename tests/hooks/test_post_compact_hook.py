"""
Tests for manifest-dev post_compact_hook.

Tests the SessionStart hook (compact matcher) that restores /do workflow context after compaction.
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


def run_post_compact_hook(
    transcript_lines: list[dict[str, Any]] | None = None,
    transcript_path: str | None = None,
    tmp_path: Path | None = None,
) -> subprocess.CompletedProcess:
    """Helper to run the post-compact hook with given transcript."""
    # Create transcript file if lines provided
    if transcript_lines is not None and tmp_path is not None:
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w", encoding="utf-8") as f:
            for line in transcript_lines:
                f.write(json.dumps(line) + "\n")
        transcript_path = str(transcript_file)

    # Prepare stdin input
    hook_input = {"transcript_path": transcript_path or ""}
    stdin_data = json.dumps(hook_input)

    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
        input=stdin_data,
        capture_output=True,
        text=True,
        cwd=str(HOOKS_DIR),
    )
    return result


@pytest.fixture
def user_do_command() -> dict[str, Any]:
    """User message invoking /do with manifest path."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:do</command-name> /tmp/manifest.md"
        },
    }


@pytest.fixture
def user_do_command_with_log() -> dict[str, Any]:
    """User message invoking /do with manifest and log path."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:do</command-name> /tmp/manifest.md /tmp/do-log.md"
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
                    "input": {
                        "skill": "manifest-dev:do",
                        "args": "/tmp/manifest.md /tmp/do-log.md",
                    },
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
def assistant_skill_escalate() -> dict[str, Any]:
    """Assistant Skill tool call for escalate."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:escalate", "args": "AC-5 blocking"},
                }
            ]
        },
    }


class TestPostCompactHookNoOutput:
    """Tests for cases where the hook should not output anything."""

    def test_no_output_without_do(self, tmp_path: Path):
        """Should not output anything when no /do in transcript."""
        lines = [{"type": "user", "message": {"content": "Hello"}}]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_without_transcript(self):
        """Should not output anything when no transcript path provided."""
        result = run_post_compact_hook(transcript_path="")

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_done(
        self,
        tmp_path: Path,
        user_do_command: dict[str, Any],
        assistant_skill_done: dict[str, Any],
    ):
        """Should not output anything when /do workflow completed with /done."""
        lines = [user_do_command, assistant_skill_done]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_escalate(
        self,
        tmp_path: Path,
        user_do_command: dict[str, Any],
        assistant_skill_escalate: dict[str, Any],
    ):
        """Should not output anything when /do workflow completed with /escalate."""
        lines = [user_do_command, assistant_skill_escalate]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_nonexistent_transcript(self):
        """Should not output anything for nonexistent transcript."""
        result = run_post_compact_hook(transcript_path="/nonexistent/path.jsonl")

        assert result.returncode == 0
        assert result.stdout.strip() == ""


class TestPostCompactHookWithActiveDoWorkflow:
    """Tests for active /do workflow recovery reminders."""

    def test_outputs_reminder_for_active_do(
        self, tmp_path: Path, user_do_command: dict[str, Any]
    ):
        """Should output recovery reminder when /do is active."""
        lines = [user_do_command]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert output["hookSpecificOutput"]["hookEventName"] == "SessionStart"
        assert "additionalContext" in output["hookSpecificOutput"]

    def test_reminder_contains_do_args(
        self, tmp_path: Path, user_do_command: dict[str, Any]
    ):
        """Recovery reminder should contain the /do arguments."""
        lines = [user_do_command]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context

    def test_reminder_wrapped_in_system_reminder(
        self, tmp_path: Path, user_do_command: dict[str, Any]
    ):
        """Recovery reminder should be wrapped in system-reminder tags."""
        lines = [user_do_command]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "<system-reminder>" in context
        assert "</system-reminder>" in context

    def test_reminder_includes_both_args_when_provided(
        self, tmp_path: Path, user_do_command_with_log: dict[str, Any]
    ):
        """Should include both manifest and log paths when both provided."""
        lines = [user_do_command_with_log]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context
        assert "/tmp/do-log.md" in context

    def test_reminder_from_skill_call(
        self, tmp_path: Path, assistant_skill_do: dict[str, Any]
    ):
        """Should extract args from Skill tool call for /do."""
        lines = [assistant_skill_do]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context
        assert "/tmp/do-log.md" in context


class TestPostCompactHookArgsExtraction:
    """Tests for /do args extraction from various formats."""

    def test_extracts_from_user_command_string_content(self, tmp_path: Path):
        """Should extract args from user command with string content."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/manifest-dev:do</command-name> /path/to/manifest.md /path/to/log.md"
                },
            }
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/path/to/manifest.md" in context
        assert "/path/to/log.md" in context

    def test_extracts_from_user_command_array_content(self, tmp_path: Path):
        """Should extract args from user command with array content."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "text",
                            "text": "<command-name>/manifest-dev:do</command-name> /path/manifest.md",
                        }
                    ]
                },
            }
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/path/manifest.md" in context

    def test_extracts_from_skill_call_short_name(self, tmp_path: Path):
        """Should extract args from Skill call with short skill name."""
        lines = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {"skill": "do", "args": "/manifest.md /log.md"},
                        }
                    ]
                },
            }
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/manifest.md" in context
        assert "/log.md" in context

    def test_second_do_resets_args(self, tmp_path: Path):
        """Second /do should use its own args, not the first /do."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/manifest-dev:do</command-name> /first/manifest.md"
                },
            },
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/manifest-dev:do</command-name> /second/manifest.md"
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/second/manifest.md" in context
        # First manifest should not be present
        assert "/first/manifest.md" not in context


class TestPostCompactHookEdgeCases:
    """Edge case tests for the post-compact hook."""

    def test_handles_invalid_json_stdin(self):
        """Should handle invalid JSON in stdin gracefully."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_handles_empty_stdin(self):
        """Should handle empty stdin gracefully."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
            input="",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_handles_empty_transcript(self, tmp_path: Path):
        """Should handle empty transcript file."""
        result = run_post_compact_hook(transcript_lines=[], tmp_path=tmp_path)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_handles_malformed_transcript_lines(self, tmp_path: Path):
        """Should handle transcript with some malformed lines."""
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w") as f:
            f.write("not json\n")
            f.write(
                '{"type": "user", "message": {"content": "<command-name>/manifest-dev:do</command-name> /tmp/manifest.md"}}\n'
            )
            f.write("also not json\n")

        hook_input = {"transcript_path": str(transcript_file)}
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )

        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context

    def test_no_stderr_on_success(
        self, tmp_path: Path, user_do_command: dict[str, Any]
    ):
        """Hook should not produce stderr output on success."""
        lines = [user_do_command]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        assert result.stderr == ""

    def test_fallback_message_when_no_args(self, tmp_path: Path):
        """Should output fallback reminder when /do has no extractable args."""
        # /do detected via is_user_skill_command but args extraction fails
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/manifest-dev:do</command-name>"
                },
            }
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        # Should still have a reminder about checking /tmp for logs
        assert "do-log" in context or "/tmp" in context
