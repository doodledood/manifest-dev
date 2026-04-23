"""
Tests for manifest-dev posttool_log_hook.

Tests the PostToolUse hook that reminds Claude to update the execution log
after milestone tool calls during an active /do workflow.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any

from hook_test_helpers import HOOKS_DIR, run_hook_raw


def run_posttool_log_hook(hook_input: dict[str, Any]) -> subprocess.CompletedProcess:
    """Helper to run the posttool_log_hook with given input."""
    return run_hook_raw("posttool_log_hook.py", hook_input)
    return result


class TestPosttoolLogHookOutput:
    """Tests for cases where the hook SHOULD inject a reminder."""

    def test_reminder_on_task_update(self, temp_transcript, user_do_command, assistant_text):
        """Should inject reminder when TaskUpdate completes during /do."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "TaskUpdate",
            "tool_input": {},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert output["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
        assert "milestone-shaped tool call" in output["hookSpecificOutput"]["additionalContext"]
        assert "TaskUpdate" in output["hookSpecificOutput"]["additionalContext"]

    def test_reminder_on_task_create(self, temp_transcript, user_do_command, assistant_text):
        """Should inject reminder when TaskCreate completes during /do."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "TaskCreate",
            "tool_input": {},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "milestone-shaped tool call" in output["hookSpecificOutput"]["additionalContext"]

    def test_reminder_on_todo_write(self, temp_transcript, user_do_command, assistant_text):
        """Should inject reminder when TodoWrite completes during /do."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "TodoWrite",
            "tool_input": {},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "milestone-shaped tool call" in output["hookSpecificOutput"]["additionalContext"]

    def test_reminder_on_skill_verify(self, temp_transcript, user_do_command, assistant_text):
        """Should inject reminder when /verify skill completes during /do."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:verify", "args": "/tmp/manifest.md"},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        ctx = output["hookSpecificOutput"]["additionalContext"]
        assert "milestone-shaped tool call" in ctx
        assert "manifest-dev:verify" in ctx

    def test_reminder_on_skill_escalate(self, temp_transcript, user_do_command, assistant_text):
        """Should inject reminder when /escalate skill completes during /do."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:escalate", "args": "Self-Amendment"},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "milestone-shaped tool call" in output["hookSpecificOutput"]["additionalContext"]

    def test_reminder_on_skill_define(self, temp_transcript, user_do_command, assistant_text):
        """Should inject reminder when /define skill completes during /do."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "define", "args": "--amend /tmp/manifest.md"},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "milestone-shaped tool call" in output["hookSpecificOutput"]["additionalContext"]

    def test_reminder_on_skill_done(self, temp_transcript, user_do_command, assistant_text):
        """Should inject reminder when /done skill completes during /do.

        Note: /done marks completion, but the hook fires AFTER the tool call.
        The hook checks transcript state BEFORE the current tool's effect is recorded,
        so /done hasn't been registered yet when the hook runs.
        """
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:done"},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "milestone-shaped tool call" in output["hookSpecificOutput"]["additionalContext"]


class TestPosttoolLogHookNoOutput:
    """Tests for cases where the hook should NOT output anything."""

    def test_no_output_non_milestone_skill(
        self, temp_transcript, user_do_command, assistant_text
    ):
        """Should not output for non-workflow skills like /learn."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:learn-from-session"},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_when_no_do(self, temp_transcript):
        """Should not output when /do hasn't been invoked."""
        transcript_path = temp_transcript(
            [{"type": "user", "message": {"content": "Hello"}}]
        )
        hook_input = {
            "tool_name": "TodoWrite",
            "tool_input": {},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_after_done(
        self, temp_transcript, user_do_command, assistant_text, assistant_skill_done
    ):
        """Should not output when /do completed (after /done in transcript)."""
        transcript_path = temp_transcript(
            [user_do_command, assistant_text, assistant_skill_done]
        )
        hook_input = {
            "tool_name": "TodoWrite",
            "tool_input": {},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_missing_transcript(self):
        """Should not output when transcript file doesn't exist."""
        hook_input = {
            "tool_name": "TodoWrite",
            "tool_input": {},
            "transcript_path": "/nonexistent/transcript.jsonl",
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_no_transcript_path(self):
        """Should not output when transcript_path is missing from input."""
        hook_input = {"tool_name": "TodoWrite", "tool_input": {}}

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_invalid_json_input(self):
        """Should not output for invalid JSON input."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "posttool_log_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )

        assert result.returncode == 0
        assert result.stdout.strip() == ""


class TestPosttoolLogHookEdgeCases:
    """Edge case tests."""

    def test_empty_transcript(self, tmp_path):
        """Should handle empty transcript gracefully."""
        transcript_file = tmp_path / "transcript.jsonl"
        transcript_file.write_text("")
        hook_input = {
            "tool_name": "TodoWrite",
            "tool_input": {},
            "transcript_path": str(transcript_file),
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_malformed_transcript_lines(self, tmp_path):
        """Should handle malformed JSONL gracefully."""
        transcript_file = tmp_path / "transcript.jsonl"
        transcript_file.write_text("not json\n{broken\n")
        hook_input = {
            "tool_name": "TaskUpdate",
            "tool_input": {},
            "transcript_path": str(transcript_file),
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_stderr_output(self, temp_transcript, user_do_command, assistant_text):
        """Hook should never write to stderr on success."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "TaskUpdate",
            "tool_input": {},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        assert result.stderr.strip() == ""

    def test_short_skill_name_without_plugin_prefix(
        self, temp_transcript, user_do_command, assistant_text
    ):
        """Should handle skill names without plugin prefix."""
        transcript_path = temp_transcript([user_do_command, assistant_text])
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "verify", "args": "/tmp/manifest.md"},
            "transcript_path": transcript_path,
        }

        result = run_posttool_log_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "milestone-shaped tool call" in output["hookSpecificOutput"]["additionalContext"]
