"""The inventory agrees with an independent Claude Code serialization oracle."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
from typing import Any

import pytest

from tests.native_eval_fixture import ARGV, RESULT, SOURCES

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "eval_contract", ROOT / "scripts/evals/eval_contract.py"
)
assert spec and spec.loader
contract_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract_module)


def instrument(tmp_path: Path, *, defaults: bool = False) -> dict[str, Any]:
    for name, source in SOURCES.items():
        if defaults and name.endswith("prompt.md"):
            source = source.replace("max_turns: 40\n", "").replace(
                "timeout_seconds: 900\n", ""
            )
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
    result: dict[str, Any] = contract_module.inventory(tmp_path, ARGV, "2.1.306")
    return result


def test_inventory_matches_independently_derived_native_result(tmp_path: Path) -> None:
    contract = instrument(tmp_path)
    contract_module.validate(RESULT, contract)
    expected = [
        {k: g[k] for k in ("name", "type", "weight", "config")}
        for g in RESULT["cases"][0]["graders"]
    ]
    assert contract["cases"][0]["graders"] == expected
    assert contract["cases"][0]["model"] == "sonnet"
    assert contract["cases"][0]["runs"] == 1


def test_native_defaults_are_retained_before_launch(tmp_path: Path) -> None:
    contract = instrument(tmp_path, defaults=True)
    result = copy.deepcopy(RESULT)
    result["cases"][0].update(maxTurns=10, timeoutSeconds=300)
    contract_module.validate(result, contract)


@pytest.mark.parametrize(
    "explanation, valid",
    [
        (
            'grader threw: case "native-case" grader focus file "manifest.md": path "manifest.md" does not exist',
            True,
        ),
        ("grader threw: focus file manifest.md does not exist", True),
        (
            'grader threw: case "different-case" grader focus file "manifest.md": path "manifest.md" does not exist',
            False,
        ),
        ("grader threw: focus file different.md does not exist", False),
        ("grader threw: focus file manifest.md is unreadable", False),
    ],
)
def test_only_absence_of_the_expected_artifact_is_a_behavioral_failure(
    tmp_path: Path,
    explanation: str,
    valid: bool,
) -> None:
    contract = instrument(tmp_path)
    result = copy.deepcopy(RESULT)
    grade = result["cases"][0]["arms"]["with"][0]["graders"][0]
    grade.update(passed=False, explanation=explanation)
    grade.pop("judgeVotes")
    grade.pop("evidence")
    if valid:
        contract_module.validate(result, contract)
    else:
        with pytest.raises(contract_module.InvalidRunError, match="grader threw"):
            contract_module.validate(result, contract)
