"""M1 whole scoped metadata edit: server CAS, ownership, history and future policy."""

from __future__ import annotations

import json
from datetime import datetime, time, timedelta
from types import SimpleNamespace
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from fastapi import Response
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_b02_schedule_place import _context

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication
from dante.modules.temporal.occurrence_api import (
    ScopedProfileEditCommand,
    accept_occurrence_profile_edit,
    get_occurrence_profile_edit_state,
)
from dante.modules.temporal.recurrence import CalendarRecurrence, RecurrenceApplication
from dante.modules.temporal.routine import RoutineApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres
ZONE = "Europe/Rome"


def _daily(start: Any) -> CalendarRecurrence:
    return CalendarRecurrence(
        family_code="calendar_wall_clock",
        range_kind="open",
        expected_occurrence_count=None,
        effective_from=start,
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


async def _edit(runtime: Any, actor: UUID, selected: UUID, state: UUID | None,
                scope: str, patch: dict[str, object], operation: str,
                expected: int = 0) -> Any:
    async with runtime.session_factory() as session, session.begin():
        return (await session.execute(
            text(
                "SELECT * FROM dante.accept_self_occurrence_profile_edit("
                ":actor,:selected,:operation,:expected,:state,:scope,:zone,"
                "CAST(:patch AS jsonb))"
            ),
            {
                "actor": actor, "selected": selected, "operation": operation,
                "expected": expected, "state": state, "scope": scope,
                "zone": ZONE, "patch": json.dumps(patch),
            },
        )).mappings().one()


async def _patch(runtime: Any, actor: UUID, selected: UUID) -> dict[str, object]:
    async with runtime.session_factory() as session, session.begin():
        result = await session.scalar(
            text("SELECT dante.get_self_occurrence_profile_patch(:actor,:selected)"),
            {"actor": actor, "selected": selected},
        )
        return dict(result)


@pytest.mark.asyncio
async def test_selected_past_and_only_later_future_become_effective(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    today = datetime.now(ZoneInfo(ZONE)).date()
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    try:
        area = (await areas.create(
            self_person_ref=alice, operation_id="m1c:area", name="Sport"
        )).area
        source = await routines.create(
            self_person_ref=alice, operation_id="m1c:routine",
            title="Corsa", life_area_ref=area.life_area_ref,
            starts_on=today - timedelta(days=3), wall_time=time(9),
        )
        state = await recurrences.get(
            owner="routine", self_person_ref=alice, owner_ref=source.routine_ref
        )
        assert state is not None
        previous = await occurrences.checkpoint(
            owner="routine", self_person_ref=alice,
            source_ref=source.routine_ref, operation_id="m1c:past",
            start_date=today - timedelta(days=3),
            end_date_exclusive=today,
            effective_zone_id=ZONE,
        )
        following = await occurrences.checkpoint(
            owner="routine", self_person_ref=alice,
            source_ref=source.routine_ref, operation_id="m1c:future",
            start_date=today + timedelta(days=2),
            end_date_exclusive=today + timedelta(days=5),
            effective_zone_id=ZONE,
        )
        assert len(previous.occurrences) == len(following.occurrences) == 3
        selected = previous.occurrences[0].occurrence_ref
        result = await _edit(
            runtime, alice, selected, state.material_state_ref,
            "this_and_following", {"title": "Corsa 15 km"},
            "m1c:past-following",
        )
        expected = {selected, *(o.occurrence_ref for o in following.occurrences)}
        assert set(result["target_occurrence_refs"]) == expected
        assert result["revision"] == 1
        assert result["replayed"] is False
        assert await _patch(runtime, alice, selected) == {"title": "Corsa 15 km"}
        for item in previous.occurrences[1:]:
            assert await _patch(runtime, alice, item.occurrence_ref) == {}
        for item in following.occurrences:
            assert await _patch(runtime, alice, item.occurrence_ref) == {
                "title": "Corsa 15 km",
            }

        later = await occurrences.checkpoint(
            owner="routine", self_person_ref=alice,
            source_ref=source.routine_ref, operation_id="m1c:later",
            start_date=today + timedelta(days=5),
            end_date_exclusive=today + timedelta(days=6),
            effective_zone_id=ZONE,
        )
        assert len(later.occurrences) == 1
        assert await _patch(runtime, alice, later.occurrences[0].occurrence_ref) == {
            "title": "Corsa 15 km",
        }
        replay = await _edit(
            runtime, alice, selected, state.material_state_ref,
            "this_and_following", {"title": "Corsa 15 km"},
            "m1c:past-following",
        )
        assert replay["replayed"] is True
        assert set(replay["target_occurrence_refs"]) == expected
        with pytest.raises(DBAPIError):
            await _edit(
                runtime, alice, selected, state.material_state_ref,
                "only_this", {"title": "Corsa 15 km"},
                "m1c:past-following",
            )
        with pytest.raises(DBAPIError):
            await _edit(
                runtime, alice, selected, state.material_state_ref,
                "only_this", {"description": "Nuova descrizione"},
                "m1c:stale", expected=0,
            )
        with pytest.raises(DBAPIError):
            await _edit(
                runtime, bob, selected, state.material_state_ref,
                "only_this", {"title": "Invasione"},
                "m1c:owner",
            )
        with pytest.raises(DBAPIError):
            await _patch(runtime, bob, selected)
        async with runtime.session_factory() as session, session.begin():
            privileges = (await session.execute(text(
                "SELECT has_function_privilege('dante_runtime',"
                "'dante.accept_self_occurrence_profile_edit("
                "uuid,uuid,text,bigint,uuid,text,text,jsonb)','EXECUTE') AS call_allowed,"
                "has_table_privilege('dante_runtime','dante.occurrence_profile_edit',"
                "'INSERT') AS direct_insert"
            ))).one()
            assert privileges.call_allowed is True
            assert privileges.direct_insert is False
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_event_parity_and_protected_future_override(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    today = datetime.now(ZoneInfo(ZONE)).date()
    areas = LifeAreaApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    try:
        area = (await areas.create(
            self_person_ref=alice, operation_id="m1c:event-area", name="Lavoro"
        )).area
        event = (await events.create_event(
            self_person_ref=alice, operation_id="m1c:event",
            title="Allineamento", life_area_ref=area.life_area_ref,
        )).event
        state = await recurrences.replace(
            owner="event", self_person_ref=alice, owner_ref=event.event_ref,
            operation_id="m1c:event-recurrence",
            expected_material_state_ref=None,
            recurrence=_daily(today - timedelta(days=2)),
        )
        rows = await occurrences.checkpoint(
            owner="event", self_person_ref=alice, source_ref=event.event_ref,
            operation_id="m1c:event-window",
            start_date=today - timedelta(days=2),
            end_date_exclusive=today + timedelta(days=4),
            effective_zone_id=ZONE,
        )
        selected = rows.occurrences[0].occurrence_ref
        future = rows.occurrences[-1].occurrence_ref
        req = SimpleNamespace(
            app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))
        )
        ctx = _context(alice)
        initial = await get_occurrence_profile_edit_state(
            future, ctx, req, Response()
        )
        assert initial.edit_revision == 0
        assert initial.source_native_ref == event.event_ref
        assert initial.recurrence_state_ref == state.recurrence.material_state_ref
        one = await accept_occurrence_profile_edit(
            future,
            ScopedProfileEditCommand(
                operation_id="m1c:event-one",
                expected_revision=initial.edit_revision,
                expected_recurrence_state_ref=initial.recurrence_state_ref,
                scope_code="only_this",
                profile_patch={"title": "Evento personale"},
            ),
            ctx, req, Response(),
        )
        assert list(one.target_occurrence_refs) == [future]
        assert await _patch(runtime, alice, future) == {"title": "Evento personale"}
        assert await _patch(runtime, alice, selected) == {}
        with pytest.raises(DBAPIError):
            await _edit(
                runtime, alice, selected, state.recurrence.material_state_ref,
                "this_and_following", {"title": "Serie nuova"},
                "m1c:event-blocked", expected=1,
            )
        assert await _patch(runtime, alice, selected) == {}
        assert await _patch(runtime, alice, future) == {"title": "Evento personale"}
        two = await _edit(
            runtime, alice, selected, state.recurrence.material_state_ref,
            "only_this", {"title": "Evento storico corretto"},
            "m1c:event-correction", expected=1,
        )
        assert two["revision"] == 2
        assert list(two["target_occurrence_refs"]) == [selected]
        assert await _patch(runtime, alice, selected) == {
            "title": "Evento storico corretto",
        }
    finally:
        await runtime.dispose()
