"""Unit acceptance for request-local resource-control contracts."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.resource import (
    ResourceAdmission,
    ResourceAdmissionOutcome,
    ResourceAdmissionRequest,
    ResourceEstimate,
    ResourceEstimateRequest,
    ResourceMeasure,
    ResourceSettlement,
    ResourceSettlementRequest,
    ResourceSettlementStatus,
    ResourceUsageCertainty,
)
from tests.unit.modules.intelligence.fakes import ScriptedResourceControl


def _measure(certainty: ResourceUsageCertainty, amount: int | None) -> ResourceMeasure:
    return ResourceMeasure(
        dimension="model_tokens",
        unit="tokens",
        certainty=certainty,
        amount=amount,
    )


def test_unknown_usage_cannot_be_encoded_as_numeric_zero() -> None:
    with pytest.raises(ValueError, match="UNKNOWN"):
        _measure(ResourceUsageCertainty.UNKNOWN, 0)
    assert _measure(ResourceUsageCertainty.UNKNOWN, None).amount is None


def test_estimate_is_not_final_known_usage() -> None:
    with pytest.raises(ValueError, match="KNOWN final usage"):
        ResourceEstimate(
            estimate_id=uuid7(),
            request_id=uuid7(),
            measures=(_measure(ResourceUsageCertainty.KNOWN, 100),),
            basis_refs=("estimate:v1",),
            evaluated_at=datetime.now(UTC),
        )


def test_settlement_cannot_hide_unknown_usage_as_settled() -> None:
    with pytest.raises(ValueError, match="SETTLED"):
        ResourceSettlement(
            settlement_id=uuid7(),
            request_id=uuid7(),
            admission_id=uuid7(),
            status=ResourceSettlementStatus.SETTLED,
            measures=(_measure(ResourceUsageCertainty.UNKNOWN, None),),
            evidence_refs=("usage:evidence",),
            settled_at=datetime.now(UTC),
        )


@pytest.mark.asyncio
async def test_resource_fake_keeps_three_control_phases_distinct() -> None:
    work_id = uuid7()
    estimate_request = ResourceEstimateRequest(
        request_id=uuid7(),
        work_id=work_id,
        work_revision=1,
        route_candidate_ref="route:test",
        requested_measures=(_measure(ResourceUsageCertainty.ESTIMATED, 100),),
        created_at=datetime.now(UTC),
    )
    estimate = ResourceEstimate(
        estimate_id=uuid7(),
        request_id=estimate_request.request_id,
        measures=(_measure(ResourceUsageCertainty.ESTIMATED, 90),),
        basis_refs=("estimate:v1",),
        evaluated_at=datetime.now(UTC),
    )
    admission_request = ResourceAdmissionRequest(
        request_id=uuid7(),
        work_id=work_id,
        work_revision=1,
        estimate_id=estimate.estimate_id,
        route_ref="route:test",
        limit_refs=("request:max-attempts:1",),
        created_at=datetime.now(UTC),
    )
    admission = ResourceAdmission(
        admission_id=uuid7(),
        request_id=admission_request.request_id,
        outcome=ResourceAdmissionOutcome.ADMITTED,
        basis_refs=("resource:request-local:v1",),
        evaluated_at=datetime.now(UTC),
        admitted_limit_refs=admission_request.limit_refs,
    )
    settlement_request = ResourceSettlementRequest(
        request_id=uuid7(),
        admission_id=admission.admission_id,
        observed_measures=(_measure(ResourceUsageCertainty.KNOWN, 82),),
        usage_evidence_refs=("usage:attempt:1",),
        created_at=datetime.now(UTC),
    )
    settlement = ResourceSettlement(
        settlement_id=uuid7(),
        request_id=settlement_request.request_id,
        admission_id=admission.admission_id,
        status=ResourceSettlementStatus.SETTLED,
        measures=settlement_request.observed_measures,
        evidence_refs=settlement_request.usage_evidence_refs,
        settled_at=datetime.now(UTC),
    )
    control = ScriptedResourceControl(
        estimates={estimate_request.request_id: estimate},
        admissions={admission_request.request_id: admission},
        settlements={settlement_request.request_id: settlement},
    )

    assert await control.estimate(estimate_request) == estimate
    assert await control.admit(admission_request) == admission
    assert await control.settle(settlement_request) == settlement
