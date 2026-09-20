"""Real PostgreSQL proof for B02-B existing Activity → accepted Schedule."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any, cast
from uuid import uuid7

import psycopg
import pytest
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.activity import (
    ActivityNotFoundError,
    ActivityOperationIdReuseError,
    TemporalActivityApplication,
)
from dante.modules.temporal.application import TemporalTimelineApplication
from dante.modules.temporal.contracts import TimelineWindowQuery
from dante.modules.temporal.schedule import FloatingLocalIntervalPlacement
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.time import TimeZoneMode, TimeZonePolicy


def _floating_local(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    return datetime(year, month, day, hour, minute)  # noqa: DTZ001


def _seed_self_person(database: Any) -> NativeRef:
    person_ref = uuid7()
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        connection.execute(
            "INSERT INTO dante.person(person_ref) VALUES (%s)",
            (person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (person_ref,),
        )
        connection.commit()
    return NativeRef(person_ref)


def _context(self_person_ref: NativeRef) -> DanteContext:
    now = datetime.now(UTC)
    return DanteContext(
        principal=Principal(
            account_ref=uuid7(),
            auth_session_ref=uuid7(),
            authenticated_at=now,
            recent_auth_at=now,
        ),
        self_person_ref=self_person_ref,
        timezone_policy=TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE),
        effective_zone_id="Europe/Rome",
    )


def _counts(database: Any, activity_ref: NativeRef) -> tuple[int, int, int, int]:
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        row = connection.execute(
            """
            SELECT
              (SELECT count(*) FROM dante.activity_intention
                WHERE activity_ref=%s),
              (SELECT count(*) FROM dante.schedule
                WHERE subject_native_ref=%s),
              (SELECT count(*)
                 FROM dante.schedule AS schedule
                 JOIN dante.schedule_current_placement AS current
                   ON current.scoped_owner_ref=schedule.schedule_ref
                WHERE schedule.subject_native_ref=%s),
              (SELECT count(*)
                 FROM dante.schedule_establish_operation AS receipt
                 JOIN dante.schedule AS schedule
                   ON schedule.schedule_ref=receipt.schedule_ref
                WHERE schedule.subject_native_ref=%s)
            """,
            (activity_ref, activity_ref, activity_ref, activity_ref),
        ).fetchone()
        assert row is not None
        return cast(tuple[int, int, int, int], row)


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_existing_unplaced_activity_is_scheduled_idempotently_and_visible_once(
    migrated_database: Any,
) -> None:
    self_person_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activity_application = TemporalActivityApplication(runtime.session_factory)
    timeline_application = TemporalTimelineApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 14, 15),
        ends_local_at=_floating_local(2026, 9, 9, 15, 0),
    )

    try:
        created = await activity_application.create_activity(
            self_person_ref=self_person_ref,
            life_area_ref=ensure_test_life_area(migrated_database, self_person_ref),
            operation_id="operation:b02-b:create-unplaced",
            title="Activity da collocare",
        )
        assert await activity_application.list_unplaced(
            self_person_ref=self_person_ref,
        ) == (created.activity,)

        placed = await activity_application.schedule_existing_activity(
            self_person_ref=self_person_ref,
            activity_ref=created.activity.activity_ref,
            operation_id="operation:b02-b:place",
            placement=placement,
        )
        assert placed.replayed is False
        assert placed.activity.activity_ref == created.activity.activity_ref
        assert placed.schedule.subject_native_ref == created.activity.activity_ref
        assert placed.schedule.schedule_ref.version == 7
        assert placed.schedule.material_state_ref.version == 7

        replay = await activity_application.schedule_existing_activity(
            self_person_ref=self_person_ref,
            activity_ref=created.activity.activity_ref,
            operation_id=" operation:b02-b:place ",
            placement=placement,
        )
        assert replay.replayed is True
        assert replay.activity.activity_ref == created.activity.activity_ref
        assert replay.schedule.schedule_ref == placed.schedule.schedule_ref
        assert replay.schedule.material_state_ref == placed.schedule.material_state_ref

        with pytest.raises(ActivityOperationIdReuseError):
            await activity_application.schedule_existing_activity(
                self_person_ref=self_person_ref,
                activity_ref=created.activity.activity_ref,
                operation_id="operation:b02-b:place",
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=_floating_local(2026, 9, 9, 15, 15),
                    ends_local_at=_floating_local(2026, 9, 9, 16, 0),
                ),
            )

        assert (
            await activity_application.list_unplaced(
                self_person_ref=self_person_ref,
            )
            == ()
        )

        window = await timeline_application.read_window(
            query=TimelineWindowQuery(
                start_date=date(2026, 9, 9),
                end_date_exclusive=date(2026, 9, 10),
            ),
            context=_context(self_person_ref),
        )
        assert len(window.items) == 1
        assert window.items[0].activity_ref == created.activity.activity_ref
        assert window.items[0].schedule_ref == placed.schedule.schedule_ref
        assert window.items[0].placement_material_state_ref == (placed.schedule.material_state_ref)
    finally:
        await runtime.dispose()

    assert _counts(
        migrated_database,
        created.activity.activity_ref,
    ) == (1, 1, 1, 1)


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_missing_or_cross_self_activity_cannot_be_scheduled(
    migrated_database: Any,
) -> None:
    owner_ref = _seed_self_person(migrated_database)
    other_ref = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalActivityApplication(runtime.session_factory)
    placement = FloatingLocalIntervalPlacement(
        starts_local_at=_floating_local(2026, 9, 9, 9, 0),
        ends_local_at=_floating_local(2026, 9, 9, 9, 30),
    )

    try:
        created = await application.create_activity(
            self_person_ref=owner_ref,
            life_area_ref=ensure_test_life_area(migrated_database, owner_ref),
            operation_id="operation:b02-b:private-create",
            title="Activity privata",
        )
        with pytest.raises(ActivityNotFoundError):
            await application.schedule_existing_activity(
                self_person_ref=other_ref,
                activity_ref=created.activity.activity_ref,
                operation_id="operation:b02-b:cross-self",
                placement=placement,
            )
        with pytest.raises(ActivityNotFoundError):
            await application.schedule_existing_activity(
                self_person_ref=owner_ref,
                activity_ref=NativeRef(uuid7()),
                operation_id="operation:b02-b:missing",
                placement=placement,
            )
    finally:
        await runtime.dispose()

    assert _counts(
        migrated_database,
        created.activity.activity_ref,
    ) == (1, 0, 0, 0)
