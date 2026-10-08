"""B14 M1: restore one-off Activity profile reads after scoped Occurrence support.

_123 introduced an SQL LATERAL read that PostgreSQL can inline and evaluate
with a NULL Occurrence even for a regular Activity. A deterministic PL/pgSQL
branch prevents invoking the strictly self-scoped Occurrence accessor unless
the Activity really belongs to a materialized Routine Occurrence.

This is a forward fix because _123 has already run in local PostgreSQL.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261008_124"
down_revision: str | None = "20261008_123"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text(_READ_ACTIVITY_PROFILE))
    bind.exec_driver_sql(
        "ALTER FUNCTION dante.get_self_activity_profile(uuid,uuid) "
        "OWNER TO dante_owner"
    )
    bind.exec_driver_sql(
        "REVOKE ALL ON FUNCTION dante.get_self_activity_profile(uuid,uuid) "
        "FROM PUBLIC,dante_runtime,dante_migrator"
    )
    bind.exec_driver_sql(
        "GRANT EXECUTE ON FUNCTION dante.get_self_activity_profile(uuid,uuid) "
        "TO dante_runtime"
    )


def downgrade() -> None:
    raise RuntimeError(
        "20261008_124 is forward-only: one-off Activity access must remain safe"
    )


_READ_ACTIVITY_PROFILE = r"""
CREATE OR REPLACE FUNCTION dante.get_self_activity_profile(
    actor uuid, requested_activity uuid
) RETURNS TABLE(
    activity_ref uuid, title text, description text, location text,
    color_code text, revision bigint
)
LANGUAGE plpgsql SECURITY DEFINER STABLE PARALLEL RESTRICTED
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    owned_activity dante.activity_intention%ROWTYPE;
    bound_occurrence uuid;
    applied_patch jsonb := '{}'::jsonb;
BEGIN
    SELECT a.* INTO owned_activity
      FROM dante.activity_intention AS a
     WHERE a.activity_ref=requested_activity
       AND a.self_person_ref=actor
       AND a.retired_at IS NULL;

    IF NOT FOUND THEN
        RETURN;
    END IF;

    bound_occurrence := dante.get_self_materialized_activity_occurrence(
        actor,owned_activity.activity_ref
    );
    IF bound_occurrence IS NOT NULL THEN
        applied_patch := dante.get_self_occurrence_profile_patch(
            actor,bound_occurrence
        );
    END IF;

    RETURN QUERY SELECT
        owned_activity.activity_ref,
        COALESCE(applied_patch->>'title',owned_activity.title),
        CASE WHEN applied_patch ? 'description'
             THEN applied_patch->>'description'
             ELSE owned_activity.description END,
        CASE WHEN applied_patch ? 'location'
             THEN applied_patch->>'location'
             ELSE owned_activity.location END,
        CASE WHEN applied_patch ? 'color_code'
             THEN applied_patch->>'color_code'
             ELSE owned_activity.color_code END,
        owned_activity.profile_revision;
END;
$function$;
"""
