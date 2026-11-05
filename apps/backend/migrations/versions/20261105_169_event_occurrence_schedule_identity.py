"""Verify an Event Occurrence Schedule through one owner-scoped capability.

The former Event Timeline Schedule listing was retired at _159. The selected
Event edit must validate its exact Schedule without runtime table SELECT or a
bounded listing that can omit a legitimate later Occurrence.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261105_169"
down_revision: str | None = "20261105_168"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_IDENTITY = r"""
CREATE FUNCTION dante.is_self_event_occurrence_schedule(
    requested_actor uuid, requested_occurrence uuid, requested_schedule uuid
) RETURNS boolean
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT EXISTS (
        SELECT 1
          FROM dante.occurrence_generation AS generation
          JOIN dante.event_expectation AS event
            ON event.event_ref=generation.source_native_ref
          JOIN dante.schedule AS schedule
            ON schedule.subject_native_ref=generation.occurrence_ref
         WHERE generation.occurrence_ref=requested_occurrence
           AND event.self_person_ref=requested_actor
           AND schedule.schedule_ref=requested_schedule
    )
$function$;
"""


def upgrade() -> None:
    db = op.get_bind()
    db.exec_driver_sql(_IDENTITY)
    signature = "dante.is_self_event_occurrence_schedule(uuid,uuid,uuid)"
    db.exec_driver_sql(f"ALTER FUNCTION {signature} OWNER TO dante_owner")
    db.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION {signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION {signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261105_169 is forward-only")
