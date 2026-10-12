"""B10-C PostgreSQL proof for contextual Confirmation pinned to Outcome MaterialState."""

from __future__ import annotations

from typing import Any

import psycopg
import pytest

from dante.modules.temporal.actual_runtime import ActualApplication
from dante.modules.temporal.activity import TemporalActivityApplication
from dante.modules.temporal.confirmation_runtime import (
    ConfirmationApplication,
    ConfirmationCurrentConflictError,
    ConfirmationNotFoundError,
    ConfirmationOperationReuseError,
)
from dante.modules.temporal.life_area import LifeAreaApplication
from dante.modules.temporal.outcome_runtime import OutcomeApplication
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
async def test_b10_c_confirmation_is_actor_purpose_and_outcome_state_scoped(
    migrated_database: Any,
) -> None:
    alice = _seed_self(migrated_database)
    bob = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    areas = LifeAreaApplication(runtime.session_factory)
    activities = TemporalActivityApplication(runtime.session_factory)
    actuals = ActualApplication(runtime.session_factory)
    outcomes = OutcomeApplication(runtime.session_factory)
    confirmations = ConfirmationApplication(runtime.session_factory)
    try:
        area = (
            await areas.create(
                self_person_ref=alice,
                operation_id="b10-c:area",
                name="Confirmation proof",
            )
        ).area
        activity = (
            await activities.create_activity(
                self_person_ref=alice,
                operation_id="b10-c:activity",
                title="Attestation target",
                life_area_ref=area.life_area_ref,
            )
        ).activity
        actual = await actuals.record(
            self_person_ref=alice,
            operation_id="b10-c:actual",
            subject_kind="activity",
            subject_native_ref=activity.activity_ref,
            realization_occurred=True,
            expected_material_state_ref=None,
        )
        outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-c:outcome",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=None,
            disposition_code="work.completed",
        )

        assert await confirmations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        ) == ()
        assert (
            await confirmations.list_for_outcome(
                self_person_ref=bob,
                outcome_ref=outcome.outcome_ref,
            )
            is None
        )

        first = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-c:alice:first",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="attested",
        )
        assert first.outcome_ref == outcome.outcome_ref
        assert first.outcome_disposition_material_state_ref == outcome.material_state_ref
        assert first.confirmer_person_ref == alice
        assert first.purpose_code == "review.personal"
        assert first.stance_code == "attested"
        assert first.confirmer_is_self
        assert not first.replayed

        replay = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-c:alice:first",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="attested",
        )
        assert replay.replayed
        assert replay.confirmation_ref == first.confirmation_ref
        assert replay.material_state_ref == first.material_state_ref

        with pytest.raises(ConfirmationOperationReuseError):
            await confirmations.record(
                self_person_ref=alice,
                operation_id="b10-c:alice:first",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=first.material_state_ref,
                purpose_code="review.personal",
                stance_code="retracted",
            )

        corrected = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-c:alice:correct",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=first.material_state_ref,
            purpose_code="review.personal",
            stance_code="retracted",
        )
        assert corrected.confirmation_ref == first.confirmation_ref
        assert corrected.material_state_ref != first.material_state_ref
        assert corrected.stance_code == "retracted"
        assert corrected.outcome_disposition_material_state_ref == outcome.material_state_ref

        with pytest.raises(ConfirmationCurrentConflictError):
            await confirmations.record(
                self_person_ref=alice,
                operation_id="b10-c:alice:stale",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=outcome.material_state_ref,
                expected_material_state_ref=first.material_state_ref,
                purpose_code="review.personal",
                stance_code="attested",
            )

        bob_first = await confirmations.record(
            self_person_ref=bob,
            operation_id="b10-c:bob:first",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="disputed",
        )
        assert bob_first.confirmation_ref != first.confirmation_ref
        assert bob_first.confirmer_person_ref == bob
        assert bob_first.outcome_disposition_material_state_ref == outcome.material_state_ref
        assert bob_first.stance_code == "disputed"

        listed = await confirmations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        )
        assert listed is not None
        assert {item.confirmation_ref for item in listed} == {
            first.confirmation_ref,
            bob_first.confirmation_ref,
        }
        own = next(item for item in listed if item.confirmer_is_self)
        other = next(item for item in listed if not item.confirmer_is_self)
        assert own.stance_code == "retracted"
        assert other.stance_code == "disputed"

        history = await confirmations.history(
            self_person_ref=alice,
            confirmation_ref=first.confirmation_ref,
        )
        assert [item.material_state_ref for item in history] == [
            first.material_state_ref,
            corrected.material_state_ref,
        ]
        assert history[0].current_until_at is not None
        assert history[1].current_until_at is None

        bob_history = await confirmations.history(
            self_person_ref=bob,
            confirmation_ref=bob_first.confirmation_ref,
        )
        assert [item.confirmation_ref for item in bob_history] == [bob_first.confirmation_ref]

        with pytest.raises(ConfirmationNotFoundError):
            await confirmations.history(
                self_person_ref=bob,
                confirmation_ref=first.confirmation_ref,
            )

        corrected_outcome = await outcomes.record(
            self_person_ref=alice,
            operation_id="b10-c:outcome:correct",
            actual_ref=actual.actual_ref,
            actual_realization_material_state_ref=actual.material_state_ref,
            expected_material_state_ref=outcome.material_state_ref,
            disposition_code="work.partial",
        )
        assert corrected_outcome.outcome_ref == outcome.outcome_ref
        assert corrected_outcome.material_state_ref != outcome.material_state_ref

        still_listed = await confirmations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        )
        assert still_listed is not None
        assert {item.confirmation_ref for item in still_listed} == {
            first.confirmation_ref,
            bob_first.confirmation_ref,
        }
        assert {
            item.outcome_disposition_material_state_ref for item in still_listed
        } == {outcome.material_state_ref}

        on_new_state = await confirmations.record(
            self_person_ref=alice,
            operation_id="b10-c:alice:new-state",
            outcome_ref=outcome.outcome_ref,
            outcome_disposition_material_state_ref=corrected_outcome.material_state_ref,
            expected_material_state_ref=None,
            purpose_code="review.personal",
            stance_code="attested",
        )
        assert on_new_state.confirmation_ref != first.confirmation_ref
        assert (
            on_new_state.outcome_disposition_material_state_ref
            == corrected_outcome.material_state_ref
        )

        after_new = await confirmations.list_for_outcome(
            self_person_ref=alice,
            outcome_ref=outcome.outcome_ref,
        )
        assert after_new is not None
        assert len(after_new) == 3
        pinned_old = [item for item in after_new if item.confirmation_ref == first.confirmation_ref]
        assert pinned_old[0].outcome_disposition_material_state_ref == outcome.material_state_ref
        assert pinned_old[0].stance_code == "retracted"

        with pytest.raises(ConfirmationNotFoundError):
            await confirmations.record(
                self_person_ref=alice,
                operation_id="b10-c:missing-target",
                outcome_ref=outcome.outcome_ref,
                outcome_disposition_material_state_ref=actual.material_state_ref,
                expected_material_state_ref=None,
                purpose_code="review.personal",
                stance_code="attested",
            )

        with _admin(migrated_database) as connection:
            proof = connection.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.confirmation WHERE outcome_ref=%s),
                  (SELECT count(*) FROM dante.confirmation
                    WHERE outcome_disposition_material_state_ref=%s),
                  (SELECT count(*) FROM dante.confirmation_attestation_state
                    WHERE confirmation_ref=%s),
                  (SELECT material_state_ref
                     FROM dante.scoped_current_material_state
                    WHERE scoped_owner_ref=%s AND facet_code='confirmation.attestation')
                """,
                (
                    outcome.outcome_ref,
                    outcome.material_state_ref,
                    first.confirmation_ref,
                    first.confirmation_ref,
                ),
            ).fetchone()
        assert proof == (3, 2, 2, corrected.material_state_ref)
    finally:
        await runtime.dispose()
