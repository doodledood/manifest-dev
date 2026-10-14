"""The workflow skills share one definition of a project, restated in each because a shipped
skill stands alone. These checks keep the copies from drifting apart.

Holds the decision in docs/adr/20261014-project-surfaces-follow-the-context.md.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parent.parent / "claude-plugins/manifest-dev/skills"

# Every copy counts a new project and excludes the same projectless places.
SHARED = (
    "or about to hold, work",
    "later sessions will change",
    "a home or scratch folder",
    "folder holding one finished artifact",
)
# Skills that gate verification also keep one-off work inside a project as project work.
ONE_OFF = "One-off work inside a project is still project work"

COPIES = {
    "figure-out/SKILL.md": True,
    "define/SKILL.md": True,
    "do/SKILL.md": True,
    "setup-project/SKILL.md": False,
}


@pytest.mark.parametrize(("path", "gates"), COPIES.items())
def test_each_skill_states_the_same_project_definition(path: str, gates: bool) -> None:
    text = re.sub(r"\s+", " ", (SKILLS / path).read_text(encoding="utf-8"))
    for clause in SHARED + ((ONE_OFF,) if gates else ()):
        assert clause in text, f"{path} lacks the shared project clause: {clause!r}"
