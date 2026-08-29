"""SQLAlchemy row mappings for DANTE Access/Auth persistence."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
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
        UniqueConstraint(
            "email_identity_ref",
            "account_ref",
            name="uq_email_identity_email_identity_ref_account_ref",
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


class PasswordSignupChallengeRow(Base):
    """Ephemeral password-signup proof state keyed by public non-secret signup_ref."""

    __tablename__ = "password_signup_challenge"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(signup_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "email_address = btrim(email_address) AND email_address <> ''",
            name="email_address",
        ),
        CheckConstraint(
            "email_comparison_key = btrim(email_comparison_key) "
            "AND email_comparison_key <> ''",
            name="email_comparison_key",
        ),
        CheckConstraint(
            "password_verifier LIKE '$argon2id$v=19$%'",
            name="password_verifier_format",
        ),
        CheckConstraint(
            "password_pepper_key_id = btrim(password_pepper_key_id) "
            "AND password_pepper_key_id <> ''",
            name="password_pepper_key_id",
        ),
        CheckConstraint(
            "octet_length(otp_verifier) = 32",
            name="otp_verifier_length",
        ),
        CheckConstraint(
            "otp_key_id = btrim(otp_key_id) AND otp_key_id <> ''",
            name="otp_key_id",
        ),
        CheckConstraint(
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
            name="chronology",
        ),
        CheckConstraint(
            "failed_verification_attempts BETWEEN 0 AND 5",
            name="failed_attempts",
        ),
        Index(
            "ix_password_signup_challenge_email_comparison_key",
            "email_comparison_key",
        ),
        Index(
            "ix_password_signup_challenge_signup_expires_at",
            "signup_expires_at",
        ),
    )

    signup_ref: Mapped[UUID] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(Text, nullable=False)
    email_comparison_key: Mapped[str] = mapped_column(Text, nullable=False)
    password_verifier: Mapped[str] = mapped_column(Text, nullable=False)
    password_pepper_key_id: Mapped[str] = mapped_column(Text, nullable=False)
    otp_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    otp_key_id: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    signup_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    verification_issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    verification_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    failed_verification_attempts: Mapped[int] = mapped_column(Integer, nullable=False)


class PasswordRecoveryChallengeRow(Base):
    """Ephemeral high-entropy password-recovery proof state for one Account/email channel."""

    __tablename__ = "password_recovery_challenge"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(password_recovery_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "octet_length(secret_verifier) = 32",
            name="secret_verifier_length",
        ),
        CheckConstraint(
            "isfinite(issued_at) AND isfinite(expires_at) AND expires_at > issued_at",
            name="chronology",
        ),
        ForeignKeyConstraint(
            ["email_identity_ref", "account_ref"],
            ["dante.email_identity.email_identity_ref", "dante.email_identity.account_ref"],
            name=(
                "fk_password_recovery_challenge_"
                "email_identity_ref_account_ref_email_identity"
            ),
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "account_ref",
            name="uq_password_recovery_challenge_account_ref",
        ),
        UniqueConstraint(
            "secret_verifier",
            name="uq_password_recovery_challenge_secret_verifier",
        ),
        Index(
            "ix_password_recovery_challenge_email_identity_ref",
            "email_identity_ref",
        ),
        Index("ix_password_recovery_challenge_expires_at", "expires_at"),
    )

    password_recovery_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    email_identity_ref: Mapped[UUID] = mapped_column(nullable=False)
    secret_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
