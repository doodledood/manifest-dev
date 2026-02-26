"""Unit tests for the slack-collab orchestrator's deterministic logic.

Tests cover state management, phase transitions, error handling,
COLLAB_CONTEXT construction, session-resume patterns, and all phase
functions. No Slack or Claude CLI needed — all subprocess calls are mocked.
"""

import importlib.util
import json
import subprocess
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
                state["phase"] = name

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
        assert "done" in phases_called

    def test_qa_skipped_when_not_requested(self, sample_state, tmp_state_dir):
        """Verify QA phase is skipped when has_qa is False."""
        sample_state["phase"] = "pr"
        sample_state["has_qa"] = False
        phases_called = []

        def mock_phase(name):
            def fn(state):
                phases_called.append(name)
                state["phase"] = name

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


# ---------------------------------------------------------------------------
# Helper: mock invoke_claude to return a sequence of responses
# ---------------------------------------------------------------------------


def _make_invoke_mock(responses):
    """Return a side_effect function that yields from *responses* in order.

    Each item is a dict that invoke_claude would return.
    """
    it = iter(responses)

    def side_effect(prompt, **kwargs):
        return next(it)

    return side_effect


# ---------------------------------------------------------------------------
# Phase: preflight
# ---------------------------------------------------------------------------


class TestPhasePreflight:
    def test_success_updates_state(self, sample_state, tmp_state_dir):
        preflight_data = {
            "channel_id": "C99",
            "channel_name": "collab-test-20260226",
            "owner_handle": "@owner",
            "stakeholders": [
                {"handle": "@dev", "name": "Dev", "role": "backend"},
            ],
            "threads": {"stakeholders": {"@dev": "111.001"}},
            "slack_mcp_available": True,
        }
        with patch.object(orch, "invoke_claude", return_value=preflight_data):
            orch.phase_preflight(sample_state)

        assert sample_state["channel_id"] == "C99"
        assert sample_state["owner_handle"] == "@owner"
        assert sample_state["phase"] == "define"
        assert sample_state["stakeholders"] == preflight_data["stakeholders"]
        assert sample_state["threads"] == preflight_data["threads"]

    def test_slack_mcp_unavailable_exits(self, sample_state, tmp_state_dir):
        data = {
            "channel_id": "C99",
            "stakeholders": [{"handle": "@x", "name": "X", "role": "r"}],
            "threads": {"stakeholders": {}},
            "slack_mcp_available": False,
        }
        with (
            patch.object(orch, "invoke_claude", return_value=data),
            pytest.raises(SystemExit),
        ):
            orch.phase_preflight(sample_state)

    def test_missing_channel_id_exits(self, sample_state, tmp_state_dir):
        data = {
            "channel_id": "",
            "stakeholders": [{"handle": "@x", "name": "X", "role": "r"}],
            "threads": {"stakeholders": {}},
            "slack_mcp_available": True,
        }
        with (
            patch.object(orch, "invoke_claude", return_value=data),
            pytest.raises(SystemExit),
        ):
            orch.phase_preflight(sample_state)

    def test_missing_stakeholders_exits(self, sample_state, tmp_state_dir):
        data = {
            "channel_id": "C99",
            "stakeholders": [],
            "threads": {"stakeholders": {}},
            "slack_mcp_available": True,
        }
        with (
            patch.object(orch, "invoke_claude", return_value=data),
            pytest.raises(SystemExit),
        ):
            orch.phase_preflight(sample_state)

    def test_has_qa_true_when_qa_stakeholder(self, sample_state, tmp_state_dir):
        data = {
            "channel_id": "C99",
            "owner_handle": "@o",
            "stakeholders": [
                {"handle": "@dev", "name": "Dev", "role": "dev"},
                {"handle": "@qa", "name": "QA", "role": "qa", "is_qa": True},
            ],
            "threads": {"stakeholders": {}},
            "slack_mcp_available": True,
        }
        with patch.object(orch, "invoke_claude", return_value=data):
            orch.phase_preflight(sample_state)
        assert sample_state["has_qa"] is True

    def test_has_qa_false_when_no_qa_stakeholder(self, sample_state, tmp_state_dir):
        data = {
            "channel_id": "C99",
            "owner_handle": "@o",
            "stakeholders": [
                {"handle": "@dev", "name": "Dev", "role": "dev"},
            ],
            "threads": {"stakeholders": {}},
            "slack_mcp_available": True,
        }
        with patch.object(orch, "invoke_claude", return_value=data):
            orch.phase_preflight(sample_state)
        assert sample_state["has_qa"] is False


# ---------------------------------------------------------------------------
# Phase: define (session-resume loop)
# ---------------------------------------------------------------------------


class TestPhaseDefine:
    def test_complete_on_first_call(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")
        complete_resp = {
            "status": "complete",
            "manifest_path": str(manifest),
            "discovery_log_path": "/tmp/log.md",
        }
        with patch.object(orch, "invoke_claude", return_value=complete_resp):
            orch.phase_define(sample_state)

        assert sample_state["manifest_path"] == str(manifest)
        assert sample_state["phase"] == "manifest_review"
        assert sample_state["define_session_id"] is not None

    def test_session_resume_loop(self, sample_state, tmp_state_dir, tmp_path):
        """Simulate: first call → waiting_for_response → poll → resume → complete."""
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")

        responses = [
            {
                "status": "waiting_for_response",
                "thread_ts": "111.001",
                "target_handle": "@bob",
                "question_summary": "What framework?",
            },
            {
                "status": "complete",
                "manifest_path": str(manifest),
            },
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch, "poll_slack_thread", return_value="Use React"),
        ):
            orch.phase_define(sample_state)

        assert sample_state["phase"] == "manifest_review"
        assert sample_state["manifest_path"] == str(manifest)

    def test_multiple_resume_rounds(self, sample_state, tmp_state_dir, tmp_path):
        """Three rounds of questions before complete."""
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")

        responses = [
            {
                "status": "waiting_for_response",
                "thread_ts": "111.001",
                "target_handle": "@bob",
                "question_summary": "Q1?",
            },
            {
                "status": "waiting_for_response",
                "thread_ts": "111.002",
                "target_handle": "@alice",
                "question_summary": "Q2?",
            },
            {
                "status": "waiting_for_response",
                "thread_ts": "111.003",
                "target_handle": "@bob",
                "question_summary": "Q3?",
            },
            {"status": "complete", "manifest_path": str(manifest)},
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch, "poll_slack_thread", return_value="Answer"),
        ):
            orch.phase_define(sample_state)

        assert sample_state["phase"] == "manifest_review"

    def test_invalid_manifest_path_exits(self, sample_state, tmp_state_dir):
        complete_resp = {
            "status": "complete",
            "manifest_path": "/tmp/nonexistent-manifest-999.md",
        }
        with (
            patch.object(orch, "invoke_claude", return_value=complete_resp),
            pytest.raises(SystemExit),
        ):
            orch.phase_define(sample_state)

    def test_unexpected_status_exits(self, sample_state, tmp_state_dir):
        bad_resp = {"status": "unknown_status"}
        with (
            patch.object(orch, "invoke_claude", return_value=bad_resp),
            pytest.raises(SystemExit),
        ):
            orch.phase_define(sample_state)

    def test_session_id_generated_and_stored(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        resp = {"status": "complete", "manifest_path": str(manifest)}
        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_define(sample_state)
        assert sample_state["define_session_id"] is not None
        assert len(sample_state["define_session_id"]) == 32  # uuid hex

    def test_reuses_existing_session_id(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        sample_state["define_session_id"] = "existing_session"
        resp = {"status": "complete", "manifest_path": str(manifest)}
        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_define(sample_state)
        assert sample_state["define_session_id"] == "existing_session"

    def test_first_call_uses_session_id_not_resume(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        resp = {"status": "complete", "manifest_path": str(manifest)}
        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_define(sample_state)
        # First call should use session_id=, not resume_session_id=
        kwargs = mock_ic.call_args[1]
        assert kwargs.get("session_id") is not None
        assert kwargs.get("resume_session_id") is None

    def test_resume_call_uses_resume_flag(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        responses = [
            {
                "status": "waiting_for_response",
                "thread_ts": "111.001",
                "target_handle": "@bob",
                "question_summary": "Q?",
            },
            {"status": "complete", "manifest_path": str(manifest)},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ) as mock_ic,
            patch.object(orch, "poll_slack_thread", return_value="Answer"),
        ):
            orch.phase_define(sample_state)
        # Second call should use resume_session_id=, not session_id=
        second_call_kwargs = mock_ic.call_args_list[1][1]
        assert second_call_kwargs.get("resume_session_id") is not None
        assert second_call_kwargs.get("session_id") is None


# ---------------------------------------------------------------------------
# Phase: manifest_review
# ---------------------------------------------------------------------------


class TestPhaseManifestReview:
    def test_approval_on_first_poll(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest content")
        sample_state["manifest_path"] = str(manifest)

        # First call = post manifest, second call = check approval
        responses = [
            {},  # post_prompt response (ignored)
            {"approved": True},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_manifest_review(sample_state)

        assert sample_state["phase"] == "execute"

    def test_manifest_read_failure_exits(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/nonexistent-manifest-999.md"
        with pytest.raises(SystemExit):
            orch.phase_manifest_review(sample_state)

    def test_feedback_triggers_redefine(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest content")
        sample_state["manifest_path"] = str(manifest)

        # post manifest, first poll = feedback, then re-define + re-review
        responses = [
            {},  # post manifest
            {"approved": False, "feedback": "Add error handling section"},
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch.time, "sleep"),
            patch.object(orch, "phase_define"),
            # Recursive call to phase_manifest_review — mock it to avoid loop
            patch.object(orch, "phase_manifest_review"),
        ):
            # Call the real function but the recursive calls are mocked
            orch.phase_manifest_review.__wrapped__ = None  # prevent recursion
            # We need to call the actual function body, but it recurses.
            # Instead, test the state mutation and verify re-define was called.
            # Let's use a different approach: just verify the state changes.
            pass

        # Better approach: test state mutation directly
        sample_state["manifest_path"] = str(manifest)
        sample_state["phase"] = "manifest_review"
        call_count = {"n": 0}

        def fake_invoke(prompt, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return {}  # post manifest
            if call_count["n"] == 2:
                return {"approved": False, "feedback": "Fix X"}
            return {}

        define_called = {"called": False}

        def fake_define(state):
            define_called["called"] = True
            state["phase"] = "manifest_review"

        review_recursion = {"count": 0}
        real_review = orch.phase_manifest_review

        def fake_review(state):
            review_recursion["count"] += 1
            if review_recursion["count"] > 1:
                # Second call = simulate approval
                state["phase"] = "execute"
                return
            return real_review(state)

        with (
            patch.object(orch, "invoke_claude", side_effect=fake_invoke),
            patch.object(orch.time, "sleep"),
            patch.object(orch, "phase_define", side_effect=fake_define),
            patch.object(orch, "phase_manifest_review", side_effect=fake_review),
        ):
            fake_review(sample_state)

        assert define_called["called"]
        assert "Fix X" in sample_state["task"]

    def test_no_response_keeps_polling(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")
        sample_state["manifest_path"] = str(manifest)

        responses = [
            {},  # post manifest
            {"approved": False, "feedback": None},  # no response
            {"approved": False, "feedback": None},  # no response
            {"approved": True},  # approved
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_manifest_review(sample_state)

        assert sample_state["phase"] == "execute"


# ---------------------------------------------------------------------------
# Phase: execute (session-resume loop)
# ---------------------------------------------------------------------------


class TestPhaseExecute:
    def test_complete_on_first_call(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        resp = {"status": "complete", "do_log_path": "/tmp/do-log.md"}
        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_execute(sample_state)

        assert sample_state["phase"] == "pr"
        assert sample_state["do_log_path"] == "/tmp/do-log.md"

    def test_escalation_resume_loop(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        responses = [
            {
                "status": "escalation_pending",
                "thread_ts": "111.001",
                "escalation_summary": "Can't meet AC-2.3",
            },
            {"status": "complete", "do_log_path": "/tmp/log.md"},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch, "poll_slack_thread", return_value="Skip AC-2.3"),
        ):
            orch.phase_execute(sample_state)

        assert sample_state["phase"] == "pr"

    def test_multiple_escalation_rounds(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        responses = [
            {
                "status": "escalation_pending",
                "thread_ts": "111.001",
                "escalation_summary": "Blocked on API",
            },
            {
                "status": "escalation_pending",
                "thread_ts": "111.002",
                "escalation_summary": "Need DB access",
            },
            {"status": "complete", "do_log_path": "/tmp/log.md"},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch, "poll_slack_thread", return_value="Granted"),
        ):
            orch.phase_execute(sample_state)

        assert sample_state["phase"] == "pr"

    def test_unexpected_status_exits(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        resp = {"status": "garbage"}
        with (
            patch.object(orch, "invoke_claude", return_value=resp),
            pytest.raises(SystemExit),
        ):
            orch.phase_execute(sample_state)

    def test_session_id_generated_and_stored(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        resp = {"status": "complete", "do_log_path": "/tmp/log.md"}
        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_execute(sample_state)
        assert sample_state["execute_session_id"] is not None
        assert len(sample_state["execute_session_id"]) == 32

    def test_first_call_uses_session_id(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        resp = {"status": "complete", "do_log_path": "/tmp/log.md"}
        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_execute(sample_state)
        kwargs = mock_ic.call_args[1]
        assert kwargs.get("session_id") is not None
        assert kwargs.get("resume_session_id") is None

    def test_resume_call_uses_resume_flag(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        responses = [
            {
                "status": "escalation_pending",
                "thread_ts": "111.001",
                "escalation_summary": "Blocked",
            },
            {"status": "complete", "do_log_path": "/tmp/log.md"},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ) as mock_ic,
            patch.object(orch, "poll_slack_thread", return_value="OK"),
        ):
            orch.phase_execute(sample_state)
        second_kwargs = mock_ic.call_args_list[1][1]
        assert second_kwargs.get("resume_session_id") is not None
        assert second_kwargs.get("session_id") is None


# ---------------------------------------------------------------------------
# Phase: PR
# ---------------------------------------------------------------------------


class TestPhasePr:
    def test_pr_creation_and_approval(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        sample_state["phase"] = "pr"

        pr_output = json.dumps(
            {
                "type": "result",
                "result": json.dumps({"pr_url": "https://github.com/org/repo/pull/42"}),
            }
        )
        mock_subprocess = MagicMock(returncode=0, stdout=pr_output, stderr="")

        invoke_responses = [
            {},  # post PR to Slack
            {"approved": True},  # PR approved
        ]

        with (
            patch.object(
                orch.subprocess,
                "run",
                return_value=mock_subprocess,
            ),
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["pr_url"] == "https://github.com/org/repo/pull/42"
        # has_qa=True in sample_state, so next phase = qa
        assert sample_state["phase"] == "qa"

    def test_pr_approval_skips_qa_when_no_qa(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        sample_state["has_qa"] = False

        pr_output = json.dumps({"type": "result", "result": "{}"})
        mock_subprocess = MagicMock(returncode=0, stdout=pr_output, stderr="")

        invoke_responses = [
            {},  # post PR
            {"approved": True},
        ]

        with (
            patch.object(orch.subprocess, "run", return_value=mock_subprocess),
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["phase"] == "done"

    def test_pr_feedback_triggers_fix(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"

        pr_output = json.dumps({"type": "result", "result": "{}"})
        mock_subprocess = MagicMock(returncode=0, stdout=pr_output, stderr="")

        invoke_responses = [
            {},  # post PR
            {"approved": False, "feedback": "Fix typo in README"},  # review comment
            {},  # fix applied
            {"approved": True},  # approved after fix
        ]

        with (
            patch.object(orch.subprocess, "run", return_value=mock_subprocess),
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["phase"] == "qa"

    def test_pr_escalates_after_max_attempts(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"

        pr_output = json.dumps({"type": "result", "result": "{}"})
        mock_subprocess = MagicMock(returncode=0, stdout=pr_output, stderr="")

        invoke_responses = [
            {},  # post PR
            {"approved": False, "feedback": "Fix A"},  # attempt 1
            {},  # fix 1
            {"approved": False, "feedback": "Fix B"},  # attempt 2
            {},  # fix 2
            {"approved": False, "feedback": "Fix C"},  # attempt 3
            {},  # fix 3
            {"approved": False, "feedback": "Still broken"},  # attempt 4 > max
            {},  # escalation posted to Slack
            {"approved": True},  # finally approved after owner helps
        ]

        with (
            patch.object(orch.subprocess, "run", return_value=mock_subprocess),
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["phase"] == "qa"

    def test_pr_creation_failure_exits(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        mock_subprocess = MagicMock(returncode=1, stdout="", stderr="error")

        with (
            patch.object(orch.subprocess, "run", return_value=mock_subprocess),
            pytest.raises(SystemExit),
        ):
            orch.phase_pr(sample_state)

    def test_pr_creation_timeout_exits(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"

        with (
            patch.object(
                orch.subprocess,
                "run",
                side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=1800),
            ),
            pytest.raises(SystemExit),
        ):
            orch.phase_pr(sample_state)


# ---------------------------------------------------------------------------
# Phase: QA
# ---------------------------------------------------------------------------


class TestPhaseQa:
    def test_no_qa_stakeholders_skips(self, sample_state, tmp_state_dir):
        sample_state["stakeholders"] = [
            {"handle": "@dev", "name": "Dev", "role": "dev"},
        ]
        orch.phase_qa(sample_state)
        assert sample_state["phase"] == "done"

    def test_qa_approval(self, sample_state, tmp_state_dir):
        sample_state["pr_url"] = "https://github.com/org/repo/pull/1"
        invoke_responses = [
            {},  # post QA request
            {"approved": True},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_qa(sample_state)
        assert sample_state["phase"] == "done"

    def test_qa_feedback_triggers_fix(self, sample_state, tmp_state_dir):
        sample_state["pr_url"] = "https://github.com/org/repo/pull/1"
        invoke_responses = [
            {},  # post QA request
            {"approved": False, "feedback": "Button doesn't work"},
            {},  # fix applied
            {"approved": True},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_qa(sample_state)
        assert sample_state["phase"] == "done"

    def test_qa_escalates_after_max_attempts(self, sample_state, tmp_state_dir):
        sample_state["pr_url"] = "https://github.com/org/repo/pull/1"
        invoke_responses = [
            {},  # post QA request
            {"approved": False, "feedback": "Bug 1"},
            {},  # fix 1
            {"approved": False, "feedback": "Bug 2"},
            {},  # fix 2
            {"approved": False, "feedback": "Bug 3"},
            {},  # fix 3
            {"approved": False, "feedback": "Still broken"},  # > max
            {},  # escalation
            {"approved": True},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_qa(sample_state)
        assert sample_state["phase"] == "done"

    def test_qa_no_response_keeps_polling(self, sample_state, tmp_state_dir):
        sample_state["pr_url"] = "https://github.com/org/repo/pull/1"
        invoke_responses = [
            {},  # post QA request
            {"approved": False, "feedback": None},  # no response
            {"approved": False, "feedback": None},  # no response
            {"approved": True},
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_qa(sample_state)
        assert sample_state["phase"] == "done"


# ---------------------------------------------------------------------------
# Phase: done
# ---------------------------------------------------------------------------


class TestPhaseDone:
    def test_posts_completion_and_sets_done(self, sample_state, tmp_state_dir):
        sample_state["pr_url"] = "https://github.com/org/repo/pull/42"
        with patch.object(orch, "invoke_claude", return_value={}):
            orch.phase_done(sample_state)
        assert sample_state["phase"] == "done"

    def test_done_with_no_pr_url(self, sample_state, tmp_state_dir):
        sample_state["pr_url"] = None
        with patch.object(orch, "invoke_claude", return_value={}) as mock_ic:
            orch.phase_done(sample_state)
        # Should still complete without error
        assert sample_state["phase"] == "done"
        assert mock_ic.called


# ---------------------------------------------------------------------------
# poll_slack_thread
# ---------------------------------------------------------------------------


class TestPollSlackThread:
    def test_returns_response_immediately(self):
        resp = {
            "has_response": True,
            "response_text": "Use PostgreSQL",
            "responder_handle": "@bob",
        }
        with (
            patch.object(orch, "invoke_claude", return_value=resp),
            patch.object(orch.time, "sleep"),
        ):
            result = orch.poll_slack_thread("C1", "111.001", "@bob", "@alice")
        assert result == "Use PostgreSQL"

    def test_polls_until_response(self):
        responses = [
            {"has_response": False},
            {"has_response": False},
            {
                "has_response": True,
                "response_text": "Yes",
                "responder_handle": "@bob",
            },
        ]
        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch.time, "sleep") as mock_sleep,
        ):
            result = orch.poll_slack_thread("C1", "111.001", "@bob", "@alice")

        assert result == "Yes"
        assert mock_sleep.call_count == 3  # sleep before each poll

    def test_owner_can_respond_for_target(self):
        resp = {
            "has_response": True,
            "response_text": "I'll answer for Bob: use Redis",
            "responder_handle": "@alice",
        }
        with (
            patch.object(orch, "invoke_claude", return_value=resp),
            patch.object(orch.time, "sleep"),
        ):
            result = orch.poll_slack_thread("C1", "111.001", "@bob", "@alice")
        assert "Redis" in result

    def test_empty_response_text_still_returns(self):
        resp = {"has_response": True, "response_text": "", "responder_handle": "@bob"}
        with (
            patch.object(orch, "invoke_claude", return_value=resp),
            patch.object(orch.time, "sleep"),
        ):
            result = orch.poll_slack_thread("C1", "111.001", "@bob", "@alice")
        assert result == ""


# ---------------------------------------------------------------------------
# run() exception handling
# ---------------------------------------------------------------------------


class TestRunExceptionHandling:
    def test_system_exit_saves_state(self, sample_state, tmp_state_dir):
        sample_state["phase"] = "execute"

        def failing_phase(state):
            raise SystemExit(1)

        with (
            patch.dict(orch.PHASE_FUNCTIONS, {"execute": failing_phase}),
            pytest.raises(SystemExit),
        ):
            orch.run(sample_state)

        # Verify state was saved
        state_file = tmp_state_dir / f"collab-state-{sample_state['run_id']}.json"
        assert state_file.exists()

    def test_generic_exception_saves_state(self, sample_state, tmp_state_dir):
        sample_state["phase"] = "execute"

        def failing_phase(state):
            raise RuntimeError("something broke")

        with (
            patch.dict(orch.PHASE_FUNCTIONS, {"execute": failing_phase}),
            pytest.raises(RuntimeError),
        ):
            orch.run(sample_state)

        state_file = tmp_state_dir / f"collab-state-{sample_state['run_id']}.json"
        assert state_file.exists()

    def test_full_flow_executes_all_phases(self, sample_state, tmp_state_dir):
        sample_state["phase"] = "preflight"
        phases_called = []

        def mock_phase(name):
            def fn(state):
                phases_called.append(name)
                # Real phase functions set state["phase"] to their OWN name;
                # run() drives ordering via the PHASES list.
                state["phase"] = name

            return fn

        with patch.dict(
            orch.PHASE_FUNCTIONS,
            {p: mock_phase(p) for p in orch.PHASES},
        ):
            orch.run(sample_state)

        assert phases_called == [
            "preflight",
            "define",
            "manifest_review",
            "execute",
            "pr",
            # qa is included because has_qa=True
            "qa",
            "done",
        ]


# ---------------------------------------------------------------------------
# main() entry point
# ---------------------------------------------------------------------------


class TestMain:
    def test_new_task_creates_state_and_runs(self, tmp_state_dir):
        with (
            patch("slack_collab_orchestrator.argparse.ArgumentParser") as mock_parser,
            patch.object(orch, "run") as mock_run,
        ):
            args = MagicMock()
            args.resume = None
            args.task = "Build login page"
            mock_parser.return_value.parse_args.return_value = args

            orch.main()

            assert mock_run.called
            state = mock_run.call_args[0][0]
            assert state["task"] == "Build login page"
            assert state["phase"] == "preflight"

    def test_resume_loads_state_and_runs(self, tmp_state_dir, tmp_path):
        state_file = tmp_path / "collab-state-abc123.json"
        state_data = {
            "run_id": "abc123",
            "task": "Test task",
            "phase": "execute",
        }
        state_file.write_text(json.dumps(state_data))

        with (
            patch("slack_collab_orchestrator.argparse.ArgumentParser") as mock_parser,
            patch.object(orch, "run") as mock_run,
        ):
            args = MagicMock()
            args.resume = str(state_file)
            args.task = None
            mock_parser.return_value.parse_args.return_value = args

            orch.main()

            assert mock_run.called
            state = mock_run.call_args[0][0]
            assert state["run_id"] == "abc123"
            assert state["phase"] == "execute"

    def test_resume_nonexistent_file_exits(self, tmp_state_dir):
        with (
            patch("slack_collab_orchestrator.argparse.ArgumentParser") as mock_parser,
            pytest.raises(SystemExit),
        ):
            args = MagicMock()
            args.resume = "/tmp/nonexistent-state-999.json"
            args.task = None
            mock_parser.return_value.parse_args.return_value = args

            orch.main()

    def test_no_args_prints_help_and_exits(self, tmp_state_dir):
        with (
            patch("slack_collab_orchestrator.argparse.ArgumentParser") as mock_parser,
            pytest.raises(SystemExit),
        ):
            args = MagicMock()
            args.resume = None
            args.task = None
            mock_parser.return_value.parse_args.return_value = args

            orch.main()

    def test_resume_sets_up_logging_before_load(self, tmp_state_dir, tmp_path):
        """Verify logging is configured before load_state on resume path."""
        state_file = tmp_path / "collab-state-test123.json"
        state_data = {
            "run_id": "test123",
            "task": "Task",
            "phase": "define",
        }
        state_file.write_text(json.dumps(state_data))

        call_order = []

        original_load = orch.load_state

        def tracking_setup(log_path):
            call_order.append("setup_logging")
            # Don't actually set up logging in tests
            return None

        def tracking_load(path):
            call_order.append("load_state")
            return original_load(path)

        with (
            patch("slack_collab_orchestrator.argparse.ArgumentParser") as mock_parser,
            patch.object(orch, "setup_logging", side_effect=tracking_setup),
            patch.object(orch, "load_state", side_effect=tracking_load),
            patch.object(orch, "run"),
        ):
            args = MagicMock()
            args.resume = str(state_file)
            args.task = None
            mock_parser.return_value.parse_args.return_value = args

            orch.main()

        assert call_order == ["setup_logging", "load_state"]

    def test_run_system_exit_logged_and_exits(self, tmp_state_dir):
        with (
            patch("slack_collab_orchestrator.argparse.ArgumentParser") as mock_parser,
            patch.object(orch, "run", side_effect=SystemExit(1)),
            pytest.raises(SystemExit) as exc_info,
        ):
            args = MagicMock()
            args.resume = None
            args.task = "test"
            mock_parser.return_value.parse_args.return_value = args

            orch.main()

        assert exc_info.value.code == 1

    def test_run_unexpected_exception_exits(self, tmp_state_dir):
        with (
            patch("slack_collab_orchestrator.argparse.ArgumentParser") as mock_parser,
            patch.object(orch, "run", side_effect=RuntimeError("boom")),
            pytest.raises(SystemExit) as exc_info,
        ):
            args = MagicMock()
            args.resume = None
            args.task = "test"
            mock_parser.return_value.parse_args.return_value = args

            orch.main()

        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# Security: SECURITY_INSTRUCTIONS presence
# ---------------------------------------------------------------------------


class TestSecurityInstructions:
    def test_security_appended_to_preflight_prompt(self, sample_state, tmp_state_dir):
        with patch.object(
            orch,
            "invoke_claude",
            return_value={
                "channel_id": "C1",
                "owner_handle": "@o",
                "stakeholders": [{"handle": "@x", "name": "X", "role": "r"}],
                "threads": {"stakeholders": {}},
                "slack_mcp_available": True,
            },
        ) as mock_ic:
            orch.phase_preflight(sample_state)
        prompt = mock_ic.call_args[0][0]
        assert "SECURITY" in prompt
        assert "untrusted" in prompt.lower() or "NEVER expose" in prompt

    def test_security_appended_to_poll_prompt(self):
        resp = {"has_response": True, "response_text": "yes", "responder_handle": "@x"}
        with (
            patch.object(orch, "invoke_claude", return_value=resp) as mock_ic,
            patch.object(orch.time, "sleep"),
        ):
            orch.poll_slack_thread("C1", "111.001", "@x", "@owner")
        prompt = mock_ic.call_args[0][0]
        assert "SECURITY" in prompt

    def test_security_in_manifest_review_prompts(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        sample_state["manifest_path"] = str(manifest)

        prompts_seen = []

        def capture_invoke(prompt, **kwargs):
            prompts_seen.append(prompt)
            if len(prompts_seen) == 1:
                return {}  # post
            return {"approved": True}

        with (
            patch.object(orch, "invoke_claude", side_effect=capture_invoke),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_manifest_review(sample_state)

        # Both post and poll prompts should include SECURITY
        for p in prompts_seen:
            assert "SECURITY" in p
