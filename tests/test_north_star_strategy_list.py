"""The North Star's strategy list is a derived index of the Strategy records in effect.

`docs/adr/CONVENTIONS.md` reserves the area `Strategy` for a guiding choice and says the North
Star's *Strategy choices in force* list holds the titles of those records in effect and nothing
else. A list kept by hand drifts from the records the way the ADR index did, so this test rebuilds
it from the records and fails on any title on one side only.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR = REPO_ROOT / "docs" / "adr"
NORTH_STAR = REPO_ROOT / "NORTH_STAR.md"
LIST_HEADING = "## Strategy choices in force"


def strategy_titles_in_effect() -> set[str]:
    titles = set()
    for record in ADR.glob("*.md"):
        if record.name in ("README.md", "CONVENTIONS.md"):
            continue
        text = record.read_text(encoding="utf-8")
        area = re.search(r"^## Area\n(.+)$", text, re.MULTILINE)
        status = re.search(r"^## Status\n(.+)$", text, re.MULTILINE)
        title = re.search(r"^# ADR: (.+)$", text, re.MULTILINE)
        assert area and status and title, f"{record.name} lacks a title, Status or Area"
        # Only an Accepted record is in effect, including one a later record amends.
        if area.group(1).strip() == "Strategy" and status.group(1).startswith(
            "Accepted"
        ):
            titles.add(title.group(1).strip())
    return titles


def listed_titles() -> set[str]:
    text = NORTH_STAR.read_text(encoding="utf-8")
    assert LIST_HEADING in text, f"NORTH_STAR.md has no `{LIST_HEADING}` section"
    section = text.split(LIST_HEADING, 1)[1].split("\n## ", 1)[0]
    return {m.group(1).strip() for m in re.finditer(r"^- (.+)$", section, re.MULTILINE)}


# Holds the decision in docs/adr/20261021-the-north-star-holds-what-decisions-are-judged-against.md.
def test_strategy_list_equals_the_strategy_records_in_effect() -> None:
    records = strategy_titles_in_effect()
    listed = listed_titles()
    assert listed == records, (
        "NORTH_STAR.md → *Strategy choices in force* must list exactly the titles of the "
        "Accepted records in docs/adr/ with area `Strategy`; rebuild it from them.\n"
        f"Listed but no such record: {sorted(listed - records)}\n"
        f"Record not listed: {sorted(records - listed)}"
    )
