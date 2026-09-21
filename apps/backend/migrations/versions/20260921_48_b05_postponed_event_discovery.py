"""B05-D: bounded discovery of postponed Event Schedules.

Revision ID: 20260921_48
Revises: 20260920_47
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260921_48"
down_revision: str | None = "20260920_47"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        sa.text(r"""
        CREATE FUNCTION dante.list_self_postponed_events(requested_self_person_ref uuid)
        RETURNS TABLE(
            event_ref uuid,
            schedule_ref uuid,
            title text,
            created_at timestamptz,
            life_area_ref uuid,
            life_area_assignment_revision bigint,
            unschedule_operation_id text
        )
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT expectation.event_ref,
                   schedule.schedule_ref,
                   expectation.title,
                   expectation.created_at,
                   assignment.life_area_ref,
                   assignment.revision,
                   latest_unschedule.operation_id
              FROM dante.event_expectation AS expectation
              JOIN dante.schedule AS schedule
                ON schedule.subject_native_ref=expectation.event_ref
              JOIN LATERAL (
                  SELECT operation.operation_id
                    FROM dante.schedule_unschedule_operation AS operation
                   WHERE operation.self_person_ref=requested_self_person_ref
                     AND operation.schedule_ref=schedule.schedule_ref
                   ORDER BY operation.created_at DESC,operation.operation_id DESC
                   LIMIT 1
              ) AS latest_unschedule ON true
              LEFT JOIN dante.event_life_area_assignment AS assignment
                ON assignment.self_person_ref=requested_self_person_ref
               AND assignment.event_ref=expectation.event_ref
             WHERE expectation.self_person_ref=requested_self_person_ref
               AND EXISTS (
                   SELECT 1 FROM dante.account_application_context
                    WHERE self_person_ref=requested_self_person_ref
               )
               AND NOT EXISTS (
                   SELECT 1 FROM dante.schedule_current_placement AS current
                    WHERE current.scoped_owner_ref=schedule.schedule_ref
               )
             ORDER BY expectation.created_at,expectation.event_ref,schedule.schedule_ref;
        $function$;
        """)
    )
    signature = "dante.list_self_postponed_events(uuid)"
    op.execute(sa.text(f"ALTER FUNCTION {signature} OWNER TO dante_owner"))
    op.execute(
        sa.text(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} "
            "FROM PUBLIC,dante_runtime,dante_migrator"
        )
    )
    op.execute(sa.text(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime"))
    op.execute(
        sa.text(r"""
        CREATE FUNCTION dante.assert_self_event_schedule(
            requested_self_person_ref uuid,
            requested_event_ref uuid,
            requested_schedule_ref uuid
        )
        RETURNS boolean
        LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
        SET search_path = pg_catalog, dante, pg_temp
        AS $function$
            SELECT EXISTS (
                SELECT 1
                  FROM dante.event_expectation AS expectation
                  JOIN dante.schedule AS schedule
                    ON schedule.subject_native_ref=expectation.event_ref
                 WHERE expectation.self_person_ref=requested_self_person_ref
                   AND expectation.event_ref=requested_event_ref
                   AND schedule.schedule_ref=requested_schedule_ref
                   AND EXISTS (
                       SELECT 1 FROM dante.account_application_context
                        WHERE self_person_ref=requested_self_person_ref
                   )
            );
        $function$;
        """)
    )
    signature = "dante.assert_self_event_schedule(uuid,uuid,uuid)"
    op.execute(sa.text(f"ALTER FUNCTION {signature} OWNER TO dante_owner"))
    op.execute(
        sa.text(
            f"REVOKE ALL PRIVILEGES ON FUNCTION {signature} "
            "FROM PUBLIC,dante_runtime,dante_migrator"
        )
    )
    op.execute(sa.text(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime"))


def downgrade() -> None:
    raise RuntimeError("B05-D postponed Event discovery requires a reviewed forward migration")
