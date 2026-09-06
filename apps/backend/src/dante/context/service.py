"""Resolve authenticated Accounts into bounded DANTE application context."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.auth.contracts import Principal
from dante.context.contracts import DanteContext, DanteContextIntegrityError
from dante.platform.database.references import NativeRef, new_native_ref
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_CONTEXT_SELECT = text(
    """
    SELECT account_ref, self_person_ref, timezone_mode, fixed_zone_id
    FROM dante.account_application_context
    WHERE account_ref = :account_ref
    """
)
_CONTEXT_ENSURE = text(
    """
    SELECT account_ref, self_person_ref, timezone_mode, fixed_zone_id
    FROM dante.ensure_account_application_context(:account_ref, :self_person_ref)
    """
)


class DanteContextService:
    """Translate one admitted Access/Auth Principal into application-facing DANTE context."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def resolve(
        self,
        *,
        principal: Principal,
        device_zone_id: str | None,
    ) -> DanteContext:
        """Resolve or lazily establish the Account context in one application transaction."""
        async with self._session_factory() as session, session.begin():
            row = (
                (
                    await session.execute(
                        _CONTEXT_SELECT,
                        {"account_ref": principal.account_ref},
                    )
                )
                .mappings()
                .one_or_none()
            )

            if row is None:
                # A newly established context defaults to follow-device. Validate that request
                # input before durable creation so malformed bootstrap traffic creates nothing.
                TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE).resolve(
                    device_zone_id=device_zone_id
                )
                row = (
                    (
                        await session.execute(
                            _CONTEXT_ENSURE,
                            {
                                "account_ref": principal.account_ref,
                                "self_person_ref": new_native_ref(),
                            },
                        )
                    )
                    .mappings()
                    .one()
                )

        return _context_from_persisted(
            principal=principal,
            row=row,
            device_zone_id=device_zone_id,
        )


def _context_from_persisted(
    *,
    principal: Principal,
    row: Mapping[str, Any] | RowMapping,
    device_zone_id: str | None,
) -> DanteContext:
    """Build the typed request context from one persistence row and current device context."""
    try:
        account_ref = UUID(str(row["account_ref"]))
        self_person_ref = NativeRef(UUID(str(row["self_person_ref"])))
        mode = TimeZoneMode(str(row["timezone_mode"]))
        fixed_zone_raw = row["fixed_zone_id"]
        fixed_zone_id = None if fixed_zone_raw is None else str(fixed_zone_raw)
        policy = TimeZonePolicy(mode=mode, fixed_zone_id=fixed_zone_id)
    except (TypeError, ValueError) as exc:
        raise DanteContextIntegrityError(
            "persisted authenticated DANTE context violates its storage contract"
        ) from exc

    if account_ref != principal.account_ref:
        raise DanteContextIntegrityError(
            "persisted DANTE context does not belong to the authenticated Account"
        )

    # Resolve follow-device input outside the persisted-state guard. A malformed device timezone
    # is a request error; an invalid fixed policy above is an internal persistence-integrity error.
    effective_zone_id = policy.resolve(device_zone_id=device_zone_id)

    return DanteContext(
        principal=principal,
        self_person_ref=self_person_ref,
        timezone_policy=policy,
        effective_zone_id=effective_zone_id,
    )
