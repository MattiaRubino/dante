"""M1-B guarded full materialized recurrence inventory — Routine/Event parity."""

from __future__ import annotations

from datetime import date, time
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
from fastapi import Response
from sqlalchemy import text
from tests.integration.temporal.test_b02_schedule_place import _context
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication, OccurrenceSourceNotFoundError
from dante.modules.temporal.occurrence_api import get_occurrence_edit_inventory
from dante.modules.temporal.occurrence_edit_inventory import OccurrenceEditInventoryApplication
from dante.modules.temporal.recurrence import (
    CalendarRecurrence,
    RecurrenceApplication,
)
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.schedule import DateSpanPlacement, TemporalScheduleApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _daily() -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=date(2026, 10, 5),
        effective_until=None,
        pattern_code="daily",
        interval_count=1,
        clock_basis_code="floating_local",
        zone_id=None,
        pattern_anchor_date=None,
        wall_times=(time(9),),
        weekdays=(),
        month_days=(),
        ordinal_weekdays=(),
        year_month_days=(),
        nonexistent_local_time_policy=None,
        ambiguous_local_time_policy=None,
    )


@pytest.mark.asyncio
async def test_inventory_reuses_self_scope_and_returns_skipped_and_extra_occurrences(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    inventory = OccurrenceEditInventoryApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    try:
        area = (await areas.create(
            self_person_ref=alice,
            operation_id="m1:area",
            name="Personale",
        )).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="m1:routine",
            title="Routine inventario",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 5),
            wall_time=time(9),
        )
        routine_checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="m1:routine:checkpoint",
            start_date=date(2026, 10, 5),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        assert len(routine_checkpoint.occurrences) == 3
        skipped = routine_checkpoint.occurrences[1]
        await occurrences.skip(
            self_person_ref=alice,
            occurrence_ref=skipped.occurrence_ref,
            operation_id="m1:routine:skip",
            reason="Correzione singola",
        )
        extra = await occurrences.create_extra(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="m1:routine:extra",
        )
        selected_ref = routine_checkpoint.occurrences[0].occurrence_ref
        # A current Schedule must not hide the selected Occurrence from
        # the materialized source inventory (unlike the Timeline pending list).
        await schedules.establish_schedule(
            self_person_ref=alice,
            operation_id="m1:routine:schedule",
            subject_native_ref=NativeRef(selected_ref),
            placement=DateSpanPlacement(
                start_date=date(2026, 10, 5),
                end_date_exclusive=date(2026, 10, 6),
            ),
        )
        snapshot = await inventory.read(
            self_person_ref=alice,
            selected_occurrence_ref=selected_ref,
        )
        assert snapshot.source_native_ref == routine.routine_ref
        assert snapshot.selected_occurrence_ref == selected_ref
        assert snapshot.captured_at.tzinfo is not None
        assert snapshot.materialized_only is True
        assert snapshot.apply_authorized is False
        assert {row.occurrence_ref for row in snapshot.occurrences} == (
            {row.occurrence_ref for row in routine_checkpoint.occurrences}
            | {extra.occurrence.occurrence_ref}
        )
        assert next(
            row for row in snapshot.occurrences if row.occurrence_ref == skipped.occurrence_ref
        ).skipped
        assert next(
            row for row in snapshot.occurrences if row.occurrence_ref == extra.occurrence.occurrence_ref
        ).origin_code == "explicit_extra"

        with pytest.raises(OccurrenceSourceNotFoundError):
            await inventory.read(self_person_ref=bob, selected_occurrence_ref=selected_ref)
        with pytest.raises(OccurrenceSourceNotFoundError):
            await inventory.read(self_person_ref=alice, selected_occurrence_ref=uuid4())

        event = (await events.create_event(
            self_person_ref=alice,
            operation_id="m1:event",
            title="Evento ricorrente",
            life_area_ref=area.life_area_ref,
        )).event
        await recurrences.replace(
            owner="event",
            self_person_ref=alice,
            owner_ref=event.event_ref,
            operation_id="m1:event:recurrence",
            expected_material_state_ref=None,
            recurrence=_daily(),
        )
        event_checkpoint = await occurrences.checkpoint(
            owner="event",
            self_person_ref=alice,
            source_ref=event.event_ref,
            operation_id="m1:event:checkpoint",
            start_date=date(2026, 10, 5),
            end_date_exclusive=date(2026, 10, 7),
            effective_zone_id="Europe/Rome",
        )
        event_snapshot = await inventory.read(
            self_person_ref=alice,
            selected_occurrence_ref=event_checkpoint.occurrences[0].occurrence_ref,
        )
        assert len(event_snapshot.occurrences) == 2
        assert event_snapshot.source_native_ref == event.event_ref
        assert {row.occurrence_ref for row in event_snapshot.occurrences} == {
            row.occurrence_ref for row in event_checkpoint.occurrences
        }
        assert not {row.occurrence_ref for row in event_snapshot.occurrences}.intersection({
            row.occurrence_ref for row in snapshot.occurrences
        })
        with pytest.raises(OccurrenceSourceNotFoundError):
            await inventory.read(
                self_person_ref=bob,
                selected_occurrence_ref=event_checkpoint.occurrences[0].occurrence_ref,
            )

        # The exposed HTTP model truthfully refuses to authorize any apply.
        api_response = Response()
        result = await get_occurrence_edit_inventory(
            selected_ref,
            _context(alice),
            SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
            api_response,
        )
        assert result.selected_occurrence_ref == selected_ref
        assert result.materialized_only
        assert not result.apply_authorized
        assert len(result.occurrences) == 4
        assert api_response.headers["cache-control"] == "no-store"
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_inventory_uses_guarded_function_without_runtime_table_grants(
    migrated_database: Any,
) -> None:
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        async with runtime.session_factory() as session, session.begin():
            row = (await session.execute(text("""
                SELECT
                  has_function_privilege(
                    'dante_runtime',
                    'dante.list_self_recurrence_edit_occurrences(uuid,uuid)',
                    'EXECUTE'
                  ) AS can_read,
                  has_table_privilege(
                    'dante_runtime','dante.occurrence_generation','SELECT'
                  ) AS can_scan_table
            """))).one()
            assert row.can_read is True
            assert row.can_scan_table is False
    finally:
        await runtime.dispose()
