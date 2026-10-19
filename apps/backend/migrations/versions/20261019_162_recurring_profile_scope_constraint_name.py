"""Align the recurring profile scope check with the canonical catalog name.

The previous migration recreated this check through Alembic's naming
convention with an already prefixed identifier, resulting in a double prefix.
Rename the existing constraint without rewriting any stored profile edits.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261019_162"
down_revision: str | None = "20261019_161"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE dante.occurrence_profile_edit "
        "RENAME CONSTRAINT ck_occurrence_profile_edit_ck_occurrence_profile_edit_scope "
        "TO ck_occurrence_profile_edit_scope"
    )


def downgrade() -> None:
    raise RuntimeError("20261019_162 is forward-only")
