"""Unit acceptance for safe-publication contracts."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.publication import (
    PublicationDecision,
    PublicationDecisionStatus,
    PublicationResult,
    PublicationResultStatus,
)
from dante.modules.intelligence.contracts.verification import VerificationStatus
from dante.modules.intelligence.contracts.work import ResultMaturity


def _decision(
    *,
    status: PublicationDecisionStatus,
    maturity: ResultMaturity,
    verification: VerificationStatus,
    emergency_denied: bool = False,
    limitations: tuple[str, ...] = (),
) -> PublicationDecision:
    return PublicationDecision(
        decision_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        representation_ref="answer:final:v1",
        recipient="self",
        surface="private_in_app",
        status=status,
        result_maturity=maturity,
        verification_result_id=uuid7(),
        verification_status=verification,
        basis_manifest_id=uuid7(),
        policy_decision_id=uuid7(),
        work_current=True,
        access_current=True,
        basis_current=True,
        emergency_denied=emergency_denied,
        final_transform_rechecked=True,
        cumulative_disclosure_rechecked=True,
        evaluated_at=datetime.now(UTC),
        limitations=limitations,
    )


def test_publication_rejects_provisional_or_unverified_result() -> None:
    with pytest.raises(ValueError, match="PUBLISHABLE"):
        _decision(
            status=PublicationDecisionStatus.PUBLISH,
            maturity=ResultMaturity.PROVISIONAL,
            verification=VerificationStatus.VERIFIED,
        )

    with pytest.raises(ValueError, match="VERIFIED or LIMITED"):
        _decision(
            status=PublicationDecisionStatus.PUBLISH,
            maturity=ResultMaturity.PUBLISHABLE,
            verification=VerificationStatus.STALE,
        )


def test_emergency_deny_blocks_otherwise_publishable_result() -> None:
    with pytest.raises(ValueError, match="emergency deny"):
        _decision(
            status=PublicationDecisionStatus.PUBLISH,
            maturity=ResultMaturity.PUBLISHABLE,
            verification=VerificationStatus.VERIFIED,
            emergency_denied=True,
        )


def test_limited_publication_must_declare_recipient_safe_limitation() -> None:
    decision = _decision(
        status=PublicationDecisionStatus.PUBLISH_WITH_LIMITATIONS,
        maturity=ResultMaturity.PUBLISHABLE,
        verification=VerificationStatus.LIMITED,
        limitations=("source freshness is bounded",),
    )
    assert decision.limitations == ("source freshness is bounded",)


def test_withheld_publication_result_cannot_claim_externalization() -> None:
    with pytest.raises(ValueError, match="WITHHELD"):
        PublicationResult(
            result_id=uuid7(),
            decision_id=uuid7(),
            status=PublicationResultStatus.WITHHELD,
            representation_ref="answer:final:v1",
        )
