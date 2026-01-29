"""
Tests for manifest-dev stop_do_hook.

Tests the stop hook that enforces verification-first workflow for /do.
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
    """Path to the stop_do_hook.py script."""
    return EXPERIMENTAL_HOOKS_DIR / "stop_do_hook.py"


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


class TestStopHookBlocking:
    """Tests for stop hook blocking behavior."""

    def test_blocks_without_done(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be blocked when /do started but no /done or /escalate."""
        transcript_path = temp_transcript([user_do_command])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "block"
        assert "verify" in result["systemMessage"].lower()

    def test_blocks_with_verify_only(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
    ):
        """Stop should be blocked when /verify was called but returned failures (no /done)."""
        transcript_path = temp_transcript([user_do_command, assistant_skill_verify])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "block"


class TestStopHookAllowing:
    """Tests for stop hook allowing behavior."""

    def test_allows_with_done(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
        assistant_skill_done: dict[str, Any],
    ):
        """Stop should be allowed when /done exists after /do."""
        transcript_path = temp_transcript([
            user_do_command,
            assistant_skill_verify,
            assistant_skill_done,
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # None means no output, which means allow (exit 0)
        assert result is None

    def test_allows_with_escalate(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
        assistant_skill_escalate: dict[str, Any],
    ):
        """Stop should be allowed when /escalate exists after /do."""
        transcript_path = temp_transcript([
            user_do_command,
            assistant_skill_verify,
            assistant_skill_escalate,
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_allows_no_do(
        self,
        experimental_hook_path: Path,
        temp_transcript,
    ):
        """Stop should be allowed when no /do in transcript."""
        transcript_path = temp_transcript([
            {"type": "user", "message": {"content": "Hello"}}
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None


class TestStopHookFreshStack:
    """Tests for fresh stack behavior per /do."""

    def test_fresh_stack(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_done: dict[str, Any],
    ):
        """Second /do should reset flow state."""
        # First /do with /done, then second /do without /done
        second_do = {
            "type": "user",
            "message": {
                "content": "<command-name>/manifest-dev:do</command-name> /tmp/define2.md"
            },
        }
        transcript_path = temp_transcript([
            user_do_command,
            assistant_skill_done,
            second_do,  # New /do, no /done after
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should block because second /do has no /done
        assert result is not None
        assert result["decision"] == "block"


class TestStopHookApiErrors:
    """Tests for API error handling."""

    def test_allows_stop_on_api_error(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be allowed when most recent assistant message is an API error."""
        # API error message (like 529 Overloaded)
        api_error_message = {
            "type": "assistant",
            "isApiErrorMessage": True,
            "message": {
                "content": [{"type": "text", "text": "API Error: Repeated 529 Overloaded errors"}]
            },
        }
        transcript_path = temp_transcript([user_do_command, api_error_message])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # None means no output, which means allow (exit 0)
        assert result is None

    def test_blocks_after_api_error_recovery(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be blocked after API error recovery (normal message follows)."""
        api_error_message = {
            "type": "assistant",
            "isApiErrorMessage": True,
            "message": {
                "content": [{"type": "text", "text": "API Error: Repeated 529 Overloaded errors"}]
            },
        }
        # Normal assistant message after API error (recovery)
        normal_message = {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "Continuing with the work..."}]
            },
        }
        transcript_path = temp_transcript([user_do_command, api_error_message, normal_message])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should block because /do is in progress and no /done (api error is no longer recent)
        assert result is not None
        assert result["decision"] == "block"

    def test_allows_api_error_with_explicit_false_flag(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Normal message with explicit isApiErrorMessage=false should still be blocked."""
        normal_message = {
            "type": "assistant",
            "isApiErrorMessage": False,  # Explicitly false
            "message": {
                "content": [{"type": "text", "text": "I'm working on this..."}]
            },
        }
        transcript_path = temp_transcript([user_do_command, normal_message])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should block because /do is in progress and no /done
        assert result is not None
        assert result["decision"] == "block"


class TestStopHookLoopDetection:
    """Tests for infinite loop detection and prevention."""

    def test_allows_after_three_short_outputs(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be allowed after 3+ consecutive short outputs (loop detected)."""
        short_outputs = [
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "."}]},
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "Done."}]},
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "Waiting."}]},
            },
        ]
        transcript_path = temp_transcript([user_do_command] + short_outputs)
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "allow"
        assert "loop" in result["reason"].lower()

    def test_blocks_with_two_short_outputs(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should still be blocked with only 2 consecutive short outputs."""
        short_outputs = [
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "."}]},
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "Done."}]},
            },
        ]
        transcript_path = temp_transcript([user_do_command] + short_outputs)
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "block"
        # Message should mention /verify and /escalate options
        assert "/verify" in result["systemMessage"]
        assert "/escalate" in result["systemMessage"]

    def test_substantial_output_breaks_loop_pattern(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Substantial output should reset the loop counter."""
        transcript_path = temp_transcript([
            user_do_command,
            # Two short outputs
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
            # Substantial output breaks the pattern
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "x" * 150}]}},
            # Only one short output after substantial
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should block because only 1 consecutive short output after substantial
        assert result is not None
        assert result["decision"] == "block"

    def test_tool_use_breaks_loop_pattern(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Non-Skill tool use should reset the loop counter."""
        transcript_path = temp_transcript([
            user_do_command,
            # Two short outputs
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
            # Tool use (not Skill) breaks the pattern
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "Let me check"},
                        {"type": "tool_use", "name": "Read", "input": {"path": "/tmp/foo"}},
                    ]
                },
            },
            # Only one short output after tool use
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should block because only 1 consecutive short output after tool use
        assert result is not None
        assert result["decision"] == "block"

    def test_escalate_skill_allows_stop_even_in_loop(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Calling /escalate (via Skill) should allow stop regardless of loop pattern."""
        transcript_path = temp_transcript([
            user_do_command,
            # Short outputs with an escalate call in the middle
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "x"},
                        {"type": "tool_use", "name": "Skill", "input": {"skill": "escalate"}},
                    ]
                },
            },
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should allow because /escalate was called (proper workflow completion)
        # Loop detection doesn't apply when /escalate was invoked
        assert result is None

    def test_non_escalate_skill_does_not_break_loop_pattern(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Skill tool use for non-completion skills should not reset loop counter."""
        transcript_path = temp_transcript([
            user_do_command,
            # Three short outputs with a non-escalate Skill call
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "x"},
                        # Some other skill, not escalate/done
                        {"type": "tool_use", "name": "Skill", "input": {"skill": "some-other-skill"}},
                    ]
                },
            },
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "."}]}},
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should allow because 3 consecutive short outputs (Skill doesn't reset counter)
        assert result is not None
        assert result["decision"] == "allow"


class TestStopHookEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_transcript(
        self,
        experimental_hook_path: Path,
        temp_transcript,
    ):
        """Should allow stop on empty transcript."""
        transcript_path = temp_transcript([])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_missing_transcript(
        self,
        experimental_hook_path: Path,
    ):
        """Should allow stop on missing transcript."""
        hook_input = {"transcript_path": "/nonexistent/path.jsonl"}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_no_transcript_path(
        self,
        experimental_hook_path: Path,
    ):
        """Should allow stop when no transcript_path provided."""
        hook_input = {}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_malformed_json_in_transcript(
        self,
        experimental_hook_path: Path,
        tmp_path: Path,
    ):
        """Should handle malformed JSON in transcript gracefully."""
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w") as f:
            f.write("not valid json\n")
            f.write('{"type": "user"}\n')

        hook_input = {"transcript_path": str(transcript_file)}

        result = run_hook(experimental_hook_path, hook_input)

        # Should allow (fail open) on parsing errors
        assert result is None
