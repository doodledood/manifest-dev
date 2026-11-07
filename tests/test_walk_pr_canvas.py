"""Drives walk-pr's canvas reference shell in headless Chromium.

The shell is code every canvas walk copies (`walk-pr/references/CANVAS_MODE.md` → *The
reference shell*), so its interaction rules are checked by running it, not by reading it:
`tests/fixtures/walk-pr-canvas/drive-canvas.mjs` presses keys and clicks as a reviewer would and
reads the page state and the copied review bundle. It skips where Node or Playwright with its
Chromium is not installed.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRIVE = ROOT / "tests/fixtures/walk-pr-canvas/drive-canvas.mjs"


def test_canvas_shell_interactions() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node unavailable")
    probe = subprocess.run(
        [node, "-e", "require('playwright').chromium.executablePath()"],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        pytest.skip("Playwright unavailable: " + probe.stderr.strip()[:200])
    result = subprocess.run(
        [node, str(DRIVE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
