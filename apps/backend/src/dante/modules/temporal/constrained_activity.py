"""Atomic Activity + Temporal Constraint authoring for the B04 product boundary."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.modules.temporal.activity import (
    ActivityInputError,
    ActivityOperationIdReuseError,
    ActivityPersistenceError,
    ActivityView,
)
from dante.modules.temporal.temporal_constraint import (
    AbsoluteBoundaryRule,
    AbsoluteWindowRule,
    SessionMinimumDurationRule,
    CreatedTemporalConstraintView,
    TemporalConstraintInputError,
    TemporalConstraintOperationIdReuseError,
    TemporalConstraintPersistenceError,
    TemporalConstraintRule,
    _mutate_in_session,
    _rule_family,
)
from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
    new_material_state_ref,
    new_native_ref,
    new_scoped_record_ref,
)


class ConstrainedActivityInputError(ValueError):
    """The atomic constrained Activity request is outside the activated B04 product contract."""


class ConstrainedActivityOperationIdReuseError(RuntimeError):
    """One operation id was reused for a materially different composite intent."""


class ConstrainedActivityPersistenceError(RuntimeError):
    """The atomic Activity + Temporal Constraint effect could not complete safely."""


class ConstrainedActivityLifeAreaUnavailableError(RuntimeError):
    """The requested Life Area cannot receive a new constrained Activity."""


@dataclass(frozen=True, slots=True)
class CreateConstrainedActivityResult:
    activity: ActivityView
    constraints: tuple[CreatedTemporalConstraintView, ...]
    replayed: bool


def _normalize_title(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 300:
        raise ConstrainedActivityInputError(
            "Activity title must contain 1 to 300 non-padding characters."
        )
    return normalized


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise ConstrainedActivityInputError(
            "Activity operation id must contain 1 to 200 characters."
        )
    return normalized


def _activity_fingerprint(*, title: str, life_area_ref: UUID) -> str:
    return hashlib.sha256(
        json.dumps(
            {"version": 2, "title": title, "life_area_ref": str(life_area_ref)},
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _rule_payload(rule: TemporalConstraintRule) -> dict[str, str]:
    if isinstance(rule, AbsoluteWindowRule):
        return {
            "family": "window",
            "relationship": rule.relationship,
            "constrained_facet": rule.constrained_facet,
            "strength": rule.strength,
            "temporal_form": "absolute",
            "starts_at": rule.starts_at.isoformat(timespec="microseconds"),
            "ends_at": rule.ends_at.isoformat(timespec="microseconds"),
        }
    if isinstance(rule, AbsoluteBoundaryRule):
        return {
            "family": "boundary",
            "boundary_kind": rule.boundary_kind,
            "constrained_facet": rule.constrained_facet,
            "strength": rule.strength,
            "temporal_form": "absolute",
            "boundary_at": rule.boundary_at.isoformat(timespec="microseconds"),
        }
    if isinstance(rule, SessionMinimumDurationRule):
        return {
            "family": "duration",
            "duration_kind": rule.duration_kind,
            "constrained_facet": rule.constrained_facet,
            "strength": rule.strength,
            "duration_microseconds": str(rule.duration_microseconds),
        }
    raise ConstrainedActivityInputError(
        "Atomic constrained Activity authoring admits only public B04 rules and B08-C Session minimum duration."
    )


def _composite_fingerprint(*, title: str, rules: tuple[TemporalConstraintRule, ...]) -> str:
    return hashlib.sha256(
        json.dumps(
            {
                "title": title,
                "rules": [_rule_payload(rule) for rule in rules],
            },
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _child_operation_id(parent_operation_id: str, index: int) -> str:
    parent_hash = hashlib.sha256(parent_operation_id.encode("utf-8")).hexdigest()[:32]
    return f"b04f-constraint:{parent_hash}:{index}"


def _child_fingerprint(composite_fingerprint: str, index: int) -> str:
    return hashlib.sha256(f"{composite_fingerprint}:{index}".encode()).hexdigest()


def _constraint_name(exc: IntegrityError) -> str | None:
    diagnostic = getattr(exc.orig, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


_CREATE_ACTIVITY_SQL = text(
    """
    SELECT activity_ref, title, created_at, life_area_ref,
           assignment_revision AS life_area_assignment_revision, replayed
      FROM dante.create_self_activity_in_life_area(
           :self_person_ref,
           :operation_id,
           :intent_fingerprint,
           :activity_ref,
           :title,
           :life_area_ref
      )
    """
)


async def _create_activity_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    operation_id: str,
    title: str,
    life_area_ref: UUID,
    requested_activity_ref: NativeRef,
) -> tuple[ActivityView, bool]:
    row = (
        (
            await database_session.execute(
                _CREATE_ACTIVITY_SQL,
                {
                    "self_person_ref": self_person_ref,
                    "operation_id": operation_id,
                    "intent_fingerprint": _activity_fingerprint(
                        title=title, life_area_ref=life_area_ref
                    ),
                    "activity_ref": requested_activity_ref,
                    "title": title,
                    "life_area_ref": life_area_ref,
                },
            )
        )
        .mappings()
        .one()
    )
    return (
        ActivityView(
            activity_ref=NativeRef(UUID(str(row["activity_ref"]))),
            title=str(row["title"]),
            created_at=cast(datetime, row["created_at"]),
            life_area_ref=UUID(str(row["life_area_ref"])),
            life_area_assignment_revision=int(row["life_area_assignment_revision"]),
        ),
        bool(row["replayed"]),
    )


class ConstrainedActivityApplication:
    """Own one atomic transaction for Activity identity plus its initial B04 constraints."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create_activity_with_constraints(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        title: str,
        life_area_ref: UUID,
        rules: tuple[TemporalConstraintRule, ...],
    ) -> CreateConstrainedActivityResult:
        normalized_title = _normalize_title(title)
        normalized_operation_id = _normalize_operation_id(operation_id)
        if not 1 <= len(rules) <= 4:
            raise ConstrainedActivityInputError(
                "Atomic constrained Activity authoring requires 1 to 4 rules."
            )
        # Force the bounded public rule union and its value-level validation before opening
        # the transaction.
        for rule in rules:
            _rule_payload(rule)

        requested_activity_ref = new_native_ref()
        composite_fingerprint = _composite_fingerprint(
            title=normalized_title,
            rules=rules,
        )

        try:
            async with self._session_factory() as database_session, database_session.begin():
                activity, activity_replayed = await _create_activity_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    title=normalized_title,
                    life_area_ref=life_area_ref,
                    requested_activity_ref=requested_activity_ref,
                )

                created: list[CreatedTemporalConstraintView] = []
                for index, rule in enumerate(rules):
                    requested_constraint_ref = new_scoped_record_ref()
                    requested_material_state_ref = new_material_state_ref()
                    row = await _mutate_in_session(
                        database_session,
                        family=_rule_family(rule),
                        self_person_ref=self_person_ref,
                        operation_id=_child_operation_id(normalized_operation_id, index),
                        fingerprint=_child_fingerprint(composite_fingerprint, index),
                        mutation_kind="create",
                        subject_native_ref=activity.activity_ref,
                        constraint_ref=requested_constraint_ref,
                        expected_material_state_ref=None,
                        resulting_material_state_ref=requested_material_state_ref,
                        rule=rule,
                    )
                    rule_replayed = bool(row["replayed"])
                    if rule_replayed is not activity_replayed:
                        raise ConstrainedActivityOperationIdReuseError(
                            "Composite constrained Activity replay state is inconsistent."
                        )
                    material_state_value = row["material_state_ref"]
                    if material_state_value is None or row["active"] is not True:
                        raise ConstrainedActivityPersistenceError(
                            "Composite Temporal Constraint create returned an invalid active state."
                        )
                    created.append(
                        CreatedTemporalConstraintView(
                            constraint_ref=ScopedRecordRef(UUID(str(row["constraint_ref"]))),
                            subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
                            subject_kind="activity",
                            material_state_ref=MaterialStateRef(UUID(str(material_state_value))),
                            rule=rule,
                            recorded_at=cast(datetime, row["created_at"]),
                            replayed=rule_replayed,
                        )
                    )

                return CreateConstrainedActivityResult(
                    activity=activity,
                    constraints=tuple(created),
                    replayed=activity_replayed,
                )
        except ConstrainedActivityOperationIdReuseError:
            raise
        except (ActivityInputError, TemporalConstraintInputError) as exc:
            raise ConstrainedActivityInputError(str(exc)) from exc
        except (
            ActivityOperationIdReuseError,
            TemporalConstraintOperationIdReuseError,
        ) as exc:
            raise ConstrainedActivityOperationIdReuseError() from exc
        except IntegrityError as exc:
            if _constraint_name(exc) == "life_area_assignment_target_unavailable":
                raise ConstrainedActivityLifeAreaUnavailableError() from exc
            if _constraint_name(exc) in {
                "pk_activity_create_operation",
                "pk_temporal_constraint_mutation_operation",
            }:
                raise ConstrainedActivityOperationIdReuseError() from exc
            raise ConstrainedActivityPersistenceError() from exc
        except (ActivityPersistenceError, TemporalConstraintPersistenceError) as exc:
            raise ConstrainedActivityPersistenceError() from exc
        except (DBAPIError, SQLAlchemyError) as exc:
            raise ConstrainedActivityPersistenceError() from exc
