"""Comprobaciones del auditor HTTP local, sin tráfico al original."""

from __future__ import annotations

import unittest

from audit_http_observed import audit_http_rows


class HttpObservedAuditTests(unittest.TestCase):
    def test_reset_then_ping_matches(self) -> None:
        rows = [
            {"id": 1, "seq": "sample", "method": "POST", "path": "/__reset",
             "auth_mode": "valid", "status": 200, "response": {"ok": True}},
            {"id": 2, "seq": "sample", "method": "POST", "path": "/msg",
             "auth_mode": "valid", "request_raw": '{"m":"PING;64"}',
             "status": 200, "response": {"pong": True}},
        ]
        report = audit_http_rows(rows)
        self.assertEqual((report["compared"], report["matched"], report["mismatches"]),
                         (2, 2, []))

    def test_detects_first_bad_observation(self) -> None:
        rows = [
            {"id": 1, "seq": "sample", "method": "POST", "path": "/__reset",
             "auth_mode": "valid", "status": 200, "response": {"ok": True}},
            {"id": 2, "seq": "sample", "method": "POST", "path": "/msg",
             "auth_mode": "valid", "request_raw": '{"m":"PING;64"}',
             "status": 400, "response": {"wrong": True}},
        ]
        report = audit_http_rows(rows)
        self.assertEqual(report["matched"], 1)
        self.assertEqual([item["id"] for item in report["mismatches"]], [2])

    def test_without_observed_reset_skips_stateful_msg(self) -> None:
        rows = [{"id": 1, "seq": "sample", "method": "POST", "path": "/msg",
                 "auth_mode": "valid", "request_raw": '{"m":"PING;64"}',
                 "status": 200, "response": {"pong": True}}]
        report = audit_http_rows(rows)
        self.assertEqual(report["compared"], 0)
        self.assertEqual(report["skipped"]["no-observed-reset"], 1)


if __name__ == "__main__":
    unittest.main()
