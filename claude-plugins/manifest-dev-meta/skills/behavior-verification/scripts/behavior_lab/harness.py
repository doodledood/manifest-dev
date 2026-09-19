"""Harness-adapter interface for the empirical skill-behavior verification framework.

A harness adapter is the one thing `experiment.py` needs to run a scenario's
prompt through a real coding-agent CLI and get back the raw traffic that CLI
exchanged with its LLM backend. Keeping the interface to exactly
`configure_for_capture` / `invoke` / `decode_call` (per this skill's PG-4) means
a method that only one adapter could ever implement stays on that adapter, not
here — resist the urge to grow this ABC to fit `ClaudeCodeHarness`'s
convenience.
"""

from __future__ import annotations

import abc
import contextlib
import gzip
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from . import proxy

_USAGE_FIELDS = (
    "input_tokens",
    "output_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
)


class InvokeResult:
    """One harness invocation's process-level outcome (not the LLM traffic itself —
    that's recovered afterward from the run directory via `decode_call`)."""

    def __init__(self, *, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class Harness(abc.ABC):
    """Minimal contract every coding-agent harness adapter implements."""

    @abc.abstractmethod
    def configure_for_capture(self, run_directory: Path) -> dict[str, str]:
        """Environment variables that route this harness's LLM traffic through a
        capture proxy logging into ``run_directory``. The caller merges these over
        its own environment before calling `invoke`."""

    @abc.abstractmethod
    def invoke(
        self, prompt: str, *, cwd: str | Path, env: Mapping[str, str]
    ) -> InvokeResult:
        """Run one prompt through this harness synchronously, in ``cwd``, with
        ``env`` (the caller's environment merged with `configure_for_capture`'s
        overrides)."""

    @abc.abstractmethod
    def decode_call(self, diagnostics_entry: Mapping[str, Any]) -> dict[str, Any]:
        """Decode one captured diagnostics entry — this harness's own per-call
        capture shape — into a normalized record: session/agent identity, token
        usage, and the turn's content blocks (text/tool_use/tool_result/thinking)."""


def _unchunk_http1(data: bytes) -> bytes:
    """Strip HTTP/1.1 chunked-transfer-encoding framing, if present.

    Each chunk is ``<hex-size>\\r\\n<chunk-bytes>\\r\\n``, terminated by a
    zero-size chunk. A capture that doesn't parse as valid chunk framing simply
    isn't chunked — the caller falls back to the raw bytes rather than treating
    that as corruption.
    """
    out = bytearray()
    i = 0
    while i < len(data):
        j = data.find(b"\r\n", i)
        if j == -1:
            raise ValueError("truncated chunk header")
        size = int(data[i:j], 16)
        if size == 0:
            break
        start = j + 2
        out += data[start : start + size]
        i = start + size + 2
    return bytes(out)


def decode_sse_events(raw: bytes) -> list[dict[str, Any]]:
    """Hex-decoded proxy bytes -> parsed SSE events.

    Real Anthropic-API captures are hex -> HTTP-chunked -> gzip -> SSE
    ``event:``/``data:`` lines. Each layer is undone in order; a layer that
    doesn't apply (e.g. a small non-chunked, non-gzipped error body) is
    skipped rather than treated as corruption, so this also degrades
    gracefully on synthetic test fixtures that skip the wire-format layers
    entirely.
    """
    with contextlib.suppress(ValueError):
        raw = _unchunk_http1(raw)
    with contextlib.suppress(OSError):
        raw = gzip.decompress(raw)
    text = raw.decode("utf-8")

    events: list[dict[str, Any]] = []
    event_name: str | None = None
    for line in text.splitlines():
        if line.startswith("event:"):
            event_name = line[len("event:") :].strip()
        elif line.startswith("data:") and event_name is not None:
            data_str = line[len("data:") :].strip()
            try:
                events.append({"event": event_name, "data": json.loads(data_str)})
            except json.JSONDecodeError:
                continue
            event_name = None
    return events


def decode_response_body(response_body: Any) -> list[dict[str, Any]]:
    """Any captured ``response_body`` value -> a uniform list of SSE-shaped events.

    Handles all three encodings a capture proxy can produce: a captured
    ``{"base64": "<hex>"}`` streaming payload (the common case for real
    ``/v1/messages`` traffic), an already-parsed JSON dict (small
    non-streaming responses, e.g. errors), or a plain string.
    """
    if isinstance(response_body, Mapping) and "base64" in response_body:
        return decode_sse_events(bytes.fromhex(response_body["base64"]))
    if isinstance(response_body, Mapping):
        return [{"event": response_body.get("type", "message"), "data": response_body}]
    if isinstance(response_body, str) and response_body:
        try:
            return [{"event": "message", "data": json.loads(response_body)}]
        except json.JSONDecodeError:
            return []
    return []


def extract_usage(response_body: Any) -> dict[str, int]:
    """Merged token usage for one call, combined across every usage-bearing event.

    ``message_start`` carries the initial input/cache usage nested under its
    ``message`` object; ``message_delta`` carries its usage at the top level,
    and only republishes the full input/cache picture there when a
    server-side tool round occurred — otherwise it carries ``output_tokens``
    alone. Both locations are checked, and fields are merged per-key across
    all events rather than letting a later event overwrite the whole dict, or
    ``message_delta``'s partial usage would silently zero out
    ``message_start``'s input/cache counts for the common case.
    """
    usage = dict.fromkeys(_USAGE_FIELDS, 0)
    for event in decode_response_body(response_body):
        data = event["data"]
        candidates = [data.get("usage"), data.get("message", {}).get("usage")]
        for candidate in candidates:
            if isinstance(candidate, Mapping):
                for field in _USAGE_FIELDS:
                    if field in candidate:
                        usage[field] = candidate.get(field) or 0
    return usage


def _assemble_response_blocks(
    response_body: Any,
) -> tuple[list[dict[str, Any]], str | None]:
    """Decoded SSE events -> the assistant turn's content blocks + stop_reason.

    Accumulates ``content_block_start``/``content_block_delta`` events per
    block index into whole text/tool_use/thinking blocks, the same shape the
    Anthropic API's non-streaming response would have returned.
    """
    blocks: dict[int, dict[str, Any]] = {}
    input_json_fragments: dict[int, list[str]] = {}
    stop_reason: str | None = None

    for event in decode_response_body(response_body):
        data = event["data"]
        event_type = data.get("type")

        if event_type == "content_block_start":
            index = data.get("index", 0)
            block = dict(data.get("content_block") or {})
            blocks[index] = block
            if block.get("type") == "tool_use":
                input_json_fragments[index] = []

        elif event_type == "content_block_delta":
            index = data.get("index", 0)
            delta = data.get("delta") or {}
            block = blocks.setdefault(index, {})
            delta_type = delta.get("type")
            if delta_type == "text_delta":
                block["type"] = block.get("type", "text")
                block["text"] = block.get("text", "") + delta.get("text", "")
            elif delta_type == "thinking_delta":
                block["type"] = block.get("type", "thinking")
                block["thinking"] = block.get("thinking", "") + delta.get(
                    "thinking", ""
                )
            elif delta_type == "input_json_delta":
                input_json_fragments.setdefault(index, []).append(
                    delta.get("partial_json", "")
                )

        elif event_type == "message_delta":
            candidate_stop = (data.get("delta") or {}).get("stop_reason")
            if candidate_stop is not None:
                stop_reason = candidate_stop

        elif event_type == "message_start":
            message = data.get("message") or {}
            if message.get("stop_reason") is not None:
                stop_reason = message["stop_reason"]

    for index, fragments in input_json_fragments.items():
        joined = "".join(fragments)
        if joined:
            try:
                blocks[index]["input"] = json.loads(joined)
            except json.JSONDecodeError:
                blocks[index]["input"] = joined

    return [blocks[i] for i in sorted(blocks)], stop_reason


class ClaudeCodeHarness(Harness):
    """Real adapter for Claude Code: routes traffic through `proxy.py`'s reverse
    proxy and decodes real Anthropic-API SSE/chunked responses."""

    def __init__(
        self,
        *,
        claude_command: Sequence[str] = ("claude", "-p"),
        host: str = "127.0.0.1",
        upstream_url: str = "https://api.anthropic.com",
    ) -> None:
        self._claude_command = tuple(claude_command)
        self._host = host
        self._upstream_url = upstream_url
        self._servers: list[proxy.ProxyServer] = []

    def configure_for_capture(self, run_directory: Path) -> dict[str, str]:
        server = proxy.build_server(
            self._host, 0, upstream_url=self._upstream_url, run_directory=run_directory
        )
        proxy.serve_forever_in_thread(server)
        self._servers.append(server)
        port = server.server_address[1]
        return {"ANTHROPIC_BASE_URL": f"http://{self._host}:{port}"}

    def invoke(
        self, prompt: str, *, cwd: str | Path, env: Mapping[str, str]
    ) -> InvokeResult:
        result = subprocess.run(
            [*self._claude_command, prompt],
            cwd=cwd,
            env=dict(env),
            capture_output=True,
            text=True,
            check=False,
        )
        return InvokeResult(
            returncode=result.returncode, stdout=result.stdout, stderr=result.stderr
        )

    def decode_call(self, diagnostics_entry: Mapping[str, Any]) -> dict[str, Any]:
        request_body = diagnostics_entry.get("request_body")
        if isinstance(request_body, str):
            request_body = json.loads(request_body) if request_body else {}
        messages = (request_body or {}).get("messages") or []
        response_blocks, stop_reason = _assemble_response_blocks(
            diagnostics_entry.get("response_body")
        )
        return {
            "session_id": diagnostics_entry.get("session_id"),
            "agent_id": diagnostics_entry.get("agent_id"),
            "is_subagent": bool(diagnostics_entry.get("is_subagent")),
            "usage": extract_usage(diagnostics_entry.get("response_body")),
            "request_messages": messages,
            "response_blocks": response_blocks,
            "stop_reason": stop_reason,
        }


class CodexHarness(Harness):
    """Stub adapter for Codex CLI.

    Confirmed (this framework's originating investigation) that Codex CLI
    supports redirecting to a local proxy via ``openai_base_url`` in
    ``~/.codex/config.toml`` — so this adapter isn't speculative, only
    unimplemented. The remaining work is Codex's own wire format: its
    ``responses``/``chat`` request/response shapes differ from Anthropic's
    SSE/chunked format decoded in this module, and need their own decoder
    before `invoke`/`decode_call` can do anything real. No live Codex traffic
    was available to build or validate that decoder against.
    """

    def configure_for_capture(self, run_directory: Path) -> dict[str, str]:
        raise NotImplementedError(
            "CodexHarness.configure_for_capture: point openai_base_url in "
            "~/.codex/config.toml at a capture proxy — a Codex-specific "
            "response-format decoder is the remaining work (see class docstring)."
        )

    def invoke(
        self, prompt: str, *, cwd: str | Path, env: Mapping[str, str]
    ) -> InvokeResult:
        raise NotImplementedError(
            "CodexHarness.invoke: not implemented — see class docstring for the "
            "confirmed openai_base_url (~/.codex/config.toml) extension point."
        )

    def decode_call(self, diagnostics_entry: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError(
            "CodexHarness.decode_call: Codex's responses/chat wire format has no "
            "decoder yet — see class docstring for the confirmed config mechanism."
        )


class PiHarness(Harness):
    """Stub adapter for Pi.

    Confirmed (this framework's originating investigation) that Pi supports
    redirecting to a local proxy via ``baseUrl`` in ``~/.pi/agent/models.json``
    — so this adapter isn't speculative, only unimplemented. The remaining
    work is Pi's own wire format, which needs its own decoder before
    `invoke`/`decode_call` can do anything real. No live Pi traffic was
    available to build or validate that decoder against.
    """

    def configure_for_capture(self, run_directory: Path) -> dict[str, str]:
        raise NotImplementedError(
            "PiHarness.configure_for_capture: point baseUrl in "
            "~/.pi/agent/models.json at a capture proxy — a Pi-specific "
            "response-format decoder is the remaining work (see class docstring)."
        )

    def invoke(
        self, prompt: str, *, cwd: str | Path, env: Mapping[str, str]
    ) -> InvokeResult:
        raise NotImplementedError(
            "PiHarness.invoke: not implemented — see class docstring for the "
            "confirmed baseUrl (~/.pi/agent/models.json) extension point."
        )

    def decode_call(self, diagnostics_entry: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError(
            "PiHarness.decode_call: Pi's own wire format has no decoder yet — see "
            "class docstring for the confirmed config mechanism."
        )
