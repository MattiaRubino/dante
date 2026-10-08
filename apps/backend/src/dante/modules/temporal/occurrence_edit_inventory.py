"""M1-B read-only complete materialized inventory for recurring edit preparation.

The database function reuses B06's self-owned Occurrence read and fails rather
than truncating >10,000 rows. This *does not* select/authorize any write:
future source-template changes and current override/fact checks are separate
CAS-guarded application requirements for M1-C.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.occurrence import (
    OccurrenceCheckpointLimitError,
    OccurrencePersistenceError,
    OccurrenceSourceNotFoundError,
    OccurrenceView,
    _occurrence,
)
from dante.platform.database.references import NativeRef


@dataclass(frozen=True, slots=True)
class OccurrenceEditInventory:
    selected_occurrence_ref: UUID
    source_native_ref: UUID
    captured_at: datetime
    occurrences: tuple[OccurrenceView, ...]
    materialized_only: bool = True
    apply_authorized: bool = False


class OccurrenceEditInventoryApplication:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def read(
        self,
        *,
        self_person_ref: NativeRef,
        selected_occurrence_ref: UUID,
    ) -> OccurrenceEditInventory:
        try:
            async with self._session_factory() as session, session.begin():
                captured_at = await session.scalar(text("SELECT transaction_timestamp()"))
                rows = (
                    await session.execute(
                        text(
                            "SELECT * FROM dante.list_self_recurrence_edit_occurrences("
                            ":actor,:selected)"
                        ),
                        {"actor": self_person_ref, "selected": selected_occurrence_ref},
                    )
                ).mappings().all()
            items = tuple(_occurrence(row) for row in rows)
            if not items:
                raise OccurrenceSourceNotFoundError()
            source_ref = items[0].source_native_ref
            if (
                not any(item.occurrence_ref == selected_occurrence_ref for item in items)
                or any(item.source_native_ref != source_ref for item in items)
                or captured_at is None
            ):
                raise OccurrencePersistenceError()
            return OccurrenceEditInventory(
                selected_occurrence_ref=selected_occurrence_ref,
                source_native_ref=source_ref,
                captured_at=captured_at,
                occurrences=items,
            )
        except DBAPIError as exc:
            identifier = getattr(getattr(exc.orig, "diag", None), "constraint_name", None)
            if identifier == "recurrence_edit_occurrence_unavailable":
                raise OccurrenceSourceNotFoundError() from exc
            if identifier == "recurrence_edit_inventory_limit":
                raise OccurrenceCheckpointLimitError() from exc
            raise OccurrencePersistenceError() from exc
        except SQLAlchemyError as exc:
            raise OccurrencePersistenceError() from exc
