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
JUDGE = DEFINE / "tasks/references/AI_JUDGE.md"


def _text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


# Holds docs/adr/20261106-hill-climbing-runs-through-figure-out-define-and-do.md.
def test_command_hands_the_climb_to_figure_out_define_and_do() -> None:
    body = _text(COMMAND).split("---", 2)[2]
    for skill in ("figure-out", "define", "do"):
        assert f"`{skill}`" in body, f"hillclimb no longer hands off to {skill}"
    assert "holds no loop of its own" in body
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
    climb = _text(DEFINE / "tasks/HILLCLIMB.md")
    assert "A climb is **quick** by default" in climb
    assert "Running unattended does not by itself make a climb thorough" in climb
    assert "The Manifest's Initial Approach opens with one line" in climb
    assert "or the original kept with the evidence that nothing tried beat it" in climb
    command = _text(COMMAND)
    assert "`--autonomous` alone does not make a climb thorough" in command
    assert "ask the requester only when the goal cannot be inferred" in command


# Holds docs/adr/20261106-a-climb-designs-its-measure-and-search-for-its-task.md.
def test_how_a_round_tries_changes_follows_the_cost_of_measuring() -> None:
    climb = _text(DEFINE / "tasks/HILLCLIMB.md")
    assert "Try changes the way the cost of measuring allows" in climb
    assert "each round tries three candidates, at least one departing boldly" in climb
    assert "each round makes one change aimed at a cause diagnosed" in climb
    assert "change the part whose gap matters most" in climb
    assert "| Staged measure |" in climb
    assert "under each condition the record names" in climb
    assert "| Measure shown good |" in climb


# Holds docs/adr/20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record.md.
def test_stop_rule_defaults_and_rerun_continue_the_record() -> None:
    climb = _text(DEFINE / "tasks/HILLCLIMB.md")
    assert (
        "two rounds in a row with no confirmed gain in a thorough climb, one in a quick climb"
        in climb
    )
    assert "The round that would meet the stop rule includes a bold attempt" in climb
    assert "with nothing new to try stops before proposing" in climb
    assert "Past 50 lines, roll older losing attempts into one line per round" in climb


# Holds docs/adr/20261106-a-climb-runs-without-a-person-choosing-by-default.md.
def test_a_climb_pushes_only_when_asked_and_its_numbers_are_defaults() -> None:
    climb = _text(DEFINE / "tasks/HILLCLIMB.md")
    assert "**Push only when asked**" in climb
    assert "carries no pull-request gate otherwise" in climb
    assert "**Every number here is a default**" in climb
    assert "No win by misleading" in climb and "can relax it" in climb


# Holds docs/adr/20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own.md.
def test_the_judge_decides_between_versions_sees_no_examples_and_keeps_guards_off() -> (
    None
):
    judge = _text(JUDGE)
    assert "A verdict between two versions" in judge
    assert "The judge is shown no example version" in judge
    assert "Prove the judge on the model the climb runs" in judge
    assert "They are off by default" in judge
    assert "Every comparison, in either, judges both orders" in judge
    assert "Votes run to the minimum the proof set" in judge
    assert "Protected parts are never left to the judge" in judge
    assert "never from the judge's own words" in judge
    assert "`references/AI_JUDGE.md`" in _text(DEFINE / "tasks/HILLCLIMB.md")
