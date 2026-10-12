"""Parent Actual admission follows direct required children and explicit policy."""

from __future__ import annotations

import hashlib
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest
from tests.integration.temporal.test_b04_f_constrained_activity_application import (
    _seed_activity,
    _seed_person,
)
from tests.integration.temporal.test_b14_u6_activity_decomposition import _mutate

from dante.modules.temporal.actual_runtime import ActualApplication, ActualParentGuardError
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _policy(database: Any, actor: UUID, activity: UUID, mode: str) -> UUID:
    with psycopg.connect(
        **database.connection_kwargs("dante_runtime", database.cluster.runtime_password)
    ) as connection:
        row = connection.execute(
            "SELECT * FROM dante.set_self_activity_decomposition_policy("
            "%s,%s,%s,%s,%s,%s,%s)",
            (actor, f"u6:guard:{activity}:{mode}", hashlib.sha256(mode.encode()).hexdigest(),
             activity, uuid7(), mode, None),
        ).fetchone()
        assert row is not None
        return row[0]


@pytest.mark.asyncio
async def test_parent_actual_block_confirm_and_none_keep_child_reality_independent(
    migrated_database: Any,
) -> None:
    actor = _seed_person(migrated_database)
    parent = _seed_activity(migrated_database, self_ref=actor, title="Parent")
    required = _seed_activity(migrated_database, self_ref=actor, title="Required")
    optional = _seed_activity(migrated_database, self_ref=actor, title="Optional")
    _mutate(migrated_database, actor=actor, operation="guard:required",
            relation=uuid7(), parent=parent, child=required)
    _mutate(migrated_database, actor=actor, operation="guard:optional",
            relation=uuid7(), parent=parent, child=optional, requirement="optional")
    _policy(migrated_database, actor, parent, "block")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    actuals = ActualApplication(runtime.session_factory)
    try:
        with pytest.raises(ActualParentGuardError):
            await actuals.record(
                self_person_ref=actor, operation_id="guard:blocked", subject_kind="activity",
                subject_native_ref=parent, realization_occurred=True,
                expected_material_state_ref=None,
            )
        child = await actuals.record(
            self_person_ref=actor, operation_id="guard:child", subject_kind="activity",
            subject_native_ref=required, realization_occurred=True,
            expected_material_state_ref=None,
        )
        assert child.realization_occurred
        accepted = await actuals.record(
            self_person_ref=actor, operation_id="guard:allowed", subject_kind="activity",
            subject_native_ref=parent, realization_occurred=True,
            expected_material_state_ref=None,
        )
        assert accepted.realization_occurred
        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password,
        )) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s", (optional,)
            ).fetchone() == (0,)

        confirm_parent = _seed_activity(migrated_database, self_ref=actor, title="Confirm")
        unresolved = _seed_activity(migrated_database, self_ref=actor, title="Unresolved")
        _mutate(migrated_database, actor=actor, operation="guard:confirm:attach",
                relation=uuid7(), parent=confirm_parent, child=unresolved)
        _policy(migrated_database, actor, confirm_parent, "confirm")
        with pytest.raises(ActualParentGuardError):
            await actuals.record(
                self_person_ref=actor, operation_id="guard:no-ack", subject_kind="activity",
                subject_native_ref=confirm_parent, realization_occurred=True,
                expected_material_state_ref=None,
            )
        confirmed = await actuals.record(
            self_person_ref=actor, operation_id="guard:ack", subject_kind="activity",
            subject_native_ref=confirm_parent, realization_occurred=True,
            expected_material_state_ref=None, acknowledge_unresolved_children=True,
        )
        replay = await actuals.record(
            self_person_ref=actor, operation_id="guard:ack", subject_kind="activity",
            subject_native_ref=confirm_parent, realization_occurred=True,
            expected_material_state_ref=None, acknowledge_unresolved_children=True,
        )
        assert confirmed.material_state_ref == replay.material_state_ref
        assert replay.replayed
        with psycopg.connect(**migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password,
        )) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.actual WHERE subject_native_ref=%s", (unresolved,)
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.activity_parent_actual_acknowledgement "
                "WHERE activity_ref=%s", (confirm_parent,)
            ).fetchone() == (1,)

        free_parent = _seed_activity(migrated_database, self_ref=actor, title="Free")
        free_child = _seed_activity(migrated_database, self_ref=actor, title="Still unknown")
        _mutate(migrated_database, actor=actor, operation="guard:free:attach",
                relation=uuid7(), parent=free_parent, child=free_child)
        free_actual = await actuals.record(
            self_person_ref=actor, operation_id="guard:none", subject_kind="activity",
            subject_native_ref=free_parent, realization_occurred=True,
            expected_material_state_ref=None,
        )
        assert free_actual.realization_occurred
    finally:
        await runtime.dispose()
