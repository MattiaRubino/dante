from __future__ import annotations

import importlib.util
import os
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from uuid import uuid7

import psycopg
from dante.auth.email import normalize_email
from psycopg import sql

_CORE_PATH = Path(__file__).with_name("serve-access-auth-stack.py")
_REQUIRED_EXTENSIONS: tuple[tuple[str, str | None], ...] = (
    ("postgis", "3.6.4"),
    ("vector", "0.8.6"),
    ("pg_trgm", None),
    ("unaccent", None),
    ("pg_stat_statements", None),
)
_E2E_RATE_CAPACITY_ENV = "DANTE_E2E_SIGNIN_RATE_CAPACITY"
_E2E_CONTROL_ID_ENV = "DANTE_E2E_CONTROL_ID"
_E2E_CONTROL_LABEL = "dante.e2e.control_id"
_E2E_ACCOUNT_COUNT = 64


def _load_core() -> ModuleType:
    spec = importlib.util.spec_from_file_location("dante_access_auth_stack_core", _CORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the Access/Auth full-stack harness core.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _control_id() -> str:
    value = os.environ.get(_E2E_CONTROL_ID_ENV)
    if value is None or not value or value.strip() != value:
        raise RuntimeError(f"{_E2E_CONTROL_ID_ENV} must be a non-blank trimmed value.")
    return value


def _docker_with_control_label(
    original: Callable[..., object], control_id: str
) -> Callable[..., object]:
    def run(*args: str, **kwargs: object) -> object:
        if args and args[0] == "run":
            return original(
                "run",
                "--label",
                f"{_E2E_CONTROL_LABEL}={control_id}",
                *args[1:],
                **kwargs,
            )
        return original(*args, **kwargs)

    return run


def _extension_guard(database_name: str) -> Callable[..., None]:
    def ensure_extensions(*, port: int, password: str) -> None:
        with psycopg.connect(
            host="127.0.0.1",
            port=port,
            dbname=database_name,
            user="postgres",
            password=password,
            autocommit=True,
        ) as connection:
            for extension_name, expected_version in _REQUIRED_EXTENSIONS:
                statement = sql.SQL("CREATE EXTENSION IF NOT EXISTS {}").format(
                    sql.Identifier(extension_name)
                )
                if expected_version is not None:
                    statement += sql.SQL(" VERSION {}").format(sql.Literal(expected_version))
                connection.execute(statement)

                row = connection.execute(
                    "SELECT extversion FROM pg_extension WHERE extname = %s",
                    (extension_name,),
                ).fetchone()
                if row is None:
                    raise RuntimeError(
                        f"Required PostgreSQL extension is unavailable: {extension_name}"
                    )
                if expected_version is not None and row[0] != expected_version:
                    raise RuntimeError(
                        "PostgreSQL extension version mismatch: "
                        f"{extension_name} expected {expected_version}, got {row[0]}"
                    )

    return ensure_extensions


def _auth_settings_override(
    original: Callable[[str, int], object],
) -> Callable[[str, int], object]:
    def build(hibp_base_url: str, smtp_port: int) -> object:
        settings = original(hibp_base_url, smtp_port)
        raw_capacity = os.environ.get(_E2E_RATE_CAPACITY_ENV)
        if raw_capacity is None:
            return settings

        try:
            capacity = int(raw_capacity)
        except ValueError as exc:
            raise RuntimeError(f"{_E2E_RATE_CAPACITY_ENV} must be a positive integer.") from exc
        if capacity < 1:
            raise RuntimeError(f"{_E2E_RATE_CAPACITY_ENV} must be at least 1.")

        model_copy = getattr(settings, "model_copy", None)
        if not callable(model_copy):
            raise TypeError("Auth settings do not support bounded E2E overrides.")
        return model_copy(update={"signin_rate_capacity": capacity})

    return build


def _seed_account_with_e2e_accounts(
    original: Callable[..., None],
    *,
    database_name: str,
    primary_email: str,
) -> Callable[..., None]:
    def seed(
        *,
        port: int,
        migrator_password: str,
        auth_settings: object,
    ) -> None:
        original(
            port=port,
            migrator_password=migrator_password,
            auth_settings=auth_settings,
        )
        if os.environ.get(_E2E_RATE_CAPACITY_ENV) is None:
            return

        primary_comparison_key = normalize_email(primary_email).comparison_key
        now = datetime.now(UTC)
        with psycopg.connect(
            host="127.0.0.1",
            port=port,
            dbname=database_name,
            user="dante_migrator",
            password=migrator_password,
            connect_timeout=2,
        ) as connection:
            connection.execute("SET ROLE dante_owner")
            connection.execute("SET search_path TO pg_catalog,dante,pg_temp")
            credential = connection.execute(
                """
                SELECT credential.verifier, credential.pepper_key_id
                FROM dante.email_identity AS identity
                JOIN dante.password_credential AS credential
                  ON credential.account_ref = identity.account_ref
                WHERE identity.comparison_key = %s
                """,
                (primary_comparison_key,),
            ).fetchone()
            if credential is None:
                raise RuntimeError("Synthetic Access/Auth E2E credential was not seeded.")
            verifier, pepper_key_id = credential

            for index in range(1, _E2E_ACCOUNT_COUNT + 1):
                normalized = normalize_email(f"synthetic.user+e2e-{index:02d}@example.com")
                account_ref = uuid7()
                connection.execute(
                    """
                    INSERT INTO dante.account(
                        account_ref, status_code, created_at, disabled_at
                    )
                    VALUES (%s, 'active', %s, NULL)
                    """,
                    (account_ref, now),
                )
                connection.execute(
                    """
                    INSERT INTO dante.email_identity(
                        email_identity_ref,
                        account_ref,
                        address,
                        comparison_key,
                        created_at,
                        verified_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        uuid7(),
                        account_ref,
                        normalized.address,
                        normalized.comparison_key,
                        now,
                        now,
                    ),
                )
                connection.execute(
                    """
                    INSERT INTO dante.password_credential(
                        password_credential_ref,
                        account_ref,
                        verifier,
                        pepper_key_id,
                        created_at,
                        updated_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        uuid7(),
                        account_ref,
                        verifier,
                        pepper_key_id,
                        now,
                        now,
                    ),
                )
            connection.commit()

    return seed


def main() -> None:
    core = _load_core()
    database_name = getattr(core, "_DATABASE_NAME", None)
    primary_email = getattr(core, "_EMAIL", None)
    if not isinstance(database_name, str) or not database_name:
        raise RuntimeError("Access/Auth harness core does not expose its database name.")
    if not isinstance(primary_email, str) or not primary_email:
        raise RuntimeError("Access/Auth harness core does not expose its synthetic email.")

    os.environ["VITE_DANTE_APPLE_ENABLED"] = "true"
    os.environ["VITE_DANTE_PASSKEY_ENABLED"] = "true"

    control_id = _control_id()
    core._docker = _docker_with_control_label(core._docker, control_id)
    core._create_extensions = _extension_guard(database_name)
    core._auth_settings = _auth_settings_override(core._auth_settings)
    core._seed_account = _seed_account_with_e2e_accounts(
        core._seed_account,
        database_name=database_name,
        primary_email=primary_email,
    )
    core.main()


if __name__ == "__main__":
    main()
