"""SQLAlchemy row mappings for DANTE Access/Auth persistence."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    LargeBinary,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base


class AccountRow(Base):
    """Persistence row for dante.account; not a Person or runtime Principal."""

    __tablename__ = "account"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(account_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "status_code IN ('active','disabled')",
            name="status_code",
        ),
        CheckConstraint(
            "isfinite(created_at)",
            name="created_at",
        ),
        CheckConstraint(
            "(status_code='active' AND disabled_at IS NULL) OR "
            "(status_code='disabled' AND disabled_at IS NOT NULL "
            "AND isfinite(disabled_at) AND disabled_at >= created_at)",
            name="disabled_state",
        ),
    )

    account_ref: Mapped[UUID] = mapped_column(primary_key=True)
    status_code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    disabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class EmailIdentityRow(Base):
    """Persistence row for one DANTE account email identity."""

    __tablename__ = "email_identity"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(email_identity_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "address = btrim(address) AND address <> ''",
            name="address",
        ),
        CheckConstraint(
            "comparison_key = btrim(comparison_key) AND comparison_key <> ''",
            name="comparison_key",
        ),
        CheckConstraint(
            "isfinite(created_at)",
            name="created_at",
        ),
        CheckConstraint(
            "verified_at IS NULL OR (isfinite(verified_at) AND verified_at >= created_at)",
            name="verified_at",
        ),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_email_identity_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "comparison_key",
            name="uq_email_identity_comparison_key",
        ),
        Index("ix_email_identity_account_ref", "account_ref"),
    )

    email_identity_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    comparison_key: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class PasswordCredentialRow(Base):
    """Persistence row for the current optional password credential of an Account."""

    __tablename__ = "password_credential"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(password_credential_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "verifier LIKE '$argon2id$v=19$%'",
            name="verifier_format",
        ),
        CheckConstraint(
            "pepper_key_id = btrim(pepper_key_id) AND pepper_key_id <> ''",
            name="pepper_key_id",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) AND updated_at >= created_at",
            name="chronology",
        ),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_password_credential_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "account_ref",
            name="uq_password_credential_account_ref",
        ),
    )

    password_credential_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    verifier: Mapped[str] = mapped_column(Text, nullable=False)
    pepper_key_id: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AuthSessionRow(Base):
    """Persistence row for one independent server-authoritative authentication session."""

    __tablename__ = "auth_session"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(auth_session_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "octet_length(secret_verifier) = 32",
            name="secret_verifier_length",
        ),
        CheckConstraint(
            "isfinite(created_at) "
            "AND isfinite(authenticated_at) "
            "AND isfinite(recent_auth_at) "
            "AND isfinite(last_user_activity_at) "
            "AND isfinite(expires_at) "
            "AND authenticated_at >= created_at "
            "AND recent_auth_at >= authenticated_at "
            "AND last_user_activity_at >= created_at "
            "AND expires_at > authenticated_at",
            name="chronology",
        ),
        CheckConstraint(
            "(revoked_at IS NULL AND revocation_reason_code IS NULL) OR "
            "(revoked_at IS NOT NULL AND isfinite(revoked_at) "
            "AND revoked_at >= created_at "
            "AND revocation_reason_code IS NOT NULL "
            "AND revocation_reason_code = btrim(revocation_reason_code) "
            "AND revocation_reason_code <> '')",
            name="revocation",
        ),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_auth_session_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "secret_verifier",
            name="uq_auth_session_secret_verifier",
        ),
        Index("ix_auth_session_account_ref", "account_ref"),
    )

    auth_session_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    secret_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    authenticated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recent_auth_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_user_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_reason_code: Mapped[str | None] = mapped_column(Text, nullable=True)
