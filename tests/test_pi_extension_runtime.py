from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
NODE_TEST = ROOT / "tests" / "pi_extension_runtime.test.mjs"
RUNTIME_TS = ROOT / "pi" / "extensions" / "manifest-dev-runtime.ts"


def test_pi_extension_runtime_behavior() -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed; cannot run Pi extension runtime tests")

    strip_types_check = subprocess.run(
        [node, "--experimental-strip-types", "--check", str(RUNTIME_TS)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if strip_types_check.returncode != 0:
        pytest.skip(
            "node does not support --experimental-strip-types for TypeScript tests"
        )

    subprocess.run(
        [node, "--experimental-strip-types", "--test", str(NODE_TEST)],
        cwd=ROOT,
        check=True,
    )
