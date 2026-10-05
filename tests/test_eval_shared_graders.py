"""A grader shared across eval cases stays one rubric across its copies."""

from __future__ import annotations

from pathlib import Path

import pytest

EVALS = Path(__file__).parent.parent / "claude-plugins/manifest-dev/evals"
SHARED = [
    "define/*/graders/gates-are-settleable.md",
    "define/*/graders/binding-lives-in-gates.md",
    "*/graders/turn-discipline.md",
]


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


ONE_WORD = "Work through the steps below privately, without writing them out."


def test_llm_graders_ask_for_a_one_word_reply() -> None:
    # The eval CLI's judge must reply with exactly PASS or FAIL. A rubric that asks it to list
    # or quote first gets a written answer back, which the CLI scores as FAIL.
    missing = []
    for grader in sorted(EVALS.glob("**/graders/*.md")):
        _, frontmatter, body = grader.read_text().split("---\n", 2)
        if "type: llm" in frontmatter and not body.startswith(ONE_WORD):
            missing.append(str(grader.relative_to(EVALS)))
    assert not missing, f"llm graders missing the one-word reply line: {missing}"
