"""The reader-task surface for this repository's living documents points at sections that exist.

Each entry in `docs/reader-tasks/TASKS.md` names the documents a reader relies on as
`FILE` → *Section*: a Markdown heading, or a site chapter's `data-name`. A renamed or removed
section leaves the entry pointing at nothing, so the walk it describes cannot run.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "docs" / "reader-tasks" / "TASKS.md"

ENTRY = re.compile(r"^## (.+?)\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
POINTER = re.compile(
    r"`([\w./-]+\.(?:md|html))` → \*([^*\n]+)\*((?: and \*[^*\n]+\*)*)"
)
STATUS = re.compile(
    r"^- \*\*Status:\*\* (unverified|verified \(\d{4}-\d{2}-\d{2}\)|stale \(\d{4}-\d{2}-\d{2}\).*)$",
    re.MULTILINE,
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
        pointers = POINTER.findall(body)
        if not pointers:
            broken.append(f"{task}: names no document section")
        if body.count("→") + body.count("->") != len(pointers):
            broken.append(f"{task}: a pointer is not written `FILE` → *Section*")
        if not STATUS.search(body):
            broken.append(f"{task}: no valid status")
        for file, title, more in pointers:
            path = ROOT / file
            if not path.is_file():
                broken.append(f"{task}: {file} does not exist")
                continue
            for name in [title, *re.findall(r"\*([^*\n]+)\*", more)]:
                if not _has_section(path, name):
                    broken.append(f"{task}: {file} has no section *{name}*")
    assert not broken, "\n".join(broken)
