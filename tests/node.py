"""Locate the real Node binary for tests that run subprocesses with a stripped PATH."""

from __future__ import annotations

import shutil
import subprocess


def real_node() -> str | None:
    """Return the real Node executable path, unwrapping PATH-dependent shims."""
    node = shutil.which("node")
    if node is None:
        return None
    try:
        probe = subprocess.run(
            [node, "-p", "process.execPath"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return node
    resolved = probe.stdout.strip()
    return resolved if probe.returncode == 0 and resolved else node
