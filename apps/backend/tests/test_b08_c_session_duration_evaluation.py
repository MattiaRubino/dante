"""Unit proofs for the B08-C Session duration read projection."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import pytest

from dante.modules.temporal.session_runtime import SessionApplication, SessionView
from dante.platform.database.references import MaterialStateRef, NativeRef

_SESSION_REF = NativeRef(UUID("0199a8c0-4e70-7abf-89c0-91e3f2e4506c"))
_SUBJECT_REF = NativeRef(UUID("0199a8c0-5e71-7bc0-8ad0-a2f403f5617d"))
_TIMING_REF = MaterialStateRef(UUID("0199a8c0-7e73-7de2-8cf2-c4062517839f"))
_CONSTRAINT_REF = UUID("0199a8c0-6e72-7cd1-9be1-b3f51406728e")
_CONSTRAINT_STATE_REF = UUID("0199a8c0-8e74-7ef3-9d03-d517362894a0")
_STARTED_AT = datetime(2026, 9, 24, 8, 0, tzinfo=UTC)


def _session(*, ended_at: datetime | None) -> SessionView:
    return SessionView(
        session_ref=_SESSION_REF,
        subject_native_ref=_SUBJECT_REF,
        timing_material_state_ref=_TIMING_REF,
        started_at=_STARTED_AT,
        ended_at=ended_at,
    )


def _row(*, active_seconds: Decimal) -> dict[str, object]:
    return {
        "constraint_ref": _CONSTRAINT_REF,
        "constraint_material_state_ref": _CONSTRAINT_STATE_REF,
        "strength_code": "soft",
        "duration_microseconds": 45 * 60 * 1_000_000,
        "active_seconds": active_seconds,
    }


@pytest.mark.parametrize(
    ("session", "active_seconds", "expected"),
    [
        (_session(ended_at=None), Decimal("44.999999"), "pending"),
        (_session(ended_at=None), Decimal("45"), "satisfied"),
        (_session(ended_at=_STARTED_AT), Decimal("44.999999"), "violated"),
        (_session(ended_at=_STARTED_AT), Decimal("45"), "satisfied"),
    ],
)
def test_session_minimum_evaluation_compares_active_microseconds_exactly(
    session: SessionView,
    active_seconds: Decimal,
    expected: str,
) -> None:
    result = SessionApplication._duration_evaluations(
        rows=[_row(active_seconds=active_seconds)],
        session=session,
    )

    assert len(result) == 1
    assert result[0].evaluation == expected
    assert result[0].constraint_ref == _CONSTRAINT_REF
    assert result[0].material_state_ref == _CONSTRAINT_STATE_REF
