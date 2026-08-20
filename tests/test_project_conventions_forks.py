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


def _strip_comments(text: str) -> str:
    """Drop HTML comments; the recipe does not copy them into a project's file."""
    return HTML_COMMENT.sub("", text)


def _section_of(text: str, heading: str) -> str:
    """The heading and its body, up to the next same-level heading or end of file."""
    start = text.index(heading)
    nxt = text.find("\n## ", start + len(heading))
    return text[start:] if nxt == -1 else text[start:nxt]


def _span_text(default: str, start: str, end: str | None) -> str:
    if start not in default:
        raise AssertionError(
            f"boundary heading {start!r} is missing from the default. A boundary heading "
            f"is load-bearing: renaming one silently changes what a project's copy should "
            f"carry. Restore it, or update this test's span table and the recipe in "
            f"init-context/SKILL.md in the same edit."
        )
    begin = default.index(start)
    if end is None:
        return default[begin:].rstrip() + "\n"
    if end not in default:
        raise AssertionError(f"boundary heading {end!r} is missing from the default.")
    return default[begin : default.index(end)].rstrip() + "\n"


def _sections_behind(fork: Fork) -> list[str]:
    default = _strip_comments(fork.default_path.read_text(encoding="utf-8"))
    copy = _strip_comments(fork.copy_path.read_text(encoding="utf-8"))

    behind: list[str] = []
    for start, end in fork.spans:
        expected = _span_text(default, start, end)
        headings = _headings_in(expected)
        if not headings:
            # Framing prose the recipe carries verbatim but that sits under no heading of
            # its own; there is nothing to compare section by section, so compare it whole.
            if expected.strip() not in copy:
                behind.append(f"the framing prose beginning {start[:44]!r}")
            continue
        for heading in headings:
            if heading in fork.ruled_exceptions:
                continue
            section = _section_of(expected, heading).rstrip() + "\n"
            if section not in copy:
                behind.append(heading)
    return behind


def test_forks_reproduce_the_emitted_default() -> None:
    report = []
    for fork in FORKS:
        behind = _sections_behind(fork)
        if not behind:
            continue
        listed = "\n".join(f"    {heading}" for heading in behind)
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
            f"heading to that fork's `ruled_exceptions` with the reason.\n"
        )


def _headings_in(span: str) -> list[str]:
    return [line for line in span.splitlines() if line.startswith("## ")]


def test_every_declared_boundary_is_marked_in_the_default() -> None:
    """A span boundary carries a comment, so the recipe and this table cannot drift apart."""
    for fork in FORKS:
        default = fork.default_path.read_text(encoding="utf-8")
        assert BOUNDARY_COMMENT.findall(default), (
            f"{fork.default_path.relative_to(REPO_ROOT)} declares span boundaries in this "
            f"test but carries no fixed-boundary comment saying so. A reader editing that "
            f"file has no way to know a heading is load-bearing."
        )
        for start, _ in fork.spans:
            before = default[: default.index(start)]
            assert BOUNDARY_COMMENT.search(before[-600:]), (
                f"span start {start!r} in "
                f"{fork.default_path.relative_to(REPO_ROOT)} has no fixed-boundary "
                f"comment immediately above it."
            )
