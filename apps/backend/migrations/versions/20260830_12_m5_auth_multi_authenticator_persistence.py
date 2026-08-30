"""Materialize M5 multi-authenticator persistence foundations.

Revision ID: 20260830_12
Revises: 20260829_11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260830_12"
down_revision: str | None = "20260829_11"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_RUNTIME = "dante_runtime"
_MIGRATOR = "dante_migrator"
_M5_TABLES = (
    "external_identity",
    "external_auth_transaction",
    "apple_auth_grant",
    "external_link_challenge",
    "external_signup_challenge",
    "account_profile_bootstrap",
    "webauthn_account",
    "passkey_credential",
    "webauthn_challenge",
)


def _deny_new_table_access() -> None:
    for table_name in _M5_TABLES:
        op.execute(
            sa.text(
                "REVOKE ALL PRIVILEGES ON TABLE "
                f"{_SCHEMA}.{table_name} FROM PUBLIC, {_RUNTIME}, {_MIGRATOR}"
            )
        )


def _activate_runtime_acl() -> None:
    statements = (
        "GRANT UPDATE (recovery_restriction_code, "
        "recovery_restriction_observed_at) ON TABLE "
        "dante.email_identity TO dante_runtime",
        "GRANT SELECT ON TABLE dante.external_identity TO dante_runtime",
        "GRANT INSERT (external_identity_ref, account_ref, email_identity_ref, "
        "provider_code, issuer, subject, provider_email_address, "
        "provider_email_private, status_code, created_at, status_changed_at, "
        "last_authenticated_at, revoked_at, revocation_reason_code) "
        "ON TABLE dante.external_identity TO dante_runtime",
        "GRANT UPDATE (provider_email_address, provider_email_private, status_code, "
        "status_changed_at, last_authenticated_at, revoked_at, "
        "revocation_reason_code) ON TABLE dante.external_identity TO dante_runtime",
        "GRANT SELECT, INSERT, DELETE ON TABLE "
        "dante.external_auth_transaction TO dante_runtime",
        "GRANT UPDATE (claimed_at) ON TABLE "
        "dante.external_auth_transaction TO dante_runtime",
        "GRANT SELECT, INSERT ON TABLE dante.apple_auth_grant TO dante_runtime",
        "GRANT UPDATE (external_identity_ref, refresh_token_ciphertext, "
        "refresh_token_nonce, encryption_key_id, status_code, updated_at, "
        "status_changed_at, pending_expires_at, revocation_requested_at, revoked_at) "
        "ON TABLE dante.apple_auth_grant TO dante_runtime",
        "GRANT SELECT, INSERT, DELETE ON TABLE "
        "dante.external_link_challenge TO dante_runtime",
        "GRANT SELECT, INSERT, DELETE ON TABLE "
        "dante.external_signup_challenge TO dante_runtime",
        "GRANT UPDATE (email_address, email_comparison_key, otp_verifier, otp_key_id, "
        "verification_issued_at, verification_expires_at, "
        "failed_verification_attempts, updated_at) ON TABLE "
        "dante.external_signup_challenge TO dante_runtime",
        "GRANT SELECT, INSERT, DELETE ON TABLE "
        "dante.account_profile_bootstrap TO dante_runtime",
        "GRANT SELECT, INSERT ON TABLE dante.webauthn_account TO dante_runtime",
        "GRANT SELECT, INSERT ON TABLE dante.passkey_credential TO dante_runtime",
        "GRANT UPDATE (sign_count, backup_state, label, status_code, updated_at, "
        "last_used_at, revoked_at, revocation_reason_code) ON TABLE "
        "dante.passkey_credential TO dante_runtime",
        "GRANT SELECT, INSERT, DELETE ON TABLE "
        "dante.webauthn_challenge TO dante_runtime",
        "GRANT UPDATE (claimed_at) ON TABLE dante.webauthn_challenge TO dante_runtime",
    )
    for statement in statements:
        op.execute(sa.text(statement))


def upgrade() -> None:
    """Materialize the reviewed M5 multi-authenticator persistence spine."""
    op.add_column(
        "email_identity",
        sa.Column("recovery_restriction_code", sa.Text(), nullable=True),
        schema=_SCHEMA,
    )
    op.add_column(
        "email_identity",
        sa.Column(
            "recovery_restriction_observed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        schema=_SCHEMA,
    )
    op.create_check_constraint(
        "ck_email_identity_recovery_restriction_code",
        "email_identity",
        "recovery_restriction_code IS NULL OR "
        "recovery_restriction_code = 'provider_delivery_disabled'",
        schema=_SCHEMA,
    )
    op.create_check_constraint(
        "ck_email_identity_recovery_restriction_observed",
        "email_identity",
        "recovery_restriction_code IS NULL OR "
        "recovery_restriction_observed_at IS NOT NULL",
        schema=_SCHEMA,
    )
    op.create_check_constraint(
        "ck_email_identity_recovery_restriction_chronology",
        "email_identity",
        "recovery_restriction_observed_at IS NULL OR "
        "(isfinite(recovery_restriction_observed_at) "
        "AND recovery_restriction_observed_at >= created_at)",
        schema=_SCHEMA,
    )
    op.create_unique_constraint(
        "uq_auth_session_auth_session_ref_account_ref",
        "auth_session",
        ["auth_session_ref", "account_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "external_identity",
        sa.Column("external_identity_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email_identity_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("provider_code", sa.Text(), nullable=False),
        sa.Column("issuer", sa.Text(), nullable=False),
        sa.Column("subject", sa.Text(), nullable=False),
        sa.Column("provider_email_address", sa.Text(), nullable=True),
        sa.Column("provider_email_private", sa.Boolean(), nullable=True),
        sa.Column("status_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status_changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_authenticated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_reason_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("external_identity_ref", name="pk_external_identity"),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_external_identity_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["email_identity_ref", "account_ref"],
            ["dante.email_identity.email_identity_ref", "dante.email_identity.account_ref"],
            name="fk_external_identity_email_account_email_identity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint("issuer", "subject", name="uq_external_identity_issuer_subject"),
        sa.UniqueConstraint(
            "external_identity_ref",
            "issuer",
            "subject",
            name="uq_external_identity_external_identity_ref_issuer_subject",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(external_identity_ref) IS NOT DISTINCT FROM 7",
            name="ck_external_identity_uuidv7",
        ),
        sa.CheckConstraint(
            "provider_code IN ('google','apple')",
            name="ck_external_identity_provider_code",
        ),
        sa.CheckConstraint(
            "(provider_code='google' AND issuer='https://accounts.google.com') OR "
            "(provider_code='apple' AND issuer='https://appleid.apple.com')",
            name="ck_external_identity_provider_issuer",
        ),
        sa.CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="ck_external_identity_subject",
        ),
        sa.CheckConstraint(
            "(provider_email_address IS NULL AND provider_email_private IS NULL) OR "
            "(provider_email_address IS NOT NULL "
            "AND provider_email_address=btrim(provider_email_address) "
            "AND provider_email_address<>'' "
            "AND char_length(provider_email_address)<=320 "
            "AND provider_email_private IS NOT NULL)",
            name="ck_external_identity_provider_email",
        ),
        sa.CheckConstraint(
            "status_code IN ('active','revoked')",
            name="ck_external_identity_status_code",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(status_changed_at) "
            "AND isfinite(last_authenticated_at) "
            "AND status_changed_at>=created_at "
            "AND last_authenticated_at>=created_at",
            name="ck_external_identity_chronology",
        ),
        sa.CheckConstraint(
            "(status_code='active' AND revoked_at IS NULL "
            "AND revocation_reason_code IS NULL) OR "
            "(status_code='revoked' AND revoked_at IS NOT NULL "
            "AND isfinite(revoked_at) AND revoked_at>=created_at "
            "AND revocation_reason_code IN "
            "('user_unlinked','provider_revoked','provider_account_deleted'))",
            name="ck_external_identity_revocation",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_identity_account_ref",
        "external_identity",
        ["account_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_identity_email_identity_ref",
        "external_identity",
        ["email_identity_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "external_auth_transaction",
        sa.Column(
            "external_auth_transaction_ref",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("provider_code", sa.Text(), nullable=False),
        sa.Column("expected_issuer", sa.Text(), nullable=False),
        sa.Column("purpose_code", sa.Text(), nullable=False),
        sa.Column("state_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("nonce_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("auth_session_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("auth_session_secret_verifier", sa.LargeBinary(), nullable=True),
        sa.Column("return_target_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "external_auth_transaction_ref",
            name="pk_external_auth_transaction",
        ),
        sa.ForeignKeyConstraint(
            ["auth_session_ref"],
            ["dante.auth_session.auth_session_ref"],
            name="fk_external_auth_transaction_auth_session_ref_auth_session",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "state_verifier",
            name="uq_external_auth_transaction_state_verifier",
        ),
        sa.UniqueConstraint(
            "nonce_verifier",
            name="uq_external_auth_transaction_nonce_verifier",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(external_auth_transaction_ref) IS NOT DISTINCT FROM 7",
            name="ck_external_auth_transaction_uuidv7",
        ),
        sa.CheckConstraint(
            "provider_code IN ('google','apple')",
            name="ck_external_auth_transaction_provider_code",
        ),
        sa.CheckConstraint(
            "(provider_code='google' "
            "AND expected_issuer='https://accounts.google.com') OR "
            "(provider_code='apple' "
            "AND expected_issuer='https://appleid.apple.com')",
            name="ck_external_auth_transaction_provider_issuer",
        ),
        sa.CheckConstraint(
            "purpose_code IN ('sign_in','link','reauthenticate')",
            name="ck_external_auth_transaction_purpose_code",
        ),
        sa.CheckConstraint(
            "return_target_code IN ('access','security')",
            name="ck_external_auth_transaction_return_target_code",
        ),
        sa.CheckConstraint(
            "octet_length(state_verifier)=32",
            name="ck_external_auth_transaction_state_verifier_length",
        ),
        sa.CheckConstraint(
            "octet_length(nonce_verifier)=32",
            name="ck_external_auth_transaction_nonce_verifier_length",
        ),
        sa.CheckConstraint(
            "(purpose_code='sign_in' AND auth_session_ref IS NULL "
            "AND auth_session_secret_verifier IS NULL) OR "
            "(purpose_code IN ('link','reauthenticate') "
            "AND auth_session_ref IS NOT NULL "
            "AND auth_session_secret_verifier IS NOT NULL "
            "AND octet_length(auth_session_secret_verifier)=32)",
            name="ck_external_auth_transaction_session_binding",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '15 minutes'",
            name="ck_external_auth_transaction_chronology",
        ),
        sa.CheckConstraint(
            "claimed_at IS NULL OR (isfinite(claimed_at) "
            "AND claimed_at>=created_at AND claimed_at<=expires_at)",
            name="ck_external_auth_transaction_claimed_at",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_auth_transaction_expires_at",
        "external_auth_transaction",
        ["expires_at"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_auth_transaction_auth_session_ref",
        "external_auth_transaction",
        ["auth_session_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "apple_auth_grant",
        sa.Column("apple_auth_grant_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("external_identity_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("issuer", sa.Text(), nullable=False),
        sa.Column("subject", sa.Text(), nullable=False),
        sa.Column("client_id", sa.Text(), nullable=False),
        sa.Column("refresh_token_ciphertext", sa.LargeBinary(), nullable=True),
        sa.Column("refresh_token_nonce", sa.LargeBinary(), nullable=True),
        sa.Column("encryption_key_id", sa.Text(), nullable=True),
        sa.Column("status_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status_changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("pending_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_requested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("apple_auth_grant_ref", name="pk_apple_auth_grant"),
        sa.ForeignKeyConstraint(
            ["external_identity_ref", "issuer", "subject"],
            [
                "dante.external_identity.external_identity_ref",
                "dante.external_identity.issuer",
                "dante.external_identity.subject",
            ],
            name="fk_apple_auth_grant_external_identity_subject",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint("issuer", "subject", name="uq_apple_auth_grant_issuer_subject"),
        sa.UniqueConstraint(
            "external_identity_ref",
            name="uq_apple_auth_grant_external_identity_ref",
        ),
        sa.UniqueConstraint(
            "apple_auth_grant_ref",
            "issuer",
            "subject",
            name="uq_apple_auth_grant_ref_issuer_subject",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(apple_auth_grant_ref) IS NOT DISTINCT FROM 7",
            name="ck_apple_auth_grant_uuidv7",
        ),
        sa.CheckConstraint(
            "issuer='https://appleid.apple.com'",
            name="ck_apple_auth_grant_issuer",
        ),
        sa.CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="ck_apple_auth_grant_subject",
        ),
        sa.CheckConstraint(
            "client_id=btrim(client_id) AND client_id<>'' "
            "AND char_length(client_id)<=255",
            name="ck_apple_auth_grant_client_id",
        ),
        sa.CheckConstraint(
            "status_code IN ('pending','active','revocation_pending','revoked')",
            name="ck_apple_auth_grant_status_code",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) "
            "AND isfinite(status_changed_at) AND updated_at>=created_at "
            "AND status_changed_at>=created_at "
            "AND (pending_expires_at IS NULL OR "
            "(isfinite(pending_expires_at) AND pending_expires_at>created_at "
            "AND pending_expires_at<=created_at+interval '30 minutes')) "
            "AND (revocation_requested_at IS NULL OR "
            "(isfinite(revocation_requested_at) "
            "AND revocation_requested_at>=created_at)) "
            "AND (revoked_at IS NULL OR "
            "(isfinite(revoked_at) AND revoked_at>=created_at))",
            name="ck_apple_auth_grant_chronology",
        ),
        sa.CheckConstraint(
            "refresh_token_ciphertext IS NULL OR "
            "(octet_length(refresh_token_ciphertext)>16 "
            "AND octet_length(refresh_token_ciphertext)<=16384)",
            name="ck_apple_auth_grant_ciphertext",
        ),
        sa.CheckConstraint(
            "refresh_token_nonce IS NULL OR octet_length(refresh_token_nonce)=12",
            name="ck_apple_auth_grant_nonce",
        ),
        sa.CheckConstraint(
            "encryption_key_id IS NULL OR "
            "(encryption_key_id=btrim(encryption_key_id) "
            "AND encryption_key_id<>'' AND char_length(encryption_key_id)<=128)",
            name="ck_apple_auth_grant_encryption_key_id",
        ),
        sa.CheckConstraint(
            "(status_code='pending' AND pending_expires_at IS NOT NULL "
            "AND refresh_token_ciphertext IS NOT NULL "
            "AND refresh_token_nonce IS NOT NULL "
            "AND encryption_key_id IS NOT NULL "
            "AND revocation_requested_at IS NULL AND revoked_at IS NULL) OR "
            "(status_code='active' AND external_identity_ref IS NOT NULL "
            "AND pending_expires_at IS NULL "
            "AND refresh_token_ciphertext IS NOT NULL "
            "AND refresh_token_nonce IS NOT NULL "
            "AND encryption_key_id IS NOT NULL "
            "AND revocation_requested_at IS NULL AND revoked_at IS NULL) OR "
            "(status_code='revocation_pending' AND pending_expires_at IS NULL "
            "AND refresh_token_ciphertext IS NOT NULL "
            "AND refresh_token_nonce IS NOT NULL "
            "AND encryption_key_id IS NOT NULL "
            "AND revocation_requested_at IS NOT NULL AND revoked_at IS NULL) OR "
            "(status_code='revoked' AND pending_expires_at IS NULL "
            "AND refresh_token_ciphertext IS NULL "
            "AND refresh_token_nonce IS NULL AND encryption_key_id IS NULL "
            "AND revoked_at IS NOT NULL)",
            name="ck_apple_auth_grant_state",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_apple_auth_grant_status_updated_at",
        "apple_auth_grant",
        ["status_code", "updated_at"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_apple_auth_grant_pending_expires_at",
        "apple_auth_grant",
        ["pending_expires_at"],
        schema=_SCHEMA,
    )

    op.create_table(
        "external_link_challenge",
        sa.Column("external_link_challenge_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_email_identity_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider_code", sa.Text(), nullable=False),
        sa.Column("issuer", sa.Text(), nullable=False),
        sa.Column("subject", sa.Text(), nullable=False),
        sa.Column("provider_email_address", sa.Text(), nullable=True),
        sa.Column("provider_email_private", sa.Boolean(), nullable=True),
        sa.Column("apple_auth_grant_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("continuation_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "external_link_challenge_ref",
            name="pk_external_link_challenge",
        ),
        sa.ForeignKeyConstraint(
            ["target_account_ref"],
            ["dante.account.account_ref"],
            name="fk_external_link_challenge_target_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["target_email_identity_ref", "target_account_ref"],
            ["dante.email_identity.email_identity_ref", "dante.email_identity.account_ref"],
            name="fk_external_link_challenge_target_email_account_email_identity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["apple_auth_grant_ref", "issuer", "subject"],
            [
                "dante.apple_auth_grant.apple_auth_grant_ref",
                "dante.apple_auth_grant.issuer",
                "dante.apple_auth_grant.subject",
            ],
            name="fk_external_link_challenge_apple_grant",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "issuer",
            "subject",
            name="uq_external_link_challenge_issuer_subject",
        ),
        sa.UniqueConstraint(
            "continuation_verifier",
            name="uq_external_link_challenge_continuation_verifier",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(external_link_challenge_ref) IS NOT DISTINCT FROM 7",
            name="ck_external_link_challenge_uuidv7",
        ),
        sa.CheckConstraint(
            "provider_code IN ('google','apple')",
            name="ck_external_link_challenge_provider_code",
        ),
        sa.CheckConstraint(
            "(provider_code='google' AND issuer='https://accounts.google.com') OR "
            "(provider_code='apple' AND issuer='https://appleid.apple.com')",
            name="ck_external_link_challenge_provider_issuer",
        ),
        sa.CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="ck_external_link_challenge_subject",
        ),
        sa.CheckConstraint(
            "(provider_email_address IS NULL AND provider_email_private IS NULL) OR "
            "(provider_email_address IS NOT NULL "
            "AND provider_email_address=btrim(provider_email_address) "
            "AND provider_email_address<>'' "
            "AND char_length(provider_email_address)<=320 "
            "AND provider_email_private IS NOT NULL)",
            name="ck_external_link_challenge_provider_email",
        ),
        sa.CheckConstraint(
            "(provider_code='google' AND apple_auth_grant_ref IS NULL) OR "
            "(provider_code='apple' AND apple_auth_grant_ref IS NOT NULL)",
            name="ck_external_link_challenge_provider_grant",
        ),
        sa.CheckConstraint(
            "octet_length(continuation_verifier)=32",
            name="ck_external_link_challenge_continuation_verifier_length",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '15 minutes'",
            name="ck_external_link_challenge_chronology",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_link_challenge_target_account_ref",
        "external_link_challenge",
        ["target_account_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_link_challenge_target_email_identity_ref",
        "external_link_challenge",
        ["target_email_identity_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_link_challenge_apple_auth_grant_ref",
        "external_link_challenge",
        ["apple_auth_grant_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_link_challenge_expires_at",
        "external_link_challenge",
        ["expires_at"],
        schema=_SCHEMA,
    )

    op.create_table(
        "external_signup_challenge",
        sa.Column("external_signup_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider_code", sa.Text(), nullable=False),
        sa.Column("issuer", sa.Text(), nullable=False),
        sa.Column("subject", sa.Text(), nullable=False),
        sa.Column("provider_email_address", sa.Text(), nullable=True),
        sa.Column("provider_email_private", sa.Boolean(), nullable=True),
        sa.Column("apple_auth_grant_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("continuation_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("email_address", sa.Text(), nullable=True),
        sa.Column("email_comparison_key", sa.Text(), nullable=True),
        sa.Column("otp_verifier", sa.LargeBinary(), nullable=True),
        sa.Column("otp_key_id", sa.Text(), nullable=True),
        sa.Column("verification_issued_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verification_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_verification_attempts", sa.Integer(), nullable=False),
        sa.Column("bootstrap_display_name", sa.Text(), nullable=True),
        sa.Column("bootstrap_given_name", sa.Text(), nullable=True),
        sa.Column("bootstrap_family_name", sa.Text(), nullable=True),
        sa.Column("bootstrap_picture_url", sa.Text(), nullable=True),
        sa.Column("bootstrap_locale", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("external_signup_ref", name="pk_external_signup_challenge"),
        sa.ForeignKeyConstraint(
            ["apple_auth_grant_ref", "issuer", "subject"],
            [
                "dante.apple_auth_grant.apple_auth_grant_ref",
                "dante.apple_auth_grant.issuer",
                "dante.apple_auth_grant.subject",
            ],
            name="fk_external_signup_challenge_apple_grant",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "issuer",
            "subject",
            name="uq_external_signup_challenge_issuer_subject",
        ),
        sa.UniqueConstraint(
            "continuation_verifier",
            name="uq_external_signup_challenge_continuation_verifier",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(external_signup_ref) IS NOT DISTINCT FROM 7",
            name="ck_external_signup_challenge_uuidv7",
        ),
        sa.CheckConstraint(
            "provider_code IN ('google','apple')",
            name="ck_external_signup_challenge_provider_code",
        ),
        sa.CheckConstraint(
            "(provider_code='google' AND issuer='https://accounts.google.com') OR "
            "(provider_code='apple' AND issuer='https://appleid.apple.com')",
            name="ck_external_signup_challenge_provider_issuer",
        ),
        sa.CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="ck_external_signup_challenge_subject",
        ),
        sa.CheckConstraint(
            "(provider_email_address IS NULL AND provider_email_private IS NULL) OR "
            "(provider_email_address IS NOT NULL "
            "AND provider_email_address=btrim(provider_email_address) "
            "AND provider_email_address<>'' "
            "AND char_length(provider_email_address)<=320 "
            "AND provider_email_private IS NOT NULL)",
            name="ck_external_signup_challenge_provider_email",
        ),
        sa.CheckConstraint(
            "(provider_code='google' AND apple_auth_grant_ref IS NULL) OR "
            "(provider_code='apple' AND apple_auth_grant_ref IS NOT NULL)",
            name="ck_external_signup_challenge_provider_grant",
        ),
        sa.CheckConstraint(
            "octet_length(continuation_verifier)=32",
            name="ck_external_signup_challenge_continuation_verifier_length",
        ),
        sa.CheckConstraint(
            "(email_address IS NULL AND email_comparison_key IS NULL) OR "
            "(email_address IS NOT NULL AND email_comparison_key IS NOT NULL)",
            name="ck_external_signup_challenge_email_pair",
        ),
        sa.CheckConstraint(
            "(email_address IS NULL AND otp_verifier IS NULL AND otp_key_id IS NULL "
            "AND verification_issued_at IS NULL "
            "AND verification_expires_at IS NULL "
            "AND failed_verification_attempts=0) OR "
            "(email_address IS NOT NULL "
            "AND email_address=btrim(email_address) AND email_address<>'' "
            "AND char_length(email_address)<=320 "
            "AND email_comparison_key=btrim(email_comparison_key) "
            "AND email_comparison_key<>'' "
            "AND char_length(email_comparison_key)<=320 "
            "AND otp_verifier IS NOT NULL AND octet_length(otp_verifier)=32 "
            "AND otp_key_id IS NOT NULL AND otp_key_id=btrim(otp_key_id) "
            "AND otp_key_id<>'' AND char_length(otp_key_id)<=128 "
            "AND verification_issued_at IS NOT NULL "
            "AND isfinite(verification_issued_at) "
            "AND verification_expires_at IS NOT NULL "
            "AND isfinite(verification_expires_at) "
            "AND verification_expires_at>verification_issued_at "
            "AND verification_expires_at<=verification_issued_at+interval '15 minutes' "
            "AND verification_expires_at<=expires_at)",
            name="ck_external_signup_challenge_email_verification",
        ),
        sa.CheckConstraint(
            "failed_verification_attempts BETWEEN 0 AND 5",
            name="ck_external_signup_challenge_failed_attempts",
        ),
        sa.CheckConstraint(
            "bootstrap_display_name IS NULL OR "
            "(bootstrap_display_name=btrim(bootstrap_display_name) "
            "AND bootstrap_display_name<>'' "
            "AND char_length(bootstrap_display_name)<=256)",
            name="ck_external_signup_challenge_bootstrap_display_name",
        ),
        sa.CheckConstraint(
            "bootstrap_given_name IS NULL OR "
            "(bootstrap_given_name=btrim(bootstrap_given_name) "
            "AND bootstrap_given_name<>'' "
            "AND char_length(bootstrap_given_name)<=128)",
            name="ck_external_signup_challenge_bootstrap_given_name",
        ),
        sa.CheckConstraint(
            "bootstrap_family_name IS NULL OR "
            "(bootstrap_family_name=btrim(bootstrap_family_name) "
            "AND bootstrap_family_name<>'' "
            "AND char_length(bootstrap_family_name)<=128)",
            name="ck_external_signup_challenge_bootstrap_family_name",
        ),
        sa.CheckConstraint(
            "bootstrap_picture_url IS NULL OR "
            "(bootstrap_picture_url=btrim(bootstrap_picture_url) "
            "AND bootstrap_picture_url<>'' "
            "AND char_length(bootstrap_picture_url)<=2048)",
            name="ck_external_signup_challenge_bootstrap_picture_url",
        ),
        sa.CheckConstraint(
            "bootstrap_locale IS NULL OR "
            "(bootstrap_locale=btrim(bootstrap_locale) "
            "AND bootstrap_locale<>'' "
            "AND char_length(bootstrap_locale)<=64)",
            name="ck_external_signup_challenge_bootstrap_locale",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) "
            "AND isfinite(expires_at) AND updated_at>=created_at "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '30 minutes'",
            name="ck_external_signup_challenge_chronology",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_signup_challenge_email_comparison_key",
        "external_signup_challenge",
        ["email_comparison_key"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_signup_challenge_apple_auth_grant_ref",
        "external_signup_challenge",
        ["apple_auth_grant_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_external_signup_challenge_expires_at",
        "external_signup_challenge",
        ["expires_at"],
        schema=_SCHEMA,
    )

    op.create_table(
        "account_profile_bootstrap",
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_provider_code", sa.Text(), nullable=False),
        sa.Column("source_issuer", sa.Text(), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=True),
        sa.Column("given_name", sa.Text(), nullable=True),
        sa.Column("family_name", sa.Text(), nullable=True),
        sa.Column("picture_url", sa.Text(), nullable=True),
        sa.Column("locale", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("account_ref", name="pk_account_profile_bootstrap"),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_account_profile_bootstrap_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.CheckConstraint(
            "source_provider_code IN ('google','apple')",
            name="ck_account_profile_bootstrap_source_provider_code",
        ),
        sa.CheckConstraint(
            "(source_provider_code='google' "
            "AND source_issuer='https://accounts.google.com') OR "
            "(source_provider_code='apple' "
            "AND source_issuer='https://appleid.apple.com')",
            name="ck_account_profile_bootstrap_source_provider_issuer",
        ),
        sa.CheckConstraint(
            "display_name IS NOT NULL OR given_name IS NOT NULL "
            "OR family_name IS NOT NULL OR picture_url IS NOT NULL "
            "OR locale IS NOT NULL",
            name="ck_account_profile_bootstrap_nonempty",
        ),
        sa.CheckConstraint(
            "display_name IS NULL OR (display_name=btrim(display_name) "
            "AND display_name<>'' AND char_length(display_name)<=256)",
            name="ck_account_profile_bootstrap_display_name",
        ),
        sa.CheckConstraint(
            "given_name IS NULL OR (given_name=btrim(given_name) "
            "AND given_name<>'' AND char_length(given_name)<=128)",
            name="ck_account_profile_bootstrap_given_name",
        ),
        sa.CheckConstraint(
            "family_name IS NULL OR (family_name=btrim(family_name) "
            "AND family_name<>'' AND char_length(family_name)<=128)",
            name="ck_account_profile_bootstrap_family_name",
        ),
        sa.CheckConstraint(
            "picture_url IS NULL OR (picture_url=btrim(picture_url) "
            "AND picture_url<>'' AND char_length(picture_url)<=2048)",
            name="ck_account_profile_bootstrap_picture_url",
        ),
        sa.CheckConstraint(
            "locale IS NULL OR (locale=btrim(locale) "
            "AND locale<>'' AND char_length(locale)<=64)",
            name="ck_account_profile_bootstrap_locale",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '30 days'",
            name="ck_account_profile_bootstrap_chronology",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_account_profile_bootstrap_expires_at",
        "account_profile_bootstrap",
        ["expires_at"],
        schema=_SCHEMA,
    )

    op.create_table(
        "webauthn_account",
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_handle", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("account_ref", name="pk_webauthn_account"),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_webauthn_account_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint("user_handle", name="uq_webauthn_account_user_handle"),
        sa.UniqueConstraint(
            "account_ref",
            "user_handle",
            name="uq_webauthn_account_account_ref_user_handle",
        ),
        sa.CheckConstraint(
            "octet_length(user_handle)=32",
            name="ck_webauthn_account_user_handle_length",
        ),
        sa.CheckConstraint("isfinite(created_at)", name="ck_webauthn_account_created_at"),
        schema=_SCHEMA,
    )

    op.create_table(
        "passkey_credential",
        sa.Column("passkey_credential_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("credential_id", sa.LargeBinary(), nullable=False),
        sa.Column("credential_public_key", sa.LargeBinary(), nullable=False),
        sa.Column("cose_algorithm", sa.Integer(), nullable=False),
        sa.Column("sign_count", sa.BigInteger(), nullable=False),
        sa.Column("backup_eligible", sa.Boolean(), nullable=False),
        sa.Column("backup_state", sa.Boolean(), nullable=False),
        sa.Column("transports", postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column("status_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_reason_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("passkey_credential_ref", name="pk_passkey_credential"),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            ["dante.webauthn_account.account_ref"],
            name="fk_passkey_credential_account_ref_webauthn_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "credential_id",
            name="uq_passkey_credential_credential_id",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(passkey_credential_ref) IS NOT DISTINCT FROM 7",
            name="ck_passkey_credential_uuidv7",
        ),
        sa.CheckConstraint(
            "octet_length(credential_id) BETWEEN 1 AND 1023",
            name="ck_passkey_credential_credential_id_length",
        ),
        sa.CheckConstraint(
            "octet_length(credential_public_key) BETWEEN 1 AND 8192",
            name="ck_passkey_credential_public_key_length",
        ),
        sa.CheckConstraint(
            "sign_count BETWEEN 0 AND 4294967295",
            name="ck_passkey_credential_sign_count",
        ),
        sa.CheckConstraint(
            "cardinality(transports)<=8 AND array_position(transports,NULL) IS NULL",
            name="ck_passkey_credential_transports",
        ),
        sa.CheckConstraint(
            "NOT backup_state OR backup_eligible",
            name="ck_passkey_credential_backup_state",
        ),
        sa.CheckConstraint(
            "label=btrim(label) AND label<>'' AND char_length(label)<=100",
            name="ck_passkey_credential_label",
        ),
        sa.CheckConstraint(
            "status_code IN ('active','revoked')",
            name="ck_passkey_credential_status_code",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) "
            "AND updated_at>=created_at "
            "AND (last_used_at IS NULL OR "
            "(isfinite(last_used_at) AND last_used_at>=created_at "
            "AND last_used_at<=updated_at))",
            name="ck_passkey_credential_chronology",
        ),
        sa.CheckConstraint(
            "(status_code='active' AND revoked_at IS NULL "
            "AND revocation_reason_code IS NULL) OR "
            "(status_code='revoked' AND revoked_at IS NOT NULL "
            "AND isfinite(revoked_at) AND revoked_at>=created_at "
            "AND revoked_at<=updated_at "
            "AND revocation_reason_code='user_removed')",
            name="ck_passkey_credential_revocation",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_passkey_credential_account_status",
        "passkey_credential",
        ["account_ref", "status_code"],
        schema=_SCHEMA,
    )

    op.create_table(
        "webauthn_challenge",
        sa.Column("webauthn_challenge_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ceremony_code", sa.Text(), nullable=False),
        sa.Column("challenge_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("auth_session_ref", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("auth_session_secret_verifier", sa.LargeBinary(), nullable=True),
        sa.Column("user_handle", sa.LargeBinary(), nullable=True),
        sa.Column("rp_id", sa.Text(), nullable=False),
        sa.Column("expected_origin", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("webauthn_challenge_ref", name="pk_webauthn_challenge"),
        sa.ForeignKeyConstraint(
            ["auth_session_ref", "account_ref"],
            ["dante.auth_session.auth_session_ref", "dante.auth_session.account_ref"],
            name="fk_webauthn_challenge_session_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.ForeignKeyConstraint(
            ["account_ref", "user_handle"],
            ["dante.webauthn_account.account_ref", "dante.webauthn_account.user_handle"],
            name="fk_webauthn_challenge_account_user_handle",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "challenge_verifier",
            name="uq_webauthn_challenge_challenge_verifier",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(webauthn_challenge_ref) IS NOT DISTINCT FROM 7",
            name="ck_webauthn_challenge_uuidv7",
        ),
        sa.CheckConstraint(
            "ceremony_code IN ('registration','authentication','reauthentication')",
            name="ck_webauthn_challenge_ceremony_code",
        ),
        sa.CheckConstraint(
            "octet_length(challenge_verifier)=32",
            name="ck_webauthn_challenge_challenge_verifier_length",
        ),
        sa.CheckConstraint(
            "rp_id=btrim(rp_id) AND rp_id<>'' AND char_length(rp_id)<=253",
            name="ck_webauthn_challenge_rp_id",
        ),
        sa.CheckConstraint(
            "expected_origin=btrim(expected_origin) AND expected_origin<>'' "
            "AND char_length(expected_origin)<=2048",
            name="ck_webauthn_challenge_expected_origin",
        ),
        sa.CheckConstraint(
            "(ceremony_code='authentication' AND account_ref IS NULL "
            "AND auth_session_ref IS NULL "
            "AND auth_session_secret_verifier IS NULL "
            "AND user_handle IS NULL) OR "
            "(ceremony_code IN ('registration','reauthentication') "
            "AND account_ref IS NOT NULL AND auth_session_ref IS NOT NULL "
            "AND auth_session_secret_verifier IS NOT NULL "
            "AND octet_length(auth_session_secret_verifier)=32 "
            "AND user_handle IS NOT NULL AND octet_length(user_handle)=32)",
            name="ck_webauthn_challenge_session_binding",
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '5 minutes'",
            name="ck_webauthn_challenge_chronology",
        ),
        sa.CheckConstraint(
            "claimed_at IS NULL OR (isfinite(claimed_at) "
            "AND claimed_at>=created_at AND claimed_at<=expires_at)",
            name="ck_webauthn_challenge_claimed_at",
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_webauthn_challenge_expires_at",
        "webauthn_challenge",
        ["expires_at"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_webauthn_challenge_account_ref",
        "webauthn_challenge",
        ["account_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_webauthn_challenge_auth_session_ref",
        "webauthn_challenge",
        ["auth_session_ref"],
        schema=_SCHEMA,
    )

    _deny_new_table_access()
    _activate_runtime_acl()


def downgrade() -> None:
    """Remove only the M5 persistence delta and restore the exact M4 posture."""
    op.execute(
        sa.text(
            "REVOKE UPDATE (recovery_restriction_code, "
            "recovery_restriction_observed_at) ON TABLE "
            "dante.email_identity FROM dante_runtime"
        )
    )
    for table_name in reversed(_M5_TABLES):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON TABLE {_SCHEMA}.{table_name} "
                f"FROM {_RUNTIME}"
            )
        )
        op.drop_table(table_name, schema=_SCHEMA)
    op.drop_constraint(
        "uq_auth_session_auth_session_ref_account_ref",
        "auth_session",
        type_="unique",
        schema=_SCHEMA,
    )
    op.drop_constraint(
        "ck_email_identity_recovery_restriction_chronology",
        "email_identity",
        type_="check",
        schema=_SCHEMA,
    )
    op.drop_constraint(
        "ck_email_identity_recovery_restriction_observed",
        "email_identity",
        type_="check",
        schema=_SCHEMA,
    )
    op.drop_constraint(
        "ck_email_identity_recovery_restriction_code",
        "email_identity",
        type_="check",
        schema=_SCHEMA,
    )
    op.drop_column(
        "email_identity",
        "recovery_restriction_observed_at",
        schema=_SCHEMA,
    )
    op.drop_column("email_identity", "recovery_restriction_code", schema=_SCHEMA)
