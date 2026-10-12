"""Application proof for B04-E planned Schedule duration evaluation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid7

import psycopg
import pytest

from dante.modules.temporal.temporal_constraint import (
    AbsoluteIntervalPlacement,
    AbsoluteWindowRule,
    ScheduleDurationRule,
    TemporalConstraintApplication,
)
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime


def _seed_event(database: Any, *, suffix: str) -> tuple[NativeRef, NativeRef]:
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
            VALUES (%s,%s,%s,%s)
            """,
            (event_ref, self_person_ref, f"B04-E duration {suffix}", datetime.now(UTC)),
        )
        connection.commit()
    return self_person_ref, event_ref


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_e_soft_duration_violation_is_admissible_with_explanation(
    migrated_database: Any,
) -> None:
    self_ref, event_ref = _seed_event(migrated_database, suffix="soft")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    try:
        created = await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-e:soft-duration",
            subject_native_ref=event_ref,
            rule=ScheduleDurationRule(
                duration_kind="maximum",
                strength="soft",
                duration_microseconds=30 * 60 * 1_000_000,
            ),
        )
        current = await application.get_constraint(
            self_person_ref=self_ref,
            constraint_ref=created.constraint_ref,
        )
        assert current.current_rule is not None
        assert current.current_rule.family == "duration"
        assert current.current_rule.duration_kind == "maximum"
        assert current.current_rule.duration_microseconds == 30 * 60 * 1_000_000

        evaluated = await application.evaluate_constraints(
            self_person_ref=self_ref,
            subject_native_ref=event_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 5, 10, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 5, 11, 0, tzinfo=UTC),
            ),
        )
        assert evaluated.status == "admissible_with_soft_violations"
        assert evaluated.hard_set_status == "feasible"
        assert len(evaluated.items) == 1
        assert evaluated.items[0].family == "duration"
        assert evaluated.items[0].rule_code == "maximum"
        assert evaluated.items[0].evaluation == "violated"
        assert evaluated.items[0].reason_code == "schedule_duration_above_maximum"
    finally:
        await runtime.dispose()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_e_hard_maximum_duration_rejects_candidate(
    migrated_database: Any,
) -> None:
    self_ref, event_ref = _seed_event(migrated_database, suffix="hard-max")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    try:
        await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-e:hard-max-duration",
            subject_native_ref=event_ref,
            rule=ScheduleDurationRule(
                duration_kind="maximum",
                strength="hard",
                duration_microseconds=60 * 60 * 1_000_000,
            ),
        )
        evaluated = await application.evaluate_constraints(
            self_person_ref=self_ref,
            subject_native_ref=event_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 5, 10, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 5, 12, 0, tzinfo=UTC),
            ),
        )
        assert evaluated.status == "inadmissible"
        assert evaluated.hard_set_status == "feasible"
        assert evaluated.items[0].evaluation == "violated"
        assert evaluated.items[0].reason_code == "schedule_duration_above_maximum"
    finally:
        await runtime.dispose()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_b04_e_hard_set_detects_window_duration_infeasibility(
    migrated_database: Any,
) -> None:
    self_ref, event_ref = _seed_event(migrated_database, suffix="infeasible")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    application = TemporalConstraintApplication(runtime.session_factory)
    try:
        await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-e:contained-window",
            subject_native_ref=event_ref,
            rule=AbsoluteWindowRule(
                relationship="full_placement_contained",
                constrained_facet="schedule.placement",
                strength="hard",
                starts_at=datetime(2026, 10, 6, 10, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 6, 10, 30, tzinfo=UTC),
            ),
        )
        await application.create_constraint(
            self_person_ref=self_ref,
            operation_id="operation:b04-e:min-duration-infeasible",
            subject_native_ref=event_ref,
            rule=ScheduleDurationRule(
                duration_kind="minimum",
                strength="hard",
                duration_microseconds=60 * 60 * 1_000_000,
            ),
        )
        evaluated = await application.evaluate_constraints(
            self_person_ref=self_ref,
            subject_native_ref=event_ref,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 6, 10, 0, tzinfo=UTC),
                ends_at=datetime(2026, 10, 6, 10, 30, tzinfo=UTC),
            ),
        )
        assert evaluated.hard_set_status == "infeasible"
        assert evaluated.status == "inadmissible"
        by_family = {item.family: item for item in evaluated.items}
        assert by_family["window"].evaluation == "satisfied"
        assert by_family["duration"].evaluation == "violated"
    finally:
        await runtime.dispose()


def test_b04_e_duration_rule_rejects_non_positive_value() -> None:
    with pytest.raises(ValueError):
        ScheduleDurationRule(
            duration_kind="minimum",
            strength="hard",
            duration_microseconds=0,
        )
