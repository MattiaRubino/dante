"""Grant the bounded runtime ACL required for M5 authenticator lifecycle.

Revision ID: 20260831_13
Revises: 20260830_12
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260831_13"
down_revision: str | None = "20260830_12"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_SCHEMA = "dante"
_RUNTIME = "dante_runtime"


def upgrade() -> None:
    """Allow only governed removal of the optional current PasswordCredential."""
    op.execute(
        sa.text(
            f"GRANT DELETE ON TABLE {_SCHEMA}.password_credential TO {_RUNTIME}"
        )
    )


def downgrade() -> None:
    """Restore the prior M4/M5-A runtime ACL exactly."""
    op.execute(
        sa.text(
            f"REVOKE DELETE ON TABLE {_SCHEMA}.password_credential FROM {_RUNTIME}"
        )
    )
