"""Recognize the physical first Schedule as the converted Event Occurrence.

The first instance of a converted Event is backed by the already-existing
Event's Schedule, not a second Schedule owned by the generated Occurrence.
The same owner-scoped edit capability must admit this first Schedule, just
as it admits Schedules materialized for later Occurrences.

No new table, synthetic Event copy or cross-owner Schedule permission.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261110_184"
down_revision: str | None = "20261109_183"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_IDENTITY = r"""
CREATE OR REPLACE FUNCTION dante.is_self_event_occurrence_schedule(
    requested_actor uuid, requested_occurrence uuid, requested_schedule uuid
) RETURNS boolean
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT EXISTS (
        -- Native recurring Events: a Schedule belongs to the generated Occurrence.
        SELECT 1
          FROM dante.occurrence_generation AS generation
          JOIN dante.event_expectation AS source
            ON source.event_ref=generation.source_native_ref
          JOIN dante.schedule AS schedule
            ON schedule.subject_native_ref=generation.occurrence_ref
         WHERE generation.occurrence_ref=requested_occurrence
           AND source.self_person_ref=requested_actor
           AND schedule.schedule_ref=requested_schedule
        UNION ALL
        -- Converted Events: the original physical Schedule IS the first
        -- Occurrence Schedule. Keep its identity, owner and edit authority.
        SELECT 1
          FROM dante.get_self_event_recurring_first_by_occurrence(
                   requested_actor,requested_occurrence
               ) AS linked
          JOIN dante.event_expectation AS original
            ON original.event_ref=linked.first_event_ref
          JOIN dante.event_expectation AS source
            ON source.event_ref=linked.source_event_ref
          JOIN dante.schedule AS schedule
            ON schedule.subject_native_ref=original.event_ref
         WHERE original.self_person_ref=requested_actor
           AND source.self_person_ref=requested_actor
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
    raise RuntimeError("20261110_184 is forward-only")
