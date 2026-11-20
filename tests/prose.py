"""Helpers for tests that assert phrases in shipped prose."""

from __future__ import annotations

from pathlib import Path


def flat(text: str) -> str:
    """Collapse whitespace so a phrase assertion survives prose re-wrapping."""
    return " ".join(text.split())


def flat_file(path: Path) -> str:
    """A file's text with its whitespace collapsed, as `flat` does."""
    return flat(path.read_text(encoding="utf-8"))
