"""Real PostgreSQL proof for persistent LOCAL/DEV dogfood/persona seed semantics."""

from typing import Any

import psycopg
import pytest

from tooling.pre_vertical_foundation.account_seed import (
    SeedPasswordMismatchError,
    ensure_account_application_context,
    seed_password_account,
    set_seed_timezone_policy,
)
from tooling.pre_vertical_foundation.personas import TEMPORAL_EDGE

pytestmark = pytest.mark.postgres

_PEPPER_KEY_ID = "test-password-v1"
_PEPPER_RING = {_PEPPER_KEY_ID: b"p" * 32}
_PASSWORD = "correct horse battery staple"


def test_persona_seed_is_idempotent_and_preserves_account_and_self_person(
    migrated_database: Any,
) -> None:
    migrator_kwargs = migrated_database.connection_kwargs(
        "dante_migrator",
        migrated_database.cluster.migrator_password,
    )
    runtime_kwargs = migrated_database.connection_kwargs(
        "dante_runtime",
        migrated_database.cluster.runtime_password,
    )

    with (
        psycopg.connect(**migrator_kwargs, autocommit=True) as migrator,
        psycopg.connect(**runtime_kwargs, autocommit=True) as runtime,
    ):
        first_account = seed_password_account(
            migrator,
            email=TEMPORAL_EDGE.email,
            password=_PASSWORD,
            current_pepper_key_id=_PEPPER_KEY_ID,
            pepper_ring=_PEPPER_RING,
            expected_account_ref=TEMPORAL_EDGE.account_ref,
        )
        first_context = ensure_account_application_context(
            runtime,
            account_ref=TEMPORAL_EDGE.account_ref,
            expected_self_person_ref=TEMPORAL_EDGE.self_person_ref,
        )
        set_seed_timezone_policy(
            migrator,
            account_ref=TEMPORAL_EDGE.account_ref,
            desired=TEMPORAL_EDGE.timezone_policy,
        )
        fixed_context = ensure_account_application_context(
            runtime,
            account_ref=TEMPORAL_EDGE.account_ref,
            expected_self_person_ref=TEMPORAL_EDGE.self_person_ref,
        )

        second_account = seed_password_account(
            migrator,
            email=TEMPORAL_EDGE.email,
            password=_PASSWORD,
            current_pepper_key_id=_PEPPER_KEY_ID,
            pepper_ring=_PEPPER_RING,
            expected_account_ref=TEMPORAL_EDGE.account_ref,
        )
        second_context = ensure_account_application_context(
            runtime,
            account_ref=TEMPORAL_EDGE.account_ref,
            expected_self_person_ref=TEMPORAL_EDGE.self_person_ref,
        )

        assert first_account.created is True
        assert second_account.created is False
        assert first_account.account_ref == second_account.account_ref == TEMPORAL_EDGE.account_ref
        assert first_context.self_person_ref == TEMPORAL_EDGE.self_person_ref
        assert second_context.self_person_ref == TEMPORAL_EDGE.self_person_ref
        assert fixed_context.timezone_policy == TEMPORAL_EDGE.timezone_policy
        assert second_context.timezone_policy == TEMPORAL_EDGE.timezone_policy

        with migrator.transaction():
            migrator.execute("SET LOCAL ROLE dante_owner")
            shape = migrator.execute(
                """
                SELECT
                  (SELECT count(*) FROM dante.account WHERE account_ref=%s),
                  (SELECT count(*) FROM dante.email_identity WHERE account_ref=%s),
                  (SELECT count(*) FROM dante.password_credential WHERE account_ref=%s),
                  (SELECT count(*) FROM dante.person WHERE person_ref=%s),
                  (SELECT count(*) FROM dante.native_address
                     WHERE native_ref=%s AND owner_family='person'),
                  (SELECT count(*) FROM dante.account_application_context WHERE account_ref=%s)
                """,
                (
                    TEMPORAL_EDGE.account_ref,
                    TEMPORAL_EDGE.account_ref,
                    TEMPORAL_EDGE.account_ref,
                    TEMPORAL_EDGE.self_person_ref,
                    TEMPORAL_EDGE.self_person_ref,
                    TEMPORAL_EDGE.account_ref,
                ),
            ).fetchone()
        assert shape == (1, 1, 1, 1, 1, 1)


def test_existing_seed_password_mismatch_is_fail_closed_without_credential_rewrite(
    migrated_database: Any,
) -> None:
    migrator_kwargs = migrated_database.connection_kwargs(
        "dante_migrator",
        migrated_database.cluster.migrator_password,
    )

    with psycopg.connect(**migrator_kwargs, autocommit=True) as migrator:
        seeded = seed_password_account(
            migrator,
            email=TEMPORAL_EDGE.email,
            password=_PASSWORD,
            current_pepper_key_id=_PEPPER_KEY_ID,
            pepper_ring=_PEPPER_RING,
            expected_account_ref=TEMPORAL_EDGE.account_ref,
        )

        with migrator.transaction():
            migrator.execute("SET LOCAL ROLE dante_owner")
            before = migrator.execute(
                """
                SELECT verifier,pepper_key_id,updated_at
                FROM dante.password_credential
                WHERE account_ref=%s
                """,
                (seeded.account_ref,),
            ).fetchone()
        assert before is not None

        with pytest.raises(SeedPasswordMismatchError):
            seed_password_account(
                migrator,
                email=TEMPORAL_EDGE.email,
                password="different password that must not reset",
                current_pepper_key_id=_PEPPER_KEY_ID,
                pepper_ring=_PEPPER_RING,
                expected_account_ref=TEMPORAL_EDGE.account_ref,
            )

        with migrator.transaction():
            migrator.execute("SET LOCAL ROLE dante_owner")
            after = migrator.execute(
                """
                SELECT verifier,pepper_key_id,updated_at
                FROM dante.password_credential
                WHERE account_ref=%s
                """,
                (seeded.account_ref,),
            ).fetchone()
        assert after == before
