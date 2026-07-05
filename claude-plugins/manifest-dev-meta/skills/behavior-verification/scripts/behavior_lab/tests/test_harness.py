from __future__ import annotations

import pytest

from behavior_lab.harness import (
    ClaudeCodeHarness,
    CodexHarness,
    PiHarness,
    decode_response_body,
    decode_sse_events,
    extract_usage,
)

_SSE_TEXT = "\n".join(
    [
        "event: message_start",
        'data: {"type": "message_start", "message": {"id": "msg1", "usage": '
        '{"input_tokens": 100, "cache_creation_input_tokens": 0, '
        '"cache_read_input_tokens": 0, "output_tokens": 0}}}',
        "event: content_block_start",
        'data: {"type": "content_block_start", "index": 0, "content_block": '
        '{"type": "text", "text": ""}}',
        "event: content_block_delta",
        'data: {"type": "content_block_delta", "index": 0, "delta": '
        '{"type": "text_delta", "text": "Hello"}}',
        "event: content_block_start",
        'data: {"type": "content_block_start", "index": 1, "content_block": '
        '{"type": "tool_use", "id": "tool1", "name": "Skill", "input": {}}}',
        "event: content_block_delta",
        'data: {"type": "content_block_delta", "index": 1, "delta": '
        '{"type": "input_json_delta", "partial_json": "{\\"skill\\": \\"do\\"}"}}',
        "event: message_delta",
        'data: {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, '
        '"usage": {"output_tokens": 42}}',
        "event: message_stop",
        'data: {"type": "message_stop"}',
        "",
    ]
)

_SSE_TEXT_ONLY_TEXT_BLOCK = "\n".join(
    [
        "event: message_start",
        'data: {"type": "message_start", "message": {"usage": '
        '{"input_tokens": 10, "output_tokens": 0}}}',
        "event: content_block_start",
        'data: {"type": "content_block_start", "index": 0, "content_block": '
        '{"type": "text", "text": ""}}',
        "event: content_block_delta",
        'data: {"type": "content_block_delta", "index": 0, "delta": '
        '{"type": "text_delta", "text": "just text, no tools"}}',
        "event: message_delta",
        'data: {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, '
        '"usage": {"output_tokens": 5}}',
        "",
    ]
)


def _response_body(sse_text: str) -> dict[str, str]:
    return {"base64": sse_text.encode("utf-8").hex()}


def test_decode_sse_events_parses_plain_text_stream() -> None:
    events = decode_sse_events(_SSE_TEXT.encode("utf-8"))
    types = [e["data"]["type"] for e in events]
    assert types == [
        "message_start",
        "content_block_start",
        "content_block_delta",
        "content_block_start",
        "content_block_delta",
        "message_delta",
        "message_stop",
    ]


def test_extract_usage_merges_across_events_without_zeroing() -> None:
    usage = extract_usage(_response_body(_SSE_TEXT))
    assert usage == {
        "input_tokens": 100,
        "output_tokens": 42,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }


def test_extract_usage_negative_no_usage_present() -> None:
    usage = extract_usage({"type": "error", "error": {"message": "boom"}})
    assert usage == {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
    }


def test_decode_response_body_handles_plain_dict() -> None:
    events = decode_response_body({"type": "error", "error": {"message": "boom"}})
    assert events == [
        {"event": "error", "data": {"type": "error", "error": {"message": "boom"}}}
    ]


def test_claude_code_harness_decode_call_assembles_tool_use_and_text() -> None:
    harness = ClaudeCodeHarness()
    diagnostics_entry = {
        "session_id": "sess-1",
        "agent_id": None,
        "is_subagent": False,
        "request_body": {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": "do something"}]}
            ]
        },
        "response_body": _response_body(_SSE_TEXT),
    }

    decoded = harness.decode_call(diagnostics_entry)

    assert decoded["session_id"] == "sess-1"
    assert decoded["usage"]["input_tokens"] == 100
    assert decoded["stop_reason"] == "end_turn"
    blocks_by_type = {b["type"]: b for b in decoded["response_blocks"]}
    assert blocks_by_type["text"]["text"] == "Hello"
    assert blocks_by_type["tool_use"]["name"] == "Skill"
    assert blocks_by_type["tool_use"]["input"] == {"skill": "do"}


def test_claude_code_harness_decode_call_negative_no_tool_use() -> None:
    harness = ClaudeCodeHarness()
    diagnostics_entry = {
        "session_id": "sess-2",
        "agent_id": "agent-7",
        "is_subagent": True,
        "request_body": {"messages": [{"role": "user", "content": "hi"}]},
        "response_body": _response_body(_SSE_TEXT_ONLY_TEXT_BLOCK),
    }

    decoded = harness.decode_call(diagnostics_entry)

    assert decoded["is_subagent"] is True
    assert all(block["type"] != "tool_use" for block in decoded["response_blocks"])


@pytest.mark.parametrize("harness_cls", [CodexHarness, PiHarness])
def test_stub_harnesses_raise_not_implemented(harness_cls: type, tmp_path) -> None:
    harness = harness_cls()
    with pytest.raises(NotImplementedError):
        harness.configure_for_capture(tmp_path)
    with pytest.raises(NotImplementedError):
        harness.invoke("prompt", cwd=tmp_path, env={})
    with pytest.raises(NotImplementedError):
        harness.decode_call({})
