"""Materialize deterministic pre-vertical personas into a persistent LOCAL/DEV database."""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

from tooling.pre_vertical_foundation.account_seed import (
    SeedContextConflictError,
    connect_migrator,
    connect_runtime,
    database_target_from_environment,
    ensure_account_application_context,
    password_pepper_configuration_from_environment,
    read_local_secret,
    seed_password_account,
    set_seed_timezone_policy,
)
from tooling.pre_vertical_foundation.personas import PERSONAS, PERSONAS_BY_SLUG, PersonaSpec

_LOGGER = logging.getLogger("dante.pre_vertical.personas")


@dataclass(frozen=True, slots=True)
class _Arguments:
    password_file: Path
    migrator_password_file: Path
    persona_slugs: tuple[str, ...]


def _parse_args() -> _Arguments:
    parser = argparse.ArgumentParser(
        description="Materialize deterministic DANTE pre-vertical personas in LOCAL/DEV.",
    )
    parser.add_argument(
        "--password-file",
        type=Path,
        required=True,
        help="Ignored *.local file containing the shared synthetic persona password.",
    )
    parser.add_argument(
        "--migrator-password-file",
        type=Path,
        required=True,
        help="Ignored *.local file containing the dante_migrator database password.",
    )
    parser.add_argument(
        "--persona",
        action="append",
        choices=tuple(PERSONAS_BY_SLUG),
        dest="personas",
        help="Materialize only the named persona; repeat to select several. Default: all.",
    )
    namespace = parser.parse_args()
    selected = tuple(namespace.personas) if namespace.personas else tuple(p.slug for p in PERSONAS)
    return _Arguments(
        password_file=Path(namespace.password_file),
        migrator_password_file=Path(namespace.migrator_password_file),
        persona_slugs=selected,
    )


def _materialize_persona(
    persona: PersonaSpec,
    *,
    password: str,
    migrator: object,
    runtime: object,
    current_pepper_key_id: str,
    pepper_ring: dict[str, bytes],
) -> tuple[bool, str]:
    # Runtime typing is narrowed at call sites by the concrete psycopg connection factories.
    account = seed_password_account(  # type: ignore[arg-type]
        migrator,
        email=persona.email,
        password=password,
        current_pepper_key_id=current_pepper_key_id,
        pepper_ring=pepper_ring,
        expected_account_ref=persona.account_ref,
    )
    ensure_account_application_context(  # type: ignore[arg-type]
        runtime,
        account_ref=persona.account_ref,
        expected_self_person_ref=persona.self_person_ref,
    )
    set_seed_timezone_policy(  # type: ignore[arg-type]
        migrator,
        account_ref=persona.account_ref,
        desired=persona.timezone_policy,
    )
    confirmed = ensure_account_application_context(  # type: ignore[arg-type]
        runtime,
        account_ref=persona.account_ref,
        expected_self_person_ref=persona.self_person_ref,
    )
    if confirmed.timezone_policy != persona.timezone_policy:
        raise SeedContextConflictError(
            f"persona {persona.slug} persisted timezone policy differs from its deterministic spec"
        )
    return account.created, confirmed.timezone_policy.mode.value


def main() -> None:
    """Materialize selected deterministic personas without printing any secret material."""
    arguments = _parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    target = database_target_from_environment()
    current_pepper_key_id, pepper_ring = password_pepper_configuration_from_environment()
    persona_password = read_local_secret(arguments.password_file)
    migrator_password = read_local_secret(arguments.migrator_password_file)

    with (
        connect_migrator(target, password=migrator_password) as migrator,
        connect_runtime(target) as runtime,
    ):
        for slug in arguments.persona_slugs:
            persona = PERSONAS_BY_SLUG[slug]
            created, timezone_mode = _materialize_persona(
                persona,
                password=persona_password,
                migrator=migrator,
                runtime=runtime,
                current_pepper_key_id=current_pepper_key_id,
                pepper_ring=pepper_ring,
            )
            _LOGGER.info(
                "persona=%s account_ref=%s self_person_ref=%s account=%s timezone=%s",
                persona.slug,
                persona.account_ref,
                persona.self_person_ref,
                "created" if created else "verified",
                timezone_mode,
            )


if __name__ == "__main__":
    main()
