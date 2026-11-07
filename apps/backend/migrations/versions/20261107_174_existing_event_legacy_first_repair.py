"""Recover proven legacy first Event Occurrences on the normal Timeline checkpoint.

Revision ID: 20261107_174
Revises: 20261107_173

The migration only installs the guarded repair capability. No rows are
modified at upgrade time. A later owner-scoped Event checkpoint performs
an eligible repair transactionally, preserving the original Event graph.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261107_174"
down_revision: str | None = "20261107_173"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    for name, type_ in (
        ("legacy_exclusion_ref", sa.Uuid()),
        ("legacy_exclusion_operation_id", sa.Text()),
        ("legacy_exclusion_fingerprint", sa.Text()),
        ("legacy_exclusion_accepted_at", sa.DateTime(timezone=True)),
        ("legacy_repaired_at", sa.DateTime(timezone=True)),
    ):
        op.add_column(
            "event_recurring_seed",
            sa.Column(name, type_, nullable=True),
            schema="dante",
        )
    op.create_check_constraint(
        "ck_event_recurring_seed_legacy_proof",
        "event_recurring_seed",
        """(
            legacy_repaired_at IS NULL
            AND legacy_exclusion_ref IS NULL
            AND legacy_exclusion_operation_id IS NULL
            AND legacy_exclusion_fingerprint IS NULL
            AND legacy_exclusion_accepted_at IS NULL
        ) OR (
            legacy_repaired_at IS NOT NULL
            AND first_occurrence_ref IS NOT NULL
            AND legacy_exclusion_ref IS NOT NULL
            AND legacy_exclusion_operation_id IS NOT NULL
            AND legacy_exclusion_fingerprint IS NOT NULL
            AND legacy_exclusion_accepted_at IS NOT NULL
        )""",
        schema="dante",
    )
    connection = op.get_bind()
    connection.exec_driver_sql(_REPAIR_LEGACY_FIRST.replace("%", "%%"))
    signature = "repair_self_event_legacy_first(uuid,uuid)"
    connection.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
    connection.exec_driver_sql(
        f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
    )
    connection.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261107_174 is forward-only")


_REPAIR_LEGACY_FIRST = r"""
CREATE FUNCTION dante.repair_self_event_legacy_first(
    requested_actor uuid, requested_source uuid
) RETURNS uuid
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE
    seed_row dante.event_recurring_seed%ROWTYPE;
    recurrence_row record;
    original_schedule record;
    excluded record;
    exclusion_count bigint;
    schedule_count bigint;
    first_day date;
    first_wall time;
    first_resolved timestamptz;
    first_zone text;
    checkpoint_operation text;
    checkpoint_fingerprint text;
    checkpoint_result record;
    first_occurrence uuid;
BEGIN
    -- Constant-time indexed lookup for a legacy association; normal recurring
    -- Event sources and already linked first Events have nothing to repair.
    SELECT * INTO seed_row
      FROM dante.event_recurring_seed AS seed
     WHERE seed.source_event_ref=requested_source
       AND seed.self_person_ref=requested_actor;
    IF NOT FOUND OR seed_row.first_occurrence_ref IS NOT NULL THEN
        RETURN NULL;
    END IF;
    -- A changed Recurrence must never be retroactively reinterpreted as its
    -- former first candidate. Keep that association for explicit review.
    SELECT current.material_state_ref,state.family_code,
           calendar.clock_basis_code,calendar.zone_id,boundary.date_value
      INTO recurrence_row
      FROM dante.event_recurrence_current_history AS current
      JOIN dante.event_recurrence_state AS state
        ON state.material_state_ref=current.material_state_ref
      JOIN dante.event_recurrence_calendar_state AS calendar
        ON calendar.material_state_ref=current.material_state_ref
      JOIN dante.event_recurrence_boundary_state AS boundary
        ON boundary.material_state_ref=current.material_state_ref
       AND boundary.boundary_role='effective_from'
     WHERE current.event_ref=requested_source
       AND current.current_until_at IS NULL
       AND EXISTS (
           SELECT 1 FROM dante.event_expectation AS source
            WHERE source.event_ref=current.event_ref
              AND source.self_person_ref=requested_actor
       );
    IF NOT FOUND
       OR recurrence_row.family_code<>'calendar_wall_clock'
       OR recurrence_row.clock_basis_code<>'named_zone'
       OR recurrence_row.zone_id IS NULL THEN
        RETURN NULL;
    END IF;
    SELECT count(*) INTO schedule_count
      FROM dante.schedule AS schedule
     WHERE schedule.subject_native_ref=seed_row.event_ref;
    IF schedule_count<>1 THEN
        RETURN NULL;
    END IF;
    SELECT placement.material_state_ref,state.temporal_form_code,
           zoned.starts_local_at,zoned.zone_id,zoned.resolved_start_at,
           lower(dates.date_span) AS start_date
      INTO original_schedule
      FROM dante.schedule AS schedule
      JOIN dante.schedule_current_placement AS placement
        ON placement.scoped_owner_ref=schedule.schedule_ref
      JOIN dante.schedule_placement_state AS state
        ON state.schedule_ref=schedule.schedule_ref
       AND state.material_state_ref=placement.material_state_ref
 LEFT JOIN dante.schedule_placement_named_zone_state AS zoned
        ON zoned.material_state_ref=state.material_state_ref
 LEFT JOIN dante.schedule_placement_date_state AS dates
        ON dates.material_state_ref=state.material_state_ref
     WHERE schedule.subject_native_ref=seed_row.event_ref;
    IF NOT FOUND THEN
        RETURN NULL;
    END IF;
    IF original_schedule.temporal_form_code='named_zone_local' THEN
        first_day:=original_schedule.starts_local_at::date;
        first_wall:=original_schedule.starts_local_at::time;
        first_resolved:=original_schedule.resolved_start_at;
        first_zone:=original_schedule.zone_id;
        IF first_zone IS DISTINCT FROM recurrence_row.zone_id
           OR first_wall IS NULL
           OR NOT EXISTS (
               SELECT 1 FROM dante.event_recurrence_calendar_wall_time AS w
                WHERE w.material_state_ref=recurrence_row.material_state_ref
                  AND w.wall_time=first_wall
           ) THEN
            RETURN NULL;
        END IF;
    ELSIF original_schedule.temporal_form_code='date_span' THEN
        first_day:=original_schedule.start_date;
        first_wall:=NULL;
        first_resolved:=NULL;
        first_zone:=recurrence_row.zone_id;
        IF EXISTS (
            SELECT 1 FROM dante.event_recurrence_calendar_wall_time AS w
             WHERE w.material_state_ref=recurrence_row.material_state_ref
        ) THEN
            RETURN NULL;
        END IF;
    ELSE
        RETURN NULL;
    END IF;
    IF first_day IS NULL OR first_day<>recurrence_row.date_value THEN
        RETURN NULL;
    END IF;

    -- The 171 conversion minted exactly one dated exclusion using a dedicated
    -- deterministic operation id. Other exclusions or skipped Occurrences are
    -- not interchangeable with this proof.
    SELECT count(*) INTO exclusion_count
      FROM dante.occurrence_exclusion AS exclusion
     WHERE exclusion.self_person_ref=requested_actor
       AND exclusion.source_native_ref=requested_source
       AND exclusion.governing_recurrence_state_ref=recurrence_row.material_state_ref
       AND exclusion.family_code='calendar_wall_clock'
       AND exclusion.generated_date=first_day
       AND exclusion.generated_wall_time IS NOT DISTINCT FROM first_wall;
    IF exclusion_count<>1 THEN
        RETURN NULL;
    END IF;
    SELECT exclusion.exclusion_ref,exclusion.accepted_at,
           receipt.operation_id,receipt.intent_fingerprint
      INTO excluded
      FROM dante.occurrence_exclusion AS exclusion
      JOIN dante.occurrence_exclusion_operation AS receipt
        ON receipt.exclusion_ref=exclusion.exclusion_ref
       AND receipt.self_person_ref=requested_actor
     WHERE exclusion.self_person_ref=requested_actor
       AND exclusion.source_native_ref=requested_source
       AND exclusion.governing_recurrence_state_ref=recurrence_row.material_state_ref
       AND exclusion.family_code='calendar_wall_clock'
       AND exclusion.generated_date=first_day
       AND exclusion.generated_wall_time IS NOT DISTINCT FROM first_wall
       AND exclusion.expected_at IS NULL
       AND exclusion.position_index IS NULL
       AND receipt.operation_id ~ '^b06d:existing-event-first:[0-9a-f]{64}$'
       AND exclusion.accepted_at<=seed_row.accepted_at;
    IF NOT FOUND OR EXISTS (
        SELECT 1 FROM dante.occurrence_generation AS generated
        JOIN dante.occurrence_generation_calendar AS coordinate
          ON coordinate.occurrence_ref=generated.occurrence_ref
       WHERE generated.source_native_ref=requested_source
         AND generated.governing_recurrence_state_ref=recurrence_row.material_state_ref
         AND coordinate.generated_date=first_day
         AND coordinate.generated_wall_time IS NOT DISTINCT FROM first_wall
    ) THEN
        RETURN NULL;
    END IF;
    checkpoint_operation:='b06d:legacy-event-first:'||
                           replace(seed_row.event_ref::text,'-','');
    checkpoint_fingerprint:=encode(
        sha256(convert_to(
            'legacy-event-first-v1:'||requested_actor::text||':'||
            requested_source::text||':'||first_day::text||':'||
            COALESCE(first_wall::text,'all-day')||':'||
            recurrence_row.material_state_ref::text,
            'UTF8'
        )),
        'hex'
    );
    -- The canonical checkpoint locks the source Recurrence using the
    -- established advisory-lock namespace before the exclusion is removed.
    SELECT * INTO checkpoint_result
      FROM dante.begin_self_event_occurrence_checkpoint(
          requested_actor,checkpoint_operation,checkpoint_fingerprint,
          requested_source,first_day,first_day+1,first_zone
      );
    IF checkpoint_result.replayed THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='event_legacy_first_receipt_conflict',
            MESSAGE='Legacy first Event checkpoint already used without a binding';
    END IF;
    SELECT * INTO seed_row
      FROM dante.event_recurring_seed AS seed
     WHERE seed.source_event_ref=requested_source
       AND seed.self_person_ref=requested_actor
     FOR UPDATE;
    IF NOT FOUND OR seed_row.first_occurrence_ref IS NOT NULL
       OR NOT EXISTS (
           SELECT 1 FROM dante.event_recurrence_current_history AS current
            WHERE current.event_ref=requested_source
              AND current.material_state_ref=recurrence_row.material_state_ref
              AND current.current_until_at IS NULL
       ) OR NOT EXISTS (
           SELECT 1 FROM dante.event_expectation AS original
            WHERE original.event_ref=seed_row.event_ref
              AND original.self_person_ref=requested_actor
       ) OR NOT EXISTS (
           SELECT 1 FROM dante.schedule AS schedule
           JOIN dante.schedule_current_placement AS placement
             ON placement.scoped_owner_ref=schedule.schedule_ref
           WHERE schedule.subject_native_ref=seed_row.event_ref
             AND placement.material_state_ref=original_schedule.material_state_ref
       ) THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='event_legacy_first_concurrent',
            MESSAGE='First Event link changed during recovery';
    END IF;
    SELECT exclusion.exclusion_ref,exclusion.accepted_at,
           receipt.operation_id,receipt.intent_fingerprint
      INTO excluded
      FROM dante.occurrence_exclusion AS exclusion
      JOIN dante.occurrence_exclusion_operation AS receipt
        ON receipt.exclusion_ref=exclusion.exclusion_ref
       AND receipt.self_person_ref=requested_actor
     WHERE exclusion.self_person_ref=requested_actor
       AND exclusion.source_native_ref=requested_source
       AND exclusion.governing_recurrence_state_ref=recurrence_row.material_state_ref
       AND exclusion.family_code='calendar_wall_clock'
       AND exclusion.generated_date=first_day
       AND exclusion.generated_wall_time IS NOT DISTINCT FROM first_wall
       AND exclusion.expected_at IS NULL
       AND exclusion.position_index IS NULL
       AND receipt.operation_id ~ '^b06d:existing-event-first:[0-9a-f]{64}$'
       AND exclusion.accepted_at<=seed_row.accepted_at
     FOR UPDATE OF exclusion,receipt;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='event_legacy_first_unproven',
            MESSAGE='The legacy exclusion changed during recovery';
    END IF;
    DELETE FROM dante.occurrence_exclusion_operation AS operation
     WHERE operation.exclusion_ref=excluded.exclusion_ref
       AND operation.self_person_ref=requested_actor
       AND operation.operation_id=excluded.operation_id;
    DELETE FROM dante.occurrence_exclusion AS exclusion
     WHERE exclusion.exclusion_ref=excluded.exclusion_ref
       AND exclusion.self_person_ref=requested_actor;
    SELECT created.occurrence_ref INTO first_occurrence
      FROM dante.materialize_self_event_occurrence_candidate(
          requested_actor,checkpoint_operation,requested_source,
          recurrence_row.material_state_ref,'calendar_wall_clock',
          first_day,first_wall,'named_zone',first_zone,first_resolved,
          NULL,NULL,NULL,NULL,NULL,NULL
      ) AS created;
    IF first_occurrence IS NULL THEN
        RAISE EXCEPTION USING ERRCODE='23514',
            CONSTRAINT='event_legacy_first_materialization_failed',
            MESSAGE='Canonical first Event Occurrence was not generated';
    END IF;
    UPDATE dante.event_recurring_seed AS seed
       SET first_occurrence_ref=first_occurrence,
           legacy_exclusion_ref=excluded.exclusion_ref,
           legacy_exclusion_operation_id=excluded.operation_id,
           legacy_exclusion_fingerprint=excluded.intent_fingerprint,
           legacy_exclusion_accepted_at=excluded.accepted_at,
           legacy_repaired_at=statement_timestamp()
     WHERE seed.source_event_ref=requested_source
       AND seed.self_person_ref=requested_actor
       AND seed.first_occurrence_ref IS NULL;
    IF NOT FOUND THEN
        RAISE EXCEPTION USING ERRCODE='23505',
            CONSTRAINT='event_legacy_first_concurrent',
            MESSAGE='First Event link changed during recovery';
    END IF;
    RETURN first_occurrence;
END;
$function$;
"""
