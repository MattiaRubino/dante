"""PostgreSQL integration: irreversible Event and recurring Activity deletion scopes."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast
from uuid import UUID
from zoneinfo import ZoneInfo

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_primary_life_area_assignment import _seed_self
from tests.integration.temporal.test_recurring_event_create import _daily_named_zone

from dante.context.contracts import DanteContext
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.event_occurrence_policy import EventOccurrencePolicyApplication
from dante.modules.temporal.execution_policy_api import (
    ExecutionPolicyCommand,
    set_execution_policy,
)
from dante.modules.temporal.reality_objective_api import (
    ObjectiveCreateCommand,
    RealityPolicyCommand,
    TemporalHardDeleteCommand,
    TemporalHardDeleteScope,
    apply_temporal_hard_deletion,
    create_activity_objective,
    list_event_deletion_occurrences,
    preview_temporal_hard_deletion,
    set_activity_reality_policy,
    set_event_reality_policy,
    set_occurrence_reality_policy,
)
from dante.modules.temporal.recurring_authoring import RecurringAuthoringApplication
from dante.modules.temporal.recurring_conversion import (
    ExistingEventBasis,
    RecurringConversionApplication,
)
from dante.modules.temporal.routine_occurrence_materialization import (
    RoutineOccurrenceMaterializationApplication,
)
from dante.modules.temporal.routine_occurrence_policy import RoutineOccurrencePolicyApplication
from dante.modules.temporal.schedule import NamedZoneLocalIntervalPlacement
from dante.modules.temporal.session_runtime import SessionApplication
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres


def _request(runtime: Any) -> Request:
    return cast(
        Request,
        SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))),
    )


def _context(actor: Any) -> DanteContext:
    return cast(DanteContext, SimpleNamespace(self_person_ref=actor))


async def _preview(runtime: Any, actor: Any, ref: Any, scope: TemporalHardDeleteScope) -> str:
    result = await preview_temporal_hard_deletion(
        ref, scope, _context(actor), _request(runtime), Response()
    )
    assert result.scope == scope
    assert len(result.fingerprint) == 64
    return result.fingerprint


async def _delete(
    runtime: Any, actor: Any, ref: Any, scope: TemporalHardDeleteScope, fingerprint: str
) -> int:
    result = await apply_temporal_hard_deletion(
        ref,
        TemporalHardDeleteCommand(scope=scope, expected_fingerprint=fingerprint),
        _context(actor),
        _request(runtime),
        Response(),
    )
    assert result.requested_ref == ref
    assert result.deleted_rows > 0
    return result.deleted_rows


def _owner_sql(database: Any, sql_text: str, args: tuple[Any, ...]) -> list[tuple[Any, ...]]:
    # Introspection is exclusively for the test owner role, never runtime DML.
    with psycopg.connect(
        **database.connection_kwargs("dante_migrator", database.cluster.migrator_password)
    ) as connection:
        connection.execute("SET ROLE dante_owner")
        return list(connection.execute(sql_text, args).fetchall())


def _occurrences(database: Any, source: Any) -> list[Any]:
    return [
        row[0]
        for row in _owner_sql(
            database,
            "SELECT occurrence_ref FROM dante.occurrence_generation "
            "WHERE source_native_ref=%s ORDER BY occurrence_ref",
            (source,),
        )
    ]


def _exists(database: Any, sql_text: str, ref: Any) -> bool:
    return bool(_owner_sql(database, sql_text, (ref,))[0][0])


async def _activity_for(runtime: Any, actor: Any, occurrence: Any) -> Any:
    async with runtime.session_factory() as session, session.begin():
        return await session.scalar(
            text(
                "SELECT activity_ref FROM dante.list_self_routine_occurrence_activities("
                ":actor,CAST(ARRAY[:occurrence] AS uuid[]))"
            ),
            {"actor": actor, "occurrence": occurrence},
        )


@pytest.mark.asyncio
async def test_recurring_activity_instance_skip_and_whole_series_no_regeneration(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        routine = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="hard:activity:routine",
            title="Ricorrenza da eliminare",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=45,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "planned_slices": [{"name": "Fase", "time_enabled": False}],
            },
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:activity:window",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        occurrences = _occurrences(migrated_database, routine.source_ref)
        assert len(occurrences) == 2
        first, second = occurrences
        first_activity = await _activity_for(runtime, actor, first)
        second_activity = await _activity_for(runtime, actor, second)
        assert first_activity is not None
        assert second_activity is not None
        await set_activity_reality_policy(
            first_activity,
            RealityPolicyCommand(operation_id="hard:activity:policy", mode_code="review_on_end"),
            _context(actor),
            _request(runtime),
            Response(),
        )
        await set_activity_reality_policy(
            second_activity,
            RealityPolicyCommand(
                operation_id="hard:activity:sibling-policy", mode_code="review_on_end"
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )

        with pytest.raises(ProblemError) as foreign:
            await _preview(runtime, stranger, first_activity, "activity_instance")
        assert foreign.value.status == 404

        fingerprint = await _preview(runtime, actor, first_activity, "activity_instance")
        await create_activity_objective(
            first_activity,
            ObjectiveCreateCommand(
                operation_id="hard:activity:stale-objective",
                label="Obiettivo aggiunto dopo anteprima",
                result_kind="boolean",
                presentation_order=0,
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        with pytest.raises(ProblemError) as stale:
            await _delete(runtime, actor, first_activity, "activity_instance", fingerprint)
        assert stale.value.status == 409
        assert await _activity_for(runtime, actor, first) == first_activity
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )

        fingerprint = await _preview(runtime, actor, first_activity, "activity_instance")
        await _delete(runtime, actor, first_activity, "activity_instance", fingerprint)
        assert await _activity_for(runtime, actor, first) is None
        assert await _activity_for(runtime, actor, second) == second_activity
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.reality_review_policy "
            "WHERE subject_kind='activity' AND subject_native_ref=%s)",
            first_activity,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.reality_review_policy "
            "WHERE subject_kind='activity' AND subject_native_ref=%s)",
            second_activity,
        )

        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.routine_intention WHERE routine_ref=%s)",
            routine.source_ref,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:activity:replay",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        assert await _activity_for(runtime, actor, first) is None

        series = await _preview(runtime, actor, second_activity, "activity_series")
        await _delete(runtime, actor, second_activity, "activity_series", series)
        assert _occurrences(migrated_database, routine.source_ref) == []
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.reality_review_policy "
            "WHERE subject_kind='activity' AND subject_native_ref=%s)",
            second_activity,
        )
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            assert connection.execute(
                "SELECT count(*) FROM dante.routine WHERE routine_ref=%s",
                (routine.source_ref,),
            ).fetchone() == (0,)
            assert connection.execute(
                "SELECT count(*) FROM dante.activity WHERE activity_ref IN (%s,%s)",
                (first_activity, second_activity),
            ).fetchone() == (0,)
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_confirmed_recurring_instance_deletion_removes_open_session_atomically(
    migrated_database: Any,
) -> None:
    """Explicitly confirmed deletion removes an active Session and its one instance."""
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    sessions = SessionApplication(runtime.session_factory)
    try:
        routine = await RecurringAuthoringApplication(runtime.session_factory).create_routine(
            self_person_ref=actor,
            operation_id="hard:active-session:routine",
            title="Confirmed deletion removes active Session",
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await RoutineOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            routine_ref=routine.source_ref,
            duration_minutes=30,
            reminder_lead_minutes=None,
            activity_template={
                "version": 1,
                "planned_slices": [{"name": "Fase", "time_enabled": False}],
            },
        )
        target_day = datetime.now(ZoneInfo("Europe/Rome")).date()
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:active-session:initial",
            start_date=target_day,
            end_date_exclusive=target_day + timedelta(days=2),
            effective_zone_id="Europe/Rome",
        )
        instances = _occurrences(migrated_database, routine.source_ref)
        assert len(instances) == 2
        occurrence, sibling_occurrence = instances
        activity = await _activity_for(runtime, actor, occurrence)
        assert activity is not None
        sibling_activity = await _activity_for(runtime, actor, sibling_occurrence)
        assert sibling_activity is not None
        assert sibling_activity != activity

        # Materialization may already seed an Activity execution policy.
        # Treat the canonical state as a CAS precondition; the generic
        # enable_live_capture() fixture assumes a brand-new Activity and
        # incorrectly passes a null expected state for an inherited policy.
        async with runtime.session_factory() as session, session.begin():
            current_policy = (
                (
                    await session.execute(
                        text(
                            "SELECT state_ref, mode_code "
                            "FROM dante.get_self_activity_execution_policy(:actor,:activity)"
                        ),
                        {"actor": actor, "activity": activity},
                    )
                )
                .mappings()
                .one()
            )
        if current_policy["mode_code"] not in {"live", "record_and_live"}:
            await set_execution_policy(
                activity,
                ExecutionPolicyCommand(
                    operation_id="hard:active-session:enable",
                    mode_code="live",
                    expected_state_ref=current_policy["state_ref"],
                ),
                _context(actor),
                _request(runtime),
                Response(),
            )
        started = await sessions.start(
            self_person_ref=actor,
            operation_id="hard:active-session:start",
            subject_kind="activity",
            subject_native_ref=activity,
        )
        assert started.open

        # Preview is read-only. Until the person explicitly confirms, both
        # the Activity and its running Session must be untouched.
        fingerprint = await _preview(runtime, actor, activity, "activity_instance")
        assert await _activity_for(runtime, actor, occurrence) == activity
        running = await sessions.get(
            self_person_ref=actor, session_ref=started.session_ref
        )
        assert running.open
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            occurrence,
        )

        # The confirmed destructive action is allowed while the Session is
        # still running. The same DB transaction must remove its entire owned
        # graph, retain the technical Occurrence skip, and leave siblings alone.
        await _delete(runtime, actor, activity, "activity_instance", fingerprint)
        assert await _activity_for(runtime, actor, occurrence) is None
        assert await _activity_for(runtime, actor, sibling_occurrence) == sibling_activity
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            occurrence,
        )
        for table, column in (
            ("dante.session", "session_ref"),
            ("dante.session_execution_subject", "session_ref"),
            ("dante.session_timing_current_history", "session_ref"),
            ("dante.native_address", "native_ref"),
        ):
            assert not _exists(
                migrated_database,
                f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {column}=%s)",
                started.session_ref,
            )
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.activity_intention WHERE activity_ref=%s)",
            activity,
        )

        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:active-session:recheckpoint",
            start_date=target_day,
            end_date_exclusive=target_day + timedelta(days=2),
            effective_zone_id="Europe/Rome",
        )
        assert await _activity_for(runtime, actor, occurrence) is None
        assert await _activity_for(runtime, actor, sibling_occurrence) == sibling_activity
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            occurrence,
        )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_recurring_event_single_occurrence_then_full_series(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    materializer = RoutineOccurrenceMaterializationApplication(runtime.session_factory)
    try:
        created = await RecurringAuthoringApplication(runtime.session_factory).create_event(
            self_person_ref=actor,
            operation_id="hard:event:create",
            title="Eventi ricorrenti",
            agenda_parts=("Agenda",),
            life_area_intent=None,
            recurrence=_daily_named_zone(),
        )
        await EventOccurrencePolicyApplication(runtime.session_factory).set(
            self_person_ref=actor,
            event_ref=created.source_ref,
            placement_kind="timed",
            duration_minutes=40,
            duration_days=None,
            reminder_lead_minutes=10,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:event:checkpoint",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        first, second = _occurrences(migrated_database, created.source_ref)
        await set_occurrence_reality_policy(
            first,
            RealityPolicyCommand(operation_id="hard:event:first-policy", mode_code="review_on_end"),
            _context(actor),
            _request(runtime),
            Response(),
        )
        await set_occurrence_reality_policy(
            second,
            RealityPolicyCommand(
                operation_id="hard:event:second-policy", mode_code="review_on_end"
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        await set_event_reality_policy(
            created.source_ref,
            RealityPolicyCommand(
                operation_id="hard:event:source-policy", mode_code="review_on_end"
            ),
            _context(actor),
            _request(runtime),
            Response(),
        )
        selectable = await list_event_deletion_occurrences(
            created.source_ref, _context(actor), _request(runtime), Response()
        )
        assert {row.occurrence_ref for row in selectable} == {first, second}
        assert all(row.schedule_ref is not None for row in selectable)
        fingerprint = await _preview(runtime, actor, first, "event_instance")
        await _delete(runtime, actor, first, "event_instance", fingerprint)
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )
        selectable = await list_event_deletion_occurrences(
            created.source_ref, _context(actor), _request(runtime), Response()
        )
        assert {row.occurrence_ref for row in selectable} == {second}
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.schedule WHERE subject_native_ref=%s)",
            first,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.schedule WHERE subject_native_ref=%s)",
            second,
        )
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.reality_review_policy "
            "WHERE subject_kind='occurrence' AND subject_native_ref=%s)",
            first,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.reality_review_policy "
            "WHERE subject_kind='occurrence' AND subject_native_ref=%s)",
            second,
        )
        await materializer.checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:event:after-single",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.schedule WHERE subject_native_ref=%s)",
            first,
        )

        series = await _preview(runtime, actor, second, "event_series")
        await _delete(runtime, actor, second, "event_series", series)
        assert _occurrences(migrated_database, created.source_ref) == []
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            created.source_ref,
        )
        for removed_ref in (created.source_ref, second):
            assert not _exists(
                migrated_database,
                "SELECT EXISTS(SELECT 1 FROM dante.reality_review_policy "
                "WHERE subject_native_ref=%s)",
                removed_ref,
            )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_single_event_delete_keeps_unrelated_actors(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        authoring = TemporalAuthoringApplication(runtime.session_factory)
        selected = await authoring.create_event(
            self_person_ref=actor,
            operation_id="hard:oneoff:owner",
            title="Evento singolo",
        )
        retained = await authoring.create_event(
            self_person_ref=stranger,
            operation_id="hard:oneoff:other",
            title="Evento estraneo",
        )
        ref = selected.item.subject_native_ref
        impact = await _preview(runtime, actor, ref, "event_once")
        await set_event_reality_policy(
            ref,
            RealityPolicyCommand(operation_id="hard:oneoff:policy", mode_code="review_on_end"),
            _context(actor),
            _request(runtime),
            Response(),
        )
        with pytest.raises(ProblemError) as stale:
            await _delete(runtime, actor, ref, "event_once", impact)
        assert stale.value.status == 409
        assert _exists(
            migrated_database, "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)", ref
        )
        impact = await _preview(runtime, actor, ref, "event_once")
        await _delete(runtime, actor, ref, "event_once", impact)
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            ref,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            retained.item.subject_native_ref,
        )
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.reality_review_policy "
            "WHERE subject_kind='event' AND subject_native_ref=%s)",
            ref,
        )
    finally:
        await runtime.dispose()


async def _linked_existing_event(
    runtime: Any, actor: UUID, operation_id: str
) -> tuple[UUID, UUID, UUID]:
    """Author a physical first Event and link it to a canonical recurring source."""
    owner = NativeRef(actor)
    created = await TemporalAuthoringApplication(runtime.session_factory).create_event(
        self_person_ref=owner,
        operation_id=f"{operation_id}:original",
        title="Visita iniziale",
        agenda_parts=("Accoglienza",),
        placement=NamedZoneLocalIntervalPlacement(
            starts_local_at=datetime(2026, 10, 6, 10),  # noqa: DTZ001
            ends_local_at=datetime(2026, 10, 6, 11),  # noqa: DTZ001
            zone_id="Europe/Rome",
            disambiguation="earlier",
        ),
    )
    original = created.item.subject_native_ref
    assert created.schedule is not None
    async with runtime.session_factory() as session, session.begin():
        revision = await session.scalar(
            text("SELECT dante.get_self_event_profile_revision(:actor,:event)"),
            {"actor": actor, "event": original},
        )
    started = await RecurringConversionApplication(runtime.session_factory).event(
        self_person_ref=owner,
        operation_id=f"{operation_id}:repeat",
        basis=ExistingEventBasis(
            event_ref=original,
            expected_profile_revision=revision,
            schedule_ref=created.schedule.schedule_ref,
            expected_placement_state_ref=created.schedule.material_state_ref,
        ),
        recurrence=_daily_named_zone(),
    )
    await RoutineOccurrenceMaterializationApplication(runtime.session_factory).checkpoint_window(
        self_person_ref=owner,
        operation_id=f"{operation_id}:checkpoint",
        start_date=date(2026, 10, 6),
        end_date_exclusive=date(2026, 10, 8),
        effective_zone_id="Europe/Rome",
    )
    async with runtime.session_factory() as session, session.begin():
        first = await session.scalar(
            text(
                "SELECT first_occurrence_ref "
                "FROM dante.get_self_event_recurring_first_by_source(:actor,:source)"
            ),
            {"actor": actor, "source": started.source_ref},
        )
        assert first is not None
    return original, started.source_ref, first


@pytest.mark.asyncio
@pytest.mark.parametrize("scope", ["event_once", "event_instance"])
async def test_existing_first_event_single_delete_keeps_future_siblings(
    migrated_database: Any, scope: TemporalHardDeleteScope
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        original, source, first = await _linked_existing_event(
            runtime, actor, f"hard:first:{scope}"
        )
        siblings = set(_occurrences(migrated_database, source)) - {first}
        assert len(siblings) == 1
        choices = await list_event_deletion_occurrences(
            source, _context(actor), _request(runtime), Response()
        )
        selected = next(item for item in choices if item.occurrence_ref == first)
        assert selected.schedule_ref is not None
        assert "2026-10-06" in selected.display_label

        target = original if scope == "event_once" else first
        with pytest.raises(ProblemError) as unauthorized:
            await _preview(runtime, stranger, target, scope)
        assert unauthorized.value.status == 404

        fingerprint = await _preview(runtime, actor, target, scope)
        await _delete(runtime, actor, target, scope, fingerprint)
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            original,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            source,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )
        assert set(_occurrences(migrated_database, source)) == siblings | {first}
        for remaining in siblings:
            assert _exists(
                migrated_database,
                "SELECT EXISTS(SELECT 1 FROM dante.schedule WHERE subject_native_ref=%s)",
                remaining,
            )
        await RoutineOccurrenceMaterializationApplication(
            runtime.session_factory
        ).checkpoint_window(
            self_person_ref=actor,
            operation_id=f"hard:first:{scope}:repeat-checkpoint",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )
        selectable = await list_event_deletion_occurrences(
            source, _context(actor), _request(runtime), Response()
        )
        assert {item.occurrence_ref for item in selectable} == siblings
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_existing_first_event_series_deletes_both_roots_and_all_occurrences(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        original, source, first = await _linked_existing_event(runtime, actor, "hard:first:whole")
        all_occurrences = set(_occurrences(migrated_database, source))
        assert first in all_occurrences
        assert len(all_occurrences) == 2
        with pytest.raises(ProblemError) as unauthorized:
            await _preview(runtime, stranger, original, "event_series")
        assert unauthorized.value.status == 404
        from_original = await _preview(runtime, actor, original, "event_series")
        from_source = await _preview(runtime, actor, source, "event_series")
        assert from_original != from_source
        await _delete(runtime, actor, original, "event_series", from_original)
        for native in (original, source):
            assert not _exists(
                migrated_database,
                "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
                native,
            )
        assert _occurrences(migrated_database, source) == []
        await RoutineOccurrenceMaterializationApplication(
            runtime.session_factory
        ).checkpoint_window(
            self_person_ref=actor,
            operation_id="hard:first:whole:repeat-checkpoint",
            start_date=date(2026, 10, 6),
            end_date_exclusive=date(2026, 10, 8),
            effective_zone_id="Europe/Rome",
        )
        assert _occurrences(migrated_database, source) == []
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("change_kind", ["profile", "reality_policy"])
async def test_existing_first_event_series_rejects_stale_native_state(
    migrated_database: Any, change_kind: str
) -> None:
    actor = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        original, source, first = await _linked_existing_event(runtime, actor, "hard:first:stale")
        stale = await _preview(runtime, actor, source, "event_series")
        if change_kind == "profile":
            async with runtime.session_factory() as session, session.begin():
                revision = await session.scalar(
                    text("SELECT dante.get_self_event_profile_revision(:actor,:event)"),
                    {"actor": actor, "event": original},
                )
                await session.execute(
                    text(
                        "SELECT * FROM dante.revise_self_event_profile("
                        ":actor,:event,:operation,:expected,:title,:description,:location,:color)"
                    ),
                    {
                        "actor": actor,
                        "event": original,
                        "operation": "hard:first:stale:revise",
                        "expected": revision,
                        "title": "Visita cambiata",
                        "description": None,
                        "location": None,
                        "color": None,
                    },
                )
        else:
            await set_event_reality_policy(
                original,
                RealityPolicyCommand(
                    operation_id="hard:first:stale:reality",
                    mode_code="review_on_end",
                ),
                _context(actor),
                _request(runtime),
                Response(),
            )
        with pytest.raises(ProblemError) as rejected:
            await _delete(runtime, actor, source, "event_series", stale)
        assert rejected.value.status == 409
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            original,
        )
        assert _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.event WHERE event_ref=%s)",
            source,
        )
        assert first in _occurrences(migrated_database, source)
        assert not _exists(
            migrated_database,
            "SELECT EXISTS(SELECT 1 FROM dante.occurrence_skip WHERE occurrence_ref=%s)",
            first,
        )
    finally:
        await runtime.dispose()
