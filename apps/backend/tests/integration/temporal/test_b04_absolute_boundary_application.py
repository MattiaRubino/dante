"""Application proof for B04-B typed absolute boundary rules."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    TemporalConstraintApplication,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime


def _seed_event(database: Any) -> tuple[NativeRef, NativeRef]:
    self_person_ref = NativeRef(uuid7())
    event_ref = NativeRef(uuid7())
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
        connection.execute("INSERT INTO dante.event(event_ref) VALUES (%s)", (event_ref,))
        connection.execute(
            "INSERT INTO dante.native_address(native_ref,owner_family) VALUES (%s,'event')",
            (event_ref,),
        )
        connection.execute(
            """
            INSERT INTO dante.event_expectation(
                event_ref,self_person_ref,title,created_at
            ) VALUES (%s,%s,'B04-B Event',%s)
            """,
            (event_ref, self_person_ref, datetime.now(UTC)),
        )
        connection.commit()
    return self_person_ref, event_ref


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_b_application_reads_and_revises_latest_bound_rule_kinds(
    migrated_database: Any,
) -> None:
    self_ref, event_ref = _seed_event(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    latest_start = AbsoluteBoundaryRule(
        boundary_kind="latest_start",
        constrained_facet="schedule.start",
        strength="hard",
        boundary_at=datetime(2026, 9, 26, 9, 0, tzinfo=UTC),
    )
    deadline = AbsoluteBoundaryRule(
        boundary_kind="latest_completion",
        constrained_facet="schedule.completion",
        strength="soft",
        boundary_at=datetime(2026, 9, 26, 17, 0, tzinfo=UTC),
    )

    try:
        created = await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-b:application-latest-start",
            subject_native_ref=event_ref,
            rule=latest_start,
        )
        assert created.rule == latest_start

        current = await application.get_constraint(
            self_person_ref=self_ref,
            constraint_ref=created.constraint_ref,
        )
        assert current.current_rule is not None
        assert current.current_rule.boundary_kind == "latest_start"
        assert current.current_rule.constrained_facet == "schedule.start"
        assert current.current_rule.boundary_at == latest_start.boundary_at

        revised = await application.revise_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-b:application-deadline",
            constraint_ref=created.constraint_ref,
            expected_material_state_ref=created.material_state_ref,
            rule=deadline,
        )
        assert revised.rule == deadline

        after_revision = await application.get_constraint(
            self_person_ref=self_ref,
            constraint_ref=created.constraint_ref,
        )
        assert after_revision.current_rule is not None
        assert after_revision.current_rule.boundary_kind == "latest_completion"
        assert after_revision.current_rule.constrained_facet == "schedule.completion"
        assert after_revision.current_rule.strength == "soft"
        assert after_revision.current_rule.boundary_at == deadline.boundary_at
    finally:
        await runtime.dispose()


def test_b04_b_application_rule_rejects_noncanonical_kind_facet_pair() -> None:
    with pytest.raises(ValueError):
        AbsoluteBoundaryRule(
            boundary_kind="latest_start",
            constrained_facet="schedule.completion",
            strength="hard",
            boundary_at=datetime(2026, 9, 26, 9, 0, tzinfo=UTC),
        )
