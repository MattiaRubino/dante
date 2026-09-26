"""B11-A advanced elapsed Recurrence runtime.

This module extends the canonical B06 ``elapsed_interval`` family with dynamic
Actual-backed anchors.  It does not introduce a second Recurrence identity or a
generic trigger/anchor abstraction.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef

AdvancedRecurrenceOwner = Literal["routine", "event"]
AdvancedAnchorMode = Literal["previous_completion", "anchor_stream"]
AnchorSourceFamily = Literal["routine", "event"]
RangeKind = Literal["open", "until_boundary", "expected_count"]


class AdvancedRecurrenceInputError(ValueError):
    """The advanced Recurrence command is internally inconsistent."""


class AdvancedRecurrenceUnavailableError(RuntimeError):
    """The source/anchor Recurrence is unavailable in the caller self scope."""


class AdvancedRecurrenceOperationReuseError(RuntimeError):
    """The idempotency key has already been accepted for a different intent."""


class AdvancedRecurrenceStateConflictError(RuntimeError):
    """The mutation/checkpoint was based on a stale Recurrence MaterialState."""


class AdvancedRecurrencePersistenceError(RuntimeError):
    """The canonical B11-A persistence boundary could not complete."""


@dataclass(frozen=True, slots=True)
class AdvancedElapsedRecurrence:
    range_kind: RangeKind
    expected_occurrence_count: int | None
    effective_from: datetime
    effective_until: datetime | None
    elapsed_seconds: Decimal
    anchor_mode_code: AdvancedAnchorMode
    anchor_source_family: AnchorSourceFamily | None = None
    anchor_source_native_ref: UUID | None = None


@dataclass(frozen=True, slots=True)
class AdvancedRecurrenceView:
    owner_kind: AdvancedRecurrenceOwner
    source_ref: UUID
    material_state_ref: UUID
    recurrence: AdvancedElapsedRecurrence


@dataclass(frozen=True, slots=True)
class AdvancedRecurrenceMutation:
    recurrence: AdvancedRecurrenceView
    accepted_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class AdvancedOccurrence:
    occurrence_ref: UUID
    expected_at: datetime
    anchor_occurrence_ref: UUID
    anchor_actual_ref: UUID
    anchor_actual_material_state_ref: UUID
    anchor_completed_at: datetime
    created: bool


@dataclass(frozen=True, slots=True)
class AdvancedCheckpointResult:
    owner_kind: AdvancedRecurrenceOwner
    source_ref: UUID
    governing_recurrence_state_ref: UUID
    accepted_at: datetime
    occurrences: tuple[AdvancedOccurrence, ...]
    replayed: bool


def _bounded_operation_id(value: str) -> str:
    key = value.strip()
    if not key or len(key) > 200:
        raise AdvancedRecurrenceInputError(
            "Advanced Recurrence operation id must contain 1 to 200 characters."
        )
    return key


def _validate(spec: AdvancedElapsedRecurrence) -> None:
    if spec.elapsed_seconds <= 0 or spec.elapsed_seconds.as_tuple().exponent < -6:
        raise AdvancedRecurrenceInputError(
            "Elapsed interval must be positive with at most six decimal places."
        )
    if spec.effective_from.tzinfo is None or (
        spec.effective_until is not None and spec.effective_until.tzinfo is None
    ):
        raise AdvancedRecurrenceInputError(
            "Advanced elapsed Recurrence requires absolute instants."
        )
    if spec.range_kind == "until_boundary":
        if spec.effective_until is None or spec.effective_until <= spec.effective_from:
            raise AdvancedRecurrenceInputError(
                "Until-boundary Recurrence requires a later effective end."
            )
    elif spec.effective_until is not None:
        raise AdvancedRecurrenceInputError(
            "Only until-boundary Recurrence may carry an effective end."
        )
    if spec.range_kind == "expected_count":
        if spec.expected_occurrence_count is None or spec.expected_occurrence_count < 1:
            raise AdvancedRecurrenceInputError(
                "Expected-count Recurrence requires a positive count."
            )
    elif spec.expected_occurrence_count is not None:
        raise AdvancedRecurrenceInputError(
            "Only expected-count Recurrence may carry a count."
        )
    if spec.anchor_mode_code == "previous_completion":
        if (
            spec.anchor_source_family is not None
            or spec.anchor_source_native_ref is not None
        ):
            raise AdvancedRecurrenceInputError(
                "Completion-relative Recurrence uses its own source completion stream."
            )
    elif (
        spec.anchor_source_family not in {"routine", "event"}
        or spec.anchor_source_native_ref is None
    ):
        raise AdvancedRecurrenceInputError(
            "Anchor-stream Recurrence requires one typed source."
        )


def _fingerprint(payload: dict[str, object]) -> str:
    def default(value: object) -> str:
        if isinstance(value, Decimal):
            return format(value.normalize(), "f")
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, UUID):
            return str(value)
        return str(value)

    return hashlib.sha256(
        json.dumps(
            payload,
            default=default,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def _error(exc: DBAPIError) -> RuntimeError:
    original = getattr(exc, "orig", None)
    sqlstate = getattr(original, "sqlstate", None)
    diagnostic = getattr(original, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None) if diagnostic else None
    message = str(original or exc)
    if sqlstate == "23505":
        return AdvancedRecurrenceOperationReuseError(message)
    if sqlstate == "40001":
        return AdvancedRecurrenceStateConflictError(message)
    if sqlstate in {"23503", "P0002"}:
        return AdvancedRecurrenceUnavailableError(message)
    if sqlstate in {"22023", "23514"}:
        return AdvancedRecurrenceInputError(message)
    if constraint and "state_conflict" in str(constraint):
        return AdvancedRecurrenceStateConflictError(message)
    return AdvancedRecurrencePersistenceError(message)


class AdvancedRecurrenceApplication:
    """Author and checkpoint B11-A dynamic elapsed Recurrence state."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def _read_in_session(
        self,
        session: AsyncSession,
        *,
        owner: AdvancedRecurrenceOwner,
        self_person_ref: NativeRef,
        source_ref: UUID,
    ) -> AdvancedRecurrenceView | None:
        try:
            base = (
                await session.execute(
                    text(f"SELECT * FROM dante.get_self_{owner}_recurrence(:actor,:source)"),
                    {"actor": self_person_ref, "source": source_ref},
                )
            ).mappings().one_or_none()
            if (
                base is None
                or str(base["family_code"]) != "elapsed_interval"
                or str(base["elapsed_anchor_mode_code"])
                not in {"previous_completion", "anchor_stream"}
            ):
                return None
            anchor = (
                await session.execute(
                    text(
                        f"SELECT * FROM dante.get_self_{owner}_dynamic_elapsed_anchor(:actor,:source)"
                    ),
                    {"actor": self_person_ref, "source": source_ref},
                )
            ).mappings().one_or_none()
        except DBAPIError as exc:
            raise _error(exc) from exc

        if anchor is None:
            raise AdvancedRecurrencePersistenceError(
                "Dynamic Recurrence state lost its canonical anchor descriptor."
            )
        recurrence = AdvancedElapsedRecurrence(
            range_kind=base["range_kind"],
            expected_occurrence_count=base["expected_occurrence_count"],
            effective_from=base["effective_from_instant"],
            effective_until=base["effective_until_instant"],
            elapsed_seconds=Decimal(str(base["elapsed_seconds"])),
            anchor_mode_code=anchor["anchor_mode_code"],
            anchor_source_family=anchor["anchor_source_family"],
            anchor_source_native_ref=anchor["anchor_source_native_ref"],
        )
        return AdvancedRecurrenceView(
            owner_kind=owner,
            source_ref=source_ref,
            material_state_ref=UUID(str(base["material_state_ref"])),
            recurrence=recurrence,
        )

    async def get(
        self,
        *,
        owner: AdvancedRecurrenceOwner,
        self_person_ref: NativeRef,
        source_ref: UUID,
    ) -> AdvancedRecurrenceView | None:
        try:
            async with self._session_factory() as session:
                return await self._read_in_session(
                    session,
                    owner=owner,
                    self_person_ref=self_person_ref,
                    source_ref=source_ref,
                )
        except AdvancedRecurrenceUnavailableError:
            raise
        except SQLAlchemyError as exc:
            raise AdvancedRecurrencePersistenceError() from exc

    async def replace(
        self,
        *,
        owner: AdvancedRecurrenceOwner,
        self_person_ref: NativeRef,
        operation_id: str,
        source_ref: UUID,
        expected_material_state_ref: UUID,
        recurrence: AdvancedElapsedRecurrence,
    ) -> AdvancedRecurrenceMutation:
        key = _bounded_operation_id(operation_id)
        _validate(recurrence)
        fingerprint = _fingerprint(
            {
                "version": 1,
                "kind": "b11a.dynamic_elapsed_replace",
                "owner": owner,
                "source_ref": source_ref,
                "expected_material_state_ref": expected_material_state_ref,
                "recurrence": recurrence,
            }
        )
        params = {
            "actor": self_person_ref,
            "operation": key,
            "fingerprint": fingerprint,
            "source": source_ref,
            "expected": expected_material_state_ref,
            "range_kind": recurrence.range_kind,
            "count": recurrence.expected_occurrence_count,
            "effective_from": recurrence.effective_from,
            "effective_until": recurrence.effective_until,
            "elapsed_seconds": recurrence.elapsed_seconds,
            "anchor_mode": recurrence.anchor_mode_code,
            "anchor_family": recurrence.anchor_source_family,
            "anchor_source": recurrence.anchor_source_native_ref,
        }
        try:
            async with self._session_factory() as session, session.begin():
                receipt = (
                    await session.execute(
                        text(
                            f"""SELECT * FROM dante.replace_self_{owner}_dynamic_elapsed_recurrence(
                              :actor,:operation,:fingerprint,:source,:expected,:range_kind,:count,
                              :effective_from,:effective_until,:elapsed_seconds,:anchor_mode,
                              :anchor_family,:anchor_source)"""
                        ),
                        params,
                    )
                ).mappings().one()
                current = await self._read_in_session(
                    session,
                    owner=owner,
                    self_person_ref=self_person_ref,
                    source_ref=source_ref,
                )
                if current is None or current.material_state_ref != UUID(
                    str(receipt["material_state_ref"])
                ):
                    raise AdvancedRecurrencePersistenceError(
                        "Accepted B11-A Recurrence was not readable as current truth."
                    )
                return AdvancedRecurrenceMutation(
                    recurrence=current,
                    accepted_at=receipt["accepted_at"],
                    replayed=bool(receipt["replayed"]),
                )
        except (
            AdvancedRecurrenceInputError,
            AdvancedRecurrenceUnavailableError,
            AdvancedRecurrenceOperationReuseError,
            AdvancedRecurrenceStateConflictError,
            AdvancedRecurrencePersistenceError,
        ):
            raise
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise AdvancedRecurrencePersistenceError() from exc

    async def checkpoint(
        self,
        *,
        owner: AdvancedRecurrenceOwner,
        self_person_ref: NativeRef,
        operation_id: str,
        source_ref: UUID,
        governing_recurrence_state_ref: UUID,
        start_at: datetime,
        end_at_exclusive: datetime,
    ) -> AdvancedCheckpointResult:
        key = _bounded_operation_id(operation_id)
        if (
            start_at.tzinfo is None
            or end_at_exclusive.tzinfo is None
            or end_at_exclusive <= start_at
        ):
            raise AdvancedRecurrenceInputError(
                "Checkpoint requires a non-empty absolute half-open window."
            )
        fingerprint = _fingerprint(
            {
                "version": 1,
                "kind": "b11a.dynamic_elapsed_checkpoint",
                "owner": owner,
                "source_ref": source_ref,
                "governing_recurrence_state_ref": governing_recurrence_state_ref,
                "start_at": start_at,
                "end_at_exclusive": end_at_exclusive,
            }
        )
        try:
            async with self._session_factory() as session, session.begin():
                rows = (
                    await session.execute(
                        text(
                            f"""SELECT * FROM dante.checkpoint_self_{owner}_dynamic_elapsed_occurrences(
                              :actor,:operation,:fingerprint,:source,:state,:start_at,:end_at)"""
                        ),
                        {
                            "actor": self_person_ref,
                            "operation": key,
                            "fingerprint": fingerprint,
                            "source": source_ref,
                            "state": governing_recurrence_state_ref,
                            "start_at": start_at,
                            "end_at": end_at_exclusive,
                        },
                    )
                ).mappings().all()
        except DBAPIError as exc:
            raise _error(exc) from exc
        except SQLAlchemyError as exc:
            raise AdvancedRecurrencePersistenceError() from exc

        if not rows:
            raise AdvancedRecurrencePersistenceError(
                "Checkpoint capability returned no receipt."
            )
        accepted_at = rows[0]["accepted_at"]
        replayed = bool(rows[0]["replayed"])
        occurrences = tuple(
            AdvancedOccurrence(
                occurrence_ref=UUID(str(row["occurrence_ref"])),
                expected_at=row["expected_at"],
                anchor_occurrence_ref=UUID(str(row["anchor_occurrence_ref"])),
                anchor_actual_ref=UUID(str(row["anchor_actual_ref"])),
                anchor_actual_material_state_ref=UUID(
                    str(row["anchor_actual_material_state_ref"])
                ),
                anchor_completed_at=row["anchor_completed_at"],
                created=bool(row["created"]),
            )
            for row in rows
            if row["occurrence_ref"] is not None
        )
        return AdvancedCheckpointResult(
            owner_kind=owner,
            source_ref=source_ref,
            governing_recurrence_state_ref=governing_recurrence_state_ref,
            accepted_at=accepted_at,
            occurrences=occurrences,
            replayed=replayed,
        )
