"""Provider-agnostic Semantic Query contracts for structured DANTE meaning."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Literal, Protocol
from uuid import UUID

from dante.modules.intelligence.contracts.context import (
    ContextStrategy,
    InformationGuarantee,
    InformationNeed,
    SourceCurrentness,
)
from dante.modules.intelligence.contracts.references import TargetRef


class SemanticQueryStatus(StrEnum):
    """Structured query outcome independent of DB/provider implementation."""

    SUCCEEDED = "succeeded"
    UNSUPPORTED = "unsupported"
    NOT_INTEGRATION_READY = "not_integration_ready"
    POLICY_BLOCKED = "policy_blocked"
    SOURCE_UNAVAILABLE = "source_unavailable"


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


type SemanticScalar = str | int | float | bool | UUID | datetime


@dataclass(frozen=True, slots=True)
class SemanticField:
    """One typed field in a semantic record payload."""

    name: str
    value: SemanticScalar

    def __post_init__(self) -> None:
        _require_text(self.name, name="field name")
        if isinstance(self.value, str):
            _require_text(self.value, name="field value")
        elif isinstance(self.value, datetime):
            _require_aware(self.value, name="field datetime")


@dataclass(frozen=True, slots=True)
class SemanticRecord:
    """Typed record payload returned by an owning capability query seam."""

    fields: tuple[SemanticField, ...]
    kind: Literal["record"] = "record"

    def __post_init__(self) -> None:
        if not self.fields:
            raise ValueError("record fields must not be empty")
        names = tuple(field.name for field in self.fields)
        if len(names) != len(set(names)):
            raise ValueError("record fields must not contain duplicate names")


@dataclass(frozen=True, slots=True)
class SemanticRecordSet:
    """Bounded typed record collection; not a generic JSON response."""

    records: tuple[SemanticRecord, ...]
    kind: Literal["record_set"] = "record_set"


@dataclass(frozen=True, slots=True)
class SemanticAggregate:
    """Typed deterministic aggregate payload."""

    metric: str
    value: SemanticScalar
    unit: str | None = None
    kind: Literal["aggregate"] = "aggregate"

    def __post_init__(self) -> None:
        _require_text(self.metric, name="metric")
        if isinstance(self.value, str):
            _require_text(self.value, name="aggregate value")
        elif isinstance(self.value, datetime):
            _require_aware(self.value, name="aggregate datetime")
        if self.unit is not None:
            _require_text(self.unit, name="unit")


type SemanticQueryPayload = SemanticRecord | SemanticRecordSet | SemanticAggregate


@dataclass(frozen=True, slots=True)
class SemanticQueryRequest:
    """Bounded semantic query request against an owning public typed seam."""

    query_id: UUID
    work_id: UUID
    work_revision: int
    information_need: InformationNeed
    strategy: ContextStrategy
    capability_contract_id: str
    purpose: str

    def __post_init__(self) -> None:
        _require_uuid7(self.query_id, name="query_id")
        _require_uuid7(self.work_id, name="work_id")
        if self.work_revision <= 0:
            raise ValueError("work_revision must be positive")
        _require_text(self.capability_contract_id, name="capability_contract_id")
        _require_text(self.purpose, name="purpose")
        if self.information_need.need_id != self.strategy.need_id:
            raise ValueError("strategy must target the request InformationNeed")
        if self.information_need.purpose != self.purpose:
            raise ValueError("InformationNeed purpose must match query purpose")
        if self.strategy.purpose != self.purpose:
            raise ValueError("ContextStrategy purpose must match query purpose")


@dataclass(frozen=True, slots=True)
class SemanticQueryOutcome:
    """Typed structured outcome preserving guarantee/currentness/basis semantics."""

    query_id: UUID
    status: SemanticQueryStatus
    payload: SemanticQueryPayload | None = None
    achieved_guarantee: InformationGuarantee | None = None
    source_bindings: tuple[TargetRef, ...] = ()
    currentness: SourceCurrentness | None = None
    basis_refs: tuple[str, ...] = ()
    coherence_evidence: tuple[str, ...] = ()
    source_standing: str | None = None
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_uuid7(self.query_id, name="query_id")
        _require_texts(self.basis_refs, name="basis_refs")
        _require_texts(self.coherence_evidence, name="coherence_evidence")
        _require_texts(self.limitations, name="limitations")
        if len(self.source_bindings) != len(set(self.source_bindings)):
            raise ValueError("source_bindings must not contain duplicates")
        if self.source_standing is not None:
            _require_text(self.source_standing, name="source_standing")

        if self.status is SemanticQueryStatus.SUCCEEDED:
            if self.payload is None:
                raise ValueError("SUCCEEDED requires payload")
            if self.achieved_guarantee is None:
                raise ValueError("SUCCEEDED requires achieved_guarantee")
            if self.currentness is None:
                raise ValueError("SUCCEEDED requires currentness")
            if self.source_standing is None:
                raise ValueError("SUCCEEDED requires source_standing")
            return

        if self.payload is not None or self.achieved_guarantee is not None:
            raise ValueError("non-success outcome must not carry payload/guarantee")


class SemanticQueryGateway(Protocol):
    """Application-owned gateway; implementation must use accepted owning query seams."""

    async def execute(self, request: SemanticQueryRequest) -> SemanticQueryOutcome: ...
