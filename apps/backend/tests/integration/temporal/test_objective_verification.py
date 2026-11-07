"""Objective verification: independent saved policy, optimistic edits and replay."""

from __future__ import annotations

from typing import Any
from uuid import UUID

import psycopg
import pytest
from fastapi.testclient import TestClient
from tests.integration.temporal.test_activity_core import (
    _CANONICAL_ORIGIN,
    _auth_settings,
    _base_headers,
    _seed_account,
    _settings,
    _signin,
)

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_activity_core",)


@pytest.mark.parametrize("initial_mode", ["none", "review_on_end"])
def test_objective_verification_persists_independently_and_replays(
    migrated_database: Any,
    activity_hibp_stub_url: str,
    initial_mode: str,
) -> None:
    """The Objective mode survives list/reload and is not Activity completion."""
    email = f"objective.verification.{initial_mode}@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        headers = {**_base_headers(), CSRF_HEADER_NAME: _signin(client, email)}
        activity_response = client.post(
            "/api/v1/temporal/authoring/activities",
            json={
                "operation_id": f"objective:verification:{initial_mode}:activity",
                "title": "Allenamento",
            },
            headers=headers,
        )
        assert activity_response.status_code == 201, activity_response.text
        activity_ref = activity_response.json()["activity_ref"]
        endpoint = f"/api/v1/temporal/activities/{activity_ref}/objectives"
        command = {
            "operation_id": f"objective:verification:{initial_mode}:create",
            "label": "Correre",
            "result_kind": "quantity",
            "comparator_code": "gte",
            "target_value": 5,
            "unit_code": "km",
            "presentation_order": 0,
            "verification_mode": initial_mode,
        }
        created = client.post(endpoint, json=command, headers=headers)
        assert created.status_code == 201, created.text
        objective_ref = created.json()["objective_ref"]
        assert created.json()["verification_mode"] == initial_mode

        replay = client.post(endpoint, json=command, headers=headers)
        assert replay.status_code == 200, replay.text
        assert replay.json()["objective_ref"] == objective_ref
        assert replay.json()["verification_mode"] == initial_mode

        listing = client.get(endpoint, headers=_base_headers())
        assert listing.status_code == 200, listing.text
        assert len(listing.json()) == 1
        assert listing.json()[0]["verification_mode"] == initial_mode

        definition_path = f"/api/v1/temporal/objectives/{objective_ref}/definition"
        definition = client.get(definition_path, headers=_base_headers())
        assert definition.status_code == 200, definition.text
        assert definition.json()["verification_mode"] == initial_mode
        assert definition.json()["verification_revision"] == (
            0 if initial_mode == "none" else 1
        )
        assert definition.json()["definition_revision"] == 0

        target = "review_on_end" if initial_mode == "none" else "none"
        edit = {
            "operation_id": f"objective:verification:{initial_mode}:edit",
            "expected_revision": 0,
            "expected_verification_revision": definition.json()["verification_revision"],
            "label": "Correre",
            "result_kind": "quantity",
            "comparator_code": "gte",
            "target_value": 5,
            "unit_code": "km",
            "presentation_order": 0,
            "verification_mode": target,
        }
        changed = client.put(definition_path, json=edit, headers=headers)
        assert changed.status_code == 200, changed.text
        changed_state = client.get(definition_path, headers=_base_headers())
        assert changed_state.status_code == 200, changed_state.text
        assert changed_state.json()["verification_mode"] == target
        assert changed_state.json()["verification_revision"] == (
            edit["expected_verification_revision"] + 1
        )
        assert (
            client.put(definition_path, json=edit, headers=headers).status_code
            == 200
        )
        assert (
            client.get(definition_path, headers=_base_headers()).json()[
                "verification_revision"
            ]
            == edit["expected_verification_revision"] + 1
        )
        with psycopg.connect(
            host=migrated_database.cluster.host,
            port=migrated_database.cluster.port,
            dbname=migrated_database.name,
            user=migrated_database.cluster.admin_user,
            password=migrated_database.cluster.admin_password,
        ) as connection:
            revisions = connection.execute(
                "SELECT mode_code FROM dante.temporal_objective_verification_revision "
                "WHERE objective_ref=%s ORDER BY revision",
                (UUID(objective_ref),),
            ).fetchall()
            assert [value[0] for value in revisions] == (
                [target] if initial_mode == "none" else [initial_mode, target]
            )


def test_objective_verification_rejects_unsupported_auto_mode(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    """No fabricated automatic Objective result without an evidence source."""
    email = "objective.verification.automatic@example.com"
    _seed_account(migrated_database, _auth_settings(activity_hibp_stub_url), email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        headers = {**_base_headers(), CSRF_HEADER_NAME: _signin(client, email)}
        activity_response = client.post(
            "/api/v1/temporal/authoring/activities",
            json={"operation_id": "objective:verification:auto:activity", "title": "Sport"},
            headers=headers,
        )
        assert activity_response.status_code == 201, activity_response.text
        activity_ref = activity_response.json()["activity_ref"]
        denied = client.post(
            f"/api/v1/temporal/activities/{activity_ref}/objectives",
            json={
                "operation_id": "objective:verification:auto:objective",
                "label": "Correre",
                "result_kind": "boolean",
                "presentation_order": 0,
                "verification_mode": "auto_if_evidence",
            },
            headers=headers,
        )
        assert denied.status_code == 422, denied.text
