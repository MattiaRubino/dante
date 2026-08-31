"""Fast M5-D Apple exchange/revoke semantics without external network."""

from __future__ import annotations

from base64 import urlsafe_b64encode
from typing import cast

import pytest
from pydantic import SecretStr, ValidationError

from dante.auth.apple import (
    AppleClientSecretSigner,
    AppleExchangeAmbiguousError,
    AppleProtocolClient,
)
from dante.auth.provider_runtime import (
    ProviderJsonResponse,
    ProviderMutationAmbiguousError,
    ProviderRuntime,
)
from dante.platform.config.auth_provider import AppleProviderSettings, AuthProviderSettings

_CLIENT_ID = "com.dante.web"
_REDIRECT_URI = "https://auth.dante.example/api/v1/auth/apple/callback"


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _exchange_id_token() -> str:
    return "exchange-id-token"


def _settings() -> AuthProviderSettings:
    return AuthProviderSettings(
        apple=AppleProviderSettings(
            enabled=True,
            client_id=_CLIENT_ID,
            team_id="ABCDE12345",
            key_id="APPLEKEY01",
            client_private_key_pem=SecretStr("placeholder-p8"),
            redirect_uri=_REDIRECT_URI,
            grant_encryption_current_key_id="v1",
            grant_encryption_keys={"v1": SecretStr(_secret(b"g" * 32))},
        )
    )


class _StubSigner:
    def issue(self) -> SecretStr:
        return SecretStr("signed-client-secret")


class _StubRuntime:
    def __init__(self) -> None:
        self.token_forms: list[dict[str, str]] = []
        self.revoke_forms: list[dict[str, str]] = []
        self.ambiguous = False

    async def apple_token_exchange(self, form: dict[str, str]) -> ProviderJsonResponse:
        self.token_forms.append(dict(form))
        if self.ambiguous:
            raise ProviderMutationAmbiguousError("lost response")
        return ProviderJsonResponse(
            status_code=200,
            body={
                "access_token": "discarded-by-dante",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "refresh-token",
                "id_token": _exchange_id_token(),
            },
        )

    async def apple_revoke(self, form: dict[str, str]) -> ProviderJsonResponse:
        self.revoke_forms.append(dict(form))
        return ProviderJsonResponse(status_code=200, body=None)


def _client(runtime: _StubRuntime) -> AppleProtocolClient:
    return AppleProtocolClient(
        settings=_settings(),
        provider_runtime=cast(ProviderRuntime, runtime),
        signer=cast(AppleClientSecretSigner, _StubSigner()),
    )


@pytest.mark.asyncio
async def test_code_exchange_is_single_attempt_exact_form_and_keeps_only_refresh_identity_material() -> (
    None
):
    runtime = _StubRuntime()
    client = _client(runtime)

    response = await client.exchange_code("single-use-code")

    assert response.id_token == _exchange_id_token()
    assert response.refresh_token.get_secret_value() == "refresh-token"
    assert runtime.token_forms == [
        {
            "client_id": _CLIENT_ID,
            "client_secret": "signed-client-secret",
            "code": "single-use-code",
            "grant_type": "authorization_code",
            "redirect_uri": _REDIRECT_URI,
        }
    ]


@pytest.mark.asyncio
async def test_ambiguous_code_exchange_is_never_blindly_retried() -> None:
    runtime = _StubRuntime()
    runtime.ambiguous = True
    client = _client(runtime)

    with pytest.raises(AppleExchangeAmbiguousError):
        await client.exchange_code("single-use-code")

    assert len(runtime.token_forms) == 1


@pytest.mark.asyncio
async def test_revoke_uses_refresh_hint_and_accepts_empty_200_success() -> None:
    runtime = _StubRuntime()
    client = _client(runtime)

    await client.revoke_refresh_token(SecretStr("refresh-token"))

    assert runtime.revoke_forms == [
        {
            "client_id": _CLIENT_ID,
            "client_secret": "signed-client-secret",
            "token": "refresh-token",
            "token_type_hint": "refresh_token",
        }
    ]


@pytest.mark.parametrize(
    "redirect_uri",
    [
        "http://auth.dante.example/callback",
        "https://localhost/callback",
        "https://127.0.0.1/callback",
        "https://auth.dante.example/callback?x=1",
        "https://user@auth.dante.example/callback",
    ],
)
def test_apple_redirect_uri_requires_exact_registered_https_domain(redirect_uri: str) -> None:
    with pytest.raises(ValidationError, match="Apple redirect URI"):
        AppleProviderSettings(redirect_uri=redirect_uri)
