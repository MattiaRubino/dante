"""Unit acceptance for the immutable recovery suppression ledger."""

from datetime import UTC, datetime
import json
from pathlib import Path
from uuid import UUID, uuid7

import pytest

from dante.platform.recovery.suppression_ledger import (
    RecoverySuppressionBlocked,
    commit_after_canonical_verification,
    load_committed_suppressions,
    prepare_suppression,
)


def _canonical_write(path: Path, value: dict[str, object]) -> None:
    path.chmod(0o640)
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _prepare(root: Path, *, material_ref: UUID | None = None):
    suppression_ref = uuid7()
    target_ref = material_ref or uuid7()
    prepared = prepare_suppression(
        root,
        recovery_suppression_ref=suppression_ref,
        material_state_ref=target_ref,
        facet_code="session.timing",
        retirement_code="redacted",
        accepted_at=datetime.now(UTC),
    )
    return suppression_ref, target_ref, prepared


def _commit(root: Path, suppression_ref: UUID, material_ref: UUID) -> None:
    commit_after_canonical_verification(
        root,
        recovery_suppression_ref=suppression_ref,
        verified_material_state_ref=material_ref,
        committed_at=datetime.now(UTC),
    )


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
    _commit(tmp_path, suppression_ref, material_ref)
    assert load_committed_suppressions(tmp_path) == (prepared,)
    with pytest.raises(RecoverySuppressionBlocked, match="already exists"):
        _commit(tmp_path, suppression_ref, material_ref)


def test_tampered_prepared_hash_blocks_recovery(tmp_path: Path) -> None:
    suppression_ref, material_ref, _ = _prepare(tmp_path)
    _commit(tmp_path, suppression_ref, material_ref)
    prepared_path = tmp_path / "records" / f"{suppression_ref}.prepared.json"
    value = json.loads(prepared_path.read_text(encoding="utf-8"))
    value["retirement_code"] = "unavailable"
    _canonical_write(prepared_path, value)
    with pytest.raises(RecoverySuppressionBlocked, match="hash mismatch"):
        load_committed_suppressions(tmp_path)


def test_committed_without_prepared_blocks_recovery(tmp_path: Path) -> None:
    records = tmp_path / "records"
    records.mkdir(parents=True)
    suppression_ref = uuid7()
    material_ref = uuid7()
    value: dict[str, object] = {
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


def test_naive_record_timestamp_blocks_recovery(tmp_path: Path) -> None:
    suppression_ref, material_ref, _ = _prepare(tmp_path)
    _commit(tmp_path, suppression_ref, material_ref)
    prepared_path = tmp_path / "records" / f"{suppression_ref}.prepared.json"
    value = json.loads(prepared_path.read_text(encoding="utf-8"))
    value["accepted_at"] = "2026-08-30T18:00:00"
    _canonical_write(prepared_path, value)
    with pytest.raises(RecoverySuppressionBlocked, match="timezone-aware"):
        load_committed_suppressions(tmp_path)


def test_filename_content_identity_mismatch_blocks_recovery(tmp_path: Path) -> None:
    suppression_ref, material_ref, _ = _prepare(tmp_path)
    _commit(tmp_path, suppression_ref, material_ref)
    replacement_ref = uuid7()
    records = tmp_path / "records"
    (records / f"{suppression_ref}.prepared.json").rename(
        records / f"{replacement_ref}.prepared.json"
    )
    (records / f"{suppression_ref}.committed.json").rename(
        records / f"{replacement_ref}.committed.json"
    )
    with pytest.raises(RecoverySuppressionBlocked, match="filename/content identity mismatch"):
        load_committed_suppressions(tmp_path)


def test_duplicate_material_state_target_blocks_recovery(tmp_path: Path) -> None:
    material_ref = uuid7()
    first_ref, _, _ = _prepare(tmp_path, material_ref=material_ref)
    _commit(tmp_path, first_ref, material_ref)
    second_ref, _, _ = _prepare(tmp_path, material_ref=material_ref)
    _commit(tmp_path, second_ref, material_ref)
    with pytest.raises(RecoverySuppressionBlocked, match="duplicate MaterialStateRef"):
        load_committed_suppressions(tmp_path)
