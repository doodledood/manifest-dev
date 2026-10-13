"""The reader-task surface for this repository's living documents points at sections that exist.

Each entry in `docs/reader-tasks/TASKS.md` names, on its `Where:` line, the documents a
reader relies on, as pointers `FILE` → *Section* joined by "; ", where a pointer may name more
sections as *A* and *B*. A section is a Markdown heading, or a site chapter's `data-name`. A renamed or removed
section leaves the entry pointing at nothing, so the walk it describes cannot run.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "docs" / "reader-tasks" / "TASKS.md"

ENTRY = re.compile(r"^## (.+?)\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
SECTION = r"\*([^*\n]+)\*"
POINTER = re.compile(rf"`([\w./-]+\.(?:md|html))` → ({SECTION}(?: and {SECTION})*)")
WHERE = re.compile(r"^- \*\*Where:\*\* (.+)$", re.MULTILINE)
STATUS_LINE = re.compile(r"^- \*\*Status:\*\* (.*)$", re.MULTILINE)
STATUS = re.compile(
    r"unverified|verified \(\d{4}-\d{2}-\d{2}\)|stale \(\d{4}-\d{2}-\d{2}\).*"
)


def _has_section(path: Path, title: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".html":
        return f'data-name="{title}"' in text
    return bool(re.search(rf"^#+ {re.escape(title)}\s*$", text, re.MULTILINE))


ENTRIES = ENTRY.findall(TASKS.read_text(encoding="utf-8"))


def test_entries_are_found() -> None:
    assert ENTRIES, "no entries matched; check ENTRY against TASKS.md"


def test_every_entry_points_at_existing_sections_and_carries_a_status() -> None:
    broken = []
    for task, body in ENTRIES:
        wheres = WHERE.findall(body)
        if len(wheres) != 1:
            broken.append(f"{task}: {len(wheres)} Where lines, expected one")
        parts = wheres[0].split("; ") if wheres else []
        statuses = STATUS_LINE.findall(body)
        if len(statuses) != 1 or not STATUS.fullmatch(statuses[0]):
            broken.append(f"{task}: needs exactly one valid status line")
        for part in parts:
            pointer = POINTER.fullmatch(part)
            if not pointer:
                broken.append(f"{task}: not written `FILE` → *Section*: {part}")
                continue
            path = ROOT / pointer.group(1)
            if not path.is_file():
                broken.append(f"{task}: {pointer.group(1)} does not exist")
                continue
            for name in re.findall(SECTION, pointer.group(2)):
                if not _has_section(path, name):
                    broken.append(f"{task}: {pointer.group(1)} has no section *{name}*")
    assert not broken, "\n".join(broken)
