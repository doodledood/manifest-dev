"""Unit tests for tests.node.real_node shim unwrapping and fallbacks."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tests.node import real_node


def _write_exec(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)
    return path


def test_real_node_unwraps_path_dependent_shim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shim = _write_exec(
        tmp_path / "node",
        '#!/bin/sh\nif [ "$1" = "-p" ] && [ "$2" = "process.execPath" ]; then\n'
        '  echo "/real/bin/node"\n  exit 0\nfi\nexit 1\n',
    )
    monkeypatch.setenv("PATH", str(tmp_path))
    resolved = real_node()
    assert resolved == "/real/bin/node"
    assert resolved != str(shim)


def test_real_node_returns_none_when_node_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))
    assert real_node() is None


@pytest.mark.parametrize(
    "script",
    [
        "#!/bin/sh\nexit 1\n",
        "#!/bin/sh\nprintf '   \\n'\nexit 0\n",
    ],
    ids=["nonzero-exit", "whitespace-stdout"],
)
def test_real_node_falls_back_to_which_on_failed_or_empty_probe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, script: str
) -> None:
    stub = _write_exec(tmp_path / "node", script)
    monkeypatch.setenv("PATH", str(tmp_path))
    assert real_node() == str(stub)


def test_real_node_falls_back_on_oserror_and_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    broken = _write_exec(tmp_path / "node", "#!/nonexistent/interpreter-for-test\n")
    monkeypatch.setenv("PATH", str(tmp_path))
    assert real_node() == str(broken)

    def _timeout(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(cmd="node", timeout=10)

    monkeypatch.setattr(subprocess, "run", _timeout)
    assert real_node() == str(broken)
