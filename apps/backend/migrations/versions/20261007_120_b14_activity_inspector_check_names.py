"""Reconcile Activity Inspector CHECK names with the Dictionary.

Revision ID: 20261007_120
Revises: 20261007_119
"""

from collections.abc import Sequence
from hashlib import md5

from alembic import op

revision: str = "20261007_120"
down_revision: str | None = "20261007_119"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # _119 passed already-prefixed names through the ck_<table> convention.
    # Reproduce SQLAlchemy's identifier shortening for the 63-byte name.
    for table, suffix in (
        ("activity_intention", "profile_revision"),
        ("activity_intention", "retired_pair"),
        ("activity_profile_revision", "positive"),
    ):
        accepted = f"ck_{table}_{suffix}"
        expanded = f"ck_{table}_{accepted}"
        old = (
            expanded
            if len(expanded) <= 63
            else f"{expanded[:55]}_{md5(expanded.encode(), usedforsecurity=False).hexdigest()[-4:]}"
        )
        op.execute(f"ALTER TABLE dante.{table} RENAME CONSTRAINT {old} TO {accepted}")


def downgrade() -> None:
    raise RuntimeError("20261007_120 is forward-only; CHECK names cannot be reverted")
