"""Real PostgreSQL proof for the B04-A Temporal Constraint application boundary."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.temporal_constraint import (
    AbsoluteEarliestStartRule,
    TemporalConstraintApplication,
    TemporalConstraintNotFoundError,
    TemporalConstraintOperationIdReuseError,
    TemporalConstraintStateConflictError,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime


def _seed_activity(database: Any) -> tuple[NativeRef, NativeRef]:
    self_person_ref = NativeRef(uuid7())
    activity_ref = NativeRef(uuid7())
    with psycopg.connect(
        **database.connection_kwargs(
            "dante_migrator",
            database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
        connection.execute(
            "INSERT INTO dante.person(person_ref) VALUES (%s)",
            (self_person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (self_person_ref,),
        )
        connection.execute(
            "INSERT INTO dante.activity(activity_ref) VALUES (%s)",
            (activity_ref,),
        )
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'activity')",
            (activity_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.activity_intention(
                activity_ref,self_person_ref,title,created_at
            ) VALUES (%s,%s,'Constraint subject',%s)
            """,
            (activity_ref, self_person_ref, datetime.now(UTC)),
        )
        connection.commit()
    return self_person_ref, activity_ref


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_a5_application_create_revise_read_list_retire_and_replay(
    migrated_database: Any,
) -> None:
    self_ref, activity_ref = _seed_activity(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    first_rule = AbsoluteEarliestStartRule(
        strength="hard",
        boundary_at=datetime(2026, 9, 24, 8, 0, tzinfo=UTC),
    )
    revised_rule = AbsoluteEarliestStartRule(
        strength="soft",
        boundary_at=datetime(2026, 9, 24, 10, 0, tzinfo=UTC),
    )

    try:
        created = await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-a5:application-create",
            subject_native_ref=activity_ref,
            rule=first_rule,
        )
        assert created.replayed is False
        assert created.subject_kind == "activity"

        create_replay = await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-a5:application-create",
            subject_native_ref=activity_ref,
            rule=first_rule,
        )
        assert create_replay.replayed is True
        assert create_replay.constraint_ref == created.constraint_ref
        assert create_replay.material_state_ref == created.material_state_ref
        assert create_replay.recorded_at == created.recorded_at

        current = await application.get_constraint(
            self_person_ref=self_ref,
            constraint_ref=created.constraint_ref,
        )
        assert current.status == "active"
        assert current.current_rule is not None
        assert current.current_rule.material_state_ref == created.material_state_ref
        assert current.current_rule.strength == "hard"
        assert current.current_rule.boundary_at == first_rule.boundary_at

        listed = await application.list_constraints_by_subject(
            self_person_ref=self_ref,
            subject_native_ref=activity_ref,
        )
        assert listed == [current]

        revised = await application.revise_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-a5:application-revise",
            constraint_ref=created.constraint_ref,
            expected_material_state_ref=created.material_state_ref,
            rule=revised_rule,
        )
        assert revised.replayed is False
        assert revised.previous_material_state_ref == created.material_state_ref
        assert revised.material_state_ref != created.material_state_ref

        revise_replay = await application.revise_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-a5:application-revise",
            constraint_ref=created.constraint_ref,
            expected_material_state_ref=created.material_state_ref,
            rule=revised_rule,
        )
        assert revise_replay.replayed is True
        assert revise_replay.material_state_ref == revised.material_state_ref
        assert revise_replay.recorded_at == revised.recorded_at

        with pytest.raises(TemporalConstraintOperationIdReuseError):
            await application.revise_constraint(
                self_person_ref=self_ref,
                operation_id="operation:b04-a5:application-revise",
                constraint_ref=created.constraint_ref,
                expected_material_state_ref=created.material_state_ref,
                rule=AbsoluteEarliestStartRule(
                    strength="hard",
                    boundary_at=revised_rule.boundary_at + timedelta(hours=1),
                ),
            )

        with pytest.raises(TemporalConstraintStateConflictError):
            await application.revise_constraint(
                self_person_ref=self_ref,
                operation_id="operation:b04-a5:stale-revise",
                constraint_ref=created.constraint_ref,
                expected_material_state_ref=created.material_state_ref,
                rule=revised_rule,
            )

        after_revision = await application.get_constraint(
            self_person_ref=self_ref,
            constraint_ref=created.constraint_ref,
        )
        assert after_revision.status == "active"
        assert after_revision.current_rule is not None
        assert after_revision.current_rule.material_state_ref == revised.material_state_ref
        assert after_revision.current_rule.strength == "soft"

        retired = await application.retire_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-a5:application-retire",
            constraint_ref=created.constraint_ref,
            expected_material_state_ref=revised.material_state_ref,
        )
        assert retired.replayed is False
        assert retired.previous_material_state_ref == revised.material_state_ref

        retire_replay = await application.retire_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-a5:application-retire",
            constraint_ref=created.constraint_ref,
            expected_material_state_ref=revised.material_state_ref,
        )
        assert retire_replay.replayed is True
        assert retire_replay.recorded_at == retired.recorded_at

        final = await application.get_constraint(
            self_person_ref=self_ref,
            constraint_ref=created.constraint_ref,
        )
        assert final.status == "retired"
        assert final.current_rule is None
        assert await application.list_constraints_by_subject(
            self_person_ref=self_ref,
            subject_native_ref=activity_ref,
        ) == [final]
    finally:
        await runtime.dispose()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_a5_application_rejects_cross_self_subject_reads(
    migrated_database: Any,
) -> None:
    owner_ref, activity_ref = _seed_activity(migrated_database)
    other_self_ref = NativeRef(uuid7())
    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator",
            migrated_database.cluster.migrator_password,
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (other_self_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'person')",
            (other_self_ref,),
        )
        connection.commit()

    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    try:
        created = await application.create_constraint(
            self_person_ref=owner_ref,
            operation_id="operation:b04-a5:owner-create",
            subject_native_ref=activity_ref,
            rule=AbsoluteEarliestStartRule(
                strength="hard",
                boundary_at=datetime(2026, 9, 25, 8, 0, tzinfo=UTC),
            ),
        )
        with pytest.raises(TemporalConstraintNotFoundError):
            await application.get_constraint(
                self_person_ref=other_self_ref,
                constraint_ref=created.constraint_ref,
            )
        with pytest.raises(TemporalConstraintNotFoundError):
            await application.list_constraints_by_subject(
                self_person_ref=other_self_ref,
                subject_native_ref=activity_ref,
            )
    finally:
        await runtime.dispose()
