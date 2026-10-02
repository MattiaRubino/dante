"""Reconcile Activity decomposition CHECK names after Alembic convention expansion."""

from collections.abc import Sequence
from hashlib import md5

from alembic import op

revision: str = "20261002_99"
down_revision: str | None = "20261002_98"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CHECKS = (
    ("activity_decomposition", "uuidv7"),
    ("activity_decomposition", "distinct"),
    ("activity_decomposition_state", "uuidv7"),
    ("activity_decomposition_state", "requirement"),
    ("activity_decomposition_state", "order"),
    ("activity_decomposition_state", "recorded_at"),
    ("activity_decomposition_current_history", "interval"),
    ("activity_decomposition_operation", "id"),
    ("activity_decomposition_operation", "fingerprint"),
)


def upgrade() -> None:
    # _98 supplied an already-prefixed name to a naming convention that adds
    # ck_<table> again. SQLAlchemy shortens names past PostgreSQL's 63-byte cap.
    for table, suffix in _CHECKS:
        accepted = f"ck_{table}_{suffix}"
        expanded = f"ck_{table}_{accepted}"
        old = (
            expanded
            if len(expanded) <= 63
            else f"{expanded[:55]}_{md5(expanded.encode(), usedforsecurity=False).hexdigest()[-4:]}"
        )
        op.execute(f"ALTER TABLE dante.{table} RENAME CONSTRAINT {old} TO {accepted}")


def downgrade() -> None:
    raise RuntimeError("B14-U6 catalog correction requires a reviewed forward migration")
