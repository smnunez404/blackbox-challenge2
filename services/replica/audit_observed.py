"""Replay logged black-box observations against the local model, offline only."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from domain import Model


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG = ROOT / "output" / "experimentos.jsonl"


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as source:
        for line_no, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSON inválido en línea {line_no}: {exc.msg}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"La línea {line_no} no contiene un objeto JSON")
            rows.append(row)
    return rows


def audit_rows(rows: list[dict[str, Any]], only_seq: str | None = None) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        seq = row.get("seq")
        if not isinstance(seq, str) or not seq:
            continue
        if only_seq is None or seq == only_seq:
            grouped[seq].append(row)

    summary: dict[str, Any] = {
        "sequences": len(grouped),
        "compared": 0,
        "matched": 0,
        "mismatches": [],
        "skipped": defaultdict(int),
    }

    for seq, events in grouped.items():
        model = Model()
        initialized = False
        for row in events:
            row_id = row.get("id")
            method = row.get("method", "POST")
            path = row.get("path", "/msg")
            auth_mode = row.get("auth_mode", "valid")
            status_expected = row.get("status")
            body_expected = row.get("response")
            response_raw = row.get("response_raw")
            if isinstance(response_raw, str):
                try:
                    body_expected = json.loads(response_raw)
                except json.JSONDecodeError:
                    pass

            if status_expected is None:
                summary["skipped"]["unconfirmed-response"] += 1
                initialized = False
                continue

            # Authentication and other HTTP-layer observations are covered by
            # HTTP tests, not by this domain-model replay. In particular, an
            # unauthorized reset must not mutate the replay state.
            if auth_mode != "valid":
                summary["skipped"]["outside-domain-audit"] += 1
                continue

            if method == "POST" and path == "/__reset":
                model.reset()
                initialized = status_expected == 200 and body_expected == {"ok": True}
                status_actual, body_actual = 200, {"ok": True}
            elif method == "POST" and path == "/msg":
                if not initialized:
                    summary["skipped"]["no-observed-reset"] += 1
                    continue
                request = row.get("request")
                if not isinstance(request, dict) or not isinstance(request.get("m"), str):
                    summary["skipped"]["not-a-domain-message"] += 1
                    initialized = False
                    continue
                status_actual, body_actual = model.process(request["m"])
            else:
                summary["skipped"]["outside-domain-audit"] += 1
                initialized = False
                continue

            summary["compared"] += 1
            # A few historical captures contain U+FFFD from a local encoding
            # fault. Preserve/compare their trustworthy status and stable JSON
            # fields, but do not invent the corrupted text field.
            if isinstance(response_raw, str) and ("\ufffd" in response_raw or "Ã" in response_raw):
                summary["skipped"]["capture-corrupt-text-field"] += 1
                if isinstance(body_expected, dict) and isinstance(body_actual, dict):
                    body_expected = {key: value for key, value in body_expected.items() if key != "mensaje"}
                    body_actual = {key: value for key, value in body_actual.items() if key != "mensaje"}

            if status_actual == status_expected and body_actual == body_expected:
                summary["matched"] += 1
            else:
                summary["mismatches"].append({
                    "id": row_id,
                    "seq": seq,
                    "request": row.get("request"),
                    "expected": {"status": status_expected, "response": body_expected},
                    "actual": {"status": status_actual, "response": body_actual},
                })

    summary["skipped"] = dict(summary["skipped"])
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audita el modelo local contra observaciones ya registradas; no hace red."
    )
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG,
                        help="JSONL canónico de experimentos (por defecto: output/experimentos.jsonl)")
    parser.add_argument("--seq", help="Limita la auditoría a un identificador de secuencia")
    parser.add_argument("--since-id", type=int, default=723,
                        help="Audita desde este ID (por defecto 723, inicio del replay de incidente V2)")
    parser.add_argument("--json", action="store_true", help="Emite el informe como JSON")
    args = parser.parse_args()

    try:
        rows = [row for row in load_rows(args.log) if int(row.get("id", 0)) >= args.since_id]
        report = audit_rows(rows, args.seq)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Secuencias: {report['sequences']}")
        print(f"Observaciones comparables: {report['compared']}; coincidencias: {report['matched']}; "
              f"divergencias: {len(report['mismatches'])}")
        if report["skipped"]:
            print("Omitidas: " + ", ".join(f"{key}={value}" for key, value in sorted(report["skipped"].items())))
        for mismatch in report["mismatches"]:
            print(json.dumps(mismatch, ensure_ascii=False, separators=(",", ":")))
    return 1 if report["mismatches"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
