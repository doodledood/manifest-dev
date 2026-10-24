"""Eval fixtures and final-state graders discriminate real outcomes, not tool names."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "claude-plugins/manifest-dev/evals"


def scaffold(case: str, tmp_path: Path) -> Path:
    work, home = tmp_path / "work", tmp_path / "home"
    work.mkdir()
    home.mkdir()
    subprocess.run(
        ["bash", str(EVALS / case / "scaffold.sh")],
        cwd=work,
        env={**os.environ, "HOME": str(home)},
        capture_output=True,
        check=True,
    )
    return work


def regex_passes(grader: Path, evidence: str) -> bool:
    config = yaml.safe_load(grader.read_text().split("---\n", 2)[1])
    result = subprocess.run(
        [
            "node",
            "-e",
            "const [c,s]=JSON.parse(require('fs').readFileSync(0,'utf8'));"
            "process.stdout.write(String(new RegExp(c.pattern,c.flags||'').test(s)));",
        ],
        input=json.dumps([config, evidence]),
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout == "true"


@pytest.mark.parametrize(
    "case",
    [
        "17-agreement-is-not-a-go",
        "18-read-only-experiment",
        "25-users-call-and-taste",
        "27-taste-offers",
        "28-universal-not-taste",
        "52-projectless-chat-offers-no-surfaces",
        "define/d16-approved-means-handoff",
        "define/d17-taste-in-encoding",
    ],
)
def test_final_state_checks_reject_shell_edits_and_added_files(
    case: str, tmp_path: Path
) -> None:
    work = scaffold(case, tmp_path)
    graders = EVALS / case / "graders"
    snapshots = sorted(graders.glob("state-*.md"))
    assert len(snapshots) > 1
    for grader in snapshots:
        config = yaml.safe_load(grader.read_text().split("---\n", 2)[1])
        if config["target"] == "files":
            assert regex_passes(grader, "")
            assert not regex_passes(grader, "hidden-change.py")
            if case.startswith("define/"):
                assert regex_passes(grader, "manifest.md")
                assert not regex_passes(grader, "manifest.md\nother.py")
            continue
        path = work / config["target"]["path"]
        original = path.read_text()
        assert regex_passes(grader, original)
        # Any writer can bypass Write/Edit-tool guards. Use Python as the adversarial writer.
        subprocess.run(
            [
                sys.executable,
                "-c",
                'import pathlib,sys; pathlib.Path(sys.argv[1]).write_text("changed\\n")',
                str(path),
            ],
            check=True,
        )
        assert not regex_passes(grader, path.read_text())
        assert not regex_passes(grader, original + "\n")


def test_preparation_fixture_has_a_passing_real_characterization(
    tmp_path: Path,
) -> None:
    work = scaffold("define/d20-preparatory-slice", tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=work,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    members = json.loads((work / "data/members.json").read_text())
    assert members["ana"]["loan_days"] == 28
    # The real CLI currently ignores the member's duration; a scratch behavioral change
    # must break the old-behavior check before that check is used to justify preparation.
    source = work / "src/reminders.py"
    source.write_text(source.read_text().replace("days=21", "days=280"))
    changed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=work,
        capture_output=True,
        text=True,
    )
    assert changed.returncode != 0
    assert "280 days" in changed.stderr and "21 days" in changed.stderr


def test_project_own_check_passes_and_fixture_contains_the_reported_duplicate(
    tmp_path: Path,
) -> None:
    work = scaffold("define/d21-user-rule-over-default", tmp_path)
    baseline = subprocess.run(
        ["bash", "checks/overdue.sh"], cwd=work, capture_output=True
    )
    assert baseline.returncode == 0, baseline.stderr
    output = subprocess.check_output(
        [sys.executable, "src/shelfnote.py", "overdue"], cwd=work, text=True
    )
    assert output == "Middlemarch\nMiddlemarch\n"
    source = work / "src/shelfnote.py"
    source.write_text(
        source.read_text().replace('print(event["book"])', 'print("wrong book")')
    )
    broken = subprocess.run(
        ["bash", "checks/overdue.sh"], cwd=work, capture_output=True
    )
    assert broken.returncode != 0
