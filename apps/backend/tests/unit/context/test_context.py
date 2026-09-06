"""Unit proof for authenticated DANTE application-context semantics."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContextIntegrityError
from dante.context.service import _context_from_persisted
from dante.platform.time import InvalidTimeZoneError, MissingDeviceTimeZoneError, TimeZoneMode

_ACCOUNT_REF = UUID("018f1f26-8b2e-7abc-8000-000000000001")
_SESSION_REF = UUID("018f1f26-8b2e-7abc-8000-000000000002")
_PERSON_REF = UUID("018f1f26-8b2e-7abc-8000-000000000003")
_OTHER_ACCOUNT_REF = UUID("018f1f26-8b2e-7abc-8000-000000000004")


def _principal() -> Principal:
    instant = datetime(2026, 9, 6, 12, 0, tzinfo=UTC)
    return Principal(
        account_ref=_ACCOUNT_REF,
        auth_session_ref=_SESSION_REF,
        authenticated_at=instant,
        recent_auth_at=instant,
    )


def test_follow_device_context_preserves_account_person_distinction() -> None:
    context = _context_from_persisted(
        principal=_principal(),
        row={
            "account_ref": _ACCOUNT_REF,
            "self_person_ref": _PERSON_REF,
            "timezone_mode": "follow_device",
            "fixed_zone_id": None,
        },
        device_zone_id="Europe/Rome",
    )

    assert context.principal.account_ref == _ACCOUNT_REF
    assert context.self_person_ref == _PERSON_REF
    assert context.principal.account_ref != context.self_person_ref
    assert context.timezone_policy.mode is TimeZoneMode.FOLLOW_DEVICE
    assert context.effective_zone_id == "Europe/Rome"


def test_fixed_context_ignores_changed_or_invalid_device_zone() -> None:
    context = _context_from_persisted(
        principal=_principal(),
        row={
            "account_ref": _ACCOUNT_REF,
            "self_person_ref": _PERSON_REF,
            "timezone_mode": "fixed",
            "fixed_zone_id": "America/New_York",
        },
        device_zone_id="Not/AZone",
    )

    assert context.timezone_policy.mode is TimeZoneMode.FIXED
    assert context.effective_zone_id == "America/New_York"


def test_follow_device_requires_device_timezone() -> None:
    with pytest.raises(MissingDeviceTimeZoneError):
        _context_from_persisted(
            principal=_principal(),
            row={
                "account_ref": _ACCOUNT_REF,
                "self_person_ref": _PERSON_REF,
                "timezone_mode": "follow_device",
                "fixed_zone_id": None,
            },
            device_zone_id=None,
        )


def test_follow_device_rejects_fixed_offset_identifier() -> None:
    with pytest.raises(InvalidTimeZoneError):
        _context_from_persisted(
            principal=_principal(),
            row={
                "account_ref": _ACCOUNT_REF,
                "self_person_ref": _PERSON_REF,
                "timezone_mode": "follow_device",
                "fixed_zone_id": None,
            },
            device_zone_id="+02:00",
        )


def test_invalid_persisted_fixed_timezone_is_internal_integrity_failure() -> None:
    with pytest.raises(DanteContextIntegrityError):
        _context_from_persisted(
            principal=_principal(),
            row={
                "account_ref": _ACCOUNT_REF,
                "self_person_ref": _PERSON_REF,
                "timezone_mode": "fixed",
                "fixed_zone_id": "Not/AZone",
            },
            device_zone_id="Europe/Rome",
        )


def test_invalid_persisted_timezone_mode_is_internal_integrity_failure() -> None:
    with pytest.raises(DanteContextIntegrityError):
        _context_from_persisted(
            principal=_principal(),
            row={
                "account_ref": _ACCOUNT_REF,
                "self_person_ref": _PERSON_REF,
                "timezone_mode": "broken",
                "fixed_zone_id": None,
            },
            device_zone_id="Europe/Rome",
        )


def test_persisted_context_must_match_authenticated_account() -> None:
    with pytest.raises(DanteContextIntegrityError, match="does not belong"):
        _context_from_persisted(
            principal=_principal(),
            row={
                "account_ref": _OTHER_ACCOUNT_REF,
                "self_person_ref": _PERSON_REF,
                "timezone_mode": "follow_device",
                "fixed_zone_id": None,
            },
            device_zone_id="Europe/Rome",
        )
