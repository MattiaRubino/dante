"""B10-D public API proof for Outcome-owner reconciliation."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app
from tests.integration.temporal.b05_legacy_test_support import api_test_life_area
from tests.integration.temporal.test_b01_activity_core import (
    _CANONICAL_ORIGIN,
    _auth_settings,
    _base_headers,
    _seed_account,
    _settings,
    _signin,
)
from tests.integration.temporal.test_b10_c_confirmation_api import (
    _actual_command,
    _confirmation_command,
    _outcome_command,
)

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _reconciliation_command(
    operation_id: str,
    *,
    outcome_state_ref: str,
    action_code: str,
    evidence: list[dict[str, str]],
    expected: str | None = None,
) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "outcome_disposition_material_state_ref": outcome_state_ref,
        "expected_material_state_ref": expected,
        "purpose_code": "review.personal",
        "action_code": action_code,
        "evidence": evidence,
    }


def _evidence(confirmation: dict[str, object], role: str) -> dict[str, str]:
    return {
        "confirmation_ref": str(confirmation["confirmation_ref"]),
        "confirmation_attestation_material_state_ref": str(confirmation["material_state_ref"]),
        "role_code": role,
    }


def test_b10_d_reconciliation_is_owner_only_idempotent_and_evidence_pinned(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    alice_email = "b10d.alice@example.com"
    bob_email = "b10d.bob@example.com"
    auth_settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, alice_email)
    _seed_account(migrated_database, auth_settings, bob_email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as alice_client:
        alice_csrf = _signin(alice_client, alice_email)
        alice_headers = {**_base_headers(), CSRF_HEADER_NAME: alice_csrf}
        area = api_test_life_area(alice_client, alice_headers)
        event = alice_client.post(
            "/api/v1/temporal/events",
            json={"operation_id": "b10d:event", "title": "Resolve evidence", "life_area_ref": area},
            headers=alice_headers,
        )
        assert event.status_code == 201
        event_ref = event.json()["event_ref"]
        actual = alice_client.post(
            f"/api/v1/temporal/events/{event_ref}/actual",
            json=_actual_command("b10d:actual"),
            headers=alice_headers,
        )
        assert actual.status_code == 201
        actual_ref = actual.json()["actual_ref"]
        actual_state_ref = actual.json()["material_state_ref"]
        outcome = alice_client.post(
            f"/api/v1/temporal/actuals/{actual_ref}/outcome",
            json=_outcome_command(
                "b10d:outcome",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.deferred",
            ),
            headers=alice_headers,
        )
        assert outcome.status_code == 201
        outcome_ref = outcome.json()["outcome_ref"]
        outcome_state_ref = outcome.json()["material_state_ref"]
        confirmation_path = f"/api/v1/temporal/outcomes/{outcome_ref}/confirmations"
        reconciliation_path = f"/api/v1/temporal/outcomes/{outcome_ref}/reconciliations"

        alice_confirmation_response = alice_client.post(
            confirmation_path,
            json=_confirmation_command(
                "b10d:alice:confirmation",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="attested",
            ),
            headers=alice_headers,
        )
        assert alice_confirmation_response.status_code == 201
        alice_confirmation = alice_confirmation_response.json()

        empty = alice_client.get(reconciliation_path, headers=_base_headers())
        assert empty.status_code == 200
        assert empty.json() == []

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as bob_client:
        bob_csrf = _signin(bob_client, bob_email)
        bob_headers = {**_base_headers(), CSRF_HEADER_NAME: bob_csrf}
        bob_confirmation_response = bob_client.post(
            confirmation_path,
            json=_confirmation_command(
                "b10d:bob:confirmation",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="disputed",
            ),
            headers=bob_headers,
        )
        assert bob_confirmation_response.status_code == 201
        bob_confirmation = bob_confirmation_response.json()

        forbidden_by_scope = bob_client.post(
            reconciliation_path,
            json=_reconciliation_command(
                "b10d:bob:resolve",
                outcome_state_ref=outcome_state_ref,
                action_code="unresolved",
                evidence=[],
            ),
            headers=bob_headers,
        )
        assert forbidden_by_scope.status_code == 404
        assert forbidden_by_scope.json()["code"] == "temporal.reconciliation.not_found"

        bob_list = bob_client.get(reconciliation_path, headers=_base_headers())
        assert bob_list.status_code == 404

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as alice_client:
        alice_csrf = _signin(alice_client, alice_email)
        alice_headers = {**_base_headers(), CSRF_HEADER_NAME: alice_csrf}
        payload = _reconciliation_command(
            "b10d:select",
            outcome_state_ref=outcome_state_ref,
            action_code="select",
            evidence=[
                _evidence(bob_confirmation, "considered"),
                _evidence(alice_confirmation, "selected"),
            ],
        )

        missing_csrf = alice_client.post(
            reconciliation_path,
            json=payload,
            headers=_base_headers(),
        )
        assert missing_csrf.status_code == 403
        assert missing_csrf.json()["code"] == "security.csrf_failed"

        created = alice_client.post(
            reconciliation_path,
            json=payload,
            headers=alice_headers,
        )
        assert created.status_code == 201
        first = created.json()
        assert first["outcome_ref"] == outcome_ref
        assert first["outcome_disposition_material_state_ref"] == outcome_state_ref
        assert first["purpose_code"] == "review.personal"
        assert first["action_code"] == "select"
        assert first["replayed"] is False
        assert "resolved" not in first
        assert "truth" not in first
        assert {row["role_code"] for row in first["evidence"]} == {"considered", "selected"}

        replay_payload = _reconciliation_command(
            "b10d:select",
            outcome_state_ref=outcome_state_ref,
            action_code="select",
            evidence=[
                _evidence(alice_confirmation, "selected"),
                _evidence(bob_confirmation, "considered"),
            ],
        )
        replay = alice_client.post(
            reconciliation_path,
            json=replay_payload,
            headers=alice_headers,
        )
        assert replay.status_code == 200
        assert replay.json()["replayed"] is True
        assert replay.json()["material_state_ref"] == first["material_state_ref"]

        invalid = alice_client.post(
            reconciliation_path,
            json=_reconciliation_command(
                "b10d:bad-select",
                outcome_state_ref=outcome_state_ref,
                action_code="select",
                evidence=[_evidence(bob_confirmation, "considered")],
                expected=first["material_state_ref"],
            ),
            headers=alice_headers,
        )
        assert invalid.status_code == 422
        assert invalid.json()["code"] == "temporal.reconciliation.invalid_input"

        corrected = alice_client.post(
            reconciliation_path,
            json=_reconciliation_command(
                "b10d:accept-both",
                outcome_state_ref=outcome_state_ref,
                action_code="accept_multiple",
                evidence=[
                    _evidence(alice_confirmation, "selected"),
                    _evidence(bob_confirmation, "selected"),
                ],
                expected=first["material_state_ref"],
            ),
            headers=alice_headers,
        )
        assert corrected.status_code == 201
        second = corrected.json()
        assert second["reconciliation_ref"] == first["reconciliation_ref"]
        assert second["material_state_ref"] != first["material_state_ref"]
        assert second["action_code"] == "accept_multiple"

        stale = alice_client.post(
            reconciliation_path,
            json=_reconciliation_command(
                "b10d:stale",
                outcome_state_ref=outcome_state_ref,
                action_code="unresolved",
                evidence=[],
                expected=first["material_state_ref"],
            ),
            headers=alice_headers,
        )
        assert stale.status_code == 409
        assert stale.json()["code"] == "temporal.reconciliation.current_conflict"

        listed = alice_client.get(reconciliation_path, headers=_base_headers())
        assert listed.status_code == 200
        assert len(listed.json()) == 1
        assert listed.json()[0]["material_state_ref"] == second["material_state_ref"]

        history = alice_client.get(
            f"/api/v1/temporal/reconciliations/{first['reconciliation_ref']}/history",
            headers=_base_headers(),
        )
        assert history.status_code == 200
        history_rows = history.json()
        assert [row["action_code"] for row in history_rows] == ["select", "accept_multiple"]
        assert history_rows[0]["current_until_at"] is not None
        assert history_rows[1]["current_until_at"] is None
