"""PostgreSQL Event/Occurrence Schedule unplace and monotonic Undo parity."""

from __future__ import annotations

from datetime import date, datetime
from types import SimpleNamespace
from typing import Any, cast

import pytest
from fastapi import Request, Response
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_event_create import _daily_named_zone

from dante.context.contracts import DanteContext
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.reality_objective_api import (
    list_event_timeline_schedules,
    list_event_timeline_undo,
)
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.schedule import FloatingLocalIntervalPlacement, TemporalScheduleApplication
from dante.platform.database.references import ScopedRecordRef, MaterialStateRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _request(runtime: Any) -> Request:
    return cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
    )


def _context(actor: Any) -> DanteContext:
    return cast(DanteContext, SimpleNamespace(self_person_ref=actor))


@pytest.mark.asyncio
async def test_event_timeline_unplace_and_undo_never_delete_event(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        authoring = TemporalAuthoringApplication(runtime.session_factory)
        event = await authoring.create_event(
            self_person_ref=actor,
            operation_id="event-timeline:oneoff",
            title="Evento ancora esistente",
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=datetime(2026, 10, 18, 9, 0),
                ends_local_at=datetime(2026, 10, 18, 10, 0),
            ),
        )
        ref = event.item.subject_native_ref
        assert event.schedule is not None
        assert await list_event_timeline_schedules(
            ref, _context(stranger), _request(runtime), Response()
        ) == []
        available = await list_event_timeline_schedules(
            ref, _context(actor), _request(runtime), Response()
        )
        assert len(available) == 1
        selected = available[0]
        assert selected.schedule_ref == event.schedule.schedule_ref
        assert selected.material_state_ref == event.schedule.material_state_ref

        schedules = TemporalScheduleApplication(runtime.session_factory)
        removed = await schedules.unschedule(
            self_person_ref=actor,
            operation_id="event-timeline:unplace",
            schedule_ref=ScopedRecordRef(selected.schedule_ref),
            expected_material_state_ref=MaterialStateRef(selected.material_state_ref),
        )
        receipts = await list_event_timeline_undo(
            ref, _context(actor), _request(runtime), Response()
        )
        assert any(
            item.schedule_ref == selected.schedule_ref
            and item.unschedule_operation_id == removed.unschedule_operation_id
            for item in receipts
        )
        restored = await schedules.undo_unschedule(
            self_person_ref=actor,
            operation_id="event-timeline:undo",
            schedule_ref=ScopedRecordRef(selected.schedule_ref),
            unschedule_operation_id=removed.unschedule_operation_id,
        )
        assert restored.material_state_ref != event.schedule.material_state_ref
        after = await list_event_timeline_schedules(
            ref, _context(actor), _request(runtime), Response()
        )
        assert len(after) == 1
        assert after[0].material_state_ref == restored.material_state_ref
        assert await list_event_timeline_undo(
            ref, _context(actor), _request(runtime), Response()
        ) == []
        assert (
            await authoring.create_event(
                self_person_ref=actor,
                operation_id="event-timeline:oneoff",
                title="Evento ancora esistente",
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=datetime(2026, 10, 18, 9, 0),
                    ends_local_at=datetime(2026, 10, 18, 10, 0),
                ),
            )
        ).replayed
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_event_timeline_lists_occurrence_schedule_not_source(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        source = await RecurringAuthoringApplication(runtime.session_factory).create_event(
            self_person_ref=actor,
            operation_id="event-timeline:recurring",
            title="Evento ricorrente",
            life_area_intent=None,
            agenda_parts=("Agenda",),
            recurrence=_daily_named_zone(),
        )
        await EventOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            event_ref=source.source_ref,
            placement_kind="timed",
            duration_minutes=30,
            duration_days=None,
            reminder_lead_minutes=None,
        )
        await RoutineOccurrenceMaterializationApplication(runtime.session_factory).checkpoint_window(
            self_person_ref=actor,
            operation_id="event-timeline:checkpoint",
            start_date=date(2026, 10, 18),
            end_date_exclusive=date(2026, 10, 19),
            effective_zone_id="Europe/Rome",
        )
        rows = await list_event_timeline_schedules(
            source.source_ref, _context(actor), _request(runtime), Response()
        )
        assert len(rows) == 1
        assert rows[0].subject_native_ref != source.source_ref
        assert rows[0].material_state_ref is not None
    finally:
        await runtime.dispose()
