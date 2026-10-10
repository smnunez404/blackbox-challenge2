"""Tests for the strictly offline replay of the experiment journal."""

import unittest

from audit_observed import audit_rows


class AuditObservedTests(unittest.TestCase):
    def test_unauthorized_reset_is_not_applied_to_replay_state(self) -> None:
        rows = [
            {"seq": "auth", "id": 1, "method": "POST", "path": "/__reset",
             "auth_mode": "valid", "status": 200, "response": {"ok": True}},
            {"seq": "auth", "id": 2, "method": "POST", "path": "/msg",
             "auth_mode": "valid", "request": {"m": "ALTA;Lucia;82"},
             "status": 201, "response": {"cuentaId": "AC-0001"}},
            {"seq": "auth", "id": 3, "method": "POST", "path": "/__reset",
             "auth_mode": "missing", "status": 401,
             "response": {"error": "E001", "mensaje": "no autorizado"}},
            {"seq": "auth", "id": 4, "method": "POST", "path": "/msg",
             "auth_mode": "valid", "request": {"m": "CONSULTA;AC-0001;14"},
             "status": 200, "response": {"saldo": "0.00", "cuenta_id": "AC-0001"}},
        ]

        report = audit_rows(rows)

        self.assertEqual(report["compared"], 3)
        self.assertEqual(report["matched"], 3)
        self.assertEqual(report["mismatches"], [])
        self.assertEqual(report["skipped"]["outside-domain-audit"], 1)

    def test_mojibake_capture_compares_only_trustworthy_fields(self) -> None:
        rows = [
            {"seq": "encoding", "id": 1, "method": "POST", "path": "/__reset",
             "status": 200, "response": {"ok": True}},
            {"seq": "encoding", "id": 2, "method": "POST", "path": "/msg",
             "request": {"m": "ALTA;Lucia;83"}, "status": 400,
             "response": {"error": "E202", "mensaje": "control inv\ufffdlido"},
             "response_raw": "{\"error\":\"E202\",\"mensaje\":\"control inv\ufffdlido\"}"},
        ]

        report = audit_rows(rows)

        self.assertEqual(report["compared"], 2)
        self.assertEqual(report["matched"], 2)
        self.assertEqual(report["mismatches"], [])
        self.assertEqual(report["skipped"]["capture-corrupt-text-field"], 1)

    def test_domain_observations_without_reset_are_not_replayed(self) -> None:
        rows = [{"seq": "unknown-state", "id": 1, "method": "POST", "path": "/msg",
                 "request": {"m": "CONSULTA;AC-0001;14"}, "status": 200,
                 "response": {"saldo": 0, "cuenta_id": "AC-0001"}}]

        report = audit_rows(rows)

        self.assertEqual(report["compared"], 0)
        self.assertEqual(report["skipped"]["no-observed-reset"], 1)

    def test_failed_reset_does_not_initialize_replay_state(self) -> None:
        rows = [
            {"seq": "reset-failure", "id": 1, "method": "POST", "path": "/__reset",
             "status": 200, "response": {"ok": True}},
            {"seq": "reset-failure", "id": 2, "method": "POST", "path": "/__reset",
             "status": 503, "response": {"error": "unavailable"}},
            {"seq": "reset-failure", "id": 3, "method": "POST", "path": "/msg",
             "request": {"m": "CONSULTA;AC-0001;14"}, "status": 200,
             "response": {"saldo": 0, "cuenta_id": "AC-0001"}},
        ]

        report = audit_rows(rows)

        self.assertEqual(report["compared"], 2)
        self.assertEqual(len(report["mismatches"]), 1)
        self.assertEqual(report["mismatches"][0]["id"], 2)
        self.assertEqual(report["skipped"]["no-observed-reset"], 1)

    def test_unmodeled_request_invalidates_replay_state_until_next_reset(self) -> None:
        rows = [
            {"seq": "unknown-request", "id": 1, "method": "POST", "path": "/__reset",
             "status": 200, "response": {"ok": True}},
            {"seq": "unknown-request", "id": 2, "method": "POST", "path": "/msg",
             "request": {"m": 42}, "status": 400, "response": {"error": "E102"}},
            {"seq": "unknown-request", "id": 3, "method": "POST", "path": "/msg",
             "request": {"m": "CONSULTA;AC-0001;14"}, "status": 200,
             "response": {"saldo": 0, "cuenta_id": "AC-0001"}},
        ]

        report = audit_rows(rows)

        self.assertEqual(report["compared"], 1)
        self.assertEqual(report["skipped"]["not-a-domain-message"], 1)
        self.assertEqual(report["skipped"]["no-observed-reset"], 1)
