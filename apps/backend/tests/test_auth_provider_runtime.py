"""Focused M5-B provider runtime/configuration proof."""

from __future__ import annotations

import asyncio
from base64 import urlsafe_b64encode
from collections.abc import AsyncIterator, Callable
from typing import override

import httpx2
import pytest
from pydantic import SecretStr, ValidationError

from dante.auth.proofs import FlowProofPurpose, flow_proof_matches, issue_flow_proof
from dante.auth.provider_runtime import ProviderRuntime, ProviderRuntimeError
from dante.platform.config.auth import AuthSettings
from dante.platform.config.auth_provider import (
    AppleProviderSettings,
    AuthProviderSettings,
    ProviderNetworkSettings,
)


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _public_jwk(kid: str) -> dict[str, str]:
    return {"kid": kid, "kty": "RSA", "n": "AQAB", "e": "AQAB"}


class _ChunkedStream(httpx2.AsyncByteStream):
    def __init__(self, chunks: tuple[bytes, ...]) -> None:
        self._chunks = chunks

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in self._chunks:
            yield chunk


def _mocked_runtime(
    monkeypatch: pytest.MonkeyPatch,
    handler: Callable[[httpx2.Request], httpx2.Response],
    *,
    settings: AuthProviderSettings | None = None,
) -> ProviderRuntime:
    real_async_client = httpx2.AsyncClient

    def client_factory(**_kwargs: object) -> httpx2.AsyncClient:
        return real_async_client(transport=httpx2.MockTransport(handler))

    monkeypatch.setattr("dante.auth.provider_runtime.httpx2.AsyncClient", client_factory)
    return ProviderRuntime(
        settings=settings or AuthProviderSettings(),
        release_sha="test-release",
    )


def test_provider_defaults_are_disabled_and_canonical() -> None:
    settings = AuthProviderSettings()
    assert settings.google.enabled is False
    assert settings.apple.enabled is False
    assert settings.webauthn.enabled is False
    assert settings.google.issuer == "https://accounts.google.com"
    assert settings.apple.issuer == "https://appleid.apple.com"


def test_apple_provider_identifiers_reject_blank_values() -> None:
    with pytest.raises(ValidationError, match="Apple provider identity"):
        AppleProviderSettings(client_id="   ")
    with pytest.raises(ValidationError, match="Apple provider identity"):
        AppleProviderSettings(team_id="   ")
    with pytest.raises(ValidationError, match="Apple provider identity"):
        AppleProviderSettings(key_id="   ")


def test_apple_provider_private_key_rejects_blank_material() -> None:
    with pytest.raises(ValidationError, match="private key"):
        AppleProviderSettings(client_private_key_pem=SecretStr("   "))


def test_apple_grant_key_must_be_exactly_256_bits() -> None:
    with pytest.raises(ValidationError):
        AppleProviderSettings(
            grant_encryption_current_key_id="v1",
            grant_encryption_keys={"v1": SecretStr(_secret(b"short"))},
        )


def test_apple_grant_key_cannot_reuse_other_auth_secret_material() -> None:
    reused_secret = _secret(b"p" * 32)
    pepper_key_id = "password-v1"
    provider = AuthProviderSettings(
        apple=AppleProviderSettings(
            grant_encryption_current_key_id="v1",
            grant_encryption_keys={"v1": SecretStr(reused_secret)},
        )
    )

    with pytest.raises(ValidationError, match="distinct across cryptographic purposes"):
        AuthSettings(
            canonical_web_origin="https://dante.test",
            password_current_pepper_key_id=pepper_key_id,
            password_peppers={pepper_key_id: SecretStr(reused_secret)},
            csrf_key=SecretStr(_secret(b"c" * 32)),
            signup_otp_current_key_id="otp-v1",
            signup_otp_keys={"otp-v1": SecretStr(_secret(b"o" * 32))},
            provider=provider,
            smtp_host="smtp.dante.test",
            smtp_from_address="no-reply@dante.test",
            kdf_max_concurrency=1,
            signin_rate_capacity=10,
            signin_rate_window_seconds=60,
        )


def test_flow_proofs_are_purpose_separated() -> None:
    proof = issue_flow_proof(FlowProofPurpose.PROVIDER_STATE)
    raw = proof.secret.get_secret_value()
    assert flow_proof_matches(
        purpose=FlowProofPurpose.PROVIDER_STATE,
        encoded_secret=raw,
        expected_verifier=proof.verifier,
    )
    assert not flow_proof_matches(
        purpose=FlowProofPurpose.PROVIDER_LINK,
        encoded_secret=raw,
        expected_verifier=proof.verifier,
    )


def test_jwk_ttl_respects_age_clamp_and_no_store() -> None:
    network = ProviderNetworkSettings(max_jwk_ttl_seconds=500)
    assert ProviderRuntime._ttl(
        httpx2.Headers({"Cache-Control": "public, max-age=1000", "Age": "100"}),
        network,
    ) == 500.0
    assert ProviderRuntime._ttl(
        httpx2.Headers({"Cache-Control": "no-store, max-age=1000"}),
        network,
    ) == 0.0


@pytest.mark.asyncio
async def test_provider_runtime_does_not_contact_network_at_startup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        requests.append(request)
        raise AssertionError("provider network must remain lazy at process startup")

    runtime = _mocked_runtime(monkeypatch, handler)
    await runtime.aclose()

    assert requests == []


@pytest.mark.asyncio
async def test_http_ttl_avoids_refetch_for_known_fresh_kid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        requests.append(request)
        return httpx2.Response(
            200,
            request=request,
            headers={"Cache-Control": "public, max-age=300", "ETag": '"v1"'},
            json={"keys": [_public_jwk("known")]},
        )

    runtime = _mocked_runtime(monkeypatch, handler)
    try:
        first = await runtime.jwk_for_kid(provider="google", kid="known")
        second = await runtime.jwk_for_kid(provider="google", kid="known")
    finally:
        await runtime.aclose()

    assert first == second == _public_jwk("known")
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_unknown_kid_causes_one_coordinated_refresh(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request_count = 0

    def handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1
        keys = [_public_jwk("known")]
        if request_count >= 2:
            keys.append(_public_jwk("rotated"))
        return httpx2.Response(
            200,
            request=request,
            headers={"Cache-Control": "max-age=300"},
            json={"keys": keys},
        )

    runtime = _mocked_runtime(monkeypatch, handler)
    try:
        await runtime.jwk_for_kid(provider="google", kid="known")
        results = await asyncio.gather(
            *(runtime.jwk_for_kid(provider="google", kid="rotated") for _ in range(8))
        )
    finally:
        await runtime.aclose()

    assert all(result == _public_jwk("rotated") for result in results)
    assert request_count == 2


@pytest.mark.asyncio
async def test_unknown_kid_cooldown_prevents_refresh_storms(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request_count = 0

    def handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1
        return httpx2.Response(
            200,
            request=request,
            headers={"Cache-Control": "max-age=300"},
            json={"keys": [_public_jwk("known")]},
        )

    runtime = _mocked_runtime(monkeypatch, handler)
    try:
        await runtime.jwk_for_kid(provider="google", kid="known")
        with pytest.raises(ProviderRuntimeError, match="unknown JWK kid"):
            await runtime.jwk_for_kid(provider="google", kid="missing")

        outcomes = await asyncio.gather(
            *(runtime.jwk_for_kid(provider="google", kid="missing") for _ in range(8)),
            return_exceptions=True,
        )
    finally:
        await runtime.aclose()

    assert all(isinstance(outcome, ProviderRuntimeError) for outcome in outcomes)
    assert request_count == 2


@pytest.mark.asyncio
async def test_expiry_refresh_does_not_turn_waiters_into_forced_refreshers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request_count = 0

    def handler(request: httpx2.Request) -> httpx2.Response:
        nonlocal request_count
        request_count += 1
        max_age = "0" if request_count == 1 else "300"
        return httpx2.Response(
            200,
            request=request,
            headers={"Cache-Control": f"max-age={max_age}"},
            json={"keys": [_public_jwk("known")]},
        )

    runtime = _mocked_runtime(monkeypatch, handler)
    try:
        await runtime.jwk_for_kid(provider="google", kid="known")
        outcomes = await asyncio.gather(
            *(runtime.jwk_for_kid(provider="google", kid="missing") for _ in range(8)),
            return_exceptions=True,
        )
    finally:
        await runtime.aclose()

    assert all(isinstance(outcome, ProviderRuntimeError) for outcome in outcomes)
    assert request_count == 2


@pytest.mark.asyncio
async def test_expired_cache_revalidates_conditionally_and_accepts_304(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[httpx2.Request] = []
    last_modified = "Sun, 30 Aug 2026 12:00:00 GMT"

    def handler(request: httpx2.Request) -> httpx2.Response:
        requests.append(request)
        if len(requests) == 1:
            return httpx2.Response(
                200,
                request=request,
                headers={
                    "Cache-Control": "max-age=0",
                    "ETag": '"v1"',
                    "Last-Modified": last_modified,
                },
                json={"keys": [_public_jwk("known")]},
            )
        assert request.headers["If-None-Match"] == '"v1"'
        assert request.headers["If-Modified-Since"] == last_modified
        return httpx2.Response(
            304,
            request=request,
            headers={"Cache-Control": "max-age=300", "ETag": '"v1"'},
        )

    runtime = _mocked_runtime(monkeypatch, handler)
    try:
        first = await runtime.jwk_for_kid(provider="google", kid="known")
        second = await runtime.jwk_for_kid(provider="google", kid="known")
        third = await runtime.jwk_for_kid(provider="google", kid="known")
    finally:
        await runtime.aclose()

    assert first == second == third == _public_jwk("known")
    assert len(requests) == 2


@pytest.mark.asyncio
async def test_jwks_declared_size_bound_is_enforced_before_streaming(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = AuthProviderSettings(
        network=ProviderNetworkSettings(max_jwks_response_bytes=32)
    )

    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(
            200,
            request=request,
            headers={"Content-Length": "1024"},
            content=b'{}',
        )

    runtime = _mocked_runtime(monkeypatch, handler, settings=settings)
    try:
        with pytest.raises(ProviderRuntimeError, match="configured bound"):
            await runtime.jwk_for_kid(provider="google", kid="known")
    finally:
        await runtime.aclose()


@pytest.mark.asyncio
async def test_jwks_streaming_bound_is_enforced_without_content_length(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = AuthProviderSettings(
        network=ProviderNetworkSettings(max_jwks_response_bytes=32)
    )

    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(
            200,
            request=request,
            stream=_ChunkedStream(
                (
                    b'{"keys":[{"kid":"known","kty":"RSA","padding":"',
                    b"x" * 64,
                    b'"}]}',
                )
            ),
        )

    runtime = _mocked_runtime(monkeypatch, handler, settings=settings)
    try:
        with pytest.raises(ProviderRuntimeError, match="configured bound"):
            await runtime.jwk_for_kid(provider="google", kid="known")
    finally:
        await runtime.aclose()


@pytest.mark.asyncio
async def test_public_jwks_rejects_duplicate_kids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(
            200,
            request=request,
            json={"keys": [_public_jwk("duplicate"), _public_jwk("duplicate")]},
        )

    runtime = _mocked_runtime(monkeypatch, handler)
    try:
        with pytest.raises(ProviderRuntimeError, match="duplicated"):
            await runtime.jwk_for_kid(provider="google", kid="duplicate")
    finally:
        await runtime.aclose()


@pytest.mark.asyncio
async def test_public_jwks_rejects_configured_key_count_overflow(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = AuthProviderSettings(network=ProviderNetworkSettings(max_jwk_count=1))

    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(
            200,
            request=request,
            json={"keys": [_public_jwk("one"), _public_jwk("two")]},
        )

    runtime = _mocked_runtime(monkeypatch, handler, settings=settings)
    try:
        with pytest.raises(ProviderRuntimeError, match="too many keys"):
            await runtime.jwk_for_kid(provider="google", kid="one")
    finally:
        await runtime.aclose()


@pytest.mark.asyncio
async def test_public_jwks_rejects_private_or_symmetric_material(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(
            200,
            request=request,
            json={"keys": [{"kid": "bad", "kty": "RSA", "d": "private"}]},
        )

    runtime = _mocked_runtime(monkeypatch, handler)
    try:
        with pytest.raises(ProviderRuntimeError, match="private/symmetric"):
            await runtime.jwk_for_kid(provider="google", kid="bad")
    finally:
        await runtime.aclose()
