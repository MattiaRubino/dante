"""Event Save retries only rolled-back serializable transactions."""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import Request, Response
from sqlalchemy.exc import OperationalError

from dante.context.contracts import DanteContext
from dante.modules.temporal.event_api import (
    EventAtomicEditCommand,
    EventAtomicEditResponse,
    EventAtomicLifeAreaChange,
    EventAtomicNewLifeArea,
    apply_one_off_event_atomic_edit,
)
from dante.platform.http.problem import ProblemError


class _SqlStateError(Exception):
    def __init__(self, code: str, constraint: str | None = None) -> None:
        super().__init__("database diagnostic redacted")
        self.sqlstate = code
        self.diag = SimpleNamespace(constraint_name=constraint)


def _error(code: str, constraint: str | None = None) -> OperationalError:
    return OperationalError("redacted statement", {}, _SqlStateError(code, constraint))


@pytest.mark.parametrize(
    ("outcomes", "attempts", "status"),
    [
        ([_error("40001"), "accepted"], 2, None),
        ([_error("40001"), _error("40001"), _error("40001")], 3, 503),
        ([_error("23505")], 1, 409),
        ([_error("P0001", "life_area_assignment_revision_conflict")], 1, 409),
        ([_error("40001"), _error("P0001", "life_area_assignment_revision_conflict")], 2, 409),
    ],
)
@pytest.mark.asyncio
async def test_event_atomic_edit_retries_only_serialization_abort(
    monkeypatch: pytest.MonkeyPatch,
    outcomes: list[OperationalError | str],
    attempts: int,
    status: int | None,
) -> None:
    accepted = cast(EventAtomicEditResponse, object())
    command = EventAtomicEditCommand(
        operation_id="retry:event-new-area",
        life_area=EventAtomicLifeAreaChange(
            expected_assignment_revision=0,
            life_area_ref=None,
            new_life_area=EventAtomicNewLifeArea(name="Nuova area", color_code="#8E24AA"),
        ),
    )
    actor, event_ref = uuid4(), uuid4()
    context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
    request = cast(Request, SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace())))
    response = Response()
    run_once = AsyncMock(
        side_effect=[accepted if value == "accepted" else value for value in outcomes]
    )
    monkeypatch.setattr(
        "dante.modules.temporal.event_api._commit_one_off_event_atomic_edit_once", run_once
    )

    if status is None:
        result = await apply_one_off_event_atomic_edit(
            event_ref, command, context, request, response
        )
        assert result is accepted
    else:
        with pytest.raises(ProblemError) as raised:
            await apply_one_off_event_atomic_edit(event_ref, command, context, request, response)
        assert raised.value.status == status
    assert run_once.await_count == attempts
    assert all(
        call.args == (event_ref, command, context, request) for call in run_once.await_args_list
    )
    assert response.headers["Cache-Control"] == "no-store"
