"""
Cross-plugin hook isolation tests.

With both `manifest-dev` and `manifest-dev-experimental` installed alongside,
each plugin's hooks must fire ONLY on its own plugin's skill invocations.
The hook_utils detection layer is namespace-scoped: bare skill names and
the other plugin's namespace are both ignored.

This file feeds fabricated transcripts of each plugin's invocations into
the OTHER plugin's parse_do_flow and asserts no /do is detected.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

MAIN_HOOK_UTILS = (
    REPO_ROOT / "claude-plugins" / "manifest-dev" / "hooks" / "hook_utils.py"
)
EXPERIMENTAL_HOOK_UTILS = (
    REPO_ROOT
    / "claude-plugins"
    / "manifest-dev-experimental"
    / "hooks"
    / "hook_utils.py"
)


def _load_module(name: str, path: Path):
    """Load a python module by file path (the two hook_utils.py files
    are siblings under different plugin dirs so they need explicit loading)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


main_hook_utils = _load_module("main_hook_utils", MAIN_HOOK_UTILS)
experimental_hook_utils = _load_module(
    "experimental_hook_utils", EXPERIMENTAL_HOOK_UTILS
)


def _write_transcript(tmp_path: Path, lines: list[dict[str, Any]]) -> str:
    transcript = tmp_path / "transcript.jsonl"
    with open(transcript, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(json.dumps(line) + "\n")
    return str(transcript)


class TestMainHooksIgnoreExperimentalSkillCalls:
    """Main plugin's parse_do_flow must not register experimental skill invocations."""

    def test_experimental_do_via_skill_tool_call_is_ignored(self, tmp_path: Path):
        """Assistant Skill call with manifest-dev-experimental:do should NOT register."""
        lines = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {
                                "skill": "manifest-dev-experimental:do",
                                "args": "/tmp/manifest.md",
                            },
                        }
                    ]
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = main_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is False
        assert state.has_done is False
        assert state.has_escalate is False

    def test_experimental_do_via_command_name_is_ignored(self, tmp_path: Path):
        """User /manifest-dev-experimental:do command should NOT register."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": (
                        "<command-name>/manifest-dev-experimental:do</command-name>"
                        "<command-args>/tmp/manifest.md</command-args>"
                    )
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = main_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is False

    def test_experimental_do_via_ismeta_is_ignored(self, tmp_path: Path):
        """isMeta skill expansion under manifest-dev-experimental/ should NOT register."""
        lines = [
            {
                "type": "user",
                "isMeta": True,
                "message": {
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Base directory for this skill: "
                                "/path/to/manifest-dev-experimental/skills/do\n\n"
                                "# /do - Manifest Executor"
                            ),
                        }
                    ]
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = main_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is False


class TestExperimentalHooksIgnoreMainSkillCalls:
    """Experimental plugin's parse_do_flow must not register main skill invocations."""

    def test_main_do_via_skill_tool_call_is_ignored(self, tmp_path: Path):
        """Assistant Skill call with manifest-dev:do should NOT register."""
        lines = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {
                                "skill": "manifest-dev:do",
                                "args": "/tmp/manifest.md",
                            },
                        }
                    ]
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = experimental_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is False
        assert state.has_done is False
        assert state.has_escalate is False

    def test_main_do_via_command_name_is_ignored(self, tmp_path: Path):
        """User /manifest-dev:do command should NOT register."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": (
                        "<command-name>/manifest-dev:do</command-name>"
                        "<command-args>/tmp/manifest.md</command-args>"
                    )
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = experimental_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is False

    def test_main_do_via_ismeta_is_ignored(self, tmp_path: Path):
        """isMeta skill expansion under manifest-dev/ should NOT register."""
        lines = [
            {
                "type": "user",
                "isMeta": True,
                "message": {
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Base directory for this skill: "
                                "/path/to/manifest-dev/skills/do\n\n"
                                "# /do - Manifest Executor"
                            ),
                        }
                    ]
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = experimental_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is False


class TestEachPluginDetectsItsOwnCalls:
    """Sanity check: each plugin's parse_do_flow still registers its own skill calls."""

    def test_main_detects_namespaced_do(self, tmp_path: Path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {
                                "skill": "manifest-dev:do",
                                "args": "/tmp/manifest.md",
                            },
                        }
                    ]
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = main_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is True

    def test_experimental_detects_namespaced_do(self, tmp_path: Path):
        lines = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {
                                "skill": "manifest-dev-experimental:do",
                                "args": "/tmp/manifest.md",
                            },
                        }
                    ]
                },
            }
        ]
        transcript_path = _write_transcript(tmp_path, lines)

        state = experimental_hook_utils.parse_do_flow(transcript_path)

        assert state.has_do is True
