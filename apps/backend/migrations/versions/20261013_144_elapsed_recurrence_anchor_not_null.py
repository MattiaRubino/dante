"""Enforce canonical non-null elapsed Recurrence anchors.

The accepted Dictionary declares both anchors mandatory. A prior migration
left their physical columns nullable, causing Alembic drift and allowing
unanchored materialized elapsed Recurrences. Validate data before applying
NOT NULL; never invent or backfill historical anchor instants.

Revision ID: 20261013_144
Revises: 20261012_143
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261013_144"
down_revision: str | None = "20261012_143"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABLES = (
    "routine_recurrence_elapsed_state",
    "event_recurrence_elapsed_state",
)


def upgrade() -> None:
    connection = op.get_bind()
    for table in _TABLES:
        # Both identifiers are fixed, audited DANTE migration literals.
        # Fail closed when historical data contradict the Dictionary.
        null_count = connection.exec_driver_sql(
            f"SELECT count(*) FROM dante.{table} WHERE anchor_at IS NULL"
        ).scalar_one()
        if null_count != 0:
            raise RuntimeError(
                f"Cannot enforce dante.{table}.anchor_at NOT NULL: "
                f"{null_count} existing unanchored rows require explicit review"
            )
        connection.exec_driver_sql(
            f"ALTER TABLE dante.{table} ALTER COLUMN anchor_at SET NOT NULL"
        )


def downgrade() -> None:
    raise RuntimeError(
        "20261013_144 is forward-only: "
        "Elapsed Recurrence anchors must remain non-null"
    )
