"""A handoff's file name stays unique when two sessions write one in the same second.

The name carried only a seconds timestamp, so a second handoff in the same second overwrote the
first; the audit of the skills' own state machines confirmed it by the same reasoning as
figure-out's log path.
"""

from __future__ import annotations

from pathlib import Path

HANDOFF = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md"
)


def test_handoff_name_carries_a_unique_suffix_and_is_created_only_where_free() -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    assert (
        "handoff-{timestamp}-{id}.md" in text
    ), "the handoff path must carry a random id"
    assert (
        "only where that path is free" in text
    ), "the handoff must never overwrite a file"
