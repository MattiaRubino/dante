"""Unit acceptance for the immutable recovery suppression ledger."""

from datetime import UTC, datetime
import json
from pathlib import Path
from uuid import uuid7

import pytest

from dante.platform.recovery.suppression_ledger import (
    RecoverySuppressionBlocked,
    commit_after_canonical_verification,
    load_committed_suppressions,
    prepare_suppression,
)


def _prepare(root: Path):
    suppression_ref = uuid7()
    material_ref = uuid7()
    prepared = prepare_suppression(
        root,
        recovery_suppression_ref=suppression_ref,
        material_state_ref=material_ref,
        facet_code="session.timing",
        retirement_code="redacted",
        accepted_at=datetime.now(UTC),
    )
    return suppression_ref, material_ref, prepared


def test_prepared_without_commit_blocks_recovery(tmp_path: Path) -> None:
    _prepare(tmp_path)
    with pytest.raises(RecoverySuppressionBlocked, match="prepared_without_commit"):
        load_committed_suppressions(tmp_path)


def test_commit_requires_verified_canonical_target(tmp_path: Path) -> None:
    suppression_ref, _, _ = _prepare(tmp_path)
    with pytest.raises(RecoverySuppressionBlocked, match="does not match"):
        commit_after_canonical_verification(
            tmp_path,
            recovery_suppression_ref=suppression_ref,
            verified_material_state_ref=uuid7(),
            committed_at=datetime.now(UTC),
        )


def test_committed_pair_round_trips_and_is_immutable(tmp_path: Path) -> None:
    suppression_ref, material_ref, prepared = _prepare(tmp_path)
    commit_after_canonical_verification(
        tmp_path,
        recovery_suppression_ref=suppression_ref,
        verified_material_state_ref=material_ref,
        committed_at=datetime.now(UTC),
    )
    assert load_committed_suppressions(tmp_path) == (prepared,)
    with pytest.raises(RecoverySuppressionBlocked, match="already exists"):
        commit_after_canonical_verification(
            tmp_path,
            recovery_suppression_ref=suppression_ref,
            verified_material_state_ref=material_ref,
            committed_at=datetime.now(UTC),
        )


def test_tampered_prepared_hash_blocks_recovery(tmp_path: Path) -> None:
    suppression_ref, material_ref, _ = _prepare(tmp_path)
    commit_after_canonical_verification(
        tmp_path,
        recovery_suppression_ref=suppression_ref,
        verified_material_state_ref=material_ref,
        committed_at=datetime.now(UTC),
    )
    prepared_path = tmp_path / "records" / f"{suppression_ref}.prepared.json"
    value = json.loads(prepared_path.read_text(encoding="utf-8"))
    value["retirement_code"] = "unavailable"
    prepared_path.chmod(0o640)
    prepared_path.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    with pytest.raises(RecoverySuppressionBlocked, match="hash mismatch"):
        load_committed_suppressions(tmp_path)


def test_committed_without_prepared_blocks_recovery(tmp_path: Path) -> None:
    records = tmp_path / "records"
    records.mkdir(parents=True)
    suppression_ref = uuid7()
    material_ref = uuid7()
    value = {
        "record_version": 1,
        "state": "COMMITTED",
        "recovery_suppression_ref": str(suppression_ref),
        "material_state_ref": str(material_ref),
        "prepared_sha256": "0" * 64,
        "committed_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
    (records / f"{suppression_ref}.committed.json").write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(RecoverySuppressionBlocked, match="committed_without_prepare"):
        load_committed_suppressions(tmp_path)
