"""B06-B PostgreSQL proof for immutable Routine/Event Recurrence authoring."""

from __future__ import annotations

from datetime import date, datetime, time, timezone
from decimal import Decimal
from typing import Any

import psycopg
import pytest

from dante.modules.temporal.event import TemporalEventApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.recurrence import (
    CalendarRecurrence, CyclicRecurrence, ElapsedRecurrence, QuotaRecurrence,
    RecurrenceApplication, RecurrenceNotFoundError, RecurrenceOperationReuseError,
    RecurrenceStateConflictError,
)
from dante.modules.temporal.routine import RoutineApplication
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_recurrence_authoring_preserves_four_families_history_dst_and_source_boundary(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    events = TemporalEventApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    try:
        area = (await areas.create(self_person_ref=alice, operation_id="area", name="Casa")).area
        routine = await routines.create(
            self_person_ref=alice, operation_id="routine", title="Allenamento", life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1), wall_time=time(7, 30),
        )
        event = (await events.create_event(self_person_ref=alice, operation_id="event", title="Standup", life_area_ref=area.life_area_ref)).event
        initial = await recurrences.get(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref)
        assert initial is not None and isinstance(initial.recurrence, CalendarRecurrence)
        assert await recurrences.get(owner="event", self_person_ref=alice, owner_ref=event.event_ref) is None

        named_calendar = CalendarRecurrence(
            family_code="calendar_wall_clock", range_kind="until_boundary", expected_occurrence_count=None,
            effective_from=date(2026, 10, 5), effective_until=date(2026, 11, 5),
            pattern_code="weekly_weekdays", interval_count=1, clock_basis_code="named_zone", zone_id="Europe/Rome",
            pattern_anchor_date=None, wall_times=(time(2, 30),), weekdays=(1, 3, 5), month_days=(), ordinal_weekdays=(), year_month_days=(),
            nonexistent_local_time_policy="skip_civil_candidate", ambiguous_local_time_policy="later",
        )
        accepted = await recurrences.replace(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref,
            operation_id="routine:calendar", expected_material_state_ref=initial.material_state_ref, recurrence=named_calendar)
        assert isinstance(accepted.recurrence.recurrence, CalendarRecurrence)
        assert accepted.recurrence.recurrence.ambiguous_local_time_policy == "later"
        assert (await recurrences.replace(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref,
            operation_id="routine:calendar", expected_material_state_ref=initial.material_state_ref, recurrence=named_calendar)).replayed
        with pytest.raises(RecurrenceOperationReuseError):
            await recurrences.replace(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref,
                operation_id="routine:calendar", expected_material_state_ref=accepted.recurrence.material_state_ref,
                recurrence=named_calendar)
        with pytest.raises(RecurrenceStateConflictError):
            await recurrences.replace(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref,
                operation_id="routine:stale", expected_material_state_ref=initial.material_state_ref, recurrence=named_calendar)

        elapsed = ElapsedRecurrence(
            family_code="elapsed_interval", range_kind="expected_count", expected_occurrence_count=4,
            effective_from=datetime(2026, 11, 5, 10, tzinfo=timezone.utc), effective_until=None,
            elapsed_seconds=Decimal("900.000000"), anchor_mode_code="fixed_anchor", anchor_at=datetime(2026, 11, 5, 10, tzinfo=timezone.utc),
        )
        elapsed_result = await recurrences.replace(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref,
            operation_id="routine:elapsed", expected_material_state_ref=accepted.recurrence.material_state_ref, recurrence=elapsed)
        assert isinstance(elapsed_result.recurrence.recurrence, ElapsedRecurrence)

        quota = QuotaRecurrence(
            family_code="quota_per_period", range_kind="open", expected_occurrence_count=None,
            effective_from=date(2026, 12, 7), effective_until=None, quota_count=3, period_unit_code="week", period_span=1,
            frame_code="floating_local", zone_id=None, week_start=1, pattern_anchor_date=None,
        )
        quota_result = await recurrences.replace(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref,
            operation_id="routine:quota", expected_material_state_ref=elapsed_result.recurrence.material_state_ref, recurrence=quota)
        assert isinstance(quota_result.recurrence.recurrence, QuotaRecurrence)

        cyclic = CyclicRecurrence(
            family_code="cyclic_positional", range_kind="expected_count", expected_occurrence_count=6,
            effective_from=date(2027, 1, 1), effective_until=None, cycle_length=4, position_unit_code="day",
            pattern_anchor_date=date(2027, 1, 1), generates_expected=(True, False, True, True),
        )
        cyclic_result = await recurrences.replace(owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref,
            operation_id="routine:cyclic", expected_material_state_ref=quota_result.recurrence.material_state_ref, recurrence=cyclic)
        assert isinstance(cyclic_result.recurrence.recurrence, CyclicRecurrence)

        event_calendar = await recurrences.replace(owner="event", self_person_ref=alice, owner_ref=event.event_ref,
            operation_id="event:calendar", expected_material_state_ref=None, recurrence=named_calendar)
        assert not event_calendar.replayed and isinstance(event_calendar.recurrence.recurrence, CalendarRecurrence)
        with pytest.raises(RecurrenceStateConflictError):
            await recurrences.replace(owner="event", self_person_ref=alice, owner_ref=event.event_ref,
                operation_id="event:missing-cas", expected_material_state_ref=None, recurrence=elapsed)
        with pytest.raises(RecurrenceNotFoundError):
            await recurrences.get(owner="routine", self_person_ref=bob, owner_ref=routine.routine_ref)

        with psycopg.connect(**migrated_database.connection_kwargs("dante_migrator", migrated_database.cluster.migrator_password)) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute("SELECT count(*) FROM dante.routine_recurrence_current_history WHERE routine_ref=%s", (routine.routine_ref,)).fetchone() == (5,)
            assert connection.execute("SELECT count(*) FROM dante.routine_recurrence_current_history WHERE routine_ref=%s AND current_until_at IS NULL", (routine.routine_ref,)).fetchone() == (1,)
            assert connection.execute("SELECT nonexistent_local_time_policy,ambiguous_local_time_policy FROM dante.routine_recurrence_calendar_dst_policy").fetchone() == ("skip_civil_candidate", "later")
            assert connection.execute("SELECT count(*) FROM dante.occurrence").fetchone() == (0,)
            assert connection.execute("SELECT count(*) FROM dante.schedule").fetchone() == (0,)
            assert connection.execute("SELECT count(*) FROM dante.activity").fetchone() == (0,)
    finally:
        await runtime.dispose()


def test_recurrence_runtime_retains_execute_only_surface(migrated_database: Any) -> None:
    with psycopg.connect(host=migrated_database.cluster.host, port=migrated_database.cluster.port, dbname=migrated_database.name, user=migrated_database.cluster.admin_user, password=migrated_database.cluster.admin_password) as connection:
        assert connection.execute(
            "SELECT has_table_privilege('dante_runtime','dante.routine_recurrence_operation','INSERT'),"
            "has_table_privilege('dante_runtime','dante.event_recurrence_calendar_dst_policy','SELECT'),"
            "has_function_privilege('dante_runtime','dante.replace_self_routine_recurrence(uuid,text,text,uuid,uuid,text,text,integer,date,date,timestamptz,timestamptz,text,integer,text,text,text,date,time[],smallint[],smallint[],smallint[],smallint[],smallint[],smallint[],text,text,numeric,text,timestamptz,integer,text,integer,text,text,smallint,integer,text,date,boolean[])','EXECUTE'),"
            "has_function_privilege('dante_runtime','dante.get_self_event_recurrence(uuid,uuid)','EXECUTE')"
        ).fetchone() == (False, False, True, True)
