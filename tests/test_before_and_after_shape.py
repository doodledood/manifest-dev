"""The before-and-after keeps one shape wherever a shipped skill asks for one.

Holds the decision in docs/adr/20261120-a-read-and-a-plan-summary-show-a-before-and-after.md:
figure-out's read, define's plan summary and the pull request description define's
`PR_LIFECYCLE.md` asks for each show a before-and-after whose sides say, from the person's side,
what they do and what they get or notice. Each skill states the shape itself, since a shipped
skill stands alone, so this test keeps the copies in step: a sharpening that lands in one file
must reach the others.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.prose import flat as _flat

SKILLS = Path(__file__).resolve().parent.parent / "claude-plugins/manifest-dev/skills"
RECORD = "docs/adr/20261120-a-read-and-a-plan-summary-show-a-before-and-after.md"
SHARED_CLAUSE = "from that person's side, what they do and what they get or notice"
CARRIERS = (
    "figure-out/SKILL.md",
    "define/SKILL.md",
    "define/tasks/PR_LIFECYCLE.md",
)


@pytest.mark.parametrize("relative", CARRIERS)
def test_each_before_and_after_states_the_shared_clause(relative: str) -> None:
    text = _flat((SKILLS / relative).read_text(encoding="utf-8"))
    assert SHARED_CLAUSE in text, (
        f"{relative} no longer says each side of its before-and-after speaks "
        f"{SHARED_CLAUSE!r}. Change the shape in every file of {CARRIERS} together; see {RECORD}"
    )
