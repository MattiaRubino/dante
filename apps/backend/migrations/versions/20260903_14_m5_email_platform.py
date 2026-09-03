"""Materialize the bounded M5 durable email delivery platform.

Revision ID: 20260903_14
Revises: 20260831_13
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260903_14"
down_revision: str | None = "20260831_13"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Create the minimum durable Auth/security email lifecycle and runtime ACL."""
    op.create_table(
        "email_delivery_intent",
        sa.Column("email_intent_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("purpose_code", sa.Text(), nullable=False),
        sa.Column("stream_code", sa.Text(), nullable=False),
        sa.Column("recipient_address", sa.Text(), nullable=False),
        sa.Column("recipient_comparison_key", sa.Text(), nullable=False),
        sa.Column("template_code", sa.Text(), nullable=False),
        sa.Column("template_revision", sa.Text(), nullable=False),
        sa.Column("locale_code", sa.Text(), nullable=False),
        sa.Column("operation_scope", sa.Text(), nullable=False),
        sa.Column("idempotency_key", sa.Text(), nullable=False),
        sa.Column("supersession_key", sa.Text(), nullable=True),
        sa.Column("payload_fingerprint", sa.LargeBinary(), nullable=False),
        sa.Column("sensitive_key_id", sa.Text(), nullable=True),
        sa.Column("sensitive_nonce", sa.LargeBinary(), nullable=True),
        sa.Column("sensitive_ciphertext", sa.LargeBinary(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("eligible_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dispatch_state_code", sa.Text(), nullable=False),
        sa.Column("claim_token", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("claimed_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempt_count", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("attempt_limit", sa.Integer(), nullable=False),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error_code", sa.Text(), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("terminal_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sensitive_wiped_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("email_intent_ref", name=op.f("pk_email_delivery_intent")),
        sa.UniqueConstraint(
            "operation_scope",
            "idempotency_key",
            name="uq_email_delivery_intent_operation_idempotency",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(email_intent_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_email_delivery_intent_uuidv7"),
        ),
        sa.CheckConstraint(
            "purpose_code IN "
            "('signup_verification','provider_enrollment_verification',"
            "'password_recovery','password_reset_notification')",
            name=op.f("ck_email_delivery_intent_purpose_code"),
        ),
        sa.CheckConstraint(
            "stream_code = 'auth_security'",
            name=op.f("ck_email_delivery_intent_stream_code"),
        ),
        sa.CheckConstraint(
            "recipient_address = btrim(recipient_address) AND recipient_address <> ''",
            name=op.f("ck_email_delivery_intent_recipient_address"),
        ),
        sa.CheckConstraint(
            "recipient_comparison_key = btrim(recipient_comparison_key) "
            "AND recipient_comparison_key <> ''",
            name=op.f("ck_email_delivery_intent_recipient_comparison_key"),
        ),
        sa.CheckConstraint(
            "template_code = btrim(template_code) AND template_code <> '' "
            "AND template_revision = btrim(template_revision) AND template_revision <> ''",
            name=op.f("ck_email_delivery_intent_template_identity"),
        ),
        sa.CheckConstraint(
            "locale_code = btrim(locale_code) AND locale_code <> ''",
            name=op.f("ck_email_delivery_intent_locale_code"),
        ),
        sa.CheckConstraint(
            "operation_scope = btrim(operation_scope) AND operation_scope <> '' "
            "AND idempotency_key = btrim(idempotency_key) AND idempotency_key <> ''",
            name=op.f("ck_email_delivery_intent_idempotency_identity"),
        ),
        sa.CheckConstraint(
            "octet_length(payload_fingerprint) = 32",
            name=op.f("ck_email_delivery_intent_payload_fingerprint_length"),
        ),
        sa.CheckConstraint(
            "(sensitive_key_id IS NULL AND sensitive_nonce IS NULL "
            "AND sensitive_ciphertext IS NULL) OR "
            "(sensitive_key_id IS NOT NULL AND sensitive_key_id = btrim(sensitive_key_id) "
            "AND sensitive_key_id <> '' AND octet_length(sensitive_nonce) = 12 "
            "AND octet_length(sensitive_ciphertext) >= 16)",
            name=op.f("ck_email_delivery_intent_sensitive_bundle"),
        ),
        sa.CheckConstraint(
            "dispatch_state_code IN "
            "('pending','claimed','provider_accepted','retryable_failure','ambiguous',"
            "'definitive_failure','expired','cancelled','recovery_quarantined')",
            name=op.f("ck_email_delivery_intent_dispatch_state_code"),
        ),
        sa.CheckConstraint(
            "(dispatch_state_code='claimed' AND claim_token IS NOT NULL "
            "AND claimed_until IS NOT NULL AND isfinite(claimed_until)) OR "
            "(dispatch_state_code<>'claimed' AND claim_token IS NULL AND claimed_until IS NULL)",
            name=op.f("ck_email_delivery_intent_claim_state"),
        ),
        sa.CheckConstraint(
            "attempt_limit > 0 AND attempt_count >= 0 AND attempt_count <= attempt_limit",
            name=op.f("ck_email_delivery_intent_attempt_budget"),
        ),
        sa.CheckConstraint(
            "isfinite(created_at) AND isfinite(updated_at) AND isfinite(eligible_at) "
            "AND isfinite(expires_at) AND updated_at >= created_at "
            "AND eligible_at >= created_at AND expires_at > created_at",
            name=op.f("ck_email_delivery_intent_chronology"),
        ),
        sa.CheckConstraint(
            "next_attempt_at IS NULL OR isfinite(next_attempt_at)",
            name=op.f("ck_email_delivery_intent_next_attempt_at"),
        ),
        sa.CheckConstraint(
            "accepted_at IS NULL OR (isfinite(accepted_at) AND accepted_at >= created_at)",
            name=op.f("ck_email_delivery_intent_accepted_at"),
        ),
        sa.CheckConstraint(
            "terminal_at IS NULL OR (isfinite(terminal_at) AND terminal_at >= created_at)",
            name=op.f("ck_email_delivery_intent_terminal_at"),
        ),
        sa.CheckConstraint(
            "sensitive_wiped_at IS NULL OR "
            "(isfinite(sensitive_wiped_at) AND sensitive_wiped_at >= created_at)",
            name=op.f("ck_email_delivery_intent_sensitive_wiped_at"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_email_delivery_intent_claimable",
        "email_delivery_intent",
        ["dispatch_state_code", "next_attempt_at", "eligible_at", "created_at"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_email_delivery_intent_recipient_comparison_key",
        "email_delivery_intent",
        ["recipient_comparison_key"],
        schema=_SCHEMA,
    )

    op.create_table(
        "email_delivery_attempt",
        sa.Column("email_attempt_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email_intent_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("provider_code", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("result_code", sa.Text(), nullable=False),
        sa.Column("provider_message_id", sa.Text(), nullable=True),
        sa.Column("error_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("email_attempt_ref", name=op.f("pk_email_delivery_attempt")),
        sa.ForeignKeyConstraint(
            ["email_intent_ref"],
            [f"{_SCHEMA}.email_delivery_intent.email_intent_ref"],
            name="fk_email_delivery_attempt_intent",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "email_intent_ref",
            "attempt_number",
            name="uq_email_delivery_attempt_intent_number",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(email_attempt_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_email_delivery_attempt_uuidv7"),
        ),
        sa.CheckConstraint(
            "attempt_number > 0",
            name=op.f("ck_email_delivery_attempt_attempt_number"),
        ),
        sa.CheckConstraint(
            "provider_code IN ('smtp','ses')",
            name=op.f("ck_email_delivery_attempt_provider_code"),
        ),
        sa.CheckConstraint(
            "result_code IN "
            "('in_progress','provider_accepted','retryable_failure','ambiguous',"
            "'definitive_failure')",
            name=op.f("ck_email_delivery_attempt_result_code"),
        ),
        sa.CheckConstraint(
            "isfinite(started_at) AND "
            "(finished_at IS NULL OR (isfinite(finished_at) AND finished_at >= started_at))",
            name=op.f("ck_email_delivery_attempt_chronology"),
        ),
        sa.CheckConstraint(
            "(result_code='in_progress' AND finished_at IS NULL) OR "
            "(result_code<>'in_progress' AND finished_at IS NOT NULL)",
            name=op.f("ck_email_delivery_attempt_result_completion"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_email_delivery_attempt_intent_ref",
        "email_delivery_attempt",
        ["email_intent_ref"],
        schema=_SCHEMA,
    )
    op.create_index(
        "uq_email_delivery_attempt_provider_message",
        "email_delivery_attempt",
        ["provider_code", "provider_message_id"],
        unique=True,
        schema=_SCHEMA,
        postgresql_where=sa.text("provider_message_id IS NOT NULL"),
    )

    op.create_table(
        "email_provider_event",
        sa.Column("email_provider_event_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider_code", sa.Text(), nullable=False),
        sa.Column("provider_event_id", sa.Text(), nullable=False),
        sa.Column("provider_message_id", sa.Text(), nullable=False),
        sa.Column("email_intent_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type_code", sa.Text(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload_digest", sa.LargeBinary(), nullable=False),
        sa.Column("safe_detail_code", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("email_provider_event_ref", name=op.f("pk_email_provider_event")),
        sa.ForeignKeyConstraint(
            ["email_intent_ref"],
            [f"{_SCHEMA}.email_delivery_intent.email_intent_ref"],
            name="fk_email_provider_event_intent",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "provider_code",
            "provider_event_id",
            name="uq_email_provider_event_provider_id",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(email_provider_event_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_email_provider_event_uuidv7"),
        ),
        sa.CheckConstraint(
            "provider_code = 'ses'",
            name=op.f("ck_email_provider_event_provider_code"),
        ),
        sa.CheckConstraint(
            "provider_event_id = btrim(provider_event_id) AND provider_event_id <> '' "
            "AND provider_message_id = btrim(provider_message_id) "
            "AND provider_message_id <> ''",
            name=op.f("ck_email_provider_event_provider_identity"),
        ),
        sa.CheckConstraint(
            "event_type_code IN "
            "('delivered','delivery_delayed','bounced','complained','rejected')",
            name=op.f("ck_email_provider_event_event_type_code"),
        ),
        sa.CheckConstraint(
            "isfinite(observed_at) AND isfinite(received_at)",
            name=op.f("ck_email_provider_event_timestamps"),
        ),
        sa.CheckConstraint(
            "octet_length(payload_digest) = 32",
            name=op.f("ck_email_provider_event_payload_digest_length"),
        ),
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_email_provider_event_provider_message",
        "email_provider_event",
        ["provider_code", "provider_message_id"],
        schema=_SCHEMA,
    )
    op.create_index(
        "ix_email_provider_event_intent_ref",
        "email_provider_event",
        ["email_intent_ref"],
        schema=_SCHEMA,
    )

    op.create_table(
        "email_recipient_suppression",
        sa.Column("email_recipient_suppression_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recipient_comparison_key", sa.Text(), nullable=False),
        sa.Column("reason_code", sa.Text(), nullable=False),
        sa.Column("source_provider_event_ref", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("suppressed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cleared_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint(
            "email_recipient_suppression_ref",
            name=op.f("pk_email_recipient_suppression"),
        ),
        sa.ForeignKeyConstraint(
            ["source_provider_event_ref"],
            [f"{_SCHEMA}.email_provider_event.email_provider_event_ref"],
            name="fk_email_recipient_suppression_source_event",
            onupdate="NO ACTION",
            ondelete="NO ACTION",
            deferrable=False,
        ),
        sa.UniqueConstraint(
            "recipient_comparison_key",
            name="uq_email_recipient_suppression_recipient",
        ),
        sa.CheckConstraint(
            "uuid_extract_version(email_recipient_suppression_ref) IS NOT DISTINCT FROM 7",
            name=op.f("ck_email_recipient_suppression_uuidv7"),
        ),
        sa.CheckConstraint(
            "recipient_comparison_key = btrim(recipient_comparison_key) "
            "AND recipient_comparison_key <> ''",
            name=op.f("ck_email_recipient_suppression_recipient_comparison_key"),
        ),
        sa.CheckConstraint(
            "reason_code IN ('hard_bounce','complaint')",
            name=op.f("ck_email_recipient_suppression_reason_code"),
        ),
        sa.CheckConstraint(
            "isfinite(suppressed_at) AND isfinite(updated_at) AND updated_at >= suppressed_at "
            "AND (cleared_at IS NULL OR (isfinite(cleared_at) AND cleared_at >= suppressed_at))",
            name=op.f("ck_email_recipient_suppression_chronology"),
        ),
        schema=_SCHEMA,
    )

    op.execute(
        sa.text(
            f"GRANT SELECT, INSERT, UPDATE ON TABLE "
            f"{_SCHEMA}.email_delivery_intent, "
            f"{_SCHEMA}.email_delivery_attempt, "
            f"{_SCHEMA}.email_recipient_suppression TO {_RUNTIME}"
        )
    )
    op.execute(
        sa.text(
            f"GRANT SELECT, INSERT ON TABLE {_SCHEMA}.email_provider_event TO {_RUNTIME}"
        )
    )


def downgrade() -> None:
    """Remove only the M5 email delivery platform materialized by this revision."""
    op.drop_table("email_recipient_suppression", schema=_SCHEMA)
    op.drop_table("email_provider_event", schema=_SCHEMA)
    op.drop_table("email_delivery_attempt", schema=_SCHEMA)
    op.drop_table("email_delivery_intent", schema=_SCHEMA)
