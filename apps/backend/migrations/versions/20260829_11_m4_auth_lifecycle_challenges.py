"""Materialize M4 signup/recovery challenges and narrow runtime ACL delta.

Revision ID: 20260829_11
Revises: 20260827_10
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260829_11"
down_revision: str | None = "20260827_10"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"
_M4_TABLES = ("password_signup_challenge", "password_recovery_challenge")


def _deny_new_table_access() -> None:
    for table_name in _M4_TABLES:
        op.execute(
            sa.text(
                "REVOKE ALL PRIVILEGES ON TABLE "
                f"{_DANTE_SCHEMA}.{table_name} "
                f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
            )
        )


def _activate_m4_runtime_acl() -> None:
    op.execute(
        sa.text(
            "GRANT INSERT (account_ref, status_code, created_at, disabled_at) "
            "ON TABLE dante.account TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT INSERT (email_identity_ref, account_ref, address, comparison_key, "
            "created_at, verified_at) ON TABLE dante.email_identity TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT INSERT (password_credential_ref, account_ref, verifier, pepper_key_id, "
            "created_at, updated_at) ON TABLE dante.password_credential TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT UPDATE (secret_verifier, recent_auth_at, expires_at) "
            "ON TABLE dante.auth_session TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT SELECT, INSERT, DELETE ON TABLE dante.password_signup_challenge TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT UPDATE (otp_verifier, otp_key_id, updated_at, verification_issued_at, "
            "verification_expires_at, failed_verification_attempts) "
            "ON TABLE dante.password_signup_challenge TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT SELECT, INSERT, DELETE ON TABLE "
            "dante.password_recovery_challenge TO dante_runtime"
        )
    )


def upgrade() -> None:
    """Create purpose-specific M4 challenge persistence and required runtime grants."""
    op.create_unique_constraint(
        "uq_email_identity_email_identity_ref_account_ref",
        "email_identity",
        ["email_identity_ref", "account_ref"],
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "password_signup_challenge",
        sa.Column("signup_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email_address", sa.Text(), nullable=False),
        sa.Column("email_comparison_key", sa.Text(), nullable=False),
        sa.Column("password_verifier", sa.Text(), nullable=False),
        sa.Column("password_pepper_key_id", sa.Text(), nullable=False),
        sa.Column("otp_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("otp_key_id", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("signup_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("verification_issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("verification_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("failed_verification_attempts", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("signup_ref", name=op.f("pk_password_signup_challenge")),
        sa.CheckConstraint(
            "uuid_extract_version(signup_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_password_signup_challenge_uuidv7"),
        ),
        sa.CheckConstraint(
            "email_address = btrim(email_address) AND email_address <> ''",
            name=op.f("ck_password_signup_challenge_email_address"),
        ),
        sa.CheckConstraint(
            "email_comparison_key = btrim(email_comparison_key) AND email_comparison_key <> ''",
            name=op.f("ck_password_signup_challenge_email_comparison_key"),
        ),
        sa.CheckConstraint(
            "password_verifier LIKE '$argon2id$v=19$%'",
            name=op.f("ck_password_signup_challenge_password_verifier_format"),
        ),
        sa.CheckConstraint(
            "password_pepper_key_id = btrim(password_pepper_key_id) "
            "AND password_pepper_key_id <> ''",
            name=op.f("ck_password_signup_challenge_password_pepper_key_id"),
        ),
        sa.CheckConstraint(
            "octet_length(otp_verifier) = 32",
            name=op.f("ck_password_signup_challenge_otp_verifier_length"),
        ),
        sa.CheckConstraint(
            "otp_key_id = btrim(otp_key_id) AND otp_key_id <> ''",
            name=op.f("ck_password_signup_challenge_otp_key_id"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at) "
            "AND isfinite(updated_at) "
            "AND isfinite(signup_expires_at) "
            "AND isfinite(verification_issued_at) "
            "AND isfinite(verification_expires_at) "
            "AND updated_at >= created_at "
            "AND signup_expires_at > created_at "
            "AND verification_issued_at >= created_at "
            "AND verification_expires_at > verification_issued_at "
            "AND verification_expires_at <= signup_expires_at",
            name=op.f("ck_password_signup_challenge_chronology"),
        ),
        sa.CheckConstraint(
            "failed_verification_attempts BETWEEN 0 AND 5",
            name=op.f("ck_password_signup_challenge_failed_attempts"),
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_password_signup_challenge_email_comparison_key",
        "password_signup_challenge",
        ["email_comparison_key"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_password_signup_challenge_signup_expires_at",
        "password_signup_challenge",
        ["signup_expires_at"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "password_recovery_challenge",
        sa.Column("password_recovery_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email_identity_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("secret_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "password_recovery_ref",
            name=op.f("pk_password_recovery_challenge"),
        ),
        sa.ForeignKeyConstraint(
            ["email_identity_ref", "account_ref"],
            ["dante.email_identity.email_identity_ref", "dante.email_identity.account_ref"],
            name=op.f(
                "fk_password_recovery_challenge_email_identity_ref_account_ref_email_identity"
            ),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "account_ref",
            name=op.f("uq_password_recovery_challenge_account_ref"),
        ),
        sa.UniqueConstraint(
            "secret_verifier",
            name=op.f("uq_password_recovery_challenge_secret_verifier"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(password_recovery_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_password_recovery_challenge_uuidv7"),
        ),
        sa.CheckConstraint(
            "octet_length(secret_verifier) = 32",
            name=op.f("ck_password_recovery_challenge_secret_verifier_length"),
        ),
        sa.CheckConstraint(
            "isfinite(issued_at) AND isfinite(expires_at) AND expires_at > issued_at",
            name=op.f("ck_password_recovery_challenge_chronology"),
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_password_recovery_challenge_email_identity_ref",
        "password_recovery_challenge",
        ["email_identity_ref"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_password_recovery_challenge_expires_at",
        "password_recovery_challenge",
        ["expires_at"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )

    _deny_new_table_access()
    _activate_m4_runtime_acl()


def downgrade() -> None:
    """Remove only the M4 delta while restoring the exact M3 runtime posture."""
    op.execute(
        sa.text(
            "REVOKE UPDATE (secret_verifier, recent_auth_at, expires_at) "
            "ON TABLE dante.auth_session FROM dante_runtime"
        )
    )
    op.execute(sa.text("REVOKE INSERT ON TABLE dante.password_credential FROM dante_runtime"))
    op.execute(sa.text("REVOKE INSERT ON TABLE dante.email_identity FROM dante_runtime"))
    op.execute(sa.text("REVOKE INSERT ON TABLE dante.account FROM dante_runtime"))

    for table_name in reversed(_M4_TABLES):
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON TABLE {_DANTE_SCHEMA}.{table_name} FROM {_RUNTIME_ROLE}"
            )
        )
        op.drop_table(table_name, schema=_DANTE_SCHEMA)

    op.drop_constraint(
        "uq_email_identity_email_identity_ref_account_ref",
        "email_identity",
        type_="unique",
        schema=_DANTE_SCHEMA,
    )
