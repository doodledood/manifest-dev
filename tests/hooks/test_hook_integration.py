"""
Integration tests for manifest-dev hooks.

Tests realistic user scenarios where multiple hooks fire on the same transcript.
Each test simulates a real /do or /define session and verifies all hooks
behave correctly together — no contradictory reminders, correct state transitions,
proper interaction between hooks at each lifecycle stage.

Hook inventory:
- stop_do_hook.py (Stop) — blocks premature stops
- pretool_verify_hook.py (PreToolUse/Skill) — reminds to read manifest before /verify
- prompt_submit_hook.py (UserPromptSubmit) — checks for manifest amendments
- post_compact_hook.py (SessionStart/compact) — restores /do context after compaction
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hook_test_helpers import run_hook


def run_stop_hook(transcript_path: str) -> dict[str, Any] | None:
    return run_hook("stop_do_hook.py", {"transcript_path": transcript_path})


def run_pretool_verify(skill: str, args: str = "") -> dict[str, Any] | None:
    return run_hook(
        "pretool_verify_hook.py",
        {"tool_name": "Skill", "tool_input": {"skill": skill, "args": args}},
    )


def run_prompt_submit(transcript_path: str) -> dict[str, Any] | None:
    return run_hook("prompt_submit_hook.py", {"transcript_path": transcript_path})


def run_post_compact(transcript_path: str) -> dict[str, Any] | None:
    return run_hook("post_compact_hook.py", {"transcript_path": transcript_path})


# --- Transcript building helpers ---


def user_do(args: str = "/tmp/manifest.md") -> dict[str, Any]:
    return {
        "type": "user",
        "message": {"content": f"<command-name>/manifest-dev:do</command-name> {args}"},
    }


def user_message(text: str) -> dict[str, Any]:
    return {"type": "user", "message": {"content": text}}


def assistant_text(text: str = "Working on the task...") -> dict[str, Any]:
    """Assistant text response (no tool use — classified as idle by loop detection).

    NOTE: stop_do_hook's loop detection counts consecutive idle outputs (no
    non-Skill tool_use). 3+ consecutive idle outputs triggers the escape valve.
    Text length is irrelevant. Use substantial_work() for messages with tool use
    that should reset the idle counter.
    """
    return {"type": "assistant", "message": {"content": text}}


def substantial_work(
    text: str = "Implementing the feature...",
) -> dict[str, Any]:
    """Assistant message with a non-Skill tool use that breaks loop detection.

    Loop detection only counts Skill tool_use as non-meaningful. Any other
    tool_use (Read, Write, Edit, Bash, etc.) counts as meaningful and resets
    the consecutive short output counter.
    """
    return {
        "type": "assistant",
        "message": {
            "content": [
                {"type": "text", "text": text},
                {
                    "type": "tool_use",
                    "name": "Edit",
                    "input": {
                        "file_path": "/tmp/code.py",
                        "old_string": "x",
                        "new_string": "y",
                    },
                },
            ]
        },
    }


def assistant_short(text: str = ".") -> dict[str, Any]:
    """Short assistant output for loop detection."""
    return {"type": "assistant", "message": {"content": text}}


def skill_call(skill: str, args: str = "") -> dict[str, Any]:
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": f"manifest-dev:{skill}", "args": args},
                }
            ]
        },
    }


def tool_call(tool: str, input_data: dict | None = None) -> dict[str, Any]:
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": tool,
                    "input": input_data or {},
                }
            ]
        },
    }


def make_transcript(tmp_path: Path, lines: list[dict[str, Any]]) -> str:
    transcript_file = tmp_path / "transcript.jsonl"
    with open(transcript_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(json.dumps(line) + "\n")
    return str(transcript_file)


# === E2E LIFECYCLE TESTS ===


class TestHappyPathLifecycle:
    """Full /do session: invoke → work → verify → done → stop allowed."""

    def test_full_lifecycle_all_hooks_correct(self, tmp_path: Path):
        """Simulate complete /do session and verify each hook fires correctly."""
        # Phase 1: /do invoked, assistant starts working
        transcript = make_transcript(
            tmp_path, [user_do(), assistant_text("Starting AC-1.1...")]
        )

        # User submits input during work — amendment check fires
        amendment = run_prompt_submit(transcript)
        assert amendment is not None
        assert (
            "user message arrived during"
            in amendment["hookSpecificOutput"]["additionalContext"]
        )

        # TaskUpdate happens — log reminder fires

        # Stop attempted before verify — blocked
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"

        # Phase 2: /verify about to be called — pretool reminder fires
        verify_reminder = run_pretool_verify("manifest-dev:verify", "/tmp/manifest.md")
        assert verify_reminder is not None
        assert (
            "/verify appears to be starting"
            in verify_reminder["hookSpecificOutput"]["additionalContext"]
        )

        # Phase 3: /verify completes — posttool log reminder fires

        # Phase 4: /done called — update transcript
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                assistant_text("Work done"),
                skill_call("verify", "/tmp/manifest.md"),
                skill_call("done"),
            ],
        )

        # Stop now allowed after /done
        stop_result = run_stop_hook(transcript)
        assert stop_result is None  # no output = allow

        # Prompt submit should NOT fire after /done
        amendment = run_prompt_submit(transcript)
        assert amendment is None

        # PostToolUse log reminder should NOT fire after /done

    def test_verify_fail_then_retry_then_pass(self, tmp_path: Path):
        """/verify fails → assistant fixes → /verify again → /done."""
        # After first /verify (failures returned), assistant fixes with real work
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                substantial_work("Implementing AC-1.1..."),
                skill_call("verify", "/tmp/manifest.md"),
                substantial_work("Fixing AC-1.2 failures with code edits..."),
            ],
        )

        # Stop should be blocked — /verify was called but no /done yet
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"

        # TaskUpdate during fix — log reminder fires

        # Second /verify → /done
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                substantial_work("Implementing..."),
                skill_call("verify", "/tmp/manifest.md"),
                substantial_work("Fixing failures..."),
                skill_call("verify", "/tmp/manifest.md"),
                skill_call("done"),
            ],
        )

        # Now stop is allowed
        stop_result = run_stop_hook(transcript)
        assert stop_result is None


class TestSelfAmendmentCycle:
    """/do → user changes scope → /escalate → /define --amend → /do resumes."""

    def test_amendment_hooks_fire_correctly(self, tmp_path: Path):
        """Verify hooks at each stage of the Self-Amendment cycle."""
        # Stage 1: /do active, user submits contradicting input
        transcript = make_transcript(
            tmp_path, [user_do(), assistant_text("Working on AC-1.1...")]
        )

        # prompt_submit fires — amendment check
        amendment = run_prompt_submit(transcript)
        assert amendment is not None
        assert "/define --amend" in amendment["hookSpecificOutput"]["additionalContext"]

        # Stage 2: /escalate Self-Amendment called
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                assistant_text("Working..."),
                user_message("Actually, also handle dark mode"),
                skill_call("escalate", "Self-Amendment"),
            ],
        )

        # PostToolUse log reminder fires for /escalate

        # Stop BLOCKED after Self-Amendment — must continue to /define --amend
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"
        assert "self-amendment" in stop_result["reason"].lower()

        # prompt_submit still fires — /do hasn't ended via /done
        amendment = run_prompt_submit(transcript)
        assert amendment is not None

        # Stage 3: /define --amend called (not a /do milestone)

    def test_resumed_do_after_amendment_resets_state(self, tmp_path: Path):
        """After amendment, a new /do invocation resets hook state."""
        transcript = make_transcript(
            tmp_path,
            [
                # First /do
                user_do("/tmp/manifest.md"),
                substantial_work("Working on AC-1.1..."),
                skill_call("escalate", "Self-Amendment"),
                # /define --amend happens
                skill_call("define", "--amend /tmp/manifest.md"),
                # New /do with updated manifest
                user_do("/tmp/manifest.md"),
                substantial_work("Resuming with amended manifest..."),
            ],
        )

        # Stop should be blocked — new /do is active, no /done yet
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"

        # Posttool log reminder fires — new /do is active

        # Prompt submit fires — active /do
        amendment = run_prompt_submit(transcript)
        assert amendment is not None


class TestCompactionRecovery:
    """/do active → session compacted → hooks recover correctly."""

    def test_all_hooks_work_after_compaction(self, tmp_path: Path):
        """After compaction recovery, all hooks should function correctly."""
        # Transcript after compaction — /do was active before
        transcript = make_transcript(
            tmp_path,
            [
                user_do("/tmp/manifest.md"),
                assistant_text("Working on AC-1.1..."),
                # Compaction happened — this is what's left
            ],
        )

        # post_compact_hook fires — recovery reminder
        recovery = run_post_compact(transcript)
        assert recovery is not None
        ctx = recovery["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/manifest.md" in ctx

        # All other hooks still work after recovery

        amendment = run_prompt_submit(transcript)
        assert amendment is not None

        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"

    def test_compaction_after_verify_still_blocks_stop(self, tmp_path: Path):
        """Even after compaction, stop is blocked if /done hasn't been called."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do("/tmp/manifest.md"),
                assistant_text("Work done"),
                skill_call("verify", "/tmp/manifest.md"),
                # Compaction happened here — /done wasn't called yet
            ],
        )

        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"


class TestMediumRoutingLifecycle:
    """/do with --medium slack → hooks detect non-local medium correctly."""

    def test_medium_routing_detected_across_hooks(self, tmp_path: Path):
        """All hooks should work correctly with non-local medium."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do("/tmp/manifest.md --medium slack"),
                assistant_text("Working with Slack collaboration..."),
            ],
        )

        # All hooks fire normally during work

        amendment = run_prompt_submit(transcript)
        assert amendment is not None

        # Stop blocked before verify (even with non-local medium)
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"

    def test_medium_routing_allows_stop_after_verify(self, tmp_path: Path):
        """With non-local medium, stop is allowed after /verify (escalation posted to medium)."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do("/tmp/manifest.md --medium slack"),
                assistant_text("Working..."),
                skill_call("verify", "/tmp/manifest.md"),
            ],
        )

        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert "decision" not in stop_result  # omit decision = allow
        assert "external" in stop_result.get("systemMessage", "").lower()


class TestMultipleDoSessions:
    """Sequential /do invocations with different manifests."""

    def test_second_do_resets_all_hook_state(self, tmp_path: Path):
        """After first /do completes, second /do gets fresh hook behavior."""
        transcript = make_transcript(
            tmp_path,
            [
                # First /do → done
                user_do("/tmp/manifest-1.md"),
                substantial_work("First task..."),
                skill_call("verify", "/tmp/manifest-1.md"),
                skill_call("done"),
                # Second /do (different manifest)
                user_do("/tmp/manifest-2.md"),
                substantial_work("Second task..."),
            ],
        )

        # Stop should be blocked — second /do is active, no /done yet
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"

        # PostToolUse fires for second /do

        # Prompt submit fires for second /do
        amendment = run_prompt_submit(transcript)
        assert amendment is not None

    def test_done_from_first_do_doesnt_affect_second(self, tmp_path: Path):
        """prompt_submit should fire during second /do even though first /do called /done."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do("/tmp/manifest-1.md"),
                skill_call("done"),
                # Second /do
                user_do("/tmp/manifest-2.md"),
                assistant_text("Working on second task..."),
            ],
        )

        # /done from first /do shouldn't silence hooks for second /do
        amendment = run_prompt_submit(transcript)
        assert amendment is not None


class TestLoopDetectionInteraction:
    """Stop hook loop detection interacting with other hooks."""

    def test_loop_detection_allows_stop_after_repeated_short_outputs(
        self, tmp_path: Path
    ):
        """After 3+ consecutive idle outputs, stop is allowed to break loop."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                assistant_short("Ok."),
                assistant_short("Done."),
                assistant_short("."),
            ],
        )

        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert "decision" not in stop_result  # omit decision = allow
        assert (
            "idle" in stop_result.get("reason", "").lower()
            or "loop" in stop_result.get("reason", "").lower()
        )

    def test_substantial_output_breaks_loop_pattern(self, tmp_path: Path):
        """A non-Skill tool use between idle outputs resets the idle counter.

        Only non-Skill tool_use (Read, Edit, Write, Bash, etc.) counts as
        productive. Text-only outputs are idle regardless of length.
        """
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                assistant_short("Ok."),
                substantial_work("Implementing the feature..."),
                assistant_short("Done."),
            ],
        )

        # Only 1 short output at the end — not enough for loop detection
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"


class TestInterruptedDoHandling:
    """User interrupts /do mid-execution."""

    def test_interrupted_do_silences_all_hooks(self, tmp_path: Path):
        """After user interrupts /do before assistant responds, hooks go silent."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                user_message("[Request interrupted by user]"),
                assistant_text("OK, stopping."),
            ],
        )

        # All hooks should be silent — /do was interrupted
        stop_result = run_stop_hook(transcript)
        assert stop_result is None  # allow stop

        amendment = run_prompt_submit(transcript)
        assert amendment is None  # no amendment check

    def test_reinvoked_do_after_interrupt_works(self, tmp_path: Path):
        """Re-invoking /do after interrupt restores all hook behavior."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do("/tmp/manifest-1.md"),
                user_message("[Request interrupted by user]"),
                # Re-invoke
                user_do("/tmp/manifest-1.md"),
                assistant_text("Resuming..."),
            ],
        )

        # Hooks should fire for the re-invoked /do
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"


class TestEscalateTypesNotDistinguished:
    """Hooks treat all /escalate types the same — verify this is safe."""

    def test_blocking_escalate_allows_stop(self, tmp_path: Path):
        """Blocking issue escalation allows stop."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                assistant_text("Can't fix AC-5"),
                skill_call("escalate", "AC-5 blocking after 3 attempts"),
            ],
        )
        stop_result = run_stop_hook(transcript)
        assert stop_result is None  # allowed

    def test_self_amendment_escalate_blocks_stop(self, tmp_path: Path):
        """Self-Amendment escalation blocks stop — must continue to /define --amend."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                assistant_text("User changed scope"),
                skill_call("escalate", "Self-Amendment"),
            ],
        )
        stop_result = run_stop_hook(transcript)
        assert stop_result is not None
        assert stop_result["decision"] == "block"

    def test_pause_escalate_allows_stop(self, tmp_path: Path):
        """User-Requested Pause escalation allows stop."""
        transcript = make_transcript(
            tmp_path,
            [
                user_do(),
                assistant_text("User asked to pause"),
                skill_call("escalate", "User-Requested Pause"),
            ],
        )
        stop_result = run_stop_hook(transcript)
        assert stop_result is None  # allowed


class TestPretoolVerifyIsolation:
    """pretool_verify_hook only fires for /verify, not other skills."""

    def test_no_reminder_for_do_skill(self):
        result = run_pretool_verify("manifest-dev:do", "/tmp/manifest.md")
        assert result is None

    def test_no_reminder_for_escalate_skill(self):
        result = run_pretool_verify("manifest-dev:escalate", "AC-5 blocking")
        assert result is None

    def test_no_reminder_for_define_skill(self):
        result = run_pretool_verify("manifest-dev:define", "--amend /tmp/manifest.md")
        assert result is None

    def test_reminder_for_verify_with_prefix(self):
        result = run_pretool_verify("manifest-dev:verify", "/tmp/manifest.md")
        assert result is not None
        assert (
            "/verify appears to be starting"
            in result["hookSpecificOutput"]["additionalContext"]
        )

    def test_reminder_for_verify_without_prefix(self):
        result = run_pretool_verify("verify", "/tmp/manifest.md")
        assert result is not None
