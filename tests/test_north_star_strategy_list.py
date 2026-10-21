"""The North Star's strategy list is a derived index of the Strategy records in effect.

`docs/adr/CONVENTIONS.md` reserves the area `Strategy` for a guiding choice, and
`docs/NORTH_STAR_CONVENTIONS.md` says how the North Star's *Strategy choices in force* list is
rebuilt from those records: one line per record in effect, in filename order, its title and —
where the record has a `Revisit when` field — its signpost. A list kept by hand drifts from the
records the way the ADR index did, so this test rebuilds it under that rule and fails on any
difference, a missing or stale signpost included.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR = REPO_ROOT / "docs" / "adr"
NORTH_STAR = REPO_ROOT / "NORTH_STAR.md"
LIST_HEADING = "## Strategy choices in force"
SIGNPOST_SEPARATOR = " — revisit when: "


def _field(text: str, heading: str) -> str | None:
    """The body of a `## <heading>` section, up to the next `## ` heading."""
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match["body"].strip() if match else None


def _one_line(text: str) -> str:
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def expected_lines() -> list[str]:
    lines = []
    for record in sorted(ADR.glob("*.md")):
        if record.name in ("README.md", "CONVENTIONS.md"):
            continue
        text = record.read_text(encoding="utf-8")
        area = _field(text, "Area")
        status = _field(text, "Status")
        title = re.search(r"^# ADR: (.+)$", text, re.MULTILINE)
        assert area and status and title, f"{record.name} lacks a title, Status or Area"
        # Only an Accepted record is in effect, including one a later record amends.
        if area != "Strategy" or not status.startswith("Accepted"):
            continue
        line = f"- {title.group(1).strip()}"
        signpost = _field(text, "Revisit when")
        if signpost:
            line += SIGNPOST_SEPARATOR + _one_line(signpost)
        lines.append(line)
    return lines


def listed_lines() -> list[str]:
    text = NORTH_STAR.read_text(encoding="utf-8")
    assert LIST_HEADING in text, f"NORTH_STAR.md has no `{LIST_HEADING}` section"
    section = text.split(LIST_HEADING, 1)[1].split("\n## ", 1)[0]
    return [line.rstrip() for line in section.splitlines() if line.strip()]


# Holds the decisions in docs/adr/20261021-the-north-star-holds-what-decisions-are-judged-against.md
# and docs/adr/20261021-the-north-star-opens-with-its-end-and-signposts-reopen-choices-and-deferred-work.md.
def test_strategy_list_is_rebuilt_from_the_strategy_records_in_effect() -> None:
    expected = expected_lines()
    listed = listed_lines()
    assert listed == expected, (
        "NORTH_STAR.md → *Strategy choices in force* must be exactly the lines rebuilt from the "
        "Accepted records in docs/adr/ with area `Strategy`, in filename order: `- <title>`, "
        f"plus `{SIGNPOST_SEPARATOR.strip()} <Revisit when>` where the record has one "
        "(docs/NORTH_STAR_CONVENTIONS.md → *The sections*). Rebuild it from them.\n"
        f"Listed but not rebuilt: {[line for line in listed if line not in expected]}\n"
        f"Rebuilt but not listed: {[line for line in expected if line not in listed]}"
    )
