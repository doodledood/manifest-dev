"""
Every pointer a shipped file makes to a named section of another shipped file resolves.

A pointer is written `FILE.md` → *Section*, with `FILE.md`'s *Section* accepted as the
same thing. The section must still exist in the target as a heading or as a bold
paragraph lead (`**Section.**`). A section renamed without its pointers updated sends the
reader to text that no longer exists, and nothing else notices.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PLUGINS = ROOT / "claude-plugins"

POINTER = re.compile(r"`?([\w./-]+\.md)`?(?:'s| →) \*([A-Z][^*\n]{2,80})\*")


def shipped_markdown() -> list[Path]:
    return sorted(p for p in PLUGINS.rglob("*.md") if "evals" not in p.parts)


def resolve(source: Path, target: str) -> Path | None:
    for base in (source.parent, *source.parents):
        candidate = base / target
        if candidate.is_file():
            return candidate
        if base == PLUGINS:
            break
    return None


def has_section(text: str, title: str) -> bool:
    name = re.escape(title)
    heading = re.compile(rf"^#+ {name}\s*$", re.MULTILINE)
    lead = re.compile(rf"\*\*{name}\.?\*\*")
    return bool(heading.search(text) or lead.search(text))


POINTERS = [
    (source, match.group(1), match.group(2))
    for source in shipped_markdown()
    for match in POINTER.finditer(source.read_text())
]


def test_pointers_are_found() -> None:
    assert POINTERS, "the pointer pattern no longer matches anything; check POINTER"


def test_every_pointer_resolves() -> None:
    broken = []
    for source, target, title in POINTERS:
        where = source.relative_to(ROOT)
        resolved = resolve(source, target)
        if resolved is None:
            broken.append(f"{where} points to missing {target}")
        elif not has_section(resolved.read_text(), title):
            broken.append(
                f"{where} points to *{title}* in {resolved.relative_to(ROOT)}, "
                "which has no such heading or bold lead"
            )
    assert not broken, "\n".join(broken)
