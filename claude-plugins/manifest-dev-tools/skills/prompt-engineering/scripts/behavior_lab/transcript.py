"""Session reconstruction: turn a run directory's captured diagnostics for one
session into its full turn-by-turn conversation.

Reconstruction goes through a harness adapter's `decode_call` rather than
re-implementing wire-format decoding here — this module works for any
`Harness` implementation (including a future real Codex/Pi adapter) as long
as `decode_call` returns the normalized shape `harness.py`'s interface
promises.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .harness import Harness


def load_session_entries(
    diagnostics_dir: Path | str, session_id: str
) -> list[dict[str, Any]]:
    """Every raw diagnostics entry for one session, in capture order.

    Capture order matches lexicographic filename order — proxy.py names
    files ``call-<seq>--...`` with a zero-padded sequence number."""
    entries = []
    for path in sorted(Path(diagnostics_dir).glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        if entry.get("session_id") == session_id and entry.get("method") == "POST":
            entries.append(entry)
    return entries


def reconstruct_session(
    harness: Harness, diagnostics_dir: Path | str, session_id: str
) -> list[dict[str, Any]]:
    """One session's full conversation as a flat list of turns
    (``{"role": ..., "content": [...]}``), decoded call by call via the
    harness adapter's `decode_call` — never by re-parsing wire format here."""
    turns: list[dict[str, Any]] = []
    for entry in load_session_entries(diagnostics_dir, session_id):
        decoded = harness.decode_call(entry)
        messages = decoded.get("request_messages") or []
        if messages:
            last_message = messages[-1]
            turns.append(
                {
                    "role": last_message.get("role", "user"),
                    "content": last_message.get("content"),
                }
            )
        turns.append(
            {"role": "assistant", "content": decoded.get("response_blocks", [])}
        )
    return turns


def decode_calls_for_session(
    harness: Harness, diagnostics_dir: Path | str, session_id: str
) -> list[dict[str, Any]]:
    """Every decoded call (usage + response_blocks, per `Harness.decode_call`)
    for one session, in capture order — the shape `assertions.py`'s functions
    expect."""
    return [
        harness.decode_call(entry)
        for entry in load_session_entries(diagnostics_dir, session_id)
    ]
