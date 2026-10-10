"""Pruebas locales de modelo y HTTP; no contactan al servicio original."""

from __future__ import annotations

import http.client
import json
import threading
import unittest
from pathlib import Path

from domain import Model
from http_server import ReplicaHTTPServer


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "raw" / "referencias" / "frontier-reto-2" / "pruebas" / "ejemplos.jsonl"

V2_EXAMPLE_OVERRIDES = {
    5: (200, {"saldo": "0.00", "cuenta_id": "AC-0001"}),
    8: (200, {"saldo": "400.00", "cuenta_id": "AC-0002"}),
    10: (422, {"error": "E506", "mensaje": "límite excedido"}),
    11: (200, {"saldo": "2100.00", "cuenta_id": "AC-0001"}),
    13: (404, {"error": "E402", "mensaje": "operación inexistente"}),
    14: (404, {"error": "E402", "mensaje": "operación inexistente"}),
    18: (200, {"status": "recieved", "operacionId": "OP-0003"}),
    19: (200, {"saldo": "407.00", "cuenta_id": "AC-0002"}),
}


def expected_v2(row: dict) -> tuple[int, dict]:
    number = int(str(row.get("n", row.get("id"))).lstrip("0") or "0")
    return V2_EXAMPLE_OVERRIDES.get(number, (row["status"], row["response"]))


class DomainTests(unittest.TestCase):
    def test_official_twenty_step_sequence_matches_v2_incident_replay(self) -> None:
        rows = [json.loads(line) for line in EXAMPLES.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        self.assertEqual(len(rows), 20)
        model = Model()
        model.reset()
        for row in rows:
            with self.subTest(example=row.get("n", row.get("id")), request=row["request"]):
                self.assertIsInstance(row["request"].get("m"), str)
                status, body = model.process(row["request"]["m"])
                expected_status, expected_body = expected_v2(row)
                self.assertEqual(status, expected_status)
                self.assertEqual(body, expected_body)

    def test_reset_restarts_both_id_sequences(self) -> None:
        model = Model()
        self.assertEqual(model.process("ALTA;Lucia;82"), (201, {"cuentaId": "AC-0001"}))
        self.assertEqual(model.process("ALTA;Mateo;3"), (201, {"cuentaId": "AC-0002"}))
        self.assertEqual(model.process("DEPOSITO;AC-0001;250000;86"),
                         (200, {"status": "recieved", "operacionId": "OP-0001"}))
        model.reset()
        self.assertEqual(model.process("ALTA;Lucia;82"), (201, {"cuentaId": "AC-0001"}))
        self.assertEqual(model.process("ALTA;Mateo;3"), (201, {"cuentaId": "AC-0002"}))
        self.assertEqual(model.process("DEPOSITO;AC-0002;700;35"),
                         (200, {"status": "recieved", "operacionId": "OP-0001"}))

    def test_observed_control_candidate_and_annul_state(self) -> None:
        model = Model()
        self.assertEqual(model.process("CONSULTA;AC-0003;8"),
                         (404, {"error": "E401", "mensaje": "cuenta inexistente"}))
        self.assertEqual(model.process("CONSULTA;AC-0003;9"),
                         (400, {"error": "E202", "mensaje": "control inválido"}))
        model.process("ALTA;Lucia;82")
        model.process("ALTA;Mateo;3")
        model.process("DEPOSITO;AC-0002;700;35")
        self.assertEqual(model.process("ANULA;OP-0001;72"),
                         (200, {"ok": True, "anulada": "OP-0001"}))
        self.assertEqual(model.process("CONSULTA;AC-0002;11"),
                         (200, {"saldo": "0.00", "cuenta_id": "AC-0002"}))
        self.assertEqual(model.process("ANULA;OP-0001;72"),
                         (200, {"ok": False, "motivo": "ya anulada"}))

    def test_observed_validation_precedence_cases(self) -> None:
        model = Model()
        self.assertEqual(model.process("ALTA;Lucia;Gomez;5X"),
                         (400, {"error": "E201", "mensaje": "control mal formado"}))
        self.assertEqual(model.process("ALTA;Lucia;Gomez;11"),
                         (400, {"error": "E302", "mensaje": "aridad inválida"}))
        self.assertEqual(model.process("PING;64;X"),
                         (400, {"error": "E302", "mensaje": "aridad inválida"}))
        self.assertEqual(model.process("CONSULTA;;14"),
                         (400, {"error": "E104", "mensaje": "segmento vacío"}))

    def test_deposit_control_rejections_do_not_consume_operation_ids(self) -> None:
        model = Model()
        model.process("ALTA;Lucia;82")
        model.process("ALTA;Mateo;3")
        self.assertEqual(model.process("DEPOSITO;AC-0002;700;35"),
                         (200, {"status": "recieved", "operacionId": "OP-0001"}))
        for control in (83, 86):
            with self.subTest(control=control):
                self.assertEqual(model.process(f"DEPOSITO;AC-0002;250000;{control}"),
                                 (400, {"error": "E202", "mensaje": "control inválido"}))
        self.assertEqual(model.process("DEPOSITO;AC-0001;250000;86"),
                         (200, {"status": "recieved", "operacionId": "OP-0002"}))

    def test_observed_alta_vectors_and_exact_account_lookup(self) -> None:
        model = Model()
        self.assertEqual(model.process("ALTA;Lucia;82"),
                         (201, {"cuentaId": "AC-0001"}))
        self.assertEqual(model.process("ALTA; Lucia;82"),
                         (201, {"cuentaId": "AC-0002"}))
        self.assertEqual(model.process("ALTA;Mateo;3"),
                         (201, {"cuentaId": "AC-0003"}))

        second_model = Model()
        self.assertEqual(second_model.process("ALTA;Lucia;82"),
                         (201, {"cuentaId": "AC-0001"}))
        self.assertEqual(second_model.process("ALTA;Lucib;79"),
                         (201, {"cuentaId": "AC-0002"}))
        self.assertEqual(second_model.process("ALTA;Lucic;76"),
                         (201, {"cuentaId": "AC-0003"}))

        v2_model = Model()
        self.assertEqual(v2_model.process("ALTA;Lucia;82"),
                         (201, {"cuentaId": "AC-0001"}))
        self.assertEqual(v2_model.process("ALTA;Lucid;73"),
                         (201, {"cuentaId": "AC-0002"}))

        self.assertEqual(model.process("CONSULTA;AC-0001;14"),
                         (200, {"saldo": "0.00", "cuenta_id": "AC-0001"}))
        for spelling in ("ac-0001", " AC-0001"):
            with self.subTest(spelling=spelling):
                self.assertEqual(model.process(f"CONSULTA;{spelling};14"),
                                 (404, {"error": "E401", "mensaje": "cuenta inexistente"}))

    def test_transfer_control_observations_and_precedence(self) -> None:
        model = Model()
        model.process("ALTA;Lucia;82")
        model.process("ALTA;Mateo;3")
        self.assertEqual(model.process("DEPOSITO;AC-0001;250000;86"),
                         (200, {"status": "recieved", "operacionId": "OP-0001"}))

        invalid_vectors = (
            "TRANSFER;AC-0001;AC-0009;40000;86",
            "TRANSFER;AC-0001;AC-0002;100001;12",
            "TRANSFER;AC-0002;AC-0001;10000;23",
            "TRANSFER;AC-0001;AC-0002;40000;87",
        )
        for message in invalid_vectors:
            with self.subTest(message=message):
                self.assertEqual(model.process(message),
                                 (400, {"error": "E202", "mensaje": "control inválido"}))

        self.assertEqual(model.process("TRANSFER;AC-0001;AC-0002;40000;86"),
                         (200, {"status": "recieved", "operacionId": "OP-0002"}))
        self.assertEqual(model.process("TRANSFER;AC-0001;AC-0002;100000;12"),
                         (422, {"error": "E506", "mensaje": "límite excedido"}))
        self.assertEqual(model.process("TRANSFER;AC-0002;AC-0001;50000;23"),
                         (422, {"error": "E507", "mensaje": "saldo insuficiente"}))
        self.assertEqual(model.process("CONSULTA;AC-0001;14"),
                         (200, {"saldo": "2100.00", "cuenta_id": "AC-0001"}))
        self.assertEqual(model.process("CONSULTA;AC-0002;11"),
                         (200, {"saldo": "400.00", "cuenta_id": "AC-0002"}))

        no_funds = Model()
        no_funds.process("ALTA;Lucia;82")
        no_funds.process("ALTA;Mateo;3")
        self.assertEqual(no_funds.process("TRANSFER;AC-0001;AC-0002;120000;55"),
                         (422, {"error": "E506", "mensaje": "límite excedido"}))

    def test_annul_transfer_after_receiver_spent_part_of_credit(self) -> None:
        model = Model()
        observed = [
            ("ALTA;Lucia;82", 201, {"cuentaId": "AC-0001"}),
            ("ALTA;Mateo;3", 201, {"cuentaId": "AC-0002"}),
            ("DEPOSITO;AC-0001;250000;86", 200,
             {"status": "recieved", "operacionId": "OP-0001"}),
            ("TRANSFER;AC-0001;AC-0002;40000;86", 200,
             {"status": "recieved", "operacionId": "OP-0002"}),
            ("TRANSFER;AC-0001;AC-0002;40000;86", 200,
             {"status": "recieved", "operacionId": "OP-0003"}),
            ("TRANSFER;AC-0002;AC-0001;50000;23", 200,
             {"status": "recieved", "operacionId": "OP-0004"}),
            ("CONSULTA;AC-0002;11", 200, {"saldo": "300.00", "cuenta_id": "AC-0002"}),
            ("ANULA;OP-0003;66", 200, {"ok": True, "anulada": "OP-0003"}),
            ("CONSULTA;AC-0001;14", 200, {"saldo": "2600.00", "cuenta_id": "AC-0001"}),
            ("CONSULTA;AC-0002;11", 200, {"saldo": "-100.00", "cuenta_id": "AC-0002"}),
        ]
        for message, expected_status, expected_body in observed:
            with self.subTest(message=message):
                self.assertEqual(model.process(message), (expected_status, expected_body))

    def test_huge_positive_amount_uses_conservative_default_without_crashing(self) -> None:
        model = Model()
        model.process("ALTA;Lucia;82")
        amount = "9" * 4_301
        self.assertEqual(
            model.process(f"DEPOSITO;AC-0001;{amount};86"),
            (400, {"error": "E202", "mensaje": "control inválido"}),
        )

    def test_huge_numeric_control_uses_conservative_default_without_crashing(self) -> None:
        model = Model()
        control = "9" * 4_301
        self.assertEqual(model.process(f"ALTA;Lucia;{control}"),
                         (400, {"error": "E202", "mensaje": "control inválido"}))


class HTTPTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = ReplicaHTTPServer(("127.0.0.1", 0), "unit-test-team-token", Model())
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)

    def tearDown(self) -> None:
        self.connection.close()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def request(self, method: str, path: str, body: bytes | None = None,
                token: str | None = "unit-test-team-token", content_type: str | None = "application/json"):
        headers = {}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        if content_type is not None:
            headers["Content-Type"] = content_type
        self.connection.request(method, path, body=body, headers=headers)
        response = self.connection.getresponse()
        raw = response.read()
        parsed = json.loads(raw) if raw else None
        return response.status, parsed

    def test_health_reset_auth_and_unknown_route(self) -> None:
        self.assertEqual(self.request("GET", "/health"), (200, {"ok": True}))
        self.assertEqual(self.request("GET", "/health", token=None),
                         (401, {"error": "E001", "mensaje": "no autorizado"}))
        self.assertEqual(self.request("POST", "/__reset", b"{}"), (200, {"ok": True}))
        self.assertEqual(self.request("GET", "/missing"),
                         (404, {"error": "E404", "mensaje": "ruta desconocida"}))
        self.assertEqual(self.request("GET", "/missing", token=None),
                         (404, {"error": "E404", "mensaje": "ruta desconocida"}))
        self.assertEqual(self.request("POST", "/missing", b"{}", token="wrong-token"),
                         (404, {"error": "E404", "mensaje": "ruta desconocida"}))

    def test_json_parse_and_auth_precede_parse(self) -> None:
        self.assertEqual(self.request("POST", "/msg", b"{"),
                         (400, {"error": "E100", "mensaje": "json inválido"}))
        self.assertEqual(self.request("POST", "/msg", b"{" , token=None),
                         (401, {"error": "E001", "mensaje": "no autorizado"}))
        self.assertEqual(self.request("POST", "/msg", b"[]"),
                         (400, {"error": "E102", "mensaje": "falta m"}))

    def test_http_replays_official_examples_as_v2(self) -> None:
        rows = [json.loads(line) for line in EXAMPLES.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        self.assertEqual(self.request("POST", "/__reset", b"{}"), (200, {"ok": True}))
        for row in rows:
            body = json.dumps(row["request"], ensure_ascii=False).encode("utf-8")
            status, result = self.request("POST", "/msg", body, content_type="text/plain")
            with self.subTest(example=row.get("n", row.get("id"))):
                expected_status, expected_body = expected_v2(row)
                self.assertEqual(status, expected_status)
                self.assertEqual(result, expected_body)

    def test_head_and_wrong_route_method_use_json_404(self) -> None:
        self.assertEqual(self.request("GET", "/msg"),
                         (404, {"error": "E404", "mensaje": "ruta desconocida"}))
        status, body = self.request("HEAD", "/not-here")
        self.assertEqual(status, 404)
        self.assertIsNone(body)

    def test_non_ascii_authorization_is_rejected_without_dropping_connection(self) -> None:
        self.assertEqual(self.request("GET", "/health", token="ñ"),
                         (401, {"error": "E001", "mensaje": "no autorizado"}))

    def test_huge_numeric_amount_returns_a_response_instead_of_server_error(self) -> None:
        self.request("POST", "/__reset", b"{}")
        self.request("POST", "/msg", b'{"m":"ALTA;Lucia;82"}')
        amount = "9" * 4_301
        body = json.dumps({"m": f"DEPOSITO;AC-0001;{amount};86"}).encode()
        self.assertEqual(self.request("POST", "/msg", body),
                         (400, {"error": "E202", "mensaje": "control inválido"}))

    def test_idle_keepalive_client_does_not_block_another_client(self) -> None:
        self.assertEqual(self.request("GET", "/health"), (200, {"ok": True}))
        second = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=1)
        try:
            second.request("GET", "/health", headers={"Authorization": "Bearer unit-test-team-token"})
            response = second.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), {"ok": True})
        finally:
            second.close()


if __name__ == "__main__":
    unittest.main()
