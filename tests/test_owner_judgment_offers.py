"""Optional authority-surface offers need a person; an authorized handoff is not an answer.

Holds the decision in
docs/adr/20261024-absence-is-not-acceptance-of-optional-authority-offers.md.
"""

from __future__ import annotations

import re
from pathlib import Path

SKILLS = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins"
    / "manifest-dev"
    / "skills"
)
SETUP = SKILLS / "setup-project" / "SKILL.md"
AUTONOMOUS = SKILLS / "figure-out" / "references" / "autonomous.md"


def _flat(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


def test_setup_treats_absence_as_not_an_answer() -> None:
    text = _flat(SETUP)
    assert "does not treat absence as wanted or as an answer" in text
    assert (
        "Inference from existing instructions does not make an optional item wanted "
        "when no person is present" in text
    )
    assert "Absence is not an answer" in text
    assert "the version line waits" in text
    assert "which owner-judgment items were flagged unanswered" in text


def test_setup_asks_retained_decisions_when_a_person_accepts_coordination() -> None:
    text = _flat(SETUP)
    assert "When a person accepts coordination" in text
    assert "ask which decisions they retain" in text
    assert "principle with an example they give, not a closed list" in text
    assert "The owner names the set" in text
    assert "no empty policy document" in text


def test_autonomous_handoff_does_not_self_accept_inner_owner_judgment_offers() -> None:
    text = _flat(AUTONOMOUS)
    assert "An authorized handoff runs that workflow" in text
    assert "does not self-accept that workflow's inner owner-judgment offers" in text
    assert "Those take the flagged-candidate branch" in text
    assert "The handoff exception covers the assignment itself" in text
