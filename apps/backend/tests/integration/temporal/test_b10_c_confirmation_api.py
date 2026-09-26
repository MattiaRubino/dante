"""B10-C public API proof for Confirmation over Outcome material state."""

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

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _actual_command(operation_id: str, *, expected: str | None = None, occurred: bool = True) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "expected_material_state_ref": expected,
        "realization_occurred": occurred,
        "timing": None,
        "session_bases": [],
    }


def _outcome_command(
    operation_id: str,
    *,
    actual_state_ref: str,
    disposition_code: str,
    expected: str | None = None,
) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "actual_realization_material_state_ref": actual_state_ref,
        "expected_material_state_ref": expected,
        "disposition_code": disposition_code,
    }


def _confirmation_command(
    operation_id: str,
    *,
    outcome_state_ref: str,
    purpose_code: str,
    stance_code: str,
    expected: str | None = None,
) -> dict[str, object]:
    return {
        "operation_id": operation_id,
        "outcome_disposition_material_state_ref": outcome_state_ref,
        "expected_material_state_ref": expected,
        "purpose_code": purpose_code,
        "stance_code": stance_code,
    }


def test_b10_c_confirmation_is_idempotent_multi_actor_and_outcome_state_pinned(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    alice_email = "b10c.alice@example.com"
    bob_email = "b10c.bob@example.com"
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
            json={"operation_id": "b10c:event", "title": "Review meeting", "life_area_ref": area},
            headers=alice_headers,
        )
        assert event.status_code == 201
        event_ref = event.json()["event_ref"]
        actual = alice_client.post(
            f"/api/v1/temporal/events/{event_ref}/actual",
            json=_actual_command("b10c:event:actual"),
            headers=alice_headers,
        )
        assert actual.status_code == 201
        actual_ref = actual.json()["actual_ref"]
        actual_state_ref = actual.json()["material_state_ref"]
        outcome = alice_client.post(
            f"/api/v1/temporal/actuals/{actual_ref}/outcome",
            json=_outcome_command(
                "b10c:outcome",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.deferred",
            ),
            headers=alice_headers,
        )
        assert outcome.status_code == 201
        outcome_ref = outcome.json()["outcome_ref"]
        outcome_state_ref = outcome.json()["material_state_ref"]
        path = f"/api/v1/temporal/outcomes/{outcome_ref}/confirmations"

        empty = alice_client.get(path, headers=_base_headers())
        assert empty.status_code == 200
        assert empty.json() == []

        missing_csrf = alice_client.post(
            path,
            json=_confirmation_command(
                "b10c:no-csrf",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="attested",
            ),
            headers=_base_headers(),
        )
        assert missing_csrf.status_code == 403
        assert missing_csrf.json()["code"] == "security.csrf_failed"

        created = alice_client.post(
            path,
            json=_confirmation_command(
                "b10c:alice:create",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="attested",
            ),
            headers=alice_headers,
        )
        assert created.status_code == 201
        first = created.json()
        assert first["outcome_ref"] == outcome_ref
        assert first["outcome_disposition_material_state_ref"] == outcome_state_ref
        assert first["purpose_code"] == "review.personal"
        assert first["stance_code"] == "attested"
        assert first["confirmer_is_self"] is True
        assert first["replayed"] is False
        assert "confirmed" not in first

        replay = alice_client.post(
            path,
            json=_confirmation_command(
                "b10c:alice:create",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="attested",
            ),
            headers=alice_headers,
        )
        assert replay.status_code == 200
        assert replay.json()["replayed"] is True
        assert replay.json()["material_state_ref"] == first["material_state_ref"]

        reused = alice_client.post(
            path,
            json=_confirmation_command(
                "b10c:alice:create",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="retracted",
                expected=first["material_state_ref"],
            ),
            headers=alice_headers,
        )
        assert reused.status_code == 409
        assert reused.json()["code"] == "temporal.confirmation.operation_id_reused"

        corrected = alice_client.post(
            path,
            json=_confirmation_command(
                "b10c:alice:correct",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="retracted",
                expected=first["material_state_ref"],
            ),
            headers=alice_headers,
        )
        assert corrected.status_code == 201
        second = corrected.json()
        assert second["confirmation_ref"] == first["confirmation_ref"]
        assert second["material_state_ref"] != first["material_state_ref"]
        assert second["stance_code"] == "retracted"

        stale = alice_client.post(
            path,
            json=_confirmation_command(
                "b10c:alice:stale",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="attested",
                expected=first["material_state_ref"],
            ),
            headers=alice_headers,
        )
        assert stale.status_code == 409
        assert stale.json()["code"] == "temporal.confirmation.current_conflict"

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as bob_client:
        bob_csrf = _signin(bob_client, bob_email)
        bob_headers = {**_base_headers(), CSRF_HEADER_NAME: bob_csrf}
        bob_created = bob_client.post(
            path,
            json=_confirmation_command(
                "b10c:bob:create",
                outcome_state_ref=outcome_state_ref,
                purpose_code="review.personal",
                stance_code="disputed",
            ),
            headers=bob_headers,
        )
        assert bob_created.status_code == 201
        bob_body = bob_created.json()
        assert bob_body["confirmation_ref"] != first["confirmation_ref"]
        assert bob_body["confirmer_is_self"] is True
        assert bob_body["stance_code"] == "disputed"

        bob_list = bob_client.get(path, headers=_base_headers())
        assert bob_list.status_code == 404
        assert bob_list.json()["code"] == "temporal.confirmation.not_found"

        bob_history = bob_client.get(
            f"/api/v1/temporal/confirmations/{bob_body['confirmation_ref']}/history",
            headers=_base_headers(),
        )
        assert bob_history.status_code == 200
        assert [row["stance_code"] for row in bob_history.json()] == ["disputed"]

        alice_history_as_bob = bob_client.get(
            f"/api/v1/temporal/confirmations/{first['confirmation_ref']}/history",
            headers=_base_headers(),
        )
        assert alice_history_as_bob.status_code == 404

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as alice_client:
        alice_csrf = _signin(alice_client, alice_email)
        alice_headers = {**_base_headers(), CSRF_HEADER_NAME: alice_csrf}
        listed = alice_client.get(path, headers=_base_headers())
        assert listed.status_code == 200
        rows = listed.json()
        assert {row["confirmation_ref"] for row in rows} == {
            first["confirmation_ref"],
            bob_body["confirmation_ref"],
        }

        history = alice_client.get(
            f"/api/v1/temporal/confirmations/{first['confirmation_ref']}/history",
            headers=_base_headers(),
        )
        assert history.status_code == 200
        assert [row["stance_code"] for row in history.json()] == ["attested", "retracted"]

        corrected_outcome = alice_client.post(
            f"/api/v1/temporal/actuals/{actual_ref}/outcome",
            json=_outcome_command(
                "b10c:outcome:correct",
                actual_state_ref=actual_state_ref,
                disposition_code="decision.reached",
                expected=outcome_state_ref,
            ),
            headers=alice_headers,
        )
        assert corrected_outcome.status_code == 201
        new_outcome_state = corrected_outcome.json()["material_state_ref"]
        assert new_outcome_state != outcome_state_ref

        still = alice_client.get(path, headers=_base_headers())
        assert still.status_code == 200
        assert {
            row["outcome_disposition_material_state_ref"]
            for row in still.json()
            if row["confirmation_ref"] == first["confirmation_ref"]
        } == {outcome_state_ref}

        on_new = alice_client.post(
            path,
            json=_confirmation_command(
                "b10c:alice:new-state",
                outcome_state_ref=new_outcome_state,
                purpose_code="review.personal",
                stance_code="attested",
            ),
            headers=alice_headers,
        )
        assert on_new.status_code == 201
        assert on_new.json()["confirmation_ref"] != first["confirmation_ref"]
        assert on_new.json()["outcome_disposition_material_state_ref"] == new_outcome_state
