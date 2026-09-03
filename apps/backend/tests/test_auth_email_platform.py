"""Unit acceptance for Email Platform crypto, templates and SES transport semantics."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any, cast
from uuid import uuid7

import pytest
from botocore.exceptions import (  # type: ignore[import-untyped]
    ClientError,
    EndpointConnectionError,
)

import dante.auth.email_provider as email_provider_module
from dante.auth.email_contracts import (
    ClaimedEmailIntent,
    EmailPayloadError,
    ProviderMessage,
    ProviderOutcome,
)
from dante.auth.email_crypto import EmailPayloadCipher
from dante.auth.email_provider import SesEmailProvider
from dante.auth.email_render import render_claim
from dante.platform.config.auth import AuthSettings

_OLD_KEY = b"o" * 32
_NEW_KEY = b"n" * 32
_EMAIL_PROVIDER_MODULE = cast(Any, email_provider_module)


def _protected_claim(
    *,
    cipher: EmailPayloadCipher,
    payload: dict[str, str | int],
    purpose_code: str = "signup_verification",
    template_code: str = "auth.signup_verification",
    template_revision: str = "2",
) -> ClaimedEmailIntent:
    email_intent_ref = uuid7()
    protected = cipher.protect(
        email_intent_ref=email_intent_ref,
        purpose_code=purpose_code,
        template_code=template_code,
        template_revision=template_revision,
        payload=payload,
    )
    assert protected is not None
    return ClaimedEmailIntent(
        email_intent_ref=email_intent_ref,
        email_attempt_ref=uuid7(),
        claim_token=uuid7(),
        purpose_code=purpose_code,
        template_code=template_code,
        template_revision=template_revision,
        locale_code="en",
        recipient_address="user@example.com",
        recipient_comparison_key="user@example.com",
        sensitive_key_id=protected.key_id,
        sensitive_nonce=protected.nonce,
        sensitive_ciphertext=protected.ciphertext,
        attempt_number=1,
        expires_at=datetime.now(UTC) + timedelta(minutes=15),
    )


def test_payload_aad_binds_intent_purpose_template_and_revision() -> None:
    cipher = EmailPayloadCipher(key_ring={"old": _OLD_KEY}, current_key_id="old")
    claim = _protected_claim(
        cipher=cipher,
        payload={"code": "123456", "expires_minutes": 15},
    )

    assert cipher.unprotect(claim=claim) == {"code": "123456", "expires_minutes": 15}
    ciphertext = claim.sensitive_ciphertext
    assert ciphertext is not None

    mutated_claims = (
        replace(claim, email_intent_ref=uuid7()),
        replace(claim, purpose_code="provider_enrollment_verification"),
        replace(claim, template_code="auth.provider_enrollment_verification"),
        replace(claim, template_revision="3"),
        replace(claim, sensitive_ciphertext=ciphertext[:-1] + b"\x00"),
    )
    for mutated in mutated_claims:
        with pytest.raises(EmailPayloadError, match="authentication failed"):
            cipher.unprotect(claim=mutated)


def test_fingerprint_replay_survives_retained_key_rotation() -> None:
    old_cipher = EmailPayloadCipher(key_ring={"old": _OLD_KEY}, current_key_id="old")
    payload: dict[str, str | int] = {"code": "123456", "expires_minutes": 15}
    old_fingerprint = old_cipher.fingerprint(
        purpose_code="signup_verification",
        template_code="auth.signup_verification",
        template_revision="2",
        payload=payload,
    )

    rotated_cipher = EmailPayloadCipher(
        key_ring={"old": _OLD_KEY, "new": _NEW_KEY},
        current_key_id="new",
    )
    assert rotated_cipher.matches_fingerprint(
        old_fingerprint,
        purpose_code="signup_verification",
        template_code="auth.signup_verification",
        template_revision="2",
        payload=payload,
    )
    assert not rotated_cipher.matches_fingerprint(
        old_fingerprint,
        purpose_code="signup_verification",
        template_code="auth.signup_verification",
        template_revision="2",
        payload={"code": "654321", "expires_minutes": 15},
    )


def test_revision_two_renders_multipart_html_without_remote_tracking_content() -> None:
    cipher = EmailPayloadCipher(key_ring={"old": _OLD_KEY}, current_key_id="old")
    claim = _protected_claim(
        cipher=cipher,
        payload={"code": "<123&", "expires_minutes": 15},
    )

    message = render_claim(
        claim=claim,
        cipher=cipher,
        from_address="no-reply@example.com",
        canonical_web_origin="https://app.example.com",
    )

    assert "<123&" in message.text_body
    assert message.html_body is not None
    assert "&lt;123&amp;" in message.html_body
    assert "<123&" not in message.html_body
    assert "<img" not in message.html_body.lower()
    assert "tracking" not in message.html_body.lower()
    assert "http://" not in message.html_body.lower()
    assert "https://" not in message.html_body.lower()


def test_revision_one_remains_text_only_and_unknown_revision_fails_closed() -> None:
    cipher = EmailPayloadCipher(key_ring={"old": _OLD_KEY}, current_key_id="old")
    claim = _protected_claim(
        cipher=cipher,
        payload={"code": "123456", "expires_minutes": 15},
        template_revision="1",
    )

    message = render_claim(
        claim=claim,
        cipher=cipher,
        from_address="no-reply@example.com",
        canonical_web_origin="https://app.example.com",
    )
    assert message.html_body is None

    with pytest.raises(EmailPayloadError, match="unsupported template revision"):
        render_claim(
            claim=replace(claim, template_revision="unsupported"),
            cipher=cipher,
            from_address="no-reply@example.com",
            canonical_web_origin="https://app.example.com",
        )


class _FakeSesClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.response: dict[str, Any] = {"MessageId": "ses-message-1"}
        self.error: BaseException | None = None

    def send_email(self, **request: Any) -> dict[str, Any]:
        self.calls.append(request)
        if self.error is not None:
            raise self.error
        return self.response


def _ses_settings() -> AuthSettings:
    return cast(
        AuthSettings,
        SimpleNamespace(
            ses_region="eu-west-3",
            ses_configuration_set="dante-auth-security",
            email_provider_connect_timeout_seconds=2.0,
            email_provider_read_timeout_seconds=5.0,
        ),
    )


def _provider_message() -> ProviderMessage:
    return ProviderMessage(
        email_intent_ref=uuid7(),
        from_address="no-reply@example.com",
        to_address="user@example.com",
        subject="Security message",
        text_body="Plain text",
        html_body="<html><body>HTML</body></html>",
    )


@pytest.mark.asyncio
async def test_ses_config_has_one_total_sdk_attempt_and_request_has_no_tracking_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _FakeSesClient()
    captured: dict[str, Any] = {}

    def fake_client(service_name: str, **kwargs: Any) -> _FakeSesClient:
        captured["service_name"] = service_name
        captured.update(kwargs)
        return fake

    monkeypatch.setattr(_EMAIL_PROVIDER_MODULE.boto3, "client", fake_client)
    provider = SesEmailProvider(settings=_ses_settings())
    message = _provider_message()

    result = await provider.send(message)

    assert result.outcome is ProviderOutcome.ACCEPTED
    assert result.provider_message_id == "ses-message-1"
    assert len(fake.calls) == 1
    assert captured["service_name"] == "sesv2"
    assert captured["region_name"] == "eu-west-3"
    config = captured["config"]
    assert config.retries["total_max_attempts"] == 1

    request = fake.calls[0]
    assert set(request) == {
        "FromEmailAddress",
        "Destination",
        "Content",
        "EmailTags",
        "ConfigurationSetName",
    }
    assert set(request["Content"]["Simple"]["Body"]) == {"Text", "Html"}
    assert request["EmailTags"] == [
        {"Name": "dante_intent", "Value": str(message.email_intent_ref)},
        {"Name": "dante_stream", "Value": "auth_security"},
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("ThrottlingException", ProviderOutcome.RETRYABLE_FAILURE),
        ("MessageRejected", ProviderOutcome.DEFINITIVE_FAILURE),
        ("UnexpectedProviderCode", ProviderOutcome.AMBIGUOUS),
    ],
)
async def test_ses_classifies_known_and_unknown_provider_errors_without_retry(
    monkeypatch: pytest.MonkeyPatch,
    code: str,
    expected: ProviderOutcome,
) -> None:
    fake = _FakeSesClient()
    fake.error = ClientError(
        {"Error": {"Code": code, "Message": "safe test message"}},
        "SendEmail",
    )

    def fake_client(*_args: Any, **_kwargs: Any) -> _FakeSesClient:
        return fake

    monkeypatch.setattr(_EMAIL_PROVIDER_MODULE.boto3, "client", fake_client)
    provider = SesEmailProvider(settings=_ses_settings())

    result = await provider.send(_provider_message())

    assert result.outcome is expected
    assert result.safe_error_code == code
    assert len(fake.calls) == 1


@pytest.mark.asyncio
async def test_ses_transport_disconnect_is_ambiguous_and_never_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = _FakeSesClient()
    fake.error = EndpointConnectionError(endpoint_url="https://email.eu-west-3.amazonaws.com")

    def fake_client(*_args: Any, **_kwargs: Any) -> _FakeSesClient:
        return fake

    monkeypatch.setattr(_EMAIL_PROVIDER_MODULE.boto3, "client", fake_client)
    provider = SesEmailProvider(settings=_ses_settings())

    result = await provider.send(_provider_message())

    assert result.outcome is ProviderOutcome.AMBIGUOUS
    assert result.safe_error_code == "EndpointConnectionError"
    assert len(fake.calls) == 1
