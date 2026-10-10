"""Adaptador HTTP local de la réplica; no carga el cliente experimental."""

from __future__ import annotations

import hmac
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

from domain import Model


class ReplicaHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address: tuple[str, int], token: str, model: Model | None = None):
        self.team_token = token
        self.model = model or Model()
        self.model_lock = threading.RLock()
        super().__init__(address, self._handler_type())

    def _handler_type(self):
        server = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_GET(self) -> None:
                self._handle()

            def do_POST(self) -> None:
                self._handle()

            def do_HEAD(self) -> None:
                self._handle()

            def do_PUT(self) -> None:
                self._handle()

            def do_PATCH(self) -> None:
                self._handle()

            def do_DELETE(self) -> None:
                self._handle()

            def do_OPTIONS(self) -> None:
                self._handle()

            def log_message(self, format: str, *args: object) -> None:
                return

            def __getattr__(self, name: str):
                # Unknown HTTP verbs are routed through the same observed
                # 404 response instead of BaseHTTPRequestHandler's 501 page.
                if name.startswith("do_"):
                    return self._handle
                raise AttributeError(name)

            def _json(self, status: int, body: object, *, suppress_body: bool = False) -> None:
                raw = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                if not suppress_body:
                    self.wfile.write(raw)

            def _handle(self) -> None:
                # Consume each request body exactly once, even for routes that
                # ignore it or requests rejected by auth. Otherwise unread
                # bytes desynchronize a keep-alive connection's next request.
                body_error = False
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    if length < 0 or length > 1_000_000:
                        raise ValueError("invalid length")
                    request_raw = self.rfile.read(length)
                    if len(request_raw) != length:
                        raise ValueError("incomplete body")
                except (ValueError, OSError):
                    request_raw = b""
                    body_error = True
                    self.close_connection = True

                path = urlsplit(self.path).path
                known_paths = {"/health", "/__reset", "/msg"}
                if path not in known_paths:
                    # The original returned E404 for a missing route with
                    # valid, missing, and invalid auth in the observed cases.
                    self._json(404, {"error": "E404", "mensaje": "ruta desconocida"},
                               suppress_body=self.command == "HEAD")
                    return

                supplied = self.headers.get("Authorization", "")
                expected = "Bearer " + server.team_token
                try:
                    authorized = hmac.compare_digest(supplied, expected)
                except TypeError:
                    # compare_digest rejects non-ASCII str inputs; treat such
                    # credentials as invalid instead of terminating the
                    # connection. Exact upstream behavior for this malformed
                    # header remains unverified.
                    authorized = False
                if not authorized:
                    self._json(401, {"error": "E001", "mensaje": "no autorizado"},
                               suppress_body=self.command == "HEAD")
                    return
                if body_error:
                    self._json(400, {"error": "E100", "mensaje": "json inválido"},
                               suppress_body=self.command == "HEAD")
                    return

                if self.command == "GET" and path == "/health":
                    self._json(200, {"ok": True})
                    return
                if self.command == "POST" and path == "/__reset":
                    with server.model_lock:
                        server.model.reset()
                    self._json(200, {"ok": True})
                    return
                if self.command == "POST" and path == "/msg":
                    try:
                        message_body = json.loads(
                            request_raw.decode("utf-8"),
                            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
                        )
                    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
                        self._json(400, {"error": "E100", "mensaje": "json inválido"})
                        return
                    if not isinstance(message_body, dict) or not isinstance(message_body.get("m"), str):
                        self._json(400, {"error": "E102", "mensaje": "falta m"})
                        return
                    with server.model_lock:
                        status, body = server.model.process(message_body["m"])
                    self._json(status, body)
                    return

                self._json(404, {"error": "E404", "mensaje": "ruta desconocida"},
                           suppress_body=self.command == "HEAD")

        return Handler


def serve(host: str = "127.0.0.1", port: int = 8000, token: str | None = None) -> None:
    actual_token = token if token is not None else os.environ.get("FRONTIER_TEAM_TOKEN", "")
    if not actual_token:
        raise RuntimeError("FRONTIER_TEAM_TOKEN no está configurado.")
    server = ReplicaHTTPServer((host, port), actual_token)
    try:
        server.serve_forever()
    finally:
        server.server_close()


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    serve(host, port)


if __name__ == "__main__":
    main()
