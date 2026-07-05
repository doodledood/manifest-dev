from __future__ import annotations

import json
from pathlib import Path

from behavior_lab.assertions import assert_tool_invoked
from behavior_lab.harness import ClaudeCodeHarness
from behavior_lab.transcript import (
    decode_calls_for_run,
    decode_calls_for_session,
    load_run_entries,
    load_session_entries,
    reconstruct_session,
)


def _sse(text_delta: str) -> dict[str, str]:
    lines = "\n".join(
        [
            "event: message_start",
            'data: {"type": "message_start", "message": {"usage": {"input_tokens": 10, '
            '"output_tokens": 0}}}',
            "event: content_block_start",
            'data: {"type": "content_block_start", "index": 0, "content_block": '
            '{"type": "text", "text": ""}}',
            "event: content_block_delta",
            'data: {"type": "content_block_delta", "index": 0, "delta": '
            f'{{"type": "text_delta", "text": {json.dumps(text_delta)}}}}}',
            "event: message_delta",
            'data: {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, '
            '"usage": {"output_tokens": 3}}',
            "",
        ]
    )
    return {"base64": lines.encode("utf-8").hex()}


def _write_call(
    diagnostics_dir: Path,
    name: str,
    *,
    session_id: str,
    user_text: str,
    reply_text: str,
    method: str = "POST",
) -> None:
    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    entry = {
        "session_id": session_id,
        "agent_id": None,
        "is_subagent": False,
        "method": method,
        "response_status": 200,
        "request_body": {"messages": [{"role": "user", "content": user_text}]},
        "response_body": _sse(reply_text),
    }
    (diagnostics_dir / f"{name}.json").write_text(json.dumps(entry), encoding="utf-8")


def test_reconstruct_session_orders_turns_by_capture_order(tmp_path: Path) -> None:
    diagnostics_dir = tmp_path / "diagnostics"
    _write_call(
        diagnostics_dir,
        "call-0000",
        session_id="sess-1",
        user_text="first",
        reply_text="reply one",
    )
    _write_call(
        diagnostics_dir,
        "call-0001",
        session_id="sess-1",
        user_text="second",
        reply_text="reply two",
    )
    # negative: a different session must not bleed into sess-1's reconstruction
    _write_call(
        diagnostics_dir,
        "call-0002",
        session_id="sess-2",
        user_text="other",
        reply_text="other reply",
    )

    turns = reconstruct_session(ClaudeCodeHarness(), diagnostics_dir, "sess-1")

    assert len(turns) == 4
    assert turns[0] == {"role": "user", "content": "first"}
    assert turns[1]["role"] == "assistant"
    assert turns[1]["content"][0]["text"] == "reply one"
    assert turns[2] == {"role": "user", "content": "second"}
    assert turns[3]["content"][0]["text"] == "reply two"


def test_load_session_entries_negative_excludes_other_sessions(tmp_path: Path) -> None:
    diagnostics_dir = tmp_path / "diagnostics"
    _write_call(
        diagnostics_dir, "call-0000", session_id="sess-1", user_text="a", reply_text="b"
    )
    _write_call(
        diagnostics_dir, "call-0001", session_id="sess-2", user_text="c", reply_text="d"
    )

    entries = load_session_entries(diagnostics_dir, "sess-1")
    assert len(entries) == 1
    assert entries[0]["session_id"] == "sess-1"


def test_decode_calls_for_session_returns_decoded_shape(tmp_path: Path) -> None:
    diagnostics_dir = tmp_path / "diagnostics"
    _write_call(
        diagnostics_dir,
        "call-0000",
        session_id="sess-1",
        user_text="a",
        reply_text="hello",
    )

    decoded = decode_calls_for_session(ClaudeCodeHarness(), diagnostics_dir, "sess-1")
    assert len(decoded) == 1
    assert decoded[0]["response_blocks"][0]["text"] == "hello"
    assert decoded[0]["usage"]["output_tokens"] == 3


def _write_call_with_tool_use(
    diagnostics_dir: Path, name: str, *, session_id: str, tool_name: str
) -> None:
    diagnostics_dir.mkdir(parents=True, exist_ok=True)
    lines = "\n".join(
        [
            "event: content_block_start",
            'data: {"type": "content_block_start", "index": 0, "content_block": '
            f'{{"type": "tool_use", "id": "t1", "name": "{tool_name}", "input": {{}}}}}}',
            "event: content_block_delta",
            'data: {"type": "content_block_delta", "index": 0, "delta": '
            '{"type": "input_json_delta", "partial_json": "{}"}}',
            "",
        ]
    )
    entry = {
        "session_id": session_id,
        "agent_id": None,
        "is_subagent": False,
        "method": "POST",
        "response_status": 200,
        "request_body": {"messages": [{"role": "user", "content": "run the tool"}]},
        "response_body": {"base64": lines.encode("utf-8").hex()},
    }
    (diagnostics_dir / f"{name}.json").write_text(json.dumps(entry), encoding="utf-8")


def test_decode_calls_for_run_is_the_correct_pairing_for_assert_tool_invoked(
    tmp_path: Path,
) -> None:
    """Regression test for the doc's own worked example: `decode_calls_for_run`
    (unlike `experiment.load_run_calls`) must produce entries `assert_tool_invoked`
    can actually see the tool_use block in, across every session in a run
    directory (not just one)."""
    diagnostics_dir = tmp_path / "diagnostics"
    _write_call_with_tool_use(
        diagnostics_dir, "call-0000", session_id="sess-1", tool_name="Skill"
    )
    _write_call_with_tool_use(
        diagnostics_dir, "call-0001", session_id="sess-2", tool_name="Bash"
    )

    decoded = decode_calls_for_run(ClaudeCodeHarness(), diagnostics_dir)

    assert len(decoded) == 2
    assert assert_tool_invoked(decoded, "Skill") is True
    assert assert_tool_invoked(decoded, "Bash") is True
    assert assert_tool_invoked(decoded, "Edit") is False


def test_load_run_entries_negative_excludes_non_post(tmp_path: Path) -> None:
    diagnostics_dir = tmp_path / "diagnostics"
    _write_call(
        diagnostics_dir, "call-0000", session_id="sess-1", user_text="a", reply_text="b"
    )
    _write_call(
        diagnostics_dir,
        "call-0001",
        session_id="sess-2",
        user_text="c",
        reply_text="d",
        method="GET",
    )

    entries = load_run_entries(diagnostics_dir)
    assert len(entries) == 1
    assert entries[0]["session_id"] == "sess-1"
