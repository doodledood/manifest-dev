"""Public CLI and observation regressions for optional design instruments.

DESIGN_TOOLS_TEST_BROWSER=1 requires development capture cases to execute.
DESIGN_TOOLS_TEST_IMAGES=1 requires the native Pillow image case. The shipped
runtime itself has no browser dependency.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_optional_instruments_contract() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node unavailable")
    result = subprocess.run(
        [
            node,
            "--test",
            "--test-reporter=tap",
            "tests/fixtures/design-instruments/test-instruments.mjs",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "# fail 0" in result.stdout
    if (
        os.environ.get("DESIGN_TOOLS_TEST_BROWSER") == "1"
        and os.environ.get("DESIGN_TOOLS_TEST_IMAGES") == "1"
    ):
        assert "# skipped 0" in result.stdout, result.stdout


def test_optional_instruments_javascript_parses() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node unavailable")
    scripts = list(
        (ROOT / "claude-plugins/manifest-dev/skills/design/scripts").glob("*.mjs")
    ) + list((ROOT / "scripts/design-evals").glob("*.mjs"))
    for script in scripts:
        result = subprocess.run(
            [node, "--check", str(script)], capture_output=True, text=True, check=False
        )
        assert result.returncode == 0, result.stderr
