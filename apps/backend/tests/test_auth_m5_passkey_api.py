"""Focused public M5 passkey HTTP-contract proof."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID

import pytest
from fastapi import Request, Response
from pydantic import SecretStr, ValidationError

from dante.auth.contracts import AdmittedSession, IssuedSession, PasskeyCeremonyBegun, Principal
from dante.auth.m5_passkey_api import (
    AssertionCredential,
    PasskeyAuthenticationCompleteRequest,
    PasskeyBeginRequest,
    PasskeyRegistrationCompleteRequest,
    PasskeyUpdateRequest,
    RegistrationCredential,
    begin_passkey_authentication,
    begin_passkey_registration,
    complete_passkey_authentication,
    complete_passkey_registration,
    update_passkey,
)
from dante.auth.provider_flow_runtime import ProviderFlowRuntime
from dante.platform.http.problem import ProblemError

_ACCOUNT_REF = UUID("00000000-0000-4000-8000-000000000201")
_SESSION_REF = UUID("00000000-0000-4000-8000-000000000202")
_CHALLENGE_REF = UUID("00000000-0000-4000-8000-000000000203")
_PASSKEY_REF = UUID("00000000-0000-4000-8000-000000000204")
_ORIGIN = "https://dante.test"


def _value(label: str) -> str:
    return f"dante-passkey-test-{label}-{_ACCOUNT_REF.hex}"


_SESSION_SECRET = _value("session")
_CSRF_TOKEN = _value("csrf")
_ROTATED_SESSION_SECRET = _value("rotated-session")
_ROTATED_CSRF = _value("rotated-csrf")


def _now() -> datetime:
    return datetime(2026, 9, 1, 15, 0, tzinfo=UTC)


def _admitted() -> AdmittedSession:
    now = _now()
    return AdmittedSession(
        principal=Principal(
            account_ref=_ACCOUNT_REF,
            auth_session_ref=_SESSION_REF,
            authenticated_at=now - timedelta(hours=1),
            recent_auth_at=now,
        ),
        expires_at=now + timedelta(hours=2),
        csrf_token=SecretStr(_CSRF_TOKEN),
    )


def _issued() -> IssuedSession:
    admitted = _admitted()
    return IssuedSession(
        principal=admitted.principal,
        expires_at=admitted.expires_at,
        session_secret=SecretStr(_ROTATED_SESSION_SECRET),
        csrf_token=SecretStr(_ROTATED_CSRF),
    )


def _request(*, session: bool = False, csrf: bool = False) -> Request:
    headers: list[tuple[bytes, bytes]] = [(b"origin", _ORIGIN.encode("ascii"))]
    if session:
        headers.append((b"cookie", f"__Host-dante-session={_SESSION_SECRET}".encode("ascii")))
    if csrf:
        headers.append((b"x-dante-csrf", _CSRF_TOKEN.encode("ascii")))
    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/auth/passkeys/test",
            "headers": headers,
            "client": ("127.0.0.1", 12345),
            "state": {"request_id": "test-request-id"},
        }
    )


def _registration() -> RegistrationCredential:
    return RegistrationCredential.model_validate(
        {
            "id": "credential-id",
            "rawId": "credential-id",
            "type": "public-key",
            "response": {
                "clientDataJSON": "Y2xpZW50LWRhdGE",
                "attestationObject": "YXR0ZXN0YXRpb24",
            },
            "clientExtensionResults": {},
        }
    )


def _assertion() -> AssertionCredential:
    return AssertionCredential.model_validate(
        {
            "id": "credential-id",
            "rawId": "credential-id",
            "type": "public-key",
            "response": {
                "clientDataJSON": "Y2xpZW50LWRhdGE",
                "authenticatorData": "YXV0aGVudGljYXRvcg",
                "signature": "c2lnbmF0dXJl",
                "userHandle": "dXNlci1oYW5kbGU",
            },
            "clientExtensionResults": {},
        }
    )


class _AuthService:
    session_cookie_max_age_seconds = 3600

    def __init__(self, admitted: AdmittedSession | None = None) -> None:
        self.admitted = admitted

    async def admit_session(self, cookie_value: str | None) -> AdmittedSession | None:
        if self.admitted is not None:
            assert cookie_value == _SESSION_SECRET
        return self.admitted


class _PasskeyService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    async def begin_authentication(self, **kwargs: Any) -> PasskeyCeremonyBegun:
        self.calls.append(("begin_authentication", kwargs))
        return PasskeyCeremonyBegun(
            webauthn_challenge_ref=_CHALLENGE_REF,
            options={"publicKey": {"challenge": "challenge"}},
            expires_at=_now() + timedelta(minutes=5),
        )

    async def begin_registration(self, **kwargs: Any) -> PasskeyCeremonyBegun:
        self.calls.append(("begin_registration", kwargs))
        return PasskeyCeremonyBegun(
            webauthn_challenge_ref=_CHALLENGE_REF,
            options={"publicKey": {"challenge": "challenge"}},
            expires_at=_now() + timedelta(minutes=5),
        )

    async def complete_authentication(self, **kwargs: Any) -> IssuedSession:
        self.calls.append(("complete_authentication", kwargs))
        return _issued()

    async def complete_registration(self, **kwargs: Any) -> IssuedSession:
        self.calls.append(("complete_registration", kwargs))
        return _issued()

    async def update_label(self, **kwargs: Any) -> None:
        self.calls.append(("update_label", kwargs))


def _runtime(passkey: _PasskeyService) -> ProviderFlowRuntime:
    runtime = type("Runtime", (), {"passkey_service": passkey})()
    return cast(ProviderFlowRuntime, runtime)


def _set_cookies(response: Response) -> list[str]:
    return [
        value.decode("latin-1")
        for name, value in response.raw_headers
        if name.lower() == b"set-cookie"
    ]


def test_webauthn_wire_models_fail_closed_on_unknown_or_invalid_fields() -> None:
    valid = _registration().model_dump(mode="json", by_alias=True)
    assert valid["rawId"] == "credential-id"
    assert valid["type"] == "public-key"

    with pytest.raises(ValidationError):
        RegistrationCredential.model_validate(
            {
                **valid,
                "providerSubject": "must-not-be-admitted",
            }
        )
    with pytest.raises(ValidationError):
        AssertionCredential.model_validate(
            {
                "id": "credential=id",
                "rawId": "credential=id",
                "type": "public-key",
                "response": {
                    "clientDataJSON": "Y2xpZW50",
                    "authenticatorData": "YXV0aA",
                    "signature": "c2ln",
                },
            }
        )


@pytest.mark.asyncio
async def test_anonymous_passkey_authentication_begin_uses_exact_request_origin() -> None:
    passkey = _PasskeyService()

    result = await begin_passkey_authentication(
        PasskeyBeginRequest(),
        _request(),
        _runtime(passkey),
    )

    assert result.webauthn_challenge_ref == _CHALLENGE_REF
    name, kwargs = passkey.calls[0]
    assert name == "begin_authentication"
    assert kwargs["expected_origin"] == _ORIGIN
    assert kwargs["source_context"] == "127.0.0.1"


@pytest.mark.asyncio
async def test_registration_begin_requires_session_bound_csrf_before_service_call() -> None:
    passkey = _PasskeyService()

    with pytest.raises(ProblemError) as error:
        await begin_passkey_registration(
            PasskeyBeginRequest(),
            _request(session=True, csrf=False),
            Response(),
            _AuthService(_admitted()),
            _runtime(passkey),
        )

    assert error.value.status == 403
    assert error.value.code == "security.csrf_failed"
    assert passkey.calls == []


@pytest.mark.asyncio
async def test_registration_complete_passes_bounded_wire_shape_and_rotates_session() -> None:
    passkey = _PasskeyService()
    response = Response()
    payload = PasskeyRegistrationCompleteRequest(
        webauthn_challenge_ref=_CHALLENGE_REF,
        response=_registration(),
        label="Work laptop",
        transports=("internal",),
    )

    result = await complete_passkey_registration(
        payload,
        _request(session=True, csrf=True),
        response,
        _AuthService(_admitted()),
        _runtime(passkey),
    )

    assert result.authenticated is True
    name, kwargs = passkey.calls[0]
    assert name == "complete_registration"
    assert kwargs["webauthn_challenge_ref"] == _CHALLENGE_REF
    assert kwargs["label"] == "Work laptop"
    assert kwargs["transports"] == ("internal",)
    assert kwargs["response"]["rawId"] == "credential-id"
    assert any(
        f"__Host-dante-session={_ROTATED_SESSION_SECRET}" in cookie
        for cookie in _set_cookies(response)
    )


@pytest.mark.asyncio
async def test_passkey_authentication_completion_establishes_canonical_session_cookie() -> None:
    passkey = _PasskeyService()
    response = Response()

    result = await complete_passkey_authentication(
        PasskeyAuthenticationCompleteRequest(
            webauthn_challenge_ref=_CHALLENGE_REF,
            response=_assertion(),
        ),
        _request(),
        response,
        _AuthService(),
        _runtime(passkey),
    )

    assert result.account_ref == _ACCOUNT_REF
    name, kwargs = passkey.calls[0]
    assert name == "complete_authentication"
    assert kwargs["response"]["response"]["userHandle"] == "dXNlci1oYW5kbGU"
    cookies = _set_cookies(response)
    assert any(f"__Host-dante-session={_ROTATED_SESSION_SECRET}" in cookie for cookie in cookies)
    assert any("HttpOnly" in cookie and "Secure" in cookie for cookie in cookies)


@pytest.mark.asyncio
async def test_passkey_label_update_is_csrf_protected_and_label_only() -> None:
    passkey = _PasskeyService()

    await update_passkey(
        _PASSKEY_REF,
        PasskeyUpdateRequest(label="Security key"),
        _request(session=True, csrf=True),
        Response(),
        _AuthService(_admitted()),
        _runtime(passkey),
    )

    name, kwargs = passkey.calls[0]
    assert name == "update_label"
    assert kwargs == {
        "admitted": _admitted(),
        "presented_session_secret": _SESSION_SECRET,
        "passkey_credential_ref": _PASSKEY_REF,
        "label": "Security key",
    }
