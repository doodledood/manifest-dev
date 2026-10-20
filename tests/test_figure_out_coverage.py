"""Every figure-out probe, trade-off and reference has a row in the eval README's coverage table.

Holds the decision in
docs/adr/20261020-every-figure-out-probe-has-an-eval-grader-or-a-stated-reason.md.

A probe added to a task file with no case is a claim nobody measures: the suite would run and say
nothing about it. Each row names the graders that judge the unit, or a reason the suite cannot
reach it, and a row for a unit that no longer exists points at nothing.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIGURE_OUT = ROOT / "claude-plugins/manifest-dev/skills/figure-out"
EVALS = ROOT / "claude-plugins/manifest-dev/evals"
README = EVALS / "README.md"

# Shown in a run's report but never scored, so they cannot stand for a unit on their own.
DISPLAY_ONLY = {"skill-fired", "autonomous-flag-passed"}
PROBE = re.compile(r"^- \*\*(.+?)\*\*", re.MULTILINE)
TRADE_OFF = re.compile(r"^- (.+?) — ", re.MULTILINE)
GRADER_REF = re.compile(r"`([^`/]+)/([^`/]+)`")
SKILL_FILE = "SKILL.md"
WHOLE_FILE = "(whole file)"


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


def _files(folder: Path, suffix: str = "") -> list[Path]:
    # Editor swap files, lock links and .DS_Store sit beside real files and are never units.
    return sorted(
        f
        for f in folder.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name.endswith(suffix)
    )


def expected_units(skill: Path) -> set[tuple[str, str]]:
    """Every (file, unit) the table must cover: probes and trade-offs, and reference files."""
    units: set[tuple[str, str]] = set()
    for task in _files(skill / "tasks", ".md"):
        text = task.read_text(encoding="utf-8")
        name = f"tasks/{task.name}"
        units |= {
            (name, label)
            for label in PROBE.findall(_section(text, "Blind-spot probes"))
        }
        units |= {
            (name, f"Trade-off: {line}")
            for line in TRADE_OFF.findall(_section(text, "Forced trade-offs"))
        }
    units |= {
        (f"references/{ref.name}", WHOLE_FILE) for ref in _files(skill / "references")
    }
    return units


def table_rows(readme: Path) -> list[tuple[str, str, str]]:
    """(file, unit, covered-by) for each row of the README's Coverage table."""
    rows = []
    for line in _section(readme.read_text(encoding="utf-8"), "Coverage").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or not line.lstrip().startswith("|"):
            continue
        file, unit, covered = (
            cell.strip("`") if i < 2 else cell for i, cell in enumerate(cells)
        )
        if file in ("File", "") or set(file) <= {"-", ":", " "}:
            continue
        rows.append((file, unit, covered))
    return rows


def coverage_problems(skill: Path, evals: Path, readme: Path) -> list[str]:
    expected = expected_units(skill)
    rows = table_rows(readme)
    keys = [(file, unit) for file, unit, _ in rows]
    problems = [
        f"no row for {file} · {unit}" for file, unit in sorted(expected - set(keys))
    ]
    problems += [
        f"row for {file} · {unit}, which no longer exists"
        for file, unit in sorted(set(keys) - expected)
        if file != SKILL_FILE
    ]
    problems += [
        f"duplicate row for {k[0]} · {k[1]}"
        for k in sorted({k for k in keys if keys.count(k) > 1})
    ]
    for file, unit, covered in rows:
        where = f"{file} · {unit}"
        if covered.startswith("Reason:"):
            if len(covered) <= len("Reason:") + 10:
                problems.append(f"{where}: reason too short to check")
            continue
        refs = GRADER_REF.findall(covered)
        if not refs:
            problems.append(f"{where}: names no `case/grader` and gives no Reason:")
            continue
        for case, grader in refs:
            if not (evals / case / "graders" / f"{grader}.md").is_file():
                problems.append(f"{where}: {case}/{grader} does not exist")
        if all(grader in DISPLAY_ONLY for _, grader in refs):
            problems.append(
                f"{where}: only display-only graders, which are never scored"
            )
    return problems


def test_every_figure_out_unit_has_a_coverage_row() -> None:
    problems = coverage_problems(FIGURE_OUT, EVALS, README)
    assert not problems, "coverage table out of step:\n" + "\n".join(problems)


GOOD_TABLE = (
    "## Coverage\n\n| File | Unit | Covered by |\n|---|---|---|\n"
    "| `tasks/X.md` | One | `01-c/g` |\n"
    "| `tasks/X.md` | Trade-off: A vs B | `01-c/g` |\n"
    "| `references/R.md` | (whole file) | Reason: needs a service the suite cannot reach |\n"
    "| `SKILL.md` | The log | `01-c/g` |\n\n## Next\n"
)


def _fixture(root: Path) -> tuple[Path, Path, Path]:
    skill, evals = root / "skill", root / "evals"
    (skill / "tasks").mkdir(parents=True)
    (skill / "references").mkdir()
    (skill / "tasks/X.md").write_text(
        "## Blind-spot probes\n- **One** — q?\n\n## Forced trade-offs\n- A vs B — which?\n",
        encoding="utf-8",
    )
    (skill / "references/R.md").write_text("r\n", encoding="utf-8")
    (evals / "01-c/graders").mkdir(parents=True)
    for grader in ("g", "skill-fired"):
        (evals / f"01-c/graders/{grader}.md").write_text("g\n", encoding="utf-8")
    readme = evals / "README.md"
    readme.write_text(GOOD_TABLE, encoding="utf-8")
    return skill, evals, readme


def _append(path: Path, text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def _after(path: Path, anchor: str, text: str) -> None:
    body = path.read_text(encoding="utf-8")
    path.write_text(body.replace(anchor, anchor + text, 1), encoding="utf-8")


def _edit_table(readme: Path, old: str, new: str) -> None:
    readme.write_text(GOOD_TABLE.replace(old, new), encoding="utf-8")


# Each break a contributor could make, and the text the failure message must carry to name it.
BREAKS: dict[str, tuple[Callable[[Path, Path, Path], object], str]] = {
    "new probe": (
        lambda s, e, r: _after(
            s / "tasks/X.md", "- **One** — q?\n", "- **Two** — q?\n"
        ),
        "no row for tasks/X.md · Two",
    ),
    "new trade-off": (
        lambda s, e, r: _append(s / "tasks/X.md", "- C vs D — which?\n"),
        "C vs D",
    ),
    "new reference": (
        lambda s, e, r: (s / "references/S.md").write_text("s\n", encoding="utf-8"),
        "references/S.md",
    ),
    "renamed case": (
        lambda s, e, r: (e / "01-c").rename(e / "01-x"),
        "01-c/g does not exist",
    ),
    "stale row": (
        lambda s, e, r: _edit_table(r, "| One |", "| Gone |"),
        "tasks/X.md · Gone, which no longer exists",
    ),
    "display-only row": (
        lambda s, e, r: _edit_table(
            r, "| The log | `01-c/g` |", "| The log | `01-c/skill-fired` |"
        ),
        "only display-only graders",
    ),
    "duplicate row": (
        lambda s, e, r: _edit_table(
            r, "| `SKILL.md` |", "| `tasks/X.md` | One | `01-c/g` |\n| `SKILL.md` |"
        ),
        "duplicate row for tasks/X.md · One",
    ),
    "plain-text cell": (
        lambda s, e, r: _edit_table(
            r, "| The log | `01-c/g` |", "| The log | see above |"
        ),
        "names no `case/grader`",
    ),
    "empty reason": (
        lambda s, e, r: _edit_table(
            r, "Reason: needs a service the suite cannot reach", "Reason:"
        ),
        "reason too short",
    ),
}


def test_coverage_check_passes_a_sound_table(tmp_path: Path) -> None:
    assert coverage_problems(*_fixture(tmp_path)) == []


def test_coverage_check_ignores_hidden_files(tmp_path: Path) -> None:
    skill, evals, readme = _fixture(tmp_path)
    (skill / "references/.R.md.swp").write_text("x\n", encoding="utf-8")
    (skill / "tasks/.#X.md").symlink_to(tmp_path / "gone")
    assert coverage_problems(skill, evals, readme) == []


@pytest.mark.parametrize("name", sorted(BREAKS))
def test_coverage_check_catches_each_break(tmp_path: Path, name: str) -> None:
    # The lock is trusted only after it is seen failing on each break it exists to catch.
    skill, evals, readme = _fixture(tmp_path)
    breaking, expected = BREAKS[name]
    breaking(skill, evals, readme)
    problems = coverage_problems(skill, evals, readme)
    assert any(expected in problem for problem in problems), problems
