"""
Tests for manifest-dev pretool_verify_hook.

Tests the PreToolUse hook that reminds to read manifest/log before verification.
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


def run_pretool_verify_hook(hook_input: dict[str, Any]) -> subprocess.CompletedProcess:
    """Helper to run the pretool-verify hook with given input."""
    stdin_data = json.dumps(hook_input)

    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "pretool_verify_hook.py")],
        input=stdin_data,
        capture_output=True,
        text=True,
        cwd=str(HOOKS_DIR),
    )
    return result


class TestPretoolVerifyHookNoOutput:
    """Tests for cases where the hook should not output anything."""

    def test_no_output_for_non_skill_tool(self):
        """Should not output anything for non-Skill tool calls."""
        hook_input = {
            "tool_name": "Read",
            "tool_input": {"file_path": "/tmp/foo.txt"},
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_for_non_verify_skill(self):
        """Should not output anything for non-verify Skill calls."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:do", "args": "/tmp/manifest.md"},
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_for_done_skill(self):
        """Should not output anything for /done Skill calls."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:done"},
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_output_for_escalate_skill(self):
        """Should not output anything for /escalate Skill calls."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {"skill": "manifest-dev:escalate", "args": "blocking issue"},
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""


class TestPretoolVerifyHookOutputs:
    """Tests for verify skill reminder outputs."""

    def test_outputs_reminder_for_verify_skill(self):
        """Should output reminder for /verify Skill calls."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/do-log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert "additionalContext" in output["hookSpecificOutput"]

    def test_reminder_contains_verify_args(self):
        """Reminder should contain the verify arguments."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/do-log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context
        assert "/tmp/do-log.md" in context

    def test_reminder_wrapped_in_system_reminder(self):
        """Reminder should be wrapped in system-reminder tags."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/do-log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "<system-reminder>" in context
        assert "</system-reminder>" in context

    def test_reminder_mentions_acceptance_criteria(self):
        """Reminder should mention acceptance criteria."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/do-log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "AC-" in context or "acceptance criteria" in context.lower()

    def test_reminder_mentions_global_invariants(self):
        """Reminder should mention global invariants."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/do-log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "INV-G" in context or "invariant" in context.lower()


class TestPretoolVerifyHookSkillNameVariants:
    """Tests for different verify skill name formats."""

    def test_handles_short_skill_name(self):
        """Should handle short skill name 'verify'."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "verify",
                "args": "/tmp/manifest.md /tmp/log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context

    def test_handles_full_skill_name(self):
        """Should handle full skill name 'manifest-dev:verify'."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context


class TestPretoolVerifyHookArgsVariants:
    """Tests for different argument formats."""

    def test_handles_scope_flag_in_args(self):
        """Should include --scope flag in displayed args."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/log.md --scope=files",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context
        assert "/tmp/log.md" in context
        # Args are displayed as-is
        assert "--scope" in context

    def test_handles_empty_args(self):
        """Should output minimal reminder when args are empty."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        # Should still have a reminder about verification
        assert "verification" in context.lower() or "AC-" in context

    def test_handles_no_args_key(self):
        """Should output minimal reminder when args key is missing."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "verification" in context.lower() or "AC-" in context

    def test_handles_manifest_only(self):
        """Should handle when only manifest path is provided (no log)."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in context


class TestPretoolVerifyHookEdgeCases:
    """Edge case tests for the pretool-verify hook."""

    def test_handles_invalid_json_stdin(self):
        """Should handle invalid JSON in stdin gracefully."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "pretool_verify_hook.py")],
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
            [sys.executable, str(HOOKS_DIR / "pretool_verify_hook.py")],
            input="",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_handles_missing_tool_name(self):
        """Should handle missing tool_name gracefully."""
        hook_input = {
            "tool_input": {"skill": "manifest-dev:verify"},
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_handles_missing_tool_input(self):
        """Should handle missing tool_input gracefully."""
        hook_input = {
            "tool_name": "Skill",
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_no_stderr_on_success(self):
        """Hook should not produce stderr output on success."""
        hook_input = {
            "tool_name": "Skill",
            "tool_input": {
                "skill": "manifest-dev:verify",
                "args": "/tmp/manifest.md /tmp/log.md",
            },
        }
        result = run_pretool_verify_hook(hook_input)

        assert result.stderr == ""
