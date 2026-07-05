from __future__ import annotations

import http.client
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from behavior_lab import proxy


class _MockUpstreamHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0) or 0)
        self.rfile.read(length)
        body = json.dumps({"ok": True}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        pass


def _start_mock_upstream() -> tuple[ThreadingHTTPServer, int]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _MockUpstreamHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


def test_proxy_forwards_and_logs_call(tmp_path: Path) -> None:
    upstream, upstream_port = _start_mock_upstream()
    run_directory = tmp_path / "run"
    server = proxy.build_server(
        "127.0.0.1",
        0,
        upstream_url=f"http://127.0.0.1:{upstream_port}",
        run_directory=run_directory,
    )
    proxy.serve_forever_in_thread(server)
    proxy_port = server.server_address[1]

    try:
        conn = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=5)
        conn.request(
            "POST",
            "/v1/messages",
            body=json.dumps({"messages": [{"role": "user", "content": "hi"}]}),
            headers={
                "Content-Type": "application/json",
                "x-api-key": "super-secret",
                "X-Claude-Code-Session-Id": "sess-abc123",
            },
        )
        response = conn.getresponse()
        assert response.status == 200
        response.read()
        conn.close()
    finally:
        server.shutdown()
        upstream.shutdown()

    diagnostics = list((run_directory / "diagnostics").glob("*.json"))
    assert len(diagnostics) == 1
    entry = json.loads(diagnostics[0].read_text(encoding="utf-8"))
    assert entry["method"] == "POST"
    assert entry["response_status"] == 200
    assert entry["session_id"] == "sess-abc123"
    assert entry["request_headers"]["x-api-key"] == "[redacted]"
    assert entry["response_body"] == {"ok": True}


def test_proxy_negative_upstream_unreachable_returns_502_and_does_not_log(
    tmp_path: Path,
) -> None:
    run_directory = tmp_path / "run"
    # Port 1 is a reserved low port nothing is listening on in this sandbox.
    server = proxy.build_server(
        "127.0.0.1", 0, upstream_url="http://127.0.0.1:1", run_directory=run_directory
    )
    proxy.serve_forever_in_thread(server)
    proxy_port = server.server_address[1]

    try:
        conn = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=5)
        conn.request("POST", "/v1/messages", body=b"{}")
        response = conn.getresponse()
        assert response.status == 502
        response.read()
        conn.close()
    finally:
        server.shutdown()

    diagnostics_dir = run_directory / "diagnostics"
    assert not diagnostics_dir.exists() or not list(diagnostics_dir.glob("*.json"))
