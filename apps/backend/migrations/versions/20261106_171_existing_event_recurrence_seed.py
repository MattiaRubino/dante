"""Bind a one-off Event to a separate future recurring source.

Revision ID: 20261106_171
Revises: 20261106_170
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261106_171"
down_revision: str | None = "20261106_170"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "event_recurring_seed",
        sa.Column("event_ref", sa.Uuid(), nullable=False),
        sa.Column("source_event_ref", sa.Uuid(), nullable=False),
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("event_ref", name="pk_event_recurring_seed"),
        sa.UniqueConstraint("source_event_ref", name="uq_event_recurring_seed_source"),
        sa.ForeignKeyConstraint(
            ["event_ref"], ["dante.event_expectation.event_ref"],
            name="fk_event_recurring_seed_event",
        ),
        sa.ForeignKeyConstraint(
            ["source_event_ref"], ["dante.event_expectation.event_ref"],
            name="fk_event_recurring_seed_source",
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"], ["dante.person.person_ref"],
            name="fk_event_recurring_seed_person",
        ),
        schema="dante",
    )
    db = op.get_bind()
    db.exec_driver_sql("ALTER TABLE dante.event_recurring_seed OWNER TO dante_owner")
    db.exec_driver_sql(_BIND)
    db.exec_driver_sql(_GET)
    db.exec_driver_sql(
        "REVOKE ALL ON dante.event_recurring_seed FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in (
        "bind_self_event_recurring_seed(uuid,uuid,uuid,uuid,uuid,bigint,date)",
        "get_self_event_recurring_seed(uuid,uuid)",
    ):
        db.exec_driver_sql(f"ALTER FUNCTION dante.{signature} OWNER TO dante_owner")
        db.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        db.exec_driver_sql(f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime")


def downgrade() -> None:
    raise RuntimeError("20261106_171 is forward-only")


_BIND = r"""
CREATE FUNCTION dante.bind_self_event_recurring_seed(
    actor uuid, first_event uuid, future_source uuid,
    first_schedule uuid, expected_placement uuid, expected_profile bigint,
    first_day date
) RETURNS TABLE(source_event_ref uuid, replayed boolean)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
#variable_conflict error
DECLARE prior uuid;
BEGIN
    PERFORM 1 FROM dante.event_expectation AS original
     WHERE original.event_ref=first_event AND original.self_person_ref=actor
     FOR UPDATE;
    IF NOT FOUND OR first_event=future_source
      OR (SELECT dante.get_self_event_profile_revision(actor,first_event))
            IS DISTINCT FROM expected_profile
      OR NOT EXISTS (
          SELECT 1 FROM dante.event_expectation AS future
           WHERE future.event_ref=future_source AND future.self_person_ref=actor
      )
      OR NOT EXISTS (
          SELECT 1 FROM dante.get_self_event_recurrence(actor,future_source)
      )
      OR EXISTS (
          SELECT 1 FROM dante.get_self_event_recurrence(actor,first_event)
      )
      OR EXISTS (
          SELECT 1 FROM dante.schedule AS future_schedule
           WHERE future_schedule.subject_native_ref=future_source
      )
      OR NOT EXISTS (
          SELECT 1 FROM dante.occurrence_exclusion AS excluded
          JOIN dante.event_recurrence_current_history AS active
            ON active.event_ref=future_source
           AND active.material_state_ref=excluded.governing_recurrence_state_ref
           AND active.current_until_at IS NULL
         WHERE excluded.source_native_ref=future_source
           AND excluded.self_person_ref=actor
           AND excluded.family_code='calendar_wall_clock'
           AND excluded.generated_date=first_day
      )
      OR NOT EXISTS (
          SELECT 1 FROM dante.schedule AS original_schedule
          JOIN dante.schedule_current_placement AS current
            ON current.scoped_owner_ref=original_schedule.schedule_ref
           WHERE original_schedule.schedule_ref=first_schedule
             AND original_schedule.subject_native_ref=first_event
             AND current.material_state_ref=expected_placement
      ) THEN
        RAISE EXCEPTION USING ERRCODE='23503',
            CONSTRAINT='event_recurring_seed_unavailable',
            MESSAGE='First Event or future source changed';
    END IF;
    SELECT seed.source_event_ref INTO prior
      FROM dante.event_recurring_seed AS seed
     WHERE seed.event_ref=first_event FOR UPDATE;
    IF FOUND THEN
        IF prior<>future_source THEN
            RAISE EXCEPTION USING ERRCODE='23505',
                CONSTRAINT='event_recurring_seed_conflict',
                MESSAGE='First Event already belongs to another series';
        END IF;
        RETURN QUERY SELECT prior,true;
        RETURN;
    END IF;
    INSERT INTO dante.event_recurring_seed(
        event_ref,source_event_ref,self_person_ref,accepted_at
    ) VALUES(first_event,future_source,actor,statement_timestamp());
    RETURN QUERY SELECT future_source,false;
END;
$function$;
"""


_GET = r"""
CREATE FUNCTION dante.get_self_event_recurring_seed(actor uuid, first_event uuid)
RETURNS TABLE(source_event_ref uuid, accepted_at timestamptz)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $function$
    SELECT seed.source_event_ref,seed.accepted_at
      FROM dante.event_recurring_seed AS seed
      JOIN dante.event_expectation AS original
        ON original.event_ref=seed.event_ref
       AND original.self_person_ref=actor
     WHERE seed.event_ref=first_event AND seed.self_person_ref=actor
$function$;
"""
