"""`scripts/evals/score_rounds.py` compares hill-climb rounds like with like."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "evals" / "score_rounds.py"


def grader(name: str, passed: bool, scored: bool = True) -> dict[str, Any]:
    return {
        "name": name,
        "type": "llm",
        "config": {},
        "scored": scored,
        "weight": 1,
        "passed": passed,
    }


def case(name: str, runs: list[list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "name": name,
        "graders": [{k: g[k] for k in ("name", "type", "config")} for g in runs[0]],
        "arms": {"with": [{"costUsd": 1.0, "graders": gs} for gs in runs]},
    }


def write(path: Path, *cases: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"cases": list(cases)}))
    return path


def score(tmp_path: Path, *runs: str) -> str:
    state = tmp_path / "_state.json"
    state.write_text(json.dumps({"train_ids": ["a", "b"], "test_ids": ["c"]}))
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(state), *runs],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def case_score(out: str, name: str, label_index: int) -> str:
    row = next(line for line in out.splitlines() if line.startswith(f"| {name} |"))
    return row.split("|")[3 + label_index].strip()


def test_a_grader_only_one_run_scores_is_counted_in_neither(tmp_path: Path) -> None:
    # A with-only grader: left out under with-without, scored under --ablation none.
    baseline = write(
        tmp_path / "base.json",
        case("a", [[grader("quality", False), grader("handoff", True, scored=False)]]),
    )
    round1 = write(
        tmp_path / "v1.json",
        case("a", [[grader("quality", False), grader("handoff", True)]]),
    )
    out = score(tmp_path, f"base={baseline}", f"v1={round1}")
    assert case_score(out, "a", 0) == case_score(out, "a", 1) == "0.00"


def test_a_round_run_case_by_case_merges_and_compares_on_shared_cases(
    tmp_path: Path,
) -> None:
    baseline = write(
        tmp_path / "base.json",
        case("a", [[grader("quality", False)]]),
        case("b", [[grader("quality", True)]]),
        case("c", [[grader("quality", True)]]),
    )
    write(tmp_path / "v1" / "a.json", case("a", [[grader("quality", True)]] * 3))
    write(tmp_path / "v1" / "c.json", case("c", [[grader("quality", True)]] * 3))
    out = score(tmp_path, f"base={baseline}", f"v1={tmp_path / 'v1'}")
    assert "left out: b" in out
    assert case_score(out, "a", 1) == "1.00"
    assert not any(line.startswith("| b |") for line in out.splitlines())


def test_a_case_in_two_results_of_one_round_is_refused(tmp_path: Path) -> None:
    write(tmp_path / "v1" / "a.json", case("a", [[grader("quality", True)]]))
    write(tmp_path / "v1" / "again.json", case("a", [[grader("quality", True)]]))
    state = tmp_path / "_state.json"
    state.write_text(json.dumps({"train_ids": ["a"], "test_ids": []}))
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(state), f"v1={tmp_path / 'v1'}"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "cases in more than one result: a" in result.stderr
