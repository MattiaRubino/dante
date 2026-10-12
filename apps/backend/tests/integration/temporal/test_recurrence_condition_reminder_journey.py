"""B11-D proof that Recurrence, Condition and Reminder retain separate authorities."""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from typing import Any

import psycopg
import pytest
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.advanced_recurrence import (
    AdvancedElapsedRecurrence,
    AdvancedRecurrenceApplication,
)
from dante.modules.temporal.conditional_temporal import ConditionalTemporalApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication
from dante.modules.temporal.recurrence import RecurrenceApplication
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    TemporalScheduleApplication,
)
from dante.modules.temporal.schedule_reminder import ScheduleReminderApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


@pytest.mark.asyncio
async def test_b11_d_canonical_chain_preserves_independent_history(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    recurrences = RecurrenceApplication(runtime.session_factory)
    advanced = AdvancedRecurrenceApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    conditions = ConditionalTemporalApplication(runtime.session_factory)
    schedules = TemporalScheduleApplication(runtime.session_factory)
    reminders = ScheduleReminderApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b11-d:area",
                name="Whole B11 integration",
            )
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="b11-d:routine",
            title="Completion chain",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        seed = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="b11-d:seed",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        assert len(seed.occurrences) == 1
        anchor_ref = NativeRef(seed.occurrences[0].occurrence_ref)

        current_rule = await recurrences.get(
            owner="routine", self_person_ref=alice, owner_ref=routine.routine_ref
        )
        assert current_rule is not None
        assert await advanced.get(
            owner="routine", self_person_ref=alice, source_ref=routine.routine_ref
        ) is None
        rule = await advanced.replace(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-d:rule",
            source_ref=routine.routine_ref,
            expected_material_state_ref=current_rule.material_state_ref,
            recurrence=AdvancedElapsedRecurrence(
                range_kind="open",
                expected_occurrence_count=None,
                effective_from=datetime(2026, 10, 1, tzinfo=UTC),
                effective_until=None,
                elapsed_seconds=Decimal("3600.000000"),
                anchor_mode_code="previous_completion",
            ),
        )
        window_start = datetime(2026, 10, 1, tzinfo=UTC)
        window_end = datetime(2026, 10, 4, tzinfo=UTC)
        blocked = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-d:before-actual",
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=rule.recurrence.material_state_ref,
            start_at=window_start,
            end_at_exclusive=window_end,
        )
        assert blocked.occurrences == ()

        completed_at = datetime(2026, 10, 1, 9, 45, tzinfo=UTC)
        anchor_actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b11-d:anchor-actual",
            subject_kind="occurrence",
            subject_native_ref=anchor_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
            extent_code="interval",
            started_at=completed_at - timedelta(minutes=45),
            ended_at=completed_at,
        )
        generated = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-d:after-actual",
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=rule.recurrence.material_state_ref,
            start_at=window_start,
            end_at_exclusive=window_end,
        )
        assert len(generated.occurrences) == 1
        dependent = generated.occurrences[0]
        dependent_ref = NativeRef(dependent.occurrence_ref)
        assert dependent.expected_at == completed_at + timedelta(hours=1)
        assert dependent.anchor_actual_ref == anchor_actual.actual_ref
        assert dependent.anchor_actual_material_state_ref == anchor_actual.material_state_ref

        condition = await conditions.create_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-d:condition",
            subject_kind="occurrence",
            subject_native_ref=dependent_ref,
        )
        unknown = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-d:unknown",
            condition_ref=condition.condition_ref,
        )
        assert (unknown.result_code, unknown.disposition_code) == (
            "indeterminate", "withhold"
        )
        assert unknown.actual_ref is None

        starts_at = dependent.expected_at + timedelta(days=1)
        schedule = await schedules.establish_schedule(
            self_person_ref=alice,
            operation_id="b11-d:schedule",
            subject_native_ref=dependent_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=starts_at, ends_at=starts_at + timedelta(hours=1)
            ),
        )
        reminder = await reminders.configure(
            self_person_ref=alice,
            schedule_ref=schedule.schedule_ref,
            operation_id="b11-d:reminder",
            expected_material_state_ref=None,
            enabled=True,
            lead_minutes=30,
        )
        assert reminder.due_at == starts_at - timedelta(minutes=30)
        still_unknown = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-d:after-schedule",
            condition_ref=condition.condition_ref,
        )
        assert (still_unknown.result_code, still_unknown.disposition_code) == (
            "indeterminate", "withhold"
        )

        dependent_actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b11-d:dependent-actual",
            subject_kind="occurrence",
            subject_native_ref=dependent_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
            extent_code="interval",
            started_at=dependent.expected_at,
            ended_at=dependent.expected_at + timedelta(minutes=30),
        )
        satisfied = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-d:satisfied",
            condition_ref=condition.condition_ref,
        )
        assert (satisfied.result_code, satisfied.disposition_code) == (
            "satisfied", "allow"
        )
        assert satisfied.actual_ref == dependent_actual.actual_ref
        assert satisfied.actual_realization_material_state_ref == (
            dependent_actual.material_state_ref
        )
        unchanged_reminder = await reminders.get(
            self_person_ref=alice, schedule_ref=schedule.schedule_ref
        )
        assert unchanged_reminder is not None
        assert unchanged_reminder.material_state_ref == reminder.material_state_ref
        assert unchanged_reminder.due_at == reminder.due_at

        corrected_actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b11-d:dependent-correction",
            subject_kind="occurrence",
            subject_native_ref=dependent_ref,
            realization_occurred=False,
            expected_material_state_ref=dependent_actual.material_state_ref,
        )
        corrected_evaluation = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-d:not-satisfied",
            condition_ref=condition.condition_ref,
        )
        assert (corrected_evaluation.result_code, corrected_evaluation.disposition_code) == (
            "not_satisfied", "withhold"
        )
        assert corrected_evaluation.actual_realization_material_state_ref == (
            corrected_actual.material_state_ref
        )

        revised_start = starts_at + timedelta(hours=2)
        await schedules.revise_schedule(
            self_person_ref=alice,
            operation_id="b11-d:revise-schedule",
            schedule_ref=schedule.schedule_ref,
            expected_material_state_ref=schedule.material_state_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=revised_start,
                ends_at=revised_start + timedelta(hours=1),
            ),
        )
        reloaded = await reminders.get(
            self_person_ref=alice, schedule_ref=schedule.schedule_ref
        )
        assert reloaded is not None
        assert reloaded.reminder_ref == reminder.reminder_ref
        assert reloaded.material_state_ref == reminder.material_state_ref
        assert reloaded.due_at == revised_start - timedelta(minutes=30)
        assert reloaded.due_at != reminder.due_at

        recurrence_replay = await advanced.checkpoint(
            owner="routine",
            self_person_ref=alice,
            operation_id="b11-d:after-actual",
            source_ref=routine.routine_ref,
            governing_recurrence_state_ref=rule.recurrence.material_state_ref,
            start_at=window_start,
            end_at_exclusive=window_end,
        )
        assert recurrence_replay.replayed
        assert recurrence_replay.occurrences[0].occurrence_ref == dependent.occurrence_ref

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            evaluations = connection.execute(
                """SELECT evaluation_ref,actual_realization_material_state_ref
                     FROM dante.conditional_temporal_evaluation
                    WHERE condition_ref=%s""",
                (condition.condition_ref,),
            ).fetchall()
            anchor = connection.execute(
                """SELECT anchor_actual_material_state_ref
                     FROM dante.occurrence_generation_actual_anchor
                    WHERE occurrence_ref=%s""",
                (dependent.occurrence_ref,),
            ).fetchone()
        assert (satisfied.evaluation_ref, dependent_actual.material_state_ref) in evaluations
        assert (
            corrected_evaluation.evaluation_ref,
            corrected_actual.material_state_ref,
        ) in evaluations
        assert anchor == (anchor_actual.material_state_ref,)
    finally:
        await runtime.dispose()
