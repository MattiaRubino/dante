"""Activate least-privilege runtime reads for B04-E duration rule payloads.

Revision ID: 20260919_41
Revises: 20260919_40
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260919_41"
down_revision: str | None = "20260919_40"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_RUNTIME = "dante_runtime"
_DURATION_READ_TABLE = "temporal_constraint_duration_state"
_PRIVATE_TABLES = (
    "temporal_constraint_current_history",
    "temporal_constraint_mutation_operation",
)


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    """Expose only the B04-E current duration payload required by runtime reads."""
    _sql(f"GRANT SELECT ON TABLE dante.{_DURATION_READ_TABLE} TO {_RUNTIME}")

    for table in _PRIVATE_TABLES:
        _sql(f"REVOKE ALL PRIVILEGES ON TABLE dante.{table} FROM {_RUNTIME}")


def downgrade() -> None:
    """Fail closed rather than silently break the accepted B04-E read surface."""
    raise RuntimeError(
        "B04-E duration runtime read activation downgrade is intentionally refused; use a "
        "separately reviewed forward migration"
    )
