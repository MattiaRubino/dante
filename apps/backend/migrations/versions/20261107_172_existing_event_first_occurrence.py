"""Attach the first canonical Event Occurrence to the original Event.

Revision ID: 20261107_172
Revises: 20261106_171

Existing 171 associations remain nullable legacy associations; a historical
exclusion must never be silently deleted or reinterpreted by this migration.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261107_172"
down_revision: str | None = "20261106_171"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "event_recurring_seed",
        sa.Column("first_occurrence_ref", sa.Uuid(), nullable=True),
        schema="dante",
    )
    op.create_foreign_key(
        "fk_event_recurring_seed_occurrence",
        "event_recurring_seed",
        "occurrence",
        ["first_occurrence_ref"],
        ["occurrence_ref"],
        source_schema="dante",
        referent_schema="dante",
    )
    op.create_unique_constraint(
        "uq_event_recurring_seed_occurrence",
        "event_recurring_seed",
        ["first_occurrence_ref"],
        schema="dante",
    )
    db = op.get_bind()
    for signature, definition in (
        ("bind_self_event_recurring_first(uuid,uuid,uuid,uuid,uuid,uuid,bigint,date)", _BIND),
        ("get_self_event_recurring_first_by_source(uuid,uuid)", _SOURCE),
        ("get_self_event_recurring_first_by_occurrence(uuid,uuid)", _OCCURRENCE),
    ):
        db.exec_driver_sql(definition)
        db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261107_172 is forward-only")


_BIND = r"""
CREATE FUNCTION dante.bind_self_event_recurring_first(
    actor uuid, first_event uuid, future_source uuid, first_occurrence uuid,
    first_schedule uuid, expected_placement uuid, expected_profile bigint, first_day date
) RETURNS TABLE(source_event_ref uuid, first_occurrence_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE prior record;
BEGIN
    PERFORM 1
      FROM dante.event_expectation AS original
     WHERE original.event_ref=first_event
       AND original.self_person_ref=actor
     FOR UPDATE;
    IF NOT FOUND
       OR first_event=future_source
       OR (SELECT dante.get_self_event_profile_revision(actor,first_event))
          IS DISTINCT FROM expected_profile
       OR NOT EXISTS (
           SELECT 1 FROM dante.event_expectation AS source
            WHERE source.event_ref=future_source AND source.self_person_ref=actor
       )
       OR NOT EXISTS (
           SELECT 1 FROM dante.event_recurrence_current_history AS active
            WHERE active.event_ref=future_source AND active.current_until_at IS NULL
       )
       OR EXISTS (
           SELECT 1 FROM dante.get_self_event_recurrence(actor,first_event)
       )
       OR EXISTS (
           SELECT 1 FROM dante.schedule AS source_schedule
            WHERE source_schedule.subject_native_ref=future_source
       )
       OR NOT EXISTS (
           SELECT 1
             FROM dante.schedule AS original_schedule
             JOIN dante.schedule_current_placement AS current
               ON current.scoped_owner_ref=original_schedule.schedule_ref
             WHERE original_schedule.schedule_ref=first_schedule
               AND original_schedule.subject_native_ref=first_event
               AND current.material_state_ref=expected_placement
       )
       OR NOT EXISTS (
           SELECT 1
             FROM dante.occurrence_generation AS generated
             JOIN dante.occurrence_generation_calendar AS calendar
               ON calendar.occurrence_ref=generated.occurrence_ref
             JOIN dante.event_recurrence_current_history AS active
               ON active.event_ref=future_source
              AND active.material_state_ref=generated.governing_recurrence_state_ref
              AND active.current_until_at IS NULL
             JOIN dante.schedule_placement_state AS state
               ON state.material_state_ref=expected_placement
              AND state.schedule_ref=first_schedule
        LEFT JOIN dante.schedule_placement_named_zone_state AS timed
               ON timed.material_state_ref=state.material_state_ref
        LEFT JOIN dante.schedule_placement_date_state AS days
               ON days.material_state_ref=state.material_state_ref
            WHERE generated.occurrence_ref=first_occurrence
              AND generated.source_native_ref=future_source
              AND generated.origin_code='recurrence_generated'
              AND calendar.generated_date=first_day
              AND (
                  (
                      state.temporal_form_code='named_zone_local'
                      AND timed.starts_local_at::date=first_day
                      AND calendar.generated_wall_time=timed.starts_local_at::time
                      AND calendar.zone_id=timed.zone_id
                      AND calendar.resolved_at IS NOT DISTINCT FROM timed.resolved_start_at
                  )
                  OR (
                      state.temporal_form_code='date_span'
                      AND lower(days.date_span)=first_day
                      AND calendar.generated_wall_time IS NULL
                  )
              )
              AND NOT EXISTS (
                  SELECT 1 FROM dante.occurrence_skip AS skipped
                   WHERE skipped.occurrence_ref=first_occurrence
              )
       )
    THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='event_recurring_first_unavailable',
            MESSAGE='The original Event or the canonical first Occurrence changed';
    END IF;

    SELECT * INTO prior
      FROM dante.event_recurring_seed AS seed
     WHERE seed.event_ref=first_event FOR UPDATE;
    IF FOUND THEN
        IF prior.source_event_ref<>future_source
           OR prior.first_occurrence_ref IS DISTINCT FROM first_occurrence THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='event_recurring_first_conflict',
                MESSAGE='Event already belongs to another first-instance binding';
        END IF;
        RETURN QUERY SELECT prior.source_event_ref,prior.first_occurrence_ref,true;
        RETURN;
    END IF;
    INSERT INTO dante.event_recurring_seed(
        event_ref,source_event_ref,self_person_ref,accepted_at,first_occurrence_ref
    ) VALUES(first_event,future_source,actor,statement_timestamp(),first_occurrence);
    RETURN QUERY SELECT future_source,first_occurrence,false;
END;
$function$;
"""


_SOURCE = r"""
CREATE FUNCTION dante.get_self_event_recurring_first_by_source(
    actor uuid, source uuid
) RETURNS TABLE(first_occurrence_ref uuid, first_event_ref uuid)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT seed.first_occurrence_ref,seed.event_ref
      FROM dante.event_recurring_seed AS seed
      JOIN dante.event_expectation AS original ON original.event_ref=seed.event_ref
      JOIN dante.event_expectation AS recurring ON recurring.event_ref=seed.source_event_ref
     WHERE seed.source_event_ref=source AND seed.self_person_ref=actor
       AND original.self_person_ref=actor AND recurring.self_person_ref=actor
       AND seed.first_occurrence_ref IS NOT NULL
$function$;
"""


_OCCURRENCE = r"""
CREATE FUNCTION dante.get_self_event_recurring_first_by_occurrence(
    actor uuid, first_occurrence uuid
) RETURNS TABLE(first_event_ref uuid, source_event_ref uuid)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT seed.event_ref,seed.source_event_ref
      FROM dante.event_recurring_seed AS seed
      JOIN dante.event_expectation AS original ON original.event_ref=seed.event_ref
     WHERE seed.first_occurrence_ref=first_occurrence
       AND seed.self_person_ref=actor AND original.self_person_ref=actor
$function$;
"""
