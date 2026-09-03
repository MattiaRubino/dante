"""Immutable Work and request-local execution contracts for DANTE Intelligence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from dante.modules.intelligence.contracts.references import TargetRef


class ConsequenceProfile(StrEnum):
    """Consequence posture admitted by the first Intelligence vertical."""

    READ_ONLY = "read_only"


class WorkRelationshipKind(StrEnum):
    """Relationship of this request-owned WorkContract to earlier work."""

    INDEPENDENT = "independent"
    CONTINUATION = "continuation"
    SUPERSEDES = "supersedes"


class ExecutionStatus(StrEnum):
    """Request-local execution state, never Domain Actual/Outcome."""

    ACCEPTED = "accepted"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLATION_REQUESTED = "cancellation_requested"
    CANCELLED = "cancelled"
    SUPERSEDED = "superseded"


class ResultMaturity(StrEnum):
    """Runtime result maturity independent of provider completion."""

    PROVISIONAL = "provisional"
    VERIFIED = "verified"
    PUBLISHABLE = "publishable"
    REJECTED = "rejected"


class CleanupState(StrEnum):
    """Bounded request-local cleanup state."""

    NOT_STARTED = "not_started"
    RUNNING = "running"
    COMPLETE = "complete"


def _require_text(value: str, *, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_texts(values: tuple[str, ...], *, name: str) -> None:
    if any(not value or not value.strip() for value in values):
        raise ValueError(f"{name} entries must be non-empty")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


def _require_aware(value: datetime, *, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class WorkContract:
    """Authoritative immutable contract for one bounded request-owned piece of work."""

    work_id: UUID
    revision: int
    objective: str
    purpose: str
    principal_binding: str
    recipient: str
    surface: str
    requested_capabilities: tuple[str, ...]
    execution_deadline: datetime
    target_bindings: tuple[TargetRef, ...] = ()
    actor_binding: str | None = None
    represented_party_binding: str | None = None
    protected_constraints: tuple[str, ...] = ()
    consequence_profile: ConsequenceProfile = ConsequenceProfile.READ_ONLY
    approval_conditions: tuple[str, ...] = ()
    relationship: WorkRelationshipKind = WorkRelationshipKind.INDEPENDENT
    related_work_id: UUID | None = None

    def __post_init__(self) -> None:
        _require_uuid7(self.work_id, name="work_id")
        if self.revision <= 0:
            raise ValueError("revision must be positive")
        _require_text(self.objective, name="objective")
        _require_text(self.purpose, name="purpose")
        _require_text(self.principal_binding, name="principal_binding")
        _require_text(self.recipient, name="recipient")
        _require_text(self.surface, name="surface")
        _require_texts(self.requested_capabilities, name="requested_capabilities")
        _require_texts(self.protected_constraints, name="protected_constraints")
        _require_texts(self.approval_conditions, name="approval_conditions")
        _require_aware(self.execution_deadline, name="execution_deadline")

        if not self.requested_capabilities:
            raise ValueError("requested_capabilities must not be empty")
        if len(self.requested_capabilities) != len(set(self.requested_capabilities)):
            raise ValueError("requested_capabilities must not contain duplicates")
        if len(self.target_bindings) != len(set(self.target_bindings)):
            raise ValueError("target_bindings must not contain duplicates")

        if self.actor_binding is not None:
            _require_text(self.actor_binding, name="actor_binding")
        if self.represented_party_binding is not None:
            _require_text(
                self.represented_party_binding,
                name="represented_party_binding",
            )

        if self.consequence_profile is ConsequenceProfile.READ_ONLY and self.approval_conditions:
            raise ValueError("READ_ONLY WorkContract does not admit approval conditions")

        if self.relationship is WorkRelationshipKind.INDEPENDENT:
            if self.related_work_id is not None:
                raise ValueError("independent work must not carry related_work_id")
            return

        if self.related_work_id is None:
            raise ValueError("continuation/supersession requires related_work_id")
        _require_uuid7(self.related_work_id, name="related_work_id")
        if self.related_work_id == self.work_id:
            raise ValueError("work cannot relate to itself")


@dataclass(frozen=True, slots=True)
class RequestExecutionScope:
    """Immutable snapshot of bounded request-local execution state."""

    work_id: UUID
    work_revision: int
    deadline: datetime
    status: ExecutionStatus
    result_maturity: ResultMaturity
    cancellation_requested: bool
    publication_open: bool
    cleanup_state: CleanupState
    attached_task_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_aware(self.deadline, name="deadline")
        _require_texts(self.attached_task_refs, name="attached_task_refs")
        if len(self.attached_task_refs) != len(set(self.attached_task_refs)):
            raise ValueError("attached_task_refs must not contain duplicates")
        if self.cancellation_requested and self.status in {
            ExecutionStatus.ACCEPTED,
            ExecutionStatus.RUNNING,
        }:
            raise ValueError("cancellation_requested requires cancellation-aware execution status")
        if self.status is ExecutionStatus.CANCELLED and not self.cancellation_requested:
            raise ValueError("CANCELLED requires cancellation_requested")
