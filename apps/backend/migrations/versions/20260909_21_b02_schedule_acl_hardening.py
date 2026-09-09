"""Harden B02 Schedule establishment receipt ACL.

Revision ID: 20260909_21
Revises: 20260909_20
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260909_21"
down_revision: str | None = "20260909_20"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Keep the immutable operation receipt behind the bounded DB capability."""
    op.execute(
        sa.text(f"REVOKE SELECT ON TABLE dante.schedule_establish_operation FROM {_RUNTIME}")
    )


def downgrade() -> None:
    """Restore the superseded B02-A receipt-read posture."""
    op.execute(sa.text(f"GRANT SELECT ON TABLE dante.schedule_establish_operation TO {_RUNTIME}"))
