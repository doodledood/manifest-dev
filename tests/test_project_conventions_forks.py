"""A project-owned conventions copy must reproduce what init-context would emit today.

`init-context` writes self-contained conventions files into a project so the project runs
without the plugin installed. Those copies govern, which means nothing may overwrite them —
so each one is a fork, and an improvement to the shipped default never reaches it. This
repo carries two such forks of its own. Nothing but this check would notice when a default
moves and its fork does not; the North Star pair drifted within twelve minutes of a default
edit before this existed.

The comparison is not whole-file: a correct copy differs from its default by the emission
recipe (a retitled heading, a replaced ownership section, and — for the North Star — a
dropped installer-facing chapter). What a copy must reproduce verbatim is the span or spans
the default marks with a fixed-boundary comment. Those spans are declared below, one entry
per fork, so that this repo deliberately ruling its own copy differently later is a
one-line, reviewable edit here rather than a reason to weaken the check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_SKILLS = REPO_ROOT / "claude-plugins" / "manifest-dev" / "skills"

BOUNDARY_COMMENT = re.compile(
    r"<!--(?:(?!-->).)*?fixed boundary.*?-->", re.DOTALL | re.IGNORECASE
)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


@dataclass(frozen=True)
class Fork:
    """One project-owned copy and the default it was emitted from."""

    name: str
    copy_path: Path
    default_path: Path
    # Each span runs from `start` up to `end`, both matched as literal headings in the
    # default. `end=None` means "to the end of the file". A span the recipe drops is
    # expressed by ending one span before it and starting the next after it.
    spans: tuple[tuple[str, str | None], ...]
    # Verbatim regions this repo has deliberately ruled differently for its own copy.
    # Each entry is a heading whose section is skipped, with the reason it is skipped.
    # Add entries here rather than loosening the comparison.
    ruled_exceptions: dict[str, str] = field(default_factory=dict)


FORKS = (
    Fork(
        name="ADR conventions",
        copy_path=REPO_ROOT / "docs" / "adr" / "CONVENTIONS.md",
        default_path=PLUGIN_SKILLS / "figure-out" / "references" / "ADR_FORMAT.md",
        spans=(
            (
                "Architecture Decision Records capture",
                "This file is self-contained:",
            ),
            ("## When a decision deserves a record", None),
        ),
    ),
    Fork(
        name="North Star conventions",
        copy_path=REPO_ROOT / "docs" / "NORTH_STAR_CONVENTIONS.md",
        default_path=PLUGIN_SKILLS
        / "init-context"
        / "references"
        / "NORTH_STAR_FORMAT.md",
        spans=(
            ("A North Star is a project's standing", "## Ownership and precedence"),
            ("## Where it lives", "## The project-surfaces section"),
            ("## Produce it honestly", None),
        ),
    ),
)


def _mask_comments(text: str) -> str:
    """Blank out boundary comments, preserving every offset and line break.

    Used when locating a boundary: a comment may legitimately quote the heading it
    marks, and a raw search would find that mention instead of the heading itself.
    """

    def blank(match: re.Match[str]) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    return BOUNDARY_COMMENT.sub(blank, text)


def _strip_boundary_comments(text: str) -> str:
    """Drop the boundary comments the recipe does not copy, and the gap they leave.

    Only boundary comments are removed. Any other HTML comment inside a copied span is
    content a project's copy carries, so removing those would compare two different
    things — and a regex loose enough to match an unpaired ``<!--`` in prose can swallow
    a whole span between it and the next real terminator.
    """
    return re.sub(r"\n{3,}", "\n\n", BOUNDARY_COMMENT.sub("", text))


def _locate(text: str, needle: str, where: Path, after: int = 0) -> int:
    index = _mask_comments(text).find(needle, after)
    if index == -1:
        raise AssertionError(
            f"boundary {needle!r} is missing from {where} at or after offset {after}. A "
            f"boundary is load-bearing: renaming or reordering one silently changes what "
            f"a project's copy should carry. Restore it, or update this test's span table "
            f"and the recipe in init-context/SKILL.md in the same edit."
        )
    return index


def _span_text(default: str, start: str, end: str | None, where: Path) -> str:
    begin = _locate(default, start, where)
    if end is None:
        span = default[begin:]
    else:
        span = default[begin : _locate(default, end, where, begin + len(start))]
    span = span.rstrip() + "\n"
    assert span.strip(), (
        f"the span beginning {start!r} in {where} is empty. Its boundaries are probably "
        f"out of order; an empty span would be compared against nothing and pass."
    )
    return span


def _sections_of(span: str) -> list[tuple[str, str]]:
    """Every part of a span, as (label, text), sliced by position.

    Sections are resolved by offset rather than by name: a heading line can repeat within
    one span — ``ADR_FORMAT.md``'s fenced templates reuse ``## Source``, ``## Status``,
    ``## Context`` and ``## Alternatives Considered`` — and resolving by name compares the
    first occurrence repeatedly while never comparing the later ones at all. Headings
    inside a fenced block are not boundaries, so a fence stays part of its own section,
    and any text above the first heading is carried as its own part rather than dropped.
    """
    offsets: list[tuple[int, str]] = []
    pos = 0
    in_fence = False
    for line in span.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("## "):
            offsets.append((pos, line.rstrip("\n")))
        pos += len(line)

    if not offsets:
        return [(f"the prose beginning {span.strip()[:44]!r}", span)]

    parts: list[tuple[int, int, str]] = []
    if offsets[0][0] > 0:
        parts.append((0, offsets[0][0], f"the prose beginning {span.strip()[:44]!r}"))
    for i, (start, heading) in enumerate(offsets):
        end = offsets[i + 1][0] if i + 1 < len(offsets) else len(span)
        parts.append((start, end, heading))

    return [
        (label, span[start:end].rstrip() + "\n")
        for start, end, label in parts
        if span[start:end].strip()
    ]


def _sections_behind(fork: Fork) -> list[str]:
    default = _strip_boundary_comments(fork.default_path.read_text(encoding="utf-8"))
    copy = _strip_boundary_comments(fork.copy_path.read_text(encoding="utf-8"))
    where = fork.default_path.relative_to(REPO_ROOT)

    behind: list[str] = []
    for start, end in fork.spans:
        expected = _span_text(default, start, end, where)
        for label, section in _sections_of(expected):
            if label in fork.ruled_exceptions:
                continue
            if section not in copy:
                behind.append(label)
    return behind


def test_forks_reproduce_the_emitted_default() -> None:
    report = []
    for fork in FORKS:
        behind = _sections_behind(fork)
        if not behind:
            continue
        listed = "\n".join(f"    {label}" for label in behind)
        report.append(
            f"{fork.copy_path.relative_to(REPO_ROOT)} is behind "
            f"{fork.default_path.relative_to(REPO_ROOT)} in {len(behind)} section(s):\n"
            f"{listed}"
        )

    if report:
        joined = "\n\n".join(report)
        pytest.fail(
            f"{joined}\n\n"
            f"Each copy is a fork: nothing syncs it, so a change to a default only "
            f"reaches the project when someone ports it.\n\n"
            f"Do one of two things for each section listed:\n"
            f"  1. Port it from the default into the copy — and sweep any document the "
            f"copy governs that still speaks the older wording, since a conventions file "
            f"governs the documents written under it.\n"
            f"  2. If this repo means to rule that section differently for itself, add its "
            f"label to that fork's `ruled_exceptions` with the reason.\n"
        )


def test_every_declared_boundary_is_marked_in_the_default() -> None:
    """A span boundary carries a comment, so the recipe and this table cannot drift apart."""
    for fork in FORKS:
        default = fork.default_path.read_text(encoding="utf-8")
        where = fork.default_path.relative_to(REPO_ROOT)
        assert BOUNDARY_COMMENT.findall(default), (
            f"{where} declares span boundaries in this test but carries no fixed-boundary "
            f"comment saying so. A reader editing that file has no way to know a heading "
            f"is load-bearing."
        )
        for start, _ in fork.spans:
            before = default[: _locate(default, start, where)]
            markers = list(BOUNDARY_COMMENT.finditer(before))
            assert markers and not before[markers[-1].end() :].strip(), (
                f"span start {start!r} in {where} has no fixed-boundary comment "
                f"immediately above it. A marker separated from its heading by other "
                f"text is not a marker a reader will connect to it."
            )
