"""Unit/security proof for password, KDF, session-secret and HIBP handling."""

import asyncio
import threading
from base64 import urlsafe_b64encode
from hashlib import sha1

import httpx2
import pytest

from dante.auth.contracts import KdfCapacityUnavailableError
from dante.auth.passwords import (
    BreachCheckUnavailableError,
    HibpPasswordChecker,
    PasswordInputError,
    PasswordKdf,
    normalize_password_for_authentication,
    validate_new_password,
)
from dante.auth.sessions import decode_session_secret, generate_session_secret


def _kdf(
    *,
    max_concurrency: int = 1,
    max_queue_depth: int = 0,
    queue_timeout: float = 1,
) -> PasswordKdf:
    return PasswordKdf(
        pepper_ring={"v1": b"p" * 32},
        current_pepper_key_id="v1",
        max_concurrency=max_concurrency,
        max_queue_depth=max_queue_depth,
        queue_timeout_seconds=queue_timeout,
    )


def test_password_authentication_normalization_is_nfc_without_trim_or_casefold() -> None:
    normalized = normalize_password_for_authentication("  AbC e\u0301  ")

    assert normalized == "  AbC é  "


def test_new_password_policy_requires_15_codepoints() -> None:
    with pytest.raises(PasswordInputError):
        validate_new_password("fourteen-chars"[:14])

    assert validate_new_password("fifteen-chars-ok!") == "fifteen-chars-ok!"


def test_password_resource_bounds_reject_oversized_value() -> None:
    with pytest.raises(PasswordInputError):
        normalize_password_for_authentication("x" * 1025)


def test_generated_session_secret_is_canonical_256_bit_base64url() -> None:
    secret = generate_session_secret().get_secret_value()
    decoded = decode_session_secret(secret)

    assert decoded is not None
    assert len(decoded) == 32
    assert "=" not in secret


def test_session_secret_decoder_rejects_padding_alias() -> None:
    secret = generate_session_secret().get_secret_value()

    assert decode_session_secret(secret + "=") is None


def test_session_secret_decoder_rejects_standard_base64_alias() -> None:
    canonical = urlsafe_b64encode(b"\xfb" * 32).rstrip(b"=").decode("ascii")
    standard_alias = canonical.replace("-", "+").replace("_", "/")

    assert standard_alias != canonical
    assert decode_session_secret(canonical) == b"\xfb" * 32
    assert decode_session_secret(standard_alias) is None


@pytest.mark.asyncio
async def test_production_argon2id_parameters_verify_without_rehash() -> None:
    kdf = _kdf()
    await kdf.start()
    try:
        verifier, key_id = await kdf.hash_new_password("correct horse battery staple")
        verification = await kdf.verify(
            normalized_password=normalize_password_for_authentication(
                "correct horse battery staple"
            ),
            verifier=verifier,
            pepper_key_id=key_id,
        )

        assert verifier.startswith("$argon2id$v=19$m=65536,t=3,p=4$")
        assert verification.valid is True
        assert verification.needs_rehash is False
    finally:
        await kdf.aclose()


@pytest.mark.asyncio
async def test_wrong_password_is_rejected_by_real_argon2id() -> None:
    kdf = _kdf()
    await kdf.start()
    try:
        verifier, key_id = await kdf.hash_new_password("correct horse battery staple")
        verification = await kdf.verify(
            normalized_password=normalize_password_for_authentication(
                "different horse battery staple"
            ),
            verifier=verifier,
            pepper_key_id=key_id,
        )

        assert verification.valid is False
        assert verification.needs_rehash is False
    finally:
        await kdf.aclose()


@pytest.mark.asyncio
async def test_legacy_pepper_verifier_is_marked_for_rehash() -> None:
    legacy = PasswordKdf(
        pepper_ring={"v1": b"a" * 32},
        current_pepper_key_id="v1",
        max_concurrency=1,
        max_queue_depth=0,
        queue_timeout_seconds=1,
    )
    current = PasswordKdf(
        pepper_ring={"v1": b"a" * 32, "v2": b"b" * 32},
        current_pepper_key_id="v2",
        max_concurrency=1,
        max_queue_depth=0,
        queue_timeout_seconds=1,
    )
    await legacy.start()
    await current.start()
    try:
        verifier, _ = await legacy.hash_new_password("correct horse battery staple")
        verification = await current.verify(
            normalized_password=normalize_password_for_authentication(
                "correct horse battery staple"
            ),
            verifier=verifier,
            pepper_key_id="v1",
        )

        assert verification.valid is True
        assert verification.needs_rehash is True
    finally:
        await current.aclose()
        await legacy.aclose()


@pytest.mark.asyncio
async def test_kdf_total_admission_is_bounded_before_executor_queue_growth() -> None:
    kdf = _kdf(max_concurrency=1, max_queue_depth=1, queue_timeout=1)
    worker_started = threading.Event()
    release_worker = threading.Event()

    def blocking_operation() -> str:
        worker_started.set()
        release_worker.wait(timeout=2)
        return "done"

    first = asyncio.create_task(kdf._run(blocking_operation))
    try:
        assert await asyncio.to_thread(worker_started.wait, 1)
        second = asyncio.create_task(kdf._run(lambda: "queued"))
        await asyncio.sleep(0)

        with pytest.raises(KdfCapacityUnavailableError):
            await kdf._run(lambda: "must-not-enter")

        release_worker.set()
        assert await first == "done"
        assert await second == "queued"
    finally:
        release_worker.set()
        if not first.done():
            await first
        await kdf.aclose()


@pytest.mark.asyncio
async def test_kdf_queue_wait_is_bounded_without_cancelling_running_worker() -> None:
    kdf = _kdf(max_concurrency=1, max_queue_depth=1, queue_timeout=0.01)
    worker_started = threading.Event()
    release_worker = threading.Event()

    def blocking_operation() -> str:
        worker_started.set()
        release_worker.wait(timeout=2)
        return "done"

    first = asyncio.create_task(kdf._run(blocking_operation))
    try:
        assert await asyncio.to_thread(worker_started.wait, 1)
        with pytest.raises(KdfCapacityUnavailableError):
            await kdf._run(lambda: "timed-out")
        assert first.done() is False
    finally:
        release_worker.set()
        assert await first == "done"
        await kdf.aclose()


@pytest.mark.asyncio
async def test_hibp_range_padding_and_local_suffix_match() -> None:
    candidate = "correct horse battery staple"
    digest = sha1(candidate.encode(), usedforsecurity=False).hexdigest().upper()
    expected_prefix, expected_suffix = digest[:5], digest[5:]
    observed_headers: dict[str, str] = {}

    async def handler(request: httpx2.Request) -> httpx2.Response:
        assert request.url.path == f"/range/{expected_prefix}"
        observed_headers["add-padding"] = request.headers["Add-Padding"]
        return httpx2.Response(
            200,
            text=f"{expected_suffix}:42\r\n{'0' * 35}:0\r\n",
        )

    async with httpx2.AsyncClient(
        base_url="https://api.pwnedpasswords.com",
        transport=httpx2.MockTransport(handler),
    ) as client:
        checker = HibpPasswordChecker(client=client, max_response_bytes=131_072)
        assert await checker.is_breached(candidate) is True

    assert observed_headers == {"add-padding": "true"}


@pytest.mark.asyncio
async def test_hibp_streaming_response_cap_fails_closed() -> None:
    async def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, content=b"A" * 257)

    async with httpx2.AsyncClient(
        base_url="https://api.pwnedpasswords.com",
        transport=httpx2.MockTransport(handler),
    ) as client:
        checker = HibpPasswordChecker(client=client, max_response_bytes=256)
        with pytest.raises(BreachCheckUnavailableError):
            await checker.is_breached("correct horse battery staple")


@pytest.mark.asyncio
async def test_hibp_malformed_response_fails_closed_at_adapter_boundary() -> None:
    async def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, text="not-a-valid-range-row")

    async with httpx2.AsyncClient(
        base_url="https://api.pwnedpasswords.com",
        transport=httpx2.MockTransport(handler),
    ) as client:
        checker = HibpPasswordChecker(client=client, max_response_bytes=131_072)
        with pytest.raises(BreachCheckUnavailableError):
            await checker.is_breached("correct horse battery staple")
