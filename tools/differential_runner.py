"""Runner diferencial propio para secuencias del Reto 2.

Uso offline (no abre sockets):
  python differential_runner.py --mode offline --sequence casos.jsonl --fixture fixtures/ejemplo-artificial.json

Comparación contra un servidor de réplica local (nunca contacta el original):
  python differential_runner.py --mode replica --sequence casos.jsonl --fixture fixtures/ejemplo-artificial.json --base-url http://127.0.0.1:8000

La secuencia puede ser JSON (array de pasos o {"steps": [...]}) o JSONL (un paso por línea).
Cada paso tiene {"request":{"method":"POST","path":"/msg","body":{"m":"PING;64"}},
"status":200,"response":{"pong":true}}. `status` y `response` son opcionales en la
secuencia: se usan solo para validar una captura offline cuando están presentes. La fixture
usa el mismo formato y contiene las respuestas de referencia. En modo replica se envía cada
request a localhost y se compara su status y cuerpo con la fixture. JSON se compara por valor
(el orden de claves de objetos no importa); cuerpos no JSON se comparan como texto exacto.

La primera divergencia detiene la corrida y se imprime como JSON con paso y campo. Las
fixtures bajo fixtures/ son artificiales salvo que se indique explícitamente; nunca se deben
presentar como observaciones del servicio original. Este programa no importa server.py ni lee
credenciales, logs de evidencia o configuración del servicio original.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


def load_steps(path: Path, seq_filter: str | None = None) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = [json.loads(line) for line in text.splitlines() if line.strip()]
    if isinstance(value, dict):
        value = value["steps"] if isinstance(value.get("steps"), list) else [value]
    if not isinstance(value, list) or not value:
        raise ValueError(f"{path}: se esperaba un array no vacío o un objeto con steps.")
    if seq_filter is not None:
        value = [step for step in value if isinstance(step, dict) and str(step.get("seq")) == seq_filter]
        if not value:
            raise ValueError(f"{path}: no hay pasos para seq={seq_filter!r}.")
    normalized = []
    for index, step in enumerate(value, 1):
        if not isinstance(step, dict) or not isinstance(step.get("request"), dict):
            raise ValueError(f"{path}: paso {index} debe contener un objeto request.")
        item = dict(step)
        request = dict(step["request"])
        # Admite filas del log/ejemplos del reto: request es el body, method/path
        # viven en la fila (o se asume POST /msg en ejemplos.jsonl).
        if not any(key in request for key in ("method", "path", "body", "raw_body")):
            item["request"] = {
                "method": str(step.get("method", "POST")).upper(),
                "path": str(step.get("path", "/msg")),
                "body": request,
            }
        else:
            request.setdefault("method", str(step.get("method", "POST")).upper())
            request.setdefault("path", str(step.get("path", "/msg")))
            item["request"] = request
        normalized.append(item)
    return normalized


def json_equal(left: Any, right: Any) -> bool:
    """Compara JSON estructuralmente; la igualdad de dict ignora el orden de claves."""
    return type(left) is type(right) and left == right


def divergence(index: int, field: str, expected: Any, actual: Any) -> dict[str, Any]:
    return {"ok": False, "first_divergence": {
        "step": index, "field": field, "expected": expected, "actual": actual,
    }}


def compare_offline(sequence: list[dict[str, Any]], fixture: list[dict[str, Any]]) -> dict[str, Any]:
    """Compara captura candidate (requests + outputs) frente a una fixture, sin red."""
    count = min(len(sequence), len(fixture))
    for index in range(count):
        candidate, expected = sequence[index], fixture[index]
        if not request_equal(candidate["request"], expected["request"]):
            return divergence(index + 1, "request", expected["request"], candidate["request"])
        for field in ("status", "response"):
            if field not in candidate:
                return divergence(index + 1, field, expected.get(field), "<ausente en secuencia>")
            if not json_equal(candidate[field], expected.get(field)):
                return divergence(index + 1, field, expected.get(field), candidate[field])
    if len(sequence) != len(fixture):
        return divergence(count + 1, "step_count", len(fixture), len(sequence))
    return {"ok": True, "mode": "offline", "steps_compared": count}


def request_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return json_equal(left, right)


def local_url(base_url: str, path: str) -> str:
    parsed = urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("Modo replica solo permite un host loopback (localhost/127.0.0.1/::1).")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("base-url no puede incluir credenciales, query ni fragmento.")
    if not path.startswith("/") or path.startswith("//"):
        raise ValueError("Cada request debe usar un path local que empiece con una sola barra.")
    return base_url.rstrip("/") + path


def send_local(base_url: str, request_spec: dict[str, Any], timeout: float, token_env: str | None = None) -> tuple[int, Any]:
    method = str(request_spec.get("method", "POST")).upper()
    if method not in {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}:
        raise ValueError(f"Método no permitido en runner: {method}")
    path = str(request_spec.get("path", "/msg"))
    url = local_url(base_url, path)
    headers = {"Accept": "application/json"}
    data = None
    if "raw_body" in request_spec:
        raw = request_spec["raw_body"]
        if not isinstance(raw, str):
            raise ValueError("raw_body debe ser texto.")
        data = raw.encode("utf-8")
        headers["Content-Type"] = str(request_spec.get("content_type", "application/json"))
    elif "body" in request_spec:
        data = json.dumps(request_spec["body"], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = str(request_spec.get("content_type", "application/json"))
    token = os.environ.get(token_env, "") if token_env else ""
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        response = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        payload = response.read(1_000_001)
        if len(payload) > 1_000_000:
            raise ValueError("El cuerpo de respuesta local excede 1 MB.")
        text = payload.decode("utf-8", errors="strict")
        try:
            body = json.loads(text)
        except json.JSONDecodeError:
            body = text
        return response.status, body


def compare_replica(base_url: str, sequence: list[dict[str, Any]], fixture: list[dict[str, Any]], timeout: float, token_env: str | None = None) -> dict[str, Any]:
    if len(sequence) != len(fixture):
        return divergence(min(len(sequence), len(fixture)) + 1, "step_count", len(fixture), len(sequence))
    for index, (step, expected) in enumerate(zip(sequence, fixture), 1):
        if not request_equal(step["request"], expected["request"]):
            return divergence(index, "request", expected["request"], step["request"])
        try:
            status, body = send_local(base_url, step["request"], timeout, token_env)
        except Exception as error:  # error local explícito; no reintenta mutaciones
            return divergence(index, "transport", "respuesta HTTP local", f"{type(error).__name__}: {error}")
        if status != expected.get("status"):
            return divergence(index, "status", expected.get("status"), status)
        if not json_equal(body, expected.get("response")):
            return divergence(index, "response", expected.get("response"), body)
    return {"ok": True, "mode": "replica", "steps_compared": len(sequence)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compara una réplica local con fixtures, o dos capturas offline.")
    parser.add_argument("--mode", choices=("offline", "replica"), required=True)
    parser.add_argument("--sequence", type=Path, required=True, help="Secuencia JSON o JSONL candidata.")
    parser.add_argument("--fixture", type=Path, required=True, help="Fixture de referencia JSON o JSONL.")
    parser.add_argument("--fixture-seq", help="Filtra filas JSONL por su campo seq (útil con logs observados).")
    parser.add_argument("--token-env", help="Variable de entorno cuyo token se envía solo a la réplica loopback.")
    parser.add_argument("--base-url", help="URL de la réplica local; solo loopback, requerido en modo replica.")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout por paso en segundos (default: 5).")
    args = parser.parse_args(argv)
    try:
        sequence = load_steps(args.sequence)
        fixture = load_steps(args.fixture, args.fixture_seq)
        if args.mode == "offline":
            result = compare_offline(sequence, fixture)
        else:
            if not args.base_url:
                raise ValueError("--base-url es obligatorio en modo replica.")
            local_url(args.base_url, "/")
            result = compare_replica(args.base_url, sequence, fixture, args.timeout, args.token_env)
        result["mode"] = args.mode
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        return 0 if result["ok"] else 1
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
