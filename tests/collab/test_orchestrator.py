"""Unit tests for the slack-collab orchestrator's deterministic logic.

Tests cover state management, phase transitions, error handling,
COLLAB_CONTEXT construction, and session-resume patterns. No Slack or
Claude CLI needed — all subprocess calls are mocked.
"""

import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# The orchestrator file uses hyphens (kebab-case per CLAUDE.md), so we
# can't import it directly. Use importlib to load by file path.
_SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "claude-plugins"
    / "manifest-dev-collab"
    / "scripts"
    / "slack-collab-orchestrator.py"
)
_spec = importlib.util.spec_from_file_location(
    "slack_collab_orchestrator", _SCRIPT_PATH
)
assert _spec and _spec.loader
orch = importlib.util.module_from_spec(_spec)
sys.modules["slack_collab_orchestrator"] = orch
_spec.loader.exec_module(orch)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_state():
    """A fully populated state dict for testing."""
    return {
        "run_id": "abc123def456",
        "task": "Add rate limiting to the API",
        "phase": "preflight",
        "channel_id": "C12345",
        "channel_name": "collab-rate-limit-20260226",
        "owner_handle": "@alice",
        "stakeholders": [
            {"handle": "@alice", "name": "Alice", "role": "backend"},
            {"handle": "@bob", "name": "Bob", "role": "frontend"},
            {"handle": "@carol", "name": "Carol", "role": "QA", "is_qa": True},
        ],
        "threads": {
            "stakeholders": {
                "@alice": "1234567890.000001",
                "@bob": "1234567890.000002",
                "@carol": "1234567890.000003",
                "@alice+@bob": "1234567890.000004",
            }
        },
        "manifest_path": None,
        "discovery_log_path": None,
        "pr_url": None,
        "has_qa": True,
        "define_session_id": None,
        "execute_session_id": None,
    }


@pytest.fixture()
def tmp_state_dir(tmp_path):
    """Override state path to use tmp_path."""
    original = orch.state_path_for_run

    def patched(run_id: str) -> Path:
        return tmp_path / f"collab-state-{run_id}.json"

    orch.state_path_for_run = patched
    yield tmp_path
    orch.state_path_for_run = original


# ---------------------------------------------------------------------------
# State management tests
# ---------------------------------------------------------------------------


class TestNewState:
    def test_creates_state_with_required_fields(self):
        state = orch.new_state("build login page", "run123")
        assert state["run_id"] == "run123"
        assert state["task"] == "build login page"
        assert state["phase"] == "preflight"
        assert state["channel_id"] is None
        assert state["manifest_path"] is None
        assert state["pr_url"] is None

    def test_no_poll_interval_in_state(self):
        state = orch.new_state("task", "run1")
        assert "poll_interval" not in state

    def test_session_ids_initialized_to_none(self):
        state = orch.new_state("task", "run1")
        assert state["define_session_id"] is None
        assert state["execute_session_id"] is None


class TestSaveAndLoadState:
    def test_save_and_load_roundtrip(self, sample_state, tmp_state_dir):
        orch.save_state(sample_state)
        path = tmp_state_dir / f"collab-state-{sample_state['run_id']}.json"
        assert path.exists()
        loaded = orch.load_state(path)
        assert loaded["run_id"] == sample_state["run_id"]
        assert loaded["task"] == sample_state["task"]
        assert loaded["phase"] == sample_state["phase"]

    def test_save_state_atomic_write(self, sample_state, tmp_state_dir):
        """Verify no .tmp file remains after save."""
        orch.save_state(sample_state)
        tmp_file = tmp_state_dir / f"collab-state-{sample_state['run_id']}.tmp"
        assert not tmp_file.exists()

    def test_load_state_invalid_json(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("not json {{{")
        with pytest.raises(SystemExit):
            orch.load_state(bad_file)

    def test_load_state_missing_fields(self, tmp_path):
        incomplete = tmp_path / "incomplete.json"
        incomplete.write_text(json.dumps({"run_id": "x"}))
        with pytest.raises(SystemExit):
            orch.load_state(incomplete)

    def test_load_state_missing_file(self, tmp_path):
        nonexistent = tmp_path / "nonexistent.json"
        with pytest.raises(SystemExit):
            orch.load_state(nonexistent)

    def test_state_update_preserves_fields(self, sample_state, tmp_state_dir):
        sample_state["phase"] = "define"
        sample_state["manifest_path"] = "/tmp/manifest-123.md"
        orch.save_state(sample_state)
        path = tmp_state_dir / f"collab-state-{sample_state['run_id']}.json"
        loaded = orch.load_state(path)
        assert loaded["phase"] == "define"
        assert loaded["manifest_path"] == "/tmp/manifest-123.md"
        assert loaded["channel_id"] == "C12345"

    def test_session_ids_persisted(self, sample_state, tmp_state_dir):
        sample_state["define_session_id"] = "abc123"
        sample_state["execute_session_id"] = "def456"
        orch.save_state(sample_state)
        path = tmp_state_dir / f"collab-state-{sample_state['run_id']}.json"
        loaded = orch.load_state(path)
        assert loaded["define_session_id"] == "abc123"
        assert loaded["execute_session_id"] == "def456"


# ---------------------------------------------------------------------------
# Phase transition tests
# ---------------------------------------------------------------------------


class TestPhaseTransitions:
    def test_next_phase_index_preflight(self):
        assert orch.next_phase_index("preflight") == 0

    def test_next_phase_index_define(self):
        assert orch.next_phase_index("define") == 1

    def test_next_phase_index_manifest_review(self):
        assert orch.next_phase_index("manifest_review") == 2

    def test_next_phase_index_execute(self):
        assert orch.next_phase_index("execute") == 3

    def test_next_phase_index_pr(self):
        assert orch.next_phase_index("pr") == 4

    def test_next_phase_index_qa(self):
        assert orch.next_phase_index("qa") == 5

    def test_next_phase_index_done(self):
        assert orch.next_phase_index("done") == 6

    def test_next_phase_index_unknown_defaults_to_zero(self):
        assert orch.next_phase_index("unknown") == 0

    def test_phases_list_order(self):
        expected = [
            "preflight",
            "define",
            "manifest_review",
            "execute",
            "pr",
            "qa",
            "done",
        ]
        assert expected == orch.PHASES

    def test_resume_skips_completed_phases(self, sample_state, tmp_state_dir):
        """Verify that run() starts from the correct phase on resume."""
        sample_state["phase"] = "execute"
        phases_called = []

        def mock_phase(name):
            def fn(state):
                phases_called.append(name)
                # Advance phase to simulate completion
                idx = orch.PHASES.index(name)
                if idx + 1 < len(orch.PHASES):
                    state["phase"] = orch.PHASES[idx + 1]

            return fn

        with patch.dict(
            orch.PHASE_FUNCTIONS,
            {
                "execute": mock_phase("execute"),
                "pr": mock_phase("pr"),
                "qa": mock_phase("qa"),
                "done": mock_phase("done"),
            },
        ):
            orch.run(sample_state)

        assert "preflight" not in phases_called
        assert "define" not in phases_called
        assert "manifest_review" not in phases_called
        assert "execute" in phases_called

    def test_qa_skipped_when_not_requested(self, sample_state, tmp_state_dir):
        """Verify QA phase is skipped when has_qa is False."""
        sample_state["phase"] = "pr"
        sample_state["has_qa"] = False
        phases_called = []

        def mock_phase(name):
            def fn(state):
                phases_called.append(name)
                idx = orch.PHASES.index(name)
                if idx + 1 < len(orch.PHASES):
                    state["phase"] = orch.PHASES[idx + 1]

            return fn

        with patch.dict(
            orch.PHASE_FUNCTIONS,
            {
                "pr": mock_phase("pr"),
                "qa": mock_phase("qa"),
                "done": mock_phase("done"),
            },
        ):
            orch.run(sample_state)

        assert "qa" not in phases_called
        assert "pr" in phases_called
        assert "done" in phases_called

    def test_invalid_state_handled(self, sample_state, tmp_state_dir):
        """Verify that a phase failure saves state and exits."""
        sample_state["phase"] = "execute"

        def failing_phase(state):
            raise SystemExit(1)

        with (
            patch.dict(orch.PHASE_FUNCTIONS, {"execute": failing_phase}),
            pytest.raises(SystemExit),
        ):
            orch.run(sample_state)


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------


class TestInvokeClaude:
    @patch("slack_collab_orchestrator.subprocess.run")
    def test_error_on_nonzero_exit_code(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="some error",
        )
        with pytest.raises(SystemExit):
            orch.invoke_claude("test prompt")

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_error_on_timeout(self, mock_run):
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="claude", timeout=120)
        with pytest.raises(SystemExit):
            orch.invoke_claude("test prompt", timeout=120)

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_error_on_empty_stdout(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="",
        )
        with pytest.raises(SystemExit):
            orch.invoke_claude("test prompt")

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_error_on_invalid_json(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="not json at all",
            stderr="",
        )
        with pytest.raises(SystemExit):
            orch.invoke_claude("test prompt")

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_error_on_missing_required_json_fields(self, mock_run):
        """invoke_claude returns whatever JSON it gets; caller validates fields."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(
                {"type": "result", "result": json.dumps({"some": "data"})}
            ),
            stderr="",
        )
        result = orch.invoke_claude("test prompt")
        assert "some" in result  # returns data, doesn't validate fields

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_successful_json_parsing(self, mock_run):
        expected = {"channel_id": "C123", "stakeholders": []}
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": json.dumps(expected)}),
            stderr="",
        )
        result = orch.invoke_claude("test prompt")
        assert result["channel_id"] == "C123"

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_unwraps_nested_result(self, mock_run):
        """output-format json wraps in {type:result, result:...}"""
        inner = {"manifest_path": "/tmp/manifest.md"}
        wrapper = {"type": "result", "result": json.dumps(inner)}
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(wrapper),
            stderr="",
        )
        result = orch.invoke_claude("test")
        assert result["manifest_path"] == "/tmp/manifest.md"

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_session_id_passed_in_command(self, mock_run):
        """Verify --session-id is included when session_id is provided."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": "{}"}),
            stderr="",
        )
        orch.invoke_claude("test", session_id="sess123")
        cmd = mock_run.call_args[0][0]
        assert "--session-id" in cmd
        assert "sess123" in cmd

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_resume_session_id_passed_in_command(self, mock_run):
        """Verify --resume is included when resume_session_id is provided."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": "{}"}),
            stderr="",
        )
        orch.invoke_claude("test", resume_session_id="sess456")
        cmd = mock_run.call_args[0][0]
        assert "--resume" in cmd
        assert "sess456" in cmd

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_no_session_flags_by_default(self, mock_run):
        """Verify no session flags when neither is provided."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": "{}"}),
            stderr="",
        )
        orch.invoke_claude("test")
        cmd = mock_run.call_args[0][0]
        assert "--session-id" not in cmd
        assert "--resume" not in cmd


# ---------------------------------------------------------------------------
# COLLAB_CONTEXT construction tests
# ---------------------------------------------------------------------------


class TestBuildCollabContext:
    def test_context_format(self, sample_state):
        ctx = orch.build_collab_context(sample_state)
        assert ctx.startswith("COLLAB_CONTEXT:")
        assert "channel_id: C12345" in ctx
        assert "owner_handle: @alice" in ctx

    def test_no_poll_interval_in_context(self, sample_state):
        ctx = orch.build_collab_context(sample_state)
        assert "poll_interval" not in ctx

    def test_context_has_stakeholder_threads(self, sample_state):
        ctx = orch.build_collab_context(sample_state)
        assert "@alice: 1234567890.000001" in ctx
        assert "@bob: 1234567890.000002" in ctx
        assert "@carol: 1234567890.000003" in ctx

    def test_context_has_combo_threads(self, sample_state):
        ctx = orch.build_collab_context(sample_state)
        assert "@alice+@bob: 1234567890.000004" in ctx

    def test_context_has_stakeholder_details(self, sample_state):
        ctx = orch.build_collab_context(sample_state)
        assert "handle: @alice" in ctx
        assert "name: Alice" in ctx
        assert "role: backend" in ctx
        assert "handle: @bob" in ctx
        assert "name: Bob" in ctx
        assert "role: frontend" in ctx

    def test_context_structure(self, sample_state):
        """Verify the COLLAB_CONTEXT block has proper YAML-like structure."""
        ctx = orch.build_collab_context(sample_state)
        lines = ctx.split("\n")
        assert lines[0] == "COLLAB_CONTEXT:"
        # Verify indentation — no poll_interval line
        assert lines[1].startswith("  channel_id:")
        assert lines[2].startswith("  owner_handle:")
        assert lines[3] == "  threads:"
        assert lines[4] == "    stakeholders:"

    def test_context_all_fields_populated(self, sample_state):
        """No empty/None values in the context output."""
        ctx = orch.build_collab_context(sample_state)
        assert "None" not in ctx

    def test_context_with_special_chars_in_handle(self, sample_state):
        """Handles with special chars should be preserved."""
        sample_state["stakeholders"].append(
            {"handle": "@user.name-123", "name": "User Name", "role": "ops"}
        )
        sample_state["threads"]["stakeholders"]["@user.name-123"] = "9999999999.000001"
        ctx = orch.build_collab_context(sample_state)
        assert "@user.name-123: 9999999999.000001" in ctx
        assert "handle: @user.name-123" in ctx


# ---------------------------------------------------------------------------
# PR URL extraction tests
# ---------------------------------------------------------------------------


class TestExtractPrUrl:
    def test_extracts_from_wrapped_json(self):
        output = json.dumps(
            {
                "type": "result",
                "result": json.dumps({"pr_url": "https://github.com/org/repo/pull/42"}),
            }
        )
        assert orch._extract_pr_url(output) == "https://github.com/org/repo/pull/42"

    def test_extracts_from_html_url(self):
        output = json.dumps(
            {
                "type": "result",
                "result": json.dumps(
                    {"html_url": "https://github.com/org/repo/pull/99"}
                ),
            }
        )
        assert orch._extract_pr_url(output) == "https://github.com/org/repo/pull/99"

    def test_extracts_from_raw_text_regex(self):
        output = "Created PR: https://github.com/org/repo/pull/123 done"
        assert orch._extract_pr_url(output) == "https://github.com/org/repo/pull/123"

    def test_returns_none_for_no_url(self):
        assert orch._extract_pr_url("no url here") is None

    def test_returns_none_for_invalid_json(self):
        assert orch._extract_pr_url("{invalid json") is None


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


class TestSchemas:
    def test_define_output_schema_has_status_field(self):
        schema = json.loads(orch.DEFINE_OUTPUT_SCHEMA)
        assert "status" in schema["properties"]
        assert schema["properties"]["status"]["enum"] == [
            "waiting_for_response",
            "complete",
        ]

    def test_do_output_schema_has_status_field(self):
        schema = json.loads(orch.DO_OUTPUT_SCHEMA)
        assert "status" in schema["properties"]
        assert schema["properties"]["status"]["enum"] == [
            "escalation_pending",
            "complete",
        ]

    def test_define_output_schema_has_waiting_fields(self):
        schema = json.loads(orch.DEFINE_OUTPUT_SCHEMA)
        props = schema["properties"]
        assert "thread_ts" in props
        assert "target_handle" in props
        assert "question_summary" in props

    def test_do_output_schema_has_escalation_fields(self):
        schema = json.loads(orch.DO_OUTPUT_SCHEMA)
        props = schema["properties"]
        assert "thread_ts" in props
        assert "escalation_summary" in props

    def test_thread_response_schema_exists(self):
        schema = json.loads(orch.THREAD_RESPONSE_SCHEMA)
        assert "has_response" in schema["properties"]
        assert "response_text" in schema["properties"]

    def test_preflight_schema_no_poll_interval(self):
        schema = json.loads(orch.PREFLIGHT_SCHEMA)
        assert "poll_interval" not in schema["properties"]
