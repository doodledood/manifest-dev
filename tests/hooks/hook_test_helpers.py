"""
Shared helper functions and constants for manifest-dev hook tests.

Unlike conftest.py (which provides pytest fixtures), this module provides
importable functions and constants used across test files.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# Path to the hooks directory
HOOKS_DIR = (
    Path(__file__).parent.parent.parent / "claude-plugins" / "manifest-dev" / "hooks"
)


def run_hook(hook_name: str, hook_input: dict[str, Any]) -> dict[str, Any] | None:
    """Run a hook script and return parsed JSON output, or None if no output."""
    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / hook_name)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
        cwd=str(HOOKS_DIR),
    )
    assert result.returncode == 0, f"{hook_name} crashed: {result.stderr}"
    if result.stdout.strip():
        return json.loads(result.stdout)
    return None


def run_hook_raw(
    hook_name: str, hook_input: dict[str, Any]
) -> subprocess.CompletedProcess:
    """Run a hook script and return the raw CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(HOOKS_DIR / hook_name)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
        cwd=str(HOOKS_DIR),
    )
