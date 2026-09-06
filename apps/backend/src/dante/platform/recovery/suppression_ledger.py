"""Immutable filesystem suppression ledger used only by disaster-recovery reconciliation.

PostgreSQL remains the canonical DANTE persistence surface. This ledger carries the
minimum independently surviving fact required to prevent an older backup from silently
resurrecting payload that was later validly retired/redacted.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from uuid import UUID

_RECORD_VERSION = 1
_REFERENCE_FAMILY = "MaterialStateRef"
_EFFECT = "suppress_payload"
_ALLOWED_FACETS = frozenset(
    {
        "schedule.placement",
        "actual.realization",
        "session.timing",
        "routine.recurrence",
        "event.recurrence",
    }
)
_ALLOWED_RETIREMENT_CODES = frozenset({"redacted", "unavailable"})


class RecoverySuppressionError(RuntimeError):
    """Raised when suppression evidence is incomplete, ambiguous or tampered."""


@dataclass(frozen=True, slots=True)
class PreparedSuppression:
    """Durable intent written before the canonical retirement transaction commits."""

    record_version: int
    state: str
    recovery_suppression_ref: str
    target_reference_family: str
    material_state_ref: str
    facet_code: str
    effect: str
    retirement_code: str
    accepted_at: str


@dataclass(frozen=True, slots=True)
class CommittedSuppression:
    """Commit marker written only after canonical PostgreSQL retirement is verified."""

    record_version: int
    state: str
    recovery_suppression_ref: str
    material_state_ref: str
    prepared_sha256: str
    committed_at: str


def _utc_text(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("suppression timestamps must be timezone-aware")
    return value.astimezone(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _require_uuid7(value: UUID, *, name: str) -> None:
    if value.version != 7:
        raise ValueError(f"{name} must be UUIDv7")


def _canonical_bytes(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("utf-8")


def _sha256_hex(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _fsync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _create_immutable(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o440)
    except FileExistsError as exc:
        raise RecoverySuppressionError(f"suppression record already exists: {path.name}") from exc
    try:
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(fd)
    _fsync_directory(path.parent)


def _read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise RecoverySuppressionError(f"missing suppression record: {path.name}") from exc
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RecoverySuppressionError(f"invalid suppression JSON: {path.name}") from exc
    if not isinstance(value, dict):
        raise RecoverySuppressionError(f"suppression record is not an object: {path.name}")
    if raw != _canonical_bytes(value):
        raise RecoverySuppressionError(
            f"suppression record is not canonical/immutable: {path.name}"
        )
    return value, raw


def _prepared_path(root: Path, suppression_ref: UUID) -> Path:
    return root / "records" / f"{suppression_ref}.prepared.json"


def _committed_path(root: Path, suppression_ref: UUID) -> Path:
    return root / "records" / f"{suppression_ref}.committed.json"


def _validated_uuid7_text(value: Any, *, context: str) -> UUID:
    text = str(value)
    try:
        parsed = UUID(text)
    except ValueError as exc:
        raise RecoverySuppressionError(f"invalid {context} UUID") from exc
    if parsed.version != 7 or str(parsed) != text:
        raise RecoverySuppressionError(f"{context} must be canonical UUIDv7")
    return parsed


def _validated_timestamp(value: Any, *, context: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise RecoverySuppressionError(f"invalid {context} timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RecoverySuppressionError(f"{context} timestamp must be timezone-aware")
    return parsed


def _validate_prepared(value: dict[str, Any]) -> PreparedSuppression:
    required = {
        "record_version",
        "state",
        "recovery_suppression_ref",
        "target_reference_family",
        "material_state_ref",
        "facet_code",
        "effect",
        "retirement_code",
        "accepted_at",
    }
    if set(value) != required:
        raise RecoverySuppressionError("PREPARED suppression record has unexpected fields")
    if value["record_version"] != _RECORD_VERSION or value["state"] != "PREPARED":
        raise RecoverySuppressionError("invalid PREPARED suppression version/state")
    if value["target_reference_family"] != _REFERENCE_FAMILY or value["effect"] != _EFFECT:
        raise RecoverySuppressionError("invalid PREPARED suppression semantic contract")
    if value["facet_code"] not in _ALLOWED_FACETS:
        raise RecoverySuppressionError("invalid PREPARED material facet")
    if value["retirement_code"] not in _ALLOWED_RETIREMENT_CODES:
        raise RecoverySuppressionError("invalid PREPARED retirement code")
    _validated_uuid7_text(
        value["recovery_suppression_ref"], context="PREPARED suppression reference"
    )
    _validated_uuid7_text(value["material_state_ref"], context="PREPARED MaterialStateRef")
    _validated_timestamp(value["accepted_at"], context="PREPARED accepted_at")
    return PreparedSuppression(**value)


def _validate_committed(value: dict[str, Any]) -> CommittedSuppression:
    required = {
        "record_version",
        "state",
        "recovery_suppression_ref",
        "material_state_ref",
        "prepared_sha256",
        "committed_at",
    }
    if set(value) != required:
        raise RecoverySuppressionError("COMMITTED suppression record has unexpected fields")
    if value["record_version"] != _RECORD_VERSION or value["state"] != "COMMITTED":
        raise RecoverySuppressionError("invalid COMMITTED suppression version/state")
    digest = str(value["prepared_sha256"])
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise RecoverySuppressionError("invalid COMMITTED prepared SHA-256")
    _validated_uuid7_text(
        value["recovery_suppression_ref"], context="COMMITTED suppression reference"
    )
    _validated_uuid7_text(value["material_state_ref"], context="COMMITTED MaterialStateRef")
    _validated_timestamp(value["committed_at"], context="COMMITTED committed_at")
    return CommittedSuppression(**value)


def prepare_suppression(
    root: Path,
    *,
    recovery_suppression_ref: UUID,
    material_state_ref: UUID,
    facet_code: str,
    retirement_code: str,
    accepted_at: datetime,
) -> PreparedSuppression:
    """Persist PREPARED intent before attempting the canonical PostgreSQL retirement."""
    _require_uuid7(recovery_suppression_ref, name="recovery_suppression_ref")
    _require_uuid7(material_state_ref, name="material_state_ref")
    if facet_code not in _ALLOWED_FACETS:
        raise ValueError("unsupported MaterialState facet")
    if retirement_code not in _ALLOWED_RETIREMENT_CODES:
        raise ValueError("unsupported retirement code")
    record = PreparedSuppression(
        record_version=_RECORD_VERSION,
        state="PREPARED",
        recovery_suppression_ref=str(recovery_suppression_ref),
        target_reference_family=_REFERENCE_FAMILY,
        material_state_ref=str(material_state_ref),
        facet_code=facet_code,
        effect=_EFFECT,
        retirement_code=retirement_code,
        accepted_at=_utc_text(accepted_at),
    )
    _create_immutable(
        _prepared_path(root, recovery_suppression_ref), _canonical_bytes(asdict(record))
    )
    return record


def commit_after_canonical_verification(
    root: Path,
    *,
    recovery_suppression_ref: UUID,
    verified_material_state_ref: UUID,
    committed_at: datetime,
) -> CommittedSuppression:
    """Write COMMITTED only after the caller has read back the canonical DB retirement row."""
    _require_uuid7(recovery_suppression_ref, name="recovery_suppression_ref")
    _require_uuid7(verified_material_state_ref, name="verified_material_state_ref")
    prepared_value, prepared_raw = _read_json(_prepared_path(root, recovery_suppression_ref))
    prepared = _validate_prepared(prepared_value)
    if prepared.recovery_suppression_ref != str(recovery_suppression_ref):
        raise RecoverySuppressionError("PREPARED suppression identity mismatch")
    if prepared.material_state_ref != str(verified_material_state_ref):
        raise RecoverySuppressionError(
            "canonical verification does not match PREPARED MaterialStateRef"
        )
    committed = CommittedSuppression(
        record_version=_RECORD_VERSION,
        state="COMMITTED",
        recovery_suppression_ref=str(recovery_suppression_ref),
        material_state_ref=str(verified_material_state_ref),
        prepared_sha256=_sha256_hex(prepared_raw),
        committed_at=_utc_text(committed_at),
    )
    _create_immutable(
        _committed_path(root, recovery_suppression_ref), _canonical_bytes(asdict(committed))
    )
    return committed


def load_committed_suppressions(root: Path) -> tuple[PreparedSuppression, ...]:
    """Return verified committed suppressions; any ambiguity blocks recovery."""
    records = root / "records"
    if not records.is_dir():
        raise RecoverySuppressionError("suppression ledger records directory is unavailable")

    entries = tuple(records.iterdir())
    unexpected = sorted(
        path.name
        for path in entries
        if not path.is_file()
        or not (path.name.endswith(".prepared.json") or path.name.endswith(".committed.json"))
    )
    if unexpected:
        raise RecoverySuppressionError(f"unexpected suppression ledger entries: {unexpected}")

    prepared_paths = {
        path.name.removesuffix(".prepared.json"): path
        for path in entries
        if path.name.endswith(".prepared.json")
    }
    committed_paths = {
        path.name.removesuffix(".committed.json"): path
        for path in entries
        if path.name.endswith(".committed.json")
    }
    if set(prepared_paths) != set(committed_paths):
        missing_commit = sorted(set(prepared_paths) - set(committed_paths))
        missing_prepare = sorted(set(committed_paths) - set(prepared_paths))
        raise RecoverySuppressionError(
            "ambiguous suppression ledger: "
            f"prepared_without_commit={missing_commit}, committed_without_prepare={missing_prepare}"
        )

    verified: list[PreparedSuppression] = []
    material_state_refs: set[str] = set()
    for key in sorted(prepared_paths):
        file_ref = _validated_uuid7_text(key, context="suppression filename reference")
        prepared_value, prepared_raw = _read_json(prepared_paths[key])
        committed_value, _ = _read_json(committed_paths[key])
        prepared = _validate_prepared(prepared_value)
        committed = _validate_committed(committed_value)
        if prepared.recovery_suppression_ref != str(
            file_ref
        ) or committed.recovery_suppression_ref != str(file_ref):
            raise RecoverySuppressionError("suppression filename/content identity mismatch")
        if prepared.recovery_suppression_ref != committed.recovery_suppression_ref:
            raise RecoverySuppressionError("suppression PREPARED/COMMITTED identity mismatch")
        if prepared.material_state_ref != committed.material_state_ref:
            raise RecoverySuppressionError("suppression PREPARED/COMMITTED target mismatch")
        if committed.prepared_sha256 != _sha256_hex(prepared_raw):
            raise RecoverySuppressionError("suppression PREPARED hash mismatch")
        if prepared.material_state_ref in material_state_refs:
            raise RecoverySuppressionError(
                "ambiguous suppression ledger: duplicate MaterialStateRef target"
            )
        material_state_refs.add(prepared.material_state_ref)
        verified.append(prepared)
    return tuple(verified)
