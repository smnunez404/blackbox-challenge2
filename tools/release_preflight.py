"""Comprueba el paquete de entrega sin consultar ningún servicio externo."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "output" / "experimentos.jsonl"
SPEC = ROOT / "docs" / "especificacion-provisional.md"
RUNTIME = (ROOT / "services" / "replica" / "domain.py",
           ROOT / "services" / "replica" / "http_server.py")
REQUIRED_LOG_FIELDS = {"id", "seq", "x_req", "hipotesis", "request", "status", "response"}
SECTION_TITLES = (
    "Entrada", "Integridad", "Comandos", "Memoria entre requests",
    "Errores", "Cambios durante el día", "Riesgos",
)
RULE_ROW = re.compile(r"^\|\s*([A-Z]{2}-\d{2})\s*\|")
EVIDENCE_NUMBER = re.compile(r"(?<!\d)(\d{1,3})(?:[–-](\d{1,3}))?(?!\d)")
TOKEN_PATTERN = re.compile(r"(?:cn-p-[A-Za-z0-9_-]{10,}|ftr_[A-Za-z0-9_-]{16,})")


def main() -> int:
    errors: list[str] = []
    try:
        raw_log = LOG.read_text(encoding="utf-8-sig")
        spec = SPEC.read_text(encoding="utf-8-sig")
        runtime_sources = [path.read_text(encoding="utf-8") for path in RUNTIME]
    except OSError as error:
        print(f"ERROR: archivo requerido inaccesible: {error.filename}")
        return 1

    rows: list[dict] = []
    for line_number, line in enumerate(raw_log.splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"Log línea {line_number}: JSON inválido")
            continue
        if not isinstance(row, dict):
            errors.append(f"Log línea {line_number}: se esperaba un objeto")
            continue
        if row.get("id") != line_number:
            errors.append(f"Log línea {line_number}: ID ausente o fuera de orden")
        missing = REQUIRED_LOG_FIELDS - row.keys()
        if missing:
            errors.append(f"Log línea {line_number}: faltan {', '.join(sorted(missing))}")
        rows.append(row)

    if not rows:
        errors.append("El log no contiene observaciones")
    for number, title in enumerate(SECTION_TITLES, 1):
        if not re.search(rf"^## {number}\. {re.escape(title)}\s*$", spec, re.MULTILINE):
            errors.append(f"Especificación: falta sección {number}. {title}")

    rule_ids: list[str] = []
    for line in spec.splitlines():
        match = RULE_ROW.match(line)
        if not match:
            continue
        rule_ids.append(match.group(1))
        cells = line.split("|")
        if len(cells) < 6:
            errors.append(f"Especificación {match.group(1)}: tabla incompleta")
            continue
        evidence, confidence = cells[3].strip(), cells[4].strip().lower()
        if confidence.startswith(("confirmado", "probable")):
            cited = []
            for citation in EVIDENCE_NUMBER.finditer(evidence):
                first = int(citation.group(1))
                last = int(citation.group(2)) if citation.group(2) else first
                if last < first:
                    errors.append(f"Especificación {match.group(1)}: rango de evidencia invertido")
                cited.extend((first, last))
            if not cited:
                errors.append(f"Especificación {match.group(1)}: confianza sin ID del log")
            elif any(value < 1 or value > len(rows) for value in cited):
                errors.append(f"Especificación {match.group(1)}: cita fuera del log")

    duplicates = sorted(name for name, count in Counter(rule_ids).items() if count > 1)
    if duplicates:
        errors.append("Especificación: IDs duplicados: " + ", ".join(duplicates))
    if not rule_ids:
        errors.append("La especificación no contiene reglas tabuladas")

    for path, source in zip(RUNTIME, runtime_sources):
        if "FRONTIER_ORIGINAL_TOKEN" in source or "FRONTIER_BASE_URL" in source or "caja-negra-production" in source:
            errors.append(f"Runtime {path.name}: referencia al servicio original")
    for name, content in (("log", raw_log), ("especificación", spec)):
        if TOKEN_PATTERN.search(content):
            errors.append(f"{name}: posible credencial incrustada")

    missing_x_req = sum(row.get("x_req") is None for row in rows)
    missing_status = sum(row.get("status") is None for row in rows)
    print(f"Log: {len(rows)} líneas; x_req nulos: {missing_x_req}; status nulos: {missing_status}")
    print(f"Especificación: {len(rule_ids)} reglas; siete secciones comprobadas")
    print(f"Runtime: {len(RUNTIME)} archivos inspeccionados; errores: {len(errors)}")
    for error in errors:
        print("ERROR: " + error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
