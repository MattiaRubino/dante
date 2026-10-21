"""M3-B negative proof: per-instance edits must never masquerade as series edits."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, time, timedelta
from typing import Any
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text
from tests.integration.temporal.test_objective_recurring_instance_scope import _read_checkpoint_refs
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_profile_scoped_edit import _daily

from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.life_area_assignment import LifeAreaAssignmentApplication
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.modules.temporal.schedule import (
    NamedZoneLocalIntervalPlacement,
    TemporalScheduleApplication,
)
from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
)
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
        return UUID(str(result.scalar_one()))


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


async def _envelope(runtime: Any, actor: UUID, activity: UUID) -> Any:
    async with runtime.session_factory() as session, session.begin():
        result = await session.execute(
            text(
                "SELECT role.schedule_ref, current.material_state_ref "
                "AS placement_material_state_ref "
                "FROM dante.get_self_activity_schedule_roles("
                ":actor,CAST(ARRAY[:activity] AS uuid[])) AS role "
                "JOIN dante.schedule_current_placement AS current "
                "ON current.scoped_owner_ref=role.schedule_ref "
                "WHERE role.role_code='envelope'"
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
            self_person_ref=actor,
            operation_id="m3b:source",
            title="Allenamento ricorrente",
            life_area_intent=None,
            recurrence=replace(
                _daily(tomorrow),
                clock_basis_code="named_zone",
                zone_id=ZONE,
                nonexistent_local_time_policy="skip_civil_candidate",
                ambiguous_local_time_policy="earlier",
            ),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=60,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "planned_slices": [
                    {
                        "start_offset_minutes": 0,
                        "duration_minutes": 30,
                        "name": "Preparazione",
                    }
                ],
            },
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="m3b:early",
            start_date=tomorrow,
            end_date_exclusive=tomorrow + timedelta(days=2),
            effective_zone_id=ZONE,
        )
        early = await _read_checkpoint_refs(
            runtime,
            actor,
            routine.source_ref,
            owner="routine",
            operation="m3b:early",
            start=tomorrow,
            end=tomorrow + timedelta(days=2),
        )
        assert len(early) == 2
        selected = await _activity(runtime, actor, early[0])
        untouched = await _activity(runtime, actor, early[1])
        area = (
            await LifeAreaApplication(runtime.session_factory).create(
                self_person_ref=actor,
                operation_id="m3b:area",
                name="Sport",
            )
        ).area
        assigned = await assignments.assign(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=NativeRef(selected),
            life_area_ref=area.life_area_ref,
            expected_assignment_revision=0,
            operation_id="m3b:selected-area",
        )
        assert assigned.assignment_revision == 1
        original = await _planned(runtime, actor, selected)
        assert original["display_name"] == "Preparazione"
        async with runtime.session_factory() as session, session.begin():
            revised = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.revise_self_planned_session_name("
                            ":actor,:activity,:schedule,:before,:after)"
                        ),
                        {
                            "actor": actor,
                            "activity": selected,
                            "schedule": original["schedule_ref"],
                            "before": "Preparazione",
                            "after": "Riscaldamento",
                        },
                    )
                )
                .mappings()
                .one()
            )
            assert revised["display_name"] == "Riscaldamento"
            assert revised["schedule_ref"] == original["schedule_ref"]
        # A different already-materialized instance is never edited implicitly.
        assert (await _planned(runtime, actor, selected))["display_name"] == "Riscaldamento"
        assert (await _planned(runtime, actor, untouched))["display_name"] == "Preparazione"

        # Nor is a new future Occurrence allowed to silently inherit a
        # per-instance Life Area or planned Session name correction.
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="m3b:later",
            start_date=tomorrow + timedelta(days=2),
            end_date_exclusive=tomorrow + timedelta(days=3),
            effective_zone_id=ZONE,
        )
        future = await _read_checkpoint_refs(
            runtime,
            actor,
            routine.source_ref,
            owner="routine",
            operation="m3b:later",
            start=tomorrow + timedelta(days=2),
            end=tomorrow + timedelta(days=3),
        )
        assert len(future) == 1
        future_activity = await _activity(runtime, actor, future[0])
        assert (await _planned(runtime, actor, future_activity))["display_name"] == "Preparazione"
        area_assignments = await assignments.list_assignments(self_person_ref=actor)
        assert any(
            item.subject_kind == "activity"
            and item.subject_native_ref == selected
            and item.life_area_ref == area.life_area_ref
            for item in area_assignments
        )
        assert not any(
            item.subject_kind == "activity"
            and item.subject_native_ref
            in (
                untouched,
                future_activity,
            )
            for item in area_assignments
        )

        # Assigning an area *after* materialization is a local exception even
        # on the first assignment revision. The create-time assignment shares
        # its operation id with Activity Create and remains clean.
        await assignments.assign(
            self_person_ref=actor,
            subject_kind="activity",
            subject_native_ref=NativeRef(future_activity),
            life_area_ref=area.life_area_ref,
            expected_assignment_revision=0,
            operation_id="m3b:future-area",
        )
        async with runtime.session_factory() as session, session.begin():
            area_preview = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_occurrence_profile_edit_preview("
                            ":actor,:selected,'this_and_following',:zone)"
                        ),
                        {"actor": actor, "selected": early[0], "zone": ZONE},
                    )
                )
                .mappings()
                .one()
            )
            assert any(
                item["occurrence_ref"] == str(future[0]) and item["reason"] == "local_change"
                for item in area_preview["protected_occurrences"]
            )

        # A second instance with *only* an individual planned Session rename
        # must be protected by the authoritative following-scope preview.
        untouched_plan = await _planned(runtime, actor, untouched)
        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                text(
                    "SELECT * FROM dante.revise_self_planned_session_name("
                    ":actor,:activity,:schedule,:before,:after)"
                ),
                {
                    "actor": actor,
                    "activity": untouched,
                    "schedule": untouched_plan["schedule_ref"],
                    "before": "Preparazione",
                    "after": "Riscaldamento",
                },
            )
            first_marker = await session.scalar(
                text(
                    "SELECT name_exception_reason FROM dante.activity_schedule_role "
                    "WHERE schedule_ref=:schedule"
                ),
                {"schedule": untouched_plan["schedule_ref"]},
            )
            assert first_marker == "local_edit"
            preview = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_occurrence_profile_edit_preview("
                            ":actor,:selected,'this_and_following',:zone)"
                        ),
                        {"actor": actor, "selected": early[0], "zone": ZONE},
                    )
                )
                .mappings()
                .one()
            )
            assert any(
                item["occurrence_ref"] == str(early[1]) and item["reason"] == "local_change"
                for item in preview["protected_occurrences"]
            )
            assert early[1] not in preview["target_occurrence_refs"]

            await session.execute(
                text(
                    "SELECT * FROM dante.revise_self_planned_session_name("
                    ":actor,:activity,:schedule,:before,:after)"
                ),
                {
                    "actor": actor,
                    "activity": untouched,
                    "schedule": untouched_plan["schedule_ref"],
                    "before": "Riscaldamento",
                    "after": "Preparazione",
                },
            )
            restored_marker = await session.scalar(
                text(
                    "SELECT name_exception_reason FROM dante.activity_schedule_role "
                    "WHERE schedule_ref=:schedule"
                ),
                {"schedule": untouched_plan["schedule_ref"]},
            )
            assert restored_marker == first_marker
            assert (
                await session.scalar(
                    text("SELECT dante.get_self_occurrence_edit_protection(:actor,:occurrence)"),
                    {"actor": actor, "occurrence": early[1]},
                )
                == "local_change"
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_post_binding_planned_structure_is_preserved_as_future_exception(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    tomorrow = datetime.now(ZoneInfo(ZONE)).date() + timedelta(days=1)
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        source = await authoring.create_routine(
            self_person_ref=actor,
            operation_id="structure-exception:source",
            title="Routine con Session aggiunta dopo",
            life_area_intent=None,
            recurrence=replace(
                _daily(tomorrow),
                clock_basis_code="named_zone",
                zone_id=ZONE,
                nonexistent_local_time_policy="skip_civil_candidate",
                ambiguous_local_time_policy="earlier",
            ),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=source.source_ref,
            duration_minutes=60,
            reminder_lead_minutes=None,
            activity_template={"version": 1},
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="structure-exception:window",
            start_date=tomorrow,
            end_date_exclusive=tomorrow + timedelta(days=2),
            effective_zone_id=ZONE,
        )
        selected, later = await _read_checkpoint_refs(
            runtime,
            actor,
            source.source_ref,
            owner="routine",
            operation="structure-exception:window",
            start=tomorrow,
            end=tomorrow + timedelta(days=2),
        )
        async with runtime.session_factory() as session, session.begin():
            clean = await session.scalar(
                text("SELECT dante.get_self_occurrence_edit_protection(:actor,:occurrence)"),
                {"actor": actor, "occurrence": later},
            )
            assert clean is None

        activity = await _activity(runtime, actor, later)
        start = datetime.combine(tomorrow + timedelta(days=1), time(10, 0))
        added = await TemporalScheduleApplication(runtime.session_factory).establish_schedule(
            self_person_ref=actor,
            operation_id="structure-exception:planned",
            subject_native_ref=NativeRef(activity),
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=start,
                ends_local_at=start + timedelta(minutes=30),
                zone_id=ZONE,
                disambiguation="earlier",
            ),
        )
        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                text(
                    "SELECT * FROM dante.set_self_activity_schedule_role("
                    ":actor,:activity,:schedule,'planned',1,'Aggiunta locale')"
                ),
                {
                    "actor": actor,
                    "activity": activity,
                    "schedule": added.schedule_ref,
                },
            )
            preview = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_occurrence_profile_edit_preview("
                            ":actor,:selected,'this_and_following',:zone)"
                        ),
                        {"actor": actor, "selected": selected, "zone": ZONE},
                    )
                )
                .mappings()
                .one()
            )
            assert later not in preview["target_occurrence_refs"]
            assert any(
                item["occurrence_ref"] == str(later) and item["reason"] == "local_change"
                for item in preview["protected_occurrences"]
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_checkpoint_does_not_recreate_a_replanned_materialized_activity(
    migrated_database: Any,
) -> None:
    """Refreshing a later Timeline day preserves the local Activity replan.

    The binding marks a completed generated Activity. Replaying its original
    create operation after a user moved the local Schedule produces a different
    intent and used to escape as a 500 from the Timeline checkpoint.
    """

    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    tomorrow = datetime.now(ZoneInfo(ZONE)).date() + timedelta(days=1)
    try:
        routine = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="m3b:replan-source",
            title="Lettura ricorrente",
            life_area_intent=None,
            recurrence=replace(
                _daily(tomorrow),
                clock_basis_code="named_zone",
                zone_id=ZONE,
                nonexistent_local_time_policy="skip_civil_candidate",
                ambiguous_local_time_policy="earlier",
            ),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=60,
            reminder_lead_minutes=None,
            activity_template={"version": 1},
        )
        materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="m3b:replan-first-window",
            start_date=tomorrow,
            end_date_exclusive=tomorrow + timedelta(days=1),
            effective_zone_id=ZONE,
        )
        occurrence = (
            await _read_checkpoint_refs(
                runtime,
                actor,
                routine.source_ref,
                owner="routine",
                operation="m3b:replan-first-window",
                start=tomorrow,
                end=tomorrow + timedelta(days=1),
            )
        )[0]
        activity = await _activity(runtime, actor, occurrence)
        envelope = await _envelope(runtime, actor, activity)
        assert envelope["placement_material_state_ref"] is not None

        await TemporalScheduleApplication(runtime.session_factory).revise_schedule(
            self_person_ref=NativeRef(actor),
            operation_id="m3b:move-generated-activity",
            schedule_ref=ScopedRecordRef(envelope["schedule_ref"]),
            expected_material_state_ref=MaterialStateRef(envelope["placement_material_state_ref"]),
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=datetime.combine(tomorrow, time(11)),
                ends_local_at=datetime.combine(tomorrow, time(12)),
                zone_id=ZONE,
            ),
        )

        # Navigating back through the same range uses a new checkpoint id. It
        # must not try to recreate the already bound Activity from 10:00.
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="m3b:replan-refresh-window",
            start_date=tomorrow,
            end_date_exclusive=tomorrow + timedelta(days=1),
            effective_zone_id=ZONE,
        )
        assert (await _envelope(runtime, actor, activity))["schedule_ref"] == envelope[
            "schedule_ref"
        ]
    finally:
        await runtime.dispose()
