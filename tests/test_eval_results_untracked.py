"""Eval run results stay local; the eval READMEs are the record."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESULTS = "claude-plugins/manifest-dev/evals/results"


def test_no_eval_results_are_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--", RESULTS],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    assert not tracked, (
        "eval results are committed; they carry sandbox paths and model output — "
        f"untrack them and record the numbers in the README instead: {tracked}"
    )
