"""SQLAlchemy mappings for the bounded DANTE email delivery platform."""

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
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from dante.platform.database.metadata import Base


class EmailDeliveryIntentRow(Base):
    """Durable DANTE decision to attempt one outbound email."""

    __tablename__ = "email_delivery_intent"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(email_intent_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "purpose_code IN "
            "('signup_verification','provider_enrollment_verification',"
            "'password_recovery','password_reset_notification')",
            name="purpose_code",
        ),
        CheckConstraint("stream_code = 'auth_security'", name="stream_code"),
        CheckConstraint(
            "recipient_address = btrim(recipient_address) AND recipient_address <> ''",
            name="recipient_address",
        ),
        CheckConstraint(
            "recipient_comparison_key = btrim(recipient_comparison_key) "
            "AND recipient_comparison_key <> ''",
            name="recipient_comparison_key",
        ),
        CheckConstraint(
            "template_code = btrim(template_code) AND template_code <> '' "
            "AND template_revision = btrim(template_revision) AND template_revision <> ''",
            name="template_identity",
        ),
        CheckConstraint(
            "locale_code = btrim(locale_code) AND locale_code <> ''",
            name="locale_code",
        ),
        CheckConstraint(
            "operation_scope = btrim(operation_scope) AND operation_scope <> '' "
            "AND idempotency_key = btrim(idempotency_key) AND idempotency_key <> ''",
            name="idempotency_identity",
        ),
        CheckConstraint(
            "octet_length(payload_fingerprint) = 32", name="payload_fingerprint_length"
        ),
        CheckConstraint(
            "(sensitive_key_id IS NULL AND sensitive_nonce IS NULL "
            "AND sensitive_ciphertext IS NULL) OR "
            "(sensitive_key_id IS NOT NULL AND sensitive_key_id = btrim(sensitive_key_id) "
            "AND sensitive_key_id <> '' AND octet_length(sensitive_nonce) = 12 "
            "AND octet_length(sensitive_ciphertext) >= 16)",
            name="sensitive_bundle",
        ),
        CheckConstraint(
            "dispatch_state_code IN "
            "('pending','claimed','provider_accepted','retryable_failure','ambiguous',"
            "'definitive_failure','expired','cancelled','recovery_quarantined')",
            name="dispatch_state_code",
        ),
        CheckConstraint(
            "(dispatch_state_code='claimed' AND claim_token IS NOT NULL "
            "AND claimed_until IS NOT NULL AND isfinite(claimed_until)) OR "
            "(dispatch_state_code<>'claimed' AND claim_token IS NULL AND claimed_until IS NULL)",
            name="claim_state",
        ),
        CheckConstraint(
            "attempt_limit > 0 AND attempt_count >= 0 AND attempt_count <= attempt_limit",
            name="attempt_budget",
        ),
        CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) AND isfinite(eligible_at) "
            "AND isfinite(expires_at) AND updated_at >= created_at "
            "AND eligible_at >= created_at AND expires_at > created_at",
            name="chronology",
        ),
        CheckConstraint(
            "next_attempt_at IS NULL OR isfinite(next_attempt_at)",
            name="next_attempt_at",
        ),
        CheckConstraint(
            "accepted_at IS NULL OR (isfinite(accepted_at) AND accepted_at >= created_at)",
            name="accepted_at",
        ),
        CheckConstraint(
            "terminal_at IS NULL OR (isfinite(terminal_at) AND terminal_at >= created_at)",
            name="terminal_at",
        ),
        CheckConstraint(
            "sensitive_wiped_at IS NULL OR "
            "(isfinite(sensitive_wiped_at) AND sensitive_wiped_at >= created_at)",
            name="sensitive_wiped_at",
        ),
        UniqueConstraint(
            "operation_scope",
            "idempotency_key",
            name="uq_email_delivery_intent_operation_idempotency",
        ),
        Index(
            "ix_email_delivery_intent_claimable",
            "dispatch_state_code",
            "next_attempt_at",
            "eligible_at",
            "created_at",
        ),
        Index(
            "ix_email_delivery_intent_recipient_comparison_key",
            "recipient_comparison_key",
        ),
    )

    email_intent_ref: Mapped[UUID] = mapped_column(primary_key=True)
    purpose_code: Mapped[str] = mapped_column(Text, nullable=False)
    stream_code: Mapped[str] = mapped_column(Text, nullable=False)
    recipient_address: Mapped[str] = mapped_column(Text, nullable=False)
    recipient_comparison_key: Mapped[str] = mapped_column(Text, nullable=False)
    template_code: Mapped[str] = mapped_column(Text, nullable=False)
    template_revision: Mapped[str] = mapped_column(Text, nullable=False)
    locale_code: Mapped[str] = mapped_column(Text, nullable=False)
    operation_scope: Mapped[str] = mapped_column(Text, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(Text, nullable=False)
    supersession_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload_fingerprint: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    sensitive_key_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    sensitive_nonce: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    sensitive_ciphertext: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    eligible_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    dispatch_state_code: Mapped[str] = mapped_column(Text, nullable=False)
    claim_token: Mapped[UUID | None] = mapped_column(nullable=True)
    claimed_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    attempt_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    next_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    terminal_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sensitive_wiped_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class EmailDeliveryAttemptRow(Base):
    """One external-provider attempt for one durable email intent."""

    __tablename__ = "email_delivery_attempt"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(email_attempt_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("attempt_number > 0", name="attempt_number"),
        CheckConstraint("provider_code IN ('smtp','ses')", name="provider_code"),
        CheckConstraint(
            "result_code IN "
            "('in_progress','provider_accepted','retryable_failure','ambiguous',"
            "'definitive_failure')",
            name="result_code",
        ),
        CheckConstraint(
            "isfinite(started_at) AND "
            "(finished_at IS NULL OR (isfinite(finished_at) AND finished_at >= started_at))",
            name="chronology",
        ),
        CheckConstraint(
            "(result_code='in_progress' AND finished_at IS NULL) OR "
            "(result_code<>'in_progress' AND finished_at IS NOT NULL)",
            name="result_completion",
        ),
        ForeignKeyConstraint(
            ["email_intent_ref"],
            ["dante.email_delivery_intent.email_intent_ref"],
            name="fk_email_delivery_attempt_intent",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "email_intent_ref",
            "attempt_number",
            name="uq_email_delivery_attempt_intent_number",
        ),
        Index("ix_email_delivery_attempt_intent_ref", "email_intent_ref"),
        Index(
            "uq_email_delivery_attempt_provider_message",
            "provider_code",
            "provider_message_id",
            unique=True,
            postgresql_where=text("provider_message_id IS NOT NULL"),
        ),
    )

    email_attempt_ref: Mapped[UUID] = mapped_column(primary_key=True)
    email_intent_ref: Mapped[UUID] = mapped_column(nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    provider_code: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    result_code: Mapped[str] = mapped_column(Text, nullable=False)
    provider_message_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_code: Mapped[str | None] = mapped_column(Text, nullable=True)


class EmailProviderEventRow(Base):
    """Privacy-minimized normalized evidence received from an email provider."""

    __tablename__ = "email_provider_event"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(email_provider_event_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint("provider_code = 'ses'", name="provider_code"),
        CheckConstraint(
            "provider_event_id = btrim(provider_event_id) AND provider_event_id <> '' "
            "AND provider_message_id = btrim(provider_message_id) "
            "AND provider_message_id <> ''",
            name="provider_identity",
        ),
        CheckConstraint(
            "event_type_code IN ('delivered','delivery_delayed','bounced','complained','rejected')",
            name="event_type_code",
        ),
        CheckConstraint(
            "isfinite(observed_at) AND isfinite(received_at)",
            name="timestamps",
        ),
        CheckConstraint("octet_length(payload_digest) = 32", name="payload_digest_length"),
        ForeignKeyConstraint(
            ["email_intent_ref"],
            ["dante.email_delivery_intent.email_intent_ref"],
            name="fk_email_provider_event_intent",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "provider_code",
            "provider_event_id",
            name="uq_email_provider_event_provider_id",
        ),
        Index(
            "ix_email_provider_event_provider_message",
            "provider_code",
            "provider_message_id",
        ),
        Index("ix_email_provider_event_intent_ref", "email_intent_ref"),
    )

    email_provider_event_ref: Mapped[UUID] = mapped_column(primary_key=True)
    provider_code: Mapped[str] = mapped_column(Text, nullable=False)
    provider_event_id: Mapped[str] = mapped_column(Text, nullable=False)
    provider_message_id: Mapped[str] = mapped_column(Text, nullable=False)
    email_intent_ref: Mapped[UUID] = mapped_column(nullable=False)
    event_type_code: Mapped[str] = mapped_column(Text, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payload_digest: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    safe_detail_code: Mapped[str | None] = mapped_column(Text, nullable=True)


class EmailRecipientSuppressionRow(Base):
    """Current DANTE operational projection for provider-delivery suppression."""

    __tablename__ = "email_recipient_suppression"
    __table_args__ = (
        CheckConstraint(
            "uuid_extract_version(email_recipient_suppression_ref) IS NOT DISTINCT FROM 7",
            name="uuidv7",
        ),
        CheckConstraint(
            "recipient_comparison_key = btrim(recipient_comparison_key) "
            "AND recipient_comparison_key <> ''",
            name="recipient_comparison_key",
        ),
        CheckConstraint("reason_code IN ('hard_bounce','complaint')", name="reason_code"),
        CheckConstraint(
            "isfinite(suppressed_at) AND isfinite(updated_at) AND updated_at >= suppressed_at "
            "AND (cleared_at IS NULL OR (isfinite(cleared_at) AND cleared_at >= suppressed_at))",
            name="chronology",
        ),
        ForeignKeyConstraint(
            ["source_provider_event_ref"],
            ["dante.email_provider_event.email_provider_event_ref"],
            name="fk_email_recipient_suppression_source_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        UniqueConstraint(
            "recipient_comparison_key",
            name="uq_email_recipient_suppression_recipient",
        ),
    )

    email_recipient_suppression_ref: Mapped[UUID] = mapped_column(primary_key=True)
    recipient_comparison_key: Mapped[str] = mapped_column(Text, nullable=False)
    reason_code: Mapped[str] = mapped_column(Text, nullable=False)
    source_provider_event_ref: Mapped[UUID] = mapped_column(nullable=False)
    suppressed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cleared_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
