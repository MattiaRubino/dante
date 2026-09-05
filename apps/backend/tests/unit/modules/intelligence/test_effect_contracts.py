"""Unit acceptance for the first read-only Effect boundary."""

from datetime import UTC, datetime
from uuid import uuid7

import pytest

from dante.modules.intelligence.contracts.effects import EffectDisposition, EffectOutcome
from dante.modules.intelligence.contracts.work import ConsequenceProfile


def test_read_only_work_materializes_only_explicit_no_effect() -> None:
    outcome = EffectOutcome(
        outcome_id=uuid7(),
        work_id=uuid7(),
        work_revision=1,
        consequence_profile=ConsequenceProfile.READ_ONLY,
        disposition=EffectDisposition.NO_EFFECT,
        evaluated_at=datetime.now(UTC),
    )
    assert outcome.disposition is EffectDisposition.NO_EFFECT


def test_read_only_work_rejects_proposed_or_executed_effect_semantics() -> None:
    with pytest.raises(ValueError, match="proposed or executed"):
        EffectOutcome(
            outcome_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            consequence_profile=ConsequenceProfile.READ_ONLY,
            disposition=EffectDisposition.NO_EFFECT,
            proposed_effect_refs=("effect:create-event",),
            evaluated_at=datetime.now(UTC),
        )

    with pytest.raises(ValueError, match="NO_EFFECT"):
        EffectOutcome(
            outcome_id=uuid7(),
            work_id=uuid7(),
            work_revision=1,
            consequence_profile=ConsequenceProfile.READ_ONLY,
            disposition=EffectDisposition.EXECUTED,
            evaluated_at=datetime.now(UTC),
        )
