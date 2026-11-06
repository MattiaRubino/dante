"""M4 Event Inspector metadata: self ownership, CAS, replay and immutable audit."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid7

import psycopg
import pytest
from fastapi import Request, Response
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from tests.integration.temporal.test_primary_life_area_assignment import (
    _legacy_event,
    _seed_self,
)

from dante.context.contracts import DanteContext
from dante.modules.temporal.event import TemporalEventApplication, _read_event_in_session
from dante.modules.temporal.event_api import (
    EventAtomicEditCommand,
    apply_one_off_event_atomic_edit,
)
from dante.modules.temporal.placement_lock import (
    PlacementLockApplication,
    PlacementLockNotFoundError,
)
from dante.modules.temporal.reality_objective_api import (
    ActivityObjectiveBatchCommand,
    apply_event_objective_edits_in_session,
)
from dante.modules.temporal.schedule import (
    FloatingLocalIntervalPlacement,
    NamedZoneLocalIntervalPlacement,
    SchedulePlacementLockedError,
    TemporalScheduleApplication,
)
from dante.platform.database.runtime import create_database_runtime
from dante.platform.http.problem import ProblemError

pytestmark = pytest.mark.postgres

_EDIT = text("""
    SELECT * FROM dante.revise_self_event_profile(
        :actor,:event,:operation,:expected,:title,:description,:location,:color
    )
""")

_CREATE_OBJECTIVE = text("""
    SELECT * FROM dante.create_self_temporal_objective(
        :actor,:operation,:fingerprint,:objective,'event',:event,
        :label,'boolean',NULL,NULL,NULL,NULL,NULL,0
    )
""")
_RETIRE_OBJECTIVE = text("""
    SELECT * FROM dante.retire_self_temporal_objective(
        :actor,:objective,:operation,:fingerprint,:expected
    )
""")


@pytest.mark.asyncio
async def test_event_schedule_lock_is_owner_scoped_and_blocks_movement(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    other = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "Locked Event")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    schedule_app = TemporalScheduleApplication(runtime.session_factory)
    locks = PlacementLockApplication(runtime.session_factory)
    try:
        schedule = await schedule_app.establish_schedule(
            self_person_ref=owner,
            operation_id="event:lock:schedule",
            subject_native_ref=event,
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=datetime.fromisoformat("2026-11-06T13:00:00"),
                ends_local_at=datetime.fromisoformat("2026-11-06T13:30:00"),
            ),
        )
        initial_lock = await locks.get(self_person_ref=owner, schedule_ref=schedule.schedule_ref)
        assert not initial_lock.locked
        with pytest.raises(PlacementLockNotFoundError):
            await locks.get(self_person_ref=other, schedule_ref=schedule.schedule_ref)
        locked = await locks.set(
            self_person_ref=owner,
            schedule_ref=schedule.schedule_ref,
            locked=True,
            expected_revision=None,
        )
        assert locked.locked
        assert locked.revision == 1
        with pytest.raises(PlacementLockNotFoundError):
            await locks.set(
                self_person_ref=other,
                schedule_ref=schedule.schedule_ref,
                locked=False,
                expected_revision=locked.revision,
            )
        with pytest.raises(SchedulePlacementLockedError):
            await schedule_app.revise_schedule(
                self_person_ref=owner,
                operation_id="event:lock:blocked-move",
                schedule_ref=schedule.schedule_ref,
                expected_material_state_ref=schedule.material_state_ref,
                placement=FloatingLocalIntervalPlacement(
                    starts_local_at=datetime.fromisoformat("2026-11-06T14:00:00"),
                    ends_local_at=datetime.fromisoformat("2026-11-06T14:30:00"),
                ),
            )
        unlocked = await locks.set(
            self_person_ref=owner,
            schedule_ref=schedule.schedule_ref,
            locked=False,
            expected_revision=locked.revision,
        )
        assert not unlocked.locked
        moved = await schedule_app.revise_schedule(
            self_person_ref=owner,
            operation_id="event:lock:allowed-move",
            schedule_ref=schedule.schedule_ref,
            expected_material_state_ref=schedule.material_state_ref,
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=datetime.fromisoformat("2026-11-06T14:00:00"),
                ends_local_at=datetime.fromisoformat("2026-11-06T14:30:00"),
            ),
        )
        assert moved.schedule_ref == schedule.schedule_ref
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_one_off_event_schedule_and_profile_commit_together_with_material_cas(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "Scheduled")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    context = cast(
        DanteContext,
        SimpleNamespace(self_person_ref=owner, effective_zone_id="Europe/Rome"),
    )
    request = Request(
        {"type": "http", "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))}
    )
    try:
        original = await TemporalScheduleApplication(runtime.session_factory).establish_schedule(
            self_person_ref=owner,
            operation_id="event:original:schedule",
            subject_native_ref=event,
            placement=FloatingLocalIntervalPlacement(
                starts_local_at=datetime.fromisoformat("2026-11-05T18:00:00"),
                ends_local_at=datetime.fromisoformat("2026-11-05T19:00:00"),
            ),
        )
        payload = {
            "operation_id": "event:atomic:schedule",
            "schedule": {
                "schedule_ref": original.schedule_ref,
                "expected_material_state_ref": original.material_state_ref,
                "placement": {
                    "kind": "floating_local_interval",
                    "starts_local_at": "2026-11-05T19:00:00",
                    "ends_local_at": "2026-11-05T19:30:00",
                },
            },
            "profile": {
                "operation_id": "event:atomic:schedule:profile",
                "expected_revision": 0,
                "title": "Moved",
            },
        }
        saved = await apply_one_off_event_atomic_edit(
            event, EventAtomicEditCommand.model_validate(payload), context, request, Response()
        )
        assert saved.event.title == "Moved"
        assert saved.event.profile_revision == 1
        with pytest.raises(ProblemError) as stale:
            await apply_one_off_event_atomic_edit(
                event,
                EventAtomicEditCommand.model_validate(
                    {**payload, "operation_id": "event:atomic:schedule:again", "profile": None}
                ),
                context,
                request,
                Response(),
            )
        assert stale.value.status == 409
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_event_participant_changes_are_atomic_and_cas_guarded(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "Participants")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    context = cast(
        DanteContext,
        SimpleNamespace(self_person_ref=owner, effective_zone_id="Europe/Rome"),
    )
    request = Request(
        {"type": "http", "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))}
    )
    try:
        saved = await apply_one_off_event_atomic_edit(
            event,
            EventAtomicEditCommand.model_validate(
                {
                    "operation_id": "event:participants:first",
                    "profile": {
                        "operation_id": "event:participants:profile",
                        "expected_revision": 0,
                        "title": "Participants saved",
                    },
                    "participants": [
                        {
                            "participant_ref": "self",
                            "requirement_code": "required",
                            "expected_requirement_code": None,
                        }
                    ],
                }
            ),
            context,
            request,
            Response(),
        )
        assert saved.event.title == "Participants saved"
        with pytest.raises(ProblemError) as conflict:
            await apply_one_off_event_atomic_edit(
                event,
                EventAtomicEditCommand.model_validate(
                    {
                        "operation_id": "event:participants:stale",
                        "profile": {
                            "operation_id": "event:participants:stale:profile",
                            "expected_revision": 1,
                            "title": "Should roll back",
                        },
                        "participants": [
                            {
                                "participant_ref": "self",
                                "requirement_code": "optional",
                                "expected_requirement_code": None,
                            }
                        ],
                    }
                ),
                context,
                request,
                Response(),
            )
        assert conflict.value.status == 409
        async with runtime.session_factory() as session, session.begin():
            after = await _read_event_in_session(session, self_person_ref=owner, event_ref=event)
        assert after is not None
        assert after.title == "Participants saved"
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_one_off_event_reminder_and_profile_commit_in_one_transaction(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "Reminder")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    context = cast(
        DanteContext,
        SimpleNamespace(self_person_ref=owner, effective_zone_id="Europe/Rome"),
    )
    request = Request(
        {"type": "http", "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))}
    )
    try:
        schedule = await TemporalScheduleApplication(runtime.session_factory).establish_schedule(
            self_person_ref=owner,
            operation_id="event:reminder:schedule",
            subject_native_ref=event,
            placement=NamedZoneLocalIntervalPlacement(
                starts_local_at=datetime.fromisoformat("2026-11-05T18:00:00"),
                ends_local_at=datetime.fromisoformat("2026-11-05T19:00:00"),
                zone_id="Europe/Rome",
            ),
        )
        saved = await apply_one_off_event_atomic_edit(
            event,
            EventAtomicEditCommand.model_validate(
                {
                    "operation_id": "event:atomic:reminder",
                    "profile": {
                        "operation_id": "event:atomic:reminder:profile",
                        "expected_revision": 0,
                        "title": "Reminder changed",
                    },
                    "reminder": {
                        "schedule_ref": schedule.schedule_ref,
                        "expected_state_ref": None,
                        "enabled": True,
                        "lead_minutes": 15,
                    },
                }
            ),
            context,
            request,
            Response(),
        )
        assert saved.event.title == "Reminder changed"
        async with runtime.session_factory() as session, session.begin():
            reminder = (
                (
                    await session.execute(
                        text("SELECT * FROM dante.get_self_schedule_reminder(:actor,:schedule)"),
                        {"actor": owner, "schedule": schedule.schedule_ref},
                    )
                )
                .mappings()
                .one()
            )
        assert reminder["lead_minutes"] == 15
        assert reminder["enabled"] is True
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_one_off_event_atomic_edit_rolls_back_profile_on_stale_agenda(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "Original")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    context = cast(
        DanteContext,
        SimpleNamespace(self_person_ref=owner, effective_zone_id="Europe/Rome"),
    )
    request = Request(
        {
            "type": "http",
            "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime)),
        }
    )
    application = TemporalEventApplication(runtime.session_factory)
    try:
        stale = EventAtomicEditCommand.model_validate(
            {
                "operation_id": "event:atomic:stale",
                "profile": {
                    "operation_id": "event:atomic:stale:profile",
                    "expected_revision": 0,
                    "title": "Changed",
                },
                "agenda": {
                    "operation_id": "event:atomic:stale:agenda",
                    "expected_revision": 12,
                    "agenda_parts": ["Introduction"],
                },
            }
        )
        with pytest.raises(ProblemError) as failure:
            await apply_one_off_event_atomic_edit(event, stale, context, request, Response())
        assert failure.value.status == 409
        unchanged = await application.get_event(self_person_ref=owner, event_ref=event)
        assert unchanged is not None
        assert unchanged.title == "Original"
        assert unchanged.profile_revision == 0
        assert unchanged.agenda_parts == ()

        accepted = EventAtomicEditCommand.model_validate(
            {
                "operation_id": "event:atomic:accepted",
                "profile": {
                    "operation_id": "event:atomic:accepted:profile",
                    "expected_revision": 0,
                    "title": "Changed",
                },
                "agenda": {
                    "operation_id": "event:atomic:accepted:agenda",
                    "expected_revision": 0,
                    "agenda_parts": ["Introduction"],
                },
                "objectives": {
                    "add": [
                        {
                            "operation_id": "event:atomic:objective",
                            "label": "Result",
                            "result_kind": "boolean",
                            "presentation_order": 0,
                        }
                    ]
                },
                "reality": {
                    "operation_id": "event:atomic:reality",
                    "mode_code": "review_on_end",
                    "expected_state_ref": None,
                },
            }
        )
        saved = await apply_one_off_event_atomic_edit(event, accepted, context, request, Response())
        assert saved.event.title == "Changed"
        assert saved.event.profile_revision == 1
        assert saved.event.agenda_parts == ["Introduction"]
        assert [row.label for row in saved.objectives] == ["Result"]
        async with runtime.session_factory() as session, session.begin():
            policy = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.get_self_reality_review_policy(:actor,'event',:event)"
                        ),
                        {"actor": owner, "event": event},
                    )
                )
                .mappings()
                .one()
            )
        assert policy["mode_code"] == "review_on_end"
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_one_off_event_objective_batch_rolls_back_revision_when_retirement_is_stale(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "One-off")
    revised, removed = uuid7(), uuid7()
    runtime = create_database_runtime(migrated_database.runtime_settings())
    try:
        async with runtime.session_factory() as session, session.begin():
            for index, objective in enumerate((revised, removed)):
                await session.execute(
                    _CREATE_OBJECTIVE,
                    {
                        "actor": owner,
                        "operation": f"event:batch:create:{index}",
                        "fingerprint": f"{index + 1}" * 64,
                        "objective": objective,
                        "event": event,
                        "label": f"Original {index}",
                    },
                )
        command: dict[str, Any] = {
            "add": [
                {
                    "operation_id": "event:batch:add",
                    "label": "Nuovo",
                    "result_kind": "boolean",
                    "presentation_order": 2,
                }
            ],
            "revise": [
                {
                    "objective_ref": revised,
                    "change": {
                        "operation_id": "event:batch:revise",
                        "expected_revision": 0,
                        "label": "Aggiornato",
                        "result_kind": "boolean",
                        "presentation_order": 0,
                    },
                }
            ],
            "retire": [
                {
                    "objective_ref": removed,
                    "operation_id": "event:batch:retire",
                    "expected_revision": 1,
                }
            ],
        }

        async def reject_stale_batch() -> None:
            async with runtime.session_factory() as session, session.begin():
                await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
                await apply_event_objective_edits_in_session(
                    session,
                    actor=owner,
                    subject_ref=event,
                    payload=ActivityObjectiveBatchCommand.model_validate(command),
                    effective_zone_id="Europe/Rome",
                )

        with pytest.raises(DBAPIError):
            await reject_stale_batch()

        async with runtime.session_factory() as session, session.begin():
            before = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.list_self_temporal_objectives(:actor,'event',:event)"
                        ),
                        {"actor": owner, "event": event},
                    )
                )
                .mappings()
                .all()
            )
        assert {row["label"] for row in before} == {"Original 0", "Original 1"}

        command["retire"][0]["expected_revision"] = 0
        async with runtime.session_factory() as session, session.begin():
            await session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))
            after = await apply_event_objective_edits_in_session(
                session,
                actor=owner,
                subject_ref=event,
                payload=ActivityObjectiveBatchCommand.model_validate(command),
                effective_zone_id="Europe/Rome",
            )
        assert {row.label for row in after} == {"Aggiornato", "Nuovo"}

        command["revise"][0]["change"]["scope_code"] = "this_and_following"
        with pytest.raises(ProblemError):
            async with runtime.session_factory() as session, session.begin():
                await apply_event_objective_edits_in_session(
                    session,
                    actor=owner,
                    subject_ref=event,
                    payload=ActivityObjectiveBatchCommand.model_validate(command),
                    effective_zone_id="Europe/Rome",
                )
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_one_off_event_objective_retirement_is_owner_scoped_replayable_and_revision_guarded(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "One-off")
    objective = uuid7()
    runtime = create_database_runtime(migrated_database.runtime_settings())
    command = {
        "actor": owner,
        "objective": objective,
        "operation": "event:objective:retire",
        "fingerprint": "b" * 64,
        "expected": 0,
    }
    try:
        async with runtime.session_factory() as session, session.begin():
            await session.execute(
                _CREATE_OBJECTIVE,
                {
                    "actor": owner,
                    "operation": "event:objective:create",
                    "fingerprint": "a" * 64,
                    "objective": objective,
                    "event": event,
                    "label": "Arrivare",
                },
            )

        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _RETIRE_OBJECTIVE,
                    {**command, "actor": stranger, "operation": "event:foreign"},
                )
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _RETIRE_OBJECTIVE,
                    {**command, "operation": "event:stale", "expected": 1},
                )

        async with runtime.session_factory() as session, session.begin():
            applied = (await session.execute(_RETIRE_OBJECTIVE, command)).mappings().one()
            replay = (await session.execute(_RETIRE_OBJECTIVE, command)).mappings().one()
        assert applied["objective_ref"] == objective
        assert applied["replayed"] is False
        assert replay["replayed"] is True

        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _RETIRE_OBJECTIVE,
                    {**command, "operation": "event:reused", "fingerprint": "c" * 64},
                )

        async with runtime.session_factory() as session, session.begin():
            current = (
                await session.execute(
                    text(
                        "SELECT * FROM dante.list_self_temporal_objectives(:actor,'event',:event)"
                    ),
                    {"actor": owner, "event": event},
                )
            ).all()
        assert current == []
        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator", migrated_database.cluster.migrator_password
            )
        ) as db:
            db.execute("SET ROLE dante_owner")
            tombstone = db.execute(
                "SELECT retired_at,retirement_operation_id FROM dante.temporal_objective "
                "WHERE objective_ref=%s",
                (objective,),
            ).fetchone()
        assert tombstone is not None
        assert tombstone[0] is not None
        assert tombstone[1] == command["operation"]
    finally:
        await runtime.dispose()


@pytest.mark.asyncio
async def test_event_profile_is_guarded_and_current_read_tracks_append_only_edits(
    migrated_database: Any,
) -> None:
    owner = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    event = _legacy_event(migrated_database, owner, "Original")
    runtime = create_database_runtime(migrated_database.runtime_settings())
    command = {
        "actor": owner,
        "event": event,
        "operation": "m4:metadata:edit",
        "expected": 0,
        "title": "Modificato",
        "description": "Descrizione",
        "location": "Sala A",
        "color": "#ABCDEF",
    }
    try:
        async with runtime.session_factory() as session, session.begin():
            first = (await session.execute(_EDIT, command)).mappings().one()
            replay = (await session.execute(_EDIT, command)).mappings().one()
        assert first["event_ref"] == event
        assert first["revision"] == 1
        assert first["replayed"] is False
        assert replay["revision"] == 1
        assert replay["replayed"] is True

        canonical = await TemporalEventApplication(runtime.session_factory).get_event(
            self_person_ref=owner,
            event_ref=event,
        )
        assert canonical is not None
        assert canonical.title == "Modificato"
        assert canonical.description == "Descrizione"
        assert canonical.location == "Sala A"
        assert canonical.color_code == "#ABCDEF"
        assert canonical.profile_revision == 1

        with psycopg.connect(
            **migrated_database.connection_kwargs(
                "dante_migrator",
                migrated_database.cluster.migrator_password,
            )
        ) as db:
            db.execute("SET ROLE dante_owner")
            fetched_row = db.execute(
                "SELECT previous_profile,current_profile FROM dante.event_profile_revision "
                "WHERE event_ref=%s AND revision=1",
                (event,),
            ).fetchone()
            assert fetched_row is not None
            before, after = fetched_row
        assert before["title"] == "Original"
        assert after["title"] == "Modificato"

        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(_EDIT, {**command, "operation": "m4:stale"})
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _EDIT,
                    {
                        **command,
                        "actor": stranger,
                        "operation": "m4:foreign",
                    },
                )
        with pytest.raises(DBAPIError):
            async with runtime.session_factory() as session, session.begin():
                await session.execute(
                    _EDIT,
                    {
                        **command,
                        "title": "Reused with different intent",
                    },
                )

        canonical_after = await TemporalEventApplication(runtime.session_factory).get_event(
            self_person_ref=owner,
            event_ref=event,
        )
        assert canonical_after is not None
        assert canonical_after.title == "Modificato"
        assert canonical_after.profile_revision == 1
    finally:
        await runtime.dispose()
