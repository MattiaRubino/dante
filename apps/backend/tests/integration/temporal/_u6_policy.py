"""Declare live capture explicitly for legacy B08/B10 Session fixtures."""

from __future__ import annotations

import hashlib
from uuid import UUID, uuid7

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def enable_live_capture(
    session_factory: async_sessionmaker[AsyncSession],
    *,
    actor: UUID,
    activity_ref: UUID,
) -> None:
    operation = f"fixture:live:{activity_ref}"
    fingerprint = hashlib.sha256(operation.encode()).hexdigest()
    async with session_factory() as session, session.begin():
        await session.execute(
            text("""
                SELECT * FROM dante.set_self_activity_execution_policy(
                    :actor,:operation,:fingerprint,:activity,:state,'live',NULL
                )
            """),
            {
                "actor": actor,
                "operation": operation,
                "fingerprint": fingerprint,
                "activity": activity_ref,
                "state": uuid7(),
            },
        )
