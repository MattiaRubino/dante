"""Focused M5-D Sign in with Apple protocol/trust-boundary tests."""

from __future__ import annotations

import json
from base64 import urlsafe_b64encode
from datetime import UTC, datetime
from typing import cast

import pytest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from joserfc import jwt
from joserfc.jwk import ECKey
from pydantic import SecretStr

from dante.auth.apple import (
    AppleClientSecretSigner,
    AppleNotificationVerifier,
    AppleProofError,
    AppleTokenVerifier,
    apple_code_hash,
    build_apple_authorization_url,
    parse_apple_authorization_profile,
)
from dante.auth.proofs import FlowProofPurpose, issue_flow_proof
from dante.auth.provider_runtime import ProviderRuntime, ProviderRuntimeError
from dante.platform.config.auth_provider import (
    APPLE_ISSUER,
    AppleProviderSettings,
    AuthProviderSettings,
)

_CLIENT_ID = "com.dante.web"
_TEAM_ID = "ABCDE12345"
_KEY_ID = "APPLEKEY01"
_KID = "apple-rsa-test-key"
_NOW = datetime(2026, 8, 31, 9, 0, tzinfo=UTC)


def _b64url(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _segment(value: dict[str, object]) -> str:
    return _b64url(json.dumps(value, separators=(",", ":"), sort_keys=True).encode())


def _unsigned_integer(value: int) -> str:
    size = max(1, (value.bit_length() + 7) // 8)
    return _b64url(value.to_bytes(size, "big"))


def _public_jwk(private_key: rsa.RSAPrivateKey) -> dict[str, object]:
    numbers = private_key.public_key().public_numbers()
    return {
        "kty": "RSA",
        "kid": _KID,
        "use": "sig",
        "alg": "RS256",
        "n": _unsigned_integer(numbers.n),
        "e": _unsigned_integer(numbers.e),
    }


def _signed_token(private_key: rsa.RSAPrivateKey, claims: dict[str, object]) -> str:
    header = _segment({"alg": "RS256", "kid": _KID, "typ": "JWT"})
    payload = _segment(claims)
    signing_input = f"{header}.{payload}".encode("ascii")
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{header}.{payload}.{_b64url(signature)}"


class _StubProviderRuntime:
    def __init__(self, jwk: dict[str, object], *, fail: bool = False) -> None:
        self._jwk = jwk
        self._fail = fail
        self.requests: list[tuple[str, str]] = []

    async def jwk_for_kid(self, *, provider: str, kid: str) -> dict[str, object]:
        self.requests.append((provider, kid))
        if self._fail:
            raise ProviderRuntimeError("provider unavailable")
        return dict(self._jwk)


def _provider_settings(*, private_key_pem: str = "placeholder-p8") -> AuthProviderSettings:
    return AuthProviderSettings(
        apple=AppleProviderSettings(
            enabled=True,
            client_id=_CLIENT_ID,
            team_id=_TEAM_ID,
            key_id=_KEY_ID,
            client_private_key_pem=SecretStr(private_key_pem),
            redirect_uri="https://auth.dante.example/api/v1/auth/apple/callback",
            grant_encryption_current_key_id="v1",
            grant_encryption_keys={"v1": SecretStr(_b64url(b"g" * 32))},
        )
    )


def _claims(nonce: str, code: str, **overrides: object) -> dict[str, object]:
    claims: dict[str, object] = {
        "iss": APPLE_ISSUER,
        "sub": "apple-subject-123",
        "aud": _CLIENT_ID,
        "exp": int(_NOW.timestamp()) + 600,
        "iat": int(_NOW.timestamp()) - 30,
        "nonce": nonce,
        "c_hash": apple_code_hash(code),
        "email": "person@example.com",
        "email_verified": True,
        "is_private_email": False,
    }
    claims.update(overrides)
    return claims


@pytest.mark.asyncio
async def test_valid_apple_id_token_binds_nonce_code_and_signed_mailbox() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    code = "single-use-code"
    runtime = _StubProviderRuntime(_public_jwk(private_key))
    verifier = AppleTokenVerifier(
        settings=_provider_settings(),
        provider_runtime=cast(ProviderRuntime, runtime),
        now=lambda: _NOW,
    )

    evidence = await verifier.verify(
        _signed_token(private_key, _claims(nonce.secret.get_secret_value(), code)),
        expected_nonce_verifier=nonce.verifier,
        expected_code=code,
    )

    assert evidence.issuer == APPLE_ISSUER
    assert evidence.subject == "apple-subject-123"
    assert evidence.email is not None
    assert evidence.email.comparison_key == "person@example.com"
    assert evidence.email_verified is True
    assert evidence.mailbox_authoritative is True
    assert runtime.requests == [("apple", _KID)]


@pytest.mark.asyncio
@pytest.mark.parametrize("domain", ["privaterelay.appleid.com", "private.icloud.com"])
async def test_both_sign_in_with_apple_private_mail_domains_are_recognized(domain: str) -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    code = "relay-code"
    verifier = AppleTokenVerifier(
        settings=_provider_settings(),
        provider_runtime=cast(ProviderRuntime, _StubProviderRuntime(_public_jwk(private_key))),
        now=lambda: _NOW,
    )

    evidence = await verifier.verify(
        _signed_token(
            private_key,
            _claims(
                nonce.secret.get_secret_value(),
                code,
                email=f"opaque@{domain}",
                email_verified="true",
                is_private_email=None,
            ),
        ),
        expected_nonce_verifier=nonce.verifier,
        expected_code=code,
    )

    assert evidence.email_private is True
    assert evidence.mailbox_authoritative is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("claim", "value"),
    [
        ("iss", "https://evil.example"),
        ("aud", "other-service"),
        ("sub", "  "),
        ("exp", int(_NOW.timestamp()) - 1),
        ("email_verified", "TRUE"),
        ("is_private_email", 1),
    ],
)
async def test_invalid_apple_claims_are_rejected(claim: str, value: object) -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    code = "claim-code"
    verifier = AppleTokenVerifier(
        settings=_provider_settings(),
        provider_runtime=cast(ProviderRuntime, _StubProviderRuntime(_public_jwk(private_key))),
        now=lambda: _NOW,
    )

    with pytest.raises(AppleProofError):
        await verifier.verify(
            _signed_token(
                private_key,
                _claims(nonce.secret.get_secret_value(), code, **{claim: value}),
            ),
            expected_nonce_verifier=nonce.verifier,
            expected_code=code,
        )


@pytest.mark.asyncio
async def test_wrong_nonce_and_wrong_c_hash_are_rejected_before_exchange() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    expected = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    other = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    verifier = AppleTokenVerifier(
        settings=_provider_settings(),
        provider_runtime=cast(ProviderRuntime, _StubProviderRuntime(_public_jwk(private_key))),
        now=lambda: _NOW,
    )

    with pytest.raises(AppleProofError, match="nonce"):
        await verifier.verify(
            _signed_token(private_key, _claims(other.secret.get_secret_value(), "code")),
            expected_nonce_verifier=expected.verifier,
            expected_code="code",
        )

    with pytest.raises(AppleProofError, match="c_hash"):
        await verifier.verify(
            _signed_token(private_key, _claims(expected.secret.get_secret_value(), "different")),
            expected_nonce_verifier=expected.verifier,
            expected_code="code",
        )


def test_authorization_url_is_exact_form_post_code_id_token_request() -> None:
    settings = _provider_settings()
    result = build_apple_authorization_url(settings=settings, state="state123", nonce="nonce123")

    assert result.startswith("https://appleid.apple.com/auth/authorize?")
    assert "response_type=code+id_token" in result
    assert "response_mode=form_post" in result
    assert "scope=name+email" in result
    assert "state=state123" in result
    assert "nonce=nonce123" in result
    assert (
        "redirect_uri=https%3A%2F%2Fauth.dante.example%2Fapi%2Fv1%2Fauth%2Fapple%2Fcallback"
        in result
    )


def test_one_shot_profile_is_sanitized_and_unknown_members_fail_closed() -> None:
    profile = parse_apple_authorization_profile(
        json.dumps(
            {
                "name": {"firstName": "  Ada  ", "lastName": "  Lovelace  "},
                "email": "Ada@example.com",
            }
        )
    )
    assert profile is not None
    assert profile.given_name == "Ada"
    assert profile.family_name == "Lovelace"
    assert profile.display_name == "Ada Lovelace"
    assert profile.email is not None
    assert profile.email.comparison_key == "ada@example.com"

    with pytest.raises(AppleProofError, match="unexpected"):
        parse_apple_authorization_profile(json.dumps({"email": "a@example.com", "role": "admin"}))


def test_client_secret_is_short_lived_es256_and_exactly_scoped() -> None:
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("ascii")
    public_pem = (
        private_key.public_key()
        .public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode("ascii")
    )
    signer = AppleClientSecretSigner(
        team_id=_TEAM_ID,
        key_id=_KEY_ID,
        client_id=_CLIENT_ID,
        private_key_pem=SecretStr(private_pem),
        now=lambda: _NOW,
    )

    encoded = signer.issue().get_secret_value()
    token = jwt.decode(encoded, ECKey.import_key(public_pem), algorithms=["ES256"])

    assert token.header["alg"] == "ES256"
    assert token.header["kid"] == _KEY_ID
    assert token.claims["iss"] == _TEAM_ID
    assert token.claims["aud"] == APPLE_ISSUER
    assert token.claims["sub"] == _CLIENT_ID
    assert token.claims["exp"] - token.claims["iat"] == 300


@pytest.mark.asyncio
async def test_notification_verification_normalizes_known_event() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    runtime = _StubProviderRuntime(_public_jwk(private_key))
    verifier = AppleNotificationVerifier(
        settings=_provider_settings(),
        provider_runtime=cast(ProviderRuntime, runtime),
        now=lambda: _NOW,
    )
    claims = {
        "iss": APPLE_ISSUER,
        "aud": _CLIENT_ID,
        "iat": int(_NOW.timestamp()) - 10,
        "jti": "notification-123",
        "events": {
            "type": "email-disabled",
            "sub": "apple-subject-123",
            "email": "opaque@private.icloud.com",
            "is_private_email": True,
            "event_time": int(_NOW.timestamp()) - 5,
        },
    }

    event = await verifier.verify_notification(_signed_token(private_key, claims))

    assert event.known is True
    assert event.event_type == "email-disabled"
    assert event.email is not None
    assert event.email_private is True
