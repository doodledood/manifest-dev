"""A grader shared across eval cases stays one rubric across its copies."""

from __future__ import annotations

from pathlib import Path

import pytest

EVALS = Path(__file__).parent.parent / "claude-plugins/manifest-dev/evals"
SHARED = ["define/*/graders/gates-are-settleable.md", "*/graders/turn-discipline.md"]


@pytest.mark.parametrize("pattern", SHARED)
def test_shared_grader_copies_are_identical(pattern: str) -> None:
    copies = sorted(EVALS.glob(pattern))
    assert (
        len(copies) >= 2
    ), f"expected several copies of {pattern}, found {len(copies)}"
    reference = copies[0].read_text()
    drifted = [str(c.relative_to(EVALS)) for c in copies if c.read_text() != reference]
    assert (
        not drifted
    ), f"{pattern} drifted from {copies[0].relative_to(EVALS)}: {drifted}"
