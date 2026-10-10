"""Reproduce observaciones elegibles por HTTP local; nunca contacta al original."""

from __future__ import annotations

import argparse
import http.client
import json
import threading
from collections import defaultdict
from pathlib import Path
from typing import Any

from audit_observed import DEFAULT_LOG, load_rows
from http_server import ReplicaHTTPServer


TOKEN = "local-audit-token-only"
# Estas filas investigan Content-Type, pero el log no conserva el header exacto.
# Reproducirlas con uno inventado exageraría el alcance de la auditoría.
UNKNOWN_HEADER_IDS = {87, 95, 96, 97, 105, 106, 107}


def send(port: int, row: dict[str, Any]) -> tuple[int, Any]:
    method = row.get("method") or "POST"
    path = row.get("path") or "/msg"
    mode = row.get("auth_mode", "valid")
    headers = {"Content-Type": "application/json"}
    if mode == "valid":
        headers["Authorization"] = "Bearer " + TOKEN
    elif mode == "invalid":
        headers["Authorization"] = "Bearer invalid-local-token"
    elif mode != "missing":
        raise ValueError(f"auth_mode no reproducible: {mode!r}")

    raw = row.get("request_raw")
    request = row.get("request")
    if raw is None and isinstance(request, dict) and "raw_body" in request:
        raw = request["raw_body"]
    if raw is None and isinstance(request, dict) and "m" in request:
        raw = json.dumps(request, ensure_ascii=False, separators=(",", ":"))
    data = raw.encode("utf-8") if isinstance(raw, str) else None

    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=3)
    try:
        connection.request(method, path, body=data, headers=headers)
        response = connection.getresponse()
        payload = response.read()
        if not payload:
            return response.status, ""
        decoded = payload.decode("utf-8")
        try:
            return response.status, json.loads(decoded)
        except json.JSONDecodeError:
            return response.status, decoded
    finally:
        connection.close()


def audit_http_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if isinstance(row.get("seq"), str) and row["seq"]:
            grouped[row["seq"]].append(row)

    summary: dict[str, Any] = {
        "sequences": len(grouped), "compared": 0, "matched": 0,
        "mismatches": [], "skipped": defaultdict(int),
    }
    server = ReplicaHTTPServer(("127.0.0.1", 0), TOKEN)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        for seq, events in grouped.items():
            with server.model_lock:
                server.model.reset()
            initialized = False
            for row in events:
                row_id = row.get("id")
                method = row.get("method") or "POST"
                path = row.get("path") or "/msg"
                mode = row.get("auth_mode", "valid")
                expected_status = row.get("status")
                expected_body = row.get("response")
                response_raw = row.get("response_raw")

                if expected_status is None:
                    summary["skipped"]["unconfirmed-response"] += 1
                    initialized = False
                    continue
                if row_id in UNKNOWN_HEADER_IDS:
                    summary["skipped"]["header-not-captured"] += 1
                    continue
                if method == "POST" and path == "/msg" and mode == "valid" and not initialized:
                    summary["skipped"]["no-observed-reset"] += 1
                    continue
                if method == "POST" and path == "/msg" and mode == "valid" and row.get("request_raw") is None:
                    summary["skipped"]["raw-request-not-captured"] += 1
                    initialized = False
                    continue
                if method not in {"GET", "POST", "HEAD", "PUT", "PATCH", "DELETE", "OPTIONS"}:
                    summary["skipped"]["method-not-supported-by-auditor"] += 1
                    initialized = False
                    continue

                observed_status, observed_body = send(server.server_port, row)
                if method == "POST" and path == "/__reset" and mode == "valid":
                    initialized = expected_status == 200 and expected_body == {"ok": True}

                if isinstance(response_raw, str):
                    try:
                        expected_body = json.loads(response_raw) if response_raw else ""
                    except json.JSONDecodeError:
                        pass
                if isinstance(response_raw, str) and ("\ufffd" in response_raw or "Ã" in response_raw):
                    summary["skipped"]["capture-corrupt-text-field"] += 1
                    if isinstance(expected_body, dict) and isinstance(observed_body, dict):
                        expected_body = {key: value for key, value in expected_body.items() if key != "mensaje"}
                        observed_body = {key: value for key, value in observed_body.items() if key != "mensaje"}

                summary["compared"] += 1
                if (observed_status, observed_body) == (expected_status, expected_body):
                    summary["matched"] += 1
                else:
                    summary["mismatches"].append({
                        "id": row_id, "seq": seq,
                        "expected": {"status": expected_status, "response": expected_body},
                        "actual": {"status": observed_status, "response": observed_body},
                    })
                    # A prior divergent state transition makes later steps of
                    # this sequence unsuitable as independent rule checks.
                    initialized = False
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)

    summary["skipped"] = dict(summary["skipped"])
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--since-id", type=int, default=723,
                        help="Audita desde este ID (por defecto 723, inicio del replay de incidente V2)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows = [row for row in load_rows(args.log) if int(row.get("id", 0)) >= args.since_id]
    report = audit_http_rows(rows)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Secuencias: {report['sequences']}")
        print(f"HTTP comparables: {report['compared']}; coincidencias: {report['matched']}; "
              f"divergencias: {len(report['mismatches'])}")
        print("Omitidas: " + ", ".join(f"{key}={value}" for key, value in sorted(report["skipped"].items())))
        for mismatch in report["mismatches"]:
            print(json.dumps(mismatch, ensure_ascii=False, separators=(",", ":")))
    return 1 if report["mismatches"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
