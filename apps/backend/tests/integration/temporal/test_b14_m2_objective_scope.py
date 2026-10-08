"""M2 selected generated Objective + only later future, Routine/Event provenance."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from uuid import UUID, uuid7
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_b14_m1_scoped_profile_edit import _daily
from tests.integration.temporal.test_b14_recurring_event_create import _daily_named_zone

from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres
ZONE = "Europe/Rome"


async def _definition(runtime: Any, actor: UUID, objective: UUID) -> Any:
    async with runtime.session_factory() as session, session.begin():
        return (await session.execute(
            text("SELECT * FROM dante.get_self_temporal_objective_definition(:actor,:objective)"),
            {"actor": actor, "objective": objective},
        )).mappings().one()


async def _series_state(runtime: Any, actor: UUID, objective: UUID) -> Any:
    async with runtime.session_factory() as session, session.begin():
        return (await session.execute(
            text("SELECT * FROM dante.get_self_objective_series_state(:actor,:objective)"),
            {"actor": actor, "objective": objective},
        )).mappings().one_or_none()


async def _apply(
    runtime: Any, actor: UUID, objective: UUID, *,
    operation: str, expected_source: int = 0, expected_definition: int = 0,
    recurrence_state: UUID | None = None, fingerprint: str = "a" * 64,
) -> Any:
    async with runtime.session_factory() as session, session.begin():
        return (await session.execute(
            text(
                "SELECT * FROM dante.accept_self_objective_series_edit("
                ":actor,:objective,:operation,:fingerprint,:expected_definition,"
                ":expected_source,:recurrence,:zone,:label,:kind,:comparator,"
                ":target,:minimum,:maximum,:unit,:ordering,:evaluation)"
            ),
            {
                "actor": actor, "objective": objective, "operation": operation,
                "fingerprint": fingerprint, "expected_definition": expected_definition,
                "expected_source": expected_source, "recurrence": recurrence_state,
                "zone": ZONE, "label": "Corsa sette km",
                "kind": "quantity", "comparator": "gte",
                "target": 7, "minimum": None, "maximum": None,
                "unit": "km", "ordering": 0, "evaluation": uuid7(),
            },
        )).mappings().one()


async def _objective_for_occurrence(runtime: Any, actor: UUID, occurrence: UUID) -> UUID:
    async with runtime.session_factory() as session, session.begin():
        return (await session.execute(
            text("""
                SELECT obj.objective_ref
                  FROM dante.routine_occurrence_activity_instance link
                  JOIN dante.temporal_objective obj
                    ON obj.subject_native_ref=link.activity_ref
                   AND obj.self_person_ref=:actor AND obj.subject_kind='activity'
                 WHERE link.occurrence_ref=:occurrence AND link.self_person_ref=:actor
            """),
            {"actor": actor, "occurrence": occurrence},
        )).scalar_one()


@pytest.mark.asyncio
async def test_generated_routine_objective_scope_selected_past_and_later_future(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    now = datetime.now(ZoneInfo(ZONE)).date()
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policy = RoutineOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        created = await authoring.create_routine(
            self_person_ref=alice,
            operation_id="m2scope:routine",
            title="Corsa",
            life_area_intent=None,
            recurrence=_daily(now - timedelta(days=3)),
        )
        await policy.set(
            self_person_ref=alice,
            routine_ref=created.source_ref,
            duration_minutes=60,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "objectives": [{
                    "label": "Corsa dieci km",
                    "result_kind": "quantity",
                    "comparator_code": "gte",
                    "target_value": 10,
                    "unit_code": "km",
                    "presentation_order": 0,
                }],
            },
        )
        # Materialize three past and three future Occurrences.
        await materializer.checkpoint_window(
            self_person_ref=alice, operation_id="m2scope:past",
            start_date=now - timedelta(days=3),
            end_date_exclusive=now,
            effective_zone_id=ZONE,
        )
        await materializer.checkpoint_window(
            self_person_ref=alice, operation_id="m2scope:future",
            start_date=now + timedelta(days=2),
            end_date_exclusive=now + timedelta(days=5),
            effective_zone_id=ZONE,
        )
        async with runtime.session_factory() as session, session.begin():
            occurrences = (await session.execute(
                text("""
                    SELECT g.occurrence_ref,g.generated_date
                      FROM dante.occurrence_generation g
                     WHERE g.source_native_ref=:source
                     ORDER BY g.generated_date,g.occurrence_ref
                """),
                {"source": created.source_ref},
            )).all()
        assert len(occurrences) == 6
        ids = [row[0] for row in occurrences]
        objectives = [
            await _objective_for_occurrence(runtime, alice, occurrence)
            for occurrence in ids
        ]
        state = await _series_state(runtime, alice, objectives[0])
        assert state is not None
        assert state.source_native_ref == created.source_ref
        assert state.template_slot == 0
        assert state.source_revision == 0
        assert await _series_state(runtime, bob, objectives[0]) is None

        accepted = await _apply(
            runtime, alice, objectives[0], operation="m2scope:past-following",
            recurrence_state=state.recurrence_state_ref,
        )
        assert accepted.replayed is False
        assert accepted.source_revision == 1
        assert accepted.objective_ref == objectives[0]
        assert (await _definition(runtime, alice, objectives[0])).label == "Corsa sette km"
        for objective in objectives[1:3]:
            assert (await _definition(runtime, alice, objective)).label == "Corsa dieci km"
        for objective in objectives[3:]:
            assert (await _definition(runtime, alice, objective)).label == "Corsa sette km"

        # A future Occurrence generated after acceptance inherits the policy.
        await materializer.checkpoint_window(
            self_person_ref=alice, operation_id="m2scope:later",
            start_date=now + timedelta(days=5),
            end_date_exclusive=now + timedelta(days=6),
            effective_zone_id=ZONE,
        )
        async with runtime.session_factory() as session, session.begin():
            later_ref = (await session.execute(
                text("""
                    SELECT occurrence_ref FROM dante.occurrence_generation
                     WHERE source_native_ref=:source AND generated_date=:day
                """),
                {"source": created.source_ref, "day": now + timedelta(days=5)},
            )).scalar_one()
        later_objective = await _objective_for_occurrence(runtime, alice, later_ref)
        assert (await _definition(runtime, alice, later_objective)).label == "Corsa sette km"

        replay = await _apply(
            runtime, alice, objectives[0], operation="m2scope:past-following",
            recurrence_state=state.recurrence_state_ref,
        )
        assert replay.replayed is True
        assert replay.source_revision == 1
        with pytest.raises(DBAPIError):
            await _apply(
                runtime, alice, objectives[0], operation="m2scope:stale",
                recurrence_state=state.recurrence_state_ref,
                expected_source=0,
            )
        with pytest.raises(DBAPIError):
            await _apply(
                runtime, bob, objectives[0], operation="m2scope:cross-owner",
                recurrence_state=state.recurrence_state_ref,
            )

        # A future Objective individually corrected after source inheritance
        # blocks the next series change rather than being silently overwritten.
        future_objective = objectives[4]
        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                text(
                    "SELECT * FROM dante.revise_self_temporal_objective_definition("
                    ":actor,:operation,:fingerprint,:objective,0,:label,'quantity',"
                    "'gte',9,NULL,NULL,'km',0,:evaluation)"
                ),
                {
                    "actor": alice, "operation": "m2scope:local",
                    "fingerprint": "b" * 64, "objective": future_objective,
                    "label": "Correzione personale", "evaluation": uuid7(),
                },
            )
        with pytest.raises(DBAPIError):
            await _apply(
                runtime, alice, objectives[0], operation="m2scope:blocked",
                recurrence_state=state.recurrence_state_ref,
                expected_source=1, expected_definition=1,
            )
        assert (await _definition(runtime, alice, objectives[4])).label == (
            "Correzione personale"
        )
        assert (await _definition(runtime, alice, objectives[1])).label == (
            "Corsa dieci km"
        )
    finally:
        await runtime.dispose()



@pytest.mark.asyncio
async def test_generated_event_objectives_share_future_scope_without_copying_results(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    authoring = RecurringAuthoringApplication(runtime.session_factory)
    policy = EventOccurrencePolicyApplication(runtime.session_factory)
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        source = await authoring.create_event(
            self_person_ref=actor, operation_id="m2scope:event",
            title="Riunione", life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await policy.set(
            self_person_ref=actor, event_ref=source.source_ref,
            placement_kind="timed", duration_minutes=60,
            duration_days=None, reminder_lead_minutes=None,
            objectives=({
                "label": "Arrivare puntuale",
                "result_kind": "boolean",
                "presentation_order": 0,
            },),
        )
        for token, day in (("past", 6), ("future", 13)):
            await materializer.checkpoint_window(
                self_person_ref=actor,
                operation_id=f"m2scope:event:{token}",
                start_date=datetime(2026, 10, day, tzinfo=ZoneInfo(ZONE)).date(),
                end_date_exclusive=datetime(
                    2026, 10, day, tzinfo=ZoneInfo(ZONE)
                ).date() + timedelta(days=1),
                effective_zone_id=ZONE,
            )
        async with runtime.session_factory() as session, session.begin():
            matches = (await session.execute(
                text("""
                    SELECT obj.objective_ref
                      FROM dante.temporal_objective obj
                      JOIN dante.occurrence_generation generation
                        ON generation.occurrence_ref=obj.subject_native_ref
                     WHERE generation.source_native_ref=:source
                       AND obj.subject_kind='occurrence'
                     ORDER BY generation.generated_date
                """),
                {"source": source.source_ref},
            )).scalars().all()
        assert len(matches) == 2
        past, future = matches
        state = await _series_state(runtime, actor, past)
        assert state is not None
        assert state.source_native_ref == source.source_ref
        assert state.template_slot == 0
        # A boolean Objective remains boolean. The template propagation is
        # driven by canonical Objective slot, not by UI display ordering.
        async with runtime.session_factory() as session, session.begin():
            row = (await session.execute(
                text(
                    "SELECT * FROM dante.accept_self_objective_series_edit("
                    ":actor,:objective,:operation,:fingerprint,0,0,:recurrence,"
                    ":zone,:label,'boolean',NULL,NULL,NULL,NULL,NULL,0,:evaluation)"
                ),
                {
                    "actor": actor, "objective": past,
                    "operation": "m2scope:event:series",
                    "fingerprint": "c" * 64,
                    "recurrence": state.recurrence_state_ref,
                    "zone": ZONE, "label": "Partenza puntuale",
                    "evaluation": uuid7(),
                },
            )).mappings().one()
        assert row.source_revision == 1
        assert (await _definition(runtime, actor, past)).label == "Partenza puntuale"
        assert (await _definition(runtime, actor, future)).label == "Partenza puntuale"
        assert (await _definition(runtime, actor, future)).evaluation_state_ref is None
    finally:
        await runtime.dispose()
