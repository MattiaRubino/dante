"""Provider HTTP runtime and coordinated bounded JWK cache."""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Mapping
from contextlib import suppress
from dataclasses import dataclass
from typing import Any

import httpx2

from dante.platform.config.auth_provider import AuthProviderSettings, ProviderNetworkSettings

_PRIVATE_JWK_MEMBERS = frozenset({"d", "p", "q", "dp", "dq", "qi", "oth", "k"})
_MAX_PROVIDER_RESPONSE_BYTES = 262_144


class ProviderRuntimeError(RuntimeError):
    """Provider network/JWK material failed the DANTE trust boundary."""


class ProviderMutationAmbiguousError(ProviderRuntimeError):
    """A single-use/provider mutation request lost a conclusive transport result."""


@dataclass(frozen=True, slots=True)
class ProviderJsonResponse:
    """Bounded provider response with parsed JSON only when a body is present."""

    status_code: int
    body: dict[str, Any] | None


@dataclass(slots=True)
class _JwkCacheEntry:
    keys_by_kid: dict[str, dict[str, Any]]
    expires_at: float
    etag: str | None
    last_modified: str | None


class ProviderRuntime:
    """One process-scoped bounded HTTP client plus per-provider JWK caches."""

    def __init__(self, *, settings: AuthProviderSettings, release_sha: str) -> None:
        self._settings = settings
        network = settings.network
        self._client = httpx2.AsyncClient(
            timeout=httpx2.Timeout(
                connect=network.connect_timeout_seconds,
                read=network.read_timeout_seconds,
                write=network.write_timeout_seconds,
                pool=network.pool_timeout_seconds,
            ),
            limits=httpx2.Limits(
                max_connections=network.max_connections,
                max_keepalive_connections=network.max_keepalive_connections,
            ),
            follow_redirects=False,
            trust_env=False,
            headers={"Accept": "application/json", "User-Agent": f"DANTE/{release_sha}"},
        )
        self._cache: dict[str, _JwkCacheEntry] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._last_unknown_kid_refresh_at: dict[str, float] = {}

    async def aclose(self) -> None:
        await self._client.aclose()

    async def jwk_for_kid(self, *, provider: str, kid: str) -> dict[str, Any]:
        """Resolve one trusted public JWK while coordinating cache refreshes per provider."""
        if not kid or len(kid) > 256 or kid.strip() != kid:
            raise ProviderRuntimeError("invalid JWK kid")

        url = self._trusted_jwks_url(provider)
        lock = self._locks.setdefault(provider, asyncio.Lock())

        async with lock:
            now = time.monotonic()
            entry = self._cache.get(provider)
            refreshed_expired = False

            if entry is None:
                entry = await self._refresh(provider=provider, url=url, previous=None)
                refreshed_expired = True
            elif entry.expires_at <= now:
                entry = await self._refresh(provider=provider, url=url, previous=entry)
                refreshed_expired = True

            key = entry.keys_by_kid.get(kid)
            if key is not None:
                return dict(key)

            if refreshed_expired:
                self._last_unknown_kid_refresh_at[provider] = time.monotonic()
                raise ProviderRuntimeError("unknown JWK kid")

            cooldown = self._settings.network.unknown_kid_refresh_cooldown_seconds
            last_refresh = self._last_unknown_kid_refresh_at.get(provider, float("-inf"))
            if now - last_refresh < cooldown:
                raise ProviderRuntimeError("unknown JWK kid")

            # Mark both the beginning and completion of the coordinated attempt. The first
            # assignment prevents parallel waiters from becoming independent refreshers if the
            # transport yields; the final assignment keeps the cooldown meaningful after a slow
            # or failed provider request.
            self._last_unknown_kid_refresh_at[provider] = now
            try:
                entry = await self._refresh(provider=provider, url=url, previous=entry)
            finally:
                self._last_unknown_kid_refresh_at[provider] = time.monotonic()

            key = entry.keys_by_kid.get(kid)
            if key is None:
                raise ProviderRuntimeError("unknown JWK kid")
            return dict(key)

    async def apple_token_exchange(self, form: Mapping[str, str]) -> ProviderJsonResponse:
        """POST one Apple authorization-code exchange with no automatic retry."""
        return await self._apple_form_post(url=self._settings.apple.token_url, form=form)

    async def apple_revoke(self, form: Mapping[str, str]) -> ProviderJsonResponse:
        """POST one Apple revoke request with no automatic retry."""
        return await self._apple_form_post(url=self._settings.apple.revoke_url, form=form)

    def _trusted_jwks_url(self, provider: str) -> str:
        if provider == "google":
            return self._settings.google.jwks_url
        if provider == "apple":
            return self._settings.apple.jwks_url
        raise ProviderRuntimeError("unknown provider")

    async def _apple_form_post(
        self,
        *,
        url: str,
        form: Mapping[str, str],
    ) -> ProviderJsonResponse:
        """Execute one bounded Apple form POST without exposing arbitrary provider URLs."""
        try:
            async with self._client.stream(
                "POST",
                url,
                data=dict(form),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            ) as response:
                body = await self._read_bounded_body(
                    response,
                    maximum_bytes=_MAX_PROVIDER_RESPONSE_BYTES,
                    label="Apple provider response",
                )
                status_code = response.status_code
        except ProviderRuntimeError:
            raise
        except Exception as exc:
            # Authorization codes are single-use and revoke is a provider mutation. If the
            # transport loses the response, the caller must reconcile instead of blindly retrying.
            raise ProviderMutationAmbiguousError(
                "Apple provider mutation result is ambiguous"
            ) from exc

        if not body:
            return ProviderJsonResponse(status_code=status_code, body=None)
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderRuntimeError("Apple provider response is not valid JSON") from exc
        if not isinstance(payload, dict):
            raise ProviderRuntimeError("Apple provider response must be a JSON object")
        return ProviderJsonResponse(status_code=status_code, body=payload)

    async def _refresh(
        self,
        *,
        provider: str,
        url: str,
        previous: _JwkCacheEntry | None,
    ) -> _JwkCacheEntry:
        headers: dict[str, str] = {}
        if previous is not None:
            if previous.etag:
                headers["If-None-Match"] = previous.etag
            if previous.last_modified:
                headers["If-Modified-Since"] = previous.last_modified

        async with self._client.stream("GET", url, headers=headers) as response:
            if response.status_code == 304 and previous is not None:
                entry = _JwkCacheEntry(
                    keys_by_kid=previous.keys_by_kid,
                    expires_at=time.monotonic()
                    + self._ttl(response.headers, self._settings.network),
                    etag=response.headers.get("etag", previous.etag),
                    last_modified=response.headers.get("last-modified", previous.last_modified),
                )
                self._cache[provider] = entry
                return entry

            if response.status_code != 200:
                raise ProviderRuntimeError(
                    f"JWKS request failed with status {response.status_code}"
                )

            body = await self._read_bounded_body(
                response,
                maximum_bytes=self._settings.network.max_jwks_response_bytes,
                label="JWKS response",
            )
            keys = self._parse_jwks(body)
            response_headers = response.headers

        entry = _JwkCacheEntry(
            keys_by_kid=keys,
            expires_at=time.monotonic() + self._ttl(response_headers, self._settings.network),
            etag=response_headers.get("etag"),
            last_modified=response_headers.get("last-modified"),
        )
        self._cache[provider] = entry
        return entry

    @staticmethod
    async def _read_bounded_body(
        response: Any,
        *,
        maximum_bytes: int,
        label: str,
    ) -> bytes:
        declared = response.headers.get("content-length")
        if declared is not None:
            try:
                declared_size = int(declared)
            except ValueError as exc:
                raise ProviderRuntimeError(f"invalid {label} Content-Length") from exc
            if declared_size < 0:
                raise ProviderRuntimeError(f"invalid {label} Content-Length")
            if declared_size > maximum_bytes:
                raise ProviderRuntimeError(f"{label} exceeds configured bound")

        body = bytearray()
        async for chunk in response.aiter_bytes():
            body.extend(chunk)
            if len(body) > maximum_bytes:
                raise ProviderRuntimeError(f"{label} exceeds configured bound")
        return bytes(body)

    def _parse_jwks(self, body: bytes) -> dict[str, dict[str, Any]]:
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderRuntimeError("provider JWKS is not valid JSON") from exc

        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("keys"), list)
            or not payload["keys"]
        ):
            raise ProviderRuntimeError("provider JWKS must contain a non-empty keys array")
        if len(payload["keys"]) > self._settings.network.max_jwk_count:
            raise ProviderRuntimeError("provider JWKS contains too many keys")

        result: dict[str, dict[str, Any]] = {}
        for value in payload["keys"]:
            if (
                not isinstance(value, dict)
                or not isinstance(value.get("kid"), str)
                or not isinstance(value.get("kty"), str)
            ):
                raise ProviderRuntimeError("provider JWK is malformed")

            kid = value["kid"]
            kty = value["kty"]
            if (
                not kid
                or len(kid) > 256
                or kid.strip() != kid
                or kid in result
                or not kty
                or kty.strip() != kty
            ):
                raise ProviderRuntimeError("provider JWK kid/type is invalid or duplicated")
            if _PRIVATE_JWK_MEMBERS.intersection(value):
                raise ProviderRuntimeError(
                    "provider JWKS unexpectedly contains private/symmetric material"
                )
            result[kid] = value

        return result

    @staticmethod
    def _ttl(headers: Any, network: ProviderNetworkSettings) -> float:
        directives = {
            part.strip().lower()
            for part in headers.get("cache-control", "").split(",")
            if part.strip()
        }
        if "no-store" in directives or "no-cache" in directives:
            return 0.0

        ttl = float(network.default_jwk_ttl_seconds)
        for directive in directives:
            if directive.startswith("max-age="):
                with suppress(ValueError):
                    ttl = float(max(0, int(directive.split("=", 1)[1].strip('"'))))
                break

        try:
            age = max(0.0, float(headers.get("age", "0")))
        except ValueError:
            age = 0.0

        return min(max(0.0, ttl - age), float(network.max_jwk_ttl_seconds))
