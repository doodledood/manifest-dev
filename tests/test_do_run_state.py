"""`/do`'s run state survives the events the environment can produce.

A run's state is instructions, not code: which evidence a verdict still stands on, which
log a relaunch opens, which path a run ends on. Each test here holds one rule whose absence
let a verdict outlive what it assessed, or let a run's record go somewhere a later launch
cannot find it. They pin the rule's wording in every shipped copy, since a copy that loses
the clause ships the hole again under the same skill name.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "claude-plugins/manifest-dev/skills"
CODEX = ROOT / "dist/codex/plugins/manifest-dev/skills"


def flat(relative: str) -> list[tuple[Path, str]]:
    """Every shipped copy of one skill file, whitespace-normalized."""
    copies = []
    for base in (SOURCE, CODEX):
        path = base / relative
        copies.append((path, re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))))
    return copies


# A gate broadened in place by an amendment kept its ID and its PASS: the next evaluation
# was a continued look, reporting only what the intervening code changes introduced, so
# unchanged code the broadened claim now covers was never judged, and a finding dismissed
# as outside the old claim stayed dismissed. A change to a gate's criteria — its text and
# the Manifest sections its claim reads — takes a new full look and reopens dispositions,
# and the ceiling, which reads the whole Manifest, re-verifies after every amendment.
def test_changed_criteria_take_a_new_full_look() -> None:
    for path, text in flat("do/SKILL.md"):
        assert (
            "When a judgment gate's criteria change, its next evaluation is a new full look"
            in text
        ), path
        assert (
            "A gate's criteria are its text and every Manifest section its claim reads"
            in (text)
        ), path
        assert "re-verifies after every amendment" in text, path
        assert "the ceiling when Appetite changes" not in text, path
        assert (
            "new code, changed criteria, argument or evidence can reopen them" in text
        ), path
    for path, text in flat("review-code/SKILL.md"):
        assert (
            "Criteria that changed since that evaluation make this a fresh review"
            in (text)
        ), (path)
        assert "changed code, criteria, argument or evidence can" in text, path
    for path, text in flat("do/references/LOG.md"):
        assert "taken its full look under its current criteria" in text, path
