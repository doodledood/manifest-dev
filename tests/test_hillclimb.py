"""Hill-climbing runs through figure-out, define and do, and its defaults stay where they were set.

Each test cites the decision record it holds. A climb has no runtime machinery, so what a climb
does lives in the shipped prose: these checks fail when that prose drops or reverses a decided
default, or when the pieces that carry it stop pointing at each other.
"""

from __future__ import annotations

import re
from pathlib import Path

from tests.prose import flat, flat_file

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "claude-plugins/manifest-dev/skills"
DEFINE = CORE / "define"
FIGURE_OUT = CORE / "figure-out"
COMMAND = ROOT / "claude-plugins/manifest-dev-tools/skills/hillclimb/SKILL.md"
PI_TEMPLATE = ROOT / "dist/pi/prompts/hillclimb.md"
CLIMB = DEFINE / "tasks/HILLCLIMB.md"
PROBES = FIGURE_OUT / "tasks/HILLCLIMB.md"


def _section(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match, f"{path.name} has no ## {heading} section"
    return match.group(1)


def _gate_row(aspect: str) -> str:
    section = _section(CLIMB, "Quality Gates")
    for line in section.splitlines():
        if line.startswith(f"| {aspect} |"):
            return flat(line)
    raise AssertionError(f"{CLIMB.name} has no Quality Gates row for {aspect!r}")


def _bullet(path: Path, heading: str, label: str) -> str:
    section = _section(path, heading)
    match = re.search(
        rf"(?:^|\n)(- \*\*{re.escape(label)}\*\*.*?)(?=\n- |\n\n|\Z)",
        section,
        re.DOTALL,
    )
    assert match, f"{path.name} ## {heading} has no bullet for {label!r}"
    return flat(match.group(1))


# Holds docs/adr/20261106-hill-climbing-runs-through-figure-out-define-and-do.md and
# docs/adr/20261107-climb-guidance-states-outcomes-and-rulings-not-steps.md: the command routes
# to figure-out, define and do and restates no climb rule, since a climb asked through any other
# entry point never reads it.
def test_command_routes_and_restates_no_climb_rule() -> None:
    body = flat_file(COMMAND).split("---", 2)[2]
    for skill in ("figure-out", "define", "do"):
        assert f"`{skill}`" in body, f"hillclimb no longer hands off to {skill}"
    assert "holds no loop of its own" in body
    assert "`figure-out --autonomous`" in body and "`define --autonomous`" in body
    for rule in ("quick", "thorough", "judge", "round", "candidate"):
        assert rule not in body.lower(), f"the command restates a climb rule: {rule!r}"
    assert "Use the hillclimb skill with: $ARGUMENTS" in flat_file(PI_TEMPLATE)


# Holds docs/adr/20261106-hill-climbing-runs-through-figure-out-define-and-do.md, and partly
# docs/adr/20260604-figure-out-owns-domain-probing-via-mirrored-task-files.md.
def test_each_climb_and_measure_file_has_its_mirror_and_composes_onto_measure() -> None:
    for name in ("HILLCLIMB.md", "MEASURE.md", "PERF.md"):
        assert (DEFINE / "tasks" / name).is_file(), f"define/tasks/{name} missing"
        assert (
            FIGURE_OUT / "tasks" / name
        ).is_file(), f"figure-out/tasks/{name} missing"
    for skill in (DEFINE, FIGURE_OUT):
        for name in ("HILLCLIMB.md", "PERF.md"):
            assert "`MEASURE.md`" in flat_file(
                skill / "tasks" / name
            ), f"{skill.name}/tasks/{name} no longer composes onto MEASURE.md"
        index = flat_file(skill / "SKILL.md")
        for name in ("MEASURE.md", "HILLCLIMB.md"):
            assert f"`{name}`" in index, f"{skill.name}'s task index omits {name}"


# Holds docs/adr/20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters.md.
def test_a_climb_is_quick_by_default_and_autonomy_does_not_make_it_thorough() -> None:
    climb = flat_file(CLIMB)
    assert "A climb is **quick** by default" in climb
    assert "a long run or one that keeps running unattended" in climb
    assert "Running unattended does not by itself make a climb thorough" in climb
    assert "judged by what it is for, not by how easily its commits revert" in climb
    assert (
        "The Manifest's Initial Approach opens with one line saying which and why"
        in climb
    )
    assert "a quick one asks only what it cannot infer" in climb


# Holds docs/adr/20261106-a-climb-designs-its-measure-and-search-for-its-task.md.
def test_how_a_round_tries_changes_follows_the_cost_of_measuring() -> None:
    try_changes = _bullet(
        CLIMB, "Defaults", "Try changes the way the cost of measuring allows"
    )
    assert "each round tries three candidates, at least one bold" in try_changes
    assert "each round makes one change aimed at a diagnosed cause" in try_changes
    assert _gate_row("Measure shown good")
    assert (
        "A cheap stand-in for a slow measure screens versions only after it catches"
        in _gate_row("Confirmed gains")
    )
    one_primary = _bullet(CLIMB, "Defaults", "One primary, the rest guards")
    assert "Never invent weights" in one_primary
    assert _bullet(CLIMB, "Defaults", "A behavior goal climbs offline first")


# Holds docs/adr/20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record.md.
def test_stop_rule_defaults_and_rerun_continue_the_record() -> None:
    stop_rule = _gate_row("Stop rule")
    assert (
        "two rounds in a row bring no confirmed gain in a thorough climb, one in a quick climb"
        in stop_rule
    )
    assert "The last round before stopping includes a bold attempt" in stop_rule
    assert (
        "A re-run continues the earlier record and proposes nothing it rejected"
        in stop_rule
    )
    assert (
        "with the raw evidence of why each lost rather than only its score" in stop_rule
    )
    assert "When nothing beats the original, the climb keeps it" in _gate_row(
        "Final comparison"
    )
    next_round = _bullet(PROBES, "Blind-spot probes", "What the next round sees")
    assert "raw evidence" in next_round and "why the last versions lost" in next_round


# Holds docs/adr/20261106-a-climb-runs-without-a-person-choosing-by-default.md.
def test_a_climb_pushes_only_when_asked_and_its_numbers_are_defaults() -> None:
    push = _bullet(CLIMB, "Defaults", "Push only when asked")
    assert "carries no pull-request gate otherwise" in push
    assert _bullet(CLIMB, "Defaults", "Every number here is a default")
    assert "can relax it" in _gate_row("No win by misleading")
    assert "A thorough climb settles with an attended requester" in flat_file(CLIMB)
    assert "asks at the end whether to push" in flat_file(COMMAND)


# Holds docs/adr/20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own.md
# and docs/adr/20261107-climb-guidance-states-outcomes-and-rulings-not-steps.md: the judge's proof
# is an outcome in the task file, and no judge reference ships.
def test_the_judge_is_proven_sees_no_examples_and_ships_no_reference() -> None:
    measure = _gate_row("Measure shown good")
    assert "an AI judge comparing two versions" in measure
    assert "An AI judge is shown no example version to imitate" in measure
    assert "prefers the original over a version made clearly worse" in measure
    assert (
        "ties identical versions and keeps its verdict when the two swap places"
        in measure
    )
    assert _bullet(CLIMB, "Defaults", "Extra judge guards stay off until needed")
    assert not (
        DEFINE / "tasks/references"
    ).exists(), "a define judge reference returned"
