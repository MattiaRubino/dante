"""B10-B PostgreSQL proof for canonical Outcome disposition and history truth."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.outcome_runtime import (
    OutcomeApplication,
    OutcomeCurrentConflictError,
    OutcomeNotFoundError,
    OutcomeOperationReuseError,
)
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
async def test_b10_b_outcome_is_append_only_idempotent_and_pinned_to_exact_actual_state(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    outcomes = OutcomeApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b10-b:area",
                name="Outcome proof",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b10-b:activity",
                title="Contextual disposition",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-b:actual",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
        )

        with pytest.raises(OutcomeNotFoundError):
            await outcomes.get_for_actual(
                self_person_ref=alice,
                actual_ref=actual.actual_ref,
            )

        first = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:first",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=None,
            disposition_code="work.completed",
        )
        assert first.actual_ref == actual.actual_ref
        assert first.actual_realization_material_state_ref == actual.material_state_ref
        assert first.disposition_code == "work.completed"
        assert not first.replayed

        replay = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:first",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=None,
            disposition_code="work.completed",
        )
        assert replay.replayed
        assert replay.outcome_ref == first.outcome_ref
        assert replay.material_state_ref == first.material_state_ref

        with pytest.raises(OutcomeOperationReuseError):
            await outcomes.record(
                self_person_ref=alice,
                operation_id="b10-b:outcome:first",
                actual_ref=actual.actual_ref,
                actual_realization_material_state_ref=actual.material_state_ref,
                expected_material_state_ref=first.material_state_ref,
                disposition_code="work.partial",
            )

        corrected = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:correct",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=first.material_state_ref,
            disposition_code="work.partial",
        )
        assert corrected.outcome_ref == first.outcome_ref
        assert corrected.material_state_ref != first.material_state_ref
        assert corrected.disposition_code == "work.partial"

        current = await outcomes.get_for_actual(
            self_person_ref=alice,
            actual_ref=actual.actual_ref,
        )
        assert current.material_state_ref == corrected.material_state_ref
        assert current.disposition_code == "work.partial"

        history = await outcomes.history(
            self_person_ref=alice,
            outcome_ref=first.outcome_ref,
        )
        assert [item.material_state_ref for item in history] == [
            first.material_state_ref,
            corrected.material_state_ref,
        ]
        assert history[0].current_until_at is not None
        assert history[1].current_until_at is None

        with pytest.raises(OutcomeCurrentConflictError):
            await outcomes.record(
                self_person_ref=alice,
                operation_id="b10-b:outcome:stale",
                actual_ref=actual.actual_ref,
                actual_realization_material_state_ref=actual.material_state_ref,
                expected_material_state_ref=first.material_state_ref,
                disposition_code="work.completed",
            )

        with pytest.raises(OutcomeNotFoundError):
            await outcomes.get_for_actual(
                self_person_ref=bob,
                actual_ref=actual.actual_ref,
            )

        corrected_actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-b:actual:correct",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=False,
            expected_material_state_ref=actual.material_state_ref,
        )
        assert corrected_actual.material_state_ref != actual.material_state_ref

        with pytest.raises(OutcomeCurrentConflictError):
            await outcomes.record(
                self_person_ref=alice,
                operation_id="b10-b:outcome:old-actual-basis",
                actual_ref=actual.actual_ref,
                actual_realization_material_state_ref=actual.material_state_ref,
                expected_material_state_ref=corrected.material_state_ref,
                disposition_code="work.cancelled",
            )

        rebased = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-b:outcome:new-actual-basis",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=corrected_actual.material_state_ref,
            expected_material_state_ref=corrected.material_state_ref,
            disposition_code="work.cancelled",
        )
        assert rebased.outcome_ref == first.outcome_ref
        assert rebased.actual_realization_material_state_ref == corrected_actual.material_state_ref

        with _admin(migrated_database) as connection:
            proof = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.outcome WHERE actual_ref=%s),
                  (SELECT count(*) FROM dante.outcome_disposition_state WHERE outcome_ref=%s),
                  (SELECT count(*) FROM dante.outcome_disposition_current_history WHERE outcome_ref=%s),
                  (SELECT material_state_ref
                     FROM dante.scoped_current_material_state
                    WHERE scoped_owner_ref=%s AND facet_code='outcome.disposition'),
                  (SELECT count(*) FROM dante.actual_realization_state WHERE actual_ref=%s)
                """,
                (
                    actual.actual_ref,
                    first.outcome_ref,
                    first.outcome_ref,
                    first.outcome_ref,
                    actual.actual_ref,
                ),
            ).fetchone()
        assert proof == (1, 3, 3, rebased.material_state_ref, 2)
    finally:
        await runtime.dispose()
