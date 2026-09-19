"""Activate least-privilege runtime reads for B04-C window rule payloads.

Revision ID: 20260919_36
Revises: 20260919_35
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260919_36"
down_revision: str | None = "20260919_35"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_RUNTIME = "dante_runtime"

_WINDOW_READ_TABLES = (
    "temporal_constraint_window_state",
    "temporal_constraint_window_absolute_state",
)

_PRIVATE_TABLES = (
    "temporal_constraint_current_history",
    "temporal_constraint_mutation_operation",
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    """Expose only the B04-C current-rule window tables required by runtime reads."""
    for table in _WINDOW_READ_TABLES:
        _sql(f"GRANT SELECT ON TABLE dante.{table} TO {_RUNTIME}")

    # Reassert that activation of the new read-model payload does not widen
    # access to currentness history or idempotency receipts.
    for table in _PRIVATE_TABLES:
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM {_RUNTIME}")


def downgrade() -> None:
    """Fail closed rather than silently break the accepted B04-C read surface."""
    raise RuntimeError(
        "B04-C runtime read activation downgrade is intentionally refused; use a "
        "separately reviewed forward migration"
    )
