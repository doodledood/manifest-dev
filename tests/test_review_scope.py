"""Exercise the shipped review-scope commands against real Git change states."""

from __future__ import annotations

import re
import shlex
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "claude-plugins/manifest-dev/skills/review-code/SKILL.md"


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.STDOUT
    )


def review_commands() -> list[list[str]]:
    text = SKILL.read_text(encoding="utf-8")
    scope = text.split("## Determining scope", 1)[1].split("## ", 1)[0]
    return [
        shlex.split(command.replace("<base>", "refs/remotes/origin/trunk"))
        for command in re.findall(r"`(git (?:diff|ls-files)[^`]*)`", scope)
    ]


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "state", ["committed", "staged", "unstaged", "untracked", "staged-then-reverted"]
)
def test_review_scope_includes_each_change_state(tmp_path: Path, state: str) -> None:
    git(tmp_path, "init", "-q", "-b", "trunk")
    git(tmp_path, "config", "user.name", "Scope fixture")
    git(tmp_path, "config", "user.email", "scope@example.invalid")
    tracked = tmp_path / "tracked file.txt"
    tracked.write_text("original\n", encoding="utf-8")
    git(tmp_path, "add", "--", tracked.name)
    git(tmp_path, "commit", "-qm", "fixture")
    git(tmp_path, "update-ref", "refs/remotes/origin/trunk", "HEAD")

    changed = tmp_path / "new file.txt" if state == "untracked" else tracked
    changed.write_text("changed\n", encoding="utf-8")
    if state in {"staged", "committed", "staged-then-reverted"}:
        git(tmp_path, "add", "--", changed.name)
    if state == "committed":
        git(tmp_path, "commit", "-qm", "change")
    if state == "staged-then-reverted":
        tracked.write_text("original\n", encoding="utf-8")

    commands = review_commands()
    assert commands, "The scope must supply executable Git evidence collection."
    evidence = "\n".join(
        subprocess.check_output(command, cwd=tmp_path, text=True)
        for command in commands
    )
    assert changed.name in evidence, f"The prescribed scope omitted {state} work."
    if state != "untracked":
        assert "changed" in evidence, "File names alone do not expose the changed code."
