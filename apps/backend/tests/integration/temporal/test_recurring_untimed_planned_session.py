"""A recurring Activity keeps each named untimed planned Session unplaced."""

from __future__ import annotations

from datetime import date
from typing import Any

import pytest
from sqlalchemy import text
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_b14_m2_objective_scope import _read_checkpoint_refs
from tests.integration.temporal.test_b14_recurring_event_create import _daily_named_zone

from dante.modules.temporal.activity_edit_snapshot_api import _SNAPSHOT, ActivityEditSnapshot
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_recurring_activity_keeps_untimed_planned_session(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        routine = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="recurring:untimed:create",
            title="Raccolta",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=30,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "planned_slices": [{"name": "Cernita", "time_enabled": False}],
            },
        )
        await RoutineOccurrenceMaterializationApplication(
            runtime.session_factory
        ).checkpoint_window(
            self_person_ref=actor,
            operation_id="recurring:untimed:window",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 7),
            effective_zone_id="Europe/Rome",
        )
        occurrences = await _read_checkpoint_refs(
            runtime, actor, routine.source_ref, owner="routine",
            operation="recurring:untimed:window",
            start=date(2026, 10, 6), end=date(2026, 10, 7),
        )
        assert len(occurrences) == 1
        async with runtime.session_factory() as session, session.begin():
            activity = (await session.execute(text("""
                SELECT activity_ref FROM dante.list_self_routine_occurrence_activities(
                    :actor, CAST(ARRAY[:occurrence] AS uuid[])
                )
            """), {
                "actor": actor,
                "occurrence": occurrences[0],
            })).scalar_one()
            snapshot = ActivityEditSnapshot.model_validate(await session.scalar(
                _SNAPSHOT, {"actor": actor, "activity": activity},
            ))
        planned = [row for row in snapshot.schedules if row.role_code == "planned"]
        assert len(planned) == 1
        assert planned[0].display_name == "Cernita"
        assert planned[0].placement_material_state_ref is None
    finally:
        await runtime.dispose()
