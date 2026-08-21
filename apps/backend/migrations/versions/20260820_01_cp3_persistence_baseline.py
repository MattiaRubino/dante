"""Activate Alembic as DANTE schema history authority.

Revision ID: 20260820_01
Revises:
Create Date: 2026-08-20

"""

from collections.abc import Sequence

revision: str = "20260820_01"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Record the technical persistence baseline without business schema."""


def downgrade() -> None:
    """Return the technical baseline to Alembic base."""
