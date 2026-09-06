"""Unit acceptance for verification contracts."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.verification import VerificationResult, VerificationStatus


def test_verified_requires_evidence_and_no_unresolved_limitation() -> None:
    with pytest.raises(ValueError, match="evidence_refs"):
        VerificationResult(
            verification_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            representation_ref="answer:v1",
            basis_manifest_id=uuid7(),
            status=VerificationStatus.VERIFIED,
            evaluated_at=datetime.now(UTC),
        )

    with pytest.raises(ValueError, match="limitations"):
        VerificationResult(
            verification_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            representation_ref="answer:v1",
            basis_manifest_id=uuid7(),
            status=VerificationStatus.VERIFIED,
            evaluated_at=datetime.now(UTC),
            evidence_refs=("deterministic:query:v1",),
            limitations=("still uncertain",),
        )


def test_limited_and_stale_outcomes_require_declared_limitation() -> None:
    with pytest.raises(ValueError, match="LIMITED"):
        VerificationResult(
            verification_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            representation_ref="answer:v1",
            basis_manifest_id=uuid7(),
            status=VerificationStatus.LIMITED,
            evaluated_at=datetime.now(UTC),
        )

    with pytest.raises(ValueError, match="stale/reread"):
        VerificationResult(
            verification_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            representation_ref="answer:v1",
            basis_manifest_id=uuid7(),
            status=VerificationStatus.NEEDS_REREAD,
            evaluated_at=datetime.now(UTC),
        )


def test_verified_result_is_bound_to_exact_representation_and_basis() -> None:
    result = VerificationResult(
        verification_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        representation_ref="answer:v1",
        basis_manifest_id=uuid7(),
        status=VerificationStatus.VERIFIED,
        evaluated_at=datetime.now(UTC),
        evidence_refs=("deterministic:query:v1",),
    )
    assert result.representation_ref == "answer:v1"
    assert result.evidence_refs == ("deterministic:query:v1",)
