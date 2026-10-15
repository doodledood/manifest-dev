"""The verification harness is the project's choice, never a run's. Each workflow skill that
builds, gates on or offers a harness keeps the condition that it does so only where the project
chose one, and names the project's own way of verifying as the other path.

Holds the decision in docs/adr/20261015-the-verification-harness-is-optional.md.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parent.parent / "claude-plugins/manifest-dev/skills"

# Per file: the clause making harness work conditional on the project's choice, and the clause
# naming the project's own way as the other path.
CONDITIONS = {
    "define/SKILL.md": (
        "harness is the project's choice, never the run's",
        "no gate or Deliverable builds or repairs a harness the project did not choose",
    ),
    "do/SKILL.md": (
        "names a verification harness and the work needs a part it lacks",
        "project's own way of verifying, or names none, verify through what the project keeps",
    ),
    "do/references/VERIFICATION.md": (
        "this file applies only where the project-surfaces section of the context file names a "
        "verification harness",
        "the project's choice and never the run's",
    ),
    "figure-out/SKILL.md": (
        "never a harness the project did not choose",
        "or the project's own commands and steps",
    ),
    "figure-out/tasks/CODING.md": (
        "A harness is the project's choice, offered at setup or in a report, never built as part "
        "of the work",
        "the project verifies its own way, or never chose",
    ),
    "setup-project/SKILL.md": (
        "adopt the harness, or keep verifying the project's own way",
        "record them in the own-way form of the verification bullet",
    ),
    "setup-project/references/NORTH_STAR_FORMAT.md": (
        "That entry is where the choice lives",
        "verifies its own way by choice: add no separate verification tool to it",
    ),
}

# Sentences that built or seeded a harness wherever the project named none.
UNCONDITIONAL = (
    "build one from what is found, or from nothing",
    "a new verification harness the user may remove",
    "Where it is missing, or a recipe the work touches is drifting",
)


def _text(path: str) -> str:
    return re.sub(r"\s+", " ", (SKILLS / path).read_text(encoding="utf-8"))


@pytest.mark.parametrize(("path", "clauses"), CONDITIONS.items())
def test_harness_work_is_conditional_on_the_projects_choice(
    path: str, clauses: tuple[str, str]
) -> None:
    text = _text(path)
    for clause in clauses:
        assert clause in text, f"{path} lost the optional-harness clause: {clause!r}"


@pytest.mark.parametrize("phrase", UNCONDITIONAL)
def test_no_skill_builds_a_harness_unconditionally(phrase: str) -> None:
    hits = [
        str(p.relative_to(SKILLS))
        for p in SKILLS.rglob("*.md")
        if phrase in re.sub(r"\s+", " ", p.read_text(encoding="utf-8"))
    ]
    assert (
        not hits
    ), f"{phrase!r} builds a harness the project did not choose, in {hits}"
