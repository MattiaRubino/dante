"""Application proof for B04-C windows, preferences and deterministic evaluation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    AbsoluteIntervalPlacement,
    AbsoluteWindowRule,
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
        connection.execute("INSERT INTO dante.person(person_ref) VALUES (%s)", (self_person_ref,))
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
            INSERT INTO dante.event_expectation(event_ref,self_person_ref,title,created_at)
            VALUES (%s,%s,'B04-C Event',%s)
            """,
            (event_ref, self_person_ref, datetime.now(UTC)),
        )
        connection.commit()
    return self_person_ref, event_ref


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_c_application_composes_boundary_and_soft_window_evaluation(
    migrated_database: Any,
) -> None:
    self_ref, event_ref = _seed_event(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    earliest = AbsoluteBoundaryRule(
        boundary_kind="earliest_start",
        constrained_facet="schedule.start",
        strength="hard",
        boundary_at=datetime(2026, 10, 2, 10, 0, tzinfo=UTC),
    )
    preference = AbsoluteWindowRule(
        relationship="start_within",
        constrained_facet="schedule.start",
        strength="soft",
        starts_at=datetime(2026, 10, 2, 9, 0, tzinfo=UTC),
        ends_at=datetime(2026, 10, 2, 11, 0, tzinfo=UTC),
    )

    try:
        await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-c:evaluation-boundary",
            subject_native_ref=event_ref,
            rule=earliest,
        )
        window_created = await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-c:evaluation-window",
            subject_native_ref=event_ref,
            rule=preference,
        )

        current = await application.get_constraint(
            self_person_ref=self_ref,
            constraint_ref=window_created.constraint_ref,
        )
        assert current.current_rule is not None
        assert current.current_rule.family == "window"
        assert current.current_rule.constrained_facet == "schedule.start"

        inadmissible = await application.evaluate_constraints(
            self_person_ref=self_ref,
            subject_native_ref=event_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 2, 8, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 2, 9, 0, tzinfo=UTC),
            ),
        )
        assert inadmissible.status == "inadmissible"
        assert inadmissible.hard_set_status == "feasible"
        assert {item.evaluation for item in inadmissible.items} == {"violated"}

        admissible = await application.evaluate_constraints(
            self_person_ref=self_ref,
            subject_native_ref=event_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 2, 10, 30, tzinfo=UTC),
                ends_at=datetime(2026, 10, 2, 11, 0, tzinfo=UTC),
            ),
        )
        assert admissible.status == "admissible"
        assert admissible.hard_set_status == "feasible"
        assert {item.evaluation for item in admissible.items} == {"satisfied"}
    finally:
        await runtime.dispose()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_c_hard_set_reports_infeasible_without_creating_outcome(
    migrated_database: Any,
) -> None:
    self_ref, event_ref = _seed_event(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    try:
        await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-c:hard-earliest",
            subject_native_ref=event_ref,
            rule=AbsoluteBoundaryRule(
                boundary_kind="earliest_start",
                constrained_facet="schedule.start",
                strength="hard",
                boundary_at=datetime(2026, 10, 3, 15, 0, tzinfo=UTC),
            ),
        )
        await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-c:hard-deadline",
            subject_native_ref=event_ref,
            rule=AbsoluteBoundaryRule(
                boundary_kind="latest_completion",
                constrained_facet="schedule.completion",
                strength="hard",
                boundary_at=datetime(2026, 10, 3, 14, 0, tzinfo=UTC),
            ),
        )
        evaluated = await application.evaluate_constraints(
            self_person_ref=self_ref,
            subject_native_ref=event_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 3, 13, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 3, 13, 30, tzinfo=UTC),
            ),
        )
        assert evaluated.hard_set_status == "infeasible"
        assert evaluated.status == "inadmissible"
    finally:
        await runtime.dispose()


def test_b04_c_window_rule_rejects_relation_facet_mismatch_and_zero_interval() -> None:
    with pytest.raises(ValueError):
        AbsoluteWindowRule(
            relationship="start_within",
            constrained_facet="schedule.completion",
            strength="hard",
            starts_at=datetime(2026, 10, 2, 9, 0, tzinfo=UTC),
            ends_at=datetime(2026, 10, 2, 10, 0, tzinfo=UTC),
        )
    with pytest.raises(ValueError):
        AbsoluteWindowRule(
            relationship="placement_overlaps",
            constrained_facet="schedule.placement",
            strength="hard",
            starts_at=datetime(2026, 10, 2, 9, 0, tzinfo=UTC),
            ends_at=datetime(2026, 10, 2, 9, 0, tzinfo=UTC),
        )
