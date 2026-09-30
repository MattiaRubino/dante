"""B12-D self-scoped Movement Policy authoring contract."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID

import pytest
from fastapi import Response

from dante.bootstrap.openapi_export import openapi_document
from dante.modules.temporal.movement_policy import (
    MovementPolicyApplication,
    MovementPolicyMutationView,
    MovementPolicyStateConflictError,
)
from dante.modules.temporal.movement_policy_api import (
    SetMovementPolicyBody,
    set_self_schedule_movement_policy,
)
from dante.platform.database.references import MaterialStateRef, ScopedRecordRef
from dante.platform.http.problem import ProblemError
from tests.test_temporal_constraint_api import _context

SCHEDULE = UUID("0199a8c0-5e74-7bc0-8ad0-a2f403f56185")
STATE = UUID("0199a8c0-5e74-7bc0-8ad0-a2f403f56187")


class PolicyApplication:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.error: Exception | None = None

    async def create_policy(self, **kwargs: Any) -> MovementPolicyMutationView:
        self.calls.append(("create", kwargs))
        if self.error:
            raise self.error
        return MovementPolicyMutationView(
            ScopedRecordRef(SCHEDULE),
            MaterialStateRef(STATE),
            True,
            datetime(2026, 9, 30, tzinfo=UTC),
            False,
        )

    async def revise_policy(self, **kwargs: Any) -> MovementPolicyMutationView:
        self.calls.append(("revise", kwargs))
        if self.error:
            raise self.error
        return await self.create_policy(**kwargs)


def test_movement_policy_route_is_an_explicit_mutation() -> None:
    paths = cast(dict[str, Any], openapi_document()["paths"])
    route = paths["/api/v1/temporal/schedules/{schedule_ref}/movement-policy"]
    assert set(route) == {"put"}
    assert route["put"]["operationId"] == "temporal_set_self_schedule_movement_policy"
    assert set(route["put"]["responses"]) == {"200", "401", "403", "404", "409", "422", "503"}


@pytest.mark.asyncio
async def test_policy_api_creates_and_revises_with_authenticated_self_and_cas() -> None:
    app = PolicyApplication()
    body = SetMovementPolicyBody(
        operation_id="b12d:configure",
        expected_material_state_ref=None,
        automatic_movement="automatic",
        acceptance_path="confirmation_required",
    )
    response = await set_self_schedule_movement_policy(
        SCHEDULE,
        body,
        _context(),
        cast(MovementPolicyApplication, app),
        Response(),
    )
    assert response.material_state_ref == STATE
    assert app.calls[0][0] == "create"
    assert app.calls[0][1]["self_person_ref"] == _context().self_person_ref
    assert app.calls[0][1]["schedule_ref"] == SCHEDULE
    assert app.calls[0][1]["rule"].acceptance_path == "confirmation_required"

    body.expected_material_state_ref = STATE
    await set_self_schedule_movement_policy(
        SCHEDULE,
        body,
        _context(),
        cast(MovementPolicyApplication, app),
        Response(),
    )
    assert app.calls[1][0] == "revise"
    assert app.calls[1][1]["expected_material_state_ref"] == STATE

    app.error = MovementPolicyStateConflictError()
    with pytest.raises(ProblemError) as error:
        await set_self_schedule_movement_policy(
            SCHEDULE,
            body,
            _context(),
            cast(MovementPolicyApplication, app),
            Response(),
        )
    assert error.value.status == 409
