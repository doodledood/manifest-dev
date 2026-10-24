"""Extraction never substitutes another grader, an HTML ordering, or stale output."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.eval_result_fixtures import case, edit_result, grader, write

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/evals/extract_outputs.py"


def extract(
    tmp_path: Path, path: Path, *extra: str
) -> subprocess.CompletedProcess[str]:
    state = tmp_path / "state.json"
    state.write_text(json.dumps({"train_ids": ["a"], "test_ids": ["held"]}))
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(path),
            "--out",
            str(tmp_path / "out"),
            "--state",
            str(state),
            "--cases",
            "a",
            "--grader",
            "artifact",
            *extra,
        ],
        capture_output=True,
        text=True,
    )


def test_named_grader_selects_artifact_not_first_trace_evidence(tmp_path: Path) -> None:
    trace = grader("trace", True)
    trace["config"]["focus"] = "trace"
    path = write(
        tmp_path / "result.json", case("a", [[trace, grader("artifact", False)]])
    )
    result = extract(tmp_path, path)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "out/a_rep0.md").read_text() == "artifact evidence"
    meta = json.loads((tmp_path / "out/a_rep0.grades.json").read_text())
    assert meta["source"] == {"source": "file", "path": "manifest.md"}
    assert (meta["case"], meta["arm"], meta["repetition"], meta["grader"]) == (
        "a",
        "with",
        0,
        "artifact",
    )


@pytest.mark.parametrize("evidence", [None, 123])
def test_missing_evidence_is_failure_before_any_output(
    tmp_path: Path, evidence: int | None
) -> None:
    path = write(tmp_path / "r.json", case("a", [[grader("artifact", True)]] * 2))
    data = edit_result(path)
    data["cases"][0]["arms"]["with"][1]["graders"][0]["evidence"] = evidence
    path.write_text(json.dumps(data))
    result = extract(tmp_path, path)
    assert result.returncode != 0
    assert "missing text evidence" in result.stderr
    assert not (tmp_path / "out").exists()


def test_stale_output_is_refused_and_left_intact(tmp_path: Path) -> None:
    path = write(tmp_path / "r.json", case("a", [[grader("artifact", True)]]))
    (tmp_path / "out").mkdir()
    stale = tmp_path / "out/a_rep0.md"
    stale.write_text("old")
    result = extract(tmp_path, path)
    assert result.returncode != 0
    assert "must be empty" in result.stderr
    assert stale.read_text() == "old"


def test_held_out_evidence_cannot_enter_analyzer_directory(tmp_path: Path) -> None:
    path = write(tmp_path / "r.json", case("held", [[grader("artifact", True)]]))
    result = extract(tmp_path, path, "--cases", "held")
    assert result.returncode != 0
    assert "held-out evidence stays sealed" in result.stderr


def test_html_recovery_is_not_an_identity_source(tmp_path: Path) -> None:
    path = write(tmp_path / "r.json", case("a", [[grader("artifact", True)]]))
    result = extract(tmp_path, path, "--report", "same-grades-wrong-run.html")
    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr
