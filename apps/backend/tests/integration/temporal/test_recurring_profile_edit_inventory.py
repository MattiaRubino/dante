"""M1-B guarded full materialized recurrence inventory — Routine/Event parity."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, time
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid4

import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_schedule_place import _context

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication, OccurrenceSourceNotFoundError
from dante.modules.temporal.occurrence_api import get_occurrence_edit_inventory
from dante.modules.temporal.occurrence_edit_inventory import OccurrenceEditInventoryApplication
from dante.modules.temporal.recurrence import CalendarRecurrence, RecurrenceApplication
from dante.modules.temporal.recurring_series_reconciliation import SeriesReconciliationWindow
from dante.modules.temporal.recurring_structure_preview import (
    RecurringStructurePreviewApplication,
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
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="m1:area",
                name="Personale",
            )
        ).area
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

        # Future guarded series acceptance composes this same read under its
        # source lock; it must never open a second transaction or mint write
        # authority merely because an inventory was enumerated.
        async with runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            transaction_time = await session.scalar(text("SELECT transaction_timestamp()"))
            in_session = await inventory.read_in_session(
                session,
                self_person_ref=alice,
                selected_occurrence_ref=selected_ref,
            )
            assert in_session.captured_at == transaction_time
            assert {row.occurrence_ref: row for row in in_session.occurrences} == {
                row.occurrence_ref: row for row in snapshot.occurrences
            }
            assert in_session.source_native_ref == routine.routine_ref
            assert in_session.materialized_only is True
            assert in_session.apply_authorized is False
        assert {row.occurrence_ref for row in snapshot.occurrences} == (
            {row.occurrence_ref for row in routine_checkpoint.occurrences}
            | {extra.occurrence.occurrence_ref}
        )
        assert next(
            row for row in snapshot.occurrences if row.occurrence_ref == skipped.occurrence_ref
        ).skipped
        assert (
            next(
                row
                for row in snapshot.occurrences
                if row.occurrence_ref == extra.occurrence.occurrence_ref
            ).origin_code
            == "explicit_extra"
        )

        with pytest.raises(OccurrenceSourceNotFoundError):
            await inventory.read(self_person_ref=bob, selected_occurrence_ref=selected_ref)
        with pytest.raises(OccurrenceSourceNotFoundError):
            await inventory.read(self_person_ref=alice, selected_occurrence_ref=uuid4())

        event = (
            await events.create_event(
                self_person_ref=alice,
                operation_id="m1:event",
                title="Evento ricorrente",
                life_area_ref=area.life_area_ref,
            )
        ).event
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
        assert not {row.occurrence_ref for row in event_snapshot.occurrences}.intersection(
            {row.occurrence_ref for row in snapshot.occurrences}
        )
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
            cast(
                Request,
                SimpleNamespace(
                    app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))
                ),
            ),
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
            row = (
                await session.execute(
                    text("""
                SELECT
                  has_function_privilege(
                    'dante_runtime',
                    'dante.list_self_recurrence_edit_occurrences(uuid,uuid)',
                    'EXECUTE'
                  ) AS can_read,
                  has_table_privilege(
                    'dante_runtime','dante.occurrence_generation','SELECT'
                  ) AS can_scan_table
            """)
                )
            ).one()
            assert row.can_read is True
            assert row.can_scan_table is False
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_structural_cadence_preview_preserves_skipped_future_occurrence(
    migrated_database: Any,
) -> None:
    """A real SQL preview classifies accepted exceptions without any writes."""
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    preview = RecurringStructurePreviewApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="series:preview:area",
                name="Area di prova",
            )
        ).area
        start = date(2099, 10, 5)
        source = await routines.create(
            self_person_ref=alice,
            operation_id="series:preview:routine",
            title="Serie di prova",
            life_area_ref=area.life_area_ref,
            starts_on=start,
            wall_time=time(9),
        )
        initial_recurrence = await recurrences.get(
            owner="routine",
            self_person_ref=alice,
            owner_ref=source.routine_ref,
        )
        assert initial_recurrence is not None
        proposed = replace(_daily(), effective_from=start)
        materialized = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=source.routine_ref,
            operation_id="series:preview:checkpoint",
            start_date=start,
            end_date_exclusive=date(2099, 10, 9),
            effective_zone_id="Europe/Rome",
        )
        assert len(materialized.occurrences) == 4
        exception = materialized.occurrences[2]
        await occurrences.skip(
            self_person_ref=alice,
            occurrence_ref=exception.occurrence_ref,
            operation_id="series:preview:skip",
            reason="Eccezione da conservare",
        )

        result = await preview.preview(
            self_person_ref=alice,
            selected_occurrence_ref=materialized.occurrences[0].occurrence_ref,
            scope_code="this_and_following",
            proposed_recurrence=proposed,
            window=SeriesReconciliationWindow(start, date(2099, 10, 9)),
            effective_zone_id="Europe/Rome",
        )
        assert not result.apply_authorized
        assert len(result.proposed_preview_fingerprint) == 64
        assert len(result.source_preview_fingerprint) == 32
        assert result.reconciliation.protected_occurrence_refs == (exception.occurrence_ref,)
        assert set(result.reconciliation.retained_occurrence_refs) == {
            row.occurrence_ref
            for row in materialized.occurrences
            if row.occurrence_ref != exception.occurrence_ref
        }
        assert result.reconciliation.superseded_occurrence_refs == ()
        assert result.reconciliation.new_coordinates == ()

        # The future acceptor must compute this SAME snapshot in its own
        # SERIALIZABLE transaction rather than making a second read request.
        async with runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            transaction_time = await session.scalar(text("SELECT transaction_timestamp()"))
            shared = await preview.preview_in_session(
                session,
                self_person_ref=alice,
                selected_occurrence_ref=materialized.occurrences[0].occurrence_ref,
                scope_code="this_and_following",
                proposed_recurrence=proposed,
                window=SeriesReconciliationWindow(start, date(2099, 10, 9)),
                effective_zone_id="Europe/Rome",
            )
            assert shared.scope_plan.captured_at == transaction_time
            assert shared == replace(
                result,
                scope_plan=replace(
                    result.scope_plan,
                    captured_at=shared.scope_plan.captured_at,
                ),
            )
            assert not shared.apply_authorized

        # Neither a preview nor its fingerprint may change the canonical source.
        current = await recurrences.get(
            owner="routine",
            self_person_ref=alice,
            owner_ref=source.routine_ref,
        )
        assert current is not None
        assert current.material_state_ref == initial_recurrence.material_state_ref
        assert current.recurrence == initial_recurrence.recurrence
    finally:
        await runtime.dispose()
