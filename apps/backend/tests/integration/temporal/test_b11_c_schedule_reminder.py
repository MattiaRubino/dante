"""B11-C PostgreSQL proof of self Schedule Reminder and accepted-current truth."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import psycopg
import pytest

from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    FloatingLocalIntervalPlacement,
    TemporalScheduleApplication,
)
from dante.modules.temporal.schedule_reminder import (
    ScheduleReminderApplication,
    ScheduleReminderConflictError,
    ScheduleReminderNotFoundError,
)
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.b05_legacy_test_support import ensure_test_life_area
from tests.integration.temporal.test_b02_schedule_create import _seed_self_person

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b11_c_reminder_current_replay_ownership_and_schedule_revision(
    migrated_database: Any,
) -> None:
    alice = _seed_self_person(migrated_database)
    bob = _seed_self_person(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    activities = TemporalActivityApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    reminders = ScheduleReminderApplication(runtime.session_factory)
    try:
        activity = await activities.create_activity(
            self_person_ref=alice,
            life_area_ref=ensure_test_life_area(migrated_database, alice),
            operation_id="b11c:activity",
            title="Reminder source",
        )
        floating = await schedules.establish_schedule(
            self_person_ref=alice,
            operation_id="b11c:floating",
            subject_native_ref=activity.activity.activity_ref,
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=datetime(2026, 10, 10, 9),
                ends_local_at=datetime(2026, 10, 10, 10),
            ),
        )
        with pytest.raises(ScheduleReminderNotFoundError):
            await reminders.configure(
                self_person_ref=alice, schedule_ref=floating.schedule_ref,
                operation_id="b11c:reject-floating", expected_material_state_ref=None,
                enabled=True, lead_minutes=15,
            )

        starts_at = datetime.now(UTC) + timedelta(days=2)
        exact = await schedules.revise_schedule(
            self_person_ref=alice,
            operation_id="b11c:exact",
            schedule_ref=floating.schedule_ref,
            expected_material_state_ref=floating.material_state_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=starts_at, ends_at=starts_at + timedelta(hours=1),
            ),
        )
        assert await reminders.get(self_person_ref=alice, schedule_ref=exact.schedule_ref) is None
        created = await reminders.configure(
            self_person_ref=alice, schedule_ref=exact.schedule_ref,
            operation_id="b11c:configure", expected_material_state_ref=None,
            enabled=True, lead_minutes=15,
        )
        assert created.reminder_ref.version == 7
        assert created.material_state_ref.version == 7
        assert created.schedule_starts_at == starts_at
        assert created.due_at == starts_at - timedelta(minutes=15)
        assert created.disposition_code == "pending"
        assert not created.replayed
        assert await reminders.get(self_person_ref=bob, schedule_ref=exact.schedule_ref) is None

        replay = await reminders.configure(
            self_person_ref=alice, schedule_ref=exact.schedule_ref,
            operation_id="b11c:configure", expected_material_state_ref=None,
            enabled=True, lead_minutes=15,
        )
        assert replay.replayed
        assert replay.material_state_ref == created.material_state_ref
        with pytest.raises(ScheduleReminderConflictError):
            await reminders.configure(
                self_person_ref=alice, schedule_ref=exact.schedule_ref,
                operation_id="b11c:configure", expected_material_state_ref=None,
                enabled=True, lead_minutes=30,
            )
        with pytest.raises(ScheduleReminderConflictError):
            await reminders.configure(
                self_person_ref=alice, schedule_ref=exact.schedule_ref,
                operation_id="b11c:stale", expected_material_state_ref=None,
                enabled=False, lead_minutes=15,
            )

        disabled = await reminders.configure(
            self_person_ref=alice, schedule_ref=exact.schedule_ref,
            operation_id="b11c:disable", expected_material_state_ref=created.material_state_ref,
            enabled=False, lead_minutes=15,
        )
        assert disabled.reminder_ref == created.reminder_ref
        assert disabled.material_state_ref != created.material_state_ref
        assert disabled.disposition_code == "unavailable"
        revised_start = starts_at + timedelta(hours=3)
        await schedules.revise_schedule(
            self_person_ref=alice, operation_id="b11c:replan",
            schedule_ref=exact.schedule_ref,
            expected_material_state_ref=exact.material_state_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=revised_start, ends_at=revised_start + timedelta(hours=1),
            ),
        )
        latest = await reminders.get(self_person_ref=alice, schedule_ref=exact.schedule_ref)
        assert latest is not None
        assert latest.schedule_starts_at == revised_start
        assert latest.material_state_ref == disabled.material_state_ref

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password,
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            history = connection.execute(
                """SELECT material_state_ref,current_until_at IS NULL
                     FROM dante.schedule_reminder_current_history
                    WHERE reminder_ref=%s ORDER BY current_from_at""",
                (created.reminder_ref,),
            ).fetchall()
            assert history == [
                (created.material_state_ref, False),
                (disabled.material_state_ref, True),
            ]
            assert connection.execute(
                "SELECT count(*) FROM dante.actual"
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()
