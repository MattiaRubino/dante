"""Focused M5-C Google OIDC trust-boundary tests."""

from __future__ import annotations

import json
from base64 import urlsafe_b64encode
from datetime import UTC, datetime
from typing import cast

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from dante.auth.google import (
    GoogleIdentityEvidence,
    GoogleProofError,
    GoogleProviderUnavailableError,
    GoogleTokenVerifier,
)
from dante.auth.proofs import FlowProofPurpose, issue_flow_proof
from dante.auth.provider_runtime import ProviderRuntime, ProviderRuntimeError
from dante.platform.config.auth_provider import (
    GOOGLE_ISSUER,
    AuthProviderSettings,
    GoogleProviderSettings,
)

_CLIENT_ID = "dante-google-client.apps.googleusercontent.com"
_KID = "google-test-key"
_NOW = datetime(2026, 8, 30, 18, 0, tzinfo=UTC)


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


def _signed_token(
    private_key: rsa.RSAPrivateKey,
    claims: dict[str, object],
) -> str:
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


def _settings() -> AuthProviderSettings:
    return AuthProviderSettings(
        google=GoogleProviderSettings(enabled=True, client_id=_CLIENT_ID),
    )


def _claims(nonce: str, **overrides: object) -> dict[str, object]:
    claims: dict[str, object] = {
        "iss": GOOGLE_ISSUER,
        "sub": "google-subject-123",
        "aud": _CLIENT_ID,
        "exp": int(_NOW.timestamp()) + 600,
        "iat": int(_NOW.timestamp()) - 60,
        "nonce": nonce,
        "email": "person@gmail.com",
        "email_verified": True,
        "name": "Example Person",
        "given_name": "Example",
        "family_name": "Person",
        "picture": "https://lh3.googleusercontent.com/avatar",
        "locale": "en-US",
    }
    claims.update(overrides)
    return claims


async def _verify(
    *,
    claims: dict[str, object],
    private_key: rsa.RSAPrivateKey,
    nonce_verifier: bytes,
    runtime: _StubProviderRuntime | None = None,
) -> GoogleIdentityEvidence:
    provider_runtime = runtime or _StubProviderRuntime(_public_jwk(private_key))
    verifier = GoogleTokenVerifier(
        settings=_settings(),
        provider_runtime=cast(ProviderRuntime, provider_runtime),
        now=lambda: _NOW,
    )
    return await verifier.verify(
        _signed_token(private_key, claims),
        expected_nonce_verifier=nonce_verifier,
    )


@pytest.mark.asyncio
async def test_valid_gmail_token_normalizes_identity_and_bootstrap() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    evidence = await _verify(
        claims=_claims(nonce.secret.get_secret_value()),
        private_key=private_key,
        nonce_verifier=nonce.verifier,
    )

    assert evidence.issuer == GOOGLE_ISSUER
    assert evidence.subject == "google-subject-123"
    assert evidence.email is not None
    assert evidence.email.comparison_key == "person@gmail.com"
    assert evidence.mailbox_authoritative is True
    assert evidence.display_name == "Example Person"
    assert evidence.picture_url == "https://lh3.googleusercontent.com/avatar"


@pytest.mark.asyncio
async def test_gmail_suffix_is_google_authoritative_without_relying_on_email_verified() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    evidence = await _verify(
        claims=_claims(nonce.secret.get_secret_value(), email_verified=False),
        private_key=private_key,
        nonce_verifier=nonce.verifier,
    )

    assert evidence.email is not None
    assert evidence.email.comparison_key == "person@gmail.com"
    assert evidence.mailbox_authoritative is True


@pytest.mark.asyncio
async def test_official_bare_google_issuer_is_normalized_to_canonical_https() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    evidence = await _verify(
        claims=_claims(nonce.secret.get_secret_value(), iss="accounts.google.com"),
        private_key=private_key,
        nonce_verifier=nonce.verifier,
    )

    assert evidence.issuer == GOOGLE_ISSUER


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("claim", "value"),
    [
        ("iss", "https://evil.example"),
        ("aud", "other-client"),
        ("sub", "  "),
        ("exp", int(_NOW.timestamp()) - 1),
        ("email_verified", "true"),
    ],
)
async def test_invalid_required_google_claims_are_rejected(claim: str, value: object) -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    with pytest.raises(GoogleProofError):
        await _verify(
            claims=_claims(nonce.secret.get_secret_value(), **{claim: value}),
            private_key=private_key,
            nonce_verifier=nonce.verifier,
        )


@pytest.mark.asyncio
async def test_future_nbf_beyond_clock_skew_is_rejected() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    with pytest.raises(GoogleProofError, match="not yet valid"):
        await _verify(
            claims=_claims(
                nonce.secret.get_secret_value(),
                nbf=int(_NOW.timestamp()) + 61,
            ),
            private_key=private_key,
            nonce_verifier=nonce.verifier,
        )


@pytest.mark.asyncio
async def test_multiple_audiences_require_exact_authorized_party() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    claims = _claims(
        nonce.secret.get_secret_value(),
        aud=[_CLIENT_ID, "other-client"],
    )

    with pytest.raises(GoogleProofError, match="authorized party"):
        await _verify(
            claims=claims,
            private_key=private_key,
            nonce_verifier=nonce.verifier,
        )

    claims["azp"] = _CLIENT_ID
    evidence = await _verify(
        claims=claims,
        private_key=private_key,
        nonce_verifier=nonce.verifier,
    )
    assert evidence.subject == "google-subject-123"


@pytest.mark.asyncio
async def test_wrong_oidc_nonce_is_rejected() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    expected = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    attacker = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    with pytest.raises(GoogleProofError, match="nonce"):
        await _verify(
            claims=_claims(attacker.secret.get_secret_value()),
            private_key=private_key,
            nonce_verifier=expected.verifier,
        )


@pytest.mark.asyncio
async def test_workspace_mailbox_requires_verified_email_and_hosted_domain() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    evidence = await _verify(
        claims=_claims(
            nonce.secret.get_secret_value(),
            email="person@company.example",
            email_verified=True,
            hd="company.example",
        ),
        private_key=private_key,
        nonce_verifier=nonce.verifier,
    )
    assert evidence.mailbox_authoritative is True
    assert evidence.hosted_domain == "company.example"


@pytest.mark.asyncio
async def test_verified_third_party_google_mailbox_is_not_treated_as_current_authority() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    evidence = await _verify(
        claims=_claims(
            nonce.secret.get_secret_value(),
            email="person@third-party.example",
            email_verified=True,
        ),
        private_key=private_key,
        nonce_verifier=nonce.verifier,
    )

    assert evidence.email is not None
    assert evidence.email.comparison_key == "person@third-party.example"
    assert evidence.mailbox_authoritative is False


@pytest.mark.asyncio
async def test_optional_malformed_profile_values_do_not_break_authentication() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)

    evidence = await _verify(
        claims=_claims(
            nonce.secret.get_secret_value(),
            name="  ",
            given_name=42,
            picture="http://insecure.example/avatar",
            locale="x" * 65,
        ),
        private_key=private_key,
        nonce_verifier=nonce.verifier,
    )

    assert evidence.display_name is None
    assert evidence.given_name is None
    assert evidence.picture_url is None
    assert evidence.locale is None


@pytest.mark.asyncio
async def test_provider_jwk_failure_is_mapped_without_falling_back_to_token_key_material() -> None:
    private_key = rsa.generate_private_key(public_exponent=65_537, key_size=2_048)
    nonce = issue_flow_proof(FlowProofPurpose.OIDC_NONCE)
    runtime = _StubProviderRuntime(_public_jwk(private_key), fail=True)

    with pytest.raises(GoogleProviderUnavailableError):
        await _verify(
            claims=_claims(nonce.secret.get_secret_value()),
            private_key=private_key,
            nonce_verifier=nonce.verifier,
            runtime=runtime,
        )

    assert runtime.requests == [("google", _KID)]
