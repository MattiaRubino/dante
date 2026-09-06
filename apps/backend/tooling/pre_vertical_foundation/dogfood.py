"""Bootstrap one persistent LOCAL/DEV dogfood Account and DANTE application context."""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

from tooling.pre_vertical_foundation.account_seed import (
    connect_migrator,
    connect_runtime,
    database_target_from_environment,
    ensure_account_application_context,
    password_pepper_configuration_from_environment,
    read_local_secret,
    seed_password_account,
)

_LOGGER = logging.getLogger("dante.pre_vertical.dogfood")
_DEFAULT_EMAIL = "dante.dogfood@example.com"


@dataclass(frozen=True, slots=True)
class _Arguments:
    email: str
    password_file: Path
    migrator_password_file: Path


def _parse_args() -> _Arguments:
    parser = argparse.ArgumentParser(
        description="Create or verify the persistent DANTE LOCAL/DEV dogfood account.",
    )
    parser.add_argument(
        "--email",
        default=_DEFAULT_EMAIL,
        help=f"Canonical dogfood login email (default: {_DEFAULT_EMAIL}).",
    )
    parser.add_argument(
        "--password-file",
        type=Path,
        required=True,
        help="Ignored *.local file containing the dogfood account password.",
    )
    parser.add_argument(
        "--migrator-password-file",
        type=Path,
        required=True,
        help="Ignored *.local file containing the dante_migrator database password.",
    )
    namespace = parser.parse_args()
    return _Arguments(
        email=str(namespace.email),
        password_file=Path(namespace.password_file),
        migrator_password_file=Path(namespace.migrator_password_file),
    )


def main() -> None:
    """Seed or verify dogfood identity, then resolve its stable self Person context."""
    arguments = _parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    target = database_target_from_environment()
    current_pepper_key_id, pepper_ring = password_pepper_configuration_from_environment()
    account_password = read_local_secret(arguments.password_file)
    migrator_password = read_local_secret(arguments.migrator_password_file)

    with (
        connect_migrator(target, password=migrator_password) as migrator,
        connect_runtime(target) as runtime,
    ):
        account = seed_password_account(
            migrator,
            email=arguments.email,
            password=account_password,
            current_pepper_key_id=current_pepper_key_id,
            pepper_ring=pepper_ring,
        )
        context = ensure_account_application_context(
            runtime,
            account_ref=account.account_ref,
        )

    _LOGGER.info("DANTE persistent dogfood account ready")
    _LOGGER.info("  email          : %s", account.email_address)
    _LOGGER.info("  account_ref    : %s", account.account_ref)
    _LOGGER.info("  self_person_ref: %s", context.self_person_ref)
    _LOGGER.info("  account action : %s", "created" if account.created else "verified existing")
    _LOGGER.info("  timezone mode  : %s", context.timezone_policy.mode.value)


if __name__ == "__main__":
    main()
