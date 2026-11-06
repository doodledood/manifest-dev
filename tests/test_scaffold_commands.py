"""Every command a scaffold's README lists runs in the project that scaffold builds.

A scaffold is the project a drive or an eval case puts a skill in front of. When its README
names a command that cannot run, a careful run reports the broken fixture instead of doing the
task the case measures, and the case grades the fixture rather than the skill. New cases copy an
existing scaffold, so one broken command spreads to every copy.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
# The this-repository scaffolds unpack this checkout, whose README lists no runnable example.
SCAFFOLDS = sorted(
    p
    for base in ("claude-plugins/manifest-dev/evals", "verification/scaffolds")
    for p in (ROOT / base).rglob("scaffold.sh")
    if "cat > README.md" in p.read_text(encoding="utf-8")
)
# A README lists its commands as an indented block, one command per line.
README_COMMAND = re.compile(r"^ {4}(\S.*)$", re.MULTILINE)
LIMIT_SECONDS = 60


@pytest.mark.parametrize(
    "script", SCAFFOLDS, ids=lambda p: p.parent.relative_to(ROOT).as_posix()
)
def test_each_readme_command_runs_in_the_scaffolded_project(script: Path) -> None:
    with (
        tempfile.TemporaryDirectory() as workdir,
        tempfile.TemporaryDirectory() as home,
    ):
        env = {**os.environ, "HOME": home}
        built = subprocess.run(
            ["bash", str(script)],
            cwd=workdir,
            env=env,
            capture_output=True,
            text=True,
            timeout=LIMIT_SECONDS,
            check=False,
        )
        assert built.returncode == 0, built.stderr
        readme = Path(workdir, "README.md").read_text(encoding="utf-8")
        for command in README_COMMAND.findall(readme):
            ran = subprocess.run(
                ["bash", "-c", command],
                cwd=workdir,
                env=env,
                capture_output=True,
                text=True,
                timeout=LIMIT_SECONDS,
                check=False,
            )
            assert ran.returncode == 0, f"{command}\n{ran.stderr}"


def test_red_base_scaffold_reaches_its_intended_failure(tmp_path: Path) -> None:
    """Portable setup must reach the missed caller, not fail before the task begins."""
    work, home = tmp_path / "work", tmp_path / "home"
    work.mkdir()
    home.mkdir()
    env = {**os.environ, "HOME": str(home)}
    built = subprocess.run(
        [
            "bash",
            str(ROOT / "verification/scaffolds/red-base-ticket-store/scaffold.sh"),
        ],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
        timeout=LIMIT_SECONDS,
        check=False,
    )
    assert built.returncode == 0, built.stderr
    tested = subprocess.run(
        ["python3", "-m", "unittest", "discover", "-s", "tests"],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
        timeout=LIMIT_SECONDS,
        check=False,
    )
    assert tested.returncode != 0
    assert "cannot import name 'due_date'" in tested.stderr
