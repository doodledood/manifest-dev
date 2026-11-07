"""poll-slack follows thread replies on a channel without re-reading every thread each poll."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COPIES = (
    REPO_ROOT / "claude-plugins/manifest-dev/skills/poll-slack/SKILL.md",
    REPO_ROOT / "dist/codex/plugins/manifest-dev/skills/poll-slack/SKILL.md",
)


# A reply posted in a thread appears only in that thread, so a channel poll reads each thread
# the caller passed. The caller keeps every thread cursor the poller returns, so the set only
# grows, and a poll that read every one re-read every thread of the deliberation each time.
# A thread whose first message shows no reply after its cursor is skipped, cursor unchanged.
def test_a_passed_thread_with_no_new_reply_is_not_read() -> None:
    for path in COPIES:
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
        assert "and each thread the caller passed after its own cursor" in text, path
        assert (
            "where it shows no reply after the thread's cursor, skip reading that thread and"
            " return its cursor unchanged" in text
        ), path
