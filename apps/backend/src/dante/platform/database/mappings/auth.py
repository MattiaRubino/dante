"""SQLAlchemy row mappings for DANTE Access/Auth persistence."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    LargeBinary,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects import postgresql
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
        CheckConstraint("status_code IN ('active','disabled')", name="status_code"),
        CheckConstraint("isfinite(created_at)", name="created_at"),
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
    """Persistence row for one DANTE Account email identity."""

    __tablename__ = "email_identity"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(email_identity_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("address = btrim(address) AND address <> ''", name="address"),
        CheckConstraint(
            "comparison_key = btrim(comparison_key) AND comparison_key <> ''",
            name="comparison_key",
        ),
        CheckConstraint("isfinite(created_at)", name="created_at"),
        CheckConstraint(
            "verified_at IS NULL OR "
            "(isfinite(verified_at) AND verified_at >= created_at)",
            name="verified_at",
        ),
        CheckConstraint(
            "recovery_restriction_code IS NULL OR "
            "recovery_restriction_code = 'provider_delivery_disabled'",
            name="recovery_restriction_code",
        ),
        CheckConstraint(
            "recovery_restriction_code IS NULL OR "
            "recovery_restriction_observed_at IS NOT NULL",
            name="recovery_restriction_observed",
        ),
        CheckConstraint(
            "recovery_restriction_observed_at IS NULL OR "
            "(isfinite(recovery_restriction_observed_at) "
            "AND recovery_restriction_observed_at >= created_at)",
            name="recovery_restriction_chronology",
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
        UniqueConstraint("comparison_key", name="uq_email_identity_comparison_key"),
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
    recovery_restriction_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    recovery_restriction_observed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class PasswordCredentialRow(Base):
    """Persistence row for the current optional password credential of an Account."""

    __tablename__ = "password_credential"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(password_credential_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("verifier LIKE '$argon2id$v=19$%'", name="verifier_format"),
        CheckConstraint(
            "pepper_key_id = btrim(pepper_key_id) AND pepper_key_id <> ''",
            name="pepper_key_id",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) "
            "AND updated_at >= created_at",
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
        UniqueConstraint("account_ref", name="uq_password_credential_account_ref"),
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
        CheckConstraint("octet_length(secret_verifier) = 32", name="secret_verifier_length"),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(authenticated_at) "
            "AND isfinite(recent_auth_at) AND isfinite(last_user_activity_at) "
            "AND isfinite(expires_at) AND authenticated_at >= created_at "
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
        UniqueConstraint("secret_verifier", name="uq_auth_session_secret_verifier"),
        UniqueConstraint(
            "auth_session_ref",
            "account_ref",
            name="uq_auth_session_auth_session_ref_account_ref",
        ),
        Index("ix_auth_session_account_ref", "account_ref"),
    )

    auth_session_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    secret_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    authenticated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recent_auth_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_user_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
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
        CheckConstraint("octet_length(otp_verifier) = 32", name="otp_verifier_length"),
        CheckConstraint(
            "otp_key_id = btrim(otp_key_id) AND otp_key_id <> ''",
            name="otp_key_id",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) "
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
        Index("ix_password_signup_challenge_email_comparison_key", "email_comparison_key"),
        Index("ix_password_signup_challenge_signup_expires_at", "signup_expires_at"),
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
        CheckConstraint("octet_length(secret_verifier) = 32", name="secret_verifier_length"),
        CheckConstraint(
            "isfinite(issued_at) AND isfinite(expires_at) AND expires_at > issued_at",
            name="chronology",
        ),
        ForeignKeyConstraint(
            ["email_identity_ref", "account_ref"],
            ["dante.email_identity.email_identity_ref", "dante.email_identity.account_ref"],
            name="fk_password_recovery_challenge_email_account_email_identity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint("account_ref", name="uq_password_recovery_challenge_account_ref"),
        UniqueConstraint(
            "secret_verifier",
            name="uq_password_recovery_challenge_secret_verifier",
        ),
        Index("ix_password_recovery_challenge_email_identity_ref", "email_identity_ref"),
        Index("ix_password_recovery_challenge_expires_at", "expires_at"),
    )

    password_recovery_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    email_identity_ref: Mapped[UUID] = mapped_column(nullable=False)
    secret_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExternalIdentityRow(Base):
    """Durable lifetime binding between an Account and a provider identity."""

    __tablename__ = "external_identity"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(external_identity_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("provider_code IN ('google','apple')", name="provider_code"),
        CheckConstraint(
            "(provider_code='google' AND issuer='https://accounts.google.com') OR "
            "(provider_code='apple' AND issuer='https://appleid.apple.com')",
            name="provider_issuer",
        ),
        CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="subject",
        ),
        CheckConstraint(
            "(provider_email_address IS NULL AND provider_email_private IS NULL) OR "
            "(provider_email_address IS NOT NULL "
            "AND provider_email_address=btrim(provider_email_address) "
            "AND provider_email_address<>'' "
            "AND char_length(provider_email_address)<=320 "
            "AND provider_email_private IS NOT NULL)",
            name="provider_email",
        ),
        CheckConstraint("status_code IN ('active','revoked')", name="status_code"),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(status_changed_at) "
            "AND isfinite(last_authenticated_at) "
            "AND status_changed_at>=created_at "
            "AND last_authenticated_at>=created_at",
            name="chronology",
        ),
        CheckConstraint(
            "(status_code='active' AND revoked_at IS NULL "
            "AND revocation_reason_code IS NULL) OR "
            "(status_code='revoked' AND revoked_at IS NOT NULL "
            "AND isfinite(revoked_at) AND revoked_at>=created_at "
            "AND revocation_reason_code IN "
            "('user_unlinked','provider_revoked','provider_account_deleted'))",
            name="revocation",
        ),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_external_identity_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["email_identity_ref", "account_ref"],
            ["dante.email_identity.email_identity_ref", "dante.email_identity.account_ref"],
            name="fk_external_identity_email_account_email_identity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint("issuer", "subject", name="uq_external_identity_issuer_subject"),
        UniqueConstraint(
            "external_identity_ref",
            "issuer",
            "subject",
            name="uq_external_identity_external_identity_ref_issuer_subject",
        ),
        Index("ix_external_identity_account_ref", "account_ref"),
        Index("ix_external_identity_email_identity_ref", "email_identity_ref"),
    )

    external_identity_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    email_identity_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    provider_code: Mapped[str] = mapped_column(Text, nullable=False)
    issuer: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    provider_email_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider_email_private: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    status_code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_authenticated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_reason_code: Mapped[str | None] = mapped_column(Text, nullable=True)


class ExternalAuthTransactionRow(Base):
    """Short-lived server-authoritative Google/Apple transaction state."""

    __tablename__ = "external_auth_transaction"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(external_auth_transaction_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("provider_code IN ('google','apple')", name="provider_code"),
        CheckConstraint(
            "(provider_code='google' AND expected_issuer='https://accounts.google.com') OR "
            "(provider_code='apple' AND expected_issuer='https://appleid.apple.com')",
            name="provider_issuer",
        ),
        CheckConstraint(
            "purpose_code IN ('sign_in','link','reauthenticate')",
            name="purpose_code",
        ),
        CheckConstraint("return_target_code IN ('access','security')", name="return_target_code"),
        CheckConstraint("octet_length(state_verifier)=32", name="state_verifier_length"),
        CheckConstraint("octet_length(nonce_verifier)=32", name="nonce_verifier_length"),
        CheckConstraint(
            "(purpose_code='sign_in' AND auth_session_ref IS NULL "
            "AND auth_session_secret_verifier IS NULL) OR "
            "(purpose_code IN ('link','reauthenticate') "
            "AND auth_session_ref IS NOT NULL "
            "AND auth_session_secret_verifier IS NOT NULL "
            "AND octet_length(auth_session_secret_verifier)=32)",
            name="session_binding",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '15 minutes'",
            name="chronology",
        ),
        CheckConstraint(
            "claimed_at IS NULL OR (isfinite(claimed_at) "
            "AND claimed_at>=created_at AND claimed_at<=expires_at)",
            name="claimed_at",
        ),
        ForeignKeyConstraint(
            ["auth_session_ref"],
            ["dante.auth_session.auth_session_ref"],
            name="fk_external_auth_transaction_auth_session_ref_auth_session",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint("state_verifier", name="uq_external_auth_transaction_state_verifier"),
        UniqueConstraint("nonce_verifier", name="uq_external_auth_transaction_nonce_verifier"),
        Index("ix_external_auth_transaction_expires_at", "expires_at"),
        Index("ix_external_auth_transaction_auth_session_ref", "auth_session_ref"),
    )

    external_auth_transaction_ref: Mapped[UUID] = mapped_column(primary_key=True)
    provider_code: Mapped[str] = mapped_column(Text, nullable=False)
    expected_issuer: Mapped[str] = mapped_column(Text, nullable=False)
    purpose_code: Mapped[str] = mapped_column(Text, nullable=False)
    state_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    nonce_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    auth_session_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    auth_session_secret_verifier: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    return_target_code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AppleAuthGrantRow(Base):
    """Encrypted Apple refresh-grant lifecycle."""

    __tablename__ = "apple_auth_grant"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(apple_auth_grant_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("issuer='https://appleid.apple.com'", name="issuer"),
        CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="subject",
        ),
        CheckConstraint(
            "client_id=btrim(client_id) AND client_id<>'' "
            "AND char_length(client_id)<=255",
            name="client_id",
        ),
        CheckConstraint(
            "status_code IN ('pending','active','revocation_pending','revoked')",
            name="status_code",
        ),
        CheckConstraint(
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
            name="chronology",
        ),
        CheckConstraint(
            "refresh_token_ciphertext IS NULL OR "
            "(octet_length(refresh_token_ciphertext)>16 "
            "AND octet_length(refresh_token_ciphertext)<=16384)",
            name="ciphertext",
        ),
        CheckConstraint(
            "refresh_token_nonce IS NULL OR octet_length(refresh_token_nonce)=12",
            name="nonce",
        ),
        CheckConstraint(
            "encryption_key_id IS NULL OR "
            "(encryption_key_id=btrim(encryption_key_id) "
            "AND encryption_key_id<>'' AND char_length(encryption_key_id)<=128)",
            name="encryption_key_id",
        ),
        CheckConstraint(
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
            name="state",
        ),
        ForeignKeyConstraint(
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
        UniqueConstraint("issuer", "subject", name="uq_apple_auth_grant_issuer_subject"),
        UniqueConstraint(
            "external_identity_ref",
            name="uq_apple_auth_grant_external_identity_ref",
        ),
        UniqueConstraint(
            "apple_auth_grant_ref",
            "issuer",
            "subject",
            name="uq_apple_auth_grant_ref_issuer_subject",
        ),
        Index("ix_apple_auth_grant_status_updated_at", "status_code", "updated_at"),
        Index("ix_apple_auth_grant_pending_expires_at", "pending_expires_at"),
    )

    apple_auth_grant_ref: Mapped[UUID] = mapped_column(primary_key=True)
    external_identity_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    issuer: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    client_id: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token_ciphertext: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    refresh_token_nonce: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    encryption_key_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    status_code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    pending_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_requested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ExternalLinkChallengeRow(Base):
    """Short-lived provider-first explicit-link challenge."""

    __tablename__ = "external_link_challenge"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(external_link_challenge_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("provider_code IN ('google','apple')", name="provider_code"),
        CheckConstraint(
            "(provider_code='google' AND issuer='https://accounts.google.com') OR "
            "(provider_code='apple' AND issuer='https://appleid.apple.com')",
            name="provider_issuer",
        ),
        CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="subject",
        ),
        CheckConstraint(
            "(provider_email_address IS NULL AND provider_email_private IS NULL) OR "
            "(provider_email_address IS NOT NULL "
            "AND provider_email_address=btrim(provider_email_address) "
            "AND provider_email_address<>'' "
            "AND char_length(provider_email_address)<=320 "
            "AND provider_email_private IS NOT NULL)",
            name="provider_email",
        ),
        CheckConstraint(
            "(provider_code='google' AND apple_auth_grant_ref IS NULL) OR "
            "(provider_code='apple' AND apple_auth_grant_ref IS NOT NULL)",
            name="provider_grant",
        ),
        CheckConstraint(
            "octet_length(continuation_verifier)=32",
            name="continuation_verifier_length",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '15 minutes'",
            name="chronology",
        ),
        ForeignKeyConstraint(
            ["target_account_ref"],
            ["dante.account.account_ref"],
            name="fk_external_link_challenge_target_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["target_email_identity_ref", "target_account_ref"],
            ["dante.email_identity.email_identity_ref", "dante.email_identity.account_ref"],
            name="fk_external_link_challenge_target_email_account_email_identity",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
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
        UniqueConstraint(
            "issuer",
            "subject",
            name="uq_external_link_challenge_issuer_subject",
        ),
        UniqueConstraint(
            "continuation_verifier",
            name="uq_external_link_challenge_continuation_verifier",
        ),
        Index("ix_external_link_challenge_target_account_ref", "target_account_ref"),
        Index(
            "ix_external_link_challenge_target_email_identity_ref",
            "target_email_identity_ref",
        ),
        Index("ix_external_link_challenge_apple_auth_grant_ref", "apple_auth_grant_ref"),
        Index("ix_external_link_challenge_expires_at", "expires_at"),
    )

    external_link_challenge_ref: Mapped[UUID] = mapped_column(primary_key=True)
    target_account_ref: Mapped[UUID] = mapped_column(nullable=False)
    target_email_identity_ref: Mapped[UUID] = mapped_column(nullable=False)
    provider_code: Mapped[str] = mapped_column(Text, nullable=False)
    issuer: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    provider_email_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider_email_private: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    apple_auth_grant_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    continuation_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ExternalSignupChallengeRow(Base):
    """Pending provider enrollment requiring DANTE mailbox proof."""

    __tablename__ = "external_signup_challenge"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(external_signup_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("provider_code IN ('google','apple')", name="provider_code"),
        CheckConstraint(
            "(provider_code='google' AND issuer='https://accounts.google.com') OR "
            "(provider_code='apple' AND issuer='https://appleid.apple.com')",
            name="provider_issuer",
        ),
        CheckConstraint(
            "subject=btrim(subject) AND subject<>'' AND char_length(subject)<=255",
            name="subject",
        ),
        CheckConstraint(
            "(provider_email_address IS NULL AND provider_email_private IS NULL) OR "
            "(provider_email_address IS NOT NULL "
            "AND provider_email_address=btrim(provider_email_address) "
            "AND provider_email_address<>'' "
            "AND char_length(provider_email_address)<=320 "
            "AND provider_email_private IS NOT NULL)",
            name="provider_email",
        ),
        CheckConstraint(
            "(provider_code='google' AND apple_auth_grant_ref IS NULL) OR "
            "(provider_code='apple' AND apple_auth_grant_ref IS NOT NULL)",
            name="provider_grant",
        ),
        CheckConstraint(
            "octet_length(continuation_verifier)=32",
            name="continuation_verifier_length",
        ),
        CheckConstraint(
            "(email_address IS NULL AND email_comparison_key IS NULL) OR "
            "(email_address IS NOT NULL AND email_comparison_key IS NOT NULL)",
            name="email_pair",
        ),
        CheckConstraint(
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
            name="email_verification",
        ),
        CheckConstraint(
            "failed_verification_attempts BETWEEN 0 AND 5",
            name="failed_attempts",
        ),
        CheckConstraint(
            "bootstrap_display_name IS NULL OR "
            "(bootstrap_display_name=btrim(bootstrap_display_name) "
            "AND bootstrap_display_name<>'' "
            "AND char_length(bootstrap_display_name)<=256)",
            name="bootstrap_display_name",
        ),
        CheckConstraint(
            "bootstrap_given_name IS NULL OR "
            "(bootstrap_given_name=btrim(bootstrap_given_name) "
            "AND bootstrap_given_name<>'' "
            "AND char_length(bootstrap_given_name)<=128)",
            name="bootstrap_given_name",
        ),
        CheckConstraint(
            "bootstrap_family_name IS NULL OR "
            "(bootstrap_family_name=btrim(bootstrap_family_name) "
            "AND bootstrap_family_name<>'' "
            "AND char_length(bootstrap_family_name)<=128)",
            name="bootstrap_family_name",
        ),
        CheckConstraint(
            "bootstrap_picture_url IS NULL OR "
            "(bootstrap_picture_url=btrim(bootstrap_picture_url) "
            "AND bootstrap_picture_url<>'' "
            "AND char_length(bootstrap_picture_url)<=2048)",
            name="bootstrap_picture_url",
        ),
        CheckConstraint(
            "bootstrap_locale IS NULL OR "
            "(bootstrap_locale=btrim(bootstrap_locale) "
            "AND bootstrap_locale<>'' "
            "AND char_length(bootstrap_locale)<=64)",
            name="bootstrap_locale",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) "
            "AND isfinite(expires_at) AND updated_at>=created_at "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '30 minutes'",
            name="chronology",
        ),
        ForeignKeyConstraint(
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
        UniqueConstraint(
            "issuer",
            "subject",
            name="uq_external_signup_challenge_issuer_subject",
        ),
        UniqueConstraint(
            "continuation_verifier",
            name="uq_external_signup_challenge_continuation_verifier",
        ),
        Index("ix_external_signup_challenge_email_comparison_key", "email_comparison_key"),
        Index("ix_external_signup_challenge_apple_auth_grant_ref", "apple_auth_grant_ref"),
        Index("ix_external_signup_challenge_expires_at", "expires_at"),
    )

    external_signup_ref: Mapped[UUID] = mapped_column(primary_key=True)
    provider_code: Mapped[str] = mapped_column(Text, nullable=False)
    issuer: Mapped[str] = mapped_column(Text, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    provider_email_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider_email_private: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    apple_auth_grant_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    continuation_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    email_comparison_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    otp_verifier: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    otp_key_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    verification_issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_verification_attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    bootstrap_display_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    bootstrap_given_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    bootstrap_family_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    bootstrap_picture_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    bootstrap_locale: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AccountProfileBootstrapRow(Base):
    """Bounded non-canonical provider profile bootstrap staging."""

    __tablename__ = "account_profile_bootstrap"
    __table_args__ = (
        CheckConstraint("source_provider_code IN ('google','apple')", name="source_provider_code"),
        CheckConstraint(
            "(source_provider_code='google' "
            "AND source_issuer='https://accounts.google.com') OR "
            "(source_provider_code='apple' "
            "AND source_issuer='https://appleid.apple.com')",
            name="source_provider_issuer",
        ),
        CheckConstraint(
            "display_name IS NOT NULL OR given_name IS NOT NULL "
            "OR family_name IS NOT NULL OR picture_url IS NOT NULL "
            "OR locale IS NOT NULL",
            name="nonempty",
        ),
        CheckConstraint(
            "display_name IS NULL OR (display_name=btrim(display_name) "
            "AND display_name<>'' AND char_length(display_name)<=256)",
            name="display_name",
        ),
        CheckConstraint(
            "given_name IS NULL OR (given_name=btrim(given_name) "
            "AND given_name<>'' AND char_length(given_name)<=128)",
            name="given_name",
        ),
        CheckConstraint(
            "family_name IS NULL OR (family_name=btrim(family_name) "
            "AND family_name<>'' AND char_length(family_name)<=128)",
            name="family_name",
        ),
        CheckConstraint(
            "picture_url IS NULL OR (picture_url=btrim(picture_url) "
            "AND picture_url<>'' AND char_length(picture_url)<=2048)",
            name="picture_url",
        ),
        CheckConstraint(
            "locale IS NULL OR (locale=btrim(locale) "
            "AND locale<>'' AND char_length(locale)<=64)",
            name="locale",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '30 days'",
            name="chronology",
        ),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_account_profile_bootstrap_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        Index("ix_account_profile_bootstrap_expires_at", "expires_at"),
    )

    account_ref: Mapped[UUID] = mapped_column(primary_key=True)
    source_provider_code: Mapped[str] = mapped_column(Text, nullable=False)
    source_issuer: Mapped[str] = mapped_column(Text, nullable=False)
    display_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    given_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    family_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    picture_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    locale: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class WebAuthnAccountRow(Base):
    """Stable opaque WebAuthn user handle for one Account."""

    __tablename__ = "webauthn_account"
    __table_args__ = (
        CheckConstraint("octet_length(user_handle)=32", name="user_handle_length"),
        CheckConstraint("isfinite(created_at)", name="created_at"),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.account.account_ref"],
            name="fk_webauthn_account_account_ref_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint("user_handle", name="uq_webauthn_account_user_handle"),
        UniqueConstraint(
            "account_ref",
            "user_handle",
            name="uq_webauthn_account_account_ref_user_handle",
        ),
    )

    account_ref: Mapped[UUID] = mapped_column(primary_key=True)
    user_handle: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PasskeyCredentialRow(Base):
    """Durable public WebAuthn credential owned by one Account."""

    __tablename__ = "passkey_credential"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(passkey_credential_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "octet_length(credential_id) BETWEEN 1 AND 1023",
            name="credential_id_length",
        ),
        CheckConstraint(
            "octet_length(credential_public_key) BETWEEN 1 AND 8192",
            name="public_key_length",
        ),
        CheckConstraint("sign_count BETWEEN 0 AND 4294967295", name="sign_count"),
        CheckConstraint(
            "cardinality(transports)<=8 AND array_position(transports,NULL) IS NULL",
            name="transports",
        ),
        CheckConstraint("NOT backup_state OR backup_eligible", name="backup_state"),
        CheckConstraint(
            "label=btrim(label) AND label<>'' AND char_length(label)<=100",
            name="label",
        ),
        CheckConstraint("status_code IN ('active','revoked')", name="status_code"),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) "
            "AND updated_at>=created_at "
            "AND (last_used_at IS NULL OR "
            "(isfinite(last_used_at) AND last_used_at>=created_at "
            "AND last_used_at<=updated_at))",
            name="chronology",
        ),
        CheckConstraint(
            "(status_code='active' AND revoked_at IS NULL "
            "AND revocation_reason_code IS NULL) OR "
            "(status_code='revoked' AND revoked_at IS NOT NULL "
            "AND isfinite(revoked_at) AND revoked_at>=created_at "
            "AND revoked_at<=updated_at "
            "AND revocation_reason_code='user_removed')",
            name="revocation",
        ),
        ForeignKeyConstraint(
            ["account_ref"],
            ["dante.webauthn_account.account_ref"],
            name="fk_passkey_credential_account_ref_webauthn_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "credential_id",
            name="uq_passkey_credential_credential_id",
        ),
        Index("ix_passkey_credential_account_status", "account_ref", "status_code"),
    )

    passkey_credential_ref: Mapped[UUID] = mapped_column(primary_key=True)
    account_ref: Mapped[UUID] = mapped_column(nullable=False)
    credential_id: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    credential_public_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    cose_algorithm: Mapped[int] = mapped_column(Integer, nullable=False)
    sign_count: Mapped[int] = mapped_column(BigInteger, nullable=False)
    backup_eligible: Mapped[bool] = mapped_column(Boolean, nullable=False)
    backup_state: Mapped[bool] = mapped_column(Boolean, nullable=False)
    transports: Mapped[list[str]] = mapped_column(postgresql.ARRAY(Text()), nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    status_code: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revocation_reason_code: Mapped[str | None] = mapped_column(Text, nullable=True)


class WebAuthnChallengeRow(Base):
    """Short-lived WebAuthn registration/authentication/reauthentication state."""

    __tablename__ = "webauthn_challenge"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(webauthn_challenge_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "ceremony_code IN ('registration','authentication','reauthentication')",
            name="ceremony_code",
        ),
        CheckConstraint(
            "octet_length(challenge_verifier)=32",
            name="challenge_verifier_length",
        ),
        CheckConstraint(
            "rp_id=btrim(rp_id) AND rp_id<>'' AND char_length(rp_id)<=253",
            name="rp_id",
        ),
        CheckConstraint(
            "expected_origin=btrim(expected_origin) AND expected_origin<>'' "
            "AND char_length(expected_origin)<=2048",
            name="expected_origin",
        ),
        CheckConstraint(
            "(ceremony_code='authentication' AND account_ref IS NULL "
            "AND auth_session_ref IS NULL "
            "AND auth_session_secret_verifier IS NULL "
            "AND user_handle IS NULL) OR "
            "(ceremony_code IN ('registration','reauthentication') "
            "AND account_ref IS NOT NULL AND auth_session_ref IS NOT NULL "
            "AND auth_session_secret_verifier IS NOT NULL "
            "AND octet_length(auth_session_secret_verifier)=32 "
            "AND user_handle IS NOT NULL AND octet_length(user_handle)=32)",
            name="session_binding",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(expires_at) "
            "AND expires_at>created_at "
            "AND expires_at<=created_at+interval '5 minutes'",
            name="chronology",
        ),
        CheckConstraint(
            "claimed_at IS NULL OR (isfinite(claimed_at) "
            "AND claimed_at>=created_at AND claimed_at<=expires_at)",
            name="claimed_at",
        ),
        ForeignKeyConstraint(
            ["auth_session_ref", "account_ref"],
            ["dante.auth_session.auth_session_ref", "dante.auth_session.account_ref"],
            name="fk_webauthn_challenge_session_account",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        ForeignKeyConstraint(
            ["account_ref", "user_handle"],
            ["dante.webauthn_account.account_ref", "dante.webauthn_account.user_handle"],
            name="fk_webauthn_challenge_account_user_handle",
            match="SIMPLE",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "challenge_verifier",
            name="uq_webauthn_challenge_challenge_verifier",
        ),
        Index("ix_webauthn_challenge_expires_at", "expires_at"),
        Index("ix_webauthn_challenge_account_ref", "account_ref"),
        Index("ix_webauthn_challenge_auth_session_ref", "auth_session_ref"),
    )

    webauthn_challenge_ref: Mapped[UUID] = mapped_column(primary_key=True)
    ceremony_code: Mapped[str] = mapped_column(Text, nullable=False)
    challenge_verifier: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    account_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    auth_session_ref: Mapped[UUID | None] = mapped_column(nullable=True)
    auth_session_secret_verifier: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    user_handle: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    rp_id: Mapped[str] = mapped_column(Text, nullable=False)
    expected_origin: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
