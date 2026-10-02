"""The Home queue follows current self-owned B10 truth without queue storage."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient
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
from tests.integration.temporal.test_b10_d_reconciliation_api import (
    _evidence,
    _reconciliation_command,
)

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def test_resolution_queue_follows_canonical_reconciliation_and_self_scope(
    migrated_database: Any,
    activity_hibp_stub_url: str,
) -> None:
    email = "u6.queue.alice@example.com"
    other_email = "u6.queue.bob@example.com"
    settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, settings, email)
    _seed_account(migrated_database, settings, other_email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        queue_path = "/api/v1/temporal/resolution-queue"
        initial = client.get(queue_path, headers=_base_headers())
        assert initial.status_code == 200
        assert initial.json() == {"items": [], "count": 0}

        activity = client.post(
            "/api/v1/temporal/authoring/activities",
            json={"operation_id": "u6:queue:activity", "title": "Review the evidence"},
            headers=headers,
        )
        assert activity.status_code == 201
        subject_ref = activity.json()["activity_ref"]
        assert client.get(queue_path, headers=_base_headers()).json()["count"] == 0

        actual = client.post(
            f"/api/v1/temporal/activities/{subject_ref}/actual",
            json=_actual_command("u6:queue:actual"),
            headers=headers,
        )
        assert actual.status_code == 201
        assert client.get(queue_path, headers=_base_headers()).json()["count"] == 0

        outcome = client.post(
            f"/api/v1/temporal/actuals/{actual.json()['actual_ref']}/outcome",
            json=_outcome_command(
                "u6:queue:outcome",
                actual_state_ref=actual.json()["material_state_ref"],
                disposition_code="work.partial",
            ),
            headers=headers,
        )
        assert outcome.status_code == 201
        outcome_ref = outcome.json()["outcome_ref"]
        outcome_state = outcome.json()["material_state_ref"]
        assert client.get(queue_path, headers=_base_headers()).json()["count"] == 0

        confirmation = client.post(
            f"/api/v1/temporal/outcomes/{outcome_ref}/confirmations",
            json=_confirmation_command(
                "u6:queue:confirmation", outcome_state_ref=outcome_state,
                purpose_code="review.personal", stance_code="attested",
            ),
            headers=headers,
        )
        assert confirmation.status_code == 201
        reconciliation_path = f"/api/v1/temporal/outcomes/{outcome_ref}/reconciliations"
        opened = client.post(
            reconciliation_path,
            json=_reconciliation_command(
                "u6:queue:open", outcome_state_ref=outcome_state,
                action_code="unresolved", evidence=[],
            ),
            headers=headers,
        )
        assert opened.status_code == 201
        item = client.get(queue_path, headers=_base_headers()).json()
        assert item["count"] == 1
        assert item["items"] == [{
            "reason_code": "reconciliation_open",
            "subject_kind": "activity",
            "subject_ref": subject_ref,
            "title": "Review the evidence",
            "reconciliation_ref": opened.json()["reconciliation_ref"],
            "outcome_ref": outcome_ref,
            "purpose_code": "review.personal",
        }]

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as other:
        _signin(other, other_email)
        assert other.get(queue_path, headers=_base_headers()).json() == {
            "items": [], "count": 0,
        }

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, email)
        headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        resolved = client.post(
            reconciliation_path,
            json=_reconciliation_command(
                "u6:queue:resolve", outcome_state_ref=outcome_state,
                action_code="select", evidence=[_evidence(confirmation.json(), "selected")],
                expected=opened.json()["material_state_ref"],
            ),
            headers=headers,
        )
        assert resolved.status_code == 201
        assert client.get(queue_path, headers=_base_headers()).json() == {
            "items": [], "count": 0,
        }
