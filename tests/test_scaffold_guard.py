"""A verification scaffold builds only in a fresh scratch directory of its own.

A scaffold writes its project into the current directory. Run by hand inside a checkout, one renamed
the checkout's branch and overwrote its context file before failing. Every scaffold and fixture
script sources verification/scaffold-guard.sh first, which refuses a directory holding anything but
a .git with no commit yet, and gives an empty one a repository of its own. The eval-case scaffolds
under claude-plugins/manifest-dev/evals are outside this check; scaffold-guard.sh says why and what
would close them.
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
VERIFICATION = ROOT / "verification"
GUARD = VERIFICATION / "scaffold-guard.sh"
GUARD_LINE = '. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"'
# Every shell script under verification/ builds a project, except the guard itself and the model
# checks, which read a project rather than write one.
SCRIPTS = sorted(
    p
    for p in VERIFICATION.rglob("*.sh")
    if p != GUARD and p.relative_to(VERIFICATION).parts[0] != "models"
)


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    ).stdout


def _repository_state(work: Path) -> tuple[str, str, str, list[str]]:
    config = Path(
        _git(
            work, "rev-parse", "--path-format=absolute", "--git-path", "config"
        ).strip()
    )
    return (
        _git(work, "for-each-ref"),
        _git(work, "symbolic-ref", "HEAD"),
        config.read_text(encoding="utf-8"),
        sorted(p.name for p in work.iterdir()),
    )


def _one_file(work: Path) -> None:
    (work / "keep.txt").write_text("mine\n", encoding="utf-8")


def _one_dot_file(work: Path) -> None:
    (work / ".env").write_text("mine\n", encoding="utf-8")


def _many_files(work: Path) -> None:
    # Enough entries that a check reading the directory through a pipe is cut short under pipefail.
    for n in range(20000):
        (work / f"f{n}").touch()


def _a_commit_and_no_files(work: Path) -> None:
    # A no-checkout clone: a repository with history whose files are not on disk.
    (work / "owner.txt").write_text("mine\n", encoding="utf-8")
    _git(work, "add", "owner.txt")
    _git(
        work,
        "-c",
        "user.name=o",
        "-c",
        "user.email=o@example.org",
        "commit",
        "-qm",
        "o",
    )
    (work / "owner.txt").unlink()


def _an_orphan_checkout(work: Path) -> None:
    # History on trunk, while HEAD names a new branch with no commit and no files.
    _a_commit_and_no_files(work)
    _git(work, "checkout", "-q", "--orphan", "wip")


def _a_fetched_ref(work: Path) -> None:
    # Initialised, then fetched into: refs exist, HEAD names a branch with no commit.
    source = work.parent / f"{work.name}-source"
    source.mkdir()
    _git(source, "init", "-q", "-b", "main")
    (source / "owner.txt").write_text("mine\n", encoding="utf-8")
    _git(source, "add", "owner.txt")
    _git(
        source,
        "-c",
        "user.name=o",
        "-c",
        "user.email=o@example.org",
        "commit",
        "-qm",
        "o",
    )
    _git(work, "fetch", "-q", str(source), "main:refs/remotes/origin/main")


CONTENTS: dict[str, Callable[[Path], None]] = {
    "one file": _one_file,
    "a dot-file": _one_dot_file,
    "many files": _many_files,
    "a repository with history": _a_commit_and_no_files,
    "an orphan checkout": _an_orphan_checkout,
    "a fetched ref": _a_fetched_ref,
}


@pytest.fixture(scope="module", params=[*CONTENTS, "a .git file"])
def occupied(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Iterator[Path]:
    # A correct guard writes nothing, so one occupied directory serves every script.
    work = tmp_path_factory.mktemp("occupied")
    if request.param == "a .git file":
        # A worktree-style .git file pointing at a repository kept elsewhere, with no commit.
        gitdir = tmp_path_factory.mktemp("separate") / "repo.git"
        _git(work, "init", "-q", "-b", "trunk", f"--separate-git-dir={gitdir}")
    else:
        _git(work, "init", "-q", "-b", "trunk")
        CONTENTS[request.param](work)
    yield work


def test_the_scripts_were_found() -> None:
    assert len(SCRIPTS) > 50, "the verification scaffolds were not found"


@pytest.mark.parametrize(
    "script", SCRIPTS, ids=lambda p: p.relative_to(VERIFICATION).as_posix()
)
def test_the_guard_runs_before_anything_else(script: Path) -> None:
    commands = [
        line
        for line in script.read_text(encoding="utf-8").splitlines()[1:]
        if line.strip() and not line.startswith("#")
    ]
    assert commands[0].startswith("set -"), f"{script.name} does not start with set"
    assert commands[1] == GUARD_LINE, f"{script.name} runs something before the guard"


@pytest.mark.parametrize(
    "script", SCRIPTS, ids=lambda p: p.relative_to(VERIFICATION).as_posix()
)
def test_a_scaffold_refuses_a_directory_that_is_not_fresh(
    script: Path, occupied: Path, tmp_path: Path
) -> None:
    before = _repository_state(occupied)
    result = subprocess.run(
        ["bash", str(script)],
        cwd=occupied,
        env={**os.environ, "HOME": str(tmp_path)},
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert (
        result.returncode != 0
    ), f"{script.name} ran in a directory that was not fresh"
    assert "run in an empty directory" in result.stderr
    assert _repository_state(occupied) == before, f"{script.name} changed the directory"


def test_an_empty_directory_inside_a_checkout_gets_its_own_repository(
    tmp_path: Path,
) -> None:
    outer = tmp_path / "checkout"
    inner = outer / "scratch"
    inner.mkdir(parents=True)
    _git(outer, "init", "-q")
    subprocess.run(["bash", "-c", f'. "{GUARD}"'], cwd=inner, check=True)
    assert (inner / ".git").is_dir()


def test_a_fresh_repository_is_accepted(tmp_path: Path) -> None:
    _git(tmp_path, "init", "-q")
    subprocess.run(["bash", "-c", f'. "{GUARD}"'], cwd=tmp_path, check=True)
