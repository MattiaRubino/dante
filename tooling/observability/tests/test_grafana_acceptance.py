from __future__ import annotations

import json
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

from tooling.observability import grafana_acceptance as acceptance


class _FakeClient:
    def __init__(self, responses: list[acceptance.ApiResponse]) -> None:
        self.responses = responses
        self.calls: list[tuple[str, str, Any]] = []

    def request(
        self,
        method: str,
        path: str,
        payload: Any = None,
        *,
        accepted: Any = (200,),
    ) -> acceptance.ApiResponse:
        del accepted
        self.calls.append((method, path, payload))
        return self.responses.pop(0)


class GrafanaAcceptanceTests(unittest.TestCase):
    def test_dashboard_materialization_replaces_every_datasource_input(self) -> None:
        source = {
            "__inputs": [{"name": "DS_PROMETHEUS"}],
            "id": 99,
            "uid": "dante-test",
            "panels": [
                {
                    "id": 1,
                    "datasource": {"uid": "${DS_PROMETHEUS}"},
                    "targets": [{"expr": "up", "refId": "A"}],
                },
                {
                    "id": 2,
                    "datasource": {"uid": "${DS_LOKI}"},
                    "targets": [],
                },
            ],
        }

        materialized = acceptance._materialize_dashboard(
            source,
            {"prometheus": "metrics-uid", "loki": "logs-uid", "tempo": "traces-uid"},
        )

        self.assertNotIn("__inputs", materialized)
        self.assertIsNone(materialized["id"])
        self.assertEqual(materialized["panels"][0]["datasource"]["uid"], "metrics-uid")
        self.assertEqual(materialized["panels"][1]["datasource"]["uid"], "logs-uid")
        self.assertIn("__inputs", source)
        self.assertEqual(source["id"], 99)

    def test_alert_catalog_has_exact_numeric_query_contract(self) -> None:
        catalog = json.loads(acceptance._ALERT_CATALOG.read_text(encoding="utf-8"))

        self.assertEqual(catalog["schema_version"], 2)
        self.assertEqual(len(catalog["rules"]), 8)
        rules = {rule["id"]: rule for rule in catalog["rules"]}
        unavailable = rules["dante-backend-unavailable"]
        alloy = rules["dante-alloy-missing"]
        self.assertNotIn("== 0", unavailable["expr"])
        self.assertEqual(unavailable["evaluator"], {"type": "lt", "threshold": 1})
        self.assertIn("max_over_time", alloy["expr"])
        self.assertEqual(alloy["evaluator"], {"type": "lt", "threshold": 1})
        self.assertEqual(unavailable["no_data_state"], "alerting")
        self.assertEqual(alloy["no_data_state"], "alerting")

    def test_rule_payload_keeps_query_evaluator_and_receiver_separate(self) -> None:
        rule = {
            "id": "dante-example",
            "title": "Example",
            "severity": "critical",
            "expr": "max_over_time(up[5m])",
            "lookback_seconds": 360,
            "evaluator": {"type": "lt", "threshold": 1},
            "for": "2m",
            "no_data_state": "alerting",
            "description": "Example description",
            "runbook_anchor": "example",
        }

        payload = acceptance._rule_payload(rule, "metrics-uid", "DANTE Operations")

        self.assertEqual(payload["condition"], "C")
        self.assertEqual(payload["data"][0]["model"]["expr"], rule["expr"])
        evaluator = payload["data"][2]["model"]["conditions"][0]["evaluator"]
        self.assertEqual(evaluator, {"params": [1.0], "type": "lt"})
        self.assertEqual(payload["noDataState"], "Alerting")
        self.assertEqual(payload["data"][1]["model"]["settings"], {"mode": "dropNN"})
        self.assertEqual(
            payload["notification_settings"]["receiver"], "DANTE Operations"
        )

    def test_rule_signature_accepts_numeric_normalization(self) -> None:
        source = acceptance._synthetic_rule("metrics-uid", "DANTE Operations")
        stored = json.loads(json.dumps(source))
        stored["data"][2]["model"]["conditions"][0]["evaluator"]["params"] = [0]

        self.assertEqual(
            acceptance._rule_signature(source), acceptance._rule_signature(stored)
        )

    def test_token_file_must_be_private_and_single_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            token_file = Path(directory) / "token.local"
            token_file.write_text("x" * 32, encoding="utf-8")
            token_file.chmod(0o644)
            with self.assertRaisesRegex(acceptance.AcceptanceFailure, "chmod 600"):
                acceptance._read_token(token_file)
            token_file.chmod(0o600)
            self.assertEqual(acceptance._read_token(token_file), "x" * 32)
            token_file.write_text(("x" * 32) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(acceptance.AcceptanceFailure, "whitespace"):
                acceptance._read_token(token_file)

    def test_cleanup_refuses_any_rule_without_exact_synthetic_identity(self) -> None:
        client = _FakeClient(
            [
                acceptance.ApiResponse(
                    200,
                    {
                        "uid": acceptance._SYNTHETIC_UID,
                        "title": acceptance._SYNTHETIC_TITLE,
                        "ruleGroup": acceptance._SYNTHETIC_GROUP,
                        "labels": {"environment": "prod"},
                    },
                )
            ]
        )

        with self.assertRaisesRegex(acceptance.AcceptanceFailure, "refusing to delete"):
            acceptance._cleanup_synthetic(client, True)
        self.assertEqual(len(client.calls), 1)

    def test_cleanup_deletes_and_verifies_only_the_exact_synthetic_rule(self) -> None:
        client = _FakeClient(
            [
                acceptance.ApiResponse(
                    200,
                    {
                        "uid": acceptance._SYNTHETIC_UID,
                        "title": acceptance._SYNTHETIC_TITLE,
                        "ruleGroup": acceptance._SYNTHETIC_GROUP,
                        "labels": {
                            "acceptance": "synthetic",
                            "environment": "local",
                        },
                    },
                ),
                acceptance.ApiResponse(204, None),
                acceptance.ApiResponse(404, None),
            ]
        )

        with redirect_stdout(io.StringIO()):
            acceptance._cleanup_synthetic(client, True)

        self.assertEqual([call[0] for call in client.calls], ["GET", "DELETE", "GET"])


if __name__ == "__main__":
    unittest.main()
