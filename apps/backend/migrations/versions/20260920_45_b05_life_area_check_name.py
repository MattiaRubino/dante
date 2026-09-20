"""Reconcile the accepted Life Area receipt CHECK name with the Dictionary.

Revision ID: 20260920_45
Revises: 20260920_44

The previous migration created this CHECK without op.f; SQLAlchemy applied the
naming convention to its already prefixed name, which PostgreSQL then shortened
at the identifier limit. The constraint's predicate and validated data are sound.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260920_45"
down_revision: str | None = "20260920_44"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Rename the existing validated CHECK, preserving its predicate and rows."""
    op.execute(
        sa.text("""
        ALTER TABLE dante.life_area_mutation_operation
        RENAME CONSTRAINT ck_life_area_mutation_operation_ck_life_area_mutation_o_3645
        TO ck_life_area_mutation_operation_count
    """)
    )


def downgrade() -> None:
    """Never revert accepted database catalog reconciliation."""
    raise RuntimeError("B05-A catalog reconciliation requires a reviewed forward migration")
