"""Merge Recovery and Access/Auth migration branches.

Revision ID: 20260904_17
Revises: 20260830_09, 20260904_16
"""

from collections.abc import Sequence

revision: str = "20260904_17"
down_revision: tuple[str, str] = ("20260830_09", "20260904_16")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Join the accepted Recovery and Access/Auth histories without schema mutation."""


def downgrade() -> None:
    """Split the merge point back to its two accepted parent histories."""
