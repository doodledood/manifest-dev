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


def load_run_entries(diagnostics_dir: Path | str) -> list[dict[str, Any]]:
    """Every raw diagnostics entry captured under ``diagnostics_dir``, in capture
    order — the full entry shape a harness adapter's `decode_call` expects.

    Unlike `load_session_entries`, this isn't filtered to one session: a run
    directory produced by `experiment.run_experiment` has exactly one session
    by construction, but this stays useful when it doesn't (e.g. a scenario
    whose own invocation launches subagent sessions sharing the run's proxy
    capture)."""
    entries = []
    for path in sorted(Path(diagnostics_dir).glob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        if entry.get("method") == "POST":
            entries.append(entry)
    return entries


def decode_calls_for_run(
    harness: Harness, diagnostics_dir: Path | str
) -> list[dict[str, Any]]:
    """Every decoded call (usage + response_blocks) for a whole run directory,
    in capture order — the run-scoped counterpart to `decode_calls_for_session`,
    and the correct pairing for `experiment.run_experiment`'s output with
    `assertions.assert_tool_invoked`/`diff_arms`.

    `experiment.load_run_calls` is NOT a substitute for this: it strips each
    entry down to a usage-only summary (no `request_body`/`response_body`),
    so feeding its output into `decode_call` silently yields empty
    `response_blocks` for every call rather than raising — this function
    exists specifically to avoid that trap by decoding the raw entries
    directly."""
    return [harness.decode_call(entry) for entry in load_run_entries(diagnostics_dir)]
