"""Align the existing Event legacy-proof CHECK name with the catalog.

Revision ID: 20261107_177
Revises: 20261107_176

Migration 174 supplied an already-prefixed name to Alembic, whose naming
convention added the table prefix again. Rename only the constraint; existing
seed rows and their repair provenance are untouched.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261107_177"
down_revision: str | None = "20261107_176"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE dante.event_recurring_seed "
        "RENAME CONSTRAINT ck_event_recurring_seed_ck_event_recurring_seed_legacy_proof "
        "TO ck_event_recurring_seed_legacy_proof"
    )


def downgrade() -> None:
    raise RuntimeError("20261107_177 is forward-only")
