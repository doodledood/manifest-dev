"""State rules of the pull-request skills that a run cannot recover from GitHub alone.

Each test holds one rule an audit of the skills' own state machines found missing, with the
counterexample it stops in its docstring. The rules are prompt text, so the tests check the
text in the source skill and its Codex copy.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = "manifest-dev-tools/skills"


def _copies(rel: str) -> list[Path]:
    return [
        ROOT / "claude-plugins" / TOOLS / rel,
        ROOT / "dist/codex/plugins" / TOOLS / rel,
    ]


def _text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_babysit_resumes_the_manifest_its_journal_recorded() -> None:
    """Run 1 synthesizes M1, the user amends M1, run 2 must tend M1, not a fresh M2.

    Without the resume rule, every run without `--manifest` asked define for a new lifecycle
    Manifest holding only the baseline gates, so /do never judged the amended gate.
    """
    for path in _copies("babysit-pr/SKILL.md"):
        text = _text(path)
        assert (
            "resume the Manifest an earlier tend of this PR recorded in its journal"
            in text
        ), path
        assert (
            "only when no recorded Manifest file still exists, invoke `define`" in text
        ), path
        assert (
            "Each run boundary records the Manifest path this run tends" in text
        ), path
        assert "pass `--manifest` to keep a tended Manifest" in text, path
        assert "`/do` is the sole journal consumer" not in text, path
