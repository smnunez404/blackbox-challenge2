"""Arranca el entrypoint real y prueba su contrato sin tocar el servicio original."""

from __future__ import annotations

import http.client
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOKEN = "local-smoke-token-only"
EXAMPLES = ROOT / "raw" / "referencias" / "frontier-reto-2" / "pruebas" / "ejemplos.jsonl"
V2_OVERRIDES = {
    5: (200, {"saldo": "0.00", "cuenta_id": "AC-0001"}),
    8: (200, {"saldo": "400.00", "cuenta_id": "AC-0002"}),
    10: (422, {"error": "E506", "mensaje": "límite excedido"}),
    11: (200, {"saldo": "2100.00", "cuenta_id": "AC-0001"}),
    13: (404, {"error": "E402", "mensaje": "operación inexistente"}),
    14: (404, {"error": "E402", "mensaje": "operación inexistente"}),
    18: (200, {"status": "recieved", "operacionId": "OP-0003"}),
    19: (200, {"saldo": "407.00", "cuenta_id": "AC-0002"}),
}


def request(port: int, method: str, path: str, body: object | None = None,
            *, authorized: bool = True) -> tuple[int, object]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=2)
    headers = {"Authorization": f"Bearer {TOKEN}"} if authorized else {}
    payload = None if body is None else json.dumps(body).encode("utf-8")
    if payload is not None:
        headers["Content-Type"] = "application/json"
    try:
        connection.request(method, path, body=payload, headers=headers)
        response = connection.getresponse()
        return response.status, json.loads(response.read())
    finally:
        connection.close()


def main() -> None:
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]

    env = os.environ.copy()
    env.update({"HOST": "127.0.0.1", "PORT": str(port), "FRONTIER_TEAM_TOKEN": TOKEN})
    process = subprocess.Popen(
        [sys.executable, str(ROOT / "services" / "replica" / "http_server.py")],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.monotonic() + 5
        while True:
            if process.poll() is not None:
                raise RuntimeError("El entrypoint terminó durante el arranque")
            try:
                assert request(port, "GET", "/health") == (200, {"ok": True})
                break
            except (ConnectionError, OSError):
                if time.monotonic() >= deadline:
                    raise RuntimeError("El entrypoint no respondió en cinco segundos")
                time.sleep(0.05)

        assert request(port, "GET", "/health", authorized=False) == (
            401, {"error": "E001", "mensaje": "no autorizado"})
        assert request(port, "POST", "/__reset") == (200, {"ok": True})
        assert request(port, "POST", "/msg", {"m": "PING;64"}) == (200, {"pong": True})
        assert request(port, "GET", "/ruta-inexistente") == (
            404, {"error": "E404", "mensaje": "ruta desconocida"})
        assert request(port, "POST", "/__reset") == (200, {"ok": True})
        examples = [json.loads(line) for line in EXAMPLES.read_text(encoding="utf-8-sig").splitlines()
                    if line.strip()]
        assert len(examples) == 20
        for index, example in enumerate(examples, 1):
            observed = request(port, "POST", "/msg", example["request"])
            expected = V2_OVERRIDES.get(index, (example["status"], example["response"]))
            assert observed == expected, f"Ejemplo {index}: esperado={expected}, observado={observed}"
        print("Smoke local: health, auth, reset, ruta desconocida y 20 ejemplos HTTP OK")
    finally:
        process.terminate()
        try:
            process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=3)


if __name__ == "__main__":
    main()
