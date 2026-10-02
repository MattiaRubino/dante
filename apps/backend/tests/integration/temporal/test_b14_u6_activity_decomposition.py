"""Bounded Activity relation, replay and Schedule containment proof."""

from __future__ import annotations

import hashlib
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest
from tests.integration.temporal.test_b04_absolute_window_core import _mutate as _mutate_window
from tests.integration.temporal.test_b04_f_constrained_activity_application import (
    _seed_activity,
    _seed_person,
)

from dante.modules.temporal.schedule import (
    AbsoluteIntervalPlacement,
    DateSpanPlacement,
    SchedulePersistenceError,
    TemporalScheduleApplication,
)
from dante.platform.database.runtime import create_database_runtime

pytestmark = pytest.mark.postgres


def _mutate(
    database: Any,
    *,
    actor: UUID,
    operation: str,
    relation: UUID,
    parent: UUID,
    child: UUID,
    expected: UUID | None = None,
    active: bool = True,
    requirement: str = "required",
    order: int = 1,
) -> tuple[UUID, UUID, bool, bool]:
    fingerprint = hashlib.sha256(
        f"{relation}:{parent}:{child}:{active}:{requirement}:{order}:{expected}".encode()
    ).hexdigest()
    with psycopg.connect(
        **database.connection_kwargs("dante_runtime", database.cluster.runtime_password)
    ) as connection:
        row = connection.execute(
            """
            SELECT * FROM dante.set_self_activity_decomposition(
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            (
                actor,
                operation,
                fingerprint,
                relation,
                parent,
                child,
                uuid7(),
                active,
                requirement,
                order,
                expected,
            ),
        ).fetchone()
        assert row is not None
        return row


def _children(database: Any, actor: UUID, parent: UUID) -> list[tuple[Any, ...]]:
    with psycopg.connect(
        **database.connection_kwargs("dante_runtime", database.cluster.runtime_password)
    ) as connection:
        return connection.execute(
            "SELECT * FROM dante.get_self_activity_decomposition(%s,%s)", (actor, parent)
        ).fetchall()


def test_direct_relation_is_scoped_current_ordered_and_replayable(
    migrated_database: Any,
) -> None:
    actor = _seed_person(migrated_database)
    foreign = _seed_person(migrated_database)
    root = _seed_activity(migrated_database, self_ref=actor, title="Root")
    second_root = _seed_activity(migrated_database, self_ref=actor, title="Other root")
    first = _seed_activity(migrated_database, self_ref=actor, title="First")
    second = _seed_activity(migrated_database, self_ref=actor, title="Second")
    outsider = _seed_activity(migrated_database, self_ref=foreign, title="Outside")
    first_relation, second_relation = uuid7(), uuid7()

    attached = _mutate(
        migrated_database,
        actor=actor,
        operation="u6:attach:first",
        relation=first_relation,
        parent=root,
        child=first,
        order=2,
    )
    assert attached[0] == first_relation
    assert attached[2:] == (True, False)
    replay = _mutate(
        migrated_database,
        actor=actor,
        operation="u6:attach:first",
        relation=first_relation,
        parent=root,
        child=first,
        order=2,
    )
    assert replay[1] == attached[1]
    assert replay[3] is True
    _mutate(
        migrated_database,
        actor=actor,
        operation="u6:attach:second",
        relation=second_relation,
        parent=root,
        child=second,
        requirement="optional",
    )
    assert [row[2] for row in _children(migrated_database, actor, root)] == [second, first]
    assert _children(migrated_database, foreign, root) == []

    revised = _mutate(
        migrated_database,
        actor=actor,
        operation="u6:reorder:first",
        relation=first_relation,
        parent=root,
        child=first,
        expected=attached[1],
        order=1,
    )
    assert revised[1] != attached[1]
    with pytest.raises(psycopg.errors.SerializationFailure):
        _mutate(
            migrated_database,
            actor=actor,
            operation="u6:stale:first",
            relation=first_relation,
            parent=root,
            child=first,
            expected=attached[1],
            order=3,
        )
    for operation, kwargs in (
        ("duplicate", {"relation": uuid7(), "parent": root, "child": first}),
        ("second-parent", {"relation": uuid7(), "parent": second_root, "child": first}),
        ("grandchild", {"relation": uuid7(), "parent": first, "child": second_root}),
        ("self", {"relation": uuid7(), "parent": root, "child": root}),
        ("foreign", {"relation": uuid7(), "parent": root, "child": outsider}),
    ):
        with pytest.raises((psycopg.errors.CheckViolation, psycopg.errors.ForeignKeyViolation)):
            _mutate(migrated_database, actor=actor, operation=f"u6:{operation}", **kwargs)

    detached = _mutate(
        migrated_database,
        actor=actor,
        operation="u6:detach:first",
        relation=first_relation,
        parent=root,
        child=first,
        expected=revised[1],
        active=False,
    )
    assert detached[2] is False
    assert [row[2] for row in _children(migrated_database, actor, root)] == [second]
    with psycopg.connect(
        **migrated_database.connection_kwargs(
            "dante_migrator", migrated_database.cluster.migrator_password
        )
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        assert connection.execute(
            "SELECT count(*) FROM dante.activity_intention WHERE activity_ref IN (%s,%s)",
            (root, first),
        ).fetchone() == (2,)
        assert connection.execute(
            "SELECT count(*) FROM dante.activity_decomposition_current_history "
            "WHERE decomposition_ref=%s",
            (first_relation,),
        ).fetchone() == (3,)


@pytest.mark.asyncio
async def test_child_placement_and_parent_revision_preserve_exact_containment(
    migrated_database: Any,
) -> None:
    actor = _seed_person(migrated_database)
    parent = _seed_activity(migrated_database, self_ref=actor, title="Parent")
    child = _seed_activity(migrated_database, self_ref=actor, title="Child")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    schedules = TemporalScheduleApplication(runtime.session_factory)
    try:
        parent_schedule = await schedules.establish_schedule(
            self_person_ref=actor,
            operation_id="u6:parent:plan",
            subject_native_ref=parent,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 20, 8, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 12, tzinfo=UTC),
            ),
        )
        relation = uuid7()
        attached = _mutate(
            migrated_database,
            actor=actor,
            operation="u6:relation:plan",
            relation=relation,
            parent=parent,
            child=child,
        )
        child_schedule = await schedules.establish_schedule(
            self_person_ref=actor,
            operation_id="u6:child:inside",
            subject_native_ref=child,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 20, 8, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 12, tzinfo=UTC),
            ),
        )
        assert attached[2]
        assert child_schedule.subject_native_ref == child
        with pytest.raises(SchedulePersistenceError):
            await schedules.revise_schedule(
                self_person_ref=actor,
                operation_id="u6:parent:too-narrow",
                schedule_ref=parent_schedule.schedule_ref,
                expected_material_state_ref=parent_schedule.material_state_ref,
                placement=AbsoluteIntervalPlacement(
                    starts_at=datetime(2026, 10, 20, 9, tzinfo=UTC),
                    ends_at=datetime(2026, 10, 20, 11, tzinfo=UTC),
                ),
            )
        with pytest.raises(SchedulePersistenceError):
            await schedules.establish_schedule(
                self_person_ref=actor,
                operation_id="u6:child:outside",
                subject_native_ref=child,
                placement=AbsoluteIntervalPlacement(
                    starts_at=datetime(2026, 10, 20, 7, tzinfo=UTC),
                    ends_at=datetime(2026, 10, 20, 8, tzinfo=UTC),
                ),
            )
        assert _children(migrated_database, actor, parent)[0][2] == child
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_all_day_child_date_span_must_fit_parent(
    migrated_database: Any,
) -> None:
    actor = _seed_person(migrated_database)
    parent = _seed_activity(migrated_database, self_ref=actor, title="All day parent")
    child = _seed_activity(migrated_database, self_ref=actor, title="All day child")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    schedules = TemporalScheduleApplication(runtime.session_factory)
    try:
        await schedules.establish_schedule(
            self_person_ref=actor,
            operation_id="u6:parent:date",
            subject_native_ref=parent,
            placement=DateSpanPlacement(date(2026, 10, 20), date(2026, 10, 23)),
        )
        _mutate(
            migrated_database,
            actor=actor,
            operation="u6:date:attach",
            relation=uuid7(),
            parent=parent,
            child=child,
        )
        await schedules.establish_schedule(
            self_person_ref=actor,
            operation_id="u6:child:date:inside",
            subject_native_ref=child,
            placement=DateSpanPlacement(date(2026, 10, 20), date(2026, 10, 23)),
        )
        with pytest.raises(SchedulePersistenceError):
            await schedules.establish_schedule(
                self_person_ref=actor,
                operation_id="u6:child:date:outside",
                subject_native_ref=child,
                placement=DateSpanPlacement(date(2026, 10, 19), date(2026, 10, 20)),
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_unplaced_parent_requires_a_finite_hard_containment_window(
    migrated_database: Any,
) -> None:
    actor = _seed_person(migrated_database)
    parent = _seed_activity(migrated_database, self_ref=actor, title="Window parent")
    child = _seed_activity(migrated_database, self_ref=actor, title="Window child")
    _mutate(
        migrated_database,
        actor=actor,
        operation="u6:window:attach",
        relation=uuid7(),
        parent=parent,
        child=child,
    )
    runtime = create_database_runtime(migrated_database.runtime_settings())
    schedules = TemporalScheduleApplication(runtime.session_factory)
    try:
        with pytest.raises(SchedulePersistenceError):
            await schedules.establish_schedule(
                self_person_ref=actor,
                operation_id="u6:window:missing",
                subject_native_ref=child,
                placement=AbsoluteIntervalPlacement(
                    starts_at=datetime(2026, 10, 20, 9, tzinfo=UTC),
                    ends_at=datetime(2026, 10, 20, 10, tzinfo=UTC),
                ),
            )
        window_ref = uuid7()
        window_state = uuid7()
        _mutate_window(
            migrated_database,
            self_person_ref=actor,
            operation_id="u6:parent:hard-window",
            fingerprint="a" * 64,
            mutation_kind="create",
            subject_native_ref=parent,
            constraint_ref=window_ref,
            expected_material_state_ref=None,
            resulting_material_state_ref=window_state,
            relationship_code="full_placement_contained",
            constrained_facet_code="schedule.placement",
            strength_code="hard",
            starts_at=datetime(2026, 10, 20, 8, tzinfo=UTC),
            ends_at=datetime(2026, 10, 20, 12, tzinfo=UTC),
        )
        admitted = await schedules.establish_schedule(
            self_person_ref=actor,
            operation_id="u6:window:inside",
            subject_native_ref=child,
            placement=AbsoluteIntervalPlacement(
                starts_at=datetime(2026, 10, 20, 9, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 10, tzinfo=UTC),
            ),
        )
        assert admitted.subject_native_ref == child
        with pytest.raises(psycopg.errors.CheckViolation):
            _mutate_window(
                migrated_database,
                self_person_ref=actor,
                operation_id="u6:parent:narrow-window",
                fingerprint="b" * 64,
                mutation_kind="revise",
                subject_native_ref=parent,
                constraint_ref=window_ref,
                expected_material_state_ref=window_state,
                resulting_material_state_ref=uuid7(),
                relationship_code="full_placement_contained",
                constrained_facet_code="schedule.placement",
                strength_code="hard",
                starts_at=datetime(2026, 10, 20, 10, tzinfo=UTC),
                ends_at=datetime(2026, 10, 20, 12, tzinfo=UTC),
            )
        with pytest.raises(SchedulePersistenceError):
            await schedules.establish_schedule(
                self_person_ref=actor,
                operation_id="u6:window:outside",
                subject_native_ref=child,
                placement=AbsoluteIntervalPlacement(
                    starts_at=datetime(2026, 10, 20, 13, tzinfo=UTC),
                    ends_at=datetime(2026, 10, 20, 14, tzinfo=UTC),
                ),
            )
    finally:
        await runtime.dispose()
