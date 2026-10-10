"""Fuzzer propio y acotado: genera mutaciones de una variable; no envía nada."""

from __future__ import annotations

import argparse
import json


SEED = "ALTA;Lucia;82"
MUTATIONS = [
    ("control no numérico", "ALTA;Lucia;8X"),
    ("control vecino inferior", "ALTA;Lucia;81"),
    ("control vecino superior", "ALTA;Lucia;83"),
    ("comando minúscula", "alta;Lucia;82"),
    ("comando con espacio final", "ALTA ;Lucia;82"),
    ("campo nombre vacío", "ALTA;;82"),
    ("separador extra", "ALTA;Lucia;82;"),
    ("separador faltante", "ALTA;Lucia82"),
    ("control vacío", "ALTA;Lucia;"),
]


def cases(limit: int) -> list[dict]:
    return [
        {"method": "POST", "path": "/msg", "body": {"m": value},
         "hypothesis": "Mutación controlada: " + label + " frente a " + SEED}
        for label, value in MUTATIONS[:limit]
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=9)
    parser.add_argument("--scenario", action="store_true", help="Preparar JSON para /api/run, con reset; no envía requests")
    args = parser.parse_args()
    if not 1 <= args.limit <= 9:
        parser.error("--limit debe estar entre 1 y 9")
    generated = cases(args.limit)
    if args.scenario:
        generated = {"seq": "fuzz-alta-controlado", "steps": [
            {"method": "POST", "path": "/__reset", "body": {}, "hypothesis": "Aislar secuencia de mutaciones"},
            *generated,
        ]}
    print(json.dumps(generated, ensure_ascii=False, indent=2))
