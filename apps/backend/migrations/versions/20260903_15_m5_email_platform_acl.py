"""Harden the M5 Email Platform runtime ACL to exact lifecycle columns.

Revision ID: 20260903_15
Revises: 20260903_14
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260903_15"
down_revision: str | None = "20260903_14"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Replace broad UPDATE grants with the exact Email Platform lifecycle surface."""
    for table_name in (
        "email_delivery_intent",
        "email_delivery_attempt",
        "email_recipient_suppression",
    ):
        op.execute(
            sa.text(f"REVOKE UPDATE ON TABLE {_SCHEMA}.{table_name} FROM {_RUNTIME}")
        )

    op.execute(
        sa.text(
            "GRANT UPDATE (dispatch_state_code, claim_token, claimed_until, attempt_count, "
            "next_attempt_at, last_error_code, accepted_at, terminal_at, updated_at, "
            "sensitive_key_id, sensitive_nonce, sensitive_ciphertext, sensitive_wiped_at) "
            "ON TABLE dante.email_delivery_intent TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT UPDATE (finished_at, result_code, provider_message_id, error_code) "
            "ON TABLE dante.email_delivery_attempt TO dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT UPDATE (reason_code, source_provider_event_ref, suppressed_at, "
            "updated_at, cleared_at) ON TABLE dante.email_recipient_suppression "
            "TO dante_runtime"
        )
    )


def downgrade() -> None:
    """Restore the broader revision-14 UPDATE grants exactly."""
    op.execute(
        sa.text(
            "REVOKE UPDATE (dispatch_state_code, claim_token, claimed_until, attempt_count, "
            "next_attempt_at, last_error_code, accepted_at, terminal_at, updated_at, "
            "sensitive_key_id, sensitive_nonce, sensitive_ciphertext, sensitive_wiped_at) "
            "ON TABLE dante.email_delivery_intent FROM dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "REVOKE UPDATE (finished_at, result_code, provider_message_id, error_code) "
            "ON TABLE dante.email_delivery_attempt FROM dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "REVOKE UPDATE (reason_code, source_provider_event_ref, suppressed_at, "
            "updated_at, cleared_at) ON TABLE dante.email_recipient_suppression "
            "FROM dante_runtime"
        )
    )
    op.execute(
        sa.text(
            "GRANT UPDATE ON TABLE dante.email_delivery_intent, "
            "dante.email_delivery_attempt, dante.email_recipient_suppression "
            "TO dante_runtime"
        )
    )
