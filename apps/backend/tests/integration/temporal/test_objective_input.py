"""PostgreSQL: provisional Objective input is never accepted Result until Confirm."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from types import SimpleNamespace
from typing import Any
from uuid import uuid7

import pytest
from fastapi import Request, Response
from sqlalchemy import text
from tests.integration.temporal.test_activity_quick_authoring_metadata import _seed_self

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext
from dante.modules.temporal.authoring import TemporalAuthoringApplication
from dante.modules.temporal.reality_objective_api import (
    ObjectiveCreateCommand,
    ObjectiveInputConfirm,
    ObjectiveInputDraftPayload,
    ObjectiveInputDraftSave,
    confirm_objective_input_draft,
    create_activity_objective,
    list_objective_input_drafts,
    save_objective_input_draft,
)
from dante.modules.temporal.schedule import AbsoluteIntervalPlacement
from dante.platform.database.references import NativeRef
from dante.platform.database.runtime import create_database_runtime
from dante.platform.time import TimeZoneMode, TimeZonePolicy

pytestmark = pytest.mark.postgres


def _context(self_person_ref: NativeRef) -> DanteContext:
    now = datetime.now(UTC)
    return DanteContext(
        principal=Principal(
            account_ref=uuid7(),
            auth_session_ref=uuid7(),
            authenticated_at=now,
            recent_auth_at=now,
        ),
        self_person_ref=self_person_ref,
        timezone_policy=TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE),
        effective_zone_id="Europe/Rome",
    )


@pytest.mark.asyncio
async def test_input_survives_refresh_and_is_not_observation_before_explicit_confirm(
    migrated_database: Any,
) -> None:
    actor = _seed_self(migrated_database)
    stranger = _seed_self(migrated_database)
    runtime = create_database_runtime(migrated_database.runtime_settings())
    request = Request(
        {"type": "http", "app": SimpleNamespace(state=SimpleNamespace(database_runtime=runtime))}
    )
    context = _context(actor)
    now = datetime.now(UTC)
    try:
        created = await TemporalAuthoringApplication(runtime.session_factory).create_activity(
            self_person_ref=actor,
            operation_id="objective-workspace:create",
            title="Allenamento",
            placement=AbsoluteIntervalPlacement(
                starts_at=now,
                ends_at=now + timedelta(hours=1),
            ),
        )
        activity = created.item.subject_native_ref
        objective = await create_activity_objective(
            activity,
            ObjectiveCreateCommand(
                operation_id="objective-workspace:objective",
                label="Ripetizioni",
                result_kind="quantity",
                comparator_code="gte",
                target_value=Decimal(20),
                presentation_order=1,
            ),
            context,
            request,
            Response(),
        )
        response = Response()
        first = await save_objective_input_draft(
            objective.objective_ref,
            ObjectiveInputDraftSave(
                operation_id="objective-workspace:stage",
                input=ObjectiveInputDraftPayload(observed_numeric=Decimal(15)),
            ),
            context,
            request,
            response,
        )
        assert first.revision == 1
        assert first.confirmed_at is None
        result = await list_objective_input_drafts(context, request, Response())
        assert len(result) == 1
        assert result[0].payload.observed_numeric == 15
        assert await list_objective_input_drafts(_context(stranger), request, Response()) == []
        async with runtime.session_factory() as session, session.begin():
            before = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.list_self_temporal_objectives(:actor,'activity',:ref)"
                        ),
                        {"actor": actor, "ref": activity},
                    )
                )
                .mappings()
                .all()
            )
            assert before[0]["observation_ref"] is None

        confirmed = await confirm_objective_input_draft(
            objective.objective_ref,
            ObjectiveInputConfirm(
                operation_id="objective-workspace:confirm",
                expected_revision=1,
            ),
            context,
            request,
            Response(),
        )
        assert not confirmed.replayed
        replay = await confirm_objective_input_draft(
            objective.objective_ref,
            ObjectiveInputConfirm(
                operation_id="objective-workspace:confirm",
                expected_revision=1,
            ),
            context,
            request,
            Response(),
        )
        assert replay.replayed
        assert replay.observation_ref == confirmed.observation_ref
        inputs = await list_objective_input_drafts(context, request, Response())
        assert inputs[0].confirmed_at is not None
        async with runtime.session_factory() as session, session.begin():
            after = (
                (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.list_self_temporal_objectives(:actor,'activity',:ref)"
                        ),
                        {"actor": actor, "ref": activity},
                    )
                )
                .mappings()
                .all()
            )
            assert after[0]["observation_ref"] == confirmed.observation_ref
            assert after[0]["observed_numeric"] == 15
    finally:
        await runtime.dispose()
