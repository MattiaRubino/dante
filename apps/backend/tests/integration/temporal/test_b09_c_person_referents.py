"""B09-C PostgreSQL proof for native non-Account Person referents."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.responsibility_participation import (
    ResponsibilityConflictError,
    ResponsibilityNotFoundError,
    ResponsibilityOperationReuseError,
    ResponsibilityParticipationApplication,
)
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

pytestmark = pytest.mark.postgres
pytest_plugins = ("tests.integration.temporal.test_b01_activity_core",)


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host, port=database.cluster.port,
        dbname=database.name, user=database.cluster.admin_user,
        password=database.cluster.admin_password, autocommit=True,
    )


@pytest.mark.asyncio
async def test_person_catalog_creates_native_identity_without_account_and_guards_replay(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    app = ResponsibilityParticipationApplication(runtime.session_factory)
    try:
        created = await app.create_person_referent(
            self_person_ref=alice, operation_id="person:create", display_label=" Anna ",
        )
        assert created.display_label == "Anna"
        assert created.revision == 1
        assert not created.replayed
        assert (await app.create_person_referent(
            self_person_ref=alice, operation_id="person:create", display_label="Anna",
        )).person_ref == created.person_ref
        assert (await app.create_person_referent(
            self_person_ref=alice, operation_id="person:create", display_label="Anna",
        )).replayed
        with pytest.raises(ResponsibilityOperationReuseError):
            await app.create_person_referent(
                self_person_ref=alice, operation_id="person:create", display_label="Other",
            )

        assert [p.person_ref for p in await app.list_person_referents(
            self_person_ref=alice,
        )] == [created.person_ref]
        assert await app.list_person_referents(self_person_ref=bob) == ()

        renamed = await app.rename_person_referent(
            self_person_ref=alice, operation_id="person:rename",
            person_ref=created.person_ref, expected_revision=1,
            display_label="Anna Rossi",
        )
        assert (renamed.display_label, renamed.revision) == ("Anna Rossi", 2)
        assert (await app.rename_person_referent(
            self_person_ref=alice, operation_id="person:rename",
            person_ref=created.person_ref, expected_revision=1,
            display_label="Anna Rossi",
        )).replayed
        with pytest.raises(ResponsibilityConflictError):
            await app.rename_person_referent(
                self_person_ref=alice, operation_id="person:stale",
                person_ref=created.person_ref, expected_revision=1,
                display_label="Anna Bianchi",
            )
        with pytest.raises(ResponsibilityNotFoundError):
            await app.rename_person_referent(
                self_person_ref=bob, operation_id="person:foreign",
                person_ref=created.person_ref, expected_revision=1,
                display_label="Reveal",
            )

        with _admin(migrated_database) as connection:
            assert connection.execute(
                "SELECT owner_family FROM dante.native_address WHERE native_ref=%s",
                (created.person_ref,),
            ).fetchone() == ("person",)
            assert connection.execute(
                "SELECT count(*) FROM dante.account_application_context "
                "WHERE self_person_ref=%s", (created.person_ref,),
            ).fetchone() == (0,)
            for table in ("person_referent_catalog", "person_referent_operation"):
                assert connection.execute(
                    "SELECT has_table_privilege('dante_runtime',%s,'INSERT'), "
                    "has_table_privilege('dante_runtime',%s,'UPDATE'), "
                    "has_table_privilege('dante_runtime',%s,'DELETE')",
                    (f"dante.{table}",) * 3,
                ).fetchone() == (False, False, False)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_local_person_can_hold_responsibility_and_expected_event_participation(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    app = ResponsibilityParticipationApplication(runtime.session_factory)
    try:
        person = await app.create_person_referent(
            self_person_ref=alice, operation_id="c:person", display_label="Luca",
        )
        area = (await areas.create(
            self_person_ref=alice, operation_id="c:area", name="Lavoro",
        )).area
        activity = (await activities.create_activity(
            self_person_ref=alice, operation_id="c:activity",
            title="Prepare review", life_area_ref=area.life_area_ref,
        )).activity
        event = (await events.create_event(
            self_person_ref=alice, operation_id="c:event",
            title="Review", life_area_ref=area.life_area_ref,
        )).event

        result = await app.set_responsibility(
            self_person_ref=alice, operation_id="c:assign",
            subject_kind="activity", subject_native_ref=activity.activity_ref,
            responsible_person_ref=person.person_ref,
            expected_responsible_person_ref=None,
        )
        assert result.responsible_person_ref == person.person_ref
        expectation = await app.set_expected_participation(
            self_person_ref=alice, operation_id="c:expect", event_ref=event.event_ref,
            participant_person_ref=person.person_ref, requirement_code="required",
            expected_requirement_code=None,
        )
        assert expectation.participant_person_ref == person.person_ref
        assert expectation.requirement_code == "required"

        with pytest.raises(ResponsibilityNotFoundError):
            await app.set_expected_participation(
                self_person_ref=alice, operation_id="c:foreign-person",
                event_ref=event.event_ref, participant_person_ref=bob,
                requirement_code="optional", expected_requirement_code=None,
            )
        with pytest.raises(ResponsibilityNotFoundError):
            await app.set_responsibility(
                self_person_ref=bob, operation_id="c:foreign-subject",
                subject_kind="activity", subject_native_ref=activity.activity_ref,
                responsible_person_ref=person.person_ref,
                expected_responsible_person_ref=None,
            )

        with _admin(migrated_database) as connection:
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref IN (%s,%s)",
                (activity.activity_ref, event.event_ref),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()
