"""
Shared pytest fixtures for manifest-dev hook tests.

Fixtures defined here are automatically available to all test files
in this directory without explicit imports.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Make hook_test_helpers importable from test files
sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture
def temp_transcript(tmp_path: Path):
    """Factory fixture for creating temporary transcript files."""

    def _create_transcript(lines: list[dict[str, Any]]) -> str:
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(json.dumps(line) + "\n")
        return str(transcript_file)

    return _create_transcript


@pytest.fixture
def user_do_command() -> dict[str, Any]:
    """User message invoking /do."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/manifest-dev:do</command-name> /tmp/define.md"
        },
    }


@pytest.fixture
def assistant_skill_do() -> dict[str, Any]:
    """Assistant Skill tool call for do."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:do", "args": "/tmp/define.md"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_skill_verify() -> dict[str, Any]:
    """Assistant Skill tool call for verify."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {
                        "skill": "manifest-dev:verify",
                        "args": "/tmp/define.md",
                    },
                }
            ]
        },
    }


@pytest.fixture
def assistant_skill_done() -> dict[str, Any]:
    """Assistant Skill tool call for done."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "manifest-dev:done"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_skill_escalate() -> dict[str, Any]:
    """Assistant Skill tool call for escalate."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {
                        "skill": "manifest-dev:escalate",
                        "args": "AC-5 blocking",
                    },
                }
            ]
        },
    }


@pytest.fixture
def assistant_text() -> dict[str, Any]:
    """Simple assistant text response."""
    return {
        "type": "assistant",
        "message": {"content": "Working on AC-1.1..."},
    }
