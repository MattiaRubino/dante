"""B14-U2 restore canonical descriptor read ACL for runtime.

Revision ID: 20261001_95
Revises: 20260930_94

U2 deliberately moved Activity/Event metadata writes behind bounded SECURITY
DEFINER authoring functions.  Revision _94 correctly removed direct runtime
write authority, but its blanket table revoke also removed the pre-existing
runtime SELECT required by the canonical Activity/Event read applications.

This forward-only correction restores read authority only.  Runtime still has
no direct INSERT/UPDATE/DELETE authority over either descriptor table.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261001_95"
down_revision: str | None = "20260930_94"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Restore the historical bounded runtime read contract."""
    op.execute(
        sa.text(
            "GRANT SELECT ON TABLE "
            "dante.activity_intention, dante.event_expectation "
            "TO dante_runtime"
        )
    )


def downgrade() -> None:
    """Never silently reintroduce the U2 descriptor-read regression."""
    raise RuntimeError(
        "B14-U2 descriptor runtime read ACL requires a reviewed forward migration"
    )
