"""A verification scaffold builds only in a fresh scratch directory of its own.

A scaffold writes its project into the current directory. Run by hand inside a checkout, one renamed
the checkout's branch and overwrote its context file before failing. Every scaffold and fixture
script sources verification/scaffold-guard.sh first, which refuses a directory holding anything but
.git and gives an empty one a repository of its own.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
VERIFICATION = ROOT / "verification"
SCRIPTS = sorted(
    [
        *VERIFICATION.glob("scaffolds/*/scaffold.sh"),
        *VERIFICATION.glob("fixtures/*/scaffold.sh"),
        *VERIFICATION.glob("fixtures/*/base.sh"),
    ]
)


def _env(home: Path) -> dict[str, str]:
    env = {**os.environ, "HOME": str(home)}
    env.pop("MANIFEST_DEV_SCAFFOLD_NESTED", None)
    return env


def test_the_scripts_were_found() -> None:
    assert len(SCRIPTS) > 50, "the verification scaffolds were not found"


@pytest.mark.parametrize(
    "script", SCRIPTS, ids=lambda p: p.relative_to(VERIFICATION).as_posix()
)
def test_a_scaffold_refuses_a_directory_that_holds_anything(
    script: Path, tmp_path: Path
) -> None:
    work, home = tmp_path / "work", tmp_path / "home"
    work.mkdir()
    home.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    (work / "keep.txt").write_text("mine\n", encoding="utf-8")
    result = subprocess.run(
        ["bash", str(script)],
        cwd=work,
        env=_env(home),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode != 0, f"{script.name} ran in a directory holding a file"
    assert "run in an empty directory" in result.stderr
    assert sorted(p.name for p in work.iterdir()) == [".git", "keep.txt"]
    assert (work / "keep.txt").read_text(encoding="utf-8") == "mine\n"
    refs = subprocess.run(
        ["git", "for-each-ref"], cwd=work, capture_output=True, text=True, check=True
    )
    assert refs.stdout == "", "the scaffold wrote to the directory's repository"


def test_an_empty_directory_inside_a_checkout_gets_its_own_repository(
    tmp_path: Path,
) -> None:
    outer = tmp_path / "checkout"
    inner = outer / "scratch"
    inner.mkdir(parents=True)
    subprocess.run(["git", "init", "-q"], cwd=outer, check=True)
    subprocess.run(
        ["bash", "-c", f'. "{VERIFICATION / "scaffold-guard.sh"}"'],
        cwd=inner,
        env=_env(tmp_path),
        check=True,
    )
    assert (inner / ".git").is_dir()
