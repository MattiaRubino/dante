"""A serializable abort retries the entire hard-delete transaction, not its statement."""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast
from uuid import uuid4

import pytest
from fastapi import Request, Response
from sqlalchemy.exc import OperationalError

from dante.context.contracts import DanteContext
from dante.modules.temporal.activity_inspector_api import (
    ActivityHardDeleteCommand,
    delete_self_activity_hard,
)
from dante.modules.temporal.reality_objective_api import (
    TemporalHardDeleteCommand,
    apply_temporal_hard_deletion,
)
from dante.platform.http.problem import ProblemError


class _SqlStateError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__("redacted database diagnostic")
        self.sqlstate = code


class _Transaction:
    def __init__(self, outcomes: list[int | Exception], calls: list[dict[str, object]]) -> None:
        self.outcomes = outcomes
        self.calls = calls

    async def __aenter__(self) -> _Transaction:
        return self

    async def __aexit__(self, *_: object) -> None:
        return None

    def begin(self) -> _Transaction:
        return self

    async def execute(self, *_: object) -> None:
        return None

    async def scalar(self, _statement: object, parameters: dict[str, object]) -> int:
        self.calls.append(parameters)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def _error(code: str) -> OperationalError:
    return OperationalError("redacted statement", {}, _SqlStateError(code))


@pytest.mark.parametrize("endpoint", ["activity", "temporal"])
@pytest.mark.parametrize(
    ("outcomes", "expected_attempts", "expected_status"),
    [
        ([_error("40001"), 2], 2, None),
        ([_error("40001"), _error("40001"), _error("40001")], 3, 503),
        ([_error("23505")], 1, 503),
    ],
)
@pytest.mark.asyncio
async def test_hard_delete_retries_only_serialization_abort_with_same_cas(
    endpoint: str,
    outcomes: list[int | Exception],
    expected_attempts: int,
    expected_status: int | None,
) -> None:
    attempts: list[dict[str, object]] = []
    transactions: list[_Transaction] = []
    remaining = outcomes.copy()

    def session_factory() -> _Transaction:
        transaction = _Transaction(remaining, attempts)
        transactions.append(transaction)
        return transaction

    actor, ref = uuid4(), uuid4()
    context = cast(DanteContext, SimpleNamespace(self_person_ref=actor))
    request = cast(
        Request,
        SimpleNamespace(
            app=SimpleNamespace(
                state=SimpleNamespace(
                    database_runtime=SimpleNamespace(session_factory=session_factory)
                )
            )
        ),
    )
    fingerprint = "a" * 64
    if endpoint == "activity":
        operation = delete_self_activity_hard(
            ref,
            ActivityHardDeleteCommand(expected_session_fingerprint=fingerprint),
            context,
            request,
            Response(),
        )
    else:
        operation = apply_temporal_hard_deletion(
            ref,
            TemporalHardDeleteCommand(scope="event_once", expected_fingerprint=fingerprint),
            context,
            request,
            Response(),
        )
    if expected_status is None:
        result = await operation
        assert result.deleted_rows == 2
    else:
        with pytest.raises(ProblemError) as raised:
            await operation
        assert raised.value.status == (
            409 if endpoint == "temporal" and len(outcomes) == 1 else expected_status
        )
    assert len(transactions) == expected_attempts
    assert len(attempts) == expected_attempts
    assert all(parameters == attempts[0] for parameters in attempts)
    assert attempts[0]["fingerprint"] == fingerprint
