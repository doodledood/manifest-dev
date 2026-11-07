"""Hill-climbing runs through figure-out, define and do, and its defaults stay where they were set.

Each test cites the decision record it holds. A climb has no runtime machinery, so what a climb
does lives in the shipped prose: these checks fail when that prose drops or reverses a decided
default, or when the pieces that carry it stop pointing at each other.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "claude-plugins/manifest-dev/skills"
DEFINE = CORE / "define"
FIGURE_OUT = CORE / "figure-out"
COMMAND = ROOT / "claude-plugins/manifest-dev-tools/skills/hillclimb/SKILL.md"
PI_TEMPLATE = ROOT / "dist/pi/prompts/hillclimb.md"
CLIMB = DEFINE / "tasks/HILLCLIMB.md"


def _text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


# Holds docs/adr/20261106-hill-climbing-runs-through-figure-out-define-and-do.md and
# docs/adr/20261107-climb-guidance-states-outcomes-and-rulings-not-steps.md: the command routes
# to figure-out, define and do and restates no climb rule, since a climb asked through any other
# entry point never reads it.
def test_command_routes_and_restates_no_climb_rule() -> None:
    body = _text(COMMAND).split("---", 2)[2]
    for skill in ("figure-out", "define", "do"):
        assert f"`{skill}`" in body, f"hillclimb no longer hands off to {skill}"
    assert "holds no loop of its own" in body
    assert "`figure-out --autonomous`" in body and "`define --autonomous`" in body
    for rule in ("quick", "thorough", "judge", "round", "candidate"):
        assert rule not in body.lower(), f"the command restates a climb rule: {rule!r}"
    assert "Use the hillclimb skill with: $ARGUMENTS" in _text(PI_TEMPLATE)


# Holds docs/adr/20261106-hill-climbing-runs-through-figure-out-define-and-do.md.
def test_each_climb_and_measure_file_has_its_mirror_and_composes_onto_measure() -> None:
    for name in ("HILLCLIMB.md", "MEASURE.md", "PERF.md"):
        assert (DEFINE / "tasks" / name).is_file(), f"define/tasks/{name} missing"
        assert (
            FIGURE_OUT / "tasks" / name
        ).is_file(), f"figure-out/tasks/{name} missing"
    for skill in (DEFINE, FIGURE_OUT):
        for name in ("HILLCLIMB.md", "PERF.md"):
            assert "`MEASURE.md`" in _text(
                skill / "tasks" / name
            ), f"{skill.name}/tasks/{name} no longer composes onto MEASURE.md"
        index = _text(skill / "SKILL.md")
        for name in ("MEASURE.md", "HILLCLIMB.md"):
            assert f"`{name}`" in index, f"{skill.name}'s task index omits {name}"


# Holds docs/adr/20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters.md.
def test_a_climb_is_quick_by_default_and_autonomy_does_not_make_it_thorough() -> None:
    climb = _text(CLIMB)
    assert "A climb is **quick** by default" in climb
    assert "Running unattended does not by itself make a climb thorough" in climb
    assert "judged by what it is for, not by how easily its commits revert" in climb
    assert (
        "The Manifest's Initial Approach opens with one line saying which and why"
        in climb
    )
    assert "a quick one asks only what it cannot infer" in climb


# Holds docs/adr/20261106-a-climb-designs-its-measure-and-search-for-its-task.md.
def test_how_a_round_tries_changes_follows_the_cost_of_measuring() -> None:
    climb = _text(CLIMB)
    assert "Try changes the way the cost of measuring allows" in climb
    assert "each round tries three candidates, at least one bold" in climb
    assert "each round makes one change aimed at a diagnosed cause" in climb
    assert "| Measure shown good |" in climb
    assert (
        "A cheap stand-in for a slow measure screens versions only after it catches"
        in climb
    )
    assert (
        "**One primary, the rest guards**" in climb and "Never invent weights" in climb
    )
    assert "**A behavior goal climbs offline first**" in climb


# Holds docs/adr/20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record.md.
def test_stop_rule_defaults_and_rerun_continue_the_record() -> None:
    climb = _text(CLIMB)
    assert (
        "two rounds in a row bring no confirmed gain in a thorough climb, one in a quick climb"
        in climb
    )
    assert "The last round before stopping includes a bold attempt" in climb
    assert (
        "A re-run continues the earlier record and proposes nothing it rejected"
        in climb
    )
    assert "When nothing beats the original, the climb keeps it" in climb
    assert "with the raw evidence of why each lost rather than only its score" in climb
    probes = _text(FIGURE_OUT / "tasks/HILLCLIMB.md")
    assert "**What the next round sees**" in probes


# Holds docs/adr/20261106-a-climb-runs-without-a-person-choosing-by-default.md.
def test_a_climb_pushes_only_when_asked_and_its_numbers_are_defaults() -> None:
    climb = _text(CLIMB)
    assert "**Push only when asked**" in climb
    assert "carries no pull-request gate otherwise" in climb
    assert "**Every number here is a default**" in climb
    assert "No win by misleading" in climb and "can relax it" in climb
    assert "A thorough climb settles with an attended requester" in climb
    assert "asks at the end whether to push" in _text(COMMAND)


# Holds docs/adr/20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own.md
# and docs/adr/20261107-climb-guidance-states-outcomes-and-rulings-not-steps.md: the judge's proof
# is an outcome in the task file, and no judge reference ships.
def test_the_judge_is_proven_sees_no_examples_and_ships_no_reference() -> None:
    climb = _text(CLIMB)
    assert "an AI judge comparing two versions" in climb
    assert "An AI judge is shown no example version to imitate" in climb
    assert "prefers the original over a version made clearly worse" in climb
    assert (
        "ties identical versions and keeps its verdict when the two swap places"
        in climb
    )
    assert "**Extra judge guards stay off until needed**" in climb
    assert not (
        DEFINE / "tasks/references"
    ).exists(), "a define judge reference returned"
