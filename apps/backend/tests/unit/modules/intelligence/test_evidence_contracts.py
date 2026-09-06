"""Unit acceptance for minimized runtime-evidence contracts."""

from dataclasses import fields
from datetime import UTC, datetime
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.evidence import RuntimeEvidenceEvent, RuntimeEvidenceKind
from tests.unit.modules.intelligence.fakes import RecordingRuntimeEvidencePort


def test_runtime_evidence_surface_has_no_raw_content_payload_field() -> None:
    field_names = {field.name for field in fields(RuntimeEvidenceEvent)}
    assert "payload" not in field_names
    assert "consumer_context" not in field_names
    assert "model_response" not in field_names
    assert "source_content" not in field_names


@pytest.mark.asyncio
async def test_runtime_evidence_fake_records_minimized_typed_event() -> None:
    event = RuntimeEvidenceEvent(
        event_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        kind=RuntimeEvidenceKind.PUBLICATION,
        outcome_code="withheld",
        occurred_at=datetime.now(UTC),
        correlation_refs=("publication:decision",),
        basis_refs=("policy:publication:v1",),
    )
    evidence = RecordingRuntimeEvidencePort()

    await evidence.emit(event)

    assert evidence.events == [event]
