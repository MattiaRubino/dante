"""B10-B: admit Outcome to the canonical ScopedAddress owner dispatcher.

Revision ID: 20260925_77
Revises: 20260925_76

Revision 76 materializes Outcome as a ScopedRecordRef owner and extends the
scoped-family CHECK, but the pre-existing CP6 owner-binding trigger function
still dispatches only Schedule, Actual and Temporal Constraint. This
forward-only repair extends that same canonical dispatcher to Outcome; it does
not introduce a second addressing authority or change the database topology.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260925_77"
down_revision: str | None = "20260925_76"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql(statement: str) -> None:
    op.get_bind().exec_driver_sql(statement)


def upgrade() -> None:
    _sql(
        r"""
CREATE OR REPLACE FUNCTION dante.enforce_scoped_address_owner()
RETURNS trigger
LANGUAGE plpgsql
SECURITY INVOKER
VOLATILE
PARALLEL UNSAFE
SET search_path = pg_catalog, dante, pg_temp
AS $function$
DECLARE
    owner_exists boolean := false;
BEGIN
    CASE NEW.scoped_family
        WHEN 'schedule' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.schedule
                 WHERE schedule_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'actual' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.actual
                 WHERE actual_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'temporal_constraint' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.temporal_constraint
                 WHERE constraint_ref=NEW.scoped_ref
            ) INTO owner_exists;
        WHEN 'outcome' THEN
            SELECT EXISTS (
                SELECT 1
                  FROM dante.outcome
                 WHERE outcome_ref=NEW.scoped_ref
            ) INTO owner_exists;
        ELSE
            owner_exists := false;
    END CASE;

    IF NOT owner_exists THEN
        RAISE EXCEPTION USING
            ERRCODE='23503',
            CONSTRAINT=TG_NAME,
            TABLE=TG_TABLE_NAME,
            SCHEMA=TG_TABLE_SCHEMA,
            MESSAGE='scoped address owner binding rejected',
            DETAIL='scoped address must resolve to the declared bounded owner family';
    END IF;

    RETURN NEW;
END;
$function$
"""
    )

    # Preserve the canonical ownership/least-privilege contract explicitly.
    _sql("ALTER FUNCTION dante.enforce_scoped_address_owner() OWNER TO dante_owner")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_scoped_address_owner() FROM PUBLIC")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_scoped_address_owner() FROM dante_runtime")
    _sql("REVOKE ALL ON FUNCTION dante.enforce_scoped_address_owner() FROM dante_migrator")


def downgrade() -> None:
    raise RuntimeError(
        "DANTE migrations are forward-only; B10-B Outcome ScopedAddress dispatch cannot be downgraded."
    )
