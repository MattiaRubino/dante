"""Temporal Constraint application operations over the canonical PostgreSQL core."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, cast
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dante.platform.database.references import (
    MaterialStateRef,
    NativeRef,
    ScopedRecordRef,
    new_material_state_ref,
    new_scoped_record_ref,
)
from dante.platform.time import normalize_utc_instant

TemporalConstraintSubjectKind = Literal["activity", "event"]
TemporalConstraintStrength = Literal["hard", "soft"]
TemporalConstraintStatus = Literal["active", "retired"]
TemporalConstraintBoundaryKind = Literal[
    "earliest_start",
    "latest_start",
    "latest_completion",
]
TemporalConstraintWindowRelationship = Literal[
    "start_within",
    "completion_within",
    "full_placement_contained",
    "placement_overlaps",
]
TemporalConstraintFacet = Literal[
    "schedule.start",
    "schedule.completion",
    "schedule.placement",
]
TemporalConstraintFamily = Literal["boundary", "window"]
MutationKind = Literal["create", "revise", "retire"]
ConstraintEvaluationStatus = Literal["satisfied", "violated", "not_evaluable"]
ConstraintSetEvaluationStatus = Literal[
    "admissible",
    "admissible_with_soft_violations",
    "inadmissible",
    "not_evaluable",
]
HardSetStatus = Literal["feasible", "infeasible", "undetermined"]


class TemporalConstraintInputError(ValueError):
    """The requested Temporal Constraint operation is outside the activated contract."""


class TemporalConstraintOperationIdReuseError(RuntimeError):
    """One operation id was reused for materially different Temporal Constraint intent."""


class TemporalConstraintNotFoundError(LookupError):
    """The Temporal Constraint or subject is absent from the authenticated self scope."""


class TemporalConstraintStateConflictError(RuntimeError):
    """The expected Temporal Constraint rule state is no longer current."""


class TemporalConstraintPersistenceError(RuntimeError):
    """Canonical Temporal Constraint persistence could not complete safely."""


def _normalize_instant(value: datetime) -> datetime:
    try:
        return normalize_utc_instant(value)
    except ValueError as exc:
        raise TemporalConstraintInputError(str(exc)) from exc


def _validate_strength(value: str) -> TemporalConstraintStrength:
    if value not in {"hard", "soft"}:
        raise TemporalConstraintInputError(
            "Temporal Constraint strength must be either hard or soft."
        )
    return cast(TemporalConstraintStrength, value)


def _admitted_boundary_pair(boundary_kind: str, constrained_facet: str) -> bool:
    return (
        (boundary_kind == "earliest_start" and constrained_facet == "schedule.start")
        or (boundary_kind == "latest_start" and constrained_facet == "schedule.start")
        or (
            boundary_kind == "latest_completion"
            and constrained_facet == "schedule.completion"
        )
    )


def _admitted_window_pair(relationship: str, constrained_facet: str) -> bool:
    return (
        (relationship == "start_within" and constrained_facet == "schedule.start")
        or (
            relationship == "completion_within"
            and constrained_facet == "schedule.completion"
        )
        or (
            relationship in {"full_placement_contained", "placement_overlaps"}
            and constrained_facet == "schedule.placement"
        )
    )


@dataclass(frozen=True, slots=True)
class AbsoluteBoundaryRule:
    """One complete B04-A/B typed absolute Schedule boundary rule."""

    boundary_kind: TemporalConstraintBoundaryKind
    constrained_facet: TemporalConstraintFacet
    strength: TemporalConstraintStrength
    boundary_at: datetime

    def __post_init__(self) -> None:
        _validate_strength(self.strength)
        if not _admitted_boundary_pair(self.boundary_kind, self.constrained_facet):
            raise TemporalConstraintInputError(
                "Temporal Constraint boundary kind and constrained facet are not an admitted B04-B pair."
            )
        object.__setattr__(self, "boundary_at", _normalize_instant(self.boundary_at))


@dataclass(frozen=True, slots=True)
class AbsoluteEarliestStartRule:
    """B04-A compatibility value for an absolute earliest Schedule start."""

    strength: TemporalConstraintStrength
    boundary_at: datetime

    def __post_init__(self) -> None:
        _validate_strength(self.strength)
        object.__setattr__(self, "boundary_at", _normalize_instant(self.boundary_at))

    @property
    def boundary_kind(self) -> Literal["earliest_start"]:
        return "earliest_start"

    @property
    def constrained_facet(self) -> Literal["schedule.start"]:
        return "schedule.start"


@dataclass(frozen=True, slots=True)
class AbsoluteWindowRule:
    """B04-C typed finite absolute window and its required Schedule relation."""

    relationship: TemporalConstraintWindowRelationship
    constrained_facet: TemporalConstraintFacet
    strength: TemporalConstraintStrength
    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        _validate_strength(self.strength)
        if not _admitted_window_pair(self.relationship, self.constrained_facet):
            raise TemporalConstraintInputError(
                "Temporal Constraint window relation and constrained facet are not an admitted B04-C pair."
            )
        starts_at = _normalize_instant(self.starts_at)
        ends_at = _normalize_instant(self.ends_at)
        if ends_at <= starts_at:
            raise TemporalConstraintInputError(
                "Temporal Constraint absolute window end must be later than its start."
            )
        object.__setattr__(self, "starts_at", starts_at)
        object.__setattr__(self, "ends_at", ends_at)


TemporalConstraintRule = AbsoluteBoundaryRule | AbsoluteEarliestStartRule | AbsoluteWindowRule


@dataclass(frozen=True, slots=True)
class TemporalConstraintCurrentBoundaryRuleView:
    material_state_ref: MaterialStateRef
    family: Literal["boundary"]
    boundary_kind: TemporalConstraintBoundaryKind
    constrained_facet: TemporalConstraintFacet
    strength: TemporalConstraintStrength
    temporal_form: Literal["absolute"]
    boundary_at: datetime


@dataclass(frozen=True, slots=True)
class TemporalConstraintCurrentWindowRuleView:
    material_state_ref: MaterialStateRef
    family: Literal["window"]
    relationship: TemporalConstraintWindowRelationship
    constrained_facet: TemporalConstraintFacet
    strength: TemporalConstraintStrength
    temporal_form: Literal["absolute"]
    starts_at: datetime
    ends_at: datetime


TemporalConstraintCurrentRuleView = (
    TemporalConstraintCurrentBoundaryRuleView | TemporalConstraintCurrentWindowRuleView
)


@dataclass(frozen=True, slots=True)
class TemporalConstraintView:
    constraint_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    subject_kind: TemporalConstraintSubjectKind
    status: TemporalConstraintStatus
    current_rule: TemporalConstraintCurrentRuleView | None


@dataclass(frozen=True, slots=True)
class CreatedTemporalConstraintView:
    constraint_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    subject_kind: TemporalConstraintSubjectKind
    material_state_ref: MaterialStateRef
    rule: TemporalConstraintRule
    recorded_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class RevisedTemporalConstraintView:
    constraint_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    subject_kind: TemporalConstraintSubjectKind
    previous_material_state_ref: MaterialStateRef
    material_state_ref: MaterialStateRef
    rule: TemporalConstraintRule
    recorded_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class RetiredTemporalConstraintView:
    constraint_ref: ScopedRecordRef
    subject_native_ref: NativeRef
    subject_kind: TemporalConstraintSubjectKind
    previous_material_state_ref: MaterialStateRef
    recorded_at: datetime
    replayed: bool


@dataclass(frozen=True, slots=True)
class AbsoluteIntervalPlacement:
    starts_at: datetime
    ends_at: datetime

    def __post_init__(self) -> None:
        starts_at = _normalize_instant(self.starts_at)
        ends_at = _normalize_instant(self.ends_at)
        if ends_at <= starts_at:
            raise TemporalConstraintInputError(
                "Candidate absolute interval end must be later than its start."
            )
        object.__setattr__(self, "starts_at", starts_at)
        object.__setattr__(self, "ends_at", ends_at)


@dataclass(frozen=True, slots=True)
class TemporalConstraintEvaluationItem:
    constraint_ref: ScopedRecordRef
    material_state_ref: MaterialStateRef
    family: TemporalConstraintFamily
    rule_code: str
    constrained_facet: TemporalConstraintFacet
    strength: TemporalConstraintStrength
    evaluation: ConstraintEvaluationStatus
    reason_code: str


@dataclass(frozen=True, slots=True)
class TemporalConstraintEvaluationView:
    subject_native_ref: NativeRef
    placement: AbsoluteIntervalPlacement
    status: ConstraintSetEvaluationStatus
    hard_set_status: HardSetStatus
    items: tuple[TemporalConstraintEvaluationItem, ...]


_SUBJECT_KIND_SQL = text(
    """
    SELECT address.owner_family
      FROM dante.native_address AS address
     WHERE address.native_ref=:subject_native_ref
       AND (
            (address.owner_family='activity' AND EXISTS (
                SELECT 1 FROM dante.activity_intention AS activity
                 WHERE activity.activity_ref=address.native_ref
                   AND activity.self_person_ref=:self_person_ref
            ))
            OR
            (address.owner_family='event' AND EXISTS (
                SELECT 1 FROM dante.event_expectation AS event_row
                 WHERE event_row.event_ref=address.native_ref
                   AND event_row.self_person_ref=:self_person_ref
            ))
       )
    """
)

_CONSTRAINT_IDENTITY_SQL = text(
    """
    SELECT constraint_row.subject_native_ref,
           address.owner_family AS subject_kind
      FROM dante.temporal_constraint AS constraint_row
      JOIN dante.native_address AS address
        ON address.native_ref=constraint_row.subject_native_ref
     WHERE constraint_row.constraint_ref=:constraint_ref
       AND (
            (address.owner_family='activity' AND EXISTS (
                SELECT 1 FROM dante.activity_intention AS activity
                 WHERE activity.activity_ref=constraint_row.subject_native_ref
                   AND activity.self_person_ref=:self_person_ref
            ))
            OR
            (address.owner_family='event' AND EXISTS (
                SELECT 1 FROM dante.event_expectation AS event_row
                 WHERE event_row.event_ref=constraint_row.subject_native_ref
                   AND event_row.self_person_ref=:self_person_ref
            ))
       )
    """
)

_EXPECTED_FAMILY_SQL = text(
    """
    SELECT state.family_code
      FROM dante.temporal_constraint_state AS state
     WHERE state.constraint_ref=:constraint_ref
       AND state.material_state_ref=:material_state_ref
    """
)

_READ_CONSTRAINT_BASE = """
SELECT constraint_row.constraint_ref,
       constraint_row.subject_native_ref,
       subject_address.owner_family AS subject_kind,
       current.material_state_ref,
       state.family_code,
       state.strength_code,
       state.constrained_facet_code,
       boundary.boundary_kind_code,
       boundary.temporal_form_code AS boundary_temporal_form_code,
       boundary_payload.boundary_at,
       window_state.relationship_code,
       window_state.temporal_form_code AS window_temporal_form_code,
       window_payload.starts_at,
       window_payload.ends_at
  FROM dante.temporal_constraint AS constraint_row
  JOIN dante.native_address AS subject_address
    ON subject_address.native_ref=constraint_row.subject_native_ref
  LEFT JOIN dante.scoped_current_material_state AS current
    ON current.scoped_owner_ref=constraint_row.constraint_ref
   AND current.facet_code='temporal_constraint.rule'
  LEFT JOIN dante.temporal_constraint_state AS state
    ON state.constraint_ref=constraint_row.constraint_ref
   AND state.material_state_ref=current.material_state_ref
  LEFT JOIN dante.temporal_constraint_boundary_state AS boundary
    ON boundary.material_state_ref=state.material_state_ref
  LEFT JOIN dante.temporal_constraint_boundary_absolute_state AS boundary_payload
    ON boundary_payload.material_state_ref=boundary.material_state_ref
  LEFT JOIN dante.temporal_constraint_window_state AS window_state
    ON window_state.material_state_ref=state.material_state_ref
  LEFT JOIN dante.temporal_constraint_window_absolute_state AS window_payload
    ON window_payload.material_state_ref=window_state.material_state_ref
 WHERE (
        (subject_address.owner_family='activity' AND EXISTS (
            SELECT 1 FROM dante.activity_intention AS activity
             WHERE activity.activity_ref=constraint_row.subject_native_ref
               AND activity.self_person_ref=:self_person_ref
        ))
        OR
        (subject_address.owner_family='event' AND EXISTS (
            SELECT 1 FROM dante.event_expectation AS event_row
             WHERE event_row.event_ref=constraint_row.subject_native_ref
               AND event_row.self_person_ref=:self_person_ref
        ))
 )
"""

_MUTATE_BOUNDARY_SQL = text(
    """
    SELECT constraint_ref, subject_native_ref, material_state_ref, active, created_at, replayed
      FROM dante.mutate_self_absolute_boundary_constraint(
           :self_person_ref,:operation_id,:intent_fingerprint,:mutation_kind,
           :subject_native_ref,:constraint_ref,:expected_material_state_ref,
           :resulting_material_state_ref,:boundary_kind_code,:constrained_facet_code,
           :strength_code,:boundary_at
      )
    """
)

_MUTATE_WINDOW_SQL = text(
    """
    SELECT constraint_ref, subject_native_ref, material_state_ref, active, created_at, replayed
      FROM dante.mutate_self_absolute_window_constraint(
           :self_person_ref,:operation_id,:intent_fingerprint,:mutation_kind,
           :subject_native_ref,:constraint_ref,:expected_material_state_ref,
           :resulting_material_state_ref,:relationship_code,:constrained_facet_code,
           :strength_code,:starts_at,:ends_at
      )
    """
)


def _normalize_operation_id(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 200:
        raise TemporalConstraintInputError(
            "Temporal Constraint operation id must contain 1 to 200 characters."
        )
    return normalized


def _require_uuid7(value: UUID, *, label: str) -> None:
    if value.version != 7:
        raise TemporalConstraintInputError(f"{label} must be a canonical UUIDv7 value.")


def _hash(payload: Mapping[str, str]) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _rule_family(rule: TemporalConstraintRule) -> TemporalConstraintFamily:
    return "window" if isinstance(rule, AbsoluteWindowRule) else "boundary"


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
    return {
        "family": "boundary",
        "boundary_kind": rule.boundary_kind,
        "constrained_facet": rule.constrained_facet,
        "strength": rule.strength,
        "temporal_form": "absolute",
        "boundary_at": rule.boundary_at.isoformat(timespec="microseconds"),
    }


def _create_fingerprint(*, subject_native_ref: NativeRef, rule: TemporalConstraintRule) -> str:
    return _hash(
        {
            "mutation_kind": "create",
            "subject_native_ref": str(subject_native_ref),
            **_rule_payload(rule),
        }
    )


def _revise_fingerprint(
    *,
    constraint_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
    rule: TemporalConstraintRule,
) -> str:
    return _hash(
        {
            "mutation_kind": "revise",
            "constraint_ref": str(constraint_ref),
            "expected_material_state_ref": str(expected_material_state_ref),
            **_rule_payload(rule),
        }
    )


def _retire_fingerprint(
    *,
    constraint_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
) -> str:
    return _hash(
        {
            "mutation_kind": "retire",
            "constraint_ref": str(constraint_ref),
            "expected_material_state_ref": str(expected_material_state_ref),
            "effect": "no-current-rule",
        }
    )


def _constraint_name(exc: IntegrityError) -> str | None:
    diagnostic = getattr(exc.orig, "diag", None)
    value = getattr(diagnostic, "constraint_name", None)
    return value if isinstance(value, str) else None


def _subject_kind(value: object) -> TemporalConstraintSubjectKind:
    if value not in {"activity", "event"}:
        raise TemporalConstraintPersistenceError(
            "Stored Temporal Constraint subject family is outside B04."
        )
    return cast(TemporalConstraintSubjectKind, str(value))


def _constraint_from_row(row: RowMapping) -> TemporalConstraintView:
    constraint_ref = ScopedRecordRef(UUID(str(row["constraint_ref"])))
    subject_native_ref = NativeRef(UUID(str(row["subject_native_ref"])))
    subject_kind = _subject_kind(row["subject_kind"])
    material_state_value = row["material_state_ref"]
    if material_state_value is None:
        return TemporalConstraintView(
            constraint_ref=constraint_ref,
            subject_native_ref=subject_native_ref,
            subject_kind=subject_kind,
            status="retired",
            current_rule=None,
        )

    material_state_ref = MaterialStateRef(UUID(str(material_state_value)))
    family_value = row["family_code"]
    facet_value = row["constrained_facet_code"]
    strength_value = row["strength_code"]
    if strength_value not in {"hard", "soft"}:
        raise TemporalConstraintPersistenceError("Stored Temporal Constraint strength is invalid.")

    if family_value == "boundary":
        boundary_kind_value = row["boundary_kind_code"]
        form_value = row["boundary_temporal_form_code"]
        boundary_value = row["boundary_at"]
        if (
            form_value != "absolute"
            or boundary_kind_value not in {"earliest_start", "latest_start", "latest_completion"}
            or facet_value not in {"schedule.start", "schedule.completion"}
            or not _admitted_boundary_pair(str(boundary_kind_value), str(facet_value))
            or not isinstance(boundary_value, datetime)
        ):
            raise TemporalConstraintPersistenceError(
                "Stored current boundary rule is outside the activated B04-B shape."
            )
        try:
            boundary_at = normalize_utc_instant(boundary_value)
        except ValueError as exc:
            raise TemporalConstraintPersistenceError(
                "Stored Temporal Constraint absolute boundary is not a valid instant."
            ) from exc
        current_rule: TemporalConstraintCurrentRuleView = TemporalConstraintCurrentBoundaryRuleView(
            material_state_ref=material_state_ref,
            family="boundary",
            boundary_kind=cast(TemporalConstraintBoundaryKind, str(boundary_kind_value)),
            constrained_facet=cast(TemporalConstraintFacet, str(facet_value)),
            strength=cast(TemporalConstraintStrength, str(strength_value)),
            temporal_form="absolute",
            boundary_at=boundary_at,
        )
    elif family_value == "window":
        relationship_value = row["relationship_code"]
        form_value = row["window_temporal_form_code"]
        starts_value = row["starts_at"]
        ends_value = row["ends_at"]
        if (
            form_value != "absolute"
            or relationship_value not in {
                "start_within",
                "completion_within",
                "full_placement_contained",
                "placement_overlaps",
            }
            or facet_value not in {"schedule.start", "schedule.completion", "schedule.placement"}
            or not _admitted_window_pair(str(relationship_value), str(facet_value))
            or not isinstance(starts_value, datetime)
            or not isinstance(ends_value, datetime)
        ):
            raise TemporalConstraintPersistenceError(
                "Stored current window rule is outside the activated B04-C shape."
            )
        try:
            starts_at = normalize_utc_instant(starts_value)
            ends_at = normalize_utc_instant(ends_value)
        except ValueError as exc:
            raise TemporalConstraintPersistenceError(
                "Stored Temporal Constraint absolute window is not valid."
            ) from exc
        if ends_at <= starts_at:
            raise TemporalConstraintPersistenceError(
                "Stored Temporal Constraint absolute window is not positive."
            )
        current_rule = TemporalConstraintCurrentWindowRuleView(
            material_state_ref=material_state_ref,
            family="window",
            relationship=cast(TemporalConstraintWindowRelationship, str(relationship_value)),
            constrained_facet=cast(TemporalConstraintFacet, str(facet_value)),
            strength=cast(TemporalConstraintStrength, str(strength_value)),
            temporal_form="absolute",
            starts_at=starts_at,
            ends_at=ends_at,
        )
    else:
        raise TemporalConstraintPersistenceError(
            "Stored current Temporal Constraint family is outside the activated B04-C shape."
        )

    return TemporalConstraintView(
        constraint_ref=constraint_ref,
        subject_native_ref=subject_native_ref,
        subject_kind=subject_kind,
        status="active",
        current_rule=current_rule,
    )


async def _subject_kind_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    subject_native_ref: NativeRef,
) -> TemporalConstraintSubjectKind | None:
    value = (
        await database_session.execute(
            _SUBJECT_KIND_SQL,
            {"self_person_ref": self_person_ref, "subject_native_ref": subject_native_ref},
        )
    ).scalar_one_or_none()
    return None if value is None else _subject_kind(value)


async def _constraint_identity_in_session(
    database_session: AsyncSession,
    *,
    self_person_ref: NativeRef,
    constraint_ref: ScopedRecordRef,
) -> tuple[NativeRef, TemporalConstraintSubjectKind] | None:
    row = (
        (
            await database_session.execute(
                _CONSTRAINT_IDENTITY_SQL,
                {"self_person_ref": self_person_ref, "constraint_ref": constraint_ref},
            )
        )
        .mappings()
        .one_or_none()
    )
    if row is None:
        return None
    return (
        NativeRef(UUID(str(row["subject_native_ref"]))),
        _subject_kind(row["subject_kind"]),
    )


async def _expected_family_in_session(
    database_session: AsyncSession,
    *,
    constraint_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef,
) -> TemporalConstraintFamily | None:
    value = (
        await database_session.execute(
            _EXPECTED_FAMILY_SQL,
            {
                "constraint_ref": constraint_ref,
                "material_state_ref": expected_material_state_ref,
            },
        )
    ).scalar_one_or_none()
    if value in {"boundary", "window"}:
        return cast(TemporalConstraintFamily, str(value))
    return None


async def _mutate_in_session(
    database_session: AsyncSession,
    *,
    family: TemporalConstraintFamily,
    self_person_ref: NativeRef,
    operation_id: str,
    fingerprint: str,
    mutation_kind: MutationKind,
    subject_native_ref: NativeRef,
    constraint_ref: ScopedRecordRef,
    expected_material_state_ref: MaterialStateRef | None,
    resulting_material_state_ref: MaterialStateRef | None,
    rule: TemporalConstraintRule | None,
) -> RowMapping:
    common = {
        "self_person_ref": self_person_ref,
        "operation_id": operation_id,
        "intent_fingerprint": fingerprint,
        "mutation_kind": mutation_kind,
        "subject_native_ref": subject_native_ref,
        "constraint_ref": constraint_ref,
        "expected_material_state_ref": expected_material_state_ref,
        "resulting_material_state_ref": resulting_material_state_ref,
    }
    if family == "window":
        window_rule = rule if isinstance(rule, AbsoluteWindowRule) else None
        statement = _MUTATE_WINDOW_SQL
        parameters = {
            **common,
            "relationship_code": None if window_rule is None else window_rule.relationship,
            "constrained_facet_code": None if window_rule is None else window_rule.constrained_facet,
            "strength_code": None if window_rule is None else window_rule.strength,
            "starts_at": None if window_rule is None else window_rule.starts_at,
            "ends_at": None if window_rule is None else window_rule.ends_at,
        }
    else:
        boundary_rule = None if isinstance(rule, AbsoluteWindowRule) else rule
        statement = _MUTATE_BOUNDARY_SQL
        parameters = {
            **common,
            "boundary_kind_code": None if boundary_rule is None else boundary_rule.boundary_kind,
            "constrained_facet_code": None if boundary_rule is None else boundary_rule.constrained_facet,
            "strength_code": None if boundary_rule is None else boundary_rule.strength,
            "boundary_at": None if boundary_rule is None else boundary_rule.boundary_at,
        }
    return (await database_session.execute(statement, parameters)).mappings().one()


def _raise_integrity(exc: IntegrityError, *, allow_state_conflict: bool) -> None:
    constraint = _constraint_name(exc)
    if constraint == "pk_temporal_constraint_mutation_operation":
        raise TemporalConstraintOperationIdReuseError() from exc
    if allow_state_conflict and constraint == "temporal_constraint_state_conflict":
        raise TemporalConstraintStateConflictError() from exc
    raise TemporalConstraintPersistenceError() from exc


def _evaluate_current_rule(
    constraint: TemporalConstraintView,
    placement: AbsoluteIntervalPlacement,
) -> TemporalConstraintEvaluationItem:
    rule = constraint.current_rule
    if rule is None:
        raise TemporalConstraintPersistenceError(
            "Retired Temporal Constraint cannot be evaluated as current."
        )
    satisfied: bool
    reason: str
    if isinstance(rule, TemporalConstraintCurrentBoundaryRuleView):
        if rule.boundary_kind == "earliest_start":
            satisfied = placement.starts_at >= rule.boundary_at
            reason = "schedule_start_at_or_after_earliest" if satisfied else "schedule_start_before_earliest"
        elif rule.boundary_kind == "latest_start":
            satisfied = placement.starts_at <= rule.boundary_at
            reason = "schedule_start_at_or_before_latest" if satisfied else "schedule_start_after_latest"
        else:
            satisfied = placement.ends_at <= rule.boundary_at
            reason = "schedule_completion_at_or_before_latest" if satisfied else "schedule_completion_after_latest"
        return TemporalConstraintEvaluationItem(
            constraint_ref=constraint.constraint_ref,
            material_state_ref=rule.material_state_ref,
            family="boundary",
            rule_code=rule.boundary_kind,
            constrained_facet=rule.constrained_facet,
            strength=rule.strength,
            evaluation="satisfied" if satisfied else "violated",
            reason_code=reason,
        )

    if rule.relationship == "start_within":
        satisfied = rule.starts_at <= placement.starts_at <= rule.ends_at
        reason = "schedule_start_within_window" if satisfied else "schedule_start_outside_window"
    elif rule.relationship == "completion_within":
        satisfied = rule.starts_at <= placement.ends_at <= rule.ends_at
        reason = "schedule_completion_within_window" if satisfied else "schedule_completion_outside_window"
    elif rule.relationship == "full_placement_contained":
        satisfied = placement.starts_at >= rule.starts_at and placement.ends_at <= rule.ends_at
        reason = "schedule_placement_contained" if satisfied else "schedule_placement_not_contained"
    else:
        satisfied = placement.starts_at < rule.ends_at and placement.ends_at > rule.starts_at
        reason = "schedule_placement_positive_overlap" if satisfied else "schedule_placement_no_positive_overlap"
    return TemporalConstraintEvaluationItem(
        constraint_ref=constraint.constraint_ref,
        material_state_ref=rule.material_state_ref,
        family="window",
        rule_code=rule.relationship,
        constrained_facet=rule.constrained_facet,
        strength=rule.strength,
        evaluation="satisfied" if satisfied else "violated",
        reason_code=reason,
    )


@dataclass(slots=True)
class _Bound:
    value: datetime | None = None
    strict: bool = False


def _raise_lower(bound: _Bound, value: datetime, *, strict: bool = False) -> None:
    if bound.value is None or value > bound.value:
        bound.value = value
        bound.strict = strict
    elif value == bound.value:
        bound.strict = bound.strict or strict


def _lower_upper_infeasible(lower: _Bound, upper: _Bound) -> bool:
    if lower.value is None or upper.value is None:
        return False
    if lower.value > upper.value:
        return True
    return lower.value == upper.value and (lower.strict or upper.strict)


def _lower_upper(bound: _Bound, value: datetime, *, strict: bool = False) -> None:
    if bound.value is None or value < bound.value:
        bound.value = value
        bound.strict = strict
    elif value == bound.value:
        bound.strict = bound.strict or strict


def _hard_set_status(constraints: list[TemporalConstraintView]) -> HardSetStatus:
    start_lower = _Bound()
    start_upper = _Bound()
    completion_lower = _Bound()
    completion_upper = _Bound()
    for constraint in constraints:
        rule = constraint.current_rule
        if rule is None or rule.strength != "hard":
            continue
        if isinstance(rule, TemporalConstraintCurrentBoundaryRuleView):
            if rule.boundary_kind == "earliest_start":
                _raise_lower(start_lower, rule.boundary_at)
            elif rule.boundary_kind == "latest_start":
                _lower_upper(start_upper, rule.boundary_at)
            elif rule.boundary_kind == "latest_completion":
                _lower_upper(completion_upper, rule.boundary_at)
            else:
                return "undetermined"
        elif isinstance(rule, TemporalConstraintCurrentWindowRuleView):
            if rule.relationship == "start_within":
                _raise_lower(start_lower, rule.starts_at)
                _lower_upper(start_upper, rule.ends_at)
            elif rule.relationship == "completion_within":
                _raise_lower(completion_lower, rule.starts_at)
                _lower_upper(completion_upper, rule.ends_at)
            elif rule.relationship == "full_placement_contained":
                _raise_lower(start_lower, rule.starts_at)
                _lower_upper(completion_upper, rule.ends_at)
            elif rule.relationship == "placement_overlaps":
                _lower_upper(start_upper, rule.ends_at, strict=True)
                _raise_lower(completion_lower, rule.starts_at, strict=True)
            else:
                return "undetermined"
        else:
            return "undetermined"

    if _lower_upper_infeasible(start_lower, start_upper):
        return "infeasible"
    if _lower_upper_infeasible(completion_lower, completion_upper):
        return "infeasible"
    if (
        start_lower.value is not None
        and completion_upper.value is not None
        and start_lower.value >= completion_upper.value
    ):
        return "infeasible"
    return "feasible"


class TemporalConstraintApplication:
    """Transaction-owning Temporal Constraint commands, reads and derived evaluation."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create_constraint(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        subject_native_ref: NativeRef,
        rule: TemporalConstraintRule,
    ) -> CreatedTemporalConstraintView:
        normalized_operation_id = _normalize_operation_id(operation_id)
        _require_uuid7(subject_native_ref, label="Temporal Constraint subject reference")
        family = _rule_family(rule)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                subject_kind = await _subject_kind_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    subject_native_ref=subject_native_ref,
                )
                if subject_kind is None:
                    raise TemporalConstraintNotFoundError()
                row = await _mutate_in_session(
                    database_session,
                    family=family,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    fingerprint=_create_fingerprint(
                        subject_native_ref=subject_native_ref,
                        rule=rule,
                    ),
                    mutation_kind="create",
                    subject_native_ref=subject_native_ref,
                    constraint_ref=new_scoped_record_ref(),
                    expected_material_state_ref=None,
                    resulting_material_state_ref=new_material_state_ref(),
                    rule=rule,
                )
        except IntegrityError as exc:
            _raise_integrity(exc, allow_state_conflict=False)
        except DBAPIError as exc:
            raise TemporalConstraintPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise TemporalConstraintPersistenceError() from exc

        material_state_ref = row["material_state_ref"]
        if material_state_ref is None or row["active"] is not True:
            raise TemporalConstraintPersistenceError(
                "Temporal Constraint create did not return an active rule state."
            )
        return CreatedTemporalConstraintView(
            constraint_ref=ScopedRecordRef(UUID(str(row["constraint_ref"]))),
            subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
            subject_kind=subject_kind,
            material_state_ref=MaterialStateRef(UUID(str(material_state_ref))),
            rule=rule,
            recorded_at=cast(datetime, row["created_at"]),
            replayed=bool(row["replayed"]),
        )

    async def revise_constraint(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        constraint_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
        rule: TemporalConstraintRule,
    ) -> RevisedTemporalConstraintView:
        normalized_operation_id = _normalize_operation_id(operation_id)
        _require_uuid7(constraint_ref, label="Temporal Constraint reference")
        _require_uuid7(expected_material_state_ref, label="Expected Temporal Constraint state reference")
        family = _rule_family(rule)
        try:
            async with self._session_factory() as database_session, database_session.begin():
                identity = await _constraint_identity_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    constraint_ref=constraint_ref,
                )
                if identity is None:
                    raise TemporalConstraintNotFoundError()
                subject_native_ref, subject_kind = identity
                row = await _mutate_in_session(
                    database_session,
                    family=family,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    fingerprint=_revise_fingerprint(
                        constraint_ref=constraint_ref,
                        expected_material_state_ref=expected_material_state_ref,
                        rule=rule,
                    ),
                    mutation_kind="revise",
                    subject_native_ref=subject_native_ref,
                    constraint_ref=constraint_ref,
                    expected_material_state_ref=expected_material_state_ref,
                    resulting_material_state_ref=new_material_state_ref(),
                    rule=rule,
                )
        except IntegrityError as exc:
            _raise_integrity(exc, allow_state_conflict=True)
        except DBAPIError as exc:
            raise TemporalConstraintPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise TemporalConstraintPersistenceError() from exc

        material_state_ref = row["material_state_ref"]
        if material_state_ref is None or row["active"] is not True:
            raise TemporalConstraintPersistenceError(
                "Temporal Constraint revision did not return an active rule state."
            )
        return RevisedTemporalConstraintView(
            constraint_ref=ScopedRecordRef(UUID(str(row["constraint_ref"]))),
            subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
            subject_kind=subject_kind,
            previous_material_state_ref=expected_material_state_ref,
            material_state_ref=MaterialStateRef(UUID(str(material_state_ref))),
            rule=rule,
            recorded_at=cast(datetime, row["created_at"]),
            replayed=bool(row["replayed"]),
        )

    async def retire_constraint(
        self,
        *,
        self_person_ref: NativeRef,
        operation_id: str,
        constraint_ref: ScopedRecordRef,
        expected_material_state_ref: MaterialStateRef,
    ) -> RetiredTemporalConstraintView:
        normalized_operation_id = _normalize_operation_id(operation_id)
        _require_uuid7(constraint_ref, label="Temporal Constraint reference")
        _require_uuid7(expected_material_state_ref, label="Expected Temporal Constraint state reference")
        try:
            async with self._session_factory() as database_session, database_session.begin():
                identity = await _constraint_identity_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    constraint_ref=constraint_ref,
                )
                if identity is None:
                    raise TemporalConstraintNotFoundError()
                subject_native_ref, subject_kind = identity
                family = await _expected_family_in_session(
                    database_session,
                    constraint_ref=constraint_ref,
                    expected_material_state_ref=expected_material_state_ref,
                )
                if family is None:
                    raise TemporalConstraintStateConflictError()
                row = await _mutate_in_session(
                    database_session,
                    family=family,
                    self_person_ref=self_person_ref,
                    operation_id=normalized_operation_id,
                    fingerprint=_retire_fingerprint(
                        constraint_ref=constraint_ref,
                        expected_material_state_ref=expected_material_state_ref,
                    ),
                    mutation_kind="retire",
                    subject_native_ref=subject_native_ref,
                    constraint_ref=constraint_ref,
                    expected_material_state_ref=expected_material_state_ref,
                    resulting_material_state_ref=None,
                    rule=None,
                )
        except IntegrityError as exc:
            _raise_integrity(exc, allow_state_conflict=True)
        except DBAPIError as exc:
            raise TemporalConstraintPersistenceError() from exc
        except SQLAlchemyError as exc:
            raise TemporalConstraintPersistenceError() from exc

        if row["material_state_ref"] is not None or row["active"] is not False:
            raise TemporalConstraintPersistenceError(
                "Temporal Constraint retirement returned an invalid active-state shape."
            )
        return RetiredTemporalConstraintView(
            constraint_ref=ScopedRecordRef(UUID(str(row["constraint_ref"]))),
            subject_native_ref=NativeRef(UUID(str(row["subject_native_ref"]))),
            subject_kind=subject_kind,
            previous_material_state_ref=expected_material_state_ref,
            recorded_at=cast(datetime, row["created_at"]),
            replayed=bool(row["replayed"]),
        )

    async def get_constraint(
        self,
        *,
        self_person_ref: NativeRef,
        constraint_ref: ScopedRecordRef,
    ) -> TemporalConstraintView:
        _require_uuid7(constraint_ref, label="Temporal Constraint reference")
        statement = text(_READ_CONSTRAINT_BASE + " AND constraint_row.constraint_ref=:constraint_ref")
        try:
            async with self._session_factory() as database_session, database_session.begin():
                row = (
                    (
                        await database_session.execute(
                            statement,
                            {"self_person_ref": self_person_ref, "constraint_ref": constraint_ref},
                        )
                    )
                    .mappings()
                    .one_or_none()
                )
        except SQLAlchemyError as exc:
            raise TemporalConstraintPersistenceError() from exc
        if row is None:
            raise TemporalConstraintNotFoundError()
        return _constraint_from_row(row)

    async def list_constraints_by_subject(
        self,
        *,
        self_person_ref: NativeRef,
        subject_native_ref: NativeRef,
    ) -> list[TemporalConstraintView]:
        _require_uuid7(subject_native_ref, label="Temporal Constraint subject reference")
        statement = text(
            _READ_CONSTRAINT_BASE
            + " AND constraint_row.subject_native_ref=:subject_native_ref"
            + " ORDER BY constraint_row.constraint_ref"
        )
        try:
            async with self._session_factory() as database_session, database_session.begin():
                subject_kind = await _subject_kind_in_session(
                    database_session,
                    self_person_ref=self_person_ref,
                    subject_native_ref=subject_native_ref,
                )
                if subject_kind is None:
                    raise TemporalConstraintNotFoundError()
                rows = (
                    (
                        await database_session.execute(
                            statement,
                            {
                                "self_person_ref": self_person_ref,
                                "subject_native_ref": subject_native_ref,
                            },
                        )
                    )
                    .mappings()
                    .all()
                )
        except SQLAlchemyError as exc:
            raise TemporalConstraintPersistenceError() from exc
        return [_constraint_from_row(row) for row in rows]

    async def evaluate_constraints(
        self,
        *,
        self_person_ref: NativeRef,
        subject_native_ref: NativeRef,
        placement: AbsoluteIntervalPlacement,
    ) -> TemporalConstraintEvaluationView:
        constraints = await self.list_constraints_by_subject(
            self_person_ref=self_person_ref,
            subject_native_ref=subject_native_ref,
        )
        active = [value for value in constraints if value.current_rule is not None]
        items = tuple(_evaluate_current_rule(value, placement) for value in active)
        hard_set_status = _hard_set_status(active)
        if any(item.strength == "hard" and item.evaluation == "not_evaluable" for item in items):
            status: ConstraintSetEvaluationStatus = "not_evaluable"
        elif any(item.strength == "hard" and item.evaluation == "violated" for item in items):
            status = "inadmissible"
        elif any(item.strength == "soft" and item.evaluation == "violated" for item in items):
            status = "admissible_with_soft_violations"
        else:
            status = "admissible"
        return TemporalConstraintEvaluationView(
            subject_native_ref=subject_native_ref,
            placement=placement,
            status=status,
            hard_set_status=hard_set_status,
            items=items,
        )
