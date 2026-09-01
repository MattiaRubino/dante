"""Focused public M5 provider/continuation HTTP-contract proof."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID

import pytest
from fastapi import Request, Response
from pydantic import SecretStr
from starlette.types import Message

from dante.auth.contracts import (
    AdmittedSession,
    IssuedSession,
    Principal,
    ProviderAuthenticated,
    ProviderEnrollmentRequired,
    ProviderLinkRequired,
    ProviderReturnTarget,
)
from dante.auth.m5_provider_api import (
    AppleNotificationRequest,
    GoogleAuthenticationCompleteRequest,
    ProviderLinkConfirmRequest,
    _parse_apple_form,
    complete_google_authentication,
    confirm_provider_link,
    get_provider_enrollment,
    handle_apple_callback,
    process_apple_notification,
)
from dante.auth.provider_continuation import (
    ProviderEnrollmentContinuation,
    ProviderLinkContinuation,
)
from dante.auth.provider_flow_runtime import ProviderFlowRuntime
from dante.platform.http.problem import ProblemError

_ACCOUNT_REF = UUID("00000000-0000-4000-8000-000000000101")
_SESSION_REF = UUID("00000000-0000-4000-8000-000000000102")
_TRANSACTION_REF = UUID("00000000-0000-4000-8000-000000000103")
_SIGNUP_REF = UUID("00000000-0000-4000-8000-000000000104")
_LINK_REF = UUID("00000000-0000-4000-8000-000000000105")


def _value(label: str) -> str:
    return f"dante-provider-test-{label}-{_ACCOUNT_REF.hex}"


_SESSION_SECRET = _value("session")
_CSRF_TOKEN = _value("csrf")
_ROTATED_SESSION_SECRET = _value("rotated-session")
_ROTATED_CSRF = _value("rotated-csrf")
_LINK_SECRET = _value("link")
_ENROLLMENT_SECRET = _value("enrollment")


def _now() -> datetime:
    return datetime(2026, 9, 1, 14, 0, tzinfo=UTC)


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


def _request(
    *,
    cookies: tuple[tuple[str, str], ...] = (),
    csrf: bool = False,
    body: bytes = b"",
    content_type: str = "application/json",
) -> Request:
    headers: list[tuple[bytes, bytes]] = [(b"content-type", content_type.encode("ascii"))]
    if cookies:
        headers.append(
            (
                b"cookie",
                "; ".join(f"{name}={value}" for name, value in cookies).encode("ascii"),
            )
        )
    if csrf:
        headers.append((b"x-dante-csrf", _CSRF_TOKEN.encode("ascii")))
    messages = [{"type": "http.request", "body": body, "more_body": False}]

    async def receive() -> Message:
        if messages:
            return cast(Message, messages.pop(0))
        return {"type": "http.disconnect"}

    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/auth/test",
            "headers": headers,
            "client": ("127.0.0.1", 12345),
            "state": {"request_id": "test-request-id"},
        },
        receive,
    )


def _set_cookies(response: Response) -> list[str]:
    return [
        value.decode("latin-1")
        for name, value in response.raw_headers
        if name.lower() == b"set-cookie"
    ]


class _AuthService:
    session_cookie_max_age_seconds = 3600

    def __init__(self, admitted: AdmittedSession | None = None) -> None:
        self.admitted = admitted

    async def admit_session(self, cookie_value: str | None) -> AdmittedSession | None:
        assert cookie_value == _SESSION_SECRET if self.admitted is not None else True
        return self.admitted


class _ContinuationService:
    def __init__(self, provider_code: str = "google") -> None:
        self.provider_code = provider_code

    async def resolve_enrollment(self, secret: str) -> ProviderEnrollmentContinuation:
        assert secret == _ENROLLMENT_SECRET
        return ProviderEnrollmentContinuation(
            external_signup_ref=_SIGNUP_REF,
            provider_code=self.provider_code,
            expires_at=_now() + timedelta(minutes=10),
        )

    async def resolve_link(self, secret: str) -> ProviderLinkContinuation:
        assert secret == _LINK_SECRET
        return ProviderLinkContinuation(
            external_link_challenge_ref=_LINK_REF,
            provider_code=self.provider_code,
            expires_at=_now() + timedelta(minutes=10),
        )

    async def resolve_apple_return_target(self, state: str) -> ProviderReturnTarget:
        assert state == "apple-state"
        return ProviderReturnTarget.SECURITY


class _GoogleService:
    def __init__(self, result: Any | None = None) -> None:
        self.result = result
        self.inspect_calls = 0

    async def complete_google(self, **kwargs: Any) -> Any:
        assert kwargs["external_auth_transaction_ref"] == _TRANSACTION_REF
        assert kwargs["state"] == "google-state"
        assert kwargs["credential"] == "google-credential"
        return self.result

    async def inspect_provider_enrollment(self, **_kwargs: Any) -> ProviderEnrollmentRequired:
        self.inspect_calls += 1
        raise AssertionError("Google enrollment inspector must not handle Apple continuation")


class _AppleService:
    def __init__(self, result: Any | None = None) -> None:
        self.result = result
        self.inspect_calls = 0
        self.notifications: list[str] = []

    async def inspect_provider_enrollment(self, **kwargs: Any) -> ProviderEnrollmentRequired:
        self.inspect_calls += 1
        assert kwargs["external_signup_ref"] == _SIGNUP_REF
        assert kwargs["continuation_secret"] == _ENROLLMENT_SECRET
        return ProviderEnrollmentRequired(
            external_signup_ref=_SIGNUP_REF,
            continuation_secret=SecretStr(_ENROLLMENT_SECRET),
            expires_at=_now() + timedelta(minutes=10),
            email_address="person@example.com",
            verification_expires_at=_now() + timedelta(minutes=5),
        )

    async def complete_apple(self, **kwargs: Any) -> Any:
        assert kwargs["state"] == "apple-state"
        assert kwargs["code"] == "apple-code"
        assert kwargs["id_token"] == "apple-id-token"
        return self.result

    async def process_notification(self, token: str) -> bool:
        self.notifications.append(token)
        return True


class _AuthenticatorService:
    def __init__(self) -> None:
        self.confirm_calls: list[tuple[UUID, str]] = []

    async def confirm_provider_link(self, **kwargs: Any) -> IssuedSession:
        assert kwargs["admitted"].principal.account_ref == _ACCOUNT_REF
        assert kwargs["presented_session_secret"] == _SESSION_SECRET
        self.confirm_calls.append(
            (kwargs["external_link_challenge_ref"], kwargs["continuation_secret"])
        )
        return _issued()


def _runtime(
    *,
    google: Any | None = None,
    apple: Any | None = None,
    continuation: Any | None = None,
    authenticator: Any | None = None,
) -> ProviderFlowRuntime:
    runtime = type(
        "Runtime",
        (),
        {
            "service": google,
            "apple_service": apple,
            "continuation_service": continuation or _ContinuationService(),
            "authenticator_service": authenticator or _AuthenticatorService(),
            "passkey_service": None,
        },
    )()
    return cast(ProviderFlowRuntime, runtime)


@pytest.mark.asyncio
async def test_google_link_required_uses_http_only_flow_cookie_not_json_secret() -> None:
    result = ProviderLinkRequired(
        external_link_challenge_ref=_LINK_REF,
        continuation_secret=SecretStr(_LINK_SECRET),
        expires_at=_now() + timedelta(minutes=10),
    )
    response = Response()

    payload = GoogleAuthenticationCompleteRequest(
        external_auth_transaction_ref=_TRANSACTION_REF,
        state="google-state",
        credential="google-credential",
    )
    wire = await complete_google_authentication(
        payload,
        _request(),
        response,
        _AuthService(),
        _runtime(google=_GoogleService(result)),
    )

    body = wire.model_dump(mode="json")
    assert body == {
        "outcome": "link_required",
        "external_link_challenge_ref": str(_LINK_REF),
        "expires_at": "2026-09-01T14:10:00Z",
    }
    assert "continuation" not in repr(body)
    cookies = _set_cookies(response)
    assert any(f"__Host-dante-provider-link={_LINK_SECRET}" in cookie for cookie in cookies)
    assert any(
        "HttpOnly" in cookie and "Secure" in cookie and "SameSite=lax" in cookie
        for cookie in cookies
    )


@pytest.mark.asyncio
async def test_enrollment_cookie_dispatches_to_apple_without_provider_metadata_in_cookie() -> None:
    apple = _AppleService()
    google = _GoogleService()
    request = _request(
        cookies=(("__Host-dante-provider-enrollment", _ENROLLMENT_SECRET),),
    )

    result = await get_provider_enrollment(
        request,
        _runtime(
            google=google,
            apple=apple,
            continuation=_ContinuationService(provider_code="apple"),
        ),
    )

    assert result.outcome == "enrollment_required"
    assert result.external_signup_ref == _SIGNUP_REF
    assert apple.inspect_calls == 1
    assert google.inspect_calls == 0


@pytest.mark.asyncio
async def test_provider_link_confirmation_requires_session_csrf_and_rotates_bearer() -> None:
    authenticator = _AuthenticatorService()
    runtime = _runtime(
        continuation=_ContinuationService(provider_code="google"),
        authenticator=authenticator,
    )
    response = Response()
    request = _request(
        cookies=(
            ("__Host-dante-session", _SESSION_SECRET),
            ("__Host-dante-provider-link", _LINK_SECRET),
        ),
        csrf=True,
    )

    result = await confirm_provider_link(
        ProviderLinkConfirmRequest(),
        request,
        response,
        _AuthService(_admitted()),
        runtime,
    )

    assert result.outcome == "authenticated"
    assert result.auth_session_ref == _SESSION_REF
    assert authenticator.confirm_calls == [(_LINK_REF, _LINK_SECRET)]
    cookies = _set_cookies(response)
    assert any(f"__Host-dante-session={_ROTATED_SESSION_SECRET}" in cookie for cookie in cookies)
    assert any(
        "__Host-dante-provider-link=" in cookie and "Max-Age=0" in cookie for cookie in cookies
    )


@pytest.mark.asyncio
async def test_provider_link_confirmation_rejects_missing_csrf_before_application_mutation() -> (
    None
):
    authenticator = _AuthenticatorService()
    request = _request(
        cookies=(
            ("__Host-dante-session", _SESSION_SECRET),
            ("__Host-dante-provider-link", _LINK_SECRET),
        ),
        csrf=False,
    )

    with pytest.raises(ProblemError) as error:
        await confirm_provider_link(
            ProviderLinkConfirmRequest(),
            request,
            Response(),
            _AuthService(_admitted()),
            _runtime(authenticator=authenticator),
        )

    assert error.value.status == 403
    assert error.value.code == "security.csrf_failed"
    assert authenticator.confirm_calls == []


def test_apple_form_post_parser_rejects_duplicate_and_unknown_fields() -> None:
    assert _parse_apple_form(b"state=opaque&code=code&id_token=token") == {
        "state": "opaque",
        "code": "code",
        "id_token": "token",
        "user": None,
        "error": None,
    }
    for body in (
        b"state=first&state=second",
        b"state=opaque&unexpected=value",
        b"code=missing-state",
    ):
        with pytest.raises(ProblemError) as error:
            _parse_apple_form(body)
        assert error.value.code == "request.malformed"


@pytest.mark.asyncio
async def test_apple_callback_redirects_only_to_fixed_server_resolved_target() -> None:
    apple = _AppleService(result=ProviderAuthenticated(session=_issued()))
    request = _request(
        body=b"state=apple-state&code=apple-code&id_token=apple-id-token",
        content_type="application/x-www-form-urlencoded",
    )

    response = await handle_apple_callback(
        request,
        _AuthService(),
        _runtime(apple=apple, continuation=_ContinuationService(provider_code="apple")),
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/security"
    assert any(
        f"__Host-dante-session={_ROTATED_SESSION_SECRET}" in cookie
        for cookie in _set_cookies(response)
    )


@pytest.mark.asyncio
async def test_apple_notification_boundary_passes_only_signed_envelope_to_verifier() -> None:
    apple = _AppleService()

    await process_apple_notification(
        AppleNotificationRequest(payload="signed-apple-jws"),
        _runtime(apple=apple),
    )

    assert apple.notifications == ["signed-apple-jws"]
