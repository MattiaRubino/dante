"""B14: Event occurrence Schedule/Reminder policy for recurring Event Create.

The recurring Event remains the source. Each generated Occurrence receives its
own accepted Schedule from this immutable Create policy; B11-C remains the
authority for each concrete Reminder.

Revision ID: 20261006_112
Revises: 20261006_111
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20261006_112"
down_revision: str | None = "20261006_111"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "event_occurrence_policy",
        sa.Column("self_person_ref", sa.Uuid(), nullable=False),
        sa.Column("event_ref", sa.Uuid(), nullable=False),
        sa.Column("placement_kind", sa.Text(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("duration_days", sa.Integer(), nullable=True),
        sa.Column("reminder_lead_minutes", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "self_person_ref", "event_ref", name="pk_event_occurrence_policy"
        ),
        sa.ForeignKeyConstraint(
            ["self_person_ref"],
            ["dante.person.person_ref"],
            name="fk_event_occurrence_policy_person",
        ),
        sa.ForeignKeyConstraint(
            ["event_ref"],
            ["dante.event_expectation.event_ref"],
            name="fk_event_occurrence_policy_event",
        ),
        sa.CheckConstraint(
            "placement_kind IN ('timed','all_day')",
            name="ck_event_occurrence_policy_placement_kind",
        ),
        sa.CheckConstraint(
            "("
            "placement_kind='timed' AND duration_minutes BETWEEN 1 AND 525600 "
            "AND duration_days IS NULL"
            ") OR ("
            "placement_kind='all_day' AND duration_days BETWEEN 1 AND 3660 "
            "AND duration_minutes IS NULL AND reminder_lead_minutes IS NULL"
            ")",
            name="ck_event_occurrence_policy_duration",
        ),
        sa.CheckConstraint(
            "reminder_lead_minutes IS NULL OR reminder_lead_minutes BETWEEN 0 AND 10080",
            name="ck_event_occurrence_policy_reminder",
        ),
        schema="dante",
    )
    op.create_index(
        "ix_event_occurrence_policy_event",
        "event_occurrence_policy",
        ["event_ref", "self_person_ref"],
        unique=True,
        schema="dante",
    )

    bind = op.get_bind()
    bind.exec_driver_sql(SET_POLICY)
    bind.exec_driver_sql(GET_POLICY)
    bind.exec_driver_sql(
        "REVOKE ALL ON dante.event_occurrence_policy FROM PUBLIC,dante_runtime,dante_migrator"
    )
    for signature in (
        "set_self_event_occurrence_policy(uuid,uuid,text,integer,integer,integer)",
        "get_self_event_occurrence_policy(uuid,uuid)",
    ):
        bind.exec_driver_sql(
            f"REVOKE ALL ON FUNCTION dante.{signature} FROM PUBLIC,dante_runtime,dante_migrator"
        )
        bind.exec_driver_sql(
            f"GRANT EXECUTE ON FUNCTION dante.{signature} TO dante_runtime"
        )


def downgrade() -> None:
    raise RuntimeError("20261006_112 is forward-only")


SET_POLICY = r"""
CREATE FUNCTION dante.set_self_event_occurrence_policy(
    requested_self_person_ref uuid,
    requested_event_ref uuid,
    requested_placement_kind text,
    requested_duration_minutes integer,
    requested_duration_days integer,
    requested_reminder_lead_minutes integer
) RETURNS TABLE(
    placement_kind text,
    duration_minutes integer,
    duration_days integer,
    reminder_lead_minutes integer,
    created_at timestamptz,
    replayed boolean
)
LANGUAGE plpgsql SECURITY DEFINER VOLATILE PARALLEL UNSAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
DECLARE
    prior dante.event_occurrence_policy%ROWTYPE;
    ts timestamptz := statement_timestamp();
BEGIN
    IF requested_placement_kind NOT IN ('timed','all_day')
       OR (
           requested_placement_kind='timed'
           AND (
               requested_duration_minutes IS NULL
               OR requested_duration_minutes NOT BETWEEN 1 AND 525600
               OR requested_duration_days IS NOT NULL
           )
       )
       OR (
           requested_placement_kind='all_day'
           AND (
               requested_duration_days IS NULL
               OR requested_duration_days NOT BETWEEN 1 AND 3660
               OR requested_duration_minutes IS NOT NULL
               OR requested_reminder_lead_minutes IS NOT NULL
           )
       )
       OR (
           requested_reminder_lead_minutes IS NOT NULL
           AND requested_reminder_lead_minutes NOT BETWEEN 0 AND 10080
       )
    THEN
        RAISE EXCEPTION USING
            ERRCODE='23514',
            CONSTRAINT='event_occurrence_policy_invalid',
            MESSAGE='Event occurrence policy rejected';
    END IF;

    IF NOT EXISTS (
        SELECT 1
          FROM dante.event_expectation AS event
         WHERE event.event_ref=requested_event_ref
           AND event.self_person_ref=requested_self_person_ref
    ) THEN
        RAISE EXCEPTION USING
            ERRCODE='23503',
            CONSTRAINT='event_occurrence_policy_event_unavailable',
            MESSAGE='Event occurrence policy source unavailable';
    END IF;

    SELECT *
      INTO prior
      FROM dante.event_occurrence_policy AS policy
     WHERE policy.self_person_ref=requested_self_person_ref
       AND policy.event_ref=requested_event_ref
     FOR UPDATE;

    IF FOUND THEN
        IF prior.placement_kind IS DISTINCT FROM requested_placement_kind
           OR prior.duration_minutes IS DISTINCT FROM requested_duration_minutes
           OR prior.duration_days IS DISTINCT FROM requested_duration_days
           OR prior.reminder_lead_minutes IS DISTINCT FROM requested_reminder_lead_minutes
        THEN
            RAISE EXCEPTION USING
                ERRCODE='23505',
                CONSTRAINT='pk_event_occurrence_policy',
                MESSAGE='Event occurrence policy already exists with different intent';
        END IF;
        RETURN QUERY
        SELECT prior.placement_kind,prior.duration_minutes,prior.duration_days,
               prior.reminder_lead_minutes,prior.created_at,true;
        RETURN;
    END IF;

    INSERT INTO dante.event_occurrence_policy(
        self_person_ref,event_ref,placement_kind,duration_minutes,duration_days,
        reminder_lead_minutes,created_at
    ) VALUES(
        requested_self_person_ref,requested_event_ref,requested_placement_kind,
        requested_duration_minutes,requested_duration_days,
        requested_reminder_lead_minutes,ts
    );

    RETURN QUERY
    SELECT requested_placement_kind,requested_duration_minutes,
           requested_duration_days,requested_reminder_lead_minutes,ts,false;
END
$$;
"""

GET_POLICY = r"""
CREATE FUNCTION dante.get_self_event_occurrence_policy(uuid,uuid)
RETURNS TABLE(
    placement_kind text,
    duration_minutes integer,
    duration_days integer,
    reminder_lead_minutes integer,
    created_at timestamptz
)
LANGUAGE sql SECURITY DEFINER STABLE PARALLEL SAFE
SET search_path=pg_catalog,dante,pg_temp AS $$
SELECT policy.placement_kind,policy.duration_minutes,policy.duration_days,
       policy.reminder_lead_minutes,policy.created_at
  FROM dante.event_occurrence_policy AS policy
  JOIN dante.event_expectation AS event
    ON event.event_ref=policy.event_ref
 WHERE policy.self_person_ref=$1
   AND policy.event_ref=$2
   AND event.self_person_ref=$1
$$;
"""
