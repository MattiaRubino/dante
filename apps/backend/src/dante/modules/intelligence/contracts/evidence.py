"""Minimized runtime-evidence contracts distinct from audit, telemetry and canonical truth."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class RuntimeEvidenceKind(StrEnum):
    """Typed operational evidence categories allowed at the C6 boundary."""

    WORK = "work"
    SEARCH = "search"
    SEMANTIC_QUERY = "semantic_query"
    REFERENCE_RESOLUTION = "reference_resolution"
    CONTEXT_READINESS = "context_readiness"
    BASIS = "basis"
    POLICY = "policy"
    ROUTE = "route"
    RESOURCE = "resource"
    MODEL_INVOCATION = "model_invocation"
    PROVIDER_ATTEMPT = "provider_attempt"
    EGRESS = "egress"
    VERIFICATION = "verification"
    EFFECT = "effect"
    PUBLICATION = "publication"


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
class RuntimeEvidenceMetric:
    """Non-sensitive numeric operational evidence such as token counts or latency."""

    name: str
    value: int

    def __post_init__(self) -> None:
        _require_text(self.name, name="metric name")
        if self.value < 0:
            raise ValueError("runtime evidence metric value must not be negative")


@dataclass(frozen=True, slots=True)
class RuntimeEvidenceEvent:
    """Minimized coded event with no raw request/context/source/model payload field."""

    event_id: UUID
    work_id: UUID
    work_revision: int
    kind: RuntimeEvidenceKind
    outcome_code: str
    occurred_at: datetime
    correlation_refs: tuple[str, ...] = ()
    basis_refs: tuple[str, ...] = ()
    limitation_codes: tuple[str, ...] = ()
    metrics: tuple[RuntimeEvidenceMetric, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.event_id, name="event_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.outcome_code, name="outcome_code")
        _require_aware(self.occurred_at, name="occurred_at")
        _require_texts(self.correlation_refs, name="correlation_refs")
        _require_texts(self.basis_refs, name="basis_refs")
        _require_texts(self.limitation_codes, name="limitation_codes")
        metric_names = tuple(metric.name for metric in self.metrics)
        if len(metric_names) != len(set(metric_names)):
            raise ValueError("runtime evidence metric names must be unique")
