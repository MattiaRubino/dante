"""Enforce 100 inert Draft Vault entries per owner, including atomic moves."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261123_189"
down_revision: str | None = "20261122_188"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

MAX_DRAFTS_PER_OWNER = 100

_QUOTA_FUNCTION = r"""
CREATE FUNCTION dante.enforce_temporal_draft_vault_capacity()
RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER VOLATILE
SET search_path = pg_catalog,dante,pg_temp
AS $function$
BEGIN
    -- Every writer, including Move's SERIALIZABLE transaction, passes through
    -- this INSERT trigger. Serialize the capacity decision for this owner,
    -- not the whole table. Updating an existing draft never consumes a slot.
    PERFORM pg_advisory_xact_lock(
        hashtextextended('dante:temporal-draft-vault:' || NEW.owner_person_ref::text, 0)
    );
    IF (
        SELECT count(*)
          FROM dante.temporal_draft_vault AS d
         WHERE d.owner_person_ref = NEW.owner_person_ref
    ) >= 100 THEN
        RAISE EXCEPTION 'draft vault capacity exceeded'
          USING ERRCODE = 'PZ101';
    END IF;
    RETURN NEW;
END;
$function$;
"""


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text(_QUOTA_FUNCTION))
    bind.exec_driver_sql(
        "ALTER FUNCTION dante.enforce_temporal_draft_vault_capacity() "
        "OWNER TO dante_owner"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON FUNCTION dante.enforce_temporal_draft_vault_capacity() "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(
        "CREATE TRIGGER tr_temporal_draft_vault_owner_capacity "
        "BEFORE INSERT ON dante.temporal_draft_vault "
        "FOR EACH ROW EXECUTE FUNCTION dante.enforce_temporal_draft_vault_capacity()"
    )


def downgrade() -> None:
    raise RuntimeError("Draft Vault capacity constraint requires a reviewed forward migration")
