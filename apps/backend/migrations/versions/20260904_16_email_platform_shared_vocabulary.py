"""Generalize Email Platform consumer vocabulary without weakening technical shape.

Revision ID: 20260904_16
Revises: 20260903_15
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260904_16"
down_revision: str | None = "20260903_15"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_TABLE = "email_delivery_intent"
_PURPOSE_CONSTRAINT = "ck_email_delivery_intent_purpose_code"
_STREAM_CONSTRAINT = "ck_email_delivery_intent_stream_code"


def upgrade() -> None:
    """Replace Auth-only vocabulary checks with governed shared-platform identifiers."""
    # These names were materialized as finalized convention names by revision 14.
    # op.f(...) prevents SQLAlchemy's naming convention from prefixing them again.
    op.drop_constraint(
        op.f(_PURPOSE_CONSTRAINT),
        _TABLE,
        schema=_SCHEMA,
        type_="check",
    )
    op.drop_constraint(
        op.f(_STREAM_CONSTRAINT),
        _TABLE,
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f(_PURPOSE_CONSTRAINT),
        _TABLE,
        "purpose_code = btrim(purpose_code) "
        "AND purpose_code ~ '^[a-z][a-z0-9_]{0,63}$'",
        schema=_SCHEMA,
    )
    op.create_check_constraint(
        op.f(_STREAM_CONSTRAINT),
        _TABLE,
        "stream_code = btrim(stream_code) "
        "AND stream_code ~ '^[a-z][a-z0-9_]{0,63}$'",
        schema=_SCHEMA,
    )


def downgrade() -> None:
    """Restore the historical first-consumer Auth-only vocabulary constraints."""
    op.drop_constraint(
        op.f(_STREAM_CONSTRAINT),
        _TABLE,
        schema=_SCHEMA,
        type_="check",
    )
    op.drop_constraint(
        op.f(_PURPOSE_CONSTRAINT),
        _TABLE,
        schema=_SCHEMA,
        type_="check",
    )
    op.create_check_constraint(
        op.f(_PURPOSE_CONSTRAINT),
        _TABLE,
        "purpose_code IN "
        "('signup_verification','provider_enrollment_verification',"
        "'password_recovery','password_reset_notification')",
        schema=_SCHEMA,
    )
    op.create_check_constraint(
        op.f(_STREAM_CONSTRAINT),
        _TABLE,
        "stream_code = 'auth_security'",
        schema=_SCHEMA,
    )
