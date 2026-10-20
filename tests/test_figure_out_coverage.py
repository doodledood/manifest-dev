"""Every figure-out probe, trade-off and reference has a row in the eval README's coverage table.

Holds the decision in
docs/adr/20261020-every-figure-out-probe-has-an-eval-grader-or-a-stated-reason.md.

A probe added to a task file with no case is a claim nobody measures: the suite would run and say
nothing about it. Each row names the graders that judge the unit, or a reason the suite cannot
reach it, and a row for a unit that no longer exists points at nothing.
"""

from __future__ import annotations

import re
from pathlib import Path

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


def expected_units(skill: Path) -> set[tuple[str, str]]:
    """Every (file, unit) the table must cover: probes and trade-offs, and reference files."""
    units: set[tuple[str, str]] = set()
    for task in sorted((skill / "tasks").glob("*.md")):
        text = task.read_text(encoding="utf-8")
        name = f"tasks/{task.name}"
        units |= {(name, label) for label in PROBE.findall(_section(text, "Blind-spot probes"))}
        units |= {
            (name, f"Trade-off: {line}")
            for line in TRADE_OFF.findall(_section(text, "Forced trade-offs"))
        }
    units |= {(f"references/{ref.name}", WHOLE_FILE) for ref in (skill / "references").glob("*")}
    return units


def table_rows(readme: Path) -> list[tuple[str, str, str]]:
    """(file, unit, covered-by) for each row of the README's Coverage table."""
    rows = []
    for line in _section(readme.read_text(encoding="utf-8"), "Coverage").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or not line.lstrip().startswith("|"):
            continue
        file, unit, covered = (cell.strip("`") if i < 2 else cell for i, cell in enumerate(cells))
        if file in ("File", "") or set(file) <= {"-", ":", " "}:
            continue
        rows.append((file, unit, covered))
    return rows


def coverage_problems(skill: Path, evals: Path, readme: Path) -> list[str]:
    expected = expected_units(skill)
    rows = table_rows(readme)
    keys = [(file, unit) for file, unit, _ in rows]
    problems = [f"no row for {file} · {unit}" for file, unit in sorted(expected - set(keys))]
    problems += [
        f"row for {file} · {unit}, which no longer exists"
        for file, unit in sorted(set(keys) - expected)
        if file != SKILL_FILE
    ]
    problems += [f"duplicate row for {k[0]} · {k[1]}" for k in sorted({k for k in keys if keys.count(k) > 1})]
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
            problems.append(f"{where}: only display-only graders, which are never scored")
    return problems


def test_every_figure_out_unit_has_a_coverage_row() -> None:
    problems = coverage_problems(FIGURE_OUT, EVALS, README)
    assert not problems, "coverage table out of step:\n" + "\n".join(problems)


def test_coverage_check_catches_each_break(tmp_path: Path) -> None:
    # The lock is trusted only after it is seen failing on each break it exists to catch.
    skill, evals = tmp_path / "skill", tmp_path / "evals"
    (skill / "tasks").mkdir(parents=True)
    (skill / "references").mkdir()
    (skill / "tasks/X.md").write_text(
        "## Blind-spot probes\n- **One** — q?\n\n## Forced trade-offs\n- A vs B — which?\n",
        encoding="utf-8",
    )
    (skill / "references/R.md").write_text("r\n", encoding="utf-8")
    (evals / "01-c/graders").mkdir(parents=True)
    (evals / "01-c/graders/g.md").write_text("g\n", encoding="utf-8")
    (evals / "01-c/graders/skill-fired.md").write_text("g\n", encoding="utf-8")
    readme = evals / "README.md"
    good = (
        "## Coverage\n\n| File | Unit | Covered by |\n|---|---|---|\n"
        "| `tasks/X.md` | One | `01-c/g` |\n"
        "| `tasks/X.md` | Trade-off: A vs B | `01-c/g` |\n"
        "| `references/R.md` | (whole file) | Reason: needs a service the suite cannot reach |\n"
        "| `SKILL.md` | The log | `01-c/g` |\n\n## Next\n"
    )
    readme.write_text(good, encoding="utf-8")
    assert coverage_problems(skill, evals, readme) == []

    def problems_after(edit: str, path: Path, text: str) -> list[str]:
        original = path.read_text(encoding="utf-8") if path.exists() else None
        path.write_text(text if edit == "write" else original + text, encoding="utf-8")
        try:
            return coverage_problems(skill, evals, readme)
        finally:
            if original is None:
                path.unlink()
            else:
                path.write_text(original, encoding="utf-8")

    assert any("Two" in p for p in problems_after("append", skill / "tasks/X.md", "- **Two** — q?\n"))
    tasks = skill / "tasks/X.md"
    with_trade_off = tasks.read_text(encoding="utf-8") + "- C vs D — which?\n"
    assert any("C vs D" in p for p in problems_after("write", tasks, with_trade_off))
    assert any("S.md" in p for p in problems_after("write", skill / "references/S.md", "s\n"))
    assert any("01-x/g" in p for p in problems_after("write", readme, good.replace("`01-c/g` |\n| `tasks/X.md` | Trade", "`01-x/g` |\n| `tasks/X.md` | Trade")))
    assert any("no longer exists" in p for p in problems_after("write", readme, good.replace("| Unit | Covered by |\n|---|---|---|\n", "| Unit | Covered by |\n|---|---|---|\n| `tasks/X.md` | Gone | `01-c/g` |\n")))
    assert any("display-only" in p for p in problems_after("write", readme, good.replace("| `SKILL.md` | The log | `01-c/g` |", "| `SKILL.md` | The log | `01-c/skill-fired` |")))
