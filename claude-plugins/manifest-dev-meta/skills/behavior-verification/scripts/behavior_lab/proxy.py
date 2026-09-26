"""Transparent logging reverse-proxy for capturing coding-agent <-> LLM-backend traffic.

Point a harness's base-URL environment variable at this proxy and it forwards
every request byte-identically to the real API (or, in tests, to a local mock
upstream), streams the response back unmodified, and logs each request/
response pair — full body, headers minus the API key — as one JSON file per
call under ``<run_directory>/diagnostics/``.

Ported from (not imported from — see this repo's CLAUDE.md and this
manifest's INV-G2) ``tests/cache-experiment/proxy.py``, generalized to take a
plain, already-resolved ``run_directory`` rather than computing one from
cache-staggering-experiment-specific identifying parameters (arm, manifest
path, commit, repeat index) — that layout decision now lives in
``experiment.py``, which is the caller that knows what a "run" is for this
framework's arm/scenario shape.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import socket
import ssl
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

_REDACTED_HEADERS = {"x-api-key", "authorization"}
_REDACTED_VALUE = "[redacted]"
_CHUNK_SIZE = 65536
_SAFE_CHARS = re.compile(r"[^A-Za-z0-9_.-]+")


def _slug(value: str) -> str:
    """Filesystem-safe stand-in for an arbitrary identifier string."""
    slug = _SAFE_CHARS.sub("-", value).strip("-")
    return slug or "x"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_diagnostic(directory: Path, writer_id: str, payload: Any) -> Path:
    """Write one writer's diagnostics, disambiguated by writer_id.

    Every concurrent writer within the same run directory (e.g. one verifier
    subagent among several launched in parallel) must pass a distinct
    writer_id — a per-agent or per-call identifier, not arrival order — so
    simultaneous writes land in separate files instead of clobbering each
    other.
    """
    diagnostics_dir = ensure_dir(directory / "diagnostics")
    path = diagnostics_dir / f"{_slug(writer_id)}.json"
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8"
    )
    return path


def _redact_headers(headers: list[tuple[str, str]]) -> dict[str, str]:
    return {
        name: (_REDACTED_VALUE if name.lower() in _REDACTED_HEADERS else value)
        for name, value in headers
    }


def _header_value(headers: list[tuple[str, str]], name: str) -> str | None:
    """Case-insensitive lookup — HTTP header names aren't case-stable across clients."""
    target = name.lower()
    for header_name, value in headers:
        if header_name.lower() == target:
            return value
    return None


def _parse_upstream(upstream_url: str) -> tuple[str, str, int]:
    parts = urlsplit(upstream_url)
    scheme = parts.scheme or "https"
    host = parts.hostname
    if host is None:
        raise ValueError(f"upstream URL missing host: {upstream_url!r}")
    port = parts.port or (443 if scheme == "https" else 80)
    return scheme, host, port


def _connect_upstream(scheme: str, host: str, port: int) -> socket.socket:
    raw = socket.create_connection((host, port), timeout=30)
    if scheme == "https":
        context = ssl.create_default_context()
        return context.wrap_socket(raw, server_hostname=host)
    return raw


def _read_response_head(sock: socket.socket) -> tuple[bytes, bytes]:
    """Read off the upstream socket until the header block ends.

    Returns (header_bytes, leftover_body_bytes) — any body bytes that
    arrived in the same read as the tail of the headers are returned
    separately so callers can forward them without re-reading the socket.
    """
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = sock.recv(_CHUNK_SIZE)
        if not chunk:
            break
        buf += chunk
    header_bytes, _, leftover = buf.partition(b"\r\n\r\n")
    return header_bytes, leftover


def _decode_body(raw: bytes) -> str | dict[str, str]:
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return {"base64": raw.hex()}


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # set on the server instance by build_server()
    server: ProxyServer  # type: ignore[assignment]

    def _handle(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0) or 0)
        request_body = self.rfile.read(content_length) if content_length else b""
        request_headers = [(k, v) for k, v in self.headers.items()]

        try:
            upstream_sock = _connect_upstream(
                self.server.upstream_scheme,
                self.server.upstream_host,
                self.server.upstream_port,
            )
        except OSError as exc:
            self._send_upstream_unreachable(exc)
            return

        try:
            outgoing_headers = [
                (name, value)
                for name, value in request_headers
                if name.lower() not in ("host", "connection")
            ]
            outgoing_headers.append(("Host", self.server.upstream_host))
            # A fresh upstream socket is opened per request (no connection
            # reuse), so force the upstream to close after responding —
            # otherwise a keep-alive upstream leaves the response-relay loop
            # below blocked in recv() waiting for bytes that never arrive.
            outgoing_headers.append(("Connection", "close"))
            request_line = f"{self.command} {self.path} HTTP/1.1\r\n"
            header_block = "".join(
                f"{name}: {value}\r\n" for name, value in outgoing_headers
            )
            upstream_sock.sendall(
                request_line.encode("latin-1")
                + header_block.encode("latin-1")
                + b"\r\n"
                + request_body
            )

            header_bytes, leftover = _read_response_head(upstream_sock)
            status_line, _, header_lines = header_bytes.partition(b"\r\n")
            status_parts = status_line.decode("latin-1").split(" ", 2)
            status_code = int(status_parts[1]) if len(status_parts) > 1 else 502
            reason = status_parts[2] if len(status_parts) > 2 else ""

            response_headers: list[tuple[str, str]] = []
            for line in header_lines.split(b"\r\n"):
                if not line:
                    continue
                name, _, value = line.decode("latin-1").partition(":")
                response_headers.append((name.strip(), value.strip()))

            self.send_response(status_code, reason)
            for name, value in response_headers:
                if name.lower() in ("connection",):
                    continue
                self.send_header(name, value)
            self.end_headers()

            response_body = bytearray()
            if leftover:
                self.wfile.write(leftover)
                self.wfile.flush()
                response_body += leftover

            while True:
                chunk = upstream_sock.recv(_CHUNK_SIZE)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
                response_body += chunk
        except OSError:
            # Upstream reset mid-stream after headers were already relayed to
            # the client — nothing more can be forwarded, and the call is
            # incomplete, so it isn't logged, matching the pre-connect
            # failure path's behavior above.
            return
        finally:
            upstream_sock.close()

        self._log_call(
            request_headers=request_headers,
            request_body=request_body,
            response_status=status_code,
            response_headers=response_headers,
            response_body=bytes(response_body),
        )

    def _send_upstream_unreachable(self, exc: OSError) -> None:
        """Fail the forwarded request clearly rather than fabricating a response.

        A capture run must never mistake a proxy-side connectivity failure for
        a real API result, so this returns an explicit 502 with the
        underlying error instead of e.g. silently returning 200 with an empty
        body.
        """
        body = json.dumps(
            {
                "error": "proxy_upstream_unreachable",
                "detail": f"{self.server.upstream_host}:{self.server.upstream_port}: {exc}",
            }
        ).encode("utf-8")
        self.send_response(502, "Bad Gateway")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()

    def _log_call(
        self,
        *,
        request_headers: list[tuple[str, str]],
        request_body: bytes,
        response_status: int,
        response_headers: list[tuple[str, str]],
        response_body: bytes,
    ) -> None:
        call_id = f"call-{next(self.server.call_counter):04d}"
        session_id = _header_value(request_headers, "X-Claude-Code-Session-Id")
        agent_id = _header_value(request_headers, "x-claude-code-agent-id")
        anthropic_request_id = _header_value(response_headers, "request-id")
        entry = {
            "call_id": call_id,
            "session_id": session_id,
            "agent_id": agent_id,
            "is_subagent": agent_id is not None,
            "anthropic_request_id": anthropic_request_id,
            "method": self.command,
            "path": self.path,
            "request_headers": _redact_headers(request_headers),
            "request_body": _decode_body(request_body),
            "response_status": response_status,
            "response_headers": dict(response_headers),
            "response_body": _decode_body(response_body),
        }
        # Session/agent tags ride along in the filename (not just the JSON body) so a
        # plain `ls`/`grep` over diagnostics/ can filter to one session or group calls
        # by the specific subagent that made them, without opening every file.
        session_tag = f"sess-{session_id[:8]}" if session_id else "sess-none"
        agent_tag = f"agent-{agent_id}" if agent_id else "orchestrator"
        writer_id = f"{call_id}--{session_tag}--{agent_tag}"
        write_diagnostic(self.server.run_directory, writer_id, entry)

    def do_GET(self) -> None:
        self._handle()

    def do_POST(self) -> None:
        self._handle()

    def do_PUT(self) -> None:
        self._handle()

    def do_DELETE(self) -> None:
        self._handle()

    def do_PATCH(self) -> None:
        self._handle()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass  # silence default stderr access logging; diagnostics carry the real log


class ProxyServer(ThreadingHTTPServer):
    def __init__(
        self,
        address: tuple[str, int],
        handler: type[BaseHTTPRequestHandler],
        *,
        upstream_url: str,
        run_directory: Path,
    ) -> None:
        super().__init__(address, handler)
        self.upstream_scheme, self.upstream_host, self.upstream_port = _parse_upstream(
            upstream_url
        )
        self.run_directory = ensure_dir(run_directory)
        self.call_counter = itertools.count()


def build_server(
    host: str,
    port: int,
    *,
    upstream_url: str,
    run_directory: Path,
) -> ProxyServer:
    """Build a proxy server bound to (host, port) — pass port=0 for an
    OS-assigned ephemeral port, then read it back from ``server.server_address``."""
    return ProxyServer(
        (host, port),
        ProxyHandler,
        upstream_url=upstream_url,
        run_directory=run_directory,
    )


def serve_forever_in_thread(server: ProxyServer) -> threading.Thread:
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return thread


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--upstream", default="https://api.anthropic.com")
    parser.add_argument("--run-directory", required=True, type=Path)
    args = parser.parse_args()

    server = build_server(
        args.host,
        args.port,
        upstream_url=args.upstream,
        run_directory=args.run_directory,
    )
    print(f"Proxying {args.host}:{args.port} -> {args.upstream}")
    print(f"Logging to {args.run_directory / 'diagnostics'}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
