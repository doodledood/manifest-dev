"""`scripts/check.sh` runs its tools from the project's virtual environment, or not at all.

A global mypy, ruff or black that happens to be on PATH gives wrong verdicts — a global mypy
cannot see pytest's types and reports dozens of false errors — so the script must never fall
through to one. Each test runs a copy of the script in a scratch tree whose `.venv/bin` holds
stand-in tools that record their name, with a decoy of each first on PATH that fails.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ("ruff", "black", "mypy", "python")


def _tool(path: Path, body: str) -> None:
    path.write_text(f"#!/usr/bin/env bash\n{body}\n")
    path.chmod(0o755)


def _tree(tmp_path: Path, *, venv: bool) -> tuple[Path, dict[str, str]]:
    tree = tmp_path / "repo"
    (tree / "scripts").mkdir(parents=True)
    shutil.copy(ROOT / "scripts" / "check.sh", tree / "scripts" / "check.sh")
    log = tmp_path / "calls"
    if venv:
        bin_dir = tree / ".venv" / "bin"
        bin_dir.mkdir(parents=True)
        for name in TOOLS:
            _tool(bin_dir / name, f'echo "venv {name} $*" >> {log}')
    decoys = tmp_path / "decoys"
    decoys.mkdir()
    for name in (*TOOLS, "python3"):
        _tool(decoys / name, f'echo "decoy {name}" >> {log}; exit 1')
    _tool(decoys / "npm", f'echo "npm $*" >> {log}')
    env = {**os.environ, "PATH": f"{decoys}:{os.environ['PATH']}"}
    return tree, env


def test_every_tool_runs_from_the_virtual_environment(tmp_path: Path) -> None:
    tree, env = _tree(tmp_path, venv=True)
    result = subprocess.run(
        ["bash", str(tree / "scripts" / "check.sh")],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    calls = (tmp_path / "calls").read_text()
    assert "decoy" not in calls, calls
    for name in TOOLS:
        assert f"venv {name}" in calls, calls


def test_a_missing_virtual_environment_stops_with_the_setup_pointer(
    tmp_path: Path,
) -> None:
    tree, env = _tree(tmp_path, venv=False)
    result = subprocess.run(
        ["bash", str(tree / "scripts" / "check.sh")],
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stderr
    assert "scripts/setup.sh" in result.stderr, result.stderr
    assert not (
        tmp_path / "calls"
    ).exists(), "a tool ran without the virtual environment"
