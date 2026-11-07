"""`--no-docs` and `--team` keep a figure-out session from writing any project document.

Docs mode carries figure-out's project writes, and both flags suppress it. Recall offered its own
capture of a ruling found only in a local log as a decision record "written on acceptance" — and
`--autonomous` self-accepts an offer whose gate fires — so a run under `--no-docs`, such as the
audit-state-machines sweep that must write nothing in the audited project, could still write a
record there. Recall now names the ruling in the read instead under either flag.
"""

from __future__ import annotations

import re
from pathlib import Path

RECALL = (
    Path(__file__).resolve().parent.parent
    / "claude-plugins"
    / "manifest-dev"
    / "skills"
    / "figure-out"
    / "references"
    / "RECALL.md"
)


def test_recall_writes_no_record_under_no_docs_or_team() -> None:
    text = re.sub(r"\s+", " ", RECALL.read_text(encoding="utf-8"))
    assert "written on acceptance" in text, "recall no longer offers a captured record"
    rule = re.search(r"[^.]*`--no-docs`[^.]*\.", text)
    assert rule, f"{RECALL.name} must say what its capture does under `--no-docs`"
    assert "`--team`" in rule.group(0) and "offers no write" in rule.group(0), (
        f"{RECALL.name} must offer no project write under `--no-docs` or `--team`: "
        f"{rule.group(0)}"
    )
