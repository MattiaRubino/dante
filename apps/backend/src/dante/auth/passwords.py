"""Password normalization, Argon2id, peppering and HIBP breach intelligence."""

from __future__ import annotations

import asyncio
import hmac
import secrets
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from hashlib import sha1
from typing import TypeVar
from unicodedata import normalize

import httpx2
from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)
from argon2.low_level import Type

from dante.auth.contracts import AuthIntegrityError, KdfCapacityUnavailableError

_MIN_PASSWORD_CODEPOINTS = 15
_MAX_PASSWORD_CODEPOINTS = 1024
_MAX_PASSWORD_UTF8_BYTES = 4096

_ARGON2_MEMORY_KIB = 65_536
_ARGON2_TIME_COST = 3
_ARGON2_PARALLELISM = 4
_ARGON2_HASH_LENGTH = 32
_ARGON2_SALT_LENGTH = 16

_HIBP_RESPONSE_SUFFIX_LENGTH = 35

_T = TypeVar("_T")


class PasswordInputError(ValueError):
    """Password violates a bounded client/resource contract."""

    def __init__(
        self,
        *,
        code: str,
        detail: str,
        parameters: dict[str, int] | None = None,
    ) -> None:
        super().__init__("invalid password input")
        self.code = code
        self.detail = detail
        self.parameters = parameters


class BreachCheckUnavailableError(RuntimeError):
    """Pwned Passwords could not return a trustworthy range response."""


@dataclass(frozen=True, slots=True)
class PasswordVerification:
    """Result of one current/legacy-pepper password verification."""

    valid: bool
    needs_rehash: bool


def normalize_password_for_authentication(password: str) -> str:
    """Apply only DANTE's exact NFC normalization and resource bounds."""
    normalized = normalize("NFC", password)

    if not normalized:
        raise PasswordInputError(code="required", detail="A password is required.")
    if len(normalized) > _MAX_PASSWORD_CODEPOINTS:
        raise PasswordInputError(
            code="too_long",
            detail="The password exceeds the supported length.",
            parameters={"maximum": _MAX_PASSWORD_CODEPOINTS},
        )
    if len(normalized.encode("utf-8")) > _MAX_PASSWORD_UTF8_BYTES:
        raise PasswordInputError(
            code="too_long",
            detail="The normalized password exceeds the supported byte length.",
            parameters={"maximum_bytes": _MAX_PASSWORD_UTF8_BYTES},
        )
    return normalized


def validate_new_password(password: str) -> str:
    """Apply establishment policy on top of authentication resource bounds."""
    normalized = normalize_password_for_authentication(password)
    if len(normalized) < _MIN_PASSWORD_CODEPOINTS:
        raise PasswordInputError(
            code="too_short",
            detail="The password does not meet the minimum length.",
            parameters={"minimum": _MIN_PASSWORD_CODEPOINTS},
        )
    return normalized


class PasswordKdf:
    """Dedicated Argon2id executor with bounded workers and bounded admission."""

    def __init__(
        self,
        *,
        pepper_ring: dict[str, bytes],
        current_pepper_key_id: str,
        max_concurrency: int,
        max_queue_depth: int,
        queue_timeout_seconds: float,
    ) -> None:
        if current_pepper_key_id not in pepper_ring:
            raise ValueError("current pepper key is absent from the pepper ring")

        self._pepper_ring = dict(pepper_ring)
        self._current_pepper_key_id = current_pepper_key_id
        self._queue_timeout_seconds = queue_timeout_seconds
        self._max_inflight = max_concurrency + max_queue_depth
        self._inflight = 0
        self._slots = asyncio.BoundedSemaphore(max_concurrency)
        self._executor = ThreadPoolExecutor(
            max_workers=max_concurrency,
            thread_name_prefix="dante-password-kdf",
        )
        self._hasher = PasswordHasher(
            time_cost=_ARGON2_TIME_COST,
            memory_cost=_ARGON2_MEMORY_KIB,
            parallelism=_ARGON2_PARALLELISM,
            hash_len=_ARGON2_HASH_LENGTH,
            salt_len=_ARGON2_SALT_LENGTH,
            type=Type.ID,
        )
        self._dummy_verifier: str | None = None

    @property
    def current_pepper_key_id(self) -> str:
        """Return the non-secret key identifier used for new verifiers."""
        return self._current_pepper_key_id

    async def start(self) -> None:
        """Warm one real-policy dummy verifier before accepting signin traffic."""
        dummy_value = secrets.token_urlsafe(32)
        prehash = self._prehash(dummy_value, self._current_pepper_key_id)
        try:
            self._dummy_verifier = await self._run(lambda: self._hasher.hash(prehash))
        except HashingError as exc:
            raise AuthIntegrityError("Argon2 dummy verifier initialization failed") from exc

    async def aclose(self) -> None:
        """Stop owned KDF workers without blocking the event loop."""
        await asyncio.to_thread(
            self._executor.shutdown,
            wait=True,
            cancel_futures=True,
        )

    async def hash_new_password(self, password: str) -> tuple[str, str]:
        """Validate and hash one new password with the current pepper/policy."""
        normalized = validate_new_password(password)
        return await self.hash_normalized_password(normalized)

    async def hash_normalized_password(self, normalized_password: str) -> tuple[str, str]:
        """Hash a previously bounded normalized password with current policy."""
        prehash = self._prehash(normalized_password, self._current_pepper_key_id)
        try:
            verifier = await self._run(lambda: self._hasher.hash(prehash))
        except HashingError as exc:
            raise AuthIntegrityError("Argon2 hashing failed") from exc
        return verifier, self._current_pepper_key_id

    async def verify(
        self,
        *,
        normalized_password: str,
        verifier: str,
        pepper_key_id: str,
    ) -> PasswordVerification:
        """Verify the exact stored pepper key and detect a safe upgrade need."""
        if pepper_key_id not in self._pepper_ring:
            raise AuthIntegrityError("stored PasswordCredential references unknown pepper key")

        prehash = self._prehash(normalized_password, pepper_key_id)

        def operation() -> PasswordVerification:
            try:
                self._hasher.verify(verifier, prehash)
            except VerifyMismatchError:
                return PasswordVerification(valid=False, needs_rehash=False)
            except (InvalidHashError, VerificationError) as exc:
                raise AuthIntegrityError("stored Argon2 verifier is invalid") from exc

            return PasswordVerification(
                valid=True,
                needs_rehash=(
                    pepper_key_id != self._current_pepper_key_id
                    or self._hasher.check_needs_rehash(verifier)
                ),
            )

        return await self._run(operation)

    async def verify_dummy(self, normalized_password: str) -> None:
        """Execute one current-policy Argon2 verification for an unknown credential."""
        verifier = self._dummy_verifier
        if verifier is None:
            raise AuthIntegrityError("PasswordKdf.start() was not completed")

        prehash = self._prehash(normalized_password, self._current_pepper_key_id)

        def operation() -> None:
            try:
                self._hasher.verify(verifier, prehash)
            except VerifyMismatchError:
                return
            except (InvalidHashError, VerificationError) as exc:
                raise AuthIntegrityError("dummy Argon2 verifier is invalid") from exc

        await self._run(operation)

    def _prehash(self, normalized_password: str, pepper_key_id: str) -> bytes:
        return hmac.digest(
            self._pepper_ring[pepper_key_id],
            normalized_password.encode("utf-8"),
            "sha256",
        )

    def _admit(self) -> None:
        if self._inflight >= self._max_inflight:
            raise KdfCapacityUnavailableError()
        self._inflight += 1

    def _release_admission(self) -> None:
        self._inflight -= 1

    def _release_cancelled_worker(self, _future: object) -> None:
        self._slots.release()
        self._release_admission()

    async def _run(self, operation: Callable[[], _T]) -> _T:
        self._admit()
        slot_acquired = False
        release_here = True

        try:
            try:
                async with asyncio.timeout(self._queue_timeout_seconds):
                    await self._slots.acquire()
                slot_acquired = True
            except TimeoutError as exc:
                raise KdfCapacityUnavailableError() from exc

            loop = asyncio.get_running_loop()
            worker_future = loop.run_in_executor(self._executor, operation)
            try:
                return await asyncio.shield(worker_future)
            except asyncio.CancelledError:
                release_here = False
                worker_future.add_done_callback(self._release_cancelled_worker)
                raise
        finally:
            if release_here:
                if slot_acquired:
                    self._slots.release()
                self._release_admission()


class HibpPasswordChecker:
    """Protocol-faithful Pwned Passwords range client with streaming byte bounds."""

    def __init__(
        self,
        *,
        client: httpx2.AsyncClient,
        max_response_bytes: int,
    ) -> None:
        self._client = client
        self._max_response_bytes = max_response_bytes

    async def is_breached(self, normalized_password: str) -> bool:
        """Return whether the complete SHA-1 appears in the k-anonymous range."""
        digest = sha1(
            normalized_password.encode("utf-8"),
            usedforsecurity=False,
        ).hexdigest().upper()
        prefix, expected_suffix = digest[:5], digest[5:]
        chunks: list[bytes] = []
        observed_bytes = 0

        try:
            async with self._client.stream(
                "GET",
                f"/range/{prefix}",
                headers={"Add-Padding": "true"},
            ) as response:
                if response.status_code != 200:
                    raise BreachCheckUnavailableError("HIBP returned a non-success status")

                content_length = response.headers.get("content-length")
                if content_length is not None:
                    try:
                        declared_length = int(content_length)
                    except ValueError as exc:
                        raise BreachCheckUnavailableError(
                            "HIBP returned an invalid content length"
                        ) from exc
                    if declared_length < 0 or declared_length > self._max_response_bytes:
                        raise BreachCheckUnavailableError(
                            "HIBP range response exceeded the configured bound"
                        )

                async for chunk in response.aiter_bytes():
                    observed_bytes += len(chunk)
                    if observed_bytes > self._max_response_bytes:
                        raise BreachCheckUnavailableError(
                            "HIBP range response exceeded the configured bound"
                        )
                    chunks.append(chunk)
        except BreachCheckUnavailableError:
            raise
        except httpx2.HTTPError as exc:
            raise BreachCheckUnavailableError("HIBP request failed") from exc

        try:
            payload = b"".join(chunks).decode("ascii")
            return self._parse_range(payload, expected_suffix=expected_suffix)
        except ValueError as exc:
            raise BreachCheckUnavailableError("HIBP returned a malformed range response") from exc

    @staticmethod
    def _parse_range(payload: str, *, expected_suffix: str) -> bool:
        for raw_line in payload.splitlines():
            if not raw_line:
                continue

            suffix, separator, raw_count = raw_line.partition(":")
            if separator != ":" or len(suffix) != _HIBP_RESPONSE_SUFFIX_LENGTH:
                raise ValueError("invalid HIBP suffix row")
            if any(character not in "0123456789ABCDEFabcdef" for character in suffix):
                raise ValueError("invalid HIBP suffix encoding")

            try:
                count = int(raw_count)
            except ValueError as exc:
                raise ValueError("invalid HIBP breach count") from exc
            if count < 0:
                raise ValueError("invalid negative HIBP breach count")

            if count > 0 and hmac.compare_digest(suffix.upper(), expected_suffix):
                return True

        return False
