"""Unit acceptance for request-local Work and execution contracts."""

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4, uuid7

import pytest

from dante.modules.intelligence.contracts.work import (
    CleanupState,
    ConsequenceProfile,
    ExecutionStatus,
    RequestExecutionScope,
    ResultMaturity,
    WorkContract,
    WorkRelationshipKind,
)


def _deadline() -> datetime:
    return datetime.now(UTC) + timedelta(minutes=5)


def _work(
    *,
    work_id: UUID | None = None,
    execution_deadline: datetime | None = None,
    approval_conditions: tuple[str, ...] = (),
    relationship: WorkRelationshipKind = WorkRelationshipKind.INDEPENDENT,
    related_work_id: UUID | None = None,
) -> WorkContract:
    return WorkContract(
        work_id=work_id or uuid7(),
        revision=1,
        objective="answer a bounded read-only question",
        purpose="ask_dante",
        principal_binding="principal:self",
        recipient="self",
        surface="web",
        requested_capabilities=("semantic_query",),
        execution_deadline=execution_deadline or _deadline(),
        approval_conditions=approval_conditions,
        relationship=relationship,
        related_work_id=related_work_id,
    )


def test_work_contract_requires_uuid7_and_timezone_aware_deadline() -> None:
    with pytest.raises(ValueError, match="UUIDv7"):
        _work(work_id=uuid4())
    with pytest.raises(ValueError, match="timezone-aware"):
        _work(execution_deadline=datetime.fromisoformat("2026-09-03T12:00:00"))


def test_first_vertical_work_is_read_only_and_has_no_approval_conditions() -> None:
    work = _work()
    assert work.consequence_profile is ConsequenceProfile.READ_ONLY
    assert work.approval_conditions == ()
    with pytest.raises(ValueError, match="does not admit approval"):
        _work(approval_conditions=("confirm",))


def test_work_relationship_requires_distinct_related_work_identity() -> None:
    with pytest.raises(ValueError, match="requires related_work_id"):
        _work(relationship=WorkRelationshipKind.SUPERSEDES)

    prior = uuid7()
    continuation = _work(
        relationship=WorkRelationshipKind.CONTINUATION,
        related_work_id=prior,
    )
    assert continuation.related_work_id == prior

    current = uuid7()
    with pytest.raises(ValueError, match="cannot relate to itself"):
        _work(
            work_id=current,
            relationship=WorkRelationshipKind.SUPERSEDES,
            related_work_id=current,
        )


def test_request_execution_scope_preserves_runtime_not_domain_state() -> None:
    scope = RequestExecutionScope(
        work_id=uuid7(),
        work_revision=1,
        deadline=_deadline(),
        status=ExecutionStatus.RUNNING,
        result_maturity=ResultMaturity.PROVISIONAL,
        cancellation_requested=False,
        publication_open=False,
        cleanup_state=CleanupState.NOT_STARTED,
        attached_task_refs=("task:context",),
    )
    assert scope.status is ExecutionStatus.RUNNING
    assert scope.result_maturity is ResultMaturity.PROVISIONAL


def test_cancelled_execution_requires_explicit_cancellation_request() -> None:
    with pytest.raises(ValueError, match="CANCELLED requires"):
        RequestExecutionScope(
            work_id=uuid7(),
            work_revision=1,
            deadline=_deadline(),
            status=ExecutionStatus.CANCELLED,
            result_maturity=ResultMaturity.REJECTED,
            cancellation_requested=False,
            publication_open=False,
            cleanup_state=CleanupState.COMPLETE,
        )
