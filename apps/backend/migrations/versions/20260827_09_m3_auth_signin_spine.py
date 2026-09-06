"""Materialize M3-A Account, email, password and AuthSession persistence.

Revision ID: 20260827_09
Revises: 20260826_08
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260827_09"
down_revision: str | None = "20260826_08"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"

_AUTH_TABLES = (
    "account",
    "email_identity",
    "password_credential",
    "auth_session",
)


def _deny_runtime_access() -> None:
    for table_name in _AUTH_TABLES:
        op.execute(
            sa.text(
                "REVOKE ALL PRIVILEGES ON TABLE "
                f"{_DANTE_SCHEMA}.{table_name} "
                f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
            )
        )


def _activate_runtime_acl() -> None:
    op.execute(sa.text("GRANT SELECT ON TABLE dante.account TO dante_runtime"))
    op.execute(sa.text("GRANT SELECT ON TABLE dante.email_identity TO dante_runtime"))
    op.execute(sa.text("GRANT SELECT ON TABLE dante.password_credential TO dante_runtime"))
    op.execute(
        sa.text(
            "GRANT UPDATE (verifier, pepper_key_id, updated_at) "
            "ON TABLE dante.password_credential TO dante_runtime"
        )
    )
    op.execute(sa.text("GRANT SELECT, INSERT ON TABLE dante.auth_session TO dante_runtime"))
    op.execute(
        sa.text(
            "GRANT UPDATE (last_user_activity_at, revoked_at, revocation_reason_code) "
            "ON TABLE dante.auth_session TO dante_runtime"
        )
    )


def upgrade() -> None:
    """Create the first executable Access/Auth persistence slice."""
    op.create_table(
        "account",
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("disabled_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("account_ref", name=op.f("pk_account")),
        sa.CheckConstraint(
            "uuid_extract_version(account_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_account_uuidv7"),
        ),
        sa.CheckConstraint(
            "status_code IN ('active','disabled')",
            name=op.f("ck_account_status_code"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at)",
            name=op.f("ck_account_created_at"),
        ),
        sa.CheckConstraint(
            "(status_code='active' AND disabled_at IS NULL) OR "
            "(status_code='disabled' AND disabled_at IS NOT NULL "
            "AND isfinite(disabled_at) AND disabled_at >= created_at)",
            name=op.f("ck_account_disabled_state"),
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "email_identity",
        sa.Column("email_identity_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("comparison_key", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("email_identity_ref", name=op.f("pk_email_identity")),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name=op.f("fk_email_identity_account_ref_account"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "comparison_key",
            name=op.f("uq_email_identity_comparison_key"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(email_identity_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_email_identity_uuidv7"),
        ),
        sa.CheckConstraint(
            "address = btrim(address) AND address <> ''",
            name=op.f("ck_email_identity_address"),
        ),
        sa.CheckConstraint(
            "comparison_key = btrim(comparison_key) AND comparison_key <> ''",
            name=op.f("ck_email_identity_comparison_key"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at)",
            name=op.f("ck_email_identity_created_at"),
        ),
        sa.CheckConstraint(
            "verified_at IS NULL OR (isfinite(verified_at) AND verified_at >= created_at)",
            name=op.f("ck_email_identity_verified_at"),
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_email_identity_account_ref",
        "email_identity",
        ["account_ref"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "password_credential",
        sa.Column("password_credential_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("verifier", sa.Text(), nullable=False),
        sa.Column("pepper_key_id", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "password_credential_ref",
            name=op.f("pk_password_credential"),
        ),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name=op.f("fk_password_credential_account_ref_account"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "account_ref",
            name=op.f("uq_password_credential_account_ref"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(password_credential_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_password_credential_uuidv7"),
        ),
        sa.CheckConstraint(
            "verifier LIKE '$argon2id$v=19$%'",
            name=op.f("ck_password_credential_verifier_format"),
        ),
        sa.CheckConstraint(
            "pepper_key_id = btrim(pepper_key_id) AND pepper_key_id <> ''",
            name=op.f("ck_password_credential_pepper_key_id"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) AND updated_at >= created_at",
            name=op.f("ck_password_credential_chronology"),
        ),
        schema=_DANTE_SCHEMA,
    )

    op.create_table(
        "auth_session",
        sa.Column("auth_session_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("account_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("secret_verifier", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("authenticated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("recent_auth_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_user_activity_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_reason_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("auth_session_ref", name=op.f("pk_auth_session")),
        sa.ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name=op.f("fk_auth_session_account_ref_account"),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "secret_verifier",
            name=op.f("uq_auth_session_secret_verifier"),
        ),
        sa.CheckConstraint(
            "uuid_extract_version(auth_session_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_auth_session_uuidv7"),
        ),
        sa.CheckConstraint(
            "octet_length(secret_verifier) = 32",
            name=op.f("ck_auth_session_secret_verifier_length"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at) "
            "AND isfinite(authenticated_at) "
            "AND isfinite(recent_auth_at) "
            "AND isfinite(last_user_activity_at) "
            "AND isfinite(expires_at) "
            "AND authenticated_at >= created_at "
            "AND recent_auth_at >= authenticated_at "
            "AND last_user_activity_at >= created_at "
            "AND expires_at > authenticated_at",
            name=op.f("ck_auth_session_chronology"),
        ),
        sa.CheckConstraint(
            "(revoked_at IS NULL AND revocation_reason_code IS NULL) OR "
            "(revoked_at IS NOT NULL AND isfinite(revoked_at) "
            "AND revoked_at >= created_at "
            "AND revocation_reason_code IS NOT NULL "
            "AND revocation_reason_code = btrim(revocation_reason_code) "
            "AND revocation_reason_code <> '')",
            name=op.f("ck_auth_session_revocation"),
        ),
        schema=_DANTE_SCHEMA,
    )
    op.create_index(
        "ix_auth_session_account_ref",
        "auth_session",
        ["account_ref"],
        unique=False,
        schema=_DANTE_SCHEMA,
    )

    _deny_runtime_access()
    _activate_runtime_acl()


def downgrade() -> None:
    """Remove the M3-A Auth persistence slice."""
    for table_name in _AUTH_TABLES:
        op.execute(
            sa.text(
                f"REVOKE ALL PRIVILEGES ON TABLE {_DANTE_SCHEMA}.{table_name} FROM {_RUNTIME_ROLE}"
            )
        )

    op.drop_table("auth_session", schema=_DANTE_SCHEMA)
    op.drop_table("password_credential", schema=_DANTE_SCHEMA)
    op.drop_table("email_identity", schema=_DANTE_SCHEMA)
    op.drop_table("account", schema=_DANTE_SCHEMA)
