"""B09-B behavioral proof for guarded Responsibility and expected Participation."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest
from fastapi.testclient import TestClient
from tests.integration.temporal.b05_legacy_test_support import api_test_life_area
from tests.integration.temporal.test_b01_activity_core import (
    _CANONICAL_ORIGIN,
    _auth_settings,
    _base_headers,
    _seed_account,
    _settings,
    _signin,
)
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.auth.sessions import CSRF_HEADER_NAME
from dante.bootstrap.app import create_app
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.responsibility_participation import (
    ResponsibilityConflictError,
    ResponsibilityNotFoundError,
    ResponsibilityOperationReuseError,
    ResponsibilityParticipationApplication,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


@pytest.mark.asyncio
async def test_b09_b_activity_responsibility_is_self_scoped_guarded_and_idempotent(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    authoring = ResponsibilityParticipationApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice, operation_id="b09-b:area", name="Work"
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b09-b:activity",
                title="Prepare the quarterly review",
                life_area_ref=area.life_area_ref,
            )
        ).activity

        empty = await authoring.get_responsibility(
            self_person_ref=alice,
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert empty.responsible_person_ref is None
        assert empty.established_at is None

        assigned = await authoring.set_responsibility(
            self_person_ref=alice,
            operation_id="b09-b:assign",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            responsible_person_ref=alice,
            expected_responsible_person_ref=None,
        )
        assert assigned.responsible_person_ref == alice
        assert not assigned.replayed
        assert isinstance(assigned.established_at, datetime)

        replay = await authoring.set_responsibility(
            self_person_ref=alice,
            operation_id="b09-b:assign",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            responsible_person_ref=alice,
            expected_responsible_person_ref=None,
        )
        assert replay.replayed
        assert replay.responsible_person_ref == alice
        assert replay.established_at == assigned.established_at

        with pytest.raises(ResponsibilityOperationReuseError):
            await authoring.set_responsibility(
                self_person_ref=alice,
                operation_id="b09-b:assign",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                responsible_person_ref=None,
                expected_responsible_person_ref=alice,
            )

        # A stale expected holder must not silently overwrite the current one.
        with pytest.raises(ResponsibilityConflictError):
            await authoring.set_responsibility(
                self_person_ref=alice,
                operation_id="b09-b:stale",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                responsible_person_ref=None,
                expected_responsible_person_ref=None,
            )

        with pytest.raises(ResponsibilityConflictError):
            await authoring.set_responsibility(
                self_person_ref=alice,
                operation_id="b09-b:no-change",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                responsible_person_ref=alice,
                expected_responsible_person_ref=alice,
            )

        # Only a Person this actor may reference is admissible.
        with pytest.raises(ResponsibilityNotFoundError):
            await authoring.set_responsibility(
                self_person_ref=alice,
                operation_id="b09-b:foreign-person",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                responsible_person_ref=bob,
                expected_responsible_person_ref=alice,
            )

        with pytest.raises(ResponsibilityNotFoundError):
            await authoring.set_responsibility(
                self_person_ref=bob,
                operation_id="b09-b:foreign-subject",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                responsible_person_ref=bob,
                expected_responsible_person_ref=None,
            )
        with pytest.raises(ResponsibilityNotFoundError):
            await authoring.get_responsibility(
                self_person_ref=bob,
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
            )

        cleared = await authoring.set_responsibility(
            self_person_ref=alice,
            operation_id="b09-b:clear",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            responsible_person_ref=None,
            expected_responsible_person_ref=alice,
        )
        assert cleared.responsible_person_ref is None

        after_clear = await authoring.get_responsibility(
            self_person_ref=alice,
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert after_clear.responsible_person_ref is None

        with _admin(migrated_database) as connection:
            counts = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.activity_responsibility
                     WHERE activity_ref=%s),
                  (SELECT count(*) FROM dante.activity_responsibility_operation
                     WHERE self_person_ref=%s),
                  (SELECT count(*) FROM dante.event_expected_participation
                     WHERE event_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s)
                """,
                (activity.activity_ref, alice, activity.activity_ref, activity.activity_ref),
            ).fetchone()
        assert counts == (0, 2, 0, 0)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_b09_b_expected_participation_is_bounded_and_creates_no_attendance(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    authoring = ResponsibilityParticipationApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice, operation_id="b09-b:event-area", name="Team"
            )
        ).area
        event = (
            await events.create_event(
                self_person_ref=alice,
                operation_id="b09-b:event",
                title="Quarterly review",
                life_area_ref=area.life_area_ref,
            )
        ).event

        assert (
            await authoring.list_expected_participation(
                self_person_ref=alice, event_ref=event.event_ref
            )
            == ()
        )

        required = await authoring.set_expected_participation(
            self_person_ref=alice,
            operation_id="b09-b:participation",
            event_ref=event.event_ref,
            participant_person_ref=alice,
            requirement_code="required",
            expected_requirement_code=None,
        )
        assert required.requirement_code == "required"
        assert not required.replayed

        replay = await authoring.set_expected_participation(
            self_person_ref=alice,
            operation_id="b09-b:participation",
            event_ref=event.event_ref,
            participant_person_ref=alice,
            requirement_code="required",
            expected_requirement_code=None,
        )
        assert replay.replayed
        assert replay.established_at == required.established_at

        with pytest.raises(ResponsibilityConflictError):
            await authoring.set_expected_participation(
                self_person_ref=alice,
                operation_id="b09-b:participation-stale",
                event_ref=event.event_ref,
                participant_person_ref=alice,
                requirement_code="optional",
                expected_requirement_code=None,
            )

        # An unknown Person is not referenceable, and a Person is not an Account.
        with pytest.raises(ResponsibilityNotFoundError):
            await authoring.set_expected_participation(
                self_person_ref=alice,
                operation_id="b09-b:participation-unknown",
                event_ref=event.event_ref,
                participant_person_ref=NativeRef(uuid7()),
                requirement_code="optional",
                expected_requirement_code=None,
            )
        with pytest.raises(ResponsibilityNotFoundError):
            await authoring.list_expected_participation(
                self_person_ref=bob, event_ref=event.event_ref
            )

        changed = await authoring.set_expected_participation(
            self_person_ref=alice,
            operation_id="b09-b:participation-optional",
            event_ref=event.event_ref,
            participant_person_ref=alice,
            requirement_code="optional",
            expected_requirement_code="required",
        )
        assert changed.requirement_code == "optional"

        listed = await authoring.list_expected_participation(
            self_person_ref=alice, event_ref=event.event_ref
        )
        assert [(item.participant_person_ref, item.requirement_code) for item in listed] == [
            (alice, "optional")
        ]

        removed = await authoring.set_expected_participation(
            self_person_ref=alice,
            operation_id="b09-b:participation-remove",
            event_ref=event.event_ref,
            participant_person_ref=alice,
            requirement_code=None,
            expected_requirement_code="optional",
        )
        assert removed.requirement_code is None
        assert (
            await authoring.list_expected_participation(
                self_person_ref=alice, event_ref=event.event_ref
            )
            == ()
        )

        with _admin(migrated_database) as connection:
            counts = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.event_expected_participation
                     WHERE event_ref=%s),
                  (SELECT count(*) FROM dante.event_expected_participation_operation
                     WHERE self_person_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.session_execution_subject
                     WHERE subject_native_ref=%s),
                  (SELECT count(*) FROM dante.event_responsibility WHERE event_ref=%s)
                """,
                (event.event_ref, alice, event.event_ref, event.event_ref, event.event_ref),
            ).fetchone()
        # Expected Participation is not attendance, not an Actual, and not Responsibility.
        assert counts == (0, 3, 0, 0, 0)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_b09_b_event_responsibility_stays_distinct_from_participation(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    authoring = ResponsibilityParticipationApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice, operation_id="b09-b:event-resp-area", name="Ops"
            )
        ).area
        event = (
            await events.create_event(
                self_person_ref=alice,
                operation_id="b09-b:event-resp",
                title="Quarterly review ownership",
                life_area_ref=area.life_area_ref,
            )
        ).event

        assigned = await authoring.set_responsibility(
            self_person_ref=alice,
            operation_id="b09-b:event-assign",
            subject_kind="event",
            subject_native_ref=event.event_ref,
            responsible_person_ref=alice,
            expected_responsible_person_ref=None,
        )
        assert assigned.subject_kind == "event"
        assert assigned.responsible_person_ref == alice
        assert not assigned.replayed

        replay = await authoring.set_responsibility(
            self_person_ref=alice,
            operation_id="b09-b:event-assign",
            subject_kind="event",
            subject_native_ref=event.event_ref,
            responsible_person_ref=alice,
            expected_responsible_person_ref=None,
        )
        assert replay.replayed
        assert replay.established_at == assigned.established_at

        with pytest.raises(ResponsibilityNotFoundError):
            await authoring.get_responsibility(
                self_person_ref=bob,
                subject_kind="event",
                subject_native_ref=event.event_ref,
            )

        current = await authoring.get_responsibility(
            self_person_ref=alice,
            subject_kind="event",
            subject_native_ref=event.event_ref,
        )
        assert current.responsible_person_ref == alice
        assert (
            await authoring.list_expected_participation(
                self_person_ref=alice, event_ref=event.event_ref
            )
            == ()
        )

        with _admin(migrated_database) as connection:
            counts = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.event_responsibility WHERE event_ref=%s),
                  (SELECT count(*) FROM dante.event_responsibility_operation
                     WHERE self_person_ref=%s),
                  (SELECT count(*) FROM dante.event_expected_participation
                     WHERE event_ref=%s),
                  (SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s)
                """,
                (event.event_ref, alice, event.event_ref, event.event_ref),
            ).fetchone()
        assert counts == (1, 1, 0, 0)
    finally:
        await runtime.dispose()


def test_b09_b_operation_tables_are_not_raw_runtime_mutation_surfaces(
    migrated_database: Any,
) -> None:
    with _admin(migrated_database) as connection:
        for table in (
            "activity_responsibility_operation",
            "event_responsibility_operation",
            "event_expected_participation_operation",
        ):
            qualified = f"dante.{table}"
            assert connection.execute(
                "SELECT "
                "has_table_privilege('dante_runtime', %s, 'SELECT'),"
                "has_table_privilege('dante_runtime', %s, 'INSERT'),"
                "has_table_privilege('dante_runtime', %s, 'UPDATE'),"
                "has_table_privilege('dante_runtime', %s, 'DELETE')",
                (qualified, qualified, qualified, qualified),
            ).fetchone() == (False, False, False, False)

        for routine in (
            "set_self_activity_responsibility",
            "set_self_event_responsibility",
            "set_self_event_expected_participation",
            "get_self_activity_responsibility",
            "get_self_event_responsibility",
            "list_self_event_expected_participation",
        ):
            assert connection.execute(
                "SELECT count(*) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
                "WHERE n.nspname='dante' AND p.proname=%s AND p.prosecdef",
                (routine,),
            ).fetchone() == (1,)

        helper = "dante._self_referenceable_person(uuid,uuid)"
        helper_acl = connection.execute(
            """
            SELECT pg_get_userbyid(p.proowner), p.prosecdef,
                   has_function_privilege('dante_runtime', %s, 'EXECUTE'),
                   has_function_privilege('dante_migrator', %s, 'EXECUTE'),
                   EXISTS (
                     SELECT 1 FROM aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) AS acl
                     WHERE acl.grantee=0 AND acl.privilege_type='EXECUTE'
                   )
              FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
             WHERE n.nspname='dante'
               AND p.oid=to_regprocedure(%s)
            """,
            (helper, helper, helper),
        ).fetchone()
        assert helper_acl == ("dante_owner", False, False, False, False)

        for signature, result in (
            (
                "dante.set_self_activity_responsibility(uuid,text,text,uuid,uuid,uuid)",
                "TABLE(subject_native_ref uuid, responsible_person_ref uuid, "
                "established_at timestamp with time zone, replayed boolean)",
            ),
            (
                "dante.set_self_event_responsibility(uuid,text,text,uuid,uuid,uuid)",
                "TABLE(subject_native_ref uuid, responsible_person_ref uuid, "
                "established_at timestamp with time zone, replayed boolean)",
            ),
            (
                "dante.set_self_event_expected_participation(uuid,text,text,uuid,uuid,text,text)",
                "TABLE(event_ref uuid, participant_person_ref uuid, requirement_code text, "
                "established_at timestamp with time zone, replayed boolean)",
            ),
            (
                "dante.get_self_activity_responsibility(uuid,uuid)",
                "TABLE(subject_native_ref uuid, responsible_person_ref uuid, "
                "established_at timestamp with time zone)",
            ),
            (
                "dante.get_self_event_responsibility(uuid,uuid)",
                "TABLE(subject_native_ref uuid, responsible_person_ref uuid, "
                "established_at timestamp with time zone)",
            ),
            (
                "dante.list_self_event_expected_participation(uuid,uuid)",
                "TABLE(event_ref uuid, participant_person_ref uuid, requirement_code text, "
                "established_at timestamp with time zone)",
            ),
        ):
            function_acl = connection.execute(
                """
                SELECT pg_get_userbyid(p.proowner), p.prosecdef,
                       pg_get_function_result(p.oid),
                       has_function_privilege('dante_runtime', %s, 'EXECUTE'),
                       has_function_privilege('dante_migrator', %s, 'EXECUTE'),
                       EXISTS (
                         SELECT 1 FROM aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) AS acl
                         WHERE acl.grantee=0 AND acl.privilege_type='EXECUTE'
                       )
                  FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
                 WHERE n.nspname='dante' AND p.oid=to_regprocedure(%s)
                """,
                (signature, signature, signature),
            ).fetchone()
            assert function_acl == ("dante_owner", True, result, True, False, False)


def test_b09_b_authenticated_api_assigns_self_without_person_or_actual(
    migrated_database: Any, activity_hibp_stub_url: str
) -> None:
    alice_email = "b09b.alice@example.com"
    bob_email = "b09b.bob@example.com"
    auth_settings = _auth_settings(activity_hibp_stub_url)
    _seed_account(migrated_database, auth_settings, alice_email)
    _seed_account(migrated_database, auth_settings, bob_email)
    app = create_app(_settings(migrated_database, activity_hibp_stub_url))
    with TestClient(app, base_url=_CANONICAL_ORIGIN) as client:
        csrf = _signin(client, alice_email)
        mutating = {**_base_headers(), CSRF_HEADER_NAME: csrf}
        area = api_test_life_area(client, mutating)
        created_activity = client.post(
            "/api/v1/temporal/activities",
            json={
                "operation_id": "b09-b:api:activity",
                "title": "Prepare the quarterly review",
                "life_area_ref": area,
            },
            headers=mutating,
        )
        assert created_activity.status_code == 201
        activity_ref = created_activity.json()["activity_ref"]
        path = f"/api/v1/temporal/activities/{activity_ref}/responsibility"

        empty = client.get(path, headers=_base_headers())
        assert empty.status_code == 200
        assert empty.json()["responsible_person_ref"] is None
        assert empty.json()["responsible_is_self"] is False

        denied = client.put(
            path,
            json={"operation_id": "b09-b:api:assign", "holder": "self"},
            headers=_base_headers(),
        )
        assert denied.status_code == 403

        assigned = client.put(
            path,
            json={
                "operation_id": "b09-b:api:assign",
                "holder": "self",
                "expected_holder": None,
            },
            headers=mutating,
        )
        assert assigned.status_code == 200
        body = assigned.json()
        assert body["subject_kind"] == "activity"
        assert body["responsible_is_self"] is True
        assert body["replayed"] is False
        assert body["responsible_person_ref"] is not None

        replay = client.put(
            path,
            json={
                "operation_id": "b09-b:api:assign",
                "holder": "self",
                "expected_holder": None,
            },
            headers=mutating,
        )
        assert replay.status_code == 200
        assert replay.json()["replayed"] is True
        assert replay.json()["responsible_person_ref"] == body["responsible_person_ref"]
        assert replay.json()["established_at"] == body["established_at"]

        reused = client.put(
            path,
            json={
                "operation_id": "b09-b:api:assign",
                "holder": None,
                "expected_holder": "self",
            },
            headers=mutating,
        )
        assert reused.status_code == 409
        assert reused.json()["code"] == "temporal.responsibility.operation_id_reused"

        created_event = client.post(
            "/api/v1/temporal/events",
            json={
                "operation_id": "b09-b:api:event",
                "title": "Quarterly review",
                "life_area_ref": area,
            },
            headers=mutating,
        )
        assert created_event.status_code == 201
        event_ref = created_event.json()["event_ref"]
        participation_path = f"/api/v1/temporal/events/{event_ref}/expected-participation"
        required = client.put(
            participation_path,
            json={
                "operation_id": "b09-b:api:participation",
                "participant": "self",
                "requirement_code": "required",
                "expected_requirement_code": None,
            },
            headers=mutating,
        )
        assert required.status_code == 200
        assert required.json()["requirement_code"] == "required"
        assert required.json()["participant_is_self"] is True
        listed = client.get(participation_path, headers=_base_headers())
        assert listed.status_code == 200
        assert [row["requirement_code"] for row in listed.json()] == ["required"]

        event_responsibility = client.put(
            f"/api/v1/temporal/events/{event_ref}/responsibility",
            json={
                "operation_id": "b09-b:api:event-assign",
                "holder": "self",
                "expected_holder": None,
            },
            headers=mutating,
        )
        assert event_responsibility.status_code == 200
        assert event_responsibility.json()["responsible_is_self"] is True

    with TestClient(app, base_url=_CANONICAL_ORIGIN) as other:
        other_csrf = _signin(other, bob_email)
        other_headers = {**_base_headers(), CSRF_HEADER_NAME: other_csrf}
        foreign = other.get(
            f"/api/v1/temporal/activities/{activity_ref}/responsibility",
            headers=_base_headers(),
        )
        assert foreign.status_code == 404
        foreign_write = other.put(
            f"/api/v1/temporal/activities/{activity_ref}/responsibility",
            json={"operation_id": "b09-b:api:foreign", "holder": "self"},
            headers=other_headers,
        )
        assert foreign_write.status_code == 404

    with _admin(migrated_database) as connection:
        counts = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.actual WHERE subject_native_ref IN (%s,%s)),
              (SELECT count(*) FROM dante.session_execution_subject
                 WHERE subject_native_ref IN (%s,%s))
            """,
            (activity_ref, event_ref, activity_ref, event_ref),
        ).fetchone()
    assert counts == (0, 0)

