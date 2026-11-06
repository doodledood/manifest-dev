"""The hill-climb recipe's fixtures still set up the situation each scenario depends on.

A climb fixture is exercised only by a paid, ask-first drive, so a fixture that stops working —
a scaffold that fails, tests that no longer pass on the starting code, a planted flaw that no
longer shows — would otherwise surface only after a run was paid for. These checks run each
scaffold the way the drive does and read the property each scenario rests on.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "verification/fixtures"
CLIMB_FIXTURES = sorted(p for p in FIXTURES.glob("climb-*") if p.is_dir())
WITH_TESTS = ("climb-number", "climb-at-best", "climb-noisy-measure", "climb-slow-sim")


def _scaffold(name: str, where: Path, home: Path) -> Path:
    project = where / name
    project.mkdir()
    # As scripts/native_drive.py does: a fresh git repository, then the scaffold with HOME isolated.
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    env = {
        **os.environ,
        "DRIVE_CHECKOUT": str(ROOT),
        "HOME": str(home),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    result = subprocess.run(
        ["bash", str(FIXTURES / name / "scaffold.sh")],
        cwd=project,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return project


def _python(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args], cwd=project, capture_output=True, text=True
    )


# Holds verification/recipes/hillclimb.md: every scenario starts from its fixture's scaffold.
@pytest.mark.parametrize("fixture", CLIMB_FIXTURES, ids=lambda p: p.name)
def test_each_scaffold_runs_and_leaves_home_alone(
    fixture: Path, tmp_path: Path
) -> None:
    home = tmp_path / "home"
    home.mkdir()
    _scaffold(fixture.name, tmp_path, home)
    assert not any(home.iterdir()), f"{fixture.name}'s scaffold wrote to HOME"


@pytest.mark.parametrize("name", WITH_TESTS)
def test_the_starting_code_passes_its_own_tests(name: str, tmp_path: Path) -> None:
    project = _scaffold(name, tmp_path, tmp_path)
    result = _python(project, "-m", "pytest", "-q", "-p", "no:cacheprovider")
    assert result.returncode == 0, result.stdout + result.stderr


def test_signup_results_carries_two_distinct_leading_versions(tmp_path: Path) -> None:
    # The scenario asks the climb to tell b (a confirmed gain) from c (none); identical pages
    # would make that a coin toss.
    project = _scaffold("climb-signup-results", tmp_path, tmp_path)
    original = (project / "index.html").read_text(encoding="utf-8")
    b = (project / "versions/b.html").read_text(encoding="utf-8")
    c = (project / "versions/c.html").read_text(encoding="utf-8")
    assert b != original and c != b
    assert "14 days free, no card needed" in b and "How it works" in c
    # The notes the page fixture carries must not deny the test the results come from.
    notes = (project / "NOTES.md").read_text(encoding="utf-8")
    assert "never run an A/B test" not in notes and "ab-results.md" in notes


def test_slow_sim_quick_check_passes_the_original_and_misses_motion(
    tmp_path: Path,
) -> None:
    # The quick check reads one still frame, so it passes the original; the scenario rests on it
    # also passing versions that move badly, which only the full measure catches.
    project = _scaffold("climb-slow-sim", tmp_path, tmp_path)
    result = _python(project, "-m", "measure.quick_check")
    assert "quick_check=PASS" in result.stdout, result.stdout + result.stderr
    probe = (
        "import measure.full as f\n"
        "f.SECONDS = 120\n"
        "print(f.score_run('grid', 1)[0])\n"
    )
    original = float(_python(project, "-c", probe).stdout.strip())
    world = project / "sim/world.py"
    text = world.read_text(encoding="utf-8")
    anchor = "            follow(car, gap, lead_speed, DT)\n"
    assert text.count(anchor) == 1
    world.write_text(
        text.replace(
            anchor,
            anchor + "            car.v = 0.0 if int(self.time * 30) % 2 else car.v\n",
        ),
        encoding="utf-8",
    )
    jittery = _python(project, "-m", "measure.quick_check")
    assert "quick_check=PASS" in jittery.stdout, jittery.stdout + jittery.stderr
    full = _python(project, "-c", probe)
    assert float(full.stdout.strip()) < original / 2, full.stdout + full.stderr


def test_slow_sim_scores_a_car_that_never_merges_as_zero(tmp_path: Path) -> None:
    # Dropping the merge removes the one-frame lane jump; it must not read as a realism gain.
    project = _scaffold("climb-slow-sim", tmp_path, tmp_path)
    world = project / "sim/world.py"
    text = world.read_text(encoding="utf-8")
    anchor = "                    car.lane = 0  # moves across in one frame\n"
    assert text.count(anchor) == 1
    world.write_text(
        text.replace(anchor, "                    continue\n"), encoding="utf-8"
    )
    probe = (
        "import measure.full as f\n"
        "f.SECONDS = 120\n"
        "print(f.score_run('highway_merge', 1)[0])\n"
    )
    result = _python(project, "-c", probe)
    assert float(result.stdout.strip()) == 0.0, result.stdout + result.stderr
    tests = _python(project, "-m", "pytest", "-q", "-p", "no:cacheprovider")
    assert tests.returncode != 0, "the merge test passed a version that never merges"
