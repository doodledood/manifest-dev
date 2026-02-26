"""Unit tests for the slack-collab orchestrator's deterministic logic (V2 Agent Teams).

Tests cover state management, phase transitions, error handling,
COLLAB_CONTEXT construction, Agent Teams environment setup, file validation,
and all phase functions. No Slack or Claude CLI needed — all subprocess calls
are mocked.
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
    """A fully populated state dict for testing (V2 — no session IDs)."""
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

    def test_no_session_ids_in_state(self):
        """V2: Agent Teams teammates manage their own lifecycle — no session IDs."""
        state = orch.new_state("task", "run1")
        assert "define_session_id" not in state
        assert "execute_session_id" not in state

    def test_has_qa_defaults_false(self):
        state = orch.new_state("task", "run1")
        assert state["has_qa"] is False

    def test_threads_initialized_empty(self):
        state = orch.new_state("task", "run1")
        assert state["threads"] == {"stakeholders": {}}


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


# ---------------------------------------------------------------------------
# Phase transition tests
# ---------------------------------------------------------------------------


class TestPhaseTransitions:
    def test_phases_index_preflight(self):
        assert orch.PHASES.index("preflight") == 0

    def test_phases_index_define(self):
        assert orch.PHASES.index("define") == 1

    def test_phases_index_manifest_review(self):
        assert orch.PHASES.index("manifest_review") == 2

    def test_phases_index_execute(self):
        assert orch.PHASES.index("execute") == 3

    def test_phases_index_pr(self):
        assert orch.PHASES.index("pr") == 4

    def test_phases_index_qa(self):
        assert orch.PHASES.index("qa") == 5

    def test_phases_index_done(self):
        assert orch.PHASES.index("done") == 6

    def test_phases_index_unknown_raises(self):
        with pytest.raises(ValueError):
            orch.PHASES.index("unknown")

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
    def test_extra_env_passed_to_subprocess(self, mock_run):
        """V2: extra_env merges with os.environ for subprocess call."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": "{}"}),
            stderr="",
        )
        orch.invoke_claude("test", extra_env={"MY_VAR": "1"})
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs["env"] is not None
        assert call_kwargs["env"]["MY_VAR"] == "1"

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_no_extra_env_passes_none(self, mock_run):
        """Without extra_env, env=None (inherit from parent process)."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": "{}"}),
            stderr="",
        )
        orch.invoke_claude("test")
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs["env"] is None

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_json_schema_included_in_command(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": "{}"}),
            stderr="",
        )
        orch.invoke_claude("test", json_schema='{"type":"object"}')
        cmd = mock_run.call_args[0][0]
        assert "--json-schema" in cmd

    @patch("slack_collab_orchestrator.subprocess.run")
    def test_no_json_schema_by_default(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({"type": "result", "result": "{}"}),
            stderr="",
        )
        orch.invoke_claude("test")
        cmd = mock_run.call_args[0][0]
        assert "--json-schema" not in cmd


# ---------------------------------------------------------------------------
# File validation tests
# ---------------------------------------------------------------------------


class TestValidateOutputFile:
    def test_empty_path_returns_false(self):
        assert orch._validate_output_file("") is False

    def test_none_path_returns_false(self):
        # Path("") would fail, but the function checks `if not path` first
        assert orch._validate_output_file("") is False

    def test_nonexistent_file_returns_false(self):
        assert orch._validate_output_file("/tmp/nonexistent-file-99999.md") is False

    def test_empty_file_returns_false(self, tmp_path):
        empty = tmp_path / "empty.md"
        empty.write_text("")
        assert orch._validate_output_file(str(empty)) is False

    def test_valid_file_returns_true(self, tmp_path):
        valid = tmp_path / "manifest.md"
        valid.write_text("# Manifest\nContent here")
        assert orch._validate_output_file(str(valid)) is True

    def test_single_byte_file_returns_true(self, tmp_path):
        minimal = tmp_path / "minimal.md"
        minimal.write_text("x")
        assert orch._validate_output_file(str(minimal)) is True


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
# Schema tests (V2 — simplified, no union types)
# ---------------------------------------------------------------------------


class TestSchemas:
    def test_define_output_schema_is_simple(self):
        """V2: Define schema has manifest_path and discovery_log_path only."""
        schema = json.loads(orch.DEFINE_OUTPUT_SCHEMA)
        props = schema["properties"]
        assert "manifest_path" in props
        assert "discovery_log_path" in props
        # No V1 fields
        assert "status" not in props
        assert "thread_ts" not in props
        assert "target_handle" not in props
        assert "question_summary" not in props

    def test_define_output_schema_required_fields(self):
        schema = json.loads(orch.DEFINE_OUTPUT_SCHEMA)
        assert schema["required"] == ["manifest_path"]

    def test_do_output_schema_is_simple(self):
        """V2: Do schema has do_log_path only."""
        schema = json.loads(orch.DO_OUTPUT_SCHEMA)
        props = schema["properties"]
        assert "do_log_path" in props
        # No V1 fields
        assert "status" not in props
        assert "thread_ts" not in props
        assert "escalation_summary" not in props

    def test_do_output_schema_required_fields(self):
        schema = json.loads(orch.DO_OUTPUT_SCHEMA)
        assert schema["required"] == ["do_log_path"]

    def test_no_thread_response_schema(self):
        """V2: THREAD_RESPONSE_SCHEMA should not exist (no poll_slack_thread)."""
        assert not hasattr(orch, "THREAD_RESPONSE_SCHEMA")

    def test_preflight_schema_no_poll_interval(self):
        schema = json.loads(orch.PREFLIGHT_SCHEMA)
        assert "poll_interval" not in schema["properties"]

    def test_poll_schema_exists(self):
        schema = json.loads(orch.POLL_SCHEMA)
        assert "approved" in schema["properties"]
        assert "feedback" in schema["properties"]


# ---------------------------------------------------------------------------
# Agent Teams environment setup tests
# ---------------------------------------------------------------------------


class TestAgentTeamsEnv:
    def test_agent_teams_env_var_constant(self):
        assert orch.AGENT_TEAMS_ENV_VAR == "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"

    def test_define_phase_passes_agent_teams_env(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """Verify define phase sets Agent Teams env var."""
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")
        resp = {"manifest_path": str(manifest)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_define(sample_state)

        kwargs = mock_ic.call_args[1]
        assert kwargs["extra_env"] == {orch.AGENT_TEAMS_ENV_VAR: "1"}

    def test_execute_phase_passes_agent_teams_env(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """Verify execute phase sets Agent Teams env var."""
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "do-log.md"
        log_file.write_text("# Log")
        resp = {"do_log_path": str(log_file)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_execute(sample_state)

        kwargs = mock_ic.call_args[1]
        assert kwargs["extra_env"] == {orch.AGENT_TEAMS_ENV_VAR: "1"}

    def test_preflight_does_not_set_agent_teams_env(
        self, sample_state, tmp_state_dir
    ):
        """Preflight uses standard invoke_claude without Agent Teams."""
        preflight_data = {
            "channel_id": "C99",
            "channel_name": "collab-test",
            "owner_handle": "@owner",
            "stakeholders": [{"handle": "@dev", "name": "Dev", "role": "dev"}],
            "threads": {"stakeholders": {"@dev": "111.001"}},
            "slack_mcp_available": True,
        }
        with patch.object(orch, "invoke_claude", return_value=preflight_data) as mock_ic:
            orch.phase_preflight(sample_state)

        kwargs = mock_ic.call_args[1]
        assert "extra_env" not in kwargs or kwargs.get("extra_env") is None


# ---------------------------------------------------------------------------
# Helper: mock invoke_claude to return a sequence of responses
# ---------------------------------------------------------------------------


def _make_invoke_mock(responses):
    """Return a side_effect function that yields from *responses* in order."""
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
# Phase: define (V2 — Agent Teams, single call + file validation)
# ---------------------------------------------------------------------------


class TestPhaseDefine:
    def test_complete_on_first_call(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")
        resp = {
            "manifest_path": str(manifest),
            "discovery_log_path": "/tmp/log.md",
        }
        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_define(sample_state)

        assert sample_state["manifest_path"] == str(manifest)
        assert sample_state["phase"] == "manifest_review"
        assert sample_state["discovery_log_path"] == "/tmp/log.md"

    def test_retries_once_on_missing_manifest(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """If first call returns nonexistent file, retries once."""
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")

        call_count = {"n": 0}

        def fake_invoke(prompt, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return {"manifest_path": "/tmp/nonexistent-999.md"}
            return {"manifest_path": str(manifest)}

        with patch.object(orch, "invoke_claude", side_effect=fake_invoke):
            orch.phase_define(sample_state)

        assert call_count["n"] == 2
        assert sample_state["manifest_path"] == str(manifest)

    def test_retries_once_on_empty_manifest(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """If first call returns empty file, retries once."""
        empty_manifest = tmp_path / "empty.md"
        empty_manifest.write_text("")
        good_manifest = tmp_path / "good.md"
        good_manifest.write_text("# Manifest")

        call_count = {"n": 0}

        def fake_invoke(prompt, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return {"manifest_path": str(empty_manifest)}
            return {"manifest_path": str(good_manifest)}

        with patch.object(orch, "invoke_claude", side_effect=fake_invoke):
            orch.phase_define(sample_state)

        assert call_count["n"] == 2
        assert sample_state["manifest_path"] == str(good_manifest)

    def test_exits_after_retry_failure(self, sample_state, tmp_state_dir):
        """If both calls return invalid files, exits."""
        resp = {"manifest_path": "/tmp/nonexistent-999.md"}
        with (
            patch.object(orch, "invoke_claude", return_value=resp),
            pytest.raises(SystemExit),
        ):
            orch.phase_define(sample_state)

    def test_uses_agent_teams_timeout(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        resp = {"manifest_path": str(manifest)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_define(sample_state)

        kwargs = mock_ic.call_args[1]
        assert kwargs["timeout"] == orch.TIMEOUT_DEFINE

    def test_uses_define_output_schema(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        resp = {"manifest_path": str(manifest)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_define(sample_state)

        kwargs = mock_ic.call_args[1]
        assert kwargs["json_schema"] == orch.DEFINE_OUTPUT_SCHEMA

    def test_lead_prompt_contains_task_and_collab_context(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        resp = {"manifest_path": str(manifest)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_define(sample_state)

        prompt = mock_ic.call_args[0][0]
        assert sample_state["task"] in prompt
        assert "COLLAB_CONTEXT:" in prompt
        assert "teammate" in prompt.lower()
        assert "/define" in prompt

    def test_no_session_id_in_state_after_define(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """V2: No session IDs stored — Agent Teams handles lifecycle."""
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        resp = {"manifest_path": str(manifest)}
        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_define(sample_state)
        assert "define_session_id" not in sample_state


# ---------------------------------------------------------------------------
# Phase: manifest_review
# ---------------------------------------------------------------------------


class TestPhaseManifestReview:
    def test_approval_on_first_poll(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest content")
        sample_state["manifest_path"] = str(manifest)

        responses = [
            {},  # post manifest
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
        """Feedback sets state['phase'] to 'define' and returns (no recursion)."""
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest content")
        sample_state["manifest_path"] = str(manifest)
        sample_state["phase"] = "manifest_review"

        responses = [
            {},  # post manifest
            {"approved": False, "feedback": "Fix X"},
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_manifest_review(sample_state)

        assert sample_state["phase"] == "define"
        assert "Fix X" in sample_state["task"]
        # Verify original_task is preserved for bounded growth
        assert "original_task" in sample_state

    def test_no_response_keeps_polling(self, sample_state, tmp_state_dir, tmp_path):
        manifest = tmp_path / "manifest.md"
        manifest.write_text("# Manifest")
        sample_state["manifest_path"] = str(manifest)

        responses = [
            {},  # post manifest
            {"approved": False, "feedback": None},
            {"approved": False, "feedback": None},
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


# ---------------------------------------------------------------------------
# Phase: execute (V2 — Agent Teams, single call + file validation)
# ---------------------------------------------------------------------------


class TestPhaseExecute:
    def test_complete_on_first_call(self, sample_state, tmp_state_dir, tmp_path):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "do-log.md"
        log_file.write_text("# Execution log")
        resp = {"do_log_path": str(log_file)}

        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_execute(sample_state)

        assert sample_state["phase"] == "pr"
        assert sample_state["do_log_path"] == str(log_file)

    def test_retries_once_on_missing_log_file(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "do-log.md"
        log_file.write_text("# Log")

        call_count = {"n": 0}

        def fake_invoke(prompt, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return {"do_log_path": "/tmp/nonexistent-log-999.md"}
            return {"do_log_path": str(log_file)}

        with patch.object(orch, "invoke_claude", side_effect=fake_invoke):
            orch.phase_execute(sample_state)

        assert call_count["n"] == 2
        assert sample_state["do_log_path"] == str(log_file)

    def test_exits_after_retry_failure(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        resp = {"do_log_path": "/tmp/nonexistent-log-999.md"}

        with (
            patch.object(orch, "invoke_claude", return_value=resp),
            pytest.raises(SystemExit),
        ):
            orch.phase_execute(sample_state)

    def test_empty_log_path_triggers_retry(self, sample_state, tmp_state_dir, tmp_path):
        """Empty do_log_path triggers retry; exits if retry also fails."""
        sample_state["manifest_path"] = "/tmp/manifest.md"
        resp = {"do_log_path": ""}

        with (
            patch.object(orch, "invoke_claude", return_value=resp),
            pytest.raises(SystemExit),
        ):
            orch.phase_execute(sample_state)

    def test_uses_agent_teams_timeout(self, sample_state, tmp_state_dir, tmp_path):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "log.md"
        log_file.write_text("x")
        resp = {"do_log_path": str(log_file)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_execute(sample_state)

        kwargs = mock_ic.call_args[1]
        assert kwargs["timeout"] == orch.TIMEOUT_EXECUTE

    def test_uses_do_output_schema(self, sample_state, tmp_state_dir, tmp_path):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "log.md"
        log_file.write_text("x")
        resp = {"do_log_path": str(log_file)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_execute(sample_state)

        kwargs = mock_ic.call_args[1]
        assert kwargs["json_schema"] == orch.DO_OUTPUT_SCHEMA

    def test_lead_prompt_contains_manifest_and_collab_context(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "log.md"
        log_file.write_text("x")
        resp = {"do_log_path": str(log_file)}

        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_execute(sample_state)

        prompt = mock_ic.call_args[0][0]
        assert "/tmp/manifest.md" in prompt
        assert "COLLAB_CONTEXT:" in prompt
        assert "teammate" in prompt.lower()
        assert "/do" in prompt

    def test_no_session_id_in_state_after_execute(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """V2: No session IDs stored."""
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "log.md"
        log_file.write_text("x")
        resp = {"do_log_path": str(log_file)}
        with patch.object(orch, "invoke_claude", return_value=resp):
            orch.phase_execute(sample_state)
        assert "execute_session_id" not in sample_state


# ---------------------------------------------------------------------------
# Phase: PR
# ---------------------------------------------------------------------------


class TestPhasePr:
    def test_pr_creation_and_approval(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        sample_state["phase"] = "pr"

        invoke_responses = [
            {"pr_url": "https://github.com/org/repo/pull/42"},  # create PR
            {},  # post PR to Slack
            {"approved": True},
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["pr_url"] == "https://github.com/org/repo/pull/42"
        assert sample_state["phase"] == "qa"

    def test_pr_approval_skips_qa_when_no_qa(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"
        sample_state["has_qa"] = False

        invoke_responses = [
            {},  # create PR
            {},  # post PR
            {"approved": True},
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["phase"] == "done"

    def test_pr_feedback_triggers_fix(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"

        invoke_responses = [
            {},  # create PR
            {},  # post PR
            {"approved": False, "feedback": "Fix typo in README"},
            {},  # fix applied
            {"approved": True},
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["phase"] == "qa"

    def test_pr_escalates_after_max_attempts(self, sample_state, tmp_state_dir):
        sample_state["manifest_path"] = "/tmp/manifest.md"

        invoke_responses = [
            {},  # create PR
            {},  # post PR
            {"approved": False, "feedback": "Fix A"},
            {},  # fix 1
            {"approved": False, "feedback": "Fix B"},
            {},  # fix 2
            {"approved": False, "feedback": "Fix C"},
            {},  # fix 3
            {"approved": False, "feedback": "Still broken"},  # > max
            {},  # escalation posted
            {"approved": True},
        ]

        with (
            patch.object(
                orch, "invoke_claude", side_effect=_make_invoke_mock(invoke_responses)
            ),
            patch.object(orch.time, "sleep"),
        ):
            orch.phase_pr(sample_state)

        assert sample_state["phase"] == "qa"

    def test_pr_creation_failure_exits(self, sample_state, tmp_state_dir):
        """invoke_claude raises SystemExit on CLI failure."""
        sample_state["manifest_path"] = "/tmp/manifest.md"

        with (
            patch.object(orch, "invoke_claude", side_effect=SystemExit(1)),
            pytest.raises(SystemExit),
        ):
            orch.phase_pr(sample_state)

    def test_pr_creation_timeout_exits(self, sample_state, tmp_state_dir):
        """invoke_claude raises SystemExit on timeout."""
        sample_state["manifest_path"] = "/tmp/manifest.md"

        with (
            patch.object(orch, "invoke_claude", side_effect=SystemExit(1)),
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
            {"approved": False, "feedback": None},
            {"approved": False, "feedback": None},
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
        assert sample_state["phase"] == "done"
        assert mock_ic.called


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

    def test_security_in_define_lead_prompt(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """V2: Security instructions in the lead session prompt for define."""
        manifest = tmp_path / "m.md"
        manifest.write_text("x")
        resp = {"manifest_path": str(manifest)}
        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_define(sample_state)
        prompt = mock_ic.call_args[0][0]
        assert "SECURITY" in prompt

    def test_security_in_execute_lead_prompt(
        self, sample_state, tmp_state_dir, tmp_path
    ):
        """V2: Security instructions in the lead session prompt for execute."""
        sample_state["manifest_path"] = "/tmp/manifest.md"
        log_file = tmp_path / "log.md"
        log_file.write_text("x")
        resp = {"do_log_path": str(log_file)}
        with patch.object(orch, "invoke_claude", return_value=resp) as mock_ic:
            orch.phase_execute(sample_state)
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

        for p in prompts_seen:
            assert "SECURITY" in p


# ---------------------------------------------------------------------------
# No poll_slack_thread in V2
# ---------------------------------------------------------------------------


class TestNoPollSlackThread:
    def test_poll_slack_thread_does_not_exist(self):
        """V2: poll_slack_thread function was removed (teammates poll themselves)."""
        assert not hasattr(orch, "poll_slack_thread")
