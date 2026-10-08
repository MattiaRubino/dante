"""M3-B negative proof: per-instance edits must never masquerade as series edits."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_b14_m1_scoped_profile_edit import _daily
from tests.integration.temporal.test_b14_m2_objective_scope import _read_checkpoint_refs

from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.life_area_assignment import LifeAreaAssignmentApplication
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres
ZONE = "Europe/Rome"


async def _activity(runtime: Any, actor: UUID, occurrence: UUID) -> UUID:
    async with runtime.session_factory() as session, session.begin():
        result = await session.execute(
            text(
                "SELECT activity_ref "
                "FROM dante.list_self_routine_occurrence_activities("
                ":actor,:occurrences) WHERE occurrence_ref=:occurrence"
            ),
            {"actor": actor, "occurrences": [occurrence], "occurrence": occurrence},
        )
        return result.scalar_one()


async def _planned(runtime: Any, actor: UUID, activity: UUID) -> Any:
    async with runtime.session_factory() as session, session.begin():
        result = await session.execute(
            text(
                "SELECT * FROM dante.get_self_activity_schedule_roles("
                ":actor,CAST(ARRAY[:activity] AS uuid[])) WHERE role_code='planned'"
            ),
            {"actor": actor, "activity": activity},
        )
        return result.mappings().one()


@pytest.mark.asyncio
async def test_selected_activity_life_area_and_planned_name_do_not_propagate(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    tomorrow = datetime.now(ZoneInfo(ZONE)).date() + timedelta(days=1)
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    assignments = LifeAreaAssignmentApplication(runtime.session_factory)
    try:
        routine = await authoring.create_routine(
            self_person_ref=actor, operation_id="m3b:source",
            title="Allenamento ricorrente", life_area_intent=None,
            recurrence=replace(
                _daily(tomorrow),
                clock_basis_code="named_zone",
                zone_id=ZONE,
                nonexistent_local_time_policy="skip_civil_candidate",
                ambiguous_local_time_policy="earlier",
            ),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor, routine_ref=routine.source_ref,
            duration_minutes=60, reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "planned_slices": [{
                    "start_offset_minutes": 0,
                    "duration_minutes": 30,
                    "name": "Preparazione",
                }],
            },
        )
        await materializer.checkpoint_window(
            self_person_ref=actor, operation_id="m3b:early",
            start_date=tomorrow,
            end_date_exclusive=tomorrow + timedelta(days=2),
            effective_zone_id=ZONE,
        )
        early = await _read_checkpoint_refs(
            runtime, actor, routine.source_ref, owner="routine",
            operation="m3b:early", start=tomorrow,
            end=tomorrow + timedelta(days=2),
        )
        assert len(early) == 2
        selected, untouched = (
            await _activity(runtime, actor, occurrence) for occurrence in early
        )
        area = (await LifeAreaApplication(runtime.session_factory).create(
            self_person_ref=actor, operation_id="m3b:area", name="Sport",
        )).area
        assigned = await assignments.assign(
            self_person_ref=actor, subject_kind="activity",
            subject_native_ref=selected, life_area_ref=area.life_area_ref,
            expected_assignment_revision=0, operation_id="m3b:selected-area",
        )
        assert assigned.assignment_revision == 1
        original = await _planned(runtime, actor, selected)
        assert original["display_name"] == "Preparazione"
        async with runtime.session_factory() as session, session.begin():
            revised = (await session.execute(
                text(
                    "SELECT * FROM dante.revise_self_planned_session_name("
                    ":actor,:activity,:schedule,:before,:after)"
                ),
                {"actor": actor, "activity": selected,
                 "schedule": original["schedule_ref"],
                 "before": "Preparazione", "after": "Riscaldamento"},
            )).mappings().one()
            assert revised["display_name"] == "Riscaldamento"
            assert revised["schedule_ref"] == original["schedule_ref"]
        # A different already-materialized instance is never edited implicitly.
        assert (await _planned(runtime, actor, selected))["display_name"] == "Riscaldamento"
        assert (await _planned(runtime, actor, untouched))["display_name"] == "Preparazione"

        # Nor is a new future Occurrence allowed to silently inherit a
        # per-instance Life Area or planned Session name correction.
        await materializer.checkpoint_window(
            self_person_ref=actor, operation_id="m3b:later",
            start_date=tomorrow + timedelta(days=2),
            end_date_exclusive=tomorrow + timedelta(days=3),
            effective_zone_id=ZONE,
        )
        future = await _read_checkpoint_refs(
            runtime, actor, routine.source_ref, owner="routine",
            operation="m3b:later", start=tomorrow + timedelta(days=2),
            end=tomorrow + timedelta(days=3),
        )
        assert len(future) == 1
        future_activity = await _activity(runtime, actor, future[0])
        assert (await _planned(runtime, actor, future_activity))["display_name"] == "Preparazione"
        area_assignments = await assignments.list_assignments(self_person_ref=actor)
        assert any(
            item.subject_kind == "activity" and item.subject_native_ref == selected
            and item.life_area_ref == area.life_area_ref
            for item in area_assignments
        )
        assert not any(
            item.subject_kind == "activity" and item.subject_native_ref in (
                untouched, future_activity,
            ) for item in area_assignments
        )
    finally:
        await runtime.dispose()
