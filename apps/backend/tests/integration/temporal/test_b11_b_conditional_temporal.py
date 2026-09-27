"""B11-B PostgreSQL proof for bounded Actual-realization conditions."""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.conditional_temporal import (
    ConditionalTemporalApplication,
    ConditionalTemporalOperationReuseError,
)
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.occurrence import OccurrenceApplication
from dante.modules.temporal.routine import RoutineApplication
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from tests.integration.temporal.test_b05_primary_life_area_assignment import _seed_self

pytestmark = pytest.mark.postgres


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


@pytest.mark.asyncio
async def test_b11_b_actual_realization_condition_pins_exact_current_truth(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    conditions = ConditionalTemporalApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b11-b:area",
                name="Conditional proof",
            )
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="b11-b:routine",
            title="Condition source",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 5),
            wall_time=time(8),
        )
        checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="b11-b:seed-occurrence",
            start_date=date(2026, 10, 5),
            end_date_exclusive=date(2026, 10, 6),
            effective_zone_id="Europe/Rome",
        )
        assert len(checkpoint.occurrences) == 1
        occurrence_ref = NativeRef(checkpoint.occurrences[0].occurrence_ref)

        condition = await conditions.create_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-b:create-condition",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
        )
        assert condition.family_code == "actual_realization"
        assert condition.subject_kind == "occurrence"
        assert condition.subject_native_ref == occurrence_ref
        assert not condition.replayed

        create_replay = await conditions.create_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-b:create-condition",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
        )
        assert create_replay.replayed
        assert create_replay.condition_ref == condition.condition_ref

        unknown = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-b:evaluate:unknown",
            condition_ref=condition.condition_ref,
        )
        assert unknown.result_code == "indeterminate"
        assert unknown.disposition_code == "withhold"
        assert unknown.actual_ref is None
        assert unknown.actual_realization_material_state_ref is None

        # Session lifecycle remains execution context only. Ending a Session must
        # not fabricate the Actual truth consumed by a B11-B condition.
        session = await sessions.start(
            self_person_ref=alice,
            operation_id="b11-b:session-start",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
        )
        ended = await sessions.end(
            self_person_ref=alice,
            operation_id="b11-b:session-end",
            session_ref=session.session_ref,
            expected_material_state_ref=session.timing_material_state_ref,
        )
        assert ended.ended_at is not None

        after_session = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-b:evaluate:after-session",
            condition_ref=condition.condition_ref,
        )
        assert after_session.result_code == "indeterminate"
        assert after_session.disposition_code == "withhold"
        assert after_session.actual_ref is None
        assert after_session.actual_realization_material_state_ref is None

        started_at = datetime(2026, 10, 5, 8, 0, tzinfo=UTC)
        ended_at = started_at + timedelta(minutes=45)
        realized = await actuals.record(
            self_person_ref=alice,
            operation_id="b11-b:actual:true",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
            extent_code="interval",
            started_at=started_at,
            ended_at=ended_at,
        )

        satisfied = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-b:evaluate:satisfied",
            condition_ref=condition.condition_ref,
        )
        assert satisfied.result_code == "satisfied"
        assert satisfied.disposition_code == "allow"
        assert satisfied.actual_ref == realized.actual_ref
        assert satisfied.actual_realization_material_state_ref == realized.material_state_ref
        assert not satisfied.replayed

        replay = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-b:evaluate:satisfied",
            condition_ref=condition.condition_ref,
        )
        assert replay.replayed
        assert replay.evaluation_ref == satisfied.evaluation_ref
        assert replay.actual_realization_material_state_ref == realized.material_state_ref

        corrected = await actuals.record(
            self_person_ref=alice,
            operation_id="b11-b:actual:false-correction",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
            realization_occurred=False,
            expected_material_state_ref=realized.material_state_ref,
        )
        assert corrected.material_state_ref != realized.material_state_ref

        not_satisfied = await conditions.evaluate_actual_realization_condition(
            self_person_ref=alice,
            operation_id="b11-b:evaluate:not-satisfied",
            condition_ref=condition.condition_ref,
        )
        assert not_satisfied.result_code == "not_satisfied"
        assert not_satisfied.disposition_code == "withhold"
        assert not_satisfied.actual_ref == realized.actual_ref
        assert not_satisfied.actual_realization_material_state_ref == corrected.material_state_ref
        assert not_satisfied.evaluation_ref != satisfied.evaluation_ref

        with pytest.raises(ConditionalTemporalOperationReuseError):
            await conditions.create_actual_realization_condition(
                self_person_ref=alice,
                operation_id="b11-b:evaluate:satisfied",
                subject_kind="occurrence",
                subject_native_ref=occurrence_ref,
            )

        with _admin(migrated_database) as connection:
            rows = connection.execute(
                """
                SELECT evaluation_ref,result_code,disposition_code,
                       actual_ref,actual_realization_material_state_ref
                  FROM dante.conditional_temporal_evaluation
                 WHERE condition_ref=%s
                 ORDER BY evaluated_at,evaluation_ref
                """,
                (condition.condition_ref,),
            ).fetchall()
            operation_count = connection.execute(
                """
                SELECT count(*)
                  FROM dante.conditional_temporal_operation
                 WHERE self_person_ref=%s
                   AND condition_ref=%s
                """,
                (alice, condition.condition_ref),
            ).fetchone()

        assert len(rows) == 4
        assert rows[0][1:3] == ("indeterminate", "withhold")
        assert rows[1][1:3] == ("indeterminate", "withhold")
        assert rows[2][0] == satisfied.evaluation_ref
        assert rows[2][1:3] == ("satisfied", "allow")
        assert rows[2][3] == realized.actual_ref
        assert rows[2][4] == realized.material_state_ref
        assert rows[3][0] == not_satisfied.evaluation_ref
        assert rows[3][1:3] == ("not_satisfied", "withhold")
        assert rows[3][3] == realized.actual_ref
        assert rows[3][4] == corrected.material_state_ref
        # One create receipt + four distinct evaluation receipts. Replay did not
        # create another evaluation/operation and no operation id became identity.
        assert operation_count == (5,)
    finally:
        await runtime.dispose()
