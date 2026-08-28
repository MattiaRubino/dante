"""Add the narrow M3 Account security serialization capability.

Revision ID: 20260827_10
Revises: 20260827_09
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260827_10"
down_revision: str | None = "20260827_09"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DANTE_SCHEMA = "dante"
_RUNTIME_ROLE = "dante_runtime"
_MIGRATOR_ROLE = "dante_migrator"
_FUNCTION_SIGNATURE = "dante.acquire_account_security_lock(uuid)"


def upgrade() -> None:
    """Expose only the Account row-lock capability required by M3 signin."""
    op.execute(
        sa.text(
            """
            CREATE FUNCTION dante.acquire_account_security_lock(p_account_ref uuid)
            RETURNS void
            LANGUAGE plpgsql
            VOLATILE
            PARALLEL UNSAFE
            SECURITY DEFINER
            SET search_path = pg_catalog, dante, pg_temp
            AS $function$
            BEGIN
                PERFORM 1
                FROM dante.account AS account
                WHERE account.account_ref = p_account_ref
                FOR UPDATE;
            END;
            $function$
            """
        )
    )
    op.execute(sa.text(f"ALTER FUNCTION {_FUNCTION_SIGNATURE} OWNER TO dante_owner"))
    op.execute(
        sa.text(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {_FUNCTION_SIGNATURE} "
            f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
        )
    )
    op.execute(sa.text(f"GRANT EXECUTE ON FUNCTION {_FUNCTION_SIGNATURE} TO {_RUNTIME_ROLE}"))


def downgrade() -> None:
    """Remove the M3 Account row-lock capability and its runtime grant."""
    op.execute(
        sa.text(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {_FUNCTION_SIGNATURE} "
            f"FROM PUBLIC, {_RUNTIME_ROLE}, {_MIGRATOR_ROLE}"
        )
    )
    op.execute(sa.text(f"DROP FUNCTION {_FUNCTION_SIGNATURE}"))
