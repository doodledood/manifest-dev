from __future__ import annotations

import json
from pathlib import Path

from behavior_lab.experiment import (
    Arm,
    RunResult,
    Scenario,
    attribute_sessions,
    discover_run_dirs,
    load_run_calls,
    run_dir,
    run_experiment,
    summarize_arm,
    summarize_run,
    summarize_run_by_label,
)
from behavior_lab.harness import Harness, InvokeResult


class _FakeHarness(Harness):
    def __init__(self) -> None:
        self.configured_dirs: list[Path] = []
        self.invoked: list[tuple[str, object, str | None]] = []

    def configure_for_capture(self, run_directory: Path) -> dict[str, str]:
        self.configured_dirs.append(run_directory)
        return {"FAKE_ENV": "1"}

    def invoke(self, prompt: str, *, cwd, env) -> InvokeResult:
        self.invoked.append((prompt, cwd, env.get("FAKE_ENV")))
        return InvokeResult(returncode=0, stdout="ok", stderr="")

    def decode_call(self, diagnostics_entry):
        return {}


def _write_call(
    diagnostics_dir: Path,
    name: str,
    *,
    session_id: str,
    method: str = "POST",
    status: int = 200,
    request_text: str = "",
    output_tokens: int = 1,
) -> None:
    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    entry = {
        "session_id": session_id,
        "agent_id": None,
        "is_subagent": False,
        "method": method,
        "response_status": status,
        "request_body": {"messages": [{"role": "user", "content": request_text}]},
        "response_body": {
            "type": "message",
            "usage": {
                "input_tokens": 10,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            },
        },
    }
    (diagnostics_dir / f"{name}.json").write_text(json.dumps(entry), encoding="utf-8")


def test_run_dir_is_deterministic_on_identical_inputs() -> None:
    a = run_dir("/base", scenario="s1", arm="baseline", repeat_index=0)
    b = run_dir("/base", scenario="s1", arm="baseline", repeat_index=0)
    assert a == b


def test_run_dir_negative_differs_on_repeat_index() -> None:
    a = run_dir("/base", scenario="s1", arm="baseline", repeat_index=0)
    b = run_dir("/base", scenario="s1", arm="baseline", repeat_index=1)
    assert a != b


def test_run_experiment_invokes_harness_and_writes_artifacts(tmp_path: Path) -> None:
    harness = _FakeHarness()
    scenario = Scenario(name="s1", prompt="do the thing", cwd=tmp_path)
    arm = Arm(name="baseline", harness=harness)

    results = run_experiment([scenario], [arm], tmp_path / "runs")

    assert len(results) == 1
    result = results[0]
    assert isinstance(result, RunResult)
    assert result.returncode == 0
    assert (result.run_directory / "prompt.txt").read_text(
        encoding="utf-8"
    ) == "do the thing"
    metadata = json.loads(
        (result.run_directory / "metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["scenario"] == "s1"
    assert metadata["arm"] == "baseline"
    assert harness.invoked == [("do the thing", tmp_path, "1")]


def test_load_run_calls_and_summarize_run(tmp_path: Path) -> None:
    diagnostics_dir = tmp_path / "diagnostics"
    _write_call(diagnostics_dir, "call-0000", session_id="sess-1", output_tokens=5)
    _write_call(diagnostics_dir, "call-0001", session_id="sess-1", output_tokens=7)
    # negative: a non-200 call must be excluded from load_run_calls/summarize_run
    _write_call(
        diagnostics_dir, "call-0002", session_id="sess-1", status=500, output_tokens=999
    )

    calls = load_run_calls(diagnostics_dir)
    assert len(calls) == 2
    assert all(c["usage"]["output_tokens"] != 999 for c in calls)

    summary = summarize_run(diagnostics_dir)
    assert summary["call_count"] == 2
    assert summary["session_count"] == 1
    assert summary["total_tokens"]["output_tokens"] == 12


def test_attribute_sessions_and_summarize_run_by_label(tmp_path: Path) -> None:
    run_directory = tmp_path / "run"
    diagnostics_dir = run_directory / "diagnostics"
    _write_call(
        diagnostics_dir,
        "call-0000",
        session_id="sess-a",
        request_text="baseline prompt text",
    )
    _write_call(
        diagnostics_dir,
        "call-0001",
        session_id="sess-b",
        request_text="amended prompt text",
    )
    _write_call(
        diagnostics_dir, "call-0002", session_id="sess-c", request_text="unrelated text"
    )

    mapping = attribute_sessions(
        run_directory,
        {"baseline": "baseline prompt text", "amended": "amended prompt text"},
    )
    assert mapping == {"sess-a": "baseline", "sess-b": "amended"}
    assert "sess-c" not in mapping

    per_label = summarize_run_by_label(
        run_directory,
        {"baseline": "baseline prompt text", "amended": "amended prompt text"},
    )
    assert per_label["baseline"]["call_count"] == 1
    assert per_label["amended"]["call_count"] == 1
    assert per_label["_unattributed"]["call_count"] == 1


def test_discover_run_dirs_and_summarize_arm(tmp_path: Path) -> None:
    base = tmp_path / "runs"
    run_directory = run_dir(base, scenario="s1", arm="baseline", repeat_index=0)
    _write_call(
        run_directory / "diagnostics", "call-0000", session_id="sess-1", output_tokens=3
    )

    found = discover_run_dirs(base, "baseline")
    assert found == [run_directory]

    summary = summarize_arm(base, "baseline")
    assert summary["run_count"] == 1
    assert summary["total_calls"] == 1
    assert summary["total_tokens"]["output_tokens"] == 3


def test_discover_run_dirs_negative_no_runs_for_arm(tmp_path: Path) -> None:
    assert discover_run_dirs(tmp_path / "runs", "nonexistent-arm") == []
