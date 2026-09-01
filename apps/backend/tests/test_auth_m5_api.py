"""Focused public M5 Auth methods/password HTTP-contract proof."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest
from fastapi import Request, Response
from pydantic import SecretStr

from dante.auth.contracts import (
    AdmittedSession,
    AuthenticationMethods,
    AuthenticationProviderMethod,
    AuthenticatorRemovalBlockedError,
    IssuedSession,
    Principal,
)
from dante.auth.m5_api import (
    PasswordEstablishRequest,
    establish_password,
    get_authentication_methods,
    remove_password,
)
from dante.platform.http.problem import ProblemError

_ACCOUNT_REF = UUID("00000000-0000-4000-8000-000000000001")
_SESSION_REF = UUID("00000000-0000-4000-8000-000000000002")
_EXTERNAL_IDENTITY_REF = UUID("00000000-0000-4000-8000-000000000003")
_SESSION_SECRET = "session-secret"
_CSRF_TOKEN = "csrf-token"


def _principal() -> Principal:
    now = datetime(2026, 9, 1, 10, 0, tzinfo=UTC)
    return Principal(
        account_ref=_ACCOUNT_REF,
        auth_session_ref=_SESSION_REF,
        authenticated_at=now - timedelta(days=1),
        recent_auth_at=now,
    )


def _admitted() -> AdmittedSession:
    return AdmittedSession(
        principal=_principal(),
        expires_at=datetime(2026, 10, 1, 10, 0, tzinfo=UTC),
        csrf_token=SecretStr(_CSRF_TOKEN),
    )


def _issued() -> IssuedSession:
    return IssuedSession(
        principal=_principal(),
        expires_at=datetime(2026, 10, 1, 10, 0, tzinfo=UTC),
        session_secret=SecretStr("rotated-secret"),
        csrf_token=SecretStr("rotated-csrf"),
    )


def _request(*, csrf: bool = False) -> Request:
    headers: list[tuple[bytes, bytes]] = [
        (b"cookie", f"__Host-dante-session={_SESSION_SECRET}".encode("ascii")),
    ]
    if csrf:
        headers.append((b"x-dante-csrf", _CSRF_TOKEN.encode("ascii")))
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/v1/auth/methods",
            "headers": headers,
            "state": {"request_id": "test-request-id"},
        }
    )


class _AuthService:
    def __init__(self, admitted: AdmittedSession | None = None) -> None:
        self.admitted = admitted
        self.presented: list[str | None] = []

    async def admit_session(self, cookie_value: str | None) -> AdmittedSession | None:
        self.presented.append(cookie_value)
        return self.admitted


class _AuthenticatorService:
    def __init__(self) -> None:
        self.calls = 0

    async def authentication_methods(self, *, admitted: AdmittedSession) -> AuthenticationMethods:
        assert admitted.principal.account_ref == _ACCOUNT_REF
        self.calls += 1
        return AuthenticationMethods(
            password_established=True,
            providers=(
                AuthenticationProviderMethod(
                    external_identity_ref=_EXTERNAL_IDENTITY_REF,
                    provider_code="google",
                    provider_email_address="person@example.com",
                    provider_email_private=False,
                ),
            ),
            active_passkey_count=2,
            recovery_eligible_email_count=1,
        )


class _LifecycleService:
    session_cookie_max_age_seconds = 3600

    def __init__(
        self,
        *,
        issued: IssuedSession | None = None,
        removal_error: Exception | None = None,
    ) -> None:
        self.issued = issued or _issued()
        self.removal_error = removal_error
        self.establish_calls: list[tuple[UUID, str, str]] = []
        self.remove_calls: list[tuple[UUID, str]] = []

    async def establish_password(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
        new_password: str,
    ) -> IssuedSession:
        self.establish_calls.append(
            (
                admitted.principal.account_ref,
                presented_session_secret,
                new_password,
            )
        )
        return self.issued

    async def remove_password(
        self,
        *,
        admitted: AdmittedSession,
        presented_session_secret: str,
    ) -> IssuedSession:
        self.remove_calls.append(
            (admitted.principal.account_ref, presented_session_secret)
        )
        if self.removal_error is not None:
            raise self.removal_error
        return self.issued


@pytest.mark.asyncio
async def test_methods_returns_safe_account_wide_inventory() -> None:
    auth_service = _AuthService(_admitted())
    authenticator_service = _AuthenticatorService()

    result = await get_authentication_methods(
        _request(),
        Response(),
        auth_service,
        authenticator_service,
    )

    assert auth_service.presented == [_SESSION_SECRET]
    assert authenticator_service.calls == 1
    assert result.model_dump(mode="json") == {
        "password_established": True,
        "providers": [
            {
                "external_identity_ref": str(_EXTERNAL_IDENTITY_REF),
                "provider_code": "google",
                "provider_email_address": "person@example.com",
                "provider_email_private": False,
            }
        ],
        "active_passkey_count": 2,
        "recovery_eligible_email_count": 1,
    }


@pytest.mark.asyncio
async def test_methods_requires_an_admitted_server_session_and_clears_stale_cookie() -> None:
    response = Response()

    with pytest.raises(ProblemError) as error:
        await get_authentication_methods(
            _request(),
            response,
            _AuthService(),
            _AuthenticatorService(),
        )

    assert error.value.status == 401
    assert error.value.code == "auth.authentication_required"
    assert "__Host-dante-session=" in response.headers["set-cookie"]
    assert "Max-Age=0" in response.headers["set-cookie"]


@pytest.mark.asyncio
async def test_password_establishment_requires_session_bound_csrf_before_mutation() -> None:
    lifecycle = _LifecycleService()

    with pytest.raises(ProblemError) as error:
        await establish_password(
            PasswordEstablishRequest(new_password="correct horse battery staple"),
            _request(csrf=False),
            Response(),
            _AuthService(_admitted()),
            lifecycle,
        )

    assert error.value.status == 403
    assert error.value.code == "security.csrf_failed"
    assert lifecycle.establish_calls == []


@pytest.mark.asyncio
async def test_password_establishment_rotates_cookie_and_returns_authoritative_session() -> None:
    response = Response()
    lifecycle = _LifecycleService()

    result = await establish_password(
        PasswordEstablishRequest(new_password="correct horse battery staple"),
        _request(csrf=True),
        response,
        _AuthService(_admitted()),
        lifecycle,
    )

    assert lifecycle.establish_calls == [
        (_ACCOUNT_REF, _SESSION_SECRET, "correct horse battery staple")
    ]
    assert result.authenticated is True
    assert result.account_ref == _ACCOUNT_REF
    assert result.csrf_token == "rotated-csrf"
    set_cookie = response.headers["set-cookie"]
    assert "__Host-dante-session=rotated-secret" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "Secure" in set_cookie
    assert "SameSite=lax" in set_cookie


@pytest.mark.asyncio
async def test_password_removal_maps_anti_lockout_to_stable_conflict() -> None:
    lifecycle = _LifecycleService(removal_error=AuthenticatorRemovalBlockedError())

    with pytest.raises(ProblemError) as error:
        await remove_password(
            _request(csrf=True),
            Response(),
            _AuthService(_admitted()),
            lifecycle,
        )

    assert error.value.status == 409
    assert error.value.code == "auth.authenticator_removal_blocked"
    assert lifecycle.remove_calls == [(_ACCOUNT_REF, _SESSION_SECRET)]
