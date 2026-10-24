"""Saved measurements must be complete and use the same frozen instrument."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.eval_result_fixtures import case, edit_result, grader, write

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/evals/score_rounds.py"


def score(
    tmp_path: Path, *runs: str, ids: tuple[str, ...] = ("a",)
) -> subprocess.CompletedProcess[str]:
    state = tmp_path / "_state.json"
    state.write_text(json.dumps({"train_ids": list(ids), "test_ids": []}))
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(state), *runs],
        capture_output=True,
        text=True,
    )


def case_score(out: str, name: str, label_index: int) -> str:
    row = next(line for line in out.splitlines() if line.startswith(f"| {name} |"))
    return row.split("|")[3 + label_index].strip()


def test_diagnostics_never_enter_quality_even_when_all_runs_score_them(
    tmp_path: Path,
) -> None:
    base = write(
        tmp_path / "base.json",
        case(
            "a", [[grader("quality", False), grader("handoff", True, diagnostic=True)]]
        ),
    )
    result = score(tmp_path, f"base={base}")
    assert result.returncode == 0, result.stderr
    assert case_score(result.stdout, "a", 0) == "0.00"


def test_a_round_can_use_explicit_subset_and_its_planned_repetition_depth(
    tmp_path: Path,
) -> None:
    baseline = write(
        tmp_path / "base.json",
        case("a", [[grader("quality", False)]]),
        case("b", [[grader("quality", True)]]),
    )
    write(tmp_path / "v1/a.json", case("a", [[grader("quality", True)]] * 3))
    result = score(tmp_path, f"base={baseline}", f"v1={tmp_path / 'v1'}")
    assert result.returncode == 0, result.stderr
    assert "not scored: b" in result.stdout
    assert case_score(result.stdout, "a", 1) == "1.00"


def test_missing_requested_case_is_not_silently_intersected(tmp_path: Path) -> None:
    result_file = write(tmp_path / "a.json", case("a", [[grader("q", True)]]))
    result = score(tmp_path, f"v1={result_file}", ids=("a", "b"))
    assert result.returncode != 0
    assert "missing requested cases: b" in result.stderr


def test_a_case_in_two_results_of_one_round_is_refused(tmp_path: Path) -> None:
    write(tmp_path / "v1/a.json", case("a", [[grader("q", True)]]))
    write(tmp_path / "v1/again.json", case("a", [[grader("q", True)]]))
    result = score(tmp_path, f"v1={tmp_path / 'v1'}")
    assert result.returncode != 0
    assert "cases in more than one result: a" in result.stderr


@pytest.mark.parametrize(
    "mutation, message",
    [
        ("missing_grader", "grader results"),
        ("missing_case", "case roster"),
        ("missing_rep", "repetitions"),
        ("error", "agent error"),
        ("partial", "partial run"),
        ("grader_error", "grader threw"),
        ("skipped", "skipped:"),
        ("weight", "changed weight"),
        ("definition", "instrument changed"),
        ("duplicate", "duplicate names"),
        ("unscored", "not scored"),
        ("model", "model differs"),
        ("votes", "incomplete judge votes"),
    ],
)
def test_incomplete_or_changed_measurement_fails_closed(
    tmp_path: Path, mutation: str, message: str
) -> None:
    path = write(
        tmp_path / "result.json",
        case("a", [[grader("q", True), grader("guard", False)]]),
    )
    data = edit_result(path)
    saved_case = data["cases"][0]
    run = saved_case["arms"]["with"][0]
    if mutation == "missing_grader":
        run["graders"].pop()
    elif mutation == "missing_case":
        data["cases"] = []
    elif mutation == "missing_rep":
        saved_case["arms"]["with"] = []
    elif mutation == "error":
        run["error"] = "API unavailable"
        run["graders"] = []
    elif mutation == "partial":
        data["partial"] = True
    elif mutation == "grader_error":
        run["graders"][0]["explanation"] = "grader threw: file absent"
    elif mutation == "skipped":
        run["graders"][0]["explanation"] = "skipped: cost ceiling"
    elif mutation == "weight":
        run["graders"][0]["weight"] = 100
    elif mutation == "definition":
        saved_case["graders"][0]["config"]["criteria"] = "easier"
    elif mutation == "duplicate":
        run["graders"].append(run["graders"][0])
    elif mutation == "unscored":
        run["graders"][0]["scored"] = False
    elif mutation == "model":
        saved_case["model"] = "sonnet"
    elif mutation == "votes":
        run["graders"][0]["judgeVotes"] = []
    path.write_text(json.dumps(data))
    result = score(tmp_path, f"run={path}")
    assert result.returncode != 0
    assert message in result.stderr
    assert "| case |" not in result.stdout


def test_individually_valid_runs_with_changed_rubrics_cannot_compare(
    tmp_path: Path,
) -> None:
    first = write(tmp_path / "base.json", case("a", [[grader("q", True)]]))
    changed = grader("q", True)
    changed["config"]["criteria"] = "an easier rubric"
    second = write(tmp_path / "round.json", case("a", [[changed]]))
    result = score(tmp_path, f"base={first}", f"round={second}")
    assert result.returncode != 0
    assert "instrument or runtime changed" in result.stderr


def test_missing_launch_instrument_is_not_reconstructed_from_checkout(
    tmp_path: Path,
) -> None:
    path = tmp_path / "old.json"
    path.write_text(json.dumps({"cases": []}))
    result = score(tmp_path, f"old={path}")
    assert result.returncode != 0
    assert "missing launch contract" in result.stderr
