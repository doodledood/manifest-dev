"""
Shared fixtures for hook tests.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Add hooks directory to path for imports
HOOKS_DIR = (
    Path(__file__).parent.parent.parent / "claude-plugins" / "manifest-dev" / "hooks"
)
sys.path.insert(0, str(HOOKS_DIR))
