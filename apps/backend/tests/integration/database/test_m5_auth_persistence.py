"""Real PostgreSQL persistence acceptance for the M5 multi-authenticator spine."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid7

import psycopg
import pytest

pytestmark = pytest.mark.postgres

_M5_TABLES = {
    "account_profile_bootstrap",
    "apple_auth_grant",
    "external_auth_transaction",
    "external_identity",
    "external_link_challenge",
    "external_signup_challenge",
    "passkey_credential",
    "webauthn_account",
    "webauthn_challenge",
}


def _admin(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        host=database.cluster.host,
        port=database.cluster.port,
        dbname=database.name,
        user=database.cluster.admin_user,
        password=database.cluster.admin_password,
        autocommit=True,
    )


def _runtime(database: Any) -> psycopg.Connection[Any]:
    return psycopg.connect(
        **database.connection_kwargs(
            "dante_runtime",
            database.cluster.runtime_password,
        ),
        autocommit=True,
    )


def _create_account(connection: psycopg.Connection[Any], account_ref: UUID, now: datetime) -> None:
    connection.execute(
        "INSERT INTO dante.account(account_ref,status_code,created_at,disabled_at) "
        "VALUES (%s,'active',%s,NULL)",
        (account_ref, now),
    )


def _create_session(
    connection: psycopg.Connection[Any],
    account_ref: UUID,
    session_ref: UUID,
    verifier: bytes,
    now: datetime,
) -> None:
    connection.execute(
        "INSERT INTO dante.auth_session("
        "auth_session_ref,account_ref,secret_verifier,created_at,authenticated_at,"
        "recent_auth_at,last_user_activity_at,expires_at,revoked_at,"
        "revocation_reason_code) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NULL,NULL)",
        (
            session_ref,
            account_ref,
            verifier,
            now,
            now,
            now,
            now,
            now + timedelta(hours=1),
        ),
    )


def _create_apple_identity(
    connection: psycopg.Connection[Any],
    account_ref: UUID,
    external_ref: UUID,
    subject: str,
    now: datetime,
) -> None:
    connection.execute(
        "INSERT INTO dante.external_identity("
        "external_identity_ref,account_ref,email_identity_ref,provider_code,issuer,subject,"
        "provider_email_address,provider_email_private,status_code,created_at,"
        "status_changed_at,last_authenticated_at,revoked_at,revocation_reason_code) "
        "VALUES (%s,%s,NULL,'apple','https://appleid.apple.com',%s,NULL,NULL,"
        "'active',%s,%s,%s,NULL,NULL)",
        (external_ref, account_ref, subject, now, now, now),
    )


def _create_active_apple_grant(
    connection: psycopg.Connection[Any],
    grant_ref: UUID,
    external_ref: UUID,
    subject: str,
    now: datetime,
) -> None:
    connection.execute(
        "INSERT INTO dante.apple_auth_grant("
        "apple_auth_grant_ref,external_identity_ref,issuer,subject,client_id,"
        "refresh_token_ciphertext,refresh_token_nonce,encryption_key_id,status_code,"
        "created_at,updated_at,status_changed_at,pending_expires_at,"
        "revocation_requested_at,revoked_at) "
        "VALUES (%s,%s,'https://appleid.apple.com',%s,'client',%s,%s,'k1','active',"
        "%s,%s,%s,NULL,NULL,NULL)",
        (
            grant_ref,
            external_ref,
            subject,
            b"ciphertext-with-auth-tag",
            b"n" * 12,
            now,
            now,
            now,
        ),
    )


def test_m5_tables_email_delta_and_runtime_acl_are_exact(migrated_database: Any) -> None:
    with _admin(migrated_database) as connection:
        tables = {
            str(row[0])
            for row in connection.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname='dante' AND tablename = ANY(%s)",
                (sorted(_M5_TABLES),),
            )
        }
        email_columns = {
            str(row[0])
            for row in connection.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema='dante' AND table_name='email_identity' "
                "AND column_name IN "
                "('recovery_restriction_code','recovery_restriction_observed_at')"
            )
        }
        table_grants = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT table_name, privilege_type "
                "FROM information_schema.table_privileges "
                "WHERE grantee='dante_runtime' AND table_schema='dante' "
                "AND table_name = ANY(%s)",
                (sorted(_M5_TABLES),),
            )
        }
        update_columns = {
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT table_name, column_name "
                "FROM information_schema.column_privileges "
                "WHERE grantee='dante_runtime' AND table_schema='dante' "
                "AND privilege_type='UPDATE' "
                "AND (table_name = ANY(%s) OR table_name='email_identity')",
                (sorted(_M5_TABLES),),
            )
        }

    assert tables == _M5_TABLES
    assert email_columns == {
        "recovery_restriction_code",
        "recovery_restriction_observed_at",
    }
    assert table_grants == {
        ("external_identity", "SELECT"),
        ("external_auth_transaction", "SELECT"),
        ("external_auth_transaction", "INSERT"),
        ("external_auth_transaction", "DELETE"),
        ("apple_auth_grant", "SELECT"),
        ("apple_auth_grant", "INSERT"),
        ("external_link_challenge", "SELECT"),
        ("external_link_challenge", "INSERT"),
        ("external_link_challenge", "DELETE"),
        ("external_signup_challenge", "SELECT"),
        ("external_signup_challenge", "INSERT"),
        ("external_signup_challenge", "DELETE"),
        ("account_profile_bootstrap", "SELECT"),
        ("account_profile_bootstrap", "INSERT"),
        ("account_profile_bootstrap", "DELETE"),
        ("webauthn_account", "SELECT"),
        ("webauthn_account", "INSERT"),
        ("passkey_credential", "SELECT"),
        ("passkey_credential", "INSERT"),
        ("webauthn_challenge", "SELECT"),
        ("webauthn_challenge", "INSERT"),
        ("webauthn_challenge", "DELETE"),
    }
    assert update_columns == {
        ("email_identity", "recovery_restriction_code"),
        ("email_identity", "recovery_restriction_observed_at"),
        ("external_identity", "provider_email_address"),
        ("external_identity", "provider_email_private"),
        ("external_identity", "status_code"),
        ("external_identity", "status_changed_at"),
        ("external_identity", "last_authenticated_at"),
        ("external_identity", "revoked_at"),
        ("external_identity", "revocation_reason_code"),
        ("external_auth_transaction", "claimed_at"),
        ("apple_auth_grant", "external_identity_ref"),
        ("apple_auth_grant", "refresh_token_ciphertext"),
        ("apple_auth_grant", "refresh_token_nonce"),
        ("apple_auth_grant", "encryption_key_id"),
        ("apple_auth_grant", "status_code"),
        ("apple_auth_grant", "updated_at"),
        ("apple_auth_grant", "status_changed_at"),
        ("apple_auth_grant", "pending_expires_at"),
        ("apple_auth_grant", "revocation_requested_at"),
        ("apple_auth_grant", "revoked_at"),
        ("external_signup_challenge", "email_address"),
        ("external_signup_challenge", "email_comparison_key"),
        ("external_signup_challenge", "otp_verifier"),
        ("external_signup_challenge", "otp_key_id"),
        ("external_signup_challenge", "verification_issued_at"),
        ("external_signup_challenge", "verification_expires_at"),
        ("external_signup_challenge", "failed_verification_attempts"),
        ("external_signup_challenge", "updated_at"),
        ("passkey_credential", "sign_count"),
        ("passkey_credential", "backup_state"),
        ("passkey_credential", "label"),
        ("passkey_credential", "status_code"),
        ("passkey_credential", "updated_at"),
        ("passkey_credential", "last_used_at"),
        ("passkey_credential", "revoked_at"),
        ("passkey_credential", "revocation_reason_code"),
        ("webauthn_challenge", "claimed_at"),
    }


def test_provider_identity_and_passkey_uniqueness_are_database_arbiters(
    migrated_database: Any,
) -> None:
    now = datetime.now(UTC)
    account_a = uuid7()
    account_b = uuid7()
    with _admin(migrated_database) as connection:
        _create_account(connection, account_a, now)
        _create_account(connection, account_b, now)
        connection.execute(
            "INSERT INTO dante.external_identity("
            "external_identity_ref,account_ref,email_identity_ref,provider_code,issuer,subject,"
            "provider_email_address,provider_email_private,status_code,created_at,"
            "status_changed_at,last_authenticated_at,revoked_at,revocation_reason_code) "
            "VALUES (%s,%s,NULL,'google','https://accounts.google.com','stable-sub',"
            "NULL,NULL,'active',%s,%s,%s,NULL,NULL)",
            (uuid7(), account_a, now, now, now),
        )
        with pytest.raises(psycopg.errors.UniqueViolation):
            connection.execute(
                "INSERT INTO dante.external_identity("
                "external_identity_ref,account_ref,email_identity_ref,provider_code,issuer,subject,"
                "provider_email_address,provider_email_private,status_code,created_at,"
                "status_changed_at,last_authenticated_at,revoked_at,revocation_reason_code) "
                "VALUES (%s,%s,NULL,'google','https://accounts.google.com','stable-sub',"
                "NULL,NULL,'active',%s,%s,%s,NULL,NULL)",
                (uuid7(), account_b, now, now, now),
            )
        connection.execute(
            "INSERT INTO dante.webauthn_account(account_ref,user_handle,created_at) "
            "VALUES (%s,%s,%s)",
            (account_a, b"u" * 32, now),
        )
        connection.execute(
            "INSERT INTO dante.webauthn_account(account_ref,user_handle,created_at) "
            "VALUES (%s,%s,%s)",
            (account_b, b"v" * 32, now),
        )
        connection.execute(
            "INSERT INTO dante.passkey_credential("
            "passkey_credential_ref,account_ref,credential_id,credential_public_key,"
            "cose_algorithm,sign_count,backup_eligible,backup_state,transports,label,"
            "status_code,created_at,updated_at,last_used_at,revoked_at,"
            "revocation_reason_code) "
            "VALUES (%s,%s,%s,%s,-7,0,TRUE,TRUE,%s,'Primary passkey','active',"
            "%s,%s,NULL,NULL,NULL)",
            (uuid7(), account_a, b"credential-id", b"public-key", ["internal"], now, now),
        )
        with pytest.raises(psycopg.errors.UniqueViolation):
            connection.execute(
                "INSERT INTO dante.passkey_credential("
                "passkey_credential_ref,account_ref,credential_id,credential_public_key,"
                "cose_algorithm,sign_count,backup_eligible,backup_state,transports,label,"
                "status_code,created_at,updated_at,last_used_at,revoked_at,"
                "revocation_reason_code) "
                "VALUES (%s,%s,%s,%s,-7,0,FALSE,FALSE,%s,'Duplicate','active',"
                "%s,%s,NULL,NULL,NULL)",
                (uuid7(), account_b, b"credential-id", b"other-key", ["hybrid"], now, now),
            )


def test_protocol_state_constraints_reject_invalid_combinations(
    migrated_database: Any,
) -> None:
    now = datetime.now(UTC)
    account_ref = uuid7()
    session_ref = uuid7()
    with _admin(migrated_database) as connection:
        _create_account(connection, account_ref, now)
        _create_session(connection, account_ref, session_ref, b"s" * 32, now)
        with pytest.raises(psycopg.errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.external_auth_transaction("
                "external_auth_transaction_ref,provider_code,expected_issuer,purpose_code,"
                "state_verifier,nonce_verifier,auth_session_ref,auth_session_secret_verifier,"
                "return_target_code,created_at,expires_at,claimed_at) "
                "VALUES (%s,'google','https://accounts.google.com','sign_in',%s,%s,%s,%s,"
                "'access',%s,%s,NULL)",
                (
                    uuid7(),
                    b"a" * 32,
                    b"b" * 32,
                    session_ref,
                    b"s" * 32,
                    now,
                    now + timedelta(minutes=5),
                ),
            )
        with pytest.raises(psycopg.errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.apple_auth_grant("
                "apple_auth_grant_ref,external_identity_ref,issuer,subject,client_id,"
                "refresh_token_ciphertext,refresh_token_nonce,encryption_key_id,status_code,"
                "created_at,updated_at,status_changed_at,pending_expires_at,"
                "revocation_requested_at,revoked_at) "
                "VALUES (%s,NULL,'https://appleid.apple.com','apple-sub','client',%s,%s,'k1',"
                "'revoked',%s,%s,%s,NULL,NULL,%s)",
                (
                    uuid7(),
                    b"ciphertext-that-must-not-remain",
                    b"n" * 12,
                    now,
                    now,
                    now,
                    now,
                ),
            )


def test_apple_grant_and_link_state_are_subject_bound(migrated_database: Any) -> None:
    now = datetime.now(UTC)
    account_ref = uuid7()
    external_ref = uuid7()
    with _admin(migrated_database) as connection:
        _create_account(connection, account_ref, now)
        _create_apple_identity(connection, account_ref, external_ref, "subject-a", now)
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            _create_active_apple_grant(
                connection,
                uuid7(),
                external_ref,
                "subject-b",
                now,
            )

        grant_ref = uuid7()
        _create_active_apple_grant(
            connection,
            grant_ref,
            external_ref,
            "subject-a",
            now,
        )
        email_ref = uuid7()
        connection.execute(
            "INSERT INTO dante.email_identity("
            "email_identity_ref,account_ref,address,comparison_key,created_at,verified_at,"
            "recovery_restriction_code,recovery_restriction_observed_at) "
            "VALUES (%s,%s,'a@example.com','a@example.com',%s,%s,NULL,NULL)",
            (email_ref, account_ref, now, now),
        )
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.external_link_challenge("
                "external_link_challenge_ref,target_account_ref,target_email_identity_ref,"
                "provider_code,issuer,subject,provider_email_address,provider_email_private,"
                "apple_auth_grant_ref,continuation_verifier,created_at,expires_at) "
                "VALUES (%s,%s,%s,'apple','https://appleid.apple.com','subject-b',NULL,NULL,"
                "%s,%s,%s,%s)",
                (
                    uuid7(),
                    account_ref,
                    email_ref,
                    grant_ref,
                    b"c" * 32,
                    now,
                    now + timedelta(minutes=10),
                ),
            )
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.external_signup_challenge("
                "external_signup_ref,provider_code,issuer,subject,provider_email_address,"
                "provider_email_private,apple_auth_grant_ref,continuation_verifier,"
                "email_address,email_comparison_key,otp_verifier,otp_key_id,"
                "verification_issued_at,verification_expires_at,failed_verification_attempts,"
                "bootstrap_display_name,bootstrap_given_name,bootstrap_family_name,"
                "bootstrap_picture_url,bootstrap_locale,created_at,updated_at,expires_at) "
                "VALUES (%s,'apple','https://appleid.apple.com','subject-b',NULL,NULL,%s,%s,"
                "NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,%s,%s,%s)",
                (
                    uuid7(),
                    grant_ref,
                    b"d" * 32,
                    now,
                    now,
                    now + timedelta(minutes=20),
                ),
            )


def test_webauthn_account_session_and_user_handle_binding_is_exact(
    migrated_database: Any,
) -> None:
    now = datetime.now(UTC)
    account_a = uuid7()
    account_b = uuid7()
    session_a = uuid7()
    handle_a = b"a" * 32
    handle_b = b"b" * 32
    with _admin(migrated_database) as connection:
        _create_account(connection, account_a, now)
        _create_account(connection, account_b, now)
        _create_session(connection, account_a, session_a, b"s" * 32, now)
        connection.execute(
            "INSERT INTO dante.webauthn_account(account_ref,user_handle,created_at) "
            "VALUES (%s,%s,%s),(%s,%s,%s)",
            (account_a, handle_a, now, account_b, handle_b, now),
        )
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.webauthn_challenge("
                "webauthn_challenge_ref,ceremony_code,challenge_verifier,account_ref,"
                "auth_session_ref,auth_session_secret_verifier,user_handle,rp_id,"
                "expected_origin,created_at,expires_at,claimed_at) "
                "VALUES (%s,'registration',%s,%s,%s,%s,%s,'localhost',"
                "'https://localhost:4173',%s,%s,NULL)",
                (
                    uuid7(),
                    b"x" * 32,
                    account_b,
                    session_a,
                    b"s" * 32,
                    handle_b,
                    now,
                    now + timedelta(minutes=2),
                ),
            )
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.webauthn_challenge("
                "webauthn_challenge_ref,ceremony_code,challenge_verifier,account_ref,"
                "auth_session_ref,auth_session_secret_verifier,user_handle,rp_id,"
                "expected_origin,created_at,expires_at,claimed_at) "
                "VALUES (%s,'registration',%s,%s,%s,%s,%s,'localhost',"
                "'https://localhost:4173',%s,%s,NULL)",
                (
                    uuid7(),
                    b"y" * 32,
                    account_a,
                    session_a,
                    b"s" * 32,
                    handle_b,
                    now,
                    now + timedelta(minutes=2),
                ),
            )


def test_passkey_requires_webauthn_owner_and_valid_backup_state(
    migrated_database: Any,
) -> None:
    now = datetime.now(UTC)
    account_ref = uuid7()
    with _admin(migrated_database) as connection:
        _create_account(connection, account_ref, now)
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            connection.execute(
                "INSERT INTO dante.passkey_credential("
                "passkey_credential_ref,account_ref,credential_id,credential_public_key,"
                "cose_algorithm,sign_count,backup_eligible,backup_state,transports,label,"
                "status_code,created_at,updated_at,last_used_at,revoked_at,"
                "revocation_reason_code) "
                "VALUES (%s,%s,%s,%s,-7,0,FALSE,FALSE,%s,'Orphan','active',"
                "%s,%s,NULL,NULL,NULL)",
                (uuid7(), account_ref, b"orphan", b"key", [], now, now),
            )
        connection.execute(
            "INSERT INTO dante.webauthn_account(account_ref,user_handle,created_at) "
            "VALUES (%s,%s,%s)",
            (account_ref, b"h" * 32, now),
        )
        with pytest.raises(psycopg.errors.CheckViolation):
            connection.execute(
                "INSERT INTO dante.passkey_credential("
                "passkey_credential_ref,account_ref,credential_id,credential_public_key,"
                "cose_algorithm,sign_count,backup_eligible,backup_state,transports,label,"
                "status_code,created_at,updated_at,last_used_at,revoked_at,"
                "revocation_reason_code) "
                "VALUES (%s,%s,%s,%s,-7,0,FALSE,TRUE,%s,'Impossible','active',"
                "%s,%s,NULL,NULL,NULL)",
                (uuid7(), account_ref, b"backup", b"key", [], now, now),
            )


def test_durable_credentials_are_not_runtime_deletable(migrated_database: Any) -> None:
    with _runtime(migrated_database) as connection:
        for statement in (
            "DELETE FROM dante.external_identity",
            "DELETE FROM dante.apple_auth_grant",
            "DELETE FROM dante.webauthn_account",
            "DELETE FROM dante.passkey_credential",
        ):
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                connection.execute(statement)


def test_email_identity_m5_insert_acl_remains_column_scoped(
    migrated_database: Any,
) -> None:
    with _admin(migrated_database) as connection:
        table_insert = connection.execute(
            "SELECT has_table_privilege('dante_runtime','dante.email_identity','INSERT')"
        ).fetchone()
        insert_columns = {
            str(row[0])
            for row in connection.execute(
                "SELECT column_name "
                "FROM information_schema.column_privileges "
                "WHERE grantee='dante_runtime' "
                "AND table_schema='dante' "
                "AND table_name='email_identity' "
                "AND privilege_type='INSERT'"
            )
        }

    assert table_insert == (False,)
    assert insert_columns == {
        "email_identity_ref",
        "account_ref",
        "address",
        "comparison_key",
        "created_at",
        "verified_at",
        "recovery_restriction_code",
        "recovery_restriction_observed_at",
    }
