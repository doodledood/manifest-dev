"""
Tests for manifest-dev stop_do_hook.

Tests the stop hook that enforces verification-first workflow for /do.
"""

from __future__ import annotations

from typing import Any

import pytest

from hook_test_helpers import run_hook


class TestStopHookBlocking:
    """Tests for stop hook blocking behavior."""

    def test_blocks_without_done(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be blocked when /do started but no /done or /escalate."""
        transcript_path = temp_transcript([user_do_command])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "block"
        assert "verify" in result["systemMessage"].lower()

    def test_blocks_with_verify_only(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
    ):
        """Stop should be blocked when /verify was called but returned failures (no /done)."""
        transcript_path = temp_transcript([user_do_command, assistant_skill_verify])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "block"


class TestStopHookAllowing:
    """Tests for stop hook allowing behavior."""

    def test_allows_with_done(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
        assistant_skill_done: dict[str, Any],
    ):
        """Stop should be allowed when /done exists after /do."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                assistant_skill_verify,
                assistant_skill_done,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # None means no output, which means allow (exit 0)
        assert result is None

    def test_allows_with_escalate(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
        assistant_skill_escalate: dict[str, Any],
    ):
        """Stop should be allowed when /escalate exists after /do."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                assistant_skill_verify,
                assistant_skill_escalate,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is None

    def test_blocks_with_self_amendment_escalate(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be BLOCKED after Self-Amendment escalation.

        Self-Amendment is a mechanical exit that requires /define --amend
        before stopping. Unlike blocking/pause escalations, the workflow
        must continue autonomously.
        """
        self_amendment_escalate = {
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
        transcript_path = temp_transcript(
            [user_do_command, self_amendment_escalate]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "block"
        assert "self-amendment" in result["reason"].lower()

    def test_allows_no_do(
        self,
        temp_transcript,
    ):
        """Stop should be allowed when no /do in transcript."""
        transcript_path = temp_transcript(
            [{"type": "user", "message": {"content": "Hello"}}]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is None


class TestStopHookFreshStack:
    """Tests for fresh stack behavior per /do."""

    def test_fresh_stack(
        self,
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
        transcript_path = temp_transcript(
            [
                user_do_command,
                assistant_skill_done,
                second_do,  # New /do, no /done after
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because second /do has no /done
        assert result is not None
        assert result["decision"] == "block"


class TestStopHookApiErrors:
    """Tests for API error handling."""

    def test_allows_stop_on_api_error(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be allowed when most recent assistant message is an API error."""
        # API error message (like 529 Overloaded)
        api_error_message = {
            "type": "assistant",
            "isApiErrorMessage": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": "API Error: Repeated 529 Overloaded errors",
                    }
                ]
            },
        }
        transcript_path = temp_transcript([user_do_command, api_error_message])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # None means no output, which means allow (exit 0)
        assert result is None

    def test_blocks_after_api_error_recovery(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Stop should be blocked after API error recovery (normal message follows)."""
        api_error_message = {
            "type": "assistant",
            "isApiErrorMessage": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": "API Error: Repeated 529 Overloaded errors",
                    }
                ]
            },
        }
        # Normal assistant message after API error (recovery)
        normal_message = {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "Continuing with the work..."}]
            },
        }
        transcript_path = temp_transcript(
            [user_do_command, api_error_message, normal_message]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because /do is in progress and no /done (api error is no longer recent)
        assert result is not None
        assert result["decision"] == "block"

    def test_allows_api_error_with_explicit_false_flag(
        self,
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

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because /do is in progress and no /done
        assert result is not None
        assert result["decision"] == "block"


class TestStopHookLoopDetection:
    """Tests for infinite loop detection and prevention."""

    def test_allows_after_three_short_outputs(
        self,
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

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "allow"
        assert "loop" in result["reason"].lower()

    def test_blocks_with_two_short_outputs(
        self,
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

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "block"
        # Message should mention /verify and /escalate options
        assert "/verify" in result["systemMessage"]
        assert "/escalate" in result["systemMessage"]

    def test_substantial_output_breaks_loop_pattern(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Substantial output should reset the loop counter."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                # Two short outputs
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
                # Substantial output breaks the pattern
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "x" * 150}]},
                },
                # Only one short output after substantial
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because only 1 consecutive short output after substantial
        assert result is not None
        assert result["decision"] == "block"

    def test_tool_use_breaks_loop_pattern(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Non-Skill tool use should reset the loop counter."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                # Two short outputs
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
                # Tool use (not Skill) breaks the pattern
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "Let me check"},
                            {
                                "type": "tool_use",
                                "name": "Read",
                                "input": {"path": "/tmp/foo"},
                            },
                        ]
                    },
                },
                # Only one short output after tool use
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because only 1 consecutive short output after tool use
        assert result is not None
        assert result["decision"] == "block"

    def test_escalate_skill_allows_stop_even_in_loop(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Calling /escalate (via Skill) should allow stop regardless of loop pattern."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                # Short outputs with an escalate call in the middle
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "x"},
                            {
                                "type": "tool_use",
                                "name": "Skill",
                                "input": {"skill": "escalate"},
                            },
                        ]
                    },
                },
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should allow because /escalate was called (proper workflow completion)
        # Loop detection doesn't apply when /escalate was invoked
        assert result is None

    def test_non_escalate_skill_does_not_break_loop_pattern(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
    ):
        """Skill tool use for non-completion skills should not reset loop counter."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                # Three short outputs with a non-escalate Skill call
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "x"},
                            # Some other skill, not escalate/done
                            {
                                "type": "tool_use",
                                "name": "Skill",
                                "input": {"skill": "some-other-skill"},
                            },
                        ]
                    },
                },
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "."}]},
                },
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should allow because 3 consecutive short outputs (Skill doesn't reset counter)
        assert result is not None
        assert result["decision"] == "allow"


class TestStopHookInvocationPatterns:
    """Tests for various skill invocation patterns."""

    def test_detects_short_command_name(
        self,
        temp_transcript,
    ):
        """Should detect /do via short command-name (/<skill> without plugin prefix)."""
        # This is the actual format produced when users type /do
        user_do_short = {
            "type": "user",
            "message": {
                "content": "<command-name>/do</command-name><command-args>/tmp/define.md</command-args>"
            },
        }
        transcript_path = temp_transcript([user_do_short])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because /do detected but no /done
        assert result is not None
        assert result["decision"] == "block"

    def test_detects_ismeta_skill_expansion(
        self,
        temp_transcript,
    ):
        """Should detect /do via isMeta skill expansion."""
        # This is the actual format when skill content is injected
        ismeta_do_expansion = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": "Base directory for this skill: /path/to/plugins/skills/do\n\n# /do - Manifest Executor\n\n...",
                    }
                ]
            },
        }
        transcript_path = temp_transcript([ismeta_do_expansion])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because /do detected but no /done
        assert result is not None
        assert result["decision"] == "block"

    def test_define_expansion_referencing_do_does_not_trigger(
        self,
        temp_transcript,
    ):
        """isMeta /define expansion referencing skills/do/ in body should NOT detect /do."""
        # Real bug: /define SKILL.md references "../do/references/execution-modes/"
        # in its body text. The isMeta regex was matching this as a /do invocation.
        ismeta_define_expansion = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Base directory for this skill: /path/to/plugins/skills/define\n\n"
                            "# /define - Manifest Builder\n\n"
                            "Build a comprehensive Manifest...\n\n"
                            "## Verification Loop\n\n"
                            "After writing the manifest, check the manifest's `mode:` field "
                            "and the `/define manifest-verifier` row in "
                            "`../do/references/execution-modes/`.\n\n"
                            "To execute: /do /tmp/manifest-{timestamp}.md"
                        ),
                    }
                ]
            },
        }
        transcript_path = temp_transcript([ismeta_define_expansion])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — no /do invocation, just /define referencing a /do file path
        assert result is None

    def test_detects_combined_command_and_ismeta(
        self,
        temp_transcript,
        assistant_skill_done: dict[str, Any],
    ):
        """Should handle combined command-name + isMeta (real world pattern)."""
        # Real world pattern: command line followed by isMeta expansion
        user_do_command_line = {
            "type": "user",
            "message": {
                "content": "<command-name>/do</command-name><command-args>/tmp/define.md</command-args>"
            },
        }
        ismeta_expansion = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": "Base directory for this skill: /path/to/plugins/skills/do\n\n# /do - Manifest Executor\n\n...",
                    }
                ]
            },
        }
        transcript_path = temp_transcript(
            [
                user_do_command_line,
                ismeta_expansion,
                assistant_skill_done,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should allow because /done was called
        assert result is None

    def test_second_do_resets_after_done(
        self,
        temp_transcript,
        assistant_skill_done: dict[str, Any],
    ):
        """Second /do (via isMeta) should reset state after first /done."""
        first_do = {
            "type": "user",
            "message": {
                "content": "<command-name>/do</command-name><command-args>/tmp/first.md</command-args>"
            },
        }
        second_do_command = {
            "type": "user",
            "message": {
                "content": "<command-name>/do</command-name><command-args>/tmp/second.md</command-args>"
            },
        }
        second_do_ismeta = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": "Base directory for this skill: /path/to/plugins/skills/do\n\n# /do - Manifest Executor",
                    }
                ]
            },
        }
        transcript_path = temp_transcript(
            [
                first_do,
                assistant_skill_done,  # Complete first /do
                second_do_command,
                second_do_ismeta,
                # No /done for second /do
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should block because second /do has no /done
        assert result is not None
        assert result["decision"] == "block"

    def test_ignores_other_plugin_prefix(
        self,
        temp_transcript,
    ):
        """Should NOT detect /do from other plugins - only manifest-dev:do or /do."""
        user_do_other_plugin = {
            "type": "user",
            "message": {
                "content": "<command-name>/other-plugin:do</command-name><command-args>/tmp/define.md</command-args>"
            },
        }
        transcript_path = temp_transcript([user_do_other_plugin])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should allow - not our plugin's /do
        assert result is None


class TestStopHookEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_transcript(
        self,
        temp_transcript,
    ):
        """Should allow stop on empty transcript."""
        transcript_path = temp_transcript([])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is None

    def test_missing_transcript(
        self,
    ):
        """Should allow stop on missing transcript."""
        hook_input = {"transcript_path": "/nonexistent/path.jsonl"}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is None

    def test_no_transcript_path(
        self,
    ):
        """Should allow stop when no transcript_path provided."""
        hook_input = {}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is None

    def test_malformed_json_in_transcript(
        self,
        tmp_path: Path,
    ):
        """Should handle malformed JSON in transcript gracefully."""
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w") as f:
            f.write("not valid json\n")
            f.write('{"type": "user"}\n')

        hook_input = {"transcript_path": str(transcript_file)}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should allow (fail open) on parsing errors
        assert result is None


class TestStopHookCollabMode:
    """Tests for non-local medium collaboration mode behavior."""

    def test_allows_verify_with_medium_slack(
        self,
        temp_transcript,
        assistant_skill_verify: dict[str, Any],
    ):
        """With --medium slack, /do + /verify should ALLOW stop (escalation posted to medium)."""
        user_do_medium = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:do</command-name>"
                    "<command-args>/tmp/manifest.md --medium slack"
                    "</command-args>"
                )
            },
        }
        transcript_path = temp_transcript([user_do_medium, assistant_skill_verify])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "allow"
        assert "medium" in result["reason"].lower()

    def test_blocks_without_verify_even_with_medium(
        self,
        temp_transcript,
    ):
        """With --medium slack, /do without /verify should still BLOCK."""
        user_do_medium = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:do</command-name>"
                    "<command-args>/tmp/manifest.md --medium slack"
                    "</command-args>"
                )
            },
        }
        transcript_path = temp_transcript([user_do_medium])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "block"

    def test_still_blocks_verify_without_medium(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
    ):
        """Without --medium, /do + /verify should still BLOCK (local mode behavior unchanged)."""
        transcript_path = temp_transcript([user_do_command, assistant_skill_verify])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "block"

    def test_medium_via_skill_tool_call(
        self,
        temp_transcript,
        assistant_skill_verify: dict[str, Any],
    ):
        """Should detect --medium in Skill tool call args."""
        assistant_do_with_medium = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {
                            "skill": "manifest-dev:do",
                            "args": "/tmp/manifest.md --medium discord",
                        },
                    }
                ]
            },
        }
        transcript_path = temp_transcript(
            [assistant_do_with_medium, assistant_skill_verify]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "allow"

    def test_medium_local_does_not_trigger_collab(
        self,
        temp_transcript,
        assistant_skill_verify: dict[str, Any],
    ):
        """--medium local should NOT trigger collab mode (same as no --medium)."""
        user_do_local = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:do</command-name>"
                    "<command-args>/tmp/manifest.md --medium local"
                    "</command-args>"
                )
            },
        }
        transcript_path = temp_transcript([user_do_local, assistant_skill_verify])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        assert result is not None
        assert result["decision"] == "block"

    def test_medium_local_prefix_is_collab(
        self,
        temp_transcript,
        assistant_skill_verify: dict[str, Any],
    ):
        """--medium local-dev should trigger collab mode (not a false negative)."""
        user_do_local_dev = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:do</command-name>"
                    "<command-args>/tmp/manifest.md --medium local-dev"
                    "</command-args>"
                )
            },
        }
        transcript_path = temp_transcript(
            [user_do_local_dev, assistant_skill_verify]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # local-dev is NOT "local" — it should be treated as collab mode
        assert result is not None
        assert result["decision"] == "allow"


class TestStopHookInterruptHandling:
    """Tests for user interrupt handling during /do workflow.

    Bug: When /do is invoked but the user immediately interrupts before
    the assistant responds, the hook still treats the session as having
    an active /do workflow, blocking all subsequent stops.
    """

    @pytest.fixture
    def user_interrupt(self) -> dict[str, Any]:
        """User interrupt message."""
        return {
            "type": "user",
            "message": {"content": "[Request interrupted by user]"},
        }

    @pytest.fixture
    def user_regular_message(self) -> dict[str, Any]:
        """Regular user message (no skill invocation)."""
        return {
            "type": "user",
            "message": {"content": "Please continue with the define work"},
        }

    @pytest.fixture
    def assistant_working(self) -> dict[str, Any]:
        """Assistant doing substantial work (editing files)."""
        return {
            "type": "assistant",
            "message": {
                "content": [
                    {"type": "text", "text": "I'll update the manifest now."},
                    {
                        "type": "tool_use",
                        "name": "Edit",
                        "input": {"file_path": "/tmp/manifest.md"},
                    },
                ]
            },
        }

    @pytest.fixture
    def ismeta_do_expansion(self) -> dict[str, Any]:
        """isMeta expansion for /do skill."""
        return {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Base directory for this skill: "
                            "/path/to/plugins/skills/do\n\n"
                            "# /do - Manifest Executor\n\n..."
                        ),
                    }
                ]
            },
        }

    @pytest.fixture
    def ismeta_define_expansion(self) -> dict[str, Any]:
        """isMeta expansion for /define skill (references skills/do/ in body)."""
        return {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Base directory for this skill: "
                            "/path/to/plugins/skills/define\n\n"
                            "# /define - Manifest Builder\n\n"
                            "Build a comprehensive Manifest...\n\n"
                            "Check `../do/references/execution-modes/`.\n\n"
                            "To execute: /do /tmp/manifest-{timestamp}.md"
                        ),
                    }
                ]
            },
        }

    def test_allows_stop_after_interrupted_do(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        user_interrupt: dict[str, Any],
    ):
        """Stop should be allowed when /do was invoked but immediately interrupted."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                user_interrupt,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — /do was cancelled by interrupt before assistant processed it
        assert result is None

    def test_blocks_when_do_interrupted_after_assistant_response(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        assistant_working: dict[str, Any],
        user_interrupt: dict[str, Any],
    ):
        """Stop should still block when /do was interrupted AFTER assistant started processing."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                assistant_working,  # Assistant started /do work
                user_interrupt,  # User interrupts mid-execution
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should BLOCK — /do was active and assistant was working
        assert result is not None
        assert result["decision"] == "block"

    def test_interrupted_do_then_reinvoked_still_blocks(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        user_interrupt: dict[str, Any],
    ):
        """When /do is interrupted then re-invoked, the second /do should block."""
        second_do = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/manifest-dev:do</command-name>"
                    "<command-args>/tmp/define.md</command-args>"
                )
            },
        }
        transcript_path = temp_transcript(
            [
                user_do_command,
                user_interrupt,  # First /do cancelled
                second_do,  # New /do invocation
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should BLOCK — second /do is active and has no /done
        assert result is not None
        assert result["decision"] == "block"

    def test_session_reproduction_do_interrupted_then_define_continues(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        user_interrupt: dict[str, Any],
        user_regular_message: dict[str, Any],
        assistant_working: dict[str, Any],
    ):
        """Reproduce exact session bug: /do invoked, interrupted, then /define work continues.

        This is the exact scenario from session 7ae7e4d8:
        1. User invokes /do (command-name + isMeta)
        2. User immediately interrupts
        3. User sends regular message continuing /define work
        4. Assistant works on /define content
        5. Stop hook should NOT block
        """
        ismeta_do = {
            "type": "user",
            "isMeta": True,
            "message": {
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Base directory for this skill: "
                            "/path/to/plugins/skills/do\n\n"
                            "# /do - Manifest Executor\n\n..."
                        ),
                    }
                ]
            },
        }
        transcript_path = temp_transcript(
            [
                user_do_command,  # /do command (line 944 in session)
                ismeta_do,  # isMeta expansion (line 945)
                user_interrupt,  # Interrupt (line 948)
                user_regular_message,  # Regular message (line 950)
                assistant_working,  # Assistant works on /define (lines 952+)
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — /do was cancelled by interrupt, assistant is doing /define work
        assert result is None

    def test_allows_stop_after_interrupted_do_then_regular_messages(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        user_interrupt: dict[str, Any],
        user_regular_message: dict[str, Any],
    ):
        """Stop should be allowed after interrupted /do followed by regular conversation."""
        transcript_path = temp_transcript(
            [
                user_do_command,
                user_interrupt,
                user_regular_message,
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "Sure, I'll help with that."}
                        ]
                    },
                },
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — /do was cancelled
        assert result is None

    def test_multiple_interrupts(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        user_interrupt: dict[str, Any],
    ):
        """Multiple /do invocations each interrupted should all be cancelled."""
        second_do = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/do</command-name>"
                    "<command-args>/tmp/second.md</command-args>"
                )
            },
        }
        transcript_path = temp_transcript(
            [
                user_do_command,
                user_interrupt,  # First /do cancelled
                second_do,
                user_interrupt,  # Second /do cancelled
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — both /do invocations were cancelled
        assert result is None

    def test_assistant_skill_do_then_interrupted_still_blocks(
        self,
        temp_transcript,
        assistant_skill_do: dict[str, Any],
        user_interrupt: dict[str, Any],
    ):
        """When /do is invoked via assistant Skill tool call, interrupt should NOT cancel it.

        Pattern 1 (assistant Skill tool_use) means the assistant is already processing,
        so the interrupt is mid-execution, not a cancellation.
        """
        transcript_path = temp_transcript(
            [
                assistant_skill_do,
                user_interrupt,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should BLOCK — assistant was already processing /do
        assert result is not None
        assert result["decision"] == "block"

    def test_interrupted_do_with_ismeta_expansion(
        self,
        temp_transcript,
        user_interrupt: dict[str, Any],
        ismeta_do_expansion: dict[str, Any],
    ):
        """isMeta /do expansion followed by interrupt should cancel /do."""
        user_do_short = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/do</command-name>"
                    "<command-args>/tmp/define.md</command-args>"
                )
            },
        }
        transcript_path = temp_transcript(
            [
                user_do_short,
                ismeta_do_expansion,
                user_interrupt,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — /do + isMeta was interrupted before assistant processed
        assert result is None

    def test_interrupted_do_then_done_reinvoked_and_completed(
        self,
        temp_transcript,
        user_do_command: dict[str, Any],
        user_interrupt: dict[str, Any],
        assistant_skill_done: dict[str, Any],
    ):
        """Interrupted /do followed by successful /do with /done should allow."""
        second_do = {
            "type": "user",
            "message": {
                "content": (
                    "<command-name>/do</command-name>"
                    "<command-args>/tmp/define.md</command-args>"
                )
            },
        }
        transcript_path = temp_transcript(
            [
                user_do_command,
                user_interrupt,  # First /do cancelled
                second_do,  # New /do
                assistant_skill_done,  # Properly completed
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — second /do was properly completed with /done
        assert result is None

    def test_interrupt_without_do_is_harmless(
        self,
        temp_transcript,
        user_interrupt: dict[str, Any],
    ):
        """Interrupt without any /do should not affect anything."""
        transcript_path = temp_transcript(
            [
                {"type": "user", "message": {"content": "Hello"}},
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "Hi there!"}]},
                },
                user_interrupt,
            ]
        )
        hook_input = {"transcript_path": transcript_path}

        result = run_hook("stop_do_hook.py", hook_input)

        # Should ALLOW — no /do in transcript
        assert result is None
