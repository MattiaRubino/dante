"""B10-A PostgreSQL proof for Actual realization authoring and authoritative reads."""

from __future__ import annotations

from datetime import UTC, date, datetime, time, timedelta
from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import (
    ActualApplication,
    ActualCurrentConflictError,
    ActualNotFoundError,
    ActualOperationReuseError,
    ActualSessionBasis,
)
from dante.modules.temporal.activity import TemporalActivityApplication
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
async def test_b10_a_activity_actual_is_append_only_idempotent_and_session_basis_is_exact(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b10-a:activity-area",
                name="Reality",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b10-a:activity",
                title="Prove Actual",
                life_area_ref=area.life_area_ref,
            )
        ).activity

        started_session = await sessions.start(
            self_person_ref=alice,
            operation_id="b10-a:session-start",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        with _admin(migrated_database) as connection:
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s",
                (activity.activity_ref,),
            ).fetchone() == (0,)

        not_occurred = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-a:actual:first",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=False,
            expected_material_state_ref=None,
        )
        assert not not_occurred.realization_occurred
        assert not_occurred.extent_code is None
        assert not_occurred.session_bases == ()
        assert not not_occurred.replayed

        replay = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-a:actual:first",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=False,
            expected_material_state_ref=None,
        )
        assert replay.replayed
        assert replay.actual_ref == not_occurred.actual_ref
        assert replay.material_state_ref == not_occurred.material_state_ref

        with pytest.raises(ActualOperationReuseError):
            await actuals.record(
                self_person_ref=alice,
                operation_id="b10-a:actual:first",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                realization_occurred=True,
                expected_material_state_ref=not_occurred.material_state_ref,
            )

        began = datetime(2026, 9, 25, 8, 30, tzinfo=UTC)
        ended = began + timedelta(minutes=40)
        occurred = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-a:actual:second",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=not_occurred.material_state_ref,
            extent_code="interval",
            started_at=began,
            ended_at=ended,
            session_bases=(
                ActualSessionBasis(
                    session_ref=started_session.session_ref,
                    session_timing_material_state_ref=started_session.timing_material_state_ref,
                ),
            ),
        )
        assert occurred.actual_ref == not_occurred.actual_ref
        assert occurred.material_state_ref != not_occurred.material_state_ref
        assert occurred.realization_occurred
        assert occurred.extent_code == "interval"
        assert occurred.started_at == began
        assert occurred.ended_at == ended
        assert occurred.session_bases == (
            ActualSessionBasis(
                session_ref=started_session.session_ref,
                session_timing_material_state_ref=started_session.timing_material_state_ref,
            ),
        )

        current = await actuals.get_for_subject(
            self_person_ref=alice,
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
        )
        assert current.material_state_ref == occurred.material_state_ref
        assert current.realization_occurred
        assert current.session_bases == occurred.session_bases

        history = await actuals.history(
            self_person_ref=alice,
            actual_ref=occurred.actual_ref,
        )
        # Canonical history is newest-first by current_from_at.
        assert [item.material_state_ref for item in history] == [
            occurred.material_state_ref,
            not_occurred.material_state_ref,
        ]
        assert history[0].current_until_at is None
        assert history[1].current_until_at is not None

        with pytest.raises(ActualCurrentConflictError):
            await actuals.record(
                self_person_ref=alice,
                operation_id="b10-a:actual:stale",
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
                realization_occurred=False,
                expected_material_state_ref=not_occurred.material_state_ref,
            )
        with pytest.raises(ActualNotFoundError):
            await actuals.get_for_subject(
                self_person_ref=alice,
                subject_kind="event",
                subject_native_ref=activity.activity_ref,
            )
        with pytest.raises(ActualNotFoundError):
            await actuals.get_for_subject(
                self_person_ref=bob,
                subject_kind="activity",
                subject_native_ref=activity.activity_ref,
            )

        with _admin(migrated_database) as connection:
            proof = connection.execute(
                """
                SELECT
                  (SELECT material_state_ref
                     FROM dante.scoped_current_material_state
                    WHERE scoped_owner_ref=%s AND facet_code='actual.realization'),
                  (SELECT count(*) FROM dante.actual_realization_state
                    WHERE actual_ref=%s),
                  (SELECT count(*) FROM dante.actual_realization_current_history
                    WHERE actual_ref=%s),
                  (SELECT session_timing_material_state_ref
                     FROM dante.actual_realization_session_basis
                    WHERE actual_material_state_ref=%s)
                """,
                (
                    occurred.actual_ref,
                    occurred.actual_ref,
                    occurred.actual_ref,
                    occurred.material_state_ref,
                ),
            ).fetchone()
        assert proof == (
            occurred.material_state_ref,
            2,
            2,
            started_session.timing_material_state_ref,
        )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_b10_a_occurrence_uses_occurrence_identity_and_never_activity_family(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    routines = RoutineApplication(runtime.session_factory)
    occurrences = OccurrenceApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b10-a:occurrence-area",
                name="Routine reality",
            )
        ).area
        routine = await routines.create(
            self_person_ref=alice,
            operation_id="b10-a:routine",
            title="Occurrence Actual proof",
            life_area_ref=area.life_area_ref,
            starts_on=date(2026, 10, 1),
            wall_time=time(8),
        )
        checkpoint = await occurrences.checkpoint(
            owner="routine",
            self_person_ref=alice,
            source_ref=routine.routine_ref,
            operation_id="b10-a:occurrence-checkpoint",
            start_date=date(2026, 10, 1),
            end_date_exclusive=date(2026, 10, 2),
            effective_zone_id="Europe/Rome",
        )
        occurrence_ref = NativeRef(checkpoint.occurrences[0].occurrence_ref)

        recorded = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-a:occurrence-actual",
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
        )
        assert recorded.subject_native_ref == occurrence_ref
        assert recorded.realization_occurred

        current = await actuals.get_for_subject(
            self_person_ref=alice,
            subject_kind="occurrence",
            subject_native_ref=occurrence_ref,
        )
        assert current.actual_ref == recorded.actual_ref
        assert current.material_state_ref == recorded.material_state_ref

        with pytest.raises(ActualNotFoundError):
            await actuals.get_for_subject(
                self_person_ref=alice,
                subject_kind="activity",
                subject_native_ref=occurrence_ref,
            )
        with pytest.raises(ActualNotFoundError):
            await actuals.record(
                self_person_ref=alice,
                operation_id="b10-a:occurrence-wrong-family",
                subject_kind="activity",
                subject_native_ref=occurrence_ref,
                realization_occurred=True,
                expected_material_state_ref=recorded.material_state_ref,
            )
    finally:
        await runtime.dispose()
