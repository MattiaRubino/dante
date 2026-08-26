"""Deterministic transaction-scoped PostgreSQL advisory locking for DANTE."""

from __future__ import annotations

from hashlib import sha256
from typing import Final, Literal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

_LOCK_DOMAIN: Final[bytes] = b"dante-lock-v2"
_DIGEST_MASK: Final[int] = (1 << 56) - 1
_NAMESPACE_MAX: Final[int] = 127

SCHEDULE_PLACEMENT_CURRENT_NAMESPACE: Final[int] = 1
ACTUAL_REALIZATION_CURRENT_NAMESPACE: Final[int] = 2
SESSION_TIMING_CURRENT_NAMESPACE: Final[int] = 3
ROUTINE_RECURRENCE_CURRENT_NAMESPACE: Final[int] = 4
EVENT_RECURRENCE_CURRENT_NAMESPACE: Final[int] = 5
ROUTINE_OCCURRENCE_GENERATION_NAMESPACE: Final[int] = 6
EVENT_OCCURRENCE_GENERATION_NAMESPACE: Final[int] = 7


def advisory_lock_key(namespace_code: int, semantic_ref: UUID) -> int:
    """Return the frozen positive signed-bigint key for one semantic reference."""
    if not 1 <= namespace_code <= _NAMESPACE_MAX:
        raise ValueError("namespace_code must be in the frozen 1..127 range")

    digest56 = int.from_bytes(
        sha256(_LOCK_DOMAIN + semantic_ref.bytes).digest()[:7],
        byteorder="big",
        signed=False,
    )
    key = (namespace_code << 56) | (digest56 & _DIGEST_MASK)
    if not 0 < key < (1 << 63):
        raise AssertionError("DANTE advisory-lock key escaped signed bigint range")
    return key


def occurrence_generation_lock_keys(
    source_family: Literal["routine", "event"],
    source_ref: UUID,
) -> tuple[int, int]:
    """Return the sorted current-recurrence + occurrence-generation lock pair."""
    if source_family == "routine":
        namespaces = (
            ROUTINE_RECURRENCE_CURRENT_NAMESPACE,
            ROUTINE_OCCURRENCE_GENERATION_NAMESPACE,
        )
    elif source_family == "event":
        namespaces = (
            EVENT_RECURRENCE_CURRENT_NAMESPACE,
            EVENT_OCCURRENCE_GENERATION_NAMESPACE,
        )
    else:
        raise ValueError("source_family must be 'routine' or 'event'")

    keys = sorted(advisory_lock_key(code, source_ref) for code in namespaces)
    return keys[0], keys[1]


async def acquire_advisory_xact_locks(
    session: AsyncSession,
    lock_keys: list[int] | tuple[int, ...] | set[int],
) -> None:
    """Acquire deduplicated transaction locks in deterministic numeric order."""
    if not session.in_transaction():
        raise RuntimeError("an active AsyncSession transaction is required")

    for lock_key in sorted(set(lock_keys)):
        if not 0 < lock_key < (1 << 63):
            raise ValueError("advisory lock key must fit positive signed bigint")
        await session.execute(
            text("SELECT pg_catalog.pg_advisory_xact_lock(:lock_key)"),
            {"lock_key": lock_key},
        )
