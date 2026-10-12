"""B09-D whole-block proof across public API, native Persons and PostgreSQL."""

from __future__ import annotations

from typing import Any

import psycopg
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


def test_b09_d_person_roles_remain_actor_local_and_expected_not_actual(
    migrated_database: Any, activity_hibp_stub_url: str
) -> None:
    """Exercise the product API as two real Accounts without creating Accounts for referents."""
    alice_email = "b09d.alice@example.com"
    bob_email = "b09d.bob@example.com"
    auth_settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, alice_email)
    _seed_account(migrated_database, auth_settings, bob_email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, alice_email)
        mutation_headers = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        area = api_test_life_area(client, mutation_headers)
        activity = client.post(
            "/api/v1/temporal/activities",
            json={"operation_id": "b09d:activity", "title": "Prepare meeting", "life_area_ref": area},
            headers=mutation_headers,
        )
        event = client.post(
            "/api/v1/temporal/events",
            json={"operation_id": "b09d:event", "title": "Meeting", "life_area_ref": area},
            headers=mutation_headers,
        )
        assert (activity.status_code, event.status_code) == (201, 201)
        activity_ref = activity.json()["activity_ref"]
        event_ref = event.json()["event_ref"]
        people_path = "/api/v1/temporal/person-referents"

        assert client.get(people_path, headers=_base_headers()).json() == []
        created = client.post(
            people_path,
            json={"operation_id": "b09d:person:anna", "display_label": "Anna"},
            headers=mutation_headers,
        )
        assert created.status_code == 201
        anna = created.json()["person_ref"]
        assert (created.json()["revision"], created.json()["replayed"]) == (1, False)
        replay = client.post(
            people_path,
            json={"operation_id": "b09d:person:anna", "display_label": "Anna"},
            headers=mutation_headers,
        )
        assert replay.status_code == 201
        assert (replay.json()["person_ref"], replay.json()["replayed"]) == (anna, True)
        changed_intent = client.post(
            people_path,
            json={"operation_id": "b09d:person:anna", "display_label": "Another"},
            headers=mutation_headers,
        )
        assert changed_intent.status_code == 409

        renamed = client.patch(
            f"{people_path}/{anna}",
            json={"operation_id": "b09d:person:rename", "display_label": "Anna Rossi", "expected_revision": 1},
            headers=mutation_headers,
        )
        assert renamed.status_code == 200
        assert (renamed.json()["person_ref"], renamed.json()["revision"]) == (anna, 2)
        stale = client.patch(
            f"{people_path}/{anna}",
            json={"operation_id": "b09d:person:stale", "display_label": "Anna Bianchi", "expected_revision": 1},
            headers=mutation_headers,
        )
        assert stale.status_code == 409
        assert [(p["person_ref"], p["display_label"]) for p in
                client.get(people_path, headers=_base_headers()).json()] == [(anna, "Anna Rossi")]

        activity_path = f"/api/v1/temporal/activities/{activity_ref}/responsibility"
        event_path = f"/api/v1/temporal/events/{event_ref}/responsibility"
        participation_path = f"/api/v1/temporal/events/{event_ref}/expected-participation"
        for path, op in ((activity_path, "b09d:activity:assign"),
                         (event_path, "b09d:event:assign")):
            assigned = client.put(
                path,
                json={"operation_id": op, "holder": anna, "expected_holder": None},
                headers=mutation_headers,
            )
            assert assigned.status_code == 200
            assert assigned.json()["responsible_person_ref"] == anna
            assert assigned.json()["responsible_is_self"] is False
            assert client.get(path, headers=_base_headers()).json()["responsible_person_ref"] == anna

        required = client.put(
            participation_path,
            json={"operation_id": "b09d:required", "participant": anna,
                  "requirement_code": "required", "expected_requirement_code": None},
            headers=mutation_headers,
        )
        assert required.status_code == 200
        assert (required.json()["requirement_code"], required.json()["participant_is_self"]) == ("required", False)
        changed = client.put(
            participation_path,
            json={"operation_id": "b09d:optional", "participant": anna,
                  "requirement_code": "optional", "expected_requirement_code": "required"},
            headers=mutation_headers,
        )
        assert changed.status_code == 200
        assert [p["requirement_code"] for p in client.get(
            participation_path, headers=_base_headers()
        ).json()] == ["optional"]

        cleared = client.put(
            event_path,
            json={"operation_id": "b09d:event:clear", "holder": None, "expected_holder": anna},
            headers=mutation_headers,
        )
        assert cleared.status_code == 200
        assert cleared.json()["responsible_person_ref"] is None
        # Clearing Event Responsibility does not change the independent participation relation.
        assert [p["requirement_code"] for p in client.get(
            participation_path, headers=_base_headers()
        ).json()] == ["optional"]
        removed = client.put(
            participation_path,
            json={"operation_id": "b09d:participation:remove", "participant": anna,
                  "requirement_code": None, "expected_requirement_code": "optional"},
            headers=mutation_headers,
        )
        assert removed.status_code == 200
        assert client.get(participation_path, headers=_base_headers()).json() == []
        assert client.get(activity_path, headers=_base_headers()).json()["responsible_person_ref"] == anna

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as other:
        other_csrf = _signin(other, bob_email)
        other_headers = {**_base_headers(), CSRF_HEADER_NAME: other_csrf}
        assert other.get(people_path, headers=_base_headers()).json() == []
        assert other.get(activity_path, headers=_base_headers()).status_code == 404
        assert other.get(event_path, headers=_base_headers()).status_code == 404
        assert other.get(participation_path, headers=_base_headers()).status_code == 404
        assert other.patch(
            f"{people_path}/{anna}",
            json={"operation_id": "b09d:bob:rename", "display_label": "Stolen", "expected_revision": 2},
            headers=other_headers,
        ).status_code == 404
        assert other.put(
            activity_path,
            json={"operation_id": "b09d:bob:assign", "holder": anna, "expected_holder": None},
            headers=other_headers,
        ).status_code == 404

    with psycopg.connect(
        host=migrated_database.cluster.host,
        port=migrated_database.cluster.port,
        dbname=migrated_database.name,
        user=migrated_database.cluster.admin_user,
        password=migrated_database.cluster.admin_password,
        autocommit=True,
    ) as connection:
        assert connection.execute(
            "SELECT owner_family FROM dante.native_address WHERE native_ref=%s", (anna,)
        ).fetchone() == ("person",)
        assert connection.execute(
            "SELECT count(*) FROM dante.account_application_context WHERE self_person_ref=%s", (anna,)
        ).fetchone() == (0,)
        assert connection.execute(
            "SELECT count(*) FROM dante.actual WHERE subject_native_ref IN (%s,%s)",
            (activity_ref, event_ref),
        ).fetchone() == (0,)
        assert connection.execute(
            "SELECT count(*) FROM dante.session_execution_subject WHERE subject_native_ref IN (%s,%s)",
            (activity_ref, event_ref),
        ).fetchone() == (0,)
