"""Shared LOCAL/DEV account seeding primitives for pre-vertical dogfood and personas."""

from __future__ import annotations

import asyncio
import json
import os
from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid7

import psycopg
from psycopg import Connection
from psycopg.errors import UniqueViolation

from dante.auth.email import normalize_email
from dante.auth.passwords import PasswordKdf, normalize_password_for_authentication
from dante.platform.time import TimeZoneMode, TimeZonePolicy

_OWNER_ROLE = "dante_owner"
_RUNTIME_ROLE = "dante_runtime"
_SECRET_BYTES = 32
_ALLOWED_ENVIRONMENTS = frozenset({"local", "dev"})


class SeedConfigurationError(RuntimeError):
    """LOCAL/DEV seed configuration is absent or unsafe."""


class SeedAccountConflictError(RuntimeError):
    """Existing Auth state cannot be treated as the requested synthetic account."""


class SeedPasswordMismatchError(RuntimeError):
    """Existing account credential does not match the supplied seed password."""


class SeedContextConflictError(RuntimeError):
    """Existing DANTE application context conflicts with deterministic seed intent."""


@dataclass(frozen=True, slots=True)
class SeedDatabaseTarget:
    """Normal persistent DANTE database target used by LOCAL/DEV tooling."""

    host: str
    port: int
    name: str
    runtime_password: str


@dataclass(frozen=True, slots=True)
class SeededAccount:
    """Canonical Account/EmailIdentity/PasswordCredential identity returned by a seed run."""

    account_ref: UUID
    email_identity_ref: UUID
    password_credential_ref: UUID
    email_address: str
    created: bool


@dataclass(frozen=True, slots=True)
class SeededApplicationContext:
    """Persisted DANTE application context owned by one seeded Account."""

    account_ref: UUID
    self_person_ref: UUID
    timezone_policy: TimeZonePolicy


@dataclass(frozen=True, slots=True)
class _AccountSnapshot:
    account_ref: UUID
    status_code: str
    email_identity_ref: UUID
    email_address: str
    verified_at: datetime | None
    password_credential_ref: UUID | None
    verifier: str | None
    pepper_key_id: str | None


def require_seed_environment(value: str | None) -> str:
    """Permit persistent synthetic writes only in explicitly named LOCAL/DEV environments."""
    normalized = "" if value is None else value.strip().casefold()
    if normalized not in _ALLOWED_ENVIRONMENTS:
        raise SeedConfigurationError(
            "pre-vertical persistent seeding is allowed only when DANTE_ENV is local or dev"
        )
    return normalized


def database_target_from_environment(
    environ: Mapping[str, str] = os.environ,
) -> SeedDatabaseTarget:
    """Load the normal runtime database target while requiring the canonical runtime role."""
    require_seed_environment(environ.get("DANTE_ENV"))
    host = _required_trimmed(environ, "DANTE_DATABASE__HOST")
    name = _required_trimmed(environ, "DANTE_DATABASE__NAME")
    runtime_user = _required_trimmed(environ, "DANTE_DATABASE__USER")
    if runtime_user != _RUNTIME_ROLE:
        raise SeedConfigurationError(
            f"DANTE_DATABASE__USER must be exactly {_RUNTIME_ROLE} for pre-vertical seeding"
        )

    port_raw = environ.get("DANTE_DATABASE__PORT", "5432")
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise SeedConfigurationError("DANTE_DATABASE__PORT must be an integer") from exc
    if not 1 <= port <= 65_535:
        raise SeedConfigurationError("DANTE_DATABASE__PORT must be within 1..65535")

    runtime_password = environ.get("DANTE_DATABASE__PASSWORD")
    if runtime_password is None or not runtime_password:
        raise SeedConfigurationError("DANTE_DATABASE__PASSWORD is required")

    return SeedDatabaseTarget(
        host=host,
        port=port,
        name=name,
        runtime_password=runtime_password,
    )


def password_pepper_configuration_from_environment(
    environ: Mapping[str, str] = os.environ,
) -> tuple[str, dict[str, bytes]]:
    """Load the exact Auth password pepper ring used by the normal runtime."""
    current_key_id = _required_trimmed(
        environ,
        "DANTE_AUTH__PASSWORD_CURRENT_PEPPER_KEY_ID",
    )
    serialized = environ.get("DANTE_AUTH__PASSWORD_PEPPERS")
    if serialized is None:
        raise SeedConfigurationError("DANTE_AUTH__PASSWORD_PEPPERS is required")

    try:
        payload = json.loads(serialized)
    except json.JSONDecodeError as exc:
        raise SeedConfigurationError("DANTE_AUTH__PASSWORD_PEPPERS must be valid JSON") from exc
    if not isinstance(payload, dict) or not payload:
        raise SeedConfigurationError("DANTE_AUTH__PASSWORD_PEPPERS must be a non-empty object")

    ring: dict[str, bytes] = {}
    for raw_key_id, raw_secret in payload.items():
        if not isinstance(raw_key_id, str) or not raw_key_id or raw_key_id.strip() != raw_key_id:
            raise SeedConfigurationError("password pepper key IDs must be non-blank and trimmed")
        if not isinstance(raw_secret, str):
            raise SeedConfigurationError("password pepper values must be Base64URL strings")
        ring[raw_key_id] = _decode_canonical_secret(
            raw_secret,
            name=f"password pepper {raw_key_id}",
        )

    if current_key_id not in ring:
        raise SeedConfigurationError(
            "current password pepper key is absent from the configured ring"
        )
    return current_key_id, ring


def read_local_secret(path: Path) -> str:
    """Read one non-empty single-line secret from an ignored ``*.local`` file."""
    resolved = path.expanduser().resolve()
    if resolved.suffix != ".local":
        raise SeedConfigurationError("seed secret files must use the .local suffix")
    if not resolved.is_file():
        raise SeedConfigurationError(f"seed secret file does not exist: {resolved}")

    try:
        content = resolved.read_text(encoding="utf-8")
    except OSError as exc:
        raise SeedConfigurationError(f"cannot read seed secret file: {resolved}") from exc

    lines = content.splitlines()
    if len(lines) != 1 or not lines[0]:
        raise SeedConfigurationError("seed secret files must contain exactly one non-empty line")
    return lines[0]


def connect_migrator(target: SeedDatabaseTarget, *, password: str) -> Connection[Any]:
    """Open an autocommit migrator connection for bounded administrative seed writes."""
    return psycopg.connect(
        host=target.host,
        port=target.port,
        dbname=target.name,
        user="dante_migrator",
        password=password,
        connect_timeout=5,
        autocommit=True,
    )


def connect_runtime(target: SeedDatabaseTarget) -> Connection[Any]:
    """Open the normal runtime identity used to invoke the bounded PV-02 capability."""
    return psycopg.connect(
        host=target.host,
        port=target.port,
        dbname=target.name,
        user=_RUNTIME_ROLE,
        password=target.runtime_password,
        connect_timeout=5,
        autocommit=True,
    )


def seed_password_account(
    connection: Connection[Any],
    *,
    email: str,
    password: str,
    current_pepper_key_id: str,
    pepper_ring: dict[str, bytes],
    expected_account_ref: UUID | None = None,
) -> SeededAccount:
    """Create or verify one canonical password Account without silently mutating existing state."""
    normalized_email = normalize_email(email)
    snapshot = _read_account_snapshot(connection, normalized_email.comparison_key)
    if snapshot is not None:
        _verify_existing_account(
            snapshot,
            password=password,
            current_pepper_key_id=current_pepper_key_id,
            pepper_ring=pepper_ring,
            expected_account_ref=expected_account_ref,
        )
        return _seeded_account_from_snapshot(snapshot, created=False)

    verifier, pepper_key_id = _hash_new_password(
        password,
        current_pepper_key_id=current_pepper_key_id,
        pepper_ring=pepper_ring,
    )
    account_ref = expected_account_ref or uuid7()
    email_identity_ref = uuid7()
    password_credential_ref = uuid7()
    now = datetime.now(UTC)

    try:
        with connection.transaction():
            connection.execute(f"SET LOCAL ROLE {_OWNER_ROLE}")
            connection.execute(
                """
                INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at)
                VALUES (%s,'active',%s,NULL)
                """,
                (account_ref, now),
            )
            connection.execute(
                """
                INSERT INTO dante.email_identity(
                    email_identity_ref,account_ref,address,comparison_key,created_at,verified_at
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    email_identity_ref,
                    account_ref,
                    normalized_email.address,
                    normalized_email.comparison_key,
                    now,
                    now,
                ),
            )
            connection.execute(
                """
                INSERT INTO dante.password_credential(
                    password_credential_ref,account_ref,verifier,pepper_key_id,created_at,updated_at
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    password_credential_ref,
                    account_ref,
                    verifier,
                    pepper_key_id,
                    now,
                    now,
                ),
            )
    except UniqueViolation:
        # Product signup or a concurrent seed may have won the canonical email race. Re-read and
        # prove exact compatibility rather than treating the collision as permission to overwrite.
        snapshot = _read_account_snapshot(connection, normalized_email.comparison_key)
        if snapshot is None:
            raise
        _verify_existing_account(
            snapshot,
            password=password,
            current_pepper_key_id=current_pepper_key_id,
            pepper_ring=pepper_ring,
            expected_account_ref=expected_account_ref,
        )
        return _seeded_account_from_snapshot(snapshot, created=False)

    return SeededAccount(
        account_ref=account_ref,
        email_identity_ref=email_identity_ref,
        password_credential_ref=password_credential_ref,
        email_address=normalized_email.address,
        created=True,
    )


def ensure_account_application_context(
    connection: Connection[Any],
    *,
    account_ref: UUID,
    expected_self_person_ref: UUID | None = None,
) -> SeededApplicationContext:
    """Resolve or create the Account context through the bounded runtime PV-02 capability."""
    existing = connection.execute(
        """
        SELECT account_ref,self_person_ref,timezone_mode,fixed_zone_id
        FROM dante.account_application_context
        WHERE account_ref=%s
        """,
        (account_ref,),
    ).fetchone()

    if existing is None:
        candidate = expected_self_person_ref or uuid7()
        row = connection.execute(
            """
            SELECT account_ref,self_person_ref,timezone_mode,fixed_zone_id
            FROM dante.ensure_account_application_context(%s,%s)
            """,
            (account_ref, candidate),
        ).fetchone()
    else:
        row = existing

    if row is None:
        raise SeedContextConflictError("PV-02 context capability returned no application context")

    returned_account_ref = UUID(str(row[0]))
    returned_self_person_ref = UUID(str(row[1]))
    if returned_account_ref != account_ref:
        raise SeedContextConflictError("PV-02 context resolved a different Account")
    if (
        expected_self_person_ref is not None
        and returned_self_person_ref != expected_self_person_ref
    ):
        raise SeedContextConflictError(
            "existing PV-02 context uses a different deterministic self Person"
        )

    mode = TimeZoneMode(str(row[2]))
    fixed_zone_id = None if row[3] is None else str(row[3])
    return SeededApplicationContext(
        account_ref=returned_account_ref,
        self_person_ref=returned_self_person_ref,
        timezone_policy=TimeZonePolicy(mode=mode, fixed_zone_id=fixed_zone_id),
    )


def set_seed_timezone_policy(
    connection: Connection[Any],
    *,
    account_ref: UUID,
    desired: TimeZonePolicy,
) -> None:
    """Set deterministic persona policy once; never rewrite an incompatible existing seed policy."""
    with connection.transaction():
        connection.execute(f"SET LOCAL ROLE {_OWNER_ROLE}")
        row = connection.execute(
            """
            SELECT timezone_mode,fixed_zone_id
            FROM dante.account_application_context
            WHERE account_ref=%s
            FOR UPDATE
            """,
            (account_ref,),
        ).fetchone()
        if row is None:
            raise SeedContextConflictError("cannot set timezone policy before PV-02 context exists")

        current = TimeZonePolicy(
            mode=TimeZoneMode(str(row[0])),
            fixed_zone_id=None if row[1] is None else str(row[1]),
        )
        if current == desired:
            return

        # The PV-02 capability establishes new contexts as follow-device. Synthetic personas may
        # specialize that pristine default once; any other mismatch is treated as drift.
        if current != TimeZonePolicy(mode=TimeZoneMode.FOLLOW_DEVICE):
            raise SeedContextConflictError(
                "existing persona context timezone policy differs from deterministic seed intent"
            )

        connection.execute(
            """
            UPDATE dante.account_application_context
            SET timezone_mode=%s,fixed_zone_id=%s
            WHERE account_ref=%s
            """,
            (desired.mode.value, desired.fixed_zone_id, account_ref),
        )


def _read_account_snapshot(
    connection: Connection[Any],
    comparison_key: str,
) -> _AccountSnapshot | None:
    with connection.transaction():
        connection.execute(f"SET LOCAL ROLE {_OWNER_ROLE}")
        row = connection.execute(
            """
            SELECT
                a.account_ref,
                a.status_code,
                e.email_identity_ref,
                e.address,
                e.verified_at,
                p.password_credential_ref,
                p.verifier,
                p.pepper_key_id
            FROM dante.email_identity AS e
            JOIN dante.account AS a ON a.account_ref=e.account_ref
            LEFT JOIN dante.password_credential AS p ON p.account_ref=a.account_ref
            WHERE e.comparison_key=%s
            """,
            (comparison_key,),
        ).fetchone()

    if row is None:
        return None
    return _AccountSnapshot(
        account_ref=UUID(str(row[0])),
        status_code=str(row[1]),
        email_identity_ref=UUID(str(row[2])),
        email_address=str(row[3]),
        verified_at=row[4],
        password_credential_ref=None if row[5] is None else UUID(str(row[5])),
        verifier=None if row[6] is None else str(row[6]),
        pepper_key_id=None if row[7] is None else str(row[7]),
    )


def _verify_existing_account(
    snapshot: _AccountSnapshot,
    *,
    password: str,
    current_pepper_key_id: str,
    pepper_ring: dict[str, bytes],
    expected_account_ref: UUID | None,
) -> None:
    if expected_account_ref is not None and snapshot.account_ref != expected_account_ref:
        raise SeedAccountConflictError(
            "canonical seed email is already bound to a different Account"
        )
    if snapshot.status_code != "active":
        raise SeedAccountConflictError("seed Account exists but is not active")
    if snapshot.verified_at is None:
        raise SeedAccountConflictError("seed Account email exists but is not verified")
    if (
        snapshot.password_credential_ref is None
        or snapshot.verifier is None
        or snapshot.pepper_key_id is None
    ):
        raise SeedAccountConflictError("seed Account exists without a password credential")

    normalized_password = normalize_password_for_authentication(password)
    valid = _verify_password(
        normalized_password=normalized_password,
        verifier=snapshot.verifier,
        pepper_key_id=snapshot.pepper_key_id,
        current_pepper_key_id=current_pepper_key_id,
        pepper_ring=pepper_ring,
    )
    if not valid:
        raise SeedPasswordMismatchError(
            "seed Account exists but the supplied password does not match; credentials were not changed"
        )


def _seeded_account_from_snapshot(
    snapshot: _AccountSnapshot,
    *,
    created: bool,
) -> SeededAccount:
    if snapshot.password_credential_ref is None:
        raise SeedAccountConflictError("seed Account is missing its password credential")
    return SeededAccount(
        account_ref=snapshot.account_ref,
        email_identity_ref=snapshot.email_identity_ref,
        password_credential_ref=snapshot.password_credential_ref,
        email_address=snapshot.email_address,
        created=created,
    )


def _hash_new_password(
    password: str,
    *,
    current_pepper_key_id: str,
    pepper_ring: dict[str, bytes],
) -> tuple[str, str]:
    async def operation() -> tuple[str, str]:
        kdf = _password_kdf(
            current_pepper_key_id=current_pepper_key_id,
            pepper_ring=pepper_ring,
        )
        await kdf.start()
        try:
            return await kdf.hash_new_password(password)
        finally:
            await kdf.aclose()

    return asyncio.run(operation())


def _verify_password(
    *,
    normalized_password: str,
    verifier: str,
    pepper_key_id: str,
    current_pepper_key_id: str,
    pepper_ring: dict[str, bytes],
) -> bool:
    async def operation() -> bool:
        kdf = _password_kdf(
            current_pepper_key_id=current_pepper_key_id,
            pepper_ring=pepper_ring,
        )
        await kdf.start()
        try:
            result = await kdf.verify(
                normalized_password=normalized_password,
                verifier=verifier,
                pepper_key_id=pepper_key_id,
            )
            return result.valid
        finally:
            await kdf.aclose()

    return asyncio.run(operation())


def _password_kdf(
    *,
    current_pepper_key_id: str,
    pepper_ring: dict[str, bytes],
) -> PasswordKdf:
    return PasswordKdf(
        pepper_ring=pepper_ring,
        current_pepper_key_id=current_pepper_key_id,
        max_concurrency=1,
        max_queue_depth=0,
        queue_timeout_seconds=2,
    )


def _required_trimmed(environ: Mapping[str, str], name: str) -> str:
    value = environ.get(name)
    if value is None or not value or value.strip() != value or any(c in value for c in "\r\n"):
        raise SeedConfigurationError(f"{name} must be non-blank, trimmed and single-line")
    return value


def _decode_canonical_secret(value: str, *, name: str) -> bytes:
    try:
        raw_ascii = value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise SeedConfigurationError(f"{name} must use canonical Base64URL ASCII") from exc

    padding = b"=" * (-len(raw_ascii) % 4)
    try:
        decoded = b64decode(raw_ascii + padding, altchars=b"-_", validate=True)
    except (BinasciiError, ValueError) as exc:
        raise SeedConfigurationError(f"{name} must use canonical unpadded Base64URL") from exc

    canonical = urlsafe_b64encode(decoded).rstrip(b"=").decode("ascii")
    if len(decoded) != _SECRET_BYTES or canonical != value:
        raise SeedConfigurationError(
            f"{name} must be canonical unpadded Base64URL encoding exactly {_SECRET_BYTES} bytes"
        )
    return decoded
