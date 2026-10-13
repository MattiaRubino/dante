"""Restore relative Recurrence anchors and match the occurrence policy lookup indexes.

Revision ID: 20261013_145
Revises: 20261013_144

Advanced previous-completion and anchor-stream Recurrences have no fixed
instant: the B11-A check constraint requires their anchor_at to be NULL.
The preceding migration incorrectly imposed a table-wide NOT NULL. The
existing conditional CHECK remains authoritative for every anchor mode.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261013_145"
down_revision: str | None = "20261013_144"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    for prefix in ("routine", "event"):
        table = f"{prefix}_recurrence_elapsed_state"
        op.alter_column(table, "anchor_at", schema="dante", nullable=True)

        policy = f"{prefix}_occurrence_policy"
        owner_ref = f"{prefix}_ref"
        index = f"ix_{policy}_{prefix}"
        op.drop_index(index, table_name=policy, schema="dante")
        op.create_index(index, policy, [owner_ref], unique=False, schema="dante")


def downgrade() -> None:
    raise RuntimeError(
        "20261013_145 is forward-only: relative Recurrence anchors and policy indexes are canonical"
    )
