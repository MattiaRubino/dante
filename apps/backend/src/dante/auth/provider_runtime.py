"""Provider HTTP runtime and coordinated bounded JWK cache."""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any

import httpx2

from dante.platform.config.auth_provider import AuthProviderSettings, ProviderNetworkSettings

_PRIVATE_JWK_MEMBERS = frozenset({"d", "p", "q", "dp", "dq", "qi", "oth", "k"})


class ProviderRuntimeError(RuntimeError):
    """Provider network/JWK material failed the DANTE trust boundary."""


@dataclass(slots=True)
class _JwkCacheEntry:
    keys_by_kid: dict[str, dict[str, Any]]
    expires_at: float
    etag: str | None
    last_modified: str | None
    last_forced_refresh_at: float


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

    async def aclose(self) -> None:
        await self._client.aclose()

    async def jwk_for_kid(self, *, provider: str, kid: str) -> dict[str, Any]:
        if not kid or len(kid) > 256 or kid.strip() != kid:
            raise ProviderRuntimeError("invalid JWK kid")
        url = self._trusted_jwks_url(provider)
        lock = self._locks.setdefault(provider, asyncio.Lock())
        async with lock:
            now = time.monotonic()
            entry = self._cache.get(provider)
            refreshed_expired = entry is None or entry.expires_at <= now
            if refreshed_expired:
                entry = await self._refresh(provider=provider, url=url, previous=entry, forced=False)
            key = entry.keys_by_kid.get(kid)
            if key is not None:
                return dict(key)
            if refreshed_expired:
                raise ProviderRuntimeError("unknown JWK kid")
            if now - entry.last_forced_refresh_at < self._settings.network.unknown_kid_refresh_cooldown_seconds:
                raise ProviderRuntimeError("unknown JWK kid")
            entry = await self._refresh(provider=provider, url=url, previous=entry, forced=True)
            key = entry.keys_by_kid.get(kid)
            if key is None:
                raise ProviderRuntimeError("unknown JWK kid")
            return dict(key)

    def _trusted_jwks_url(self, provider: str) -> str:
        if provider == "google":
            return self._settings.google.jwks_url
        if provider == "apple":
            return self._settings.apple.jwks_url
        raise ProviderRuntimeError("unknown provider")

    async def _refresh(self, *, provider: str, url: str, previous: _JwkCacheEntry | None, forced: bool) -> _JwkCacheEntry:
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
                    expires_at=time.monotonic() + self._ttl(response.headers, self._settings.network),
                    etag=response.headers.get("etag", previous.etag),
                    last_modified=response.headers.get("last-modified", previous.last_modified),
                    last_forced_refresh_at=time.monotonic() if forced else previous.last_forced_refresh_at,
                )
                self._cache[provider] = entry
                return entry
            if response.status_code != 200:
                raise ProviderRuntimeError(f"JWKS request failed with status {response.status_code}")
            declared = response.headers.get("content-length")
            if declared is not None:
                try:
                    if int(declared) > self._settings.network.max_jwks_response_bytes:
                        raise ProviderRuntimeError("JWKS response exceeds configured bound")
                except ValueError as exc:
                    raise ProviderRuntimeError("invalid JWKS Content-Length") from exc
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > self._settings.network.max_jwks_response_bytes:
                    raise ProviderRuntimeError("JWKS response exceeds configured bound")
            keys = self._parse_jwks(bytes(body))
            response_headers = response.headers
        entry = _JwkCacheEntry(
            keys_by_kid=keys,
            expires_at=time.monotonic() + self._ttl(response_headers, self._settings.network),
            etag=response_headers.get("etag"),
            last_modified=response_headers.get("last-modified"),
            last_forced_refresh_at=time.monotonic() if forced else (previous.last_forced_refresh_at if previous else float("-inf")),
        )
        self._cache[provider] = entry
        return entry

    def _parse_jwks(self, body: bytes) -> dict[str, dict[str, Any]]:
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderRuntimeError("provider JWKS is not valid JSON") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("keys"), list) or not payload["keys"]:
            raise ProviderRuntimeError("provider JWKS must contain a non-empty keys array")
        if len(payload["keys"]) > self._settings.network.max_jwk_count:
            raise ProviderRuntimeError("provider JWKS contains too many keys")
        result: dict[str, dict[str, Any]] = {}
        for value in payload["keys"]:
            if not isinstance(value, dict) or not isinstance(value.get("kid"), str) or not isinstance(value.get("kty"), str):
                raise ProviderRuntimeError("provider JWK is malformed")
            kid = value["kid"]
            if not kid or len(kid) > 256 or kid in result:
                raise ProviderRuntimeError("provider JWK kid is invalid or duplicated")
            if _PRIVATE_JWK_MEMBERS.intersection(value):
                raise ProviderRuntimeError("provider JWKS unexpectedly contains private/symmetric material")
            result[kid] = value
        return result

    @staticmethod
    def _ttl(headers: Any, network: ProviderNetworkSettings) -> float:
        directives = {part.strip().lower() for part in headers.get("cache-control", "").split(",") if part.strip()}
        if "no-store" in directives or "no-cache" in directives:
            return 0.0
        ttl = float(network.default_jwk_ttl_seconds)
        for directive in directives:
            if directive.startswith("max-age="):
                try:
                    ttl = float(max(0, int(directive.split("=", 1)[1].strip('"'))))
                except ValueError:
                    pass
                break
        try:
            age = max(0.0, float(headers.get("age", "0")))
        except ValueError:
            age = 0.0
        return min(max(0.0, ttl - age), float(network.max_jwk_ttl_seconds))
