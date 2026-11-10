"""SQLSTATE 40001 bounded retry is distinct from real CAS conflicts."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import OperationalError

from dante.modules.temporal.recurring_series_edit import (
    RecurringSeriesAccepted,
    RecurringSeriesEditApplication,
    RecurringSeriesEditConflictError,
    _MAX_SERIALIZATION_ATTEMPTS,
    _is_serialization_failure,
)


class _SqlStateError(Exception):
    def __init__(self, sqlstate: str) -> None:
        super().__init__("database diagnostic redacted")
        self.sqlstate = sqlstate


def _database_error(sqlstate: str) -> OperationalError:
    return OperationalError(
        "redacted statement",
        {},
        _SqlStateError(sqlstate),
    )


def _intent() -> dict[str, Any]:
    return {
        "self_person_ref": uuid4(),
        "selected_occurrence_ref": uuid4(),
        "requested_scope": "this_and_following",
        "expected_revision": 2,
        "expected_state_ref": uuid4(),
        "effective_zone_id": "Europe/Rome",
        "proposed_recurrence": object(),
        "proposed_structure": {"version": 1},
        "profile_patch": {"title": "Revised"},
        "expected_fingerprint": "a" * 64,
        "operation_id": "bounded-retry:series:one-operation",
    }


def test_only_serialization_sqlstate_is_retryable() -> None:
    assert _is_serialization_failure(_database_error("40001"))
    assert not _is_serialization_failure(_database_error("23505"))
    assert not _is_serialization_failure(_database_error("40P01"))
    assert not _is_serialization_failure(RecurringSeriesEditConflictError("stale"))


@pytest.mark.asyncio
async def test_retry_reissues_same_intent_and_returns_one_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    accepted = RecurringSeriesAccepted(
        source_ref=uuid4(),
        recurrence_state_ref=uuid4(),
        superseded_count=2,
        protected_count=1,
    )
    attempt = AsyncMock(side_effect=[_database_error("40001"), accepted])
    pause = AsyncMock()
    app = RecurringSeriesEditApplication(None)  # type: ignore[arg-type]
    monkeypatch.setattr(app, "_accept_once", attempt)
    monkeypatch.setattr(
        "dante.modules.temporal.recurring_series_edit.asyncio.sleep",
        pause,
    )
    intent = _intent()
    assert await app.accept(**intent) == accepted
    assert attempt.await_count == 2
    assert attempt.await_args_list[0].kwargs == intent
    assert attempt.await_args_list[1].kwargs == intent
    pause.assert_awaited_once()


@pytest.mark.asyncio
async def test_bounded_serialization_retries_never_loop_forever(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = RecurringSeriesEditApplication(None)  # type: ignore[arg-type]
    attempt = AsyncMock(side_effect=_database_error("40001"))
    monkeypatch.setattr(app, "_accept_once", attempt)
    monkeypatch.setattr(
        "dante.modules.temporal.recurring_series_edit.asyncio.sleep",
        AsyncMock(),
    )
    with pytest.raises(
        RecurringSeriesEditConflictError,
        match="after bounded retries",
    ):
        await app.accept(**_intent())
    assert attempt.await_count == _MAX_SERIALIZATION_ATTEMPTS


@pytest.mark.asyncio
async def test_real_conflict_does_not_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = RecurringSeriesEditApplication(None)  # type: ignore[arg-type]
    attempt = AsyncMock(side_effect=RecurringSeriesEditConflictError("stale source"))
    monkeypatch.setattr(app, "_accept_once", attempt)
    pause = AsyncMock()
    monkeypatch.setattr(
        "dante.modules.temporal.recurring_series_edit.asyncio.sleep",
        pause,
    )
    with pytest.raises(RecurringSeriesEditConflictError, match="stale source"):
        await app.accept(**_intent())
    assert attempt.await_count == 1
    pause.assert_not_awaited()


@pytest.mark.asyncio
async def test_other_database_sqlstate_does_not_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = RecurringSeriesEditApplication(None)  # type: ignore[arg-type]
    attempt = AsyncMock(side_effect=_database_error("23505"))
    monkeypatch.setattr(app, "_accept_once", attempt)
    with pytest.raises(OperationalError):
        await app.accept(**_intent())
    assert attempt.await_count == 1
