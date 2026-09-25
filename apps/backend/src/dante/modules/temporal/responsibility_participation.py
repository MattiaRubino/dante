"""B09-B guarded Responsibility and expected Participation authoring."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import NativeRef, new_native_ref

ResponsibilitySubjectKind = Literal["activity", "event"]
ParticipationRequirement = Literal["required", "optional"]


class ResponsibilityInputError(ValueError):
    """The authoring command is outside the B09-B contract."""


class ResponsibilityNotFoundError(LookupError):
    """The subject or the referenced Person is unavailable to this actor."""


class ResponsibilityOperationReuseError(RuntimeError):
    """One operation id was reused for a materially different intent."""


class ResponsibilityConflictError(RuntimeError):
    """The current holder or requirement no longer matches the caller's expectation."""


class ResponsibilityPersistenceError(RuntimeError):
    """Canonical Responsibility persistence could not complete safely."""


@dataclass(frozen=True, slots=True)
class ResponsibilityView:
    """Current single-holder Responsibility for one Activity or Event."""

    subject_kind: ResponsibilitySubjectKind
    subject_native_ref: NativeRef
    responsible_person_ref: NativeRef | None
    established_at: datetime | None
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class PersonReferentView:
    """A locally labelled native Person; label is not global Person identity."""

    person_ref: NativeRef
    display_label: str
    revision: int
    replayed: bool = False


@dataclass(frozen=True, slots=True)
class ExpectedParticipationView:
    """Current expected involvement of one Person in one Event."""

    event_ref: NativeRef
    participant_person_ref: NativeRef
    requirement_code: ParticipationRequirement | None
    established_at: datetime | None
    replayed: bool = False


def _operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ResponsibilityInputError("Operation id must contain 1 to 200 characters.")
    return normalized


def _fingerprint(payload: dict[str, str | None]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _optional_ref(value: object) -> NativeRef | None:
    return None if value is None else NativeRef(UUID(str(value)))


def _map_error(exc: DBAPIError) -> Exception:
    diagnostic = getattr(exc.orig, "diag", None)
    constraint = getattr(diagnostic, "constraint_name", None)
    if constraint in {"responsibility_operation_reused", "participation_operation_reused", "person_referent_operation_reused"}:
        return ResponsibilityOperationReuseError("Operation id was reused.")
    if constraint in {
        "responsibility_subject_unavailable",
        "responsibility_person_unavailable",
        "participation_event_unavailable",
        "participation_person_unavailable",
        "person_referent_unavailable",
        "person_referent_self_unavailable",
    }:
        return ResponsibilityNotFoundError("Subject or Person is unavailable to this actor.")
    if constraint in {
        "responsibility_expected_holder_conflict",
        "responsibility_no_change",
        "participation_expected_requirement_conflict",
        "participation_no_change",
        "person_referent_revision_conflict",
        "person_referent_no_change",
    }:
        return ResponsibilityConflictError("The current state does not match the request.")
    return ResponsibilityPersistenceError("Authoring command was rejected.")


class ResponsibilityParticipationApplication:
    """Each command owns one transaction and uses only bounded DB capabilities."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def set_responsibility(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        subject_kind: ResponsibilitySubjectKind,
        subject_native_ref: NativeRef,
        responsible_person_ref: NativeRef | None,
        expected_responsible_person_ref: NativeRef | None,
    ) -> ResponsibilityView:
        if subject_kind not in ("activity", "event"):
            raise ResponsibilityInputError("Responsibility subjects are Activity and Event only.")
        normalized = _operation_id(operation_id)
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "set_responsibility",
                "subject_kind": subject_kind,
                "subject_native_ref": str(subject_native_ref),
                "responsible_person_ref": (
                    None if responsible_person_ref is None else str(responsible_person_ref)
                ),
                "expected_responsible_person_ref": (
                    None
                    if expected_responsible_person_ref is None
                    else str(expected_responsible_person_ref)
                ),
            }
        )
        row = await self._one(
            f"""
            SELECT subject_native_ref, responsible_person_ref, established_at, replayed
              FROM dante.set_self_{subject_kind}_responsibility(
                :actor, :operation_id, :fingerprint, :subject,
                :responsible, :expected
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized,
                "fingerprint": fingerprint,
                "subject": subject_native_ref,
                "responsible": responsible_person_ref,
                "expected": expected_responsible_person_ref,
            },
        )
        return self._responsibility(row, subject_kind=subject_kind)

    async def get_responsibility(
        self,
        *,
        self_person_ref: NativeRef,
        subject_kind: ResponsibilitySubjectKind,
        subject_native_ref: NativeRef,
    ) -> ResponsibilityView:
        if subject_kind not in ("activity", "event"):
            raise ResponsibilityInputError("Responsibility subjects are Activity and Event only.")
        rows = await self._rows(
            f"""
            SELECT subject_native_ref, responsible_person_ref, established_at
              FROM dante.get_self_{subject_kind}_responsibility(:actor, :subject)
            """,
            {"actor": self_person_ref, "subject": subject_native_ref},
        )
        if not rows:
            # The capability already proved self ownership; no row means no holder.
            return ResponsibilityView(
                subject_kind=subject_kind,
                subject_native_ref=subject_native_ref,
                responsible_person_ref=None,
                established_at=None,
            )
        return self._responsibility(rows[0], subject_kind=subject_kind)

    async def set_expected_participation(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        event_ref: NativeRef,
        participant_person_ref: NativeRef,
        requirement_code: ParticipationRequirement | None,
        expected_requirement_code: ParticipationRequirement | None,
    ) -> ExpectedParticipationView:
        if requirement_code is not None and requirement_code not in ("required", "optional"):
            raise ResponsibilityInputError("Expected Participation is required or optional.")
        normalized = _operation_id(operation_id)
        fingerprint = _fingerprint(
            {
                "version": "1",
                "command": "set_expected_participation",
                "event_ref": str(event_ref),
                "participant_person_ref": str(participant_person_ref),
                "requirement_code": requirement_code,
                "expected_requirement_code": expected_requirement_code,
            }
        )
        row = await self._one(
            """
            SELECT event_ref, participant_person_ref, requirement_code,
                   established_at, replayed
              FROM dante.set_self_event_expected_participation(
                :actor, :operation_id, :fingerprint, :event,
                :participant, :requirement, :expected
              )
            """,
            {
                "actor": self_person_ref,
                "operation_id": normalized,
                "fingerprint": fingerprint,
                "event": event_ref,
                "participant": participant_person_ref,
                "requirement": requirement_code,
                "expected": expected_requirement_code,
            },
        )
        return self._participation(row)

    async def list_expected_participation(
        self, *, self_person_ref: NativeRef, event_ref: NativeRef
    ) -> tuple[ExpectedParticipationView, ...]:
        rows = await self._rows(
            """
            SELECT event_ref, participant_person_ref, requirement_code, established_at
              FROM dante.list_self_event_expected_participation(:actor, :event)
            """,
            {"actor": self_person_ref, "event": event_ref},
        )
        return tuple(self._participation(row) for row in rows)

    async def create_person_referent(
        self, *, self_person_ref: NativeRef, operation_id: str, display_label: str
    ) -> PersonReferentView:
        label = display_label.strip()
        if not label or len(label) > 100:
            raise ResponsibilityInputError("Person label must contain 1 to 100 characters.")
        normalized = _operation_id(operation_id)
        rows = await self._rows(
            """
            SELECT person_ref,display_label,revision,replayed
              FROM dante.create_self_person_referent(
                :actor,:key,:fingerprint,:person,:label
              )
            """,
            {
                "actor": self_person_ref,
                "key": normalized,
                "fingerprint": _fingerprint(
                    {"version": "1", "command": "create_person_referent", "label": label}
                ),
                "person": new_native_ref(),
                "label": label,
            },
        )
        if not rows:
            raise ResponsibilityPersistenceError("Person creation returned no result.")
        return self._person_referent(rows[0])

    async def list_person_referents(
        self, *, self_person_ref: NativeRef
    ) -> tuple[PersonReferentView, ...]:
        rows = await self._rows(
            "SELECT person_ref,display_label,revision FROM dante.list_self_person_referents(:actor)",
            {"actor": self_person_ref},
        )
        return tuple(self._person_referent(row) for row in rows)

    async def rename_person_referent(
        self, *, self_person_ref: NativeRef, operation_id: str,
        person_ref: NativeRef, expected_revision: int, display_label: str
    ) -> PersonReferentView:
        label = display_label.strip()
        if not label or len(label) > 100 or expected_revision < 1:
            raise ResponsibilityInputError("Invalid Person label or expected revision.")
        rows = await self._rows(
            """
            SELECT person_ref,display_label,revision,replayed
              FROM dante.rename_self_person_referent(
                :actor,:key,:fingerprint,:person,:expected,:label
              )
            """,
            {
                "actor": self_person_ref,
                "key": _operation_id(operation_id),
                "fingerprint": _fingerprint({
                    "version": "1", "command": "rename_person_referent",
                    "person_ref": str(person_ref),
                    "expected_revision": str(expected_revision), "label": label,
                }),
                "person": person_ref,
                "expected": expected_revision,
                "label": label,
            },
        )
        if not rows:
            raise ResponsibilityPersistenceError("Person rename returned no result.")
        return self._person_referent(rows[0])

    @staticmethod
    def _person_referent(row: RowMapping) -> PersonReferentView:
        return PersonReferentView(
            person_ref=NativeRef(UUID(str(row["person_ref"]))),
            display_label=str(row["display_label"]),
            revision=int(row["revision"]),
            replayed=bool(row["replayed"]) if "replayed" in row else False,
        )

    @staticmethod
    def _responsibility(
        row: RowMapping, *, subject_kind: ResponsibilitySubjectKind
    ) -> ResponsibilityView:
        return ResponsibilityView(
            subject_kind=subject_kind,
            subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
            responsible_person_ref=_optional_ref(row["responsible_person_ref"]),
            established_at=row["established_at"],
            replayed=bool(row["replayed"]) if "replayed" in row else False,
        )

    @staticmethod
    def _participation(row: RowMapping) -> ExpectedParticipationView:
        requirement = row["requirement_code"]
        return ExpectedParticipationView(
            event_ref=NativeRef(UUID(str(row["event_ref"]))),
            participant_person_ref=NativeRef(UUID(str(row["participant_person_ref"]))),
            requirement_code=(
                None if requirement is None else cast(ParticipationRequirement, str(requirement))
            ),
            established_at=row["established_at"],
            replayed=bool(row["replayed"]) if "replayed" in row else False,
        )

    async def _one(self, statement: str, parameters: dict[str, object]) -> RowMapping:
        rows = await self._rows(statement, parameters)
        if not rows:
            raise ResponsibilityPersistenceError("Authoring command returned no canonical result.")
        return rows[0]

    async def _rows(
        self, statement: str, parameters: dict[str, object]
    ) -> list[RowMapping]:
        try:
            async with self._session_factory() as session, session.begin():
                result = await session.execute(text(statement), parameters)
                return list(result.mappings().all())
        except DBAPIError as exc:
            raise _map_error(exc) from exc
        except SQLAlchemyError as exc:
            raise ResponsibilityPersistenceError("Authoring command was rejected.") from exc
